"""Checks for the site search index (assets/search-index.json).

Run from the repo root after `python3 scripts/build.py`:

    python3 -m unittest discover -s tests

Standard library only.
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build  # noqa: E402
import search_index  # noqa: E402

INDEX = json.loads((ROOT / "assets" / "search-index.json").read_text(encoding="utf-8"))
DOCS = INDEX["docs"]
FIELDS = {"u", "k", "t", "p", "h", "g", "d", "b", "x"}


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


class SearchIndexTest(unittest.TestCase):
    def test_every_page_is_indexed(self):
        pages = {d["u"] for d in DOCS if "#" not in d["u"]}
        for path in build.site_paths():
            if path == "search/":
                continue
            self.assertIn(path, pages, f"{path or 'home'} has no page record")

    def test_search_page_is_in_the_sitemap_but_not_the_index(self):
        self.assertIn("search/", build.site_paths())
        self.assertIn("/search/</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertFalse(any(d["u"].startswith("search/") for d in DOCS))

    def test_urls_and_anchors_resolve(self):
        ids = {}
        for d in DOCS:
            path, _, anchor = d["u"].partition("#")
            page = ROOT / (path + "index.html")
            self.assertTrue(page.exists(), d["u"])
            if anchor:
                if path not in ids:
                    ids[path] = search_index.ids_in(page.read_text(encoding="utf-8"))
                self.assertIn(anchor, ids[path], f"{d['u']}: no element with that id")

    def test_urls_are_unique(self):
        urls = [d["u"] for d in DOCS]
        self.assertEqual(len(urls), len(set(urls)))

    def test_records_have_only_known_fields_and_kinds(self):
        self.assertEqual(set(INDEX["kinds"]), set(search_index.KINDS))
        for d in DOCS:
            self.assertLessEqual(set(d), FIELDS, d["u"])
            self.assertIn(d["k"], search_index.KINDS, d["u"])
            self.assertTrue(d["t"].strip(), d["u"])

    def test_kinds_cover_the_site(self):
        kinds = {d["k"] for d in DOCS}
        self.assertEqual(kinds, set(search_index.KINDS))
        by_url = {d["u"]: d for d in DOCS}
        self.assertEqual(by_url["courses/45-851/"]["k"], "course")
        self.assertEqual(by_url["reels/"]["k"], "app")
        self.assertEqual(by_url["cv/"]["k"], "cv")
        for nid in build.news_ids():
            self.assertEqual(by_url[f"news/#{nid}"]["k"], "news")

    def test_course_numbers_are_tagged(self):
        by_url = {d["u"]: d for d in DOCS}
        for c in build.ALL_COURSES:
            num = c.get("number", "")
            if re.fullmatch(r"\d{2}-\d{3}", num):
                self.assertIn(num, by_url[f"courses/{c['slug']}/"].get("g", ""), c["slug"])

    def test_no_email_address(self):
        blob = json.dumps(INDEX)
        self.assertNotIn("@", blob)
        self.assertNotIn("[at]", blob)

    def test_no_evaluation_comments(self):
        """Quote cards and letters from the evaluations stay out of search,
        even where a page shows them."""
        ev = json.loads((ROOT / "data" / "evaluations.json").read_text(encoding="utf-8"))
        texts = [q["text"] for qs in ev.get("course_quotes", {}).values() for q in qs]
        texts += [q.get("text", "") for q in ev.get("quotes", [])]
        texts += [n.get("text", "") for n in ev.get("notes", [])]
        shown = squash(" ".join(d.get(f, "") for d in DOCS for f in ("t", "h", "b")))
        for t in texts:
            words = squash(t).split()
            if len(words) < 8:
                continue
            for i in range(0, len(words) - 7, 4):
                frag = " ".join(words[i:i + 8])
                self.assertNotIn(frag, shown, f"evaluation comment in the index: {frag!r}")

    def test_no_placeholder_or_student_records(self):
        data = json.loads((ROOT / "data" / "students.json").read_text(encoding="utf-8"))
        blob = squash(json.dumps(INDEX))
        for row in data.get("papers", []) + data.get("students", []):
            if row.get("status") != "public":
                self.assertNotIn(squash(row.get("title", row.get("name", "")))[:40] or "\0", blob)
        self.assertNotIn("paste the project summary", blob)

    def test_index_matches_the_pages(self):
        """The committed index is what the build makes from the committed pages."""
        portfolio = build.load_json("portfolio.json")["projects"]
        _, _, records = build.search_records(portfolio)
        self.assertEqual(records, DOCS, "assets/search-index.json is stale: run python3 scripts/build.py")

    def test_index_is_small(self):
        import gzip
        raw = (ROOT / "assets" / "search-index.json").read_bytes()
        self.assertLess(len(gzip.compress(raw)), 100_000)


if __name__ == "__main__":
    unittest.main()
