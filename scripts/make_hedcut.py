#!/usr/bin/env python3
"""Draw assets/portrait-hedcut.png, a stippled ink version of my cartoon avatar in the
spirit of a newspaper hedcut. The header shows it small, and the home page
morphs the colour portrait into it on scroll.

Needs Pillow and numpy (unlike build.py, which is standard library only):

    python3 -m pip install pillow numpy
    python3 scripts/make_hedcut.py

The output is committed, so a normal build does not need to rerun this.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
# The flat cartoon avatar stipples more cleanly than the notebook-ink portrait (its graph paper and
# highlighter turn into noise), so the hedcut is drawn from it.
SRC = ROOT / "assets" / "avatars" / "flat-vector.webp"
OUT = ROOT / "assets" / "portrait-hedcut.png"

SIZE = 360          # output pixels; shown at 10rem at most, so this is 2x+
SUPER = 4           # supersampling factor for smooth dots
SPACING = 2.7       # dot grid pitch at output size
INK = (27, 23, 20)  # --ink


def subject_mask(img: Image.Image) -> np.ndarray:
    """1 on the person, 0 on the background, soft at the edge. The office
    behind is teal and out of focus, so a colour test finds it; a head and
    shoulders shape keeps the pillars behind from leaking in."""
    rgb = np.asarray(img.resize((SIZE, SIZE), Image.LANCZOS), dtype=np.float32)
    teal = (rgb[..., 1] > rgb[..., 0] + 8) & (rgb[..., 2] > rgb[..., 0] + 5)
    y, x = np.mgrid[0:SIZE, 0:SIZE] / (SIZE - 1)
    head = ((x - 0.5) / 0.215) ** 2 + ((y - 0.34) / 0.3) ** 2 < 1
    body = y > 0.6 + 0.5 * np.clip(np.abs(x - 0.5) - 0.12, 0, None)
    shirt = (y > 0.58) & (np.abs(x - 0.5) < 0.18)  # light blue, reads as teal
    fg = ((~teal) | shirt) & (head | body)
    m = Image.fromarray((fg * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7))
    m = m.filter(ImageFilter.GaussianBlur(3))
    return np.asarray(m, dtype=np.float32) / 255.0


def tone(img: Image.Image) -> np.ndarray:
    """Darkness 0..1 per output pixel. Highlights drop to paper, the way a
    hedcut leaves the lit side of a face almost bare, and edges get a line."""
    g = ImageOps.grayscale(img).resize((SIZE, SIZE), Image.LANCZOS)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = g.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=2))
    a = np.asarray(g, dtype=np.float32) / 255.0
    dark = np.clip((1.0 - a - 0.34) / 0.6, 0, 1) ** 1.35
    edges = np.asarray(g.filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    dark = np.clip(dark + 0.7 * np.clip(edges * 1.6 - 0.08, 0, 1), 0, 1)
    return dark * subject_mask(img)


def stipple(dark: np.ndarray) -> Image.Image:
    big = SIZE * SUPER
    canvas = Image.new("LA", (big, big), (0, 0))
    draw = ImageDraw.Draw(canvas)
    rng = np.random.default_rng(7)
    pitch = SPACING
    rows = int(SIZE / (pitch * 0.866)) + 2
    for j in range(rows):
        cy = j * pitch * 0.866
        offset = (pitch / 2) if j % 2 else 0
        cx = offset
        while cx < SIZE + pitch:
            jx, jy = rng.uniform(-0.18, 0.18, 2) * pitch
            px, py = cx + jx, cy + jy
            ix, iy = int(min(max(px, 0), SIZE - 1)), int(min(max(py, 0), SIZE - 1))
            d = float(dark[iy, ix])
            if d > 0.04:
                rad = 0.58 * pitch * np.sqrt(d) * SUPER
                bx, by = px * SUPER, py * SUPER
                draw.ellipse((bx - rad, by - rad, bx + rad, by + rad), fill=(0, 255))
            cx += pitch
    alpha = canvas.getchannel("A").resize((SIZE, SIZE), Image.LANCZOS)
    out = Image.new("RGBA", (SIZE, SIZE), INK + (0,))
    out.putalpha(alpha)
    return out


def main():
    img = Image.open(SRC).convert("RGB")
    stipple(tone(img)).save(OUT, optimize=True)
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
