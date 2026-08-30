#!/usr/bin/env python3
"""Fetch a LinkedIn profile photo via unavatar and store it under assets/students/.

Usage:
  python3 scripts/fetch_linkedin_photo.py --slug michelle-min --linkedin michelle-de-min

LinkedIn does not offer a stable public image API. This uses unavatar.io as a
convenience proxy. Prefer saving the official headshot yourself when you can.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", required=True, help="Filename stem, e.g. michelle-min")
    parser.add_argument("--linkedin", required=True, help="LinkedIn vanity slug")
    args = parser.parse_args()

    dest = ROOT / "assets" / "students" / f"{args.slug}.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://unavatar.io/linkedin/{args.linkedin}"
    subprocess.check_call(
        ["curl", "-fsSL", "-A", "Mozilla/5.0", "--max-time", "30", "-o", str(dest), url]
    )
    print(f"Wrote {dest.relative_to(ROOT)} from {url}")
    print("Update data/students.json photo path if needed, then rebuild if the HTML embeds it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
