#!/usr/bin/env python3
"""Upload, list and remove files in the ben-reels R2 bucket, inside the free tier.

    python3 scripts/r2.py usage                       # bytes stored vs the cap
    python3 scripts/r2.py ls [prefix]                 # list objects
    python3 scripts/r2.py put out.mp4 drafts/reels-v2-2026-10-05.mp4
    python3 scripts/r2.py put out.mp4 published/reels-v2-2026-10-05.mp4
    python3 scripts/r2.py rm drafts/reels-v2-2026-10-05.mp4

Keys go under drafts/ (deleted by the bucket after 30 days, never served) or
published/ (served by workers/reels-media; never overwritten, so a new render
gets a new dated name). A put is refused if it would take the bucket past
CAP_BYTES, which keeps storage under R2's 10 GB a month free tier.

Credentials come from ~/.config/r2/reels.env on Ben's Mac mini (R2_ACCOUNT_ID,
R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY), never from the repo. Signing is done
by curl's --aws-sigv4, so this needs only the standard library and curl.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

BUCKET = "ben-reels"
ENV_FILE = Path.home() / ".config" / "r2" / "reels.env"
CAP_BYTES = 8 * 10**9           # 80% of the 10 GB free tier
MAX_FILE_BYTES = 2 * 10**9      # one file; a reel MP4 is well under 200 MB
PREFIXES = ("drafts/", "published/")
PUBLIC_BASE = "https://reels-media.ben-b77.workers.dev/"
TYPES = {".mp4": "video/mp4", ".webm": "video/webm", ".webp": "image/webp", ".jpg": "image/jpeg",
         ".png": "image/png", ".json": "application/json", ".txt": "text/plain; charset=utf-8"}
NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"


def load_env() -> dict:
    if not ENV_FILE.exists():
        sys.exit(f"No credentials: {ENV_FILE} is missing. See 'Reels video storage' in README.md.")
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY"):
        if not env.get(k):
            sys.exit(f"{ENV_FILE} has no {k}.")
    return env


def curl(env: dict, args: list[str]) -> subprocess.CompletedProcess:
    """Run curl against the bucket. The keys go in a temporary config file, so
    they never appear in the process list."""
    exe = shutil.which("curl") or "/usr/bin/curl"
    with tempfile.NamedTemporaryFile("w", suffix=".curlrc", delete=True) as cfg:
        cfg.write(f'user = "{env["R2_ACCESS_KEY_ID"]}:{env["R2_SECRET_ACCESS_KEY"]}"\n')
        cfg.flush()
        os.chmod(cfg.name, 0o600)
        return subprocess.run([exe, "-sS", "--aws-sigv4", "aws:amz:auto:s3", "-K", cfg.name, *args],
                              capture_output=True, text=False)


def endpoint(env: dict, key: str = "") -> str:
    return f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com/{BUCKET}/{quote(key)}"


def list_objects(env: dict, prefix: str = "") -> list[dict]:
    out, token = [], None
    while True:
        q = f"?list-type=2&prefix={quote(prefix)}" + (f"&continuation-token={quote(token)}" if token else "")
        r = curl(env, ["-w", "\n%{http_code}", endpoint(env) + q])
        body, _, code = r.stdout.decode().rpartition("\n")
        if code != "200":
            sys.exit(f"List failed (HTTP {code}): {body[:300]}")
        root = ET.fromstring(body)
        for c in root.findall(f"{NS}Contents"):
            out.append({"key": c.findtext(f"{NS}Key"), "size": int(c.findtext(f"{NS}Size") or 0),
                        "modified": c.findtext(f"{NS}LastModified")})
        if root.findtext(f"{NS}IsTruncated") != "true":
            return out
        token = root.findtext(f"{NS}NextContinuationToken")


def used_bytes(env: dict) -> int:
    return sum(o["size"] for o in list_objects(env))


def exists(env: dict, key: str) -> bool:
    r = curl(env, ["-o", "/dev/null", "-w", "%{http_code}", "-I", endpoint(env, key)])
    return r.stdout.decode().strip() == "200"


def gb(n: int) -> str:
    return f"{n / 10**9:.2f} GB"


def cmd_usage(env: dict) -> None:
    used = used_bytes(env)
    print(f"{BUCKET}: {gb(used)} of the {gb(CAP_BYTES)} cap ({used / CAP_BYTES:.0%}); free tier is 10 GB")


def cmd_ls(env: dict, prefix: str = "") -> None:
    objs = list_objects(env, prefix)
    for o in objs:
        print(f"{o['size']:>14,}  {o['modified'][:19]}  {o['key']}")
    print(f"{len(objs)} objects, {gb(sum(o['size'] for o in objs))}")


def cmd_put(env: dict, path: str, key: str) -> None:
    src = Path(path)
    if not src.is_file():
        sys.exit(f"No such file: {src}")
    if not key.startswith(PREFIXES) or ".." in key:
        sys.exit(f"Key must start with one of {PREFIXES}: {key}")
    size = src.stat().st_size
    if size > MAX_FILE_BYTES:
        sys.exit(f"Refusing: {gb(size)} is over the {gb(MAX_FILE_BYTES)} per-file limit.")
    if key.startswith("published/") and exists(env, key):
        sys.exit(f"Refusing: {key} already exists. Published files are never overwritten; use a new dated name.")
    used = used_bytes(env)
    if used + size > CAP_BYTES:
        sys.exit(f"Refusing: {gb(used)} stored + {gb(size)} would pass the {gb(CAP_BYTES)} cap. "
                 "Remove old drafts first (python3 scripts/r2.py ls drafts/).")
    ctype = TYPES.get(src.suffix.lower(), "application/octet-stream")
    r = curl(env, ["-w", "%{http_code}", "-o", "/dev/null", "-X", "PUT", "-H", f"Content-Type: {ctype}",
                   "--upload-file", str(src), endpoint(env, key)])
    code = r.stdout.decode().strip()
    if code != "200":
        sys.exit(f"Upload failed (HTTP {code}): {r.stderr.decode()[:300]}")
    print(f"uploaded {key} ({gb(size)}); bucket now {gb(used + size)} of {gb(CAP_BYTES)}")
    if key.startswith("published/"):
        print("public URL:", PUBLIC_BASE + quote(key[len("published/"):]))


def cmd_rm(env: dict, key: str) -> None:
    r = curl(env, ["-w", "%{http_code}", "-o", "/dev/null", "-X", "DELETE", endpoint(env, key)])
    code = r.stdout.decode().strip()
    if code not in ("200", "204"):
        sys.exit(f"Delete failed (HTTP {code})")
    print("removed", key)


def main(argv: list[str]) -> None:
    cmds = {"usage": (cmd_usage, 0), "ls": (cmd_ls, None), "put": (cmd_put, 2), "rm": (cmd_rm, 1)}
    if not argv or argv[0] not in cmds:
        sys.exit(__doc__)
    fn, n = cmds[argv[0]]
    args = argv[1:]
    if n is not None and len(args) != n:
        sys.exit(__doc__)
    fn(load_env(), *args)


if __name__ == "__main__":
    main(sys.argv[1:])
