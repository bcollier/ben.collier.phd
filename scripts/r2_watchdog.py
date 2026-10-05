#!/usr/bin/env python3
"""Daily check that the reels R2 bucket stays inside Cloudflare's free tier.

    python3 scripts/r2_watchdog.py            # check, and switch the Worker off if needed
    python3 scripts/r2_watchdog.py --dry-run  # check only

Reads this month's R2 operations from Cloudflare's analytics API and the bytes
stored from the bucket itself. If any of them reaches 80% of its free amount,
it turns off https://reels-media.ben-b77.workers.dev, so nobody can read the
videos (and run up Class B reads) until Ben looks at it. Redeploying the
Worker turns the address back on. Cloudflare's own e-mail alerts at the same
thresholds tell Ben; this script is the part that actually stops the reads.

Runs once a day on Ben's Mac mini from scripts/launchd/phd.collier.r2-watchdog.plist.
Credentials: ~/.config/r2/reels.env (CLOUDFLARE_API_TOKEN, R2_ACCOUNT_ID, and the
R2 keys used by scripts/r2.py). Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2  # noqa: E402

WORKER = "reels-media"
TRIP = 0.8
FREE = {"storage_bytes": 10 * 10**9, "class_a": 1_000_000, "class_b": 10_000_000}
# How Cloudflare bills each R2 action. Deletes and aborts are free.
CLASS_A = {"ListBuckets", "PutBucket", "ListObjects", "PutObject", "CopyObject", "CompleteMultipartUpload",
           "CreateMultipartUpload", "LifecycleStorageTierTransition", "ListMultipartUploads", "UploadPart",
           "UploadPartCopy", "ListParts", "PutBucketEncryption", "PutBucketCors", "PutBucketLifecycleConfiguration"}
FREE_OPS = {"DeleteObject", "DeleteObjects", "DeleteBucket", "AbortMultipartUpload"}
API = "https://api.cloudflare.com/client/v4"


def call(env: dict, method: str, url: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {env['CLOUDFLARE_API_TOKEN']}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def operations(env: dict, start: dt.date, end: dt.date) -> tuple[int, int, dict]:
    q = """query($a: String!, $s: Date!, $e: Date!) { viewer { accounts(filter: {accountTag: $a}) {
             r2OperationsAdaptiveGroups(limit: 1000, filter: {date_geq: $s, date_leq: $e}) {
               sum { requests } dimensions { actionType } } } } }"""
    d = call(env, "POST", f"{API}/graphql", {"query": q, "variables": {
        "a": env["R2_ACCOUNT_ID"], "s": start.isoformat(), "e": end.isoformat()}})
    if d.get("errors"):
        raise RuntimeError(f"analytics query failed: {d['errors']}")
    by_type: dict[str, int] = {}
    for g in d["data"]["viewer"]["accounts"][0]["r2OperationsAdaptiveGroups"]:
        t = g["dimensions"]["actionType"]
        by_type[t] = by_type.get(t, 0) + g["sum"]["requests"]
    a = sum(n for t, n in by_type.items() if t in CLASS_A)
    # Anything else that is not free counts as Class B, so an unknown new action errs on the safe side.
    b = sum(n for t, n in by_type.items() if t not in CLASS_A and t not in FREE_OPS)
    return a, b, by_type


def switch_off(env: dict) -> None:
    d = call(env, "POST", f"{API}/accounts/{env['R2_ACCOUNT_ID']}/workers/scripts/{WORKER}/subdomain",
             {"enabled": False, "previews_enabled": False})
    if not d.get("success"):
        raise RuntimeError(f"could not switch off {WORKER}: {d.get('errors')}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="report only; never switch the Worker off")
    args = ap.parse_args()
    env = r2.load_env()
    if not env.get("CLOUDFLARE_API_TOKEN"):
        sys.exit(f"{r2.ENV_FILE} has no CLOUDFLARE_API_TOKEN.")
    today = dt.datetime.now(dt.timezone.utc).date()
    a, b, by_type = operations(env, today.replace(day=1), today)
    stored = r2.used_bytes(env)
    use = {"storage_bytes": stored, "class_a": a, "class_b": b}
    stamp = dt.datetime.now().isoformat(timespec="seconds")
    over = []
    for k, v in use.items():
        share = v / FREE[k]
        print(f"{stamp}  {k:<13} {v:>14,} of {FREE[k]:>14,} free  ({share:.1%})")
        if share >= TRIP:
            over.append(k)
    if not over:
        print(f"{stamp}  ok: everything under {TRIP:.0%} of the free tier")
        return 0
    print(f"{stamp}  OVER {TRIP:.0%}: {', '.join(over)}  (actions this month: {by_type})")
    if args.dry_run:
        print(f"{stamp}  dry run: would switch off {WORKER}")
        return 2
    switch_off(env)
    print(f"{stamp}  switched off https://{WORKER}.ben-b77.workers.dev; redeploy the Worker to turn it back on")
    return 2


if __name__ == "__main__":
    sys.exit(main())
