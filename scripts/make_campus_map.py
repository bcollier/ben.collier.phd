#!/usr/bin/env python3
"""Draw assets/campus/campus-map.svg from an OpenStreetMap extract of the CMU campus.

Not part of the build: run it once when the map needs redrawing.

  curl https://overpass.kumi.systems/api/interpreter --data-urlencode \
    'data=[out:json];(way["building"](40.4405,-79.9500,40.4475,-79.9390);way["highway"](40.4405,-79.9500,40.4475,-79.9390););out geom tags;' -o osm.json
  python3 scripts/make_campus_map.py osm.json

Map data (c) OpenStreetMap contributors, ODbL.
"""
import json
import math
import sys
from pathlib import Path

TEPPER_WAY = 583510520  # OSM way for the Tepper School of Business (Tepper Quad)
LAT0, LON0 = 40.4447, -79.9450  # frame centre: Tepper Quad slightly above centre, Forbes Ave in view
W, H, SCALE = 520, 340, 105000  # svg units per degree of latitude
LABELS = {"Gates and Hillman Centers": "Gates", "Cohon University Center": "Cohon Center", "Hunt Library": "Hunt Library",
          "Hamerschlag Hall": "Hamerschlag", "Posner Hall": "Posner", "Baker Hall": "Baker", "Wean Hall": "Wean",
          "Doherty Hall": "Doherty", "Software Engineering Institute": "SEI"}


def main(src):
    els = json.loads(Path(src).read_text())["elements"]
    kx = math.cos(math.radians(LAT0))

    def P(la, lo):
        return ((lo - LON0) * kx * SCALE + W / 2, (LAT0 - la) * SCALE + H / 2)

    def path(geom, close):
        pts = [P(g["lat"], g["lon"]) for g in geom]
        if not any(-40 < x < W + 40 and -40 < y < H + 40 for x, y in pts):
            return None
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + ("Z" if close else "")

    def centre(geom):
        pts = [P(g["lat"], g["lon"]) for g in geom]
        return sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)

    roads, blds, labels, tepper, tc = [], [], [], None, None
    for e in els:
        t, g = e.get("tags", {}), e.get("geometry")
        if not g:
            continue
        if "highway" in t:
            hw = t["highway"]
            cls = "walk" if hw in ("footway", "path", "steps", "service", "pedestrian", "cycleway", "corridor") else \
                  "major" if hw in ("primary", "secondary", "tertiary", "trunk") else "minor"
            p = path(g, False)
            if p:
                roads.append((cls, p))
        elif "building" in t:
            p = path(g, True)
            if not p:
                continue
            if e["id"] == TEPPER_WAY:
                tepper, tc = p, centre(g)
                continue
            blds.append(p)
            if t.get("name") in LABELS:
                x, y = centre(g)
                if 40 < x < W - 40 and 12 < y < H - 8:
                    labels.append((LABELS[t["name"]], x, y))
    forbes = sorted(P(g["lat"], g["lon"]) for e in els if e.get("tags", {}).get("name") == "Forbes Avenue" for g in e["geometry"])
    forbes = [p for p in forbes if 30 < p[0] < W - 90 and 10 < p[1] < H - 10]

    order = {"walk": 0, "minor": 1, "major": 2}
    out = [f'<svg class="campus-map" viewBox="0 0 {W} {H}" role="img" aria-label="Map of the Carnegie Mellon campus with Tepper Quad highlighted on Forbes Avenue">',
           '<rect class="cm-bg" width="100%" height="100%"/><g class="cm-roads">']
    out += [f'<path class="cm-{c}" d="{p}"/>' for c, p in sorted(roads, key=lambda r: order[r[0]])]
    out.append('</g><g class="cm-bld">')
    out += [f'<path d="{p}" style="--d:{(i % 23) * 18}ms"/>' for i, p in enumerate(blds)]
    out.append(f'</g><path class="cm-tepper" d="{tepper}"/>')
    out += [f'<text class="cm-label" x="{x:.0f}" y="{y:.0f}">{n}</text>' for n, x, y in labels]
    if forbes:
        x, y = forbes[len(forbes) // 5]
        out.append(f'<text class="cm-street" x="{x:.0f}" y="{y - 6:.0f}">Forbes Ave</text>')
    tag_x = -140 if tc[0] > W - 150 else 14
    out.append(f'<g class="cm-pin" transform="translate({tc[0]:.1f},{tc[1]:.1f})"><circle class="cm-ring" r="10"/><circle class="cm-dot" r="5"/>'
               f'<g class="cm-tag" transform="translate({tag_x},-44)"><rect width="128" height="38" rx="4"/>'
               '<text x="9" y="16" class="cm-t1">Tepper Quad</text><text x="9" y="30" class="cm-t2">Office 5135, fifth floor</text></g></g>')
    out.append('<text class="cm-credit" x="514" y="334" text-anchor="end">© OpenStreetMap contributors</text></svg>')
    dest = Path(__file__).resolve().parent.parent / "assets" / "campus" / "campus-map.svg"
    dest.write_text("".join(out), encoding="utf-8")
    print(f"wrote {dest.name}: {len(blds)} buildings, {len(roads)} paths, Tepper at {tc[0]:.0f},{tc[1]:.0f}")


if __name__ == "__main__":
    main(sys.argv[1])
