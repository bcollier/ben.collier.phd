#!/usr/bin/env python3
"""Generate the static faculty site. Run from the repo root: python3 scripts/build.py"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))

# Absolute URLs have to point somewhere that resolves. Until DNS for the custom
# domain is live, that is the github.io address; pointing canonical tags at a
# domain that does not answer tells search engines the real page is a dead link.
HOST = (
    f"https://{SITE['custom_domain']}"
    if SITE.get("domain_live")
    else SITE["pages_url"].rstrip("/")
)
DOMAIN_LABEL = SITE["custom_domain"]
OG_IMAGE = f"{HOST}/assets/og.png"
BUILT = date.today().isoformat()

COURSES = [
    {
        "slug": "70-445",
        "number": "70-445",
        "title": "Artificial Intelligence for Business Leaders",
        "program": "Undergraduate",
        "school": "Tepper",
        "built": True,
        "color": "c-navy",
        "one_liner": "Where AI creates business value, where it does not, and how to tell the board which is which.",
        "blurb": "A flagship, practice-oriented undergraduate course on how AI is reshaping organizations, industries, and managerial decisions. The first half covers the foundations: how machine learning, neural networks, and large language models work, and the data, chips, and compute economics underneath them. The second half works through AI in marketing, sales, finance, operations, people analytics, and strategy, plus the ethics, governance, and regulation that decide whether adoption lasts. It runs on active learning: in-class exercises, short cases, memos written for executives, student-led briefings on current AI topics, and a semester-long group project in one of three tracks: an AI investment committee for a real public company, building and red-teaming an AI agent, or earning $100 with an AI-enabled business.",
        "offerings": ["Developed for Fall 2026", "Fall 2026"],
        "materials": "No required textbook. Materials for enrolled students are on Canvas.",
    },
    {
        "slug": "45-884",
        "number": "45-884",
        "title": "AI Methods for Social and Visual Data",
        "program": "MBA",
        "school": "Tepper",
        "built": True,
        "color": "c-ink",
        "one_liner": "Work with social and visual data without pretending the model is the decision.",
        "blurb": "A course I built for Tepper MBA students who need to use modern AI on text, networks, images, and other unstructured sources. We treat models as instruments: you should be able to explain what they did, where they fail, and whether the output is ready for a business decision. Python-first, with ethics in the same labs as the code.",
        "offerings": [
            "Developed for Fall 2025",
            "Fall 2025 full-time",
            "Fall 2025 online hybrid",
            "Summer 2026",
        ],
        "materials": "Notebooks and workshop notes live on the teaching materials page as I make them public.",
    },
    {
        "slug": "70-377",
        "number": "70-377",
        "title": "Managing and Assessing Tech Talent and Organizations",
        "program": "Undergraduate",
        "school": "Tepper / CMU Qatar",
        "built": True,
        "color": "c-wine",
        "one_liner": "How to hire, grow, and evaluate technical people without managing by vibes.",
        "blurb": "A micro-course I developed on managing technical talent: assessing skill, designing work, and building teams that can actually ship. Built for undergraduates and taught as a new offering at CMU Qatar in Fall 2025.",
        "offerings": ["Developed October 2025", "Fall 2025 CMU Qatar"],
        "materials": "Course outline available to enrolled students; public excerpts go on the materials page.",
    },
    {
        "slug": "msba-math-skills-workshop",
        "number": "",
        "label": "MSBA",
        "title": "MSBA Math Skills Workshop",
        "program": "MSBA",
        "school": "Tepper",
        "built": True,
        "color": "c-clay",
        "one_liner": "The math MSBA students need in place before the quantitative core starts.",
        "blurb": "A workshop I developed for Summer 2026 for incoming MSBA students. The aim is that students arrive at the program's quantitative courses with the mathematics already in hand, rather than learning it alongside the statistics.",
        "offerings": ["Developed for Summer 2026"],
        "materials": "Workshop notes will be posted as I stabilize them for reuse.",
    },
    {
        "slug": "45-851",
        "number": "45-851",
        "title": "Data Mining",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-rust",
        "one_liner": "Find structure in messy business data, then decide whether to trust it.",
        "blurb": "The MBA data mining course: clustering, classification, evaluation, and the habit of asking what the model is for. Labs are Python. The point is not to collect algorithms. It is to leave with a workflow you can take into a messy dataset on Monday.",
        "offerings": [
            "Fall 2023",
            "Fall 2024 full-time",
            "Spring 2024",
            "Spring 2025 online hybrid",
            "Fall 2025",
        ],
        "materials": "Public notebooks and video walkthroughs are collected under Teaching materials.",
    },
    {
        "slug": "45-885",
        "number": "45-885",
        "title": "Data Visualization",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-olive",
        "one_liner": "Make a chart that changes what someone does on Monday.",
        "blurb": "Visualization as a decision tool, not decoration. Students design charts and dashboards that survive contact with executives, and they learn enough perceptual and statistical ground to know when a graphic is lying.",
        "offerings": [
            "Spring 2024",
            "Spring 2025 full-time",
            "Spring 2025 online hybrid",
            "Fall 2025",
            "Spring 2026",
        ],
        "materials": "Worked examples, redesign critiques, and Tableau/Python pairings on the materials page.",
    },
    {
        "slug": "46-885",
        "number": "46-885",
        "title": "Data Exploration and Visualization",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-pine",
        "one_liner": "Explore first, then visualize like you mean it.",
        "blurb": "The MSBA companion to visualization: exploratory analysis, chart design, dashboards, and the communication layer that makes a finding usable.",
        "offerings": ["Spring 2025 online hybrid", "Spring 2026"],
        "materials": "See Teaching materials for notebooks shared outside Canvas.",
    },
    {
        "slug": "46-880",
        "number": "46-880",
        "title": "Introduction to Probability and Statistics",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-slate",
        "one_liner": "The quantitative floor every later analytics course stands on.",
        "blurb": "Probability, inference, and the statistical reasoning MSBA students need before they reach machine learning.",
        "offerings": ["Fall 2024 full-time"],
        "materials": "Public excerpts go on the materials page as they are cleared.",
    },
    {
        "slug": "46-887",
        "number": "46-887",
        "title": "Machine Learning for Business Applications",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-copper",
        "one_liner": "Machine learning that has to survive a business constraint, not just a Kaggle score.",
        "blurb": "Applied machine learning for MSBA students: pipelines, evaluation, and the translation from a fitted model to an operational decision.",
        "offerings": ["Spring 2026"],
        "materials": "Lab notebooks posted to Teaching materials as they are cleared for public use.",
    },
    {
        "slug": "90-803",
        "number": "90-803",
        "title": "Machine Learning Foundations with Python",
        "program": "Public Policy & Management",
        "school": "Heinz College",
        "built": False,
        "color": "c-navy",
        "one_liner": "The Python machine learning foundation Heinz students need for policy work.",
        "blurb": "Selected teaching at Heinz College. A twelve-unit foundation in machine learning with Python for students who will apply these methods to public policy and management problems.",
        "offerings": ["Spring 2026 full-time"],
        "materials": "Heinz students get the full set on Canvas; public excerpts go on the materials page.",
    },
]

NEWS = [
    ("2026-08-25", "First day of 70-445 Artificial Intelligence for Business Leaders, a new undergraduate course I built."),
    ("2026-06-10", "George Leland Bach Teaching Award, voted by the MBA Class of 2026."),
    ("2026-03", "Named an AWS Academy Educator."),
    ("2026-01", "Advising two MSBA capstone teams this spring."),
    ("2025-08", "First offering of AI Methods for Social and Visual Data, a course I built for the MBA."),
    ("2025-05", "Joined gAIm Systems as Senior Director of AI and Data Science."),
    ("2025-01", "Advised five MSBA capstone projects."),
    ("2024-08", "Joined Tepper as Assistant Teaching Professor of Business Analytics."),
    ("2024-06", "Taught in the Business Analytics Summer Summit."),
    ("2024-01", "Advised four MSBA capstone projects."),
]


def load_json(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def md_to_html(md: str) -> str:
    lines = md.strip().splitlines()
    out = []
    in_ul = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        if line.startswith("# "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            # Skip top H1; page already has a title.
            continue
        if line.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h3>{inline(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f"<h2>{inline(line[3:])}</h2>")
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline(line[2:])}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        out.append(f"<p>{inline(line)}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def inline(text: str) -> str:
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    # Bare URLs become links too, so the CV source can stay plain text.
    text = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<]+?)(?=[.,;)]?(?:\s|$))', r'<a href="\1">\1</a>', text)
    return text


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def header(root: str, active: str, title: str, desc: str, canon: str, jsonld: str) -> str:
    def item(href, label, key):
        current = ' aria-current="page"' if active == key else ""
        return f'<a href="{root}{href}"{current}>{label}</a>'

    url = f"{HOST}/{canon}"
    ld = (
        f'\n  <script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{root}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="author" content="{esc(SITE['author'])}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#f3efe6" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#17130f" media="(prefers-color-scheme: dark)">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="{'profile' if canon == '' else 'article'}">
  <meta property="og:site_name" content="{esc(SITE['author'])}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ben Collier, Assistant Teaching Professor of Business Analytics, Tepper School of Business">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
  <link rel="alternate" type="application/atom+xml" title="Ben Collier — news" href="{root}feed.xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,400..600,0..100,0..1&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/site.css">{ld}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <div class="wrap">
    <header class="site">
      <a class="wordmark" href="{root}">Ben Collier</a>
      <nav class="primary" aria-label="Primary">
        {item("courses/", "courses", "courses")}
        {item("materials/", "materials", "materials")}
        {item("projects/", "projects", "projects")}
        {item("practice/", "practice", "practice")}
        {item("cv/", "cv", "cv")}
        {item("news/", "news", "news")}
        {item("contact/", "contact", "contact")}
      </nav>
    </header>
    <main id="main">
"""


