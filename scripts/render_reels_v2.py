#!/usr/bin/env python3
"""Render reels version 2 to a video file, and its poster frames.

The browser player draws every frame from the song time alone, so this opens
/reels/?capture in headless Chrome, asks for each frame in turn, and pipes the
screenshots into ffmpeg with the music. Nothing is uploaded anywhere.

    python3 -m http.server 8822 &                      # serve the repo
    python scripts/render_reels_v2.py --posters        # assets/reels/v2-poster*.webp
    python scripts/render_reels_v2.py --video out.mp4  # 1280x720, 30 fps

The video is not committed (too big for the repo). Store it in R2 with
scripts/r2.py (drafts/ or published/); see README, "Video storage".
Needs playwright (with Chrome), pillow and imageio-ffmpeg.
"""
from __future__ import annotations

import argparse
import asyncio
import io
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
URL = "http://localhost:8822/reels/?capture"
POSTER_T = 11.6  # the title over the seal


async def open_page(p, w, h):
    b = await p.chromium.launch(channel="chrome", args=["--ignore-gpu-blocklist"])
    pg = await b.new_page(viewport={"width": w, "height": h})
    await pg.goto(URL, wait_until="networkidle")
    await pg.evaluate("window.__reelsV2.fonts()")
    return b, pg


async def shot(pg, t, fmt="png", quality=None):
    await pg.evaluate(f"window.__reelsV2.frame({t})")
    return await pg.screenshot(type=fmt, quality=quality)


async def posters():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        for (w, h), name in (((1600, 900), "v2-poster.webp"), ((960, 1200), "v2-poster-tall.webp")):
            b, pg = await open_page(p, w, h)
            im = Image.open(io.BytesIO(await shot(pg, POSTER_T))).convert("RGB")
            clean = Image.new("RGB", im.size)
            clean.paste(im)
            clean.save(ROOT / "assets" / "reels" / name, "WEBP", quality=82, method=6)
            await b.close()
            print("wrote", name)


async def video(out: Path, fps: int, w: int, h: int, start: float, end: float | None):
    import imageio_ffmpeg
    from playwright.async_api import async_playwright
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    music = ROOT / "assets" / "reels" / "v2-music.mp3"
    async with async_playwright() as p:
        b, pg = await open_page(p, w, h)
        dur = await pg.evaluate("window.__reelsV2.dur")
        end = min(end or dur, dur)
        n = int((end - start) * fps)
        proc = subprocess.Popen([ff, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
                                 "-ss", str(start), "-t", str(end - start), "-i", str(music),
                                 "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                                 "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                                 "-map_metadata", "-1", str(out)], stdin=subprocess.PIPE)
        for k in range(n):
            proc.stdin.write(await shot(pg, start + k / fps, "jpeg", 92))
            if k % (fps * 10) == 0:
                print(f"  {start + k / fps:6.1f}s / {end:.1f}s", flush=True)
        proc.stdin.close()
        proc.wait()
        await b.close()
    print("wrote", out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--posters", action="store_true")
    ap.add_argument("--video", type=Path)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--end", type=float)
    a = ap.parse_args()
    if a.posters:
        asyncio.run(posters())
    if a.video:
        w, h = (int(x) for x in a.size.split("x"))
        asyncio.run(video(a.video, a.fps, w, h, a.start, a.end))


if __name__ == "__main__":
    main()
