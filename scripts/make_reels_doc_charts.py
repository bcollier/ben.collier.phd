#!/usr/bin/env python3
"""Draw the two charts in docs/reels-pipeline.md from the published reels data.

    python3 scripts/make_reels_doc_charts.py

Writes docs/reels/edit-timeline.svg (every shot of version 2 on the song's
timeline) and docs/reels/places.svg (how many version 1 photos come from each
place). Standard library only; reads data/reels.json and data/reels_v2.json.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "reels"
INK, INK2, PAPER, GRID, RED, BLUE = "#1d2633", "#4a5463", "#fbf8f1", "#d9d2c3", "#b8352a", "#2447a6"
FONT = "font-family='IBM Plex Mono, ui-monospace, monospace'"

# Section starts in beats, as directed in scripts/make_reels_v2.py.
SECTIONS = [("open", 0), ("title", 18), ("places", 34), ("pro", 82), ("drop 1: casual", 126),
            ("breakdown", 286), ("rebuild", 318), ("drop 2", 350), ("mosaic + end", 446)]
KINDS = ["sigil", "title", "photo", "grid", "panels", "kaleido", "mosaic", "end"]
KIND_LABEL = {"sigil": "seal", "title": "title card", "photo": "single photo", "grid": "2x2 grid",
              "panels": "triple panels", "kaleido": "kaleidoscope", "mosaic": "mosaic", "end": "end card"}


def timeline(v2: dict) -> str:
    per, t0, dur = 60 / v2["bpm"], v2["t0"], v2["dur"]
    W, L, R, T = 1200, 130, 20, 70
    row = 26
    H = T + row * len(KINDS) + 60
    X = lambda t: L + (t / dur) * (W - L - R)
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'>",
           f"<rect width='{W}' height='{H}' fill='{PAPER}'/>",
           f"<text x='{L}' y='22' {FONT} font-size='13' fill='{INK}' font-weight='600'>Version 2: every shot on the song's timeline "
           f"({len(v2['shots'])} shots, {v2['bpm']:.0f} BPM, {int(dur // 60)}:{int(dur % 60):02d})</text>"]
    # section bands
    starts = [(name, t0 + b * per) for name, b in SECTIONS] + [("", dur)]
    for k, (name, s) in enumerate(starts[:-1]):
        e = starts[k + 1][1]
        fill = "#f1ebdd" if k % 2 == 0 else PAPER
        out.append(f"<rect x='{X(s):.1f}' y='{T - 26}' width='{X(e) - X(s):.1f}' height='{row * len(KINDS) + 26}' fill='{fill}'/>")
        out.append(f"<text x='{X(s) + 3:.1f}' y='{T - 12}' {FONT} font-size='10' fill='{INK2}'>{escape(name)}</text>")
    # rows
    for i, k in enumerate(KINDS):
        y = T + i * row
        out.append(f"<line x1='{L}' x2='{W - R}' y1='{y + row:.1f}' y2='{y + row:.1f}' stroke='{GRID}' stroke-width='1'/>")
        out.append(f"<text x='{L - 8}' y='{y + row / 2 + 4:.1f}' {FONT} font-size='11' fill='{INK}' text-anchor='end'>{KIND_LABEL[k]}</text>")
    for s in v2["shots"]:
        i = KINDS.index(s["k"]) if s["k"] in KINDS else 2
        y = T + i * row + 5
        g = (s.get("g") or [BLUE])[0]
        x0, x1 = X(s["t"]), X(s["t"] + s["d"])
        out.append(f"<rect x='{x0:.1f}' y='{y}' width='{max(1.2, x1 - x0 - 0.6):.1f}' height='{row - 10}' rx='2' fill='{g}'/>")
    # drops
    for d in v2["drops"]:
        out.append(f"<line x1='{X(d):.1f}' x2='{X(d):.1f}' y1='{T - 26}' y2='{T + row * len(KINDS)}' stroke='{RED}' stroke-width='2'/>")
        out.append(f"<text x='{X(d) + 4:.1f}' y='{T + row * len(KINDS) + 16}' {FONT} font-size='10' fill='{RED}'>drop {int(d // 60)}:{int(d % 60):02d}</text>")
    # time axis
    for sec in range(0, int(dur) + 1, 30):
        out.append(f"<text x='{X(sec):.1f}' y='{H - 10}' {FONT} font-size='10' fill='{INK2}' text-anchor='middle'>{sec // 60}:{sec % 60:02d}</text>")
    out.append("</svg>")
    return "\n".join(out)


def places(v1: dict) -> str:
    rows = []
    for r in v1["reels"]:
        for it in r["items"]:
            rows.append((r.get("id", ""), it.get("place") or "no location"))
    c = Counter(p for _, p in rows)
    top = c.most_common(16)
    W, L, R, T, rh = 760, 190, 60, 40, 22
    H = T + rh * len(top) + 30
    mx = max(n for _, n in top)
    X = lambda n: L + n / mx * (W - L - R)  # zero baseline at L
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'>",
           f"<rect width='{W}' height='{H}' fill='{PAPER}'/>",
           f"<text x='{L}' y='22' {FONT} font-size='13' fill='{INK}' font-weight='600'>Version 1: photos per place ({len(rows)} photos, {len(c)} labels; top {len(top)})</text>",
           f"<line x1='{L}' x2='{L}' y1='{T - 4}' y2='{T + rh * len(top)}' stroke='{INK}' stroke-width='1.5'/>"]
    for i, (p, n) in enumerate(top):
        y = T + i * rh
        out.append(f"<text x='{L - 8}' y='{y + 15}' {FONT} font-size='11' fill='{INK}' text-anchor='end'>{escape(p)}</text>")
        out.append(f"<rect x='{L}' y='{y + 4}' width='{X(n) - L:.1f}' height='{rh - 8}' rx='2' fill='{BLUE}'/>")
        out.append(f"<text x='{X(n) + 6:.1f}' y='{y + 15}' {FONT} font-size='11' fill='{INK2}'>{n}</text>")
    out.append(f"<text x='{L}' y='{H - 8}' {FONT} font-size='10' fill='{INK2}'>0</text>")
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    v1 = json.loads((ROOT / "data" / "reels.json").read_text())
    v2 = json.loads((ROOT / "data" / "reels_v2.json").read_text())
    (OUT / "edit-timeline.svg").write_text(timeline(v2))
    (OUT / "places.svg").write_text(places(v1))
    print("wrote docs/reels/edit-timeline.svg and docs/reels/places.svg")


if __name__ == "__main__":
    main()
