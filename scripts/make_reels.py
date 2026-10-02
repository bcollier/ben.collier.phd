#!/usr/bin/env python3
"""Build the two face reels on /reels/ from Ben's Apple Photos library.

    python3 scripts/make_reels.py              # writes assets/reels/ and data/reels.json
    python3 scripts/make_reels.py --dry-run    # prints the picks, writes nothing
    python3 scripts/make_reels.py --per-reel 150

Then run python3 scripts/build.py.

Everything runs on this Mac. The Photos library is opened read-only with
osxphotos; faces come from Photos and Apple Vision; the professional/casual
split uses Photos' own labels plus a local CLIP model. Nothing is uploaded.
Exported images carry no metadata at all, and data/reels.json holds only a
file path, size, and a coarse place for each photo.

Needs a Python with: osxphotos, open_clip_torch, torch, pillow, pillow-heif,
numpy, pyobjc-framework-Vision. The same library always gives the same reels.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import math
import os
import sys
from pathlib import Path

try:
    import numpy as np
    import osxphotos
    from PIL import Image, ImageOps
    import pillow_heif
    import Vision
    from Foundation import NSURL
except ImportError as e:  # pragma: no cover
    sys.exit(f"Missing dependency ({e.name}). Install: pip install osxphotos open_clip_torch torch pillow pillow-heif numpy pyobjc-framework-Vision")

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "reels"
DATA = ROOT / "data" / "reels.json"
CACHE = Path.home() / "Library" / "Caches" / "ben-reels"
ME = "Benjamin Collier"

REELS = {"pro": "Professional Ben", "casual": "Casual Ben"}
# Decisions from looking at the reels by eye, keyed by Photos UUID (which says
# nothing on its own): "skip" drops a photo, "pro"/"casual" moves it.
OVERRIDES = ROOT / "scripts" / "reels_overrides.json"
LONG_SIDE, THUMB_SIDE, MIN_CROP_H = 1600, 360, 1080
PLACE_MONTH_CAP = {"pro": 3, "casual": 2}  # professional photos cluster at work, so allow a few more

DROP_LABELS = {"Document", "Handwriting", "Receipt", "Screenshot", "Text", "Menu", "Printed Page", "Whiteboard"}
PRO_LABELS = {"Suit": 0.06, "Necktie": 0.06, "Formal Wear": 0.04, "Conference": 0.08, "Classroom": 0.08, "Stage": 0.06,
              "Office": 0.05, "Podium": 0.08, "Graduation": 0.08, "Academic Dress": 0.08, "Lecture": 0.08, "Presentation": 0.06}
CASUAL_LABELS = {"Outdoor": 0.03, "Beach": 0.05, "Hill": 0.03, "Mountain Range": 0.04, "Lake": 0.03, "Hiking": 0.06,
                 "Food": 0.04, "Meal": 0.04, "Recreation": 0.04, "Sport": 0.04, "Camping": 0.05, "Forest": 0.03,
                 "Wedding": 0.05, "Bride": 0.05, "Groom": 0.05, "Christmas Tree": 0.04}
PRO_PROMPTS = ["a man in a suit and tie", "a speaker giving a talk at a podium", "a professor teaching a class",
               "people at a business conference", "a university graduation ceremony", "a professional headshot of a man",
               "a man working in an office", "a man on a university campus"]
CASUAL_PROMPTS = ["a man hiking outdoors", "a man on a beach vacation", "a tourist in front of a landmark",
                  "a family day at the park", "a man eating at a restaurant", "a man playing a sport",
                  "a man camping in the woods", "a casual selfie on a trip"]
SCREEN_PROMPTS = ["a photo of a computer screen", "a screenshot of a phone", "a photo of a printed document"]
# Never in a reel: graphics and posters with text, and shirtless photos.
AVOID_PROMPTS = ["a graphic design poster with text", "a meme with a cartoon background", "a political campaign graphic",
                 "a shirtless man"]

# Coarse place names: well-known cities by name, otherwise state (US) or country.
CITIES = {"Pittsburgh", "San Francisco", "New York", "Chicago", "Washington", "Los Angeles", "Boston", "Philadelphia",
          "Madison", "Milwaukee", "Miami", "Las Vegas", "Seattle", "London", "Paris", "Rome", "Dublin", "Edinburgh",
          "Dubai", "Abu Dhabi", "Singapore", "Bangkok", "Istanbul", "Athens", "Venice", "Florence", "Munich",
          "Amsterdam", "Copenhagen", "Stockholm", "Reykjavik", "Sydney", "Melbourne", "Auckland", "Queenstown",
          "Kuala Lumpur", "Hong Kong", "Cancun", "Toronto"}
COUNTRY_FIX = {"Türkiye": "Turkey", "United Kingdom": "United Kingdom", "Holy See (Vatican City State)": "Vatican City"}
STATES = {"AL": "Alabama", "AZ": "Arizona", "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DC": "Washington",
          "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "IA": "Iowa", "IL": "Illinois", "IN": "Indiana",
          "KY": "Kentucky", "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
          "MO": "Missouri", "NC": "North Carolina", "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey",
          "NV": "Nevada", "NY": "New York", "OH": "Ohio", "PA": "Pennsylvania", "SC": "South Carolina", "TN": "Tennessee",
          "TX": "Texas", "VA": "Virginia", "VT": "Vermont", "WA": "Washington State", "WI": "Wisconsin", "WV": "West Virginia"}


# ---------------------------------------------------------------------------
# Places
# ---------------------------------------------------------------------------

_borrowed = {}


def learn_places(db):
    """Older cameras saved no location. For those photos, borrow the place of
    the nearest located photo in the library taken within 36 hours."""
    located = sorted((p.date.timestamp(), coarse_place(p, own=True)) for p in db.photos() if p.date and p.place)
    located = [x for x in located if x[1]]
    times = [x[0] for x in located]
    import bisect

    def guess(ts):
        i = bisect.bisect_left(times, ts)
        near = [located[j] for j in (i - 1, i) if 0 <= j < len(located)]
        near = [x for x in near if abs(x[0] - ts) <= 36 * 3600]
        return min(near, key=lambda x: abs(x[0] - ts))[1] if near else ""
    return guess


def coarse_place(p, own=False) -> str:
    if not own and p.uuid in _borrowed:
        return _borrowed[p.uuid]
    pl = p.place
    if pl is not None and pl.ishome:
        return "Pittsburgh"
    a = pl.address if pl is not None else None
    if a is None or not a.country:
        return ""
    country = COUNTRY_FIX.get(a.country, a.country)
    if a.country == "Qatar":
        return "Doha, Qatar"
    if a.city in CITIES and a.city != "Washington":
        return a.city if a.country == "United States" or a.city == country else f"{a.city}, {country}"
    if a.country == "United States":
        if a.city == "Washington" and a.state_province in ("DC", "District of Columbia"):
            return "Washington, D.C."
        return STATES.get(a.state_province or "", a.state_province or "United States")
    return country


# ---------------------------------------------------------------------------
# Images, faces, and quality
# ---------------------------------------------------------------------------

def source_path(p):
    for cand in (p.path_edited if p.hasadjustments else None, p.path):
        if cand and os.path.exists(cand):
            return cand
    return None


def preview_path(p):
    return next((x for x in (p.path_derivatives or []) if x and os.path.exists(x)), None)


def open_upright(path):
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def _small(im):
    return np.asarray(im.convert("L").resize((48, 48)), dtype=np.float32)


def open_original(p):
    """The full-size original, turned to match Photos' own rendered preview
    (some rotations live in the Photos database, not in the file)."""
    im = open_upright(source_path(p))
    prev = preview_path(p)
    if not prev:
        return im
    ref = _small(open_upright(prev))
    best = min((0, 90, 180, 270), key=lambda r: float(np.abs(_small(im.rotate(r, expand=True)) - ref).mean()))
    return im.rotate(best, expand=True) if best else im


def vision(im: Image.Image):
    """Apple Vision on the full image: face boxes, people (whole or upper body,
    which catches faces cut off at the edge and people turned away), and any
    text. Boxes are (x0, y0, x1, y1), normalized, y from the top."""
    tmp = CACHE / "_vision.jpg"
    big = im.copy()
    big.thumbnail((4032, 4032))
    big.save(tmp, "JPEG", quality=92)
    faces = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    people = Vision.VNDetectHumanRectanglesRequest.alloc().init()
    try:
        people.setUpperBodyOnly_(False)
    except Exception:
        pass
    text = Vision.VNRecognizeTextRequest.alloc().init()
    text.setRecognitionLevel_(0)
    h = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(str(tmp)), None)
    h.performRequests_error_([faces, people, text], None)
    box = lambda o: (o.boundingBox().origin.x, 1 - o.boundingBox().origin.y - o.boundingBox().size.height,
                     o.boundingBox().origin.x + o.boundingBox().size.width, 1 - o.boundingBox().origin.y)
    words = []
    for o in (text.results() or []):
        c = o.topCandidates_(1)
        if c and len(c):
            words.append(str(c[0].string()))
    rolls = {box(o): abs(float(o.roll() or 0)) * 57.3 for o in (faces.results() or []) if o.roll() is not None}
    return sorted(box(o) for o in (faces.results() or [])), sorted(box(o) for o in (people.results() or [])), words, rolls


ALONE_PROMPTS = ["a selfie of one man alone", "a photo of a single man by himself"]
MULTI_PROMPTS = ["a selfie of two people together", "a photo of a man and a woman", "a man holding a baby",
                 "a man with a child", "a couple hugging or kissing", "a group of friends",
                 "a photo of two people side by side"]
_clip = {}


def second_look(view: Image.Image):
    """A second, independent check on the exact frame that will be published:
    Vision's newer face model run on the crop, and a local CLIP vote on whether
    more than one person is in it. Catches turned faces, babies and kisses that
    the first pass misses. Returns a skip reason or None."""
    tmp = CACHE / "_view.jpg"
    view.save(tmp, "JPEG", quality=92)
    req = Vision.VNDetectFaceRectanglesRequest.alloc().init()
    try:
        req.setRevision_(3)
    except Exception:
        pass
    h = Vision.VNImageRequestHandler.alloc().initWithURL_options_(NSURL.fileURLWithPath_(str(tmp)), None)
    h.performRequests_error_([req], None)
    if len(req.results() or []) > 1:
        return "second face found in the final frame"
    import open_clip
    import torch
    if not _clip:
        model, _, prep = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
        model.eval()
        with torch.no_grad():
            t = model.encode_text(open_clip.get_tokenizer("ViT-B-32")(ALONE_PROMPTS + MULTI_PROMPTS))
        _clip.update(model=model, prep=prep, text=t / t.norm(dim=-1, keepdim=True))
    with torch.no_grad():
        e = _clip["model"].encode_image(_clip["prep"](view)[None])
        e = e / e.norm(dim=-1, keepdim=True)
        s = (100 * e @ _clip["text"].T).softmax(-1)[0]
    if float(s[len(ALONE_PROMPTS):].sum()) > 0.9:
        return "looks like more than one person"
    return None


def photos_faces(p):
    """Photos' face regions, normalized to the upright image (y flipped)."""
    out = []
    for f in p.face_info or []:
        if f.size <= 0.005:
            continue
        cx, cy, s = f.center_x, 1 - f.center_y, f.size
        out.append((f.name or "", (cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2), f.age_type))
    return out