def footer(root: str) -> str:
    return f"""    </main>
    <footer class="site">
      <div>Ben Collier · Tepper School of Business · Carnegie Mellon University</div>
      <div><a href="{root or './'}">{DOMAIN_LABEL}</a> · <a href="{root}designs/">Five designs</a> · <a href="{root}feed.xml">News feed</a> · <a href="https://github.com/bcollier/ben.collier.phd">Source</a></div>
    </footer>
  </div>
  <script src="{root}js/config.js"></script>
  <script src="{root}js/site.js"></script>
</body>
</html>
"""


def page(root, active, title, desc, canon, body, jsonld="") -> str:
    return header(root, active, title, desc, canon, jsonld) + body + footer(root)


def write(rel, content: str):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", rel)


def course_label(c) -> str:
    """Short text for a course thumbnail: the catalog number, or a label for a course without one."""
    return c["number"] or c.get("label") or c["program"]


def course_name(c) -> str:
    """Catalog number and title, or just the title when there is no number."""
    return f"{c['number']} {c['title']}".strip()


def course_card(c, root):
    built = '<span class="badge built">Built</span>' if c["built"] else ""
    return f"""<a class="card" href="{root}courses/{c['slug']}/">
  <div class="thumb {c['color']}"><span>{course_label(c)}</span></div>
  <div class="body">
    <div class="meta">{built}<span>{c['program']} · {c['school']}</span></div>
    <h3>{c['title']}</h3>
    <p>{c['one_liner']}</p>
  </div>
</a>
"""


MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def human_date(iso: str) -> str:
    """2026-06-10 -> June 10, 2026. 2026-03 -> March 2026. 2026 -> 2026."""
    parts = iso.split("-")
    if len(parts) == 3:
        return f"{MONTHS[int(parts[1]) - 1]} {int(parts[2])}, {parts[0]}"
    if len(parts) == 2:
        return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    return iso


def rfc3339(iso: str) -> str:
    """Pad a partial date out to a timestamp Atom will accept."""
    parts = iso.split("-")
    while len(parts) < 3:
        parts.append("01")
    return f"{parts[0]}-{parts[1]}-{parts[2]}T12:00:00Z"


def news_items(limit=None):
    items = NEWS if limit is None else NEWS[:limit]
    out = ['<ol class="feed">']
    for iso, text in items:
        out.append(
            f'<li><time datetime="{iso}">{human_date(iso)}</time>'
            f'<div class="post"><p>{text}</p></div></li>'
        )
    out.append("</ol>")
    return "\n".join(out)


def person_jsonld() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{HOST}/#person",
        "name": SITE["author"],
        "url": f"{HOST}/",
        "image": OG_IMAGE,
        "jobTitle": SITE["job_title"],
        "email": f"mailto:{SITE['email']}",
        "worksFor": {
            "@type": "CollegeOrUniversity",
            "name": "Carnegie Mellon University",
            "department": {
                "@type": "Organization",
                "name": "Tepper School of Business",
            },
            "url": "https://www.cmu.edu/tepper/",
        },
        "knowsAbout": [
            "Business analytics",
            "Machine learning",
            "Data visualization",
            "Data mining",
            "Applied statistics",
        ],
        "sameAs": SITE["same_as"],
    }
    return json.dumps(data, indent=2)


