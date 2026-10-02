#!/usr/bin/env python3
"""Direct version 2 of the reels: a music video cut to the beat.

Version 2 reuses the exact photos version 1 published (data/reels.json and
assets/reels/), plus already-public place photos from assets/travel/ as
b-roll (listed in scripts/reels_v2_broll.json). It finds nothing new in the
Photos library and sends nothing anywhere.

What it does, on Ben's Mac:
  1. Finds the face in each reel photo with Apple Vision, so the player can
     crop and zoom toward it.
  2. Measures the music: tempo, beat phase, and where the drops are.
  3. Lays out every shot on that beat grid, section by section.
  4. Writes data/reels_v2.json, which js/reels-v2.js plays.

    python scripts/make_reels_v2.py --music path/to/track.mp3   # first time
    python scripts/make_reels_v2.py                              # reuse assets/reels/v2-music.mp3

Needs numpy, pillow, imageio-ffmpeg and pyobjc-framework-Vision.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REELS = ROOT / "data" / "reels.json"
TRAVEL = ROOT / "data" / "travel.json"
BROLL = ROOT / "scripts" / "reels_v2_broll.json"
OUT = ROOT / "data" / "reels_v2.json"
MUSIC = ROOT / "assets" / "reels" / "v2-music.mp3"
MUSIC_META = ROOT / "assets" / "reels" / "v2-music.json"


# ---------------------------------------------------------------------------
# Faces
# ---------------------------------------------------------------------------

def face_box(path: Path):
    """The largest face Vision finds, as (cx, cy, size) in 0..1 with y from
    the top. Falls back to the upper middle of the frame."""
    import Vision
    from Foundation import NSURL
    req = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    h = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(str(path)), None)
    h.performRequests_error_([req], None)
    best = None
    for o in req.results() or []:
        b = o.boundingBox()
        if best is None or b.size.width > best.size.width:
            best = b
    if best is None:
        return 0.5, 0.38, 0.0
    return (round(best.origin.x + best.size.width / 2, 3),
            round(1 - best.origin.y - best.size.height / 2, 3),
            round(best.size.width, 3))


def detail(path: Path):
    """How busy a photo is, and where: the mean edge strength, and the centre of
    its busiest patch. The kaleidoscope folds that patch."""
    g = np.asarray(Image.open(path).convert("L").resize((64, 64)), dtype=np.float32)
    e = np.abs(np.diff(g, axis=0))[:, :-1] + np.abs(np.diff(g, axis=1))[:-1, :]
    blocks = e[:56, :56].reshape(7, 8, 7, 8).mean((1, 3))
    by, bx = np.unravel_index(np.argmax(blocks), blocks.shape)
    return float(e.mean()), (round((bx + 0.5) / 7, 3), round((by + 0.5) / 7, 3))


def luminance(path: Path) -> float:
    return float(np.asarray(Image.open(path).convert("L").resize((32, 32))).mean() / 255)


# ---------------------------------------------------------------------------
# Music
# ---------------------------------------------------------------------------

def decode(path: Path, sr: int = 22050):
    import imageio_ffmpeg
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "quiet", "-i", str(path), "-ac", "1",
                          "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, sr


def beat_grid(path: Path):
    """Tempo and first beat from the kick drum's onsets (30 to 150 Hz)."""
    y, sr = decode(path)
    hop, n = 128, 1024
    fps = sr / hop
    frames = np.lib.stride_tricks.sliding_window_view(y, n)[::hop] * np.hanning(n)
    spec = np.abs(np.fft.rfft(frames, axis=1))[:, 1:8]
    flux = np.r_[0, np.maximum(0, np.diff(np.log1p(spec * 10), axis=0)).sum(1)]
    flux = (flux - flux.mean()) / flux.std()
    best = (-1e9, 120.0, 0.0)
    for bpm in np.arange(80, 180, 0.05):
        per = 60 * fps / bpm
        for o in np.arange(0, per, 0.5):
            s = flux[np.round(np.arange(o, len(flux) - 1, per)).astype(int)].mean()
            if s > best[0]:
                best = (s, bpm, o)
    _, bpm, o = best
    return round(float(bpm), 3), round(float(o / fps), 4), round(len(y) / sr, 3)