def quality(im: Image.Image):
    g = np.asarray(im.convert("L").resize((512, max(1, round(512 * im.height / im.width)))), dtype=np.float32)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(g.mean()), float(lap.var())


def overlap(a, b):
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def grow(b, f, W, H):
    w, h = (b[2] - b[0]) * W, (b[3] - b[1]) * H
    return (b[0] * W - w * f, b[1] * H - h * f, b[2] * W + w * f, b[3] * H + h * f)


def find_crop(W, H, me, others):
    """Largest 4:5 or 16:9 frame (at least MIN_CROP_H tall) that keeps my face
    with room around it and touches no other face. None if there is none."""
    mine = grow(me, 0.9, W, H)
    bad = [grow(o, 0.2, W, H) for o in others]
    best = None
    for ar in (4 / 5, 16 / 9):
        h = min(H, W / ar)
        while h >= MIN_CROP_H:
            w = h * ar
            for fx in [i / 12 for i in range(13)]:
                x0 = min(max(0, mine[0] - fx * (w - (mine[2] - mine[0]))), W - w)
                for fy in [i / 8 for i in range(9)]:
                    y0 = min(max(0, mine[1] - fy * (h - (mine[3] - mine[1]))), H - h)
                    frame = (x0, y0, x0 + w, y0 + h)
                    if not (frame[0] <= mine[0] and frame[1] <= mine[1] and frame[2] >= mine[2] and frame[3] >= mine[3]):
                        continue
                    if any(overlap(frame, o) for o in bad):
                        continue
                    if (me[2] - me[0]) * W / w < 0.06:
                        continue
                    if best is None or w * h > best[2] * best[3]:
                        best = (x0, y0, w, h)
            h *= 0.9
    return best