def course_jsonld(c) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course_name(c),
        "description": c["blurb"],
        "url": f"{HOST}/courses/{c['slug']}/",
        "provider": {
            "@type": "CollegeOrUniversity",
            "name": "Carnegie Mellon University",
            "url": "https://www.cmu.edu/",
        },
        "instructor": {
            "@type": "Person",
            "@id": f"{HOST}/#person",
            "name": SITE["author"],
        },
    }
    if c["number"]:
        data["courseCode"] = c["number"]
    return json.dumps(data, indent=2)


def build_home():
    built = [c for c in COURSES if c["built"]]
    cards = "\n".join(course_card(c, "") for c in built)
    body = f"""
      <section class="hero">
        <img class="portrait" src="assets/portrait.jpg" width="500" height="500" alt="Portrait of Ben Collier">
        <div>
          <p class="kicker">Assistant Teaching Professor of Business Analytics</p>
          <h1>Ben Collier</h1>
          <p class="lede">I teach people to build, evaluate, and ship data systems — at Tepper, at Heinz, and in the field.</p>
          <p class="role">Tepper School of Business, Carnegie Mellon University. Selected courses at Heinz College.</p>
        </div>
      </section>

      <div class="bio">
        <p>My primary appointment is at Tepper, where I teach across the MBA, MS in Business Analytics, and undergraduate programs. I also teach selected courses at Heinz College. The work is applied: Python workflows, statistical reasoning, and the ethical judgment you need when a model meets a real organization.</p>
        <p>Before returning to the faculty I led data science at Duolingo and at UPMC. That practice work — now through Hot Metal Data and gAIm Systems — is what I bring into the classroom. I build courses and advise MSBA capstones.</p>
      </div>

      <div class="notice-strip">
        <strong>Five new designs are up for review.</strong>
        <span>The same content in five completely different design directions, live side by side.</span>
        <a href="designs/">Compare all five &rarr;</a>
      </div>

      <div class="tiles">
        <a class="tile" href="courses/"><div class="n">01</div><strong>Courses</strong><span>What I built and what I teach.</span></a>
        <a class="tile" href="projects/"><div class="n">02</div><strong>Projects</strong><span>Fun things I build for my classes.</span></a>
        <a class="tile" href="cv/"><div class="n">03</div><strong>CV</strong><span>Full curriculum vitae.</span></a>
        <a class="tile" href="practice/"><div class="n">04</div><strong>Practice</strong><span>Hot Metal Data and gAIm Systems.</span></a>
      </div>

      <h2>Courses I built</h2>
      <div class="grid" style="margin-top:1rem">{cards}</div>
      <p><a href="courses/">All courses</a></p>

      <h2>Recent posts from LinkedIn</h2>
      <ol class="feed" id="linkedin-recent">
        <li>
          <time datetime="2026-06-10">Jun 10, 2026</time>
          <div class="post">
            <p>Grateful to receive the George Leland Bach Teaching Award — chosen by vote of the graduating MBA class. Many thanks to the students of the Class of 2026.</p>
            <div class="people"><span>Tepper MBA Class of 2026</span></div>
          </div>
        </li>
      </ol>
      <p><a href="news/">All posts</a> · <a href="https://www.linkedin.com/in/bcollierphd">Follow on LinkedIn</a></p>

      <h2>News</h2>
      {news_items(5)}
      <p><a href="news/">Older notes</a> · <a href="cv/">Full CV</a></p>
"""
    write(
        "index.html",
        page(
            "",
            "home",
            "Ben Collier · Teaching, Tepper School of Business",
            "Assistant Teaching Professor of Business Analytics at Carnegie Mellon. Courses, projects, and applied work.",
            "",
            body,
            person_jsonld(),
        ),
    )