def encode_music(src: Path):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "quiet", "-y", "-i", str(src), "-map_metadata", "-1",
                    "-map", "0:a", "-af", "loudnorm=I=-15:TP=-1.5", "-b:a", "128k", "-ar", "44100", str(MUSIC)], check=True)


# ---------------------------------------------------------------------------
# The edit
# ---------------------------------------------------------------------------
# Beat indices for "High Technologic Beat Explosion" at 140 BPM. Bars start on
# beats 2, 6, 10, ... The first drop lands on beat 126, the breakdown on 286,
# the rebuild on 318, the second drop on 350 and the outro on 446.
SECTIONS = {"cold": 0, "title": 18, "broll": 34, "pro": 82, "drop1": 126, "breakdown": 286,
            "rebuild": 318, "drop2": 350, "outro": 446}

# One letter per bar (4 beats). See bar() for what each does.
DROP1 = "HSGBHPKX" * 4 + "HSGBHPK"
BREAKDOWN = "bccbcccc"
REBUILD = "ssssHHHR"
DROP2 = "GhHPGhKh" * 2 + "GhHPGhK"

# Colour grades, cycled per bar: pink and cyan, gold and violet, the honmoon.
GRADES = [["#ff2d95", "#22e6ff"], ["#ffd23f", "#7b2cff"], ["#ff5ec4", "#3df2c2"], ["#ff3b3b", "#ffe14d"],
          ["#9b5cff", "#00e5ff"]]


class Director:
    def __init__(self, bpm, t0, casual, broll):
        self.per = 60 / bpm
        self.t0 = t0
        self.casual = list(casual)
        self.broll = list(broll)
        self.ci = 0
        self.bi = 0
        self.ki = 0
        self.shots = []
        self.busy = []
        self.bars = 0

    def t(self, beat: float) -> float:
        return round(self.t0 + beat * self.per, 3)

    def shot(self, b0, b1, kind, imgs=(), **kw):
        s = {"t": self.t(b0), "d": round(self.t(b1) - self.t(b0), 3), "k": kind}
        if imgs:
            s["i"] = list(imgs)
        s.update({k: v for k, v in kw.items() if v not in (None, "", [])})
        self.shots.append(s)

    def next_c(self):
        i = self.casual[self.ci]
        self.ci += 1
        return i

    def next_b(self):
        i = self.broll[self.bi % len(self.broll)]
        self.bi += 1
        return i

    def kaleido_b(self):
        # The kaleidoscope reuses the busiest places, which fold best.
        i = self.busy[self.ki % len(self.busy)]
        self.ki += 1
        return i

    def bar(self, code, b):
        g = GRADES[self.bars % len(GRADES)]
        self.bars += 1
        if code == "H":    # four hits, one photo a beat, zoom punch and colour split
            for j in range(4):
                self.shot(b + j, b + j + 1, "photo", [self.next_c()], fx="punch rgb", g=g)
        elif code == "h":  # two photos, two beats each, punched on every beat
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "photo", [self.next_c()], fx="punch rgb beat", g=g)
        elif code == "S":  # two photos framed over their own glow, slow push
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "photo", [self.next_c()], fx="frame push duo", g=g)
        elif code == "G":  # 2x2 idol grid, one cell lands per beat
            self.shot(b, b + 4, "grid", [self.next_c() for _ in range(4)], g=g)
        elif code == "B":  # b-roll, neon grade, place chip
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "photo", [self.next_b()], fx="push duo neon", g=g)
        elif code == "P":  # triple panels in three colours
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "panels", [self.next_c()], g=g)
        elif code == "K":  # kaleidoscope of a place
            self.shot(b, b + 4, "kaleido", [self.kaleido_b()], g=g)
        elif code == "X":  # glitch bar
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "photo", [self.next_c()], fx="glitch rgb beat", g=g)
        elif code == "b":  # breakdown: one place, slow, soft
            self.shot(b, b + 4, "photo", [self.next_b()], fx="push soft fadein", g=g)
        elif code == "c":  # breakdown: one photo, slow, soft
            self.shot(b, b + 4, "photo", [self.next_c()], fx="frame push soft fadein", g=g)
        elif code == "s":
            for j in (0, 2):
                self.shot(b + j, b + j + 2, "photo", [self.next_c()], fx="frame push duo", g=g)
        elif code == "R":  # riser into a drop: fast cuts, then white
            for j in (0, 1, 2):
                self.shot(b + j, b + j + 1, "photo", [self.next_c()], fx="punch rgb riser", g=g)
            self.shot(b + 3, b + 4, "photo", [self.casual[self.ci - 1]], fx="riser whiteout", g=g)
        else:
            raise ValueError(code)

    def bars_run(self, start, codes):
        for k, code in enumerate(codes):
            self.bar(code, start + 4 * k)