# ---------------------------------------------------------------------------
# CLIP scores (cached per photo, so reruns are fast and stable)
# ---------------------------------------------------------------------------

def clip_scores(photos):
    cache_file = CACHE / "clip.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    cache = {k: v for k, v in cache.items() if len(v) == 4}
    todo = [p for p in photos if p.uuid not in cache and preview_path(p)]
    if todo:
        import open_clip
        import torch
        model, _, prep = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
        tok = open_clip.get_tokenizer("ViT-B-32")
        model.eval()
        prompts = PRO_PROMPTS + CASUAL_PROMPTS + SCREEN_PROMPTS + AVOID_PROMPTS
        with torch.no_grad():
            t = model.encode_text(tok(prompts))
            t = t / t.norm(dim=-1, keepdim=True)
            for i in range(0, len(todo), 32):
                batch = todo[i:i + 32]
                ims = torch.stack([prep(open_upright(preview_path(p))) for p in batch])
                e = model.encode_image(ims)
                e = e / e.norm(dim=-1, keepdim=True)
                sims = (e @ t.T).numpy()
                for p, s in zip(batch, sims):
                    a, b = len(PRO_PROMPTS), len(PRO_PROMPTS) + len(CASUAL_PROMPTS)
                    c = b + len(SCREEN_PROMPTS)
                    cache[p.uuid] = [round(float(s[:a].max()), 4), round(float(s[a:b].max()), 4),
                                     round(float(s[b:c].max()), 4), round(float(s[c:].max()), 4)]
                print(f"  CLIP {min(i + 32, len(todo))}/{len(todo)}", end="\r", flush=True)
        print()
        cache_file.write_text(json.dumps(cache))
    return cache


