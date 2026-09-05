#!/usr/bin/env python3
"""Render assets/og.png, the 1200x630 card LinkedIn and X show when the site is shared.

  python3 scripts/make_og_image.py

Writes assets/og.svg (source) and rasterises it to assets/og.png. Rasterising
needs rsvg-convert (brew install librsvg); the committed PNG means nobody has to
install it just to build the site.
"""

from __future__ import annotations

import base64
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
PAPER, INK, SOFT, ACCENT = "#f3efe6", "#1b1714", "#5c564e", "#c24e16"


def svg() -> str:
    portrait = base64.b64encode((ROOT / "assets" / "portrait.jpg").read_bytes()).decode()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="round"><circle cx="948" cy="315" r="186"/></clipPath>
  </defs>
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <rect x="0" y="0" width="{W}" height="14" fill="{ACCENT}"/>
  <image xlink:href="data:image/jpeg;base64,{portrait}" x="762" y="129" width="372" height="372"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#round)"/>
  <circle cx="948" cy="315" r="186" fill="none" stroke="{INK}" stroke-opacity="0.14" stroke-width="2"/>
  <text x="86" y="196" font-family="Georgia, 'Times New Roman', serif" font-size="26"
        letter-spacing="4.2" fill="{SOFT}">ASSISTANT TEACHING PROFESSOR</text>
  <text x="86" y="304" font-family="Georgia, 'Times New Roman', serif" font-size="94"
        font-weight="bold" fill="{INK}">Ben Collier</text>
  <text x="86" y="374" font-family="Helvetica, Arial, sans-serif" font-size="31" fill="{SOFT}">Business Analytics · Tepper School of Business</text>
  <text x="86" y="418" font-family="Helvetica, Arial, sans-serif" font-size="31" fill="{SOFT}">Carnegie Mellon University</text>
  <rect x="86" y="468" width="72" height="4" fill="{ACCENT}"/>
  <text x="86" y="534" font-family="Helvetica, Arial, sans-serif" font-size="29" fill="{INK}">Courses, students, and applied work</text>
</svg>
"""


def main() -> int:
    src = ROOT / "assets" / "og.svg"
    out = ROOT / "assets" / "og.png"
    src.write_text(svg(), encoding="utf-8")
    print(f"wrote assets/{src.name}")
    if not shutil.which("rsvg-convert"):
        print("rsvg-convert not found; assets/og.png left as-is. brew install librsvg")
        return 0
    subprocess.check_call(
        ["rsvg-convert", "-w", str(W), "-h", str(H), "-o", str(out), str(src)]
    )
    print(f"wrote assets/{out.name} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
