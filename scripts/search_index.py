"""Build the site search index from the pages the build just wrote.

The index is made from the rendered HTML, not from the data files, so search
can only ever find what a visitor can already read on the page. Each page is
cut into records at its headings (and at project cards and news items, which
carry their own ids): one record per page intro and one per section, each with
a URL that jumps to that section.

Left out on purpose: the header, footer and sheet fields, scripts, drawings,
evaluation quotes and letters (the quote cards and blockquotes), and the
e-mail address. Facts the HTML does not spell out in one place (course
numbers, project tools, dates) come in from build.py as `meta`.

Standard library only, like the rest of the build.
"""

from __future__ import annotations

import json
import re
from html import unescape
from html.parser import HTMLParser

# Where a record files in the search results.
KINDS = {
    "course": "Courses",
    "project": "Coding with AI projects",
    "app": "Apps coded with AI",
    "talk": "Talks",
    "news": "News",
    "cv": "CV",
    "page": "Pages",
}

# Subtrees that never reach the index.
SKIP_TAGS = {"script", "style", "svg", "noscript", "template", "button", "select", "textarea",
             "blockquote", "q", "header", "footer", "form", "canvas", "video", "audio", "iframe"}
SKIP_CLASSES = {"sheet-head", "ev-quote", "ev-quotes", "ev-note", "ev-letter", "ev-env", "ev-from",
                "ev-postmark", "eml", "sec-no", "tape", "stack", "skip", "wk-has", "bar-val",
                "quote-stage", "cluster-quotes"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HEADINGS = {"h1", "h2", "h3"}
INLINE = {"a", "em", "strong", "b", "i", "mark", "abbr", "code", "small", "sup", "sub", "u", "s", "cite", "kbd"}

BODY_CHARS = 420      # text kept verbatim, for snippets
STOP = set("""a an and are as at be been but by for from had has have he her his i if in into is it its
me my of on or our she so than that the their them then there these they this to was we were what when
where which who will with you your about after also all any can did do does how just more most no not
now only other out over same some such through up very while would one two three four five six seven
eight nine ten first every own before across using why keep real short versus page hover each like make
made get got many much way""".split())


def stem(w: str) -> str:
    """The same light plural folding js/search.js applies to every word."""
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        return w[:-1]
    return w

KEEP_NUMBER = re.compile(r"^(?:\d{5}|(?:19|20)\d{2})$")   # course numbers (70445) and years
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\b\w+ \[at\] [\w.]+\b")
DATE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|"
                  r"Spring|Summer|Fall|Winter)(?: \d{1,2},)? \d{4}\b")


def norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


class Record:
    def __init__(self, anchor: str, level: int):
        self.anchor = anchor
        self.level = level
        self.title = ""
        self.headings: list[str] = []
        self.text: list[str] = []
        self.extra: list[str] = []   # image descriptions: searchable, never shown
        self.kicker = ""
        self.date = ""
        self.container = False

    def body(self) -> str:
        # text arrives in pieces split at tags; close the gaps before punctuation
        return re.sub(r"\s+([.,;:!?)])", r"\1", norm_space("".join(self.text)))


