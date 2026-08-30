#!/usr/bin/env python3
"""Append a LinkedIn post to data/linkedin.json.

LinkedIn has no public RSS API. This script stores a static copy so shout-outs
keep working on GitHub Pages and collier.phd.

Usage:
  python3 scripts/add_linkedin_post.py \\
    --url 'https://www.linkedin.com/posts/...' \\
    --date 2026-08-30 \\
    --text 'Proud of ...' \\
    --people 'Ada Lovelace' 'Grace Hopper' \\
    --tags students teaching
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "linkedin.json"


def activity_id(url: str) -> str:
    match = re.search(r"activity-(\d+)", url)
    if match:
        return match.group(1)
    match = re.search(r"(\d{15,})", url)
    return match.group(1) if match else url.rstrip("/").split("/")[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Add a LinkedIn post to the faculty site.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--text", required=True, help="The post text, or a short excerpt.")
    parser.add_argument("--people", nargs="*", default=[], help="Students or collaborators named in the post.")
    parser.add_argument("--tags", nargs="*", default=["students"], help="Use 'students' for the students page.")
    args = parser.parse_args()

    payload = json.loads(DATA.read_text(encoding="utf-8"))
    posts = payload.setdefault("posts", [])
    post_id = activity_id(args.url)
    posts = [p for p in posts if p.get("id") != post_id]
    posts.insert(
        0,
        {
            "id": post_id,
            "date": args.date,
            "url": args.url,
            "tags": args.tags,
            "people": args.people,
            "text": args.text.strip(),
        },
    )
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    payload["posts"] = posts
    payload["updated"] = date.today().isoformat()
    DATA.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {DATA.relative_to(ROOT)} ({len(posts)} posts). Rebuild is not required; the page reads this JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