# ---------------------------------------------------------------------------
# Selection
# ---------------------------------------------------------------------------

def year_quotas(counts: dict, n: int) -> dict:
    """Spread n picks over years: proportional to sqrt(available), at least 1 each."""
    years = sorted(y for y, c in counts.items() if c)
    w = {y: math.sqrt(counts[y]) for y in years}
    tot = sum(w.values())
    raw = {y: max(1.0, n * w[y] / tot) for y in years}
    q = {y: min(counts[y], int(raw[y])) for y in years}
    rem = sorted(years, key=lambda y: (-(raw[y] - int(raw[y])), y))
    i = 0
    while sum(q.values()) < n and any(q[y] < counts[y] for y in years):
        y = rem[i % len(rem)]
        if q[y] < counts[y]:
            q[y] += 1
        i += 1
    return q


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--per-reel", type=int, default=150)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    skipped = collections.Counter()

    print("Reading the Photos library (read-only)...")
    db = osxphotos.PhotosDB()
    raw = [p for p in db.photos(persons=[ME]) if p.date and p.date.year >= 1990]
    cands = []
    for p in raw:
        if p.screenshot or p.ismovie or p.hidden:
            skipped["screenshot, video, or hidden"] += 1; continue
        if set(p.labels or []) & DROP_LABELS:
            skipped["document or screen"] += 1; continue
        if not source_path(p):
            skipped["original only in iCloud"] += 1; continue
        cands.append(p)

    # Bursts and series: keep the best photo from any run taken within a minute.
    cands.sort(key=lambda p: (p.date.timestamp(), p.uuid))
    best, groups, cur = [], [], []
    for p in cands:
        if cur and p.date.timestamp() - cur[0].date.timestamp() > 60:
            groups.append(cur); cur = []
        cur.append(p)
    if cur:
        groups.append(cur)
    for g in groups:
        g.sort(key=lambda p: (-(p.score.overall if p.score else 0), p.uuid))
        best.append(g[0])
        skipped["near-duplicate"] += len(g) - 1
    print(f"{len(raw)} photos of {ME}; {len(best)} after filters and duplicates.")
    guess = learn_places(db)
    for p in best:
        if not coarse_place(p, own=True):
            _borrowed[p.uuid] = guess(p.date.timestamp())

    print("Scoring scenes with a local CLIP model...")
    clip = clip_scores(best)

    over = json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    pool = {"pro": [], "casual": []}
    for p in best:
        if over.get(p.uuid) == "skip":
            skipped["removed on review"] += 1; continue
        s = clip.get(p.uuid)
        if not s:
            skipped["no preview"] += 1; continue
        pro, cas, scr, avoid = s
        if scr > max(pro, cas):
            skipped["photo of a screen or document"] += 1; continue
        if avoid > max(pro, cas) + 0.01:
            skipped["graphic, poster, or shirtless"] += 1; continue
        labels = set(p.labels or [])
        pro += sum(v for k, v in PRO_LABELS.items() if k in labels)
        cas += sum(v for k, v in CASUAL_LABELS.items() if k in labels)
        only_me = sum(1 for f in p.face_info or [] if f.size > 0.005) <= 1
        rank = max(pro, cas) + (0.03 if only_me else 0) + 0.02 * (p.score.overall if p.score else 0)
        # Professional means it really looks like work: a strong CLIP match, or
        # a solid one backed by Photos' own labels (suit, tie, conference...).
        backed = any(k in labels for k in PRO_LABELS)
        reel = "pro" if (pro > cas + 0.015 and pro > 0.235) or (backed and pro > cas and pro > 0.22) else "casual"
        reel = over.get(p.uuid, reel)
        pool[reel].append((round(rank, 4), p))

    print("pools:", {k: len(v) for k, v in pool.items()})
    picks, report = {}, {}
    for reel, items in pool.items():
        by_year = collections.defaultdict(list)
        for r, p in items:
            by_year[p.date.year].append((r, p))
        for y in by_year:
            by_year[y].sort(key=lambda t: (-t[0], t[1].uuid))
        quotas = year_quotas({y: len(v) for y, v in by_year.items()}, args.per_reel)
        chosen, place_month = [], collections.Counter()
        leftover = 0
        for y in sorted(by_year):
            got = 0
            for r, p in by_year[y]:
                if got >= quotas[y]:
                    break
                pm = (coarse_place(p), p.date.strftime("%Y-%m"))
                if place_month[pm] >= PLACE_MONTH_CAP[reel]:
                    continue
                frame = prepare(p, skipped)
                if frame is None:
                    continue
                if any(int((frame["hash"] != f["hash"]).sum()) < 10 for _, f in chosen):
                    skipped["looks like a photo already picked"] += 1
                    continue
                place_month[pm] += 1
                chosen.append((p, frame)); got += 1
            leftover += quotas[y] - got
        # Fill any shortfall from the strongest remaining photos in thin years first.
        if leftover:
            taken = {p.uuid for p, _ in chosen}
            rest = sorted(((r, p) for r, p in items if p.uuid not in taken), key=lambda t: (len([1 for c, _ in chosen if c.date.year == t[1].date.year]), -t[0], t[1].uuid))
            for r, p in rest:
                if leftover <= 0:
                    break
                pm = (coarse_place(p), p.date.strftime("%Y-%m"))
                if place_month[pm] >= PLACE_MONTH_CAP[reel]:
                    continue
                frame = prepare(p, skipped)
                if frame is None:
                    continue
                if any(int((frame["hash"] != f["hash"]).sum()) < 10 for _, f in chosen):
                    skipped["looks like a photo already picked"] += 1
                    continue
                place_month[pm] += 1
                chosen.append((p, frame)); leftover -= 1
        chosen.sort(key=lambda t: (t[0].date.timestamp(), t[0].uuid))
        picks[reel] = chosen
        report[reel] = {"years": collections.Counter(p.date.year for p, _ in chosen),
                        "places": collections.Counter(coarse_place(p) or "(no place)" for p, _ in chosen)}
        print(f"{REELS[reel]}: {len(chosen)} photos, {min(report[reel]['years'])} to {max(report[reel]['years'])}")

    if args.dry_run:
        for reel, chosen in picks.items():
            print(f"\n== {REELS[reel]}")
            for i, (p, fr) in enumerate(chosen, 1):
                print(f"{i:3}  {p.date:%Y-%m}  {coarse_place(p) or '-':24}  {'crop' if fr['crop'] else 'full'}  {p.uuid}")
        write_report(picks, report, skipped, dry=True)
        return

    export(picks)
    write_report(picks, report, skipped, dry=False)