def slots(codes: str) -> int:
    per = {"H": 4, "h": 2, "S": 2, "G": 4, "B": 0, "P": 2, "K": 0, "X": 2, "b": 0, "c": 1, "s": 2, "R": 3}
    return sum(per[c] for c in codes)


def fit(need):
    """Adjust the bar patterns until every casual photo is used exactly once:
    trade four-hit bars for two-hit bars (2 fewer photos each), last section
    first, then swap a breakdown photo for a place if one is left over."""
    parts = [list(DROP1), list(BREAKDOWN), list(REBUILD), list(DROP2)]
    total = lambda: 2 + sum(slots("".join(q)) for q in parts)  # 2: the photos under the drop titles
    order = [3, 2, 0]
    while total() - need >= 2:
        q = next((q for q in order if "H" in parts[q]), None)
        if q is None:
            break
        k = len(parts[q]) - 1 - parts[q][::-1].index("H")
        parts[q][k] = "h"
    while need - total() >= 2:
        q = next((q for q in order[::-1] if "h" in parts[q]), None)
        if q is None:
            break
        parts[q][parts[q].index("h")] = "H"
    if total() - need == 1 and "c" in parts[1]:
        parts[1][len(parts[1]) - 1 - parts[1][::-1].index("c")] = "b"
    elif need - total() == 1 and "b" in parts[1]:
        parts[1][parts[1].index("b")] = "c"
    return ["".join(q) for q in parts] + [total()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--music", type=Path, help="source track to encode as assets/reels/v2-music.mp3")
    args = ap.parse_args()
    if args.music:
        encode_music(args.music)
    if not MUSIC.exists():
        raise SystemExit("no assets/reels/v2-music.mp3; pass --music")

    reels = {r["id"]: r for r in json.loads(REELS.read_text())["reels"]}
    places = {}
    # Place photos are labelled by country, or by state inside the US, the same
    # coarse level as the reel photos.
    states = {"AL": "Alabama", "CA": "California", "DC": "Washington, D.C.", "DE": "Delaware", "FL": "Florida",
              "IA": "Iowa", "IL": "Illinois", "IN": "Indiana", "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine",
              "MI": "Michigan", "MN": "Minnesota", "NC": "North Carolina", "NE": "Nebraska", "NH": "New Hampshire",
              "NJ": "New Jersey", "NV": "Nevada", "NY": "New York", "OH": "Ohio", "PA": "Pennsylvania",
              "VA": "Virginia", "WI": "Wisconsin", "WV": "West Virginia"}
    big = {"New York": "New York City", "San Francisco": "San Francisco", "Pittsburgh": "Pittsburgh",
           "Las Vegas": "Las Vegas", "Philadelphia": "Philadelphia", "Washington": "Washington, D.C.", "Miami": "Miami"}
    for c in json.loads(TRAVEL.read_text())["countries"]:
        for p in c.get("photos", []):
            places[p["src"]] = c["name"] if c["cc"] != "US" else ""
        for city in c.get("cities", []):
            for p in city.get("photos", []):
                places[p["src"]] = big.get(city["name"]) or states.get(city["state"], city["state"])
    broll_src = json.loads(BROLL.read_text())["broll"]

    imgs, ids = [], {}

    def add(src, w, h, place, kind):
        p = ROOT / src
        cx, cy, fs = face_box(p) if kind != "b" else (0.5, 0.45, 0.0)
        thumb = src.replace(".webp", "-t.webp")
        ids[src] = len(imgs)
        imgs.append({"src": src, "t": thumb if (ROOT / thumb).exists() else src, "w": w, "h": h,
                     "f": [cx, cy, fs], "p": place, "r": kind})
        return ids[src]

    pro = [add(i["src"], i["w"], i["h"], i["place"], "p") for i in reels["pro"]["items"]]
    cas = [add(i["src"], i["w"], i["h"], i["place"], "c") for i in reels["casual"]["items"]]
    rolls, busy = [], []
    for src in broll_src:
        with Image.open(ROOT / src) as im:
            w, h = im.size
        i = add(src, w, h, places.get(src, ""), "b")
        score, (bx, by) = detail(ROOT / src)
        imgs[i]["f"] = [bx, by, 0.0]
        rolls.append((luminance(ROOT / src), i))
        busy.append((score, i))
    # Day first, then dusk, then night, so the b-roll run walks into the dark
    # before the professional section. The rest are saved for later sections.
    rolls_sorted = [i for _, i in sorted(rolls, key=lambda x: -x[0])]
    intro_broll = rolls_sorted[::2][:24]
    later_broll = [i for i in rolls_sorted if i not in intro_broll]

    bpm, t0, dur = beat_grid(MUSIC)
    d1, bd, rb, d2, n = fit(len(cas))
    if n != len(cas):
        raise SystemExit(f"could not fit {len(cas)} casual photos into the edit ({n} slots)")

    D = Director(bpm, t0, cas, later_broll)
    D.busy = [i for _, i in sorted(busy, reverse=True)][:12]
    S = SECTIONS
    # Cold open: the seal draws itself, then the title.
    D.shot(0, S["title"], "sigil", text="")
    D.shot(S["title"], S["broll"], "title", text="BEN COLLIER", sub="2000 to 2026", fx="glitchin")
    # B-roll: 24 places, two beats each.
    for k, i in enumerate(intro_broll):
        b = S["broll"] + 2 * k
        D.shot(b, b + 2, "photo", [i], fx="push duo neon" + (" rgb" if k % 4 == 3 else ""), g=GRADES[k // 2 % len(GRADES)])
    # Professional Ben: title, then 29 photos speeding up into the drop.
    D.shot(S["pro"], S["pro"] + 4, "title", [pro[0]], text="PROFESSIONAL BEN", fx="slam")
    b = S["pro"] + 4
    for k, i in enumerate(pro):
        if k < 11:
            L = 2
        elif k < len(pro) - 2:
            L = 1
        elif k == len(pro) - 2:
            L = 0.5
        else:
            L = S["drop1"] - b
        fx = ("frame push duo" if k < 11 else "punch rgb") + (" riser whiteout" if k == len(pro) - 1 else "")
        D.shot(b, b + L, "photo", [i], fx=fx, g=GRADES[k // 4 % len(GRADES)])
        b += L
    # Drop one: title slam over the first casual photo, then the bar pattern.
    D.shot(S["drop1"], S["drop1"] + 4, "title", [D.next_c()], text="CASUAL BEN", fx="slam drop")
    D.bars_run(S["drop1"] + 4, d1)
    D.bars_run(S["breakdown"], bd)
    D.bars_run(S["rebuild"], rb)
    D.shot(S["drop2"], S["drop2"] + 4, "title", [D.next_c()], text="STILL BEN", fx="slam drop")
    D.bars_run(S["drop2"] + 4, d2)
    end_beat = int((dur - t0) / D.per)
    D.shot(S["outro"], S["outro"] + 32, "mosaic", pro + cas)
    D.shot(S["outro"] + 32, end_beat, "end", pro + cas, text="BEN COLLIER, PhD",
           sub=f"{len(pro) + len(cas)} photos · {len({imgs[i]['p'] for i in pro + cas if imgs[i]['p']})} places · 2000 to 2026")
    assert D.ci == len(cas), (D.ci, len(cas))

    meta = json.loads(MUSIC_META.read_text()) if MUSIC_META.exists() else {}
    out = {"generated_by": "scripts/make_reels_v2.py", "bpm": bpm, "t0": t0, "dur": dur,
           "drops": [D.t(S["drop1"]), D.t(S["drop2"])],
           "calm": [[D.t(S["cold"]), D.t(S["broll"])], [D.t(S["breakdown"]), D.t(S["rebuild"])]],
           "music": meta, "img": imgs, "shots": D.shots}
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print(f"{bpm} BPM, first beat {t0}s, {dur}s; {len(D.shots)} shots; "
          f"{len(pro)} pro, {len(cas)} casual, {len(broll_src)} b-roll; bars {d1} | {bd} | {rb} | {d2}")


if __name__ == "__main__":
    main()
