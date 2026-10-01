"""Original diagrams for advised projects, drawn as inline SVG at build time.

Each project in data/advising.json names an `art` key. The drawing depicts the
idea of the project, never its data or deliverables: nothing here comes from
the students' work. Each drawing is taped onto the advising page like a print.
"""

from __future__ import annotations

import math
import random

W, H = 320, 180
INK = "251,248,242"
WARM = "240,169,127"
TINTS = {
    "forecast": "#2f4a43", "decision": "#3d4c5c", "experiment": "#243652",
    "cabinet": "#6e2f3a", "vol": "#2a2420", "bids": "#8a4b28", "segments": "#243652",
    "drift": "#3d4c5c", "ab": "#4d5a3c", "personas": "#2a2420", "textnet": "#6e2f3a",
    "routes": "#4d5a3c", "survey": "#8f5334",
}


def ink(a: float) -> str:
    return f"rgba({INK},{a})"


def warm(a: float) -> str:
    return f"rgba({WARM},{a})"


def label(x, y, text, size=10, anchor="start", alpha=0.6, mono=True):
    fam = "ui-monospace, Menlo, monospace" if mono else "'Source Sans 3', system-ui, sans-serif"
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'fill="{ink(alpha)}" text-anchor="{anchor}">{text}</text>')


def poly(points, stroke, width=1.5, fill="none", dash=None):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{extra}/>'


def forecast(r):
    out = [label(16, 22, "price forecast to 2038")]
    x0, x1 = 20, 300
    for k, (base, drift, col) in enumerate([(130, -1.6, ink(0.55)), (120, -2.4, warm(0.95)), (150, -0.9, ink(0.35))]):
        pts, y = [], base
        for i in range(29):
            x = x0 + i * (x1 - x0) / 28
            y += drift + r.uniform(-4, 4) * (1 if i < 14 else 0.35)
            pts.append((x, max(34, y)))
        out.append(poly(pts[:15], col, 1.8))
        out.append(poly(pts[14:], col, 1.8, dash="4 3"))
    out.append(f'<line x1="160" y1="30" x2="160" y2="160" stroke="{ink(0.25)}" stroke-dasharray="2 3"/>')
    out.append(label(164, 166, "today", 9, alpha=0.5))
    return out


def decision(r):
    out = []
    nodes = [(40, 90, "gate"), (130, 55, "build"), (130, 125, "stop"), (230, 35, "+NPV"), (230, 80, "-NPV"), (230, 125, "")]
    edges = [(0, 1, True), (0, 2, False), (1, 3, True), (1, 4, False)]
    for a, b, good in edges:
        (xa, ya, _), (xb, yb, _) = nodes[a], nodes[b]
        out.append(f'<line x1="{xa+18}" y1="{ya}" x2="{xb-18}" y2="{yb}" stroke="{warm(0.9) if good else ink(0.35)}" stroke-width="{2 if good else 1.2}"/>')
    for i, (x, y, t) in enumerate(nodes[:5]):
        shape = (f'<rect x="{x-18}" y="{y-11}" width="36" height="22" rx="4"' if i else f'<polygon points="{x-18},{y} {x},{y-16} {x+18},{y} {x},{y+16}"')
        out.append(shape + f' fill="{warm(0.25) if i in (1, 3) else ink(0.08)}" stroke="{ink(0.6)}"/>')
        out.append(label(x, y + 3.5, t, 9, "middle", 0.85))
    out.append(label(300, 166, "81 scenarios", 10, "end"))
    return out


def experiment(r):
    out = [label(16, 22, "randomized: dashboard vs AI")]
    for k, (x, t) in enumerate([(40, "dashboard"), (185, "ask in words")]):
        out.append(f'<rect x="{x}" y="38" width="100" height="84" rx="5" fill="{ink(0.06)}" stroke="{ink(0.45)}"/>')
        if k == 0:
            for i, h in enumerate([30, 48, 22, 40, 56]):
                out.append(f'<rect x="{x+10+i*17}" y="{112-h}" width="11" height="{h}" fill="{ink(0.5)}"/>')
        else:
            for i, w in enumerate([70, 52, 78, 40]):
                col = warm(0.8) if i % 2 else ink(0.45)
                out.append(f'<rect x="{x + (22 if i % 2 else 8)}" y="{48+i*17}" width="{w}" height="10" rx="5" fill="{col}"/>')
        out.append(label(x + 50, 138, t, 10, "middle"))
    for i in range(14):
        cx = 20 + i * 21
        out.append(f'<circle cx="{cx}" cy="160" r="4" fill="{warm(0.9) if i % 2 else ink(0.7)}"/>')
    return out