_prepared = {}


def prepare(p, skipped):
    """Open the original, check quality, find my face, and choose a frame
    that holds no other face. Returns {"crop": (x0,y0,x1,y1)|None} or None."""
    if p.uuid in _prepared:
        return _prepared[p.uuid]
    res = None
    try:
        im = open_original(p)
    except Exception:
        skipped["could not open original"] += 1
        _prepared[p.uuid] = None
        return None
    W, H = im.size
    lum, sharp = quality(im)
    if lum < 45:
        skipped["too dark"] += 1
    elif sharp < 25:
        skipped["too blurry"] += 1
    elif min(W, H) < 480:
        skipped["too small"] += 1
    else:
        vis, bodies, words, rolls = vision(im)
        pf = photos_faces(p)
        mine = [b for n, b, _ in pf if n == ME]
        me = None
        if mine:
            cx, cy = (mine[0][0] + mine[0][2]) / 2, (mine[0][1] + mine[0][3]) / 2
            near = [v for v in vis if v[0] <= cx <= v[2] and v[1] <= cy <= v[3]]
            if near:
                me = near[0]
        import re as _re
        if me is None:
            skipped["could not locate my face"] += 1
        elif rolls.get(me, 0) > 55:
            skipped["sideways in the library"] += 1
        elif any(_re.fullmatch(r"\d{3,5}", w.strip()) for w in words):
            skipped["shows a house or street number"] += 1
        else:
            others = [v for v in vis if v is not me]
            others += [b for n, b, _ in pf if n != ME and not any(overlap(b, v) for v in vis)]
            # Other people's bodies, so a face cut off at the frame edge or a
            # child turned away cannot sneak in. Mine is the one holding my face.
            mx, my = (me[0] + me[2]) / 2, (me[1] + me[3]) / 2
            others += [b for b in bodies if not (b[0] <= mx <= b[2] and b[1] <= my <= b[3]) and (b[3] - b[1]) > 0.05]
            if not others and (me[2] - me[0]) >= 0.06:
                res = {"crop": None}
            elif not others:
                skipped["my face too small in the frame"] += 1
            else:
                c = find_crop(W, H, me, others)
                if c is None:
                    kid = any(n != ME and age in (1, 2) for n, _, age in pf)
                    skipped["other faces, child could not be cropped out" if kid else "other faces could not be cropped out"] += 1
                else:
                    res = {"crop": (c[0], c[1], c[0] + c[2], c[1] + c[3])}
    if res is not None:
        view = im.crop(tuple(round(v) for v in res["crop"])) if res["crop"] else im
        why = second_look(view.convert("RGB"))
        if why:
            skipped[why] += 1
            _prepared[p.uuid] = None
            return None
        g = np.asarray(view.convert("L").resize((9, 8)), dtype=np.float32)
        res["hash"] = (g[:, 1:] > g[:, :-1]).flatten()
    _prepared[p.uuid] = res
    return res