def build_courses_index():
    built = "\n".join(course_card(c, "../") for c in COURSES if c["built"])
    taught = "\n".join(course_card(c, "../") for c in COURSES if not c["built"])
    body = f"""
      <p class="kicker">Teaching</p>
      <h1>Courses</h1>
      <p class="lede">Built ones first, then the ones I currently teach.</p>

      <h2>Courses I built</h2>
      <div class="grid">{built}</div>

      <h2>Courses I teach</h2>
      <div class="grid">{taught}</div>
"""
    write(
        "courses/index.html",
        page(
            "../",
            "courses",
            "Courses · Ben Collier",
            "Courses Ben Collier built and teaches at Tepper and Heinz.",
            "courses/",
            body,
        ),
    )


def build_course_pages():
    for c in COURSES:
        offerings = "".join(f"<li>{o}</li>" for o in c["offerings"])
        built = '<span class="badge built">Course I built</span>' if c["built"] else ""
        body = f"""
      <article class="course-hero prose-width">
        <p class="kicker">{c['school']} · {c['program']}</p>
        <h1>{course_name(c)}</h1>
        <p>{built}</p>
        <div class="thumb {c['color']}">{course_label(c)}</div>
        <p class="lede">{c['one_liner']}</p>
        <p>{c['blurb']}</p>
        <h2>Recent offerings</h2>
        <ul>{offerings}</ul>
        <h2>Materials</h2>
        <p>{c['materials']} <a href="../../materials/">Teaching materials</a>.</p>
      </article>
      <p><a href="../">All courses</a></p>
"""
        write(
            f"courses/{c['slug']}/index.html",
            page(
                "../../",
                "courses",
                f"{course_name(c)} · Ben Collier",
                c["one_liner"],
                f"courses/{c['slug']}/",
                body,
                course_jsonld(c),
            ),
        )


def build_cv():
    md = (ROOT / "data" / "cv.md").read_text(encoding="utf-8")
    # Keep a short head above the converted body.
    body = f"""
      <p class="kicker">Curriculum vitae</p>
      <h1>CV</h1>
      <p class="lede">Appointments, teaching, courses built, advising, and practice.</p>
      <article class="cv">
        <div class="cv-head">
          <p><strong>Ben Collier</strong> · Assistant Teaching Professor of Business Analytics</p>
          <p>Tepper School of Business, Carnegie Mellon University · also Heinz College</p>
          <p><a href="mailto:bcollier@andrew.cmu.edu">bcollier@andrew.cmu.edu</a> · <a href="mailto:ben@collier.phd">ben@collier.phd</a> · <a href="{HOST}/">ben.collier.phd</a></p>
        </div>
        {md_to_html(md)}
      </article>
"""
    write(
        "cv/index.html",
        page(
            "../",
            "cv",
            "CV · Ben Collier",
            "Curriculum vitae for Ben Collier, Assistant Teaching Professor of Business Analytics at Carnegie Mellon.",
            "cv/",
            body,
        ),
    )


def build_materials():
    body = """
      <p class="kicker">Teaching artifacts</p>
      <h1>Teaching materials</h1>
      <p class="lede">Video, notebooks, and workshop content — the public layer of the courses. Enrolled students still get the full set on Canvas.</p>

      <h2>Video series</h2>
      <div class="empty">No public playlist yet. When I publish walkthroughs for data mining, visualization, and the AI methods course, they land here.</div>

      <h2>Notebooks</h2>
      <ul class="materials">
        <li><strong>Data mining labs.</strong> Python notebooks for clustering, classification, and evaluation.</li>
        <li><strong>Visualization redesigns.</strong> Before/after chart critiques paired with Tableau and Python.</li>
        <li><strong>AI methods for social and visual data.</strong> Course I built. Notebooks release as the offering settles.</li>
      </ul>

      <h2>Workshops</h2>
      <ul class="materials">
        <li><strong>MSBA Math Skills Workshop</strong> — developed for Summer 2026.</li>
        <li><strong>Business Analytics Summer Summit</strong> — instructor, 2024 and 2025.</li>
        <li><strong>Hot Metal Data workshops</strong> — corporate training outlines on request.</li>
      </ul>
"""
    write(
        "materials/index.html",
        page(
            "../",
            "materials",
            "Teaching materials · Ben Collier",
            "Public teaching materials: videos, notebooks, and workshops.",
            "materials/",
            body,
        ),
    )
    hub = """
      <p class="kicker">Teaching</p>
      <h1>Teaching</h1>
      <p class="lede">Courses I built, projects I show in class, and the materials that travel with them.</p>
      <div class="tiles">
        <a class="tile" href="../courses/"><div class="n">01</div><strong>Courses</strong><span>Built, taught, student projects.</span></a>
        <a class="tile" href="../projects/"><div class="n">02</div><strong>Projects</strong><span>Fun things built for class.</span></a>
        <a class="tile" href="../materials/"><div class="n">03</div><strong>Materials</strong><span>Notebooks, video, workshops.</span></a>
        <a class="tile" href="../cv/"><div class="n">04</div><strong>CV</strong><span>Full curriculum vitae.</span></a>
      </div>
"""
    write(
        "teaching/index.html",
        page(
            "../",
            "courses",
            "Teaching · Ben Collier",
            "Teaching hub: courses, projects, materials, CV.",
            "teaching/",
            hub,
        ),
    )