def cabinet(r):
    out = [label(16, 22, "par level vs demand")]
    for row in range(3):
        for col in range(5):
            x, y = 22 + col * 58, 34 + row * 44
            fill = r.random()
            low = fill < 0.22
            out.append(f'<rect x="{x}" y="{y}" width="50" height="36" rx="3" fill="{ink(0.05)}" stroke="{warm(0.9) if low else ink(0.4)}" stroke-width="{2 if low else 1}"/>')
            out.append(f'<rect x="{x+4}" y="{y+32-28*fill:.1f}" width="42" height="{28*fill:.1f}" fill="{warm(0.85) if low else ink(0.45)}"/>')
            out.append(f'<line x1="{x+2}" y1="{y+14}" x2="{x+48}" y2="{y+14}" stroke="{ink(0.7)}" stroke-dasharray="2 2"/>')
    return out


def vol(r):
    out = [label(16, 22, "implied volatility smile")]
    xs = [20 + i * 7 for i in range(41)]
    before = [(x, 128 - 0.13 * ((x - 160) / 7) ** 2) for x in xs]
    after = [(x, 150 - 0.06 * ((x - 160) / 7) ** 2) for x in xs]
    out.append(poly(before, warm(0.95), 2.2))
    out.append(poly(after, ink(0.5), 1.6, dash="4 3"))
    out.append(label(300, 52, "before earnings", 9, "end"))
    out.append(label(160, 170, "after: the crush", 9, "middle"))
    out.append(label(24, 170, "strike", 9, alpha=0.4))
    return out


def bids(r):
    out = [label(16, 22, "unit price vs the low bid")]
    out.append(f'<line x1="20" y1="120" x2="300" y2="60" stroke="{warm(0.9)}" stroke-width="2"/>')
    for i in range(70):
        x = r.uniform(24, 296)
        base = 120 - (x - 20) * 60 / 280
        y = base + abs(r.gauss(0, 14)) * (1 if r.random() < 0.85 else -0.3)
        mine = i % 9 == 0
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.2 if mine else 2.2}" fill="{warm(1) if mine else ink(0.55)}"/>')
    out.append(label(300, 170, "750,000 line items", 9, "end"))
    return out


def segments(r):
    out = [label(16, 22, "two generations, two messages")]
    for cx, cy, col in [(95, 95, ink(0.75)), (225, 95, warm(0.95))]:
        for _ in range(38):
            out.append(f'<circle cx="{cx + r.gauss(0, 20):.1f}" cy="{cy + r.gauss(0, 18):.1f}" r="2.4" fill="{col}"/>')
    out.append(f'<path d="M 125 70 C 160 45, 175 45, 200 70" fill="none" stroke="{ink(0.6)}" stroke-width="1.5" marker-end="url(#arr)"/>')
    out.append(label(95, 150, "passing it on", 10, "middle"))
    out.append(label(225, 150, "receiving it", 10, "middle"))
    return out


def drift(r):
    out = [label(16, 22, "a portfolio leaving its style")]
    out.append(f'<rect x="20" y="70" width="280" height="44" fill="{ink(0.08)}"/>')
    for k in range(6):
        pts, y = [], 92 + r.uniform(-8, 8)
        for i in range(29):
            y += r.uniform(-2, 2)
            y = max(74, min(110, y))
            pts.append((20 + i * 10, y))
        out.append(poly(pts, ink(0.45), 1.2))
    pts, y = [], 90
    for i in range(29):
        y += r.uniform(-1.5, 1.5) - (1.9 if i > 15 else 0)
        pts.append((20 + i * 10, y))
    out.append(poly(pts, warm(0.95), 2.2))
    out.append(f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]:.1f}" r="4" fill="{warm(1)}"/>')
    out.append(label(300, 166, "flag before it happens", 9, "end"))
    return out