def clean_copy(im: Image.Image) -> Image.Image:
    """A pixel-only copy: no EXIF, XMP, ICC, or any other metadata."""
    out = Image.new("RGB", im.size)
    out.paste(im)
    return out


def export(picks):
    data = {"generated_by": "scripts/make_reels.py", "reels": []}
    manifest = {}
    for reel, chosen in picks.items():
        folder = OUT / reel
        folder.mkdir(parents=True, exist_ok=True)
        for f in folder.glob("*.webp"):
            f.unlink()
        items = []
        for i, (p, fr) in enumerate(chosen, 1):
            im = open_original(p)
            if fr["crop"]:
                im = im.crop(tuple(round(v) for v in fr["crop"]))
            im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
            im = clean_copy(im)
            name = f"{i:03d}"
            im.save(folder / f"{name}.webp", "WEBP", quality=80, method=6)
            th = im.copy()
            th.thumbnail((THUMB_SIDE, THUMB_SIDE), Image.LANCZOS)
            th.save(folder / f"{name}-t.webp", "WEBP", quality=72, method=6)
            items.append({"src": f"assets/reels/{reel}/{name}.webp", "w": im.width, "h": im.height, "place": coarse_place(p)})
            manifest[f"{reel}/{name}"] = p.uuid
            print(f"  {REELS[reel]} {i}/{len(chosen)}", end="\r", flush=True)
        print()
        data["reels"].append({"id": reel, "title": REELS[reel], "items": items})
    music = OUT / "music.json"
    if music.exists():
        data["music"] = json.loads(music.read_text())
    DATA.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    (CACHE / "manifest.json").write_text(json.dumps(manifest, indent=1))  # private: which photo each file came from
    print(f"wrote {DATA.relative_to(ROOT)} and assets/reels/")


def write_report(picks, report, skipped, dry):
    lines = [f"# Reels report{' (dry run)' if dry else ''}", ""]
    for reel, r in report.items():
        lines += [f"## {REELS[reel]}: {len(picks[reel])} photos", "", "By year: " + ", ".join(f"{y}: {c}" for y, c in sorted(r["years"].items())),
                  "", f"Places ({len(r['places'])}): " + ", ".join(f"{k} {v}" for k, v in r["places"].most_common()), ""]
    lines += ["## Skipped", ""] + [f"- {k}: {v}" for k, v in skipped.most_common()]
    path = CACHE / "report.md"
    path.write_text("\n".join(lines) + "\n")
    print(f"private report: {path}")


if __name__ == "__main__":
    main()
