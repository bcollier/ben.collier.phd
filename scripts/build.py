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
        "one_liner": "Where AI creates value in a business, where it does not, and how to explain the difference to the people paying for it.",
        "blurb": "An undergraduate course on how AI is changing organizations and the decisions managers make. The first part covers how AI works, from expert systems to machine learning, neural networks, and large language models. The second part puts students to work with AI agents on business problems. The third looks at AI in marketing, finance, people analytics, operations, and strategy, and at the ethics, economics, and regulation that decide whether adoption lasts. The semester project has three tracks. Teams can act as an AI investment committee for a real public company, build and red-team an AI agent, or try to earn $100 with a business that uses AI.",
        "offerings": [
            "Designed February to August 2026",
            "Fall 2026",
        ],
        "materials": "There is no required textbook. Enrolled students find the materials on Canvas.",
        "history": [
            "I started designing this course in February 2026 and taught it for the first time on August 25, 2026. It is open to undergraduates with no prerequisites. About forty students enrolled in the first section, and several had already used AI at work during a summer internship.",
            "My first plan spent several weeks on the history and hardware of AI and saved agents for the end of the term. Before the term began I moved agents up to week five, and they have become the thread that runs through the rest of the course. I am rebuilding the later weeks around one pattern: choose a use case, build it, deploy it, then try to break it.",
        ],
        "topics": [
            "What AI is, and why now",
            "A short history of AI",
            "Rules, search, and expert systems",
            "The five tribes of machine learning",
            "Machine learning fundamentals",
            "Neural networks and deep learning",
            "How large language models work",
            "Agentic AI and AI workflows, with a lab building a multi-agent customer support system",
            "Software development with AI assistance",
            "AI in marketing, finance, people analytics, and operations",
            "Bias and fairness",
            "The economics of AI, and AI strategy",
            "Governance, risk, and regulation",
        ],
    },
    {
        "slug": "45-884",
        "number": "45-884",
        "title": "AI Methods for Social and Visual Data",
        "program": "MBA",
        "school": "Tepper",
        "built": True,
        "color": "c-ink",
        "one_liner": "Using AI on text, networks, and images, and knowing when the output is ready for a decision.",
        "blurb": "I built this course for Tepper MBA students who need to use current AI methods on text, networks, images, and other unstructured data. We treat each model as a measuring instrument. Students should be able to say what it did, where it fails, and whether its output is good enough to act on. The labs are in Python, and we discuss ethics in the same labs as the code.",
        "offerings": [
            "Developed for Fall 2025",
            "Fall 2025 full-time",
            "Fall 2025 online hybrid",
            "Summer 2026",
            "Fall 2026",
        ],
        "materials": "I post notebooks and workshop notes on the materials page as they become public.",
        "history": [
            "I began building this course in December 2024 and first taught it in Fall 2025 to MBA and other master's students. It covers the data most business analytics courses skip: text, images, and the output of language models.",
            "For Summer 2026 I rebuilt it for a part-time format, with one live session a week and a set of hands-on videos I recorded for each module. They run from a first Python lesson through retrieval over company filings, computer vision, and agent workflows. For Fall 2026 I moved agentic AI earlier in the term, and students now get a summary and a cleaned transcript after each class.",
        ],
        "topics": [
            "AI models and unstructured data: Python, JSON, calling a model's API, and prompt engineering",
            "Natural language processing fundamentals",
            "Text mining for business insight, with retrieval over company filings and vector databases",
            "Computer vision fundamentals: object detection with YOLO, ResNet, and vision transformers",
            "Mining visual data, with a case comparing Tesla Vision and Waymo's sensor fusion",
            "Agentic AI and AI workflows, including building a first agent in n8n",
            "Emerging tools: evaluations, LLM-as-judge, and MCP",
        ],
    },
    {
        "slug": "70-377",
        "number": "70-377",
        "title": "Managing and Assessing Tech Talent and Organizations",
        "program": "Undergraduate",
        "school": "Tepper / CMU Qatar",
        "built": True,
        "color": "c-wine",
        "one_liner": "How to hire, develop, and evaluate technical people using evidence instead of instinct.",
        "blurb": "A micro-course I developed on managing technical talent: how to assess skill, how to design the work, and how to build teams that deliver. I wrote it for undergraduates, and it ran for the first time at CMU Qatar in Fall 2025.",
        "offerings": [
            "Proposed February 2025",
            "Fall 2025, CMU Qatar",
        ],
        "materials": "The course outline is available to enrolled students. Public excerpts will go on the materials page.",
        "history": [
            "I proposed this micro-course to Carnegie Mellon in Qatar in February 2025 and taught it in Fall 2025. Most sessions met on Zoom in the evening, Doha time, and the middle block met in person in Doha over three days. It was open to technical and business students with no prerequisites.",
        ],
        "topics": [
            "Interviewing for software development roles, including AI-driven assessment",
            "Interviewing for data and quantitative roles",
            "Case and behavioral interviews",
            "Onboarding technical talent: the first ninety days",
            "Running technical projects and leading an effective team",
            "Project management with work breakdown structures and OKRs",
            "Managing performance, promotion, and termination",
        ],
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
        "one_liner": "The math incoming MSBA students need before the quantitative core begins.",
        "blurb": "A workshop I developed for incoming MSBA students in Summer 2026. The goal is for students to start the program's quantitative courses with the mathematics already in place, so they are not learning it at the same time as the statistics.",
        "offerings": [
            "Built December 2025 to August 2026",
            "Summer 2026",
        ],
        "materials": "I will post the workshop notes once they are ready for reuse.",
        "history": [
            "A self-paced online course for incoming MSBA students, built with Tepper's learning technologies team between December 2025 and August 2026. I recorded every lesson, about thirty short videos across six modules, each pairing slides with worked problems written out by hand.",
        ],
        "topics": [
            "Algebra fundamentals and functions",
            "Calculus for analytics: derivatives, optimization, and gradient descent",
            "Linear algebra for data analytics: matrices, eigenvalues, least squares, PCA, and PageRank",
            "Descriptive statistics",
            "Probability foundations",
            "Statistical inference: sampling distributions, confidence intervals, and hypothesis tests",
        ],
    },
    {
        "slug": "45-851",
        "number": "45-851",
        "title": "Data Mining",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-rust",
        "one_liner": "Finding structure in messy business data, then deciding whether to trust it.",
        "blurb": "The MBA data mining course. It covers clustering, classification, and model evaluation, and it keeps asking what each model is for. Labs are in Python. The goal is not a long list of algorithms. It is a workflow students can apply to an unfamiliar dataset the week after the course ends.",
        "offerings": [
            "Fall 2023 full-time",
            "Spring 2024 online hybrid",
            "Fall 2024 full-time",
            "Spring 2025 online hybrid",
            "Fall 2025 full-time",
            "Fall 2025 online hybrid",
        ],
        "materials": "Public notebooks and video walkthroughs are collected on the materials page.",
        "history": [
            "I first taught Data Mining in Fall 2023, as an adjunct, to full-time MBA students. I taught it every fall and spring through Fall 2025, in both the full-time and the online hybrid programs.",
            "The first version was in R. For the Spring 2024 online hybrid section I scripted and recorded a video module for each topic. In Fall 2024 I moved the whole course to Python and then re-recorded the videos, and Fall 2025 added principal component analysis. The course is organized around the questions data mining answers in a business: which customers are alike, what something is worth, which class a case falls into, what happens next, and what a pile of text says.",
        ],
        "topics": [
            "Data exploration and visualization in Python",
            "Clustering, with a lab",
            "Principal component analysis",
            "Regression, with a lab",
            "Classification, with a lab",
            "Forecasting with time series data",
            "Natural language processing, with a lab",
            "Neural networks and large language models",
        ],
    },
    {
        "slug": "45-885",
        "number": "45-885",
        "title": "Data Visualization",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-olive",
        "one_liner": "Charts and dashboards designed to change a decision.",
        "blurb": "Visualization as a tool for making decisions. Students design charts and dashboards for executive audiences, and they learn enough about perception and statistics to spot a graphic that misleads.",
        "offerings": [
            "Spring 2024 evening",
            "Spring 2025 full-time",
            "Spring 2025 online hybrid",
            "Fall 2025 full-time",
            "Spring 2026 full-time",
            "Spring 2026 online hybrid",
        ],
        "materials": "Worked examples and chart redesigns are on the materials page.",
        "history": [
            "I took over Data Visualization in Spring 2024 with an evening section. At the time the course mixed Tableau with R and ggplot2. Since Spring 2025 it has been a Tableau course that needs no programming, and for the online hybrid students I recorded a library of about fifty short screencast lessons.",
            "In Fall 2025 I split each week into a lecture and a lab and gave visual design, typography, and color sessions of their own. The final project is a recorded data story of five to seven minutes.",
        ],
        "topics": [
            "Design of visual information, and Tableau fundamentals",
            "Principles of visual design, and storytelling with data",
            "Typography, color, and calculations in Tableau",
            "Visualizing spatial data",
            "Dashboards and interactive displays",
            "Clustering and social network graphs",
            "Explainable AI, data preparation, and animation",
        ],
    },
    {
        "slug": "46-885",
        "number": "46-885",
        "title": "Data Exploration and Visualization",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-pine",
        "one_liner": "Exploratory analysis first, then charts that make the finding clear.",
        "blurb": "The MSBA counterpart to the visualization course. It covers exploratory analysis, chart design, dashboards, and how to present a finding so that someone can use it.",
        "offerings": ["Spring 2025 online hybrid", "Spring 2026"],
        "materials": "Notebooks I share outside Canvas are on the materials page.",
        "history": [
            "The MSBA version of the visualization course. I first taught it in Spring 2025 and again in Spring 2026, with one session a week. It follows the same seven modules as the MBA course, all in Tableau, and ends with the same recorded data story.",
        ],
        "topics": [
            "Design of visual information, and Tableau fundamentals",
            "Storytelling with data",
            "Calculations, parameters, and trends in Tableau",
            "Visualizing spatial data",
            "Dashboards and interactive displays",
            "Clustering and social network graphs",
            "Explainable AI and visualization for machine learning",
        ],
    },
    {
        "slug": "46-880",
        "number": "46-880",
        "title": "Introduction to Probability and Statistics",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-slate",
        "one_liner": "The statistics every later analytics course depends on.",
        "blurb": "Probability, inference, and the statistical reasoning MSBA students need before they reach machine learning.",
        "offerings": ["Fall 2024 full-time"],
        "materials": "Public excerpts will go on the materials page once they are cleared.",
        "history": [
            "I taught the MSBA's first-term statistics course in Fall 2024, in two morning sections. I reworked the slide decks I inherited and used Excel and Python alongside the textbook, so that every idea had both a formula and a working example.",
        ],
        "topics": [
            "Probability and Bayes' theorem",
            "Discrete and continuous random variables and their distributions",
            "The normal distribution and joint distributions",
            "Sampling and the central limit theorem",
            "Interval estimation",
            "Hypothesis testing",
            "Regression, and inference with regression",
        ],
    },
    {
        "slug": "46-887",
        "number": "46-887",
        "title": "Machine Learning for Business Applications",
        "program": "MSBA",
        "school": "Tepper",
        "built": False,
        "color": "c-copper",
        "one_liner": "Machine learning that has to work under real business constraints, not just score well on a leaderboard.",
        "blurb": "Applied machine learning for MSBA students: building pipelines, evaluating models, and turning a fitted model into an operational decision.",
        "offerings": ["Spring 2026"],
        "materials": "Lab notebooks will go on the materials page once they are cleared for public use.",
        "history": [
            "I redesigned this MSBA course for Spring 2026 around a question that is easy to leave for later: how a model becomes part of a working business system. Mondays are lecture and Wednesdays are lab. Students build pipelines on AWS, put the results in Tableau or Streamlit dashboards, and finish with a team project demo.",
        ],
        "topics": [
            "From machine learning models to AI systems",
            "Integrating models into business services, with a cloud setup lab",
            "Evaluating, testing, and monitoring machine learning systems",
            "Natural language processing and large language models",
            "Imbalanced classification and anomaly detection",
            "Time series forecasting, with a cloud-connected Tableau dashboard",
            "Reinforcement learning",
        ],
    },
    {
        "slug": "90-803",
        "number": "90-803",
        "title": "Machine Learning Foundations with Python",
        "program": "Public Policy & Management",
        "school": "Heinz College",
        "built": False,
        "color": "c-navy",
        "one_liner": "Machine learning in Python for students headed into policy and management work.",
        "blurb": "A twelve-unit course at Heinz College that teaches machine learning with Python to students who will apply it to public policy and management problems.",
        "offerings": ["Spring 2026 full-time"],
        "materials": "Heinz students get the full materials on Canvas. Public excerpts will go on the materials page.",
        "history": [
            "I took over this Heinz College course in Spring 2026 and rebuilt it as fourteen modules, each pairing a lecture with a lab. It runs from clustering and regression through A/B testing to language models and computer vision. It ends with a teaching case I wrote comparing Tesla's camera-only approach to self-driving with Waymo's sensor fusion.",
        ],
        "topics": [
            "Machine learning and analytics in organizations",
            "Clustering, factor reduction, and feature engineering",
            "Regression and classification",
            "Model evaluation and hyperparameter tuning",
            "Forecasting with time series data",
            "A/B testing and multi-armed bandits",
            "Natural language processing and neural networks",
            "Large language models, and text mining with them",
            "Computer vision, and the Tesla Vision vs. Waymo case",
        ],
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
  <link rel="alternate" type="application/atom+xml" title="Ben Collier: news" href="{root}feed.xml">
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
      <div><a href="{root or './'}">{DOMAIN_LABEL}</a> · <a href="https://github.com/bcollier/ben.collier.phd/releases/tag/cs15-113-submission">15-113 version</a> · <a href="{root}feed.xml">News feed</a> · <a href="https://github.com/bcollier/ben.collier.phd">Source</a></div>
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
          <p class="lede">I teach business analytics and machine learning at Carnegie Mellon, and I still build AI and data systems outside the classroom.</p>
          <p class="role">Tepper School of Business, with selected courses at Heinz College.</p>
        </div>
      </section>

      <div class="bio">
        <p>Most of my teaching is at Tepper, in the MBA, the MS in Business Analytics, and the undergraduate program. I also teach at Heinz College. The courses are hands-on. Students write Python, reason about uncertainty, and decide what a model should and should not be used for once it leaves the notebook.</p>
        <p>Before joining Tepper I led data science at Duolingo and at UPMC. I still do that work, as Senior Director of AI and Data Science at gAIm Systems and through my consulting practice, Hot Metal Data. The problems I bring into class come from that work. I also advise MSBA capstone teams.</p>
      </div>

      <div class="tiles">
        <a class="tile" href="courses/"><div class="n">01</div><strong>Courses</strong><span>What I built and what I teach.</span></a>
        <a class="tile" href="projects/"><div class="n">02</div><strong>Projects</strong><span>Things I build for my classes.</span></a>
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
            <p>Grateful to receive the George Leland Bach Teaching Award, chosen by vote of the graduating MBA class. Many thanks to the students of the Class of 2026.</p>
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
      <p class="lede">Courses I designed come first, followed by the ones I teach.</p>

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
        history = ""
        if c.get("history"):
            paras = "".join(f"        <p>{p}</p>\n" for p in c["history"])
            history = f"        <h2>How the course developed</h2>\n{paras}"
        topics = ""
        if c.get("topics"):
            items = "".join(f"<li>{t}</li>" for t in c["topics"])
            topics = f"        <h2>Topics</h2>\n        <ol>{items}</ol>\n"
        built = '<span class="badge built">Course I built</span>' if c["built"] else ""
        body = f"""
      <article class="course-hero prose-width">
        <p class="kicker">{c['school']} · {c['program']}</p>
        <h1>{course_name(c)}</h1>
        <p>{built}</p>
        <div class="thumb {c['color']}">{course_label(c)}</div>
        <p class="lede">{c['one_liner']}</p>
        <p>{c['blurb']}</p>
{history}{topics}        <h2>Offerings</h2>
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
          <p><a href="mailto:bcollier@andrew.cmu.edu">bcollier@andrew.cmu.edu</a> · <a href="mailto:ben@collier.phd">ben@collier.phd</a> · <a href="{HOST}/">{DOMAIN_LABEL}</a></p>
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
      <p class="lede">Videos, notebooks, and workshop material I can share publicly. Enrolled students get the complete set on Canvas.</p>

      <h2>Video series</h2>
      <div class="empty">There is no public playlist yet. Walkthroughs for data mining, visualization, and the AI methods course will appear here when I publish them.</div>

      <h2>Notebooks</h2>
      <ul class="materials">
        <li><strong>Data mining labs.</strong> Python notebooks on clustering, classification, and evaluation.</li>
        <li><strong>Visualization redesigns.</strong> Before-and-after chart critiques in Tableau.</li>
        <li><strong>AI methods for social and visual data.</strong> Notebooks from the course I built, released as each offering settles.</li>
      </ul>

      <h2>Workshops</h2>
      <ul class="materials">
        <li><strong>MSBA Math Skills Workshop</strong>, developed for Summer 2026.</li>
        <li><strong>Business Analytics Summer Summit</strong>, where I taught in 2024 and 2025.</li>
        <li><strong>Hot Metal Data workshops</strong>. Outlines of my corporate training are available on request.</li>
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
      <p class="lede">Courses I built, projects I show in class, and the materials that go with them.</p>
      <div class="tiles">
        <a class="tile" href="../courses/"><div class="n">01</div><strong>Courses</strong><span>What I built and what I teach.</span></a>
        <a class="tile" href="../projects/"><div class="n">02</div><strong>Projects</strong><span>Things I build for class.</span></a>
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
    # Optional aside: context that is not the project itself, such as related
    # private work. Rendered muted so it reads as a footnote to the card.
    note = f'    <p class="note">{p["note"]}</p>\n' if p.get("note") else ""
    return f"""<article class="portfolio-item" id="{p['id']}">
  <a href="{esc(p['links'][0]['href'])}"><img class="shot" src="{root}{p['image']}" alt="{esc(p['image_alt'])}" width="{p['image_width']}" height="{p['image_height']}" loading="lazy"></a>
  <div class="body">
    <div class="meta">{esc(p['kind'])} · {esc(p['tools'])} · {esc(p['date'])}</div>
    <h2>{esc(p['title'])}</h2>
    <p>{p['summary']}</p>
    <p>{p['process']}</p>
{note}    <p class="links">{links}</p>
  </div>
</article>"""


def build_portfolio(portfolio):
    items = "\n".join(portfolio_card(p, "../") for p in portfolio)
    body = f"""
      <p class="kicker">Portfolio</p>
      <h1>Projects</h1>
      <p class="lede">Small projects I build to show my classes what current AI tools can do. Each one works, and each repo shows how it was made. More are on the way.</p>
      <div class="portfolio">{items}</div>
"""
    write(
        "projects/index.html",
        page(
            "../",
            "projects",
            "Projects · Ben Collier",
            "Projects Ben Collier builds for his classes, with source code, prompts, and build logs.",
            "projects/",
            body,
        ),
    )


def build_practice():
    body = """
      <p class="kicker">Applied work</p>
      <h1>Practice</h1>
      <p class="lede">The industry work behind my teaching.</p>

      <h2>Hot Metal Data</h2>
      <p class="prose-width">My consulting and corporate training practice. The work runs from finding the right use case, to building the model, to teaching a team to carry it on without me. Some directories list it as Hot Metal AI.</p>

      <h2>gAIm Systems</h2>
      <p class="prose-width">I am Senior Director of AI and Data Science. We build tools that help sports organizations recruit players, develop them, and put teams together on evidence rather than folklore. <a href="https://gaimsystems.com">gaimsystems.com</a></p>

      <h2>Earlier</h2>
      <ul class="prose-width">
        <li><strong>Duolingo</strong>. Staff and lead data scientist, working on experimentation, monetization analytics, and forecasting around the IPO and the launch of Duolingo Max.</li>
        <li><strong>UPMC</strong>. Senior Director of Data Science. I was the founding data scientist on a joint venture with IBM Watson Health and led CognitiveRx, which Premier later acquired.</li>
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
      <p class="lede">A dated log of teaching, advising, and practice.</p>
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
      <p class="lede">Email is the most reliable way to reach me. Students, please put the course number in the subject line.</p>
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
    paths = ["", "courses/", "materials/", "projects/", "practice/", "cv/", "news/", "contact/", "teaching/"]
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
        f"  <title>Ben Collier: news</title>\n"
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
    print(f"done: absolute URLs point at {HOST}")


if __name__ == "__main__":
    main()