def ab(r):
    out = [label(16, 22, "14-day vs 30-day trial")]
    for i, (name, start, enough) in enumerate([("14 days", 0.70, 0.65), ("30 days", 0.71, 0.80)]):
        y = 50 + i * 55
        out.append(label(20, y + 4, name, 10, alpha=0.8))
        out.append(f'<rect x="80" y="{y-8}" width="{start*200:.1f}" height="12" fill="{ink(0.4)}"/>')
        out.append(f'<rect x="80" y="{y+8}" width="{enough*200:.1f}" height="12" fill="{warm(0.9) if i else ink(0.7)}"/>')
    out.append(label(80, 166, "would start / had time to decide", 9, alpha=0.5))
    return out


def personas(r):
    out = [f'<rect x="90" y="30" width="200" height="130" rx="6" fill="{ink(0.06)}" stroke="{ink(0.45)}"/>',
           f'<line x1="90" y1="46" x2="290" y2="46" stroke="{ink(0.35)}"/>']
    for i in range(3):
        out.append(f'<circle cx="{100+i*9}" cy="38" r="2.5" fill="{ink(0.5)}"/>')
    for i, w in enumerate([150, 110, 170, 90]):
        out.append(f'<rect x="104" y="{58+i*18}" width="{w}" height="8" rx="4" fill="{ink(0.3)}"/>')
    for i in range(5):
        y = 38 + i * 26
        out.append(f'<circle cx="40" cy="{y}" r="9" fill="{warm(0.85) if i == 2 else ink(0.55)}"/>')
        out.append(f'<line x1="50" y1="{y}" x2="88" y2="{70 + i * 12}" stroke="{ink(0.25)}"/>')
        for s in range(5):
            out.append(f'<circle cx="{58+s*6}" cy="{y+12}" r="1.8" fill="{warm(0.9) if s < 3 + (i % 3) else ink(0.25)}"/>')
    return out


def textnet(r):
    out = [label(16, 22, "text confirms the image model")]
    for i in range(7):
        y = 38 + i * 16
        x = 20
        for j in range(r.randint(4, 7)):
            w = r.randint(14, 34)
            hot = r.random() < 0.13
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="2" fill="{warm(0.9) if hot else ink(0.35)}"/>')
            x += w + 5
            if x > 190:
                break
    out.append(f'<rect x="228" y="52" width="70" height="70" rx="6" fill="{ink(0.06)}" stroke="{ink(0.5)}"/>')
    out.append(f'<path d="M 245 90 l 10 10 l 22 -24" fill="none" stroke="{warm(1)}" stroke-width="3"/>')
    out.append(label(263, 140, "two checks", 9, "middle"))
    return out


def routes(r):
    out = [label(16, 22, "rescues at risk of going unclaimed")]
    pts = [(r.uniform(30, 290), r.uniform(40, 160)) for _ in range(22)]
    for i in range(0, 20, 2):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        out.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{ink(0.3)}" stroke-dasharray="3 3"/>')
    for i, (x, y) in enumerate(pts):
        risky = i % 5 == 0
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{5 if risky else 3.5}" fill="{"none" if risky else ink(0.7)}" stroke="{warm(1) if risky else "none"}" stroke-width="2"/>')
    return out


def survey(r):
    out = [label(16, 22, "who would install it?")]
    rows = [("18-24", 0.45), ("25-34", 0.88), ("35-44", 0.72), ("45-54", 0.30), ("55+", 0.15)]
    for i, (age, v) in enumerate(rows):
        y = 40 + i * 24
        out.append(label(20, y + 10, age, 10, alpha=0.75))
        out.append(f'<rect x="70" y="{y}" width="{v*220:.1f}" height="14" fill="{warm(0.9) if age in ("25-34", "35-44") else ink(0.45)}"/>')
    out.append(label(300, 170, "EN / 中文 survey", 9, "end"))
    return out


ART = {f.__name__: f for f in (forecast, decision, experiment, cabinet, vol, bids, segments, drift, ab, personas, textnet, routes, survey)}


def draw(key: str, alt: str, seed: int = 0) -> str:
    r = random.Random(f"{key}-{seed}")
    body = "\n  ".join(ART[key](r))
    bg = TINTS.get(key, "#2a2420")
    return (
        f'<svg class="advising-art" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}" xmlns="http://www.w3.org/2000/svg">\n'
        f'  <defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{ink(0.6)}"/></marker></defs>\n'
        f'  <rect width="{W}" height="{H}" fill="{bg}"/>\n  {body}\n</svg>'
    )