def portfolio_card(p, root):
    links = " · ".join(f'<a href="{esc(l["href"])}">{esc(l["label"])}</a>' for l in p["links"])
    return f"""<article class="portfolio-item" id="{p['id']}">
  <a href="{esc(p['links'][0]['href'])}"><img class="shot" src="{root}{p['image']}" alt="{esc(p['image_alt'])}" width="{p['image_width']}" height="{p['image_height']}" loading="lazy"></a>
  <div class="body">
    <div class="meta">{esc(p['kind'])} · {esc(p['tools'])} · {esc(p['date'])}</div>
    <h2>{esc(p['title'])}</h2>
    <p>{p['summary']}</p>
    <p>{p['process']}</p>
    <p class="links">{links}</p>
  </div>
</article>"""


def build_portfolio(portfolio):
    items = "\n".join(portfolio_card(p, "../") for p in portfolio)
    body = f"""
      <p class="kicker">Portfolio</p>
      <h1>Projects</h1>
      <p class="lede">Things I build to show my classes what the tools can do now. Small, playable, and honest about how they were made. More are coming.</p>
      <div class="portfolio">{items}</div>
"""
    write(
        "projects/index.html",
        page(
            "../",
            "projects",
            "Projects · Ben Collier",
            "Fun projects Ben Collier builds for his classes, with source, prompts, and build logs.",
            "projects/",
            body,
        ),
    )


def build_practice():
    body = """
      <p class="kicker">Applied work</p>
      <h1>Practice</h1>
      <p class="lede">Industry work that feeds the classroom.</p>

      <h2>Hot Metal Data</h2>
      <p class="prose-width">Applied analytics consulting and corporate training — use-case discovery, model development, and teaching teams to apply the work themselves. Pittsburgh-born. Also listed in some directories as Hot Metal AI.</p>

      <h2>gAIm Systems</h2>
      <p class="prose-width">Senior Director of AI and Data Science. Tools so sports organizations can recruit, develop, and assemble teams with something better than folklore. <a href="https://gaimsystems.com">gaimsystems.com</a>.</p>

      <h2>Earlier</h2>
      <ul class="prose-width">
        <li><strong>Duolingo</strong> — Staff / Lead data scientist. Experimentation, monetization analytics, forecasting around the IPO and Duolingo Max.</li>
        <li><strong>UPMC</strong> — Senior Director of Data Science. Founding data scientist on a joint venture with IBM Watson Health; led CognitiveRx, later acquired by Premier.</li>
      </ul>
"""
    write(
        "practice/index.html",
        page(
            "../",
            "practice",
            "Practice · Ben Collier",
            "Hot Metal Data, gAIm Systems, and earlier applied data science.",
            "practice/",
            body,
        ),
    )


def build_news():
    body = f"""
      <p class="kicker">Log</p>
      <h1>News</h1>
      <p class="lede">A dated running log. Cheap to maintain, and the fastest way to show the site is alive.</p>
      {news_items()}
      <h2>LinkedIn</h2>
      <ol class="feed" id="linkedin-all"></ol>
"""
    write(
        "news/index.html",
        page(
            "../",
            "news",
            "News · Ben Collier",
            "Dated notes from teaching, advising, and practice.",
            "news/",
            body,
        ),
    )