class PageParser(HTMLParser):
    """Splits <main> into records. A record starts at an h1 or h2, at an h3
    with its own id, and at an <article id> or <li id> (project cards, news
    items), which hold their own record until they close."""

    def __init__(self, skip_tables: bool = False):
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, str, bool]] = []   # (tag, id, opened a container record)
        self.in_main = False
        self.skip_depth = 0
        self.skip_tables = skip_tables
        self.records: list[Record] = []
        self.containers: list[Record] = []
        self.current: Record | None = None
        self.capture: list[str] | None = None   # heading text being read
        self.capture_tag = ""
        self.capture_rec: Record | None = None
        self.capture_kind = ""
        self.kicker_buf: list[str] | None = None
        self.time_buf: list[str] | None = None
        self.kicker_tag = ""
        self.pending_kicker = ""

    # -- helpers ---------------------------------------------------------
    def nearest_id(self) -> str:
        for tag, ident, _ in reversed(self.stack):
            if ident and ident != "main":
                return ident
        return ""

    def new_record(self, anchor: str, level: int) -> Record:
        rec = Record(anchor, level)
        self.records.append(rec)
        return rec

    def flush_kicker(self):
        """A kicker that was not followed by a heading belongs to the text around it."""
        if self.pending_kicker:
            rec = self.target()
            rec.kicker = rec.kicker or self.pending_kicker
            rec.text.append(" " + self.pending_kicker + " ")
            self.pending_kicker = ""

    def target(self) -> Record:
        if self.current is None:
            self.current = self.new_record("", 1)
        return self.current

    # -- parser events ---------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True
        if not self.in_main:
            return
        if tag in VOID:
            if tag == "br" and not self.skip_depth and self.current is not None:
                self.current.text.append(" ")
            if tag == "img" and not self.skip_depth and a.get("alt"):
                self.target().extra.append(a["alt"])
            return
        if tag not in INLINE and not self.skip_depth and self.current is not None:
            self.current.text.append(" ")
        classes = set((a.get("class") or "").split())
        ident = a.get("id", "")
        skip = (tag in SKIP_TAGS or classes & SKIP_CLASSES or a.get("aria-hidden") == "true"
                or (self.skip_tables and tag == "table"))
        opened = False
        if self.skip_depth or skip:
            self.skip_depth += 1
            self.stack.append((tag, ident, False))
            return
        if tag in ("article", "li") and ident:
            rec = self.new_record(ident, 2)
            rec.container = True
            self.containers.append(self.current)
            self.current = rec
            opened = True
        self.stack.append((tag, ident, opened))
        if tag in HEADINGS:
            level = int(tag[1])
            cur = self.current
            inside = cur is not None and cur.container
            if inside:
                kind = "title" if not cur.title else "heading"
            elif tag in ("h1", "h2") or (tag == "h3" and ident):
                anchor = "" if tag == "h1" else (ident or self.nearest_id())
                if not (tag == "h1" and cur is not None and cur.level == 1 and not cur.title):
                    # (the page's opening lines before its h1 stay in the h1's record)
                    self.current = self.new_record(anchor, level)
                kind = "title"
                if self.pending_kicker:
                    self.current.kicker = self.pending_kicker
                    self.current.text.append(self.pending_kicker + " ")
                    self.pending_kicker = ""
            else:
                kind = "heading"
            self.capture, self.capture_tag, self.capture_rec, self.capture_kind = [], tag, self.target(), kind
        elif "kicker" in classes and self.kicker_buf is None:
            self.kicker_buf = []
            self.kicker_tag = tag
        elif tag == "time" and self.time_buf is None:
            self.time_buf = []

    def handle_endtag(self, tag):
        if not self.in_main:
            return
        if tag == "main":
            self.in_main = False
            return
        if tag in VOID:
            return
        if tag not in INLINE and not self.skip_depth and self.current is not None:
            self.current.text.append(" ")
        # pop to the matching tag (tolerates sloppy nesting)
        while self.stack:
            t, ident, opened = self.stack.pop()
            if self.skip_depth:
                self.skip_depth -= 1
                if t == tag:
                    return
                continue
            if t in HEADINGS and self.capture is not None and t == self.capture_tag:
                text = norm_space("".join(self.capture))
                if text:
                    if self.capture_kind == "title":
                        self.capture_rec.title = text
                    else:
                        self.capture_rec.headings.append(text)
                self.capture = None
            if t == "time" and self.time_buf is not None:
                text = norm_space("".join(self.time_buf))
                rec = self.target()
                if text and rec.container and not rec.date:
                    rec.date = text
                self.time_buf = None
            if opened:
                self.current = self.containers.pop() if self.containers else None
            if t == tag:
                break
        if self.kicker_buf is not None and tag == self.kicker_tag:
            self.flush_kicker()
            self.pending_kicker = norm_space("".join(self.kicker_buf))
            self.kicker_buf = None

    def handle_data(self, data):
        if not self.in_main or self.skip_depth:
            return
        if self.capture is not None:
            self.capture.append(data)
            return
        if self.kicker_buf is not None:
            self.kicker_buf.append(data)
            return
        if data.strip():
            self.flush_kicker()
        if self.time_buf is not None:
            self.time_buf.append(data)
        self.target().text.append(data)


def ids_in(html: str) -> set[str]:
    return set(re.findall(r'\sid="([^"]+)"', html))