def build_contact():
    body = f"""
      <p class="kicker">Office</p>
      <h1>Contact</h1>
      <p class="lede">Email is the reliable door. Students: put the course number in the subject line.</p>
      <ul class="contact-list">
        <li><span>CMU email</span><div><a href="mailto:bcollier@andrew.cmu.edu">bcollier@andrew.cmu.edu</a></div></li>
        <li><span>Personal</span><div><a href="mailto:ben@collier.phd">ben@collier.phd</a></div></li>
        <li><span>Site</span><div><a href="../">{DOMAIN_LABEL}</a></div></li>
        <li><span>Office</span><div>Tepper School of Business<br>Carnegie Mellon University<br>5000 Forbes Avenue<br>Pittsburgh, PA 15213</div></li>
        <li><span>Office hours</span><div id="calendly-slot">Email me two times that work and I will confirm one.</div></li>
        <li><span>LinkedIn</span><div><a href="https://www.linkedin.com/in/bcollierphd">linkedin.com/in/bcollierphd</a></div></li>
        <li><span>GitHub</span><div><a href="https://github.com/bcollier">github.com/bcollier</a></div></li>
        <li><span>ORCID</span><div><a href="https://orcid.org/0000-0002-4651-7684">0000-0002-4651-7684</a></div></li>
        <li><span>CV</span><div><a href="../cv/">Full CV</a></div></li>
      </ul>
"""
    write(
        "contact/index.html",
        page(
            "../",
            "contact",
            "Contact · Ben Collier",
            "Email, office, and links for Ben Collier.",
            "contact/",
            body,
        ),
    )


def build_404():
    body = """
      <h1>Page not found</h1>
      <p class="lede">That URL is not on this site.</p>
      <p><a href="./">Home</a> · <a href="./courses/">Courses</a> · <a href="./projects/">Projects</a> · <a href="./cv/">CV</a></p>
"""
    write(
        "404.html",
        page("", "home", "Not found · Ben Collier", "Page not found.", "404.html", body),
    )


def site_paths():
    """Every canonical URL path on the site, in navigation order."""
    paths = ["", "courses/", "materials/", "projects/", "practice/", "cv/", "news/", "contact/", "teaching/", "designs/"]
    paths += [f"courses/{c['slug']}/" for c in COURSES]
    return paths


def build_sitemap():
    urls = []
    for path in site_paths():
        priority = "1.0" if path == "" else "0.7" if "/" in path.rstrip("/") else "0.8"
        urls.append(
            "  <url>\n"
            f"    <loc>{HOST}/{path}</loc>\n"
            f"    <lastmod>{BUILT}</lastmod>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    write(
        "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n",
    )


def build_robots():
    write(
        "robots.txt",
        "User-agent: *\nAllow: /\n\n" f"Sitemap: {HOST}/sitemap.xml\n",
    )


def build_feed():
    entries = []
    for iso, text in NEWS:
        stamp = rfc3339(iso)
        entries.append(
            "  <entry>\n"
            f"    <title>{esc(text)}</title>\n"
            f'    <link href="{HOST}/news/"/>\n'
            f"    <id>tag:{DOMAIN_LABEL},{iso.split('-')[0]}:news/{iso}</id>\n"
            f"    <updated>{stamp}</updated>\n"
            f"    <summary>{esc(text)}</summary>\n"
            "  </entry>"
        )
    latest = rfc3339(NEWS[0][0]) if NEWS else f"{BUILT}T12:00:00Z"
    write(
        "feed.xml",
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        f"  <title>Ben Collier — news</title>\n"
        f"  <subtitle>Teaching, advising, and applied work.</subtitle>\n"
        f'  <link href="{HOST}/feed.xml" rel="self"/>\n'
        f'  <link href="{HOST}/"/>\n'
        f"  <id>{HOST}/</id>\n"
        f"  <updated>{latest}</updated>\n"
        f"  <author><name>{SITE['author']}</name></author>\n"
        + "\n".join(entries)
        + "\n</feed>\n",
    )


def main():
    portfolio = load_json("portfolio.json")["projects"]
    build_home()
    build_courses_index()
    build_course_pages()
    build_cv()
    build_portfolio(portfolio)
    build_materials()
    build_practice()
    build_news()
    build_contact()
    build_404()
    build_sitemap()
    build_robots()
    build_feed()
    print(f"done — absolute URLs point at {HOST}")


if __name__ == "__main__":
    main()