def page_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = unescape(m.group(1)) if m else ""
    return t.split(" · ")[0].strip()


def kind_of(path: str, app_paths: set[str]) -> str:
    if path.startswith("courses/"):
        return "course"
    if path == "projects/":
        return "project"
    if path in app_paths:
        return "app"
    return {"talks/": "talk", "news/": "news", "cv/": "cv"}.get(path, "page")


def tokens(text: str) -> list[str]:
    text = re.sub(r"\b(\d{2})-(\d{3})\b", r"\1\2", text.lower())
    return re.findall(r"[a-z0-9]+", text)


def trim(text: str, n: int) -> tuple[str, str]:
    """Cut at a word boundary near n characters; return (kept, rest)."""
    if len(text) <= n:
        return text, ""
    cut = text.rfind(" ", 0, n)
    cut = cut if cut > n * 0.6 else n
    return text[:cut].rstrip(" ,;:") + "…", text[cut:]


def extra_terms(rest: str, kept: str, alts: list[str]) -> str:
    """The words of the cut-off text and image descriptions, once each, so the
    whole section stays findable without shipping all of it."""
    seen = {stem(w) for w in tokens(kept)}
    out = []
    for w in tokens(rest + " " + " ".join(alts)):
        if w in STOP or len(w) < 2 or stem(w) in seen or (w.isdigit() and not KEEP_NUMBER.match(w)):
            continue
        seen.add(stem(w))
        out.append(w)
    return " ".join(out)


def build_records(pages: dict[str, str], meta: dict[str, dict], app_paths: set[str]) -> list[dict]:
    """pages: {path: html} for every page to index, in site order.
    meta: {url: {"g": tags, "d": date}} extra facts keyed by record URL."""
    out = []
    for path, html in pages.items():
        parser = PageParser(skip_tables=path.startswith("evaluations"))
        parser.feed(html)
        kind = kind_of(path, app_paths)
        ptitle = ""
        for rec in parser.records:
            if rec.level == 1 and rec.title:
                ptitle = rec.title
                break
        ptitle = ptitle or page_title(html)
        seen_urls = set()
        for i, rec in enumerate(parser.records):
            body = EMAIL.sub("", rec.body())
            if rec.date and body.startswith(rec.date):
                body = body[len(rec.date):].lstrip()   # the date has its own field
            title = rec.title
            if not title and rec.level == 1:
                title = ptitle
            if not title:
                # A news item or other untitled card: its first sentence is its title.
                first = re.split(r"(?<=[.!?])\s", body, maxsplit=1)[0]
                title, _ = trim(first, 90)
            if not title or (not body and not rec.headings and rec.level != 1):
                continue
            url = path + (f"#{rec.anchor}" if rec.anchor else "")
            if url in seen_urls:
                # two headings under one anchor: fold into the earlier record
                prev = next(r for r in reversed(out) if r["u"] == url)
                prev["h"] = " · ".join(dict.fromkeys(x for x in [prev.get("h", ""), title, *rec.headings]
                                                     if x and x != prev["t"]))
                more = extra_terms(body, prev.get("b", "") + " " + prev.get("x", ""), rec.extra)
                if more:
                    prev["x"] = norm_space(prev.get("x", "") + " " + more)
                continue
            seen_urls.add(url)
            kept, rest = trim(body, BODY_CHARS)
            m = meta.get(url, {})
            tags = m.get("g", "")
            if rec.level == 1 and page_title(html) not in (title, "Ben Collier"):
                tags = page_title(html) + (" · " + tags if tags else "")
            date = m.get("d") or rec.date or (DATE.search(rec.kicker).group(0) if DATE.search(rec.kicker or "") else "")
            r = {
                "u": url,
                "k": m.get("k", kind),
                "t": title,
                "p": m.get("p", "" if rec.level == 1 else ptitle),
                "h": " · ".join(dict.fromkeys(rec.headings)),
                "g": norm_space(tags),
                "d": date,
                "b": kept,
                "x": extra_terms(rest, kept, rec.extra),
            }
            out.append({k: v for k, v in r.items() if v or k in ("u", "k", "t")})
    return out


def write_index(records: list[dict]) -> str:
    doc = {"v": 1, "kinds": KINDS, "docs": records}
    return json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
