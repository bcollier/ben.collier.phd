#!/usr/bin/env python3
"""Generate the static faculty site. Run from the repo root: python3 scripts/build.py"""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from advising_art import draw as draw_art  # noqa: E402

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
        "hero": "agents",
        "number": "70-445",
        "title": "Artificial Intelligence for Business Leaders",
        "program": "Undergraduate",
        "school": "Tepper",
        "built": True,
        "color": "c-navy",
        "one_liner": "Where AI creates value in a business, where it does not, and how to explain the difference to the people paying for it.",
        "blurb": "An undergraduate course on how AI is changing organizations and the decisions managers make. The first part covers how AI works, from expert systems to machine learning, neural networks, and large language models. The second part puts students to work with AI agents on business problems. The third looks at AI in marketing, finance, people analytics, operations, and strategy, and at the ethics, economics, and regulation that decide whether adoption lasts. The semester project has three tracks. Teams can act as an AI investment committee for a real public company, build and red-team an AI agent, or try to earn $100 with a business that uses AI.",
        "offerings": [
            "Fall 2026",
        ],
        "materials": "There is no required textbook. Enrolled students find the materials on Canvas.",
        "history": [
            "I started designing this course in February 2026 and taught it for the first time on August 25, 2026. It is open to undergraduates with no prerequisites. About forty students enrolled in the first section, and several had already used AI at work during a summer internship.",
            "My first plan built the opening weeks around Pedro Domingos' The Master Algorithm and included a block on AI hardware and compute. Before the term began I dropped the hardware block, added a session on rules, search, and expert systems, and moved agentic AI and software development with AI assistance up to weeks five and six, so students work with agents before the course turns to AI in each business function.",
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
        "panel": '<figure class="panel"><figcaption>In-class exercise: the 99% accurate fraud vendor</figcaption><table><tr><th>Transactions a day</th><td>100,000</td></tr><tr><th>Fraud rate</th><td>0.5%</td></tr><tr><th>Transactions the model flags</th><td>1,490</td></tr><tr><th>Flags that are real fraud</th><td>495</td></tr><tr><th>Cost of a review / a missed fraud</th><td>$12 / $400</td></tr></table><p>At a 0.5% fraud rate, buying pays. Sell the same model to a client with 0.01% fraud and the decision flips.</p></figure>',
        "story": [
            "The agents lab sits at the center of the course. Students build a customer support team of AI agents for a fictional outdoor retailer, a manager and three specialists, then test it to find where it fails.",
            "The history of AI is taught through its predictions and its failures, with a lot of Pittsburgh in it: Newell and Simon's Logic Theorist, the Navlab van, XCON. In the third class a coding agent built puzzle solvers live while students placed their bets. A solver a student wrote by hand in 2017 scored 34 of 96 on Raven's Matrices. By the end of class the language model solver had about 86, and it claimed 99% confidence on every answer. The finished version, on the Coding with AI Projects page, scores 93.",
            "Students learn to judge where AI creates value and to defend a recommendation to executives. Much of the work is written that way: response memos, a briefing on a current AI topic, and in-class exercises like the fraud vendor above."
        ],
        "projects": {"intro": "The first final projects are due in December 2026, in three tracks: an AI investment committee for a real public company, building and breaking an AI agent, and trying to make $100 with an AI-enabled business. Revenue is not the grade. A team that earns nothing and can explain exactly why will outscore a team that earns $200 without insight.", "types": []},
    },
    {
        "slug": "45-884",
        "hero": "vit",
        "number": "45-884",
        "title": "AI Methods for Social and Visual Data",
        "program": "MBA",
        "school": "Tepper",
        "built": True,
        "color": "c-ink",
        "one_liner": "Using AI on text, networks, and images, and knowing when the output is ready for a decision.",
        "blurb": "I built this course for Tepper MBA students who need to use current AI methods on text, networks, images, and other unstructured data. We treat each model as a measuring instrument. Students should be able to say what it did, where it fails, and whether its output is good enough to act on. The labs are in Python, and we discuss ethics in the same labs as the code.",
        "offerings": [
            "Fall 2025 full-time",
            "Fall 2025 online hybrid",
            "Summer 2026",
            "Fall 2026",
        ],
        "materials": "Enrolled students get the notebooks and recordings on Canvas.",
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
        "story": [
            "There are no prerequisites and no model training. Students use foundation models from OpenAI, Anthropic, Google, and Meta on text, images, and agent workflows, and the course teaches the Python, JSON, and API calls they need along the way.",
            "Every lab compares models. Students classify product reviews with three models and weigh cost against accuracy, chain two agents that score semiconductor companies' risk from their filings, and in the computer vision class send one photograph through three generations of vision: YOLO boxes, ResNet labels, then a multimodal model that returns a shelf-restocking report as JSON.",
            "Each class opens with AI Methods in the News, a student briefing on a product or a debate from the last six months. In Fall 2025 the agents module closed with Prasad Chalasani, co-founder of the Langroid agent framework."
        ],
        "projects": {"intro": "Final projects start from a real business question. Students show how their prompts changed and compare models before settling on one. In Summer 2026, seven of the nineteen projects were built with real companies or organizations, and three are already in use. Projects from Fall 2025 and Summer 2026, grouped by type, with one example each.", "types": [["Social listening and sentiment", 7, "Reddit sentiment through an aircraft maker's safety crisis, set against its stock price"], ["Finance and investing", 5, "An autonomous equity analyst triggered from a watchlist"], ["Career, hiring, and advising agents", 4, "A five-agent job-fit scorer with a skeptical hiring-manager critic"], ["Agentic workflow automation", 3, "Automating client outreach for a real-estate agent in n8n"], ["AI governance and ethics", 3, "Human oversight of AI in intelligence analysis"], ["Document and transcript extraction", 2, "Turning sales-call transcripts into buyer intelligence"], ["Computer vision in the field", 1, "An offline tool that helps bomb-disposal teams identify ordnance"], ["Mergers and corporate culture", 1, "Predicting merger success from culture fit in annual reports"]]},
    },
    {
        "slug": "70-377",
        "hero": "teams",
        "number": "70-377",
        "title": "Managing and Assessing Tech Talent and Organizations",
        "program": "Undergraduate",
        "school": "Tepper / CMU Qatar",
        "built": True,
        "color": "c-wine",
        "one_liner": "How to hire, develop, and evaluate technical people using evidence instead of instinct.",
        "blurb": "A micro-course I developed on managing technical talent: how to interview for technical and data roles, onboard new hires, run technical projects with OKRs, and manage performance. I wrote it for undergraduates, and it ran for the first time at CMU Qatar in Fall 2025.",
        "offerings": [
            "Fall 2025, CMU Qatar",
        ],
        "materials": "Enrolled students received the materials on Canvas.",
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
        "story": [
            "Students sit on both sides of the interview table. In live mock interviews on Zoom they rotate through interviewer, candidate, and observer, using the formats large tech companies use: live coding, data take-homes, case interviews, and behavioral interviews. Candidates may solve the coding problems in a spreadsheet, so business students take part alongside computer science students.",
            "The in-person week in Doha turned to teams and culture. Groups allocated a $120 million fund across twenty proposals, analyzed a Harvard case on a global team at Sun Microsystems, and rescued a failing mobile banking project by cutting its scope and writing recovery OKRs."
        ],
    },
    {
        "slug": "msba-math-skills-workshop",
        "hero": "descent",
        "number": "",
        "label": "Math Skills",
        "title": "MS in Business Analytics Math Skills Workshop",
        "program": "MS in Business Analytics",
        "school": "Tepper",
        "built": True,
        "color": "c-clay",
        "one_liner": "The math incoming MS in Business Analytics students need before the quantitative core begins.",
        "blurb": "A workshop I developed for incoming MS in Business Analytics students in Summer 2026. The goal is for students to start the program's quantitative courses with the mathematics already in place, so they are not learning it at the same time as the statistics.",
        "offerings": [
            "Summer 2026",
        ],
        "materials": "Incoming MS in Business Analytics students take the workshop on Canvas.",
        "history": [
            "A self-paced online course for incoming MS in Business Analytics students, built with Tepper's learning technologies team between December 2025 and August 2026. I recorded every lesson, about thirty short videos across six modules, each pairing slides with worked problems written out by hand.",
        ],
        "topics": [
            "Algebra fundamentals and functions",
            "Calculus for analytics: derivatives, optimization, and gradient descent",
            "Linear algebra for data analytics: matrices, eigenvalues, least squares, PCA, and PageRank",
            "Descriptive statistics",
            "Probability foundations",
            "Statistical inference: sampling distributions, confidence intervals, and hypothesis tests",
        ],
        "story": [
            "Each module ends where an analytics course picks up. Calculus ends with gradient descent and the sigmoid. Linear algebra ends with the normal equations, PCA, and PageRank. Probability works through a fraud alert that is 99% sensitive and still right only 9% of the time at a 0.5% base rate.",
            "I wrote the scope and sequence with the MS in Business Analytics core faculty, working backward from what their courses need. Before recording, I checked every equation symbolically."
        ],
    },
    {
        "slug": "45-851",
        "hero": "kmeans",
        "number": "45-851",
        "title": "Data Mining",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-rust",
        "one_liner": "Finding structure in messy business data, then deciding whether to trust it.",
        "blurb": "Tepper's MBA data mining course, which I have taught six times since 2023. It covers clustering, PCA, regression, classification, forecasting, and text, with labs in Python, and it keeps asking what each model is for. Labs are in Python. The goal is not a long list of algorithms. It is a workflow students can apply to an unfamiliar dataset the week after the course ends.",
        "offerings": [
            "Fall 2023 full-time",
            "Spring 2024 online hybrid",
            "Fall 2024 full-time",
            "Spring 2025 online hybrid",
            "Fall 2025 full-time",
            "Fall 2025 online hybrid",
        ],
        "materials": "Enrolled students get the notebooks and video walkthroughs on Canvas.",
        "history": [
            "I first taught Data Mining in Fall 2023, as an adjunct, to full-time MBA students. I taught it every fall and spring through Fall 2025, in both the full-time and the online hybrid programs.",
            "The first version was in R. For the Spring 2024 online hybrid section I scripted and recorded a video module for each topic. In Fall 2024 I moved the whole course to Python and then re-recorded the videos, and Fall 2025 added principal component analysis.",
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
        "story": [
            "The course is organized around business questions, not algorithms. Each module opens with one a manager would ask: which customers look alike, what a house will sell for, who is about to leave, what customers are saying in their reviews. The first class is a case from my own work, predicting drug price spikes for a 40-hospital health system that buys $1.5 billion of pharmaceuticals a year, followed from the business question to a commercial product.",
            "Students work the way analysts work now. Labs are in Python in Colab, generative AI is allowed, and teams hand in their AI chat transcripts with the work. The classification project is a prediction competition: every team scores a holdout file, I grade the predictions against the true labels, and the top fifth earn extra credit."
        ],
        "projects": {"intro": "In the final project, teams bring their own business question and data, often from their own employer, and answer it with a method from the course. Projects from Spring 2024, Fall 2024, and Spring 2025, grouped by type, with one example each.", "types": [["Finance, markets, and credit risk", 6, "Do a CEO's posts move an electric carmaker's stock price?"], ["Sports analytics", 5, "Predicting baseball Hall of Fame induction from career statistics"], ["Healthcare and wellbeing", 5, "Does wearing a fitness tracker go with better health?"], ["Customer segmentation and retail", 4, "Segmenting 85 grocery stores by their department sales mix"], ["Transportation and mobility", 4, "Where should Pennsylvania put new EV chargers?"], ["Churn, retention, and satisfaction", 3, "Predicting and segmenting airline passenger satisfaction"], ["Real estate and places", 3, "What drives Airbnb nightly prices in New York?"], ["Economic forecasting", 2, "Forecasting US retail sales with Prophet"], ["Media and entertainment", 2, "What predicts a song's stream count?"]]},
    },
    {
        "slug": "45-885",
        "hero": "charts",
        "number": "45-885",
        "title": "Data Visualization",
        "program": "MBA",
        "school": "Tepper",
        "built": False,
        "color": "c-olive",
        "one_liner": "Charts and dashboards designed to change a decision.",
        "blurb": "A Tableau course for MBA students on designing charts and dashboards for executives, and on spotting graphics that mislead. Students design charts and dashboards for executive audiences, and they learn enough about perception and statistics to spot a graphic that misleads.",
        "offerings": [
            "Spring 2024 evening",
            "Spring 2025 full-time",
            "Spring 2025 online hybrid",
            "Fall 2025 full-time",
            "Spring 2026 full-time",
            "Spring 2026 online hybrid",
        ],
        "materials": "Enrolled students get the Tableau workbooks and screencast lessons on Canvas.",
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
        "story": [
            "No programming is required. Students start as Tableau beginners and finish with calculated fields, parameters, maps, interactive dashboards, and animation. Along the way they rebuild Hans Rosling's Gapminder bubble chart from raw World Bank tables.",
            "Every class opens with a team critiquing a data story published in the last six months, in the Financial Times, the Wall Street Journal, The Economist, or ProPublica, and remaking two or three of its charts. Before presenting, teams test their redesign with an AI Data Visualization Coach, a custom GPT I built with my colleague Zoey Jiang. It will not hand over a redesign. It questions the team from three seats: a journalist, a chart designer, and a business stakeholder.",
            "After dashboards, the course covers clustering, network graphs, and explainable AI, so students can chart what a model found and why."
        ],
        "projects": {"intro": "The final project is a Tableau workbook with an interactive dashboard and a recorded video that tells its story. Students choose their own question or one of two public datasets. Projects from Spring 2024 and Spring 2025, grouped by type, with one example each.", "types": [["Netflix content strategy", 10, "Where Netflix's catalog grew, country by country"], ["Public sector, policy, and society", 10, "Neighborhood income change by zip code in a US metro"], ["Economics, labor, and prices", 5, "Why eggs got expensive: 50 years of food prices"], ["Business performance dashboards", 5, "Does discounting drive profit? An executive retail dashboard"], ["Media and the creator economy", 4, "What drives YouTube creator revenue?"], ["Climate and environment", 4, "25 years of warming, city by city"], ["Sports", 2, "Does payroll buy wins in baseball?"], ["Consumer products", 2, "Do electric cars deliver their certified range?"]]},
    },
    {
        "slug": "46-885",
        "hero": "brush",
        "number": "46-885",
        "title": "Data Exploration and Visualization",
        "program": "MS in Business Analytics",
        "school": "Tepper",
        "built": False,
        "color": "c-pine",
        "one_liner": "The MS in Business Analytics program's Tableau course: chart design, data stories, dashboards, and visualization for machine learning.",
        "blurb": "The MS in Business Analytics counterpart to 45-885 Data Visualization: seven weekly modules in Tableau, with the same labs, weekly data stories, and AI coach as the MBA course, ending on explainable AI and visualization for machine learning.",
        "offerings": ["Spring 2025 online hybrid", "Spring 2026"],
        "materials": "Enrolled students get the workbooks and lessons on Canvas.",
        "history": [
            "I first taught it in Spring 2025 and again in Spring 2026, with one session a week. It follows the MBA online hybrid syllabus module for module, with typography and color folded into the design sessions, and ends with the same recorded data story.",
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
        "story": [
            "Students use the same labs, weekly data stories, and AI coach as the MBA sections. The last module covers explainable AI and visualization for machine learning, so the course ends where their machine learning courses begin."
        ],
    },
    {
        "slug": "46-880",
        "hero": "galton",
        "number": "46-880",
        "title": "Introduction to Probability and Statistics",
        "program": "MS in Business Analytics",
        "school": "Tepper",
        "built": False,
        "color": "c-slate",
        "one_liner": "Probability and inference taught twice over, in Excel and in Python, through business decisions.",
        "blurb": "The first quantitative course in the full-time MS in Business Analytics: probability, distributions, sampling, estimation, hypothesis tests, and regression.",
        "offerings": ["Fall 2024 full-time"],
        "materials": "Students received the problem sets and walkthrough videos on Canvas.",
        "history": [
            "I taught the MS in Business Analytics program's first-term statistics course in Fall 2024, in two morning sections. I reworked the slide decks I inherited and used Excel and Python alongside the textbook, so that every idea had both a formula and a working example.",
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
        "story": [
            "Every distribution is taught twice, once with its Excel formula and once with its Python call, and nearly every example is a business decision: overbooking a flight, a cosmetics launch whose chance of success moves from 30% to 60% after a market test, tea bottles that must hold 750 ml. Sessions open with a puzzle or a question from quant interviews.",
            "Halfway through the seven-week term I changed the pace: more worked examples in class, practice sets with solutions, a short written summary of each module, and walkthrough videos for the hardest problems."
        ],
    },
    {
        "slug": "46-887",
        "hero": "pipeline",
        "number": "46-887",
        "title": "Machine Learning for Business Applications",
        "program": "MS in Business Analytics",
        "school": "Tepper",
        "built": False,
        "color": "c-copper",
        "one_liner": "Taking a model out of the notebook and into a working business system on AWS.",
        "blurb": "Applied machine learning for MS in Business Analytics students, built around a cloud pipeline on AWS.",
        "offerings": ["Spring 2026"],
        "materials": "Enrolled students get the lab notebooks on Canvas.",
        "history": [
            "I redesigned this MS in Business Analytics course for Spring 2026 around one question: how a trained model becomes part of a working business system. Mondays are lecture and Wednesdays are lab. Students build pipelines on AWS, put the results in Tableau or Streamlit dashboards, and finish with a team project demo.",
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
        "story": [
            "The course takes models out of the notebook and into production. Students put data in S3, score it with Lambda and SageMaker, write predictions to a database they provision themselves on RDS, and read them live in Tableau or Streamlit.",
            "Accuracy is the first number students learn to distrust. The fraud lab opens with a one-line model that never flags fraud and is still 99.8% accurate, then works through class weights, SMOTE, and isolation forests on a precision-recall leaderboard. In ML Project Triage, teams sit on an insurer's strategy board with money for two of six proposals, among them a drone moonshot with no data and a pricing engine that would be illegal in most states.",
            "The team project is a working proof of concept: a model, a cloud database of its predictions, and a dashboard, shown in a live demo."
        ],
    },
    {
        "slug": "90-803",
        "hero": "network",
        "number": "90-803",
        "title": "Machine Learning Foundations with Python",
        "program": "Public Policy & Management",
        "school": "Heinz College",
        "built": False,
        "color": "c-navy",
        "one_liner": "Machine learning in Python for students headed into policy and management work.",
        "blurb": "A full-semester course at Heinz College that teaches machine learning with Python to students who will apply it to public policy and management problems.",
        "offerings": ["Spring 2026 full-time"],
        "materials": "Heinz students get the full materials on Canvas.",
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
        "story": [
            "Every method is framed as a policy question: which households in a broadband subsidy program are about to drop out, how to route thousands of student loan complaints, whether a language model and a person agree on how serious a complaint is. In the language model project, students have a model sort complaints into six policy categories and measure its agreement with other models using Cohen's kappa.",
            "Instead of one end-of-term project, students do four applied projects across the semester (clustering, classification, language models, and computer vision), a midterm project for a public agency or nonprofit, and a final project with a three- to five-minute pitch. A CMU alum working as a product data scientist gave a guest lecture on machine learning for product decisions."
        ],
    },
]

NEWS = [
    # (date, text) or (date, text, link). A link makes the item point somewhere.
    # Newest first.
    ("2026-08-25", "Taught the first class of 70-445 Artificial Intelligence for Business Leaders, a new undergraduate course I built. Students learn how AI works, work hands-on with AI agents, and then judge where AI creates value across marketing, finance, operations, and strategy, and how to defend that judgment to executives."),
    ("2026-08-24", "Started the third run of 45-884 AI Methods for Social and Visual Data, with agents moved earlier in the term and a summary and cleaned transcript for students after every class."),
    ("2026-08", "Finished recording the MS in Business Analytics Math Skills Workshop, a self-paced course for incoming MS in Business Analytics students that runs from algebra through gradient descent, PCA, and statistical inference."),
    ("2026-06-10", "George Leland Bach Teaching Award, voted by the MBA Class of 2026."),
    ("2026-06", "Really proud of this summer's AI Methods final projects. Three of the nineteen are already in use, and they range from social listening on an aircraft maker's safety crisis to an offline tool that helps bomb-disposal teams identify ordnance."),
    ("2026-05-04", "Taught AI Methods for Social and Visual Data for the second time, rebuilt for the summer with one live session a week and hands-on Python videos for every module."),
    ("2026-04-30", "Talked with Tepper for a Faculty Spotlight on what students learn in the MS in Business Analytics, and why I describe business analytics as a decathlon.", "https://www.youtube.com/watch?v=UxBPkez6Mc4"),
    ("2026-03-11", "Started teaching 46-887 Machine Learning for Business Applications to the in-person MS in Business Analytics cohort, redesigned around AWS. Students take a model from S3 through SageMaker to a database they run themselves and a live dashboard."),
    ("2026-01-13", "Started teaching 90-803 Machine Learning Foundations with Python at Heinz College, rebuilt around four applied projects on policy questions, from broadband subsidies to student loan complaints."),
    ("2026-01", "Advising two MS in Business Analytics capstone teams this spring."),
    ("2025-10-22", "Taught 70-377 Managing and Assessing Tech Talent and Organizations for CMU Qatar, my first course in Doha since 2016: mock technical interviews on Zoom, then an in-person week on teams and culture."),
    ("2025-10", "Taught Data Mining in person and online hybrid in the same seven-week term, and added principal component analysis to the course."),
    ("2025-08-26", "Taught the first class of 45-884 AI Methods for Social and Visual Data, a course I built for MBA and master's students on text, images, and AI agents, using foundation models rather than training them."),
    ("2025-05", "Joined gAIm Systems as Senior Director of AI and Data Science."),
    ("2025-05", "Proud of this spring's Data Mining final projects: teams brought their own questions, from predicting baseball Hall of Fame induction to siting EV chargers in Pennsylvania."),
    ("2025-03", "This spring's Data Visualization final projects were 29 recorded data stories, from Netflix's global catalog to city-by-city warming and public-sector dashboards."),
    ("2025-01-13", "Rebuilt Data Visualization entirely in Tableau for its second run, added clustering, network graphs, and explainable AI, and recorded about fifty short screencast lessons. Also started teaching its MS in Business Analytics counterpart, 46-885."),
    ("2025-01", "Advised five MS in Business Analytics capstone projects."),
    ("2024-10", "Taught Data Mining for the third time and moved it from R to Python, adding time series forecasting and a session on building data-driven products to clustering, regression, classification, and text mining."),
    ("2024-08-26", "Started teaching 46-880 Introduction to Probability and Statistics, the first quantitative course in the full-time MS in Business Analytics, pairing every distribution with its Excel formula and its Python call."),
    ("2024-08", "Joined Tepper as Assistant Teaching Professor of Business Analytics."),
    ("2024-06", "Taught in the Business Analytics Summer Summit."),
    ("2024-05", "Proud of the first Data Mining final projects: sixteen online hybrid MBA teams, many working on data from their own employers."),
    ("2024-03-13", "Started teaching 45-885 Data Visualization with an evening MBA section, mixing Tableau with R and ggplot2."),
    ("2024-03", "Taught Data Mining for the second time, rebuilt for the online hybrid MBA with a recorded video module for each topic and a self-directed final project in place of the exam."),
    ("2024-01", "Advising three MS in Business Analytics capstone teams this spring, with Tindoori Labs, Marinus Analytics, and 412 Food Rescue."),
    ("2023-10-25", "Started teaching 45-851 Data Mining to full-time MBA students as an adjunct, redesigning it around business questions, with labs in R and tidymodels."),
]


HERO_ALT = {
    "kmeans": "Animation: k-means clustering moves four centroids until the clusters settle",
    "vit": "Animation: an image split into patches passes up a transformer stack and becomes a caption",
    "agents": "Animation: an orchestrator agent sends work to research, CRM, email, evaluation, and code tools in turn",
    "charts": "Animation: one dataset changes from a bar chart to a scatter plot to a slope graph",
    "brush": "Animation: brushing points in a scatter plot highlights the same records in a histogram",
    "galton": "Animation: balls fall through a Galton board and the bins build a normal curve",
    "pipeline": "Animation: data flows from storage through training to a model API and a dashboard",
    "network": "Animation: a signal passes forward through the layers of a neural network",
    "descent": "Animation: gradient descent steps down a loss surface toward the minimum",
    "teams": "Animation: scattered people come together into four teams",
}


BOOK_EMAIL = "ben@collier.phd"
HOURLY_RATE = "$450"


def book_call(root: str, cls: str = "btn primary") -> str:
    """The one booking entry point used across the site. It always goes to /book/."""
    return f'<a class="{cls}" href="{root}book/">Book a free 15-minute call</a>'


def book_link(kind: str, label: str, root: str, cls: str = "btn primary") -> str:
    """A booking button. Until a Cal.com URL is set in js/config.js it is an
    honest "Email to book" link; js/site.js builds the email (the address is
    never written into the page, to keep it from address harvesters) and
    swaps in the URL and live label once one is configured. Without
    JavaScript it falls back to the contact page."""
    subject = {"freeChat": "Free 15-minute call", "paidHour": "Consulting hour"}[kind]
    fallback = "Email to " + label[0].lower() + label[1:]
    return (f'<a class="{cls}" data-book="{kind}" data-subject="{esc(subject)}" '
            f'data-live-label="{esc(label)}" href="{root}contact/">{esc(fallback)}</a>')


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
      <a class="wordmark" href="{root}">Ben Collier, PhD</a>
      <nav class="primary" aria-label="Primary">
        {item("courses/", "courses", "courses")}
        {item("projects/", "coding with AI projects", "projects")}
        {item("advising/", "advising", "advising")}
        {item("consult/", "consulting", "consult")}
        {item("cv/", "cv", "cv")}
        {item("news/", "news", "news")}
        {item("contact/", "contact", "contact")}
        <a class="nav-cta" href="{root}book/"{' aria-current="page"' if active == "book" else ""}>Book a call</a>
      </nav>
    </header>
    <main id="main">
"""


def footer(root: str) -> str:
    return f"""    </main>
    <footer class="site">
      <div>Ben Collier · Tepper School of Business · Carnegie Mellon University</div>
      <div><a href="{root or './'}">{DOMAIN_LABEL}</a> · <a href="https://github.com/bcollier/ben.collier.phd/releases/tag/cs15-113-submission">Version submitted for 15-113 (2026)</a> · <a href="{root}consult/">Consulting</a> · <a href="{root}feed.xml">News feed</a> · <a href="https://github.com/bcollier/ben.collier.phd">Source</a></div>
    </footer>
  </div>
  <script src="{root}js/config.js"></script>
  <script src="{root}js/site.js"></script>
  <script src="{root}js/course-hero.js" defer></script>
</body>
</html>
"""


def page(root, active, title, desc, canon, body, jsonld="") -> str:
    return header(root, active, title, desc, canon, jsonld) + body + footer(root)


PERSONAL_EMAIL = "ben@collier.phd"


def hide_email(html: str) -> str:
    """Replace the personal address with markup that js/site.js turns back
    into a working link. The finished page shows ben@collier.phd, but the HTML
    never contains it, which defeats most address-harvesting scrapers."""
    user, domain = PERSONAL_EMAIL.split("@")
    tag = f'<a class="eml" data-u="{user}" data-d="{domain}">{user} [at] {domain}</a>'
    html = html.replace(f'<a href="mailto:{PERSONAL_EMAIL}">{PERSONAL_EMAIL}</a>', tag)
    return html.replace(PERSONAL_EMAIL, tag)


def write(rel, content: str):
    if rel.endswith(".html"):
        content = hide_email(content)
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
  <div class="thumb {c['color']}"><canvas data-hero="{c['hero']}" data-static aria-hidden="true"></canvas><span>{course_label(c)}</span></div>
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
    for iso, text, *link in items:
        more = f' <a href="{esc(link[0])}">Watch the video</a>' if link else ""
        out.append(
            f'<li><time datetime="{iso}">{human_date(iso)}</time>'
            f'<div class="post"><p>{text}{more}</p></div></li>'
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
          <p class="lede">I teach AI and business analytics at Carnegie Mellon's Tepper School, and help companies put them to work.</p>
        </div>
      </section>

      <div class="bio">
        <p>Most of my teaching is at Tepper, in the MBA, the MS in Business Analytics, and the undergraduate program. I also teach at Heinz College. The courses are hands-on. Students write Python, reason about uncertainty, and decide what a model should and should not be used for once it leaves the notebook.</p>
        <p>Before joining Tepper I was a staff data scientist at Duolingo and Senior Director of Data Science at UPMC's Pensiamo, where I was the founding data scientist on a joint venture with IBM Watson Health. I still do that work, as Senior Director of AI and Data Science at gAIm Systems and through my consulting practice, Hot Metal Data. The problems I bring into class come from that work. I also advise MS in Business Analytics capstone teams.</p>
      </div>

      <div class="book-row">
        {book_call("")}
        <a class="btn" href="consult/">Consulting and custom education</a>
      </div>

      <ul class="stats">
        <li><strong>{sum(1 for c in COURSES if c["built"])}</strong><span>courses I designed from scratch</span></li>
        <li><strong>{len(COURSES)}</strong><span>courses taught at Carnegie Mellon since 2023</span></li>
        <li><strong>{len(load_json("advising.json")["projects"])}</strong><span>capstones and independent studies advised since 2024</span></li>
        <li><strong>2026</strong><span>George Leland Bach Teaching Award, voted by the MBA class</span></li>
      </ul>

      <h2>Courses I built</h2>
      <div class="grid" style="margin-top:1rem">{cards}</div>
      <p><a href="courses/">All courses</a></p>

      <h2>News</h2>
      {news_items(5)}
      <p><a href="news/">All news</a> · <a href="cv/">Full CV</a></p>
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
      <p class="lede">Courses I designed from scratch, then courses I took over and rebuilt.</p>

      <h2>Courses I built</h2>
      <div class="grid">{built}</div>

      <h2>Courses I took over and rebuilt</h2>
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


# Courses with an obvious version for company teams get a closing prompt.
CORPORATE_VERSIONS = {"70-445", "45-884", "45-851", "45-885", "46-887"}


def build_course_pages():
    for c in COURSES:
        def chip(o):
            kind = "hybrid" if "hybrid" in o else "evening" if "evening" in o else "qatar" if "Qatar" in o else "term"
            return f'<li class="chip {kind}">{o}</li>'
        offerings = "".join(chip(o) for o in c["offerings"])
        history = ""
        if c.get("history"):
            paras = "".join(f"        <p>{p}</p>\n" for p in c["history"])
            history = f"        <h2>How the course developed</h2>\n{paras}"
        story = ""
        if c.get("story"):
            paras = "".join(f"        <p>{p}</p>\n" for p in c["story"])
            story = f"        <h2>How the course works</h2>\n{paras}"
        projects = ""
        pj = c.get("projects")
        if pj:
            top = max([n for _, n, _ in pj["types"]] or [1])
            rows = "".join(
                f'<li><div class="bar-head"><strong>{t}</strong><span class="count">{n}</span></div>'
                f'<div class="bar" style="width:{max(6, round(100 * n / top))}%"></div>'
                f'<span class="example">{ex}</span></li>'
                for t, n, ex in pj["types"]
            )
            lst = f'        <ul class="project-types">{rows}</ul>\n' if rows else ""
            projects = f"        <h2>Final projects</h2>\n        <p>{pj['intro']}</p>\n{lst}"
        topics = ""
        if c.get("topics"):
            items = "".join(f"<li>{t}</li>" for t in c["topics"])
            topics = f"        <h2>Topics</h2>\n        <ol>{items}</ol>\n"
        built = '<span class="badge built">Course I built</span>' if c["built"] else ""
        cta = ""
        if c["slug"] in CORPORATE_VERSIONS:
            cta = f"""      <aside class="course-cta prose-width">
        <p>I also teach versions of this material to company teams, using their own data. <a href="../../consult/#education">Custom education</a></p>
        {book_call("../../")}
      </aside>
"""
        body = f"""
      <article class="course-hero prose-width">
        <p class="kicker">{c['school']} · {c['program']}</p>
        <h1>{course_name(c)}</h1>
        <p>{built}</p>
        <div class="thumb hero {c['color']}"><canvas data-hero="{c['hero']}" role="img" aria-label="{esc(HERO_ALT[c['hero']])}"></canvas><span>{course_label(c)}</span></div>
        <p class="lede">{c['one_liner']}</p>
        <p>{c['blurb']}</p>
        {c.get('panel', '')}
{topics}{story}{projects}{history}        <h2>Offerings</h2>
        <ul class="chips">{offerings}</ul>
        <p class="muted">{c['materials']}</p>
      </article>
{cta}
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
    {''.join(['<ul class="stats small">'] + [f'<li><strong>{v}</strong><span>{k}</span></li>' for k, v in p.get('stats', [])] + ['</ul>']) if p.get('stats') else ''}
    <p>{p['summary']}</p>
    {('<ul class="decisions">' + ''.join(f'<li>{d}</li>' for d in p['decisions']) + '</ul>') if p.get('decisions') else f"<p>{p['process']}</p>"}
{note}    <p class="links">{links}</p>
  </div>
</article>"""


def build_portfolio(portfolio):
    items = "\n".join(portfolio_card(p, "../") for p in portfolio)
    body = f"""
      <p class="kicker">Portfolio</p>
      <h1>Coding with AI Projects</h1>
      <p class="lede">Working projects I built with AI coding tools, several of them for 15-113 Effective Coding with AI. Each repo includes the prompts and build log, and I use them as examples in class.</p>
      <div class="portfolio">{items}</div>
"""
    write(
        "projects/index.html",
        page(
            "../",
            "projects",
            "Coding with AI Projects · Ben Collier",
            "Coding with AI projects Ben Collier builds for his classes, with source code, prompts, and build logs.",
            "projects/",
            body,
        ),
    )


def build_practice():
    """Practice was merged into Consulting. Keep the old URL working."""
    write(
        "practice/index.html",
        '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">'
        '<title>Consulting · Ben Collier</title>'
        f'<link rel="canonical" href="{HOST}/consult/">'
        '<meta http-equiv="refresh" content="0; url=../consult/#background">'
        '</head><body><p><a href="../consult/#background">This page moved to Consulting.</a></p></body></html>\n',
    )

def build_advising():
    data = load_json("advising.json")
    terms = []
    for pj in data["projects"]:
        if pj["term"] not in terms:
            terms.append(pj["term"])
    sections = []
    for term in terms:
        cards = []
        for i, pj in enumerate(x for x in data["projects"] if x["term"] == term):
            methods = "".join(f"<li>{esc(m)}</li>" for m in pj["methods"])
            art = draw_art(pj["art"], f"Diagram representing the project: {esc(pj['title'])}", i)
            cards.append(f"""        <article class="advised">
          {art}
          <div class="body">
            <p class="meta">{esc(pj['kind'])} · {esc(pj['partner'])} · {esc(pj['industry'])}</p>
            <h3>{esc(pj['title'])}</h3>
            <p>{esc(pj['summary'])}</p>
            <ul class="methods">{methods}</ul>
          </div>
        </article>""")
        sections.append(f"      <h2>{term}</h2>\n" + "\n".join(cards))
    earlier = "".join(
        f"<li><span>{esc(e['term'])}</span> {esc(e['title'])}. <em>{esc(e['place'])}</em></li>" for e in data["earlier"]
    )
    n = len(data["projects"])
    body = f"""
      <p class="kicker">Advising</p>
      <h1>Capstones and independent studies</h1>
      <p class="lede">Since 2024 I have advised MS in Business Analytics capstone teams working with companies and nonprofits, and students doing independent studies. {n} projects so far, described here without the students' names and without the partners' data.</p>
      <p class="partners">Partners include Westinghouse, RBC Wealth Management, Swank Construction, SaratogaRIM, Confirmed, Marinus Analytics, 412 Food Rescue, Tindoori Labs, and a large consulting firm.</p>
{chr(10).join(sections)}

      <h2>Earlier advising</h2>
      <p class="prose-width">Independent studies I advised while teaching organizational behavior, mostly at Carnegie Mellon's campus in Qatar.</p>
      <ul class="earlier-list">{earlier}</ul>
"""
    write(
        "advising/index.html",
        page(
            "../",
            "advising",
            "Advising · Ben Collier",
            "MS in Business Analytics capstone projects and independent studies Ben Collier has advised, with Westinghouse, RBC, Swank, SaratogaRIM, Confirmed, Marinus Analytics, 412 Food Rescue, and others.",
            "advising/",
            body,
        ),
    )


def build_consult():
    body = f"""
      <p class="kicker">Consulting</p>
      <h1>Consulting and custom education</h1>
      <p class="lede">I help organizations choose which AI and analytics projects to fund, check the models before they carry a real decision, and train their teams to run the work themselves. I do this through my practice, Hot Metal Data.</p>

      <div class="kinds">
        <section class="kind" id="education">
          <p class="offer-meta">Custom education</p>
          <h2>Training built on your data</h2>
          <p>Workshops and courses for technical teams and executives, built around your own data and problems. Most of the time is spent in hands-on labs.</p>
          <h3>Formats</h3>
          <ul>
            <li>One- to three-day workshops, on site or online</li>
            <li>Multi-week programs for technology leaders and executives</li>
            <li>Recorded, self-paced courses</li>
          </ul>
          <h3>Examples</h3>
          <ul>
            <li>Professional development courses for technology leaders and executives at Optum, AT&amp;T, Cox Communications, and RapidScale.</li>
            <li>Workshops on chatbot development, data programming, SQL and NoSQL, data mining, cloud infrastructure, and agile development.</li>
            <li>The kind of recorded course I can build for a team: the <a href="../courses/msba-math-skills-workshop/">MS in Business Analytics Math Skills Workshop</a>, about thirty short videos I scripted and recorded for incoming Carnegie Mellon MS in Business Analytics students.</li>
          </ul>
        </section>

        <section class="kind" id="ai-data">
          <p class="offer-meta">AI and data consulting</p>
          <h2>Reviews and builds</h2>
          <p>From deciding which AI projects are worth funding to reviewing a model before it carries a real decision.</p>
          <h3>Formats</h3>
          <ul>
            <li><strong>AI use-case review.</strong> About two weeks. A written go or no-go on the projects you are considering, with a build plan for the ones worth doing.</li>
            <li><strong>Model or metric review.</strong> About one week. I read the code, data, and evaluation, and tell you where it breaks.</li>
            <li><strong>Hands-on build.</strong> Scoped with you: a prototype, a pipeline, or an evaluation harness your team can keep running.</li>
          </ul>
          <h3>Through Hot Metal Data</h3>
          <ul>
            <li>A recommendation engine for healthcare specialist referrals, built for a healthcare client.</li>
          </ul>
          <h3>In industry roles</h3>
          <ul>
            <li>At UPMC's Pensiamo, as founding data scientist on a joint venture with IBM Watson Health, I did the machine learning research and built the production pipelines for CognitiveRx, a drug price and shortage tool for a 40-hospital system buying $1.5 billion of pharmaceuticals a year. Premier later acquired it.</li>
            <li>At Duolingo, experimentation, monetization analytics, and forecasting through the IPO and the launch of Duolingo Max.</li>
            <li>At gAIm Systems, AI tools and research studies that help sports teams recruit players, develop them, and build rosters.</li>
          </ul>
        </section>
      </div>

      <p class="prose-width">I also advise MS in Business Analytics capstone teams working with companies such as Westinghouse, RBC Wealth Management, and Swank Construction. <a href="../advising/">See those projects</a>.</p>

      <div class="book-row">
        <a class="btn primary" href="../book/">Book time</a>
        <span class="muted">Most engagements start with a free 15-minute call.</span>
      </div>

      <h2 id="background">Background</h2>
      <ol class="timeline">
        <li><span>2025 to now</span><strong>gAIm Systems</strong> Senior Director of AI and Data Science</li>
        <li><span>2023 to now</span><strong>Tepper School of Business, Carnegie Mellon</strong> Assistant Teaching Professor of Business Analytics, after starting as an adjunct in Fall 2023</li>
        <li><span>2020 to 2023</span><strong>Duolingo</strong> Senior, lead, then staff data scientist, on monetization</li>
        <li><span>2018 to now</span><strong>Hot Metal Data</strong> Founder. Analytics consulting and corporate training, alongside everything else</li>
        <li><span>2016 to 2020</span><strong>UPMC's Pensiamo</strong> Data scientist, then Senior Director of Data Science</li>
        <li><span>2012 to 2016</span><strong>Carnegie Mellon University in Qatar</strong> Assistant Teaching Professor of Organizational Behavior, and co-director of executive education</li>
      </ol>
      <p><a href="../cv/">Full CV</a></p>
"""
    write(
        "consult/index.html",
        page(
            "../",
            "consult",
            "Consulting · Ben Collier",
            "Custom education and AI and data consulting from Ben Collier: workshops built on your data, AI use-case reviews, and model and metric reviews.",
            "consult/",
            body,
        ),
    )


def build_book():
    body = f"""
      <p class="kicker">Book time</p>
      <h1>Book a call</h1>
      <p class="lede">Start with a free intro call, or book a working hour on a specific problem. Not sure what you need? See the kinds of <a href="../consult/">consulting and custom education</a> I do.</p>

      <div class="offers">
        <section class="offer">
          <p class="offer-meta">15 minutes · online · free</p>
          <h2>Intro call</h2>
          <p>A short call to see whether I can help. Tell me what you are working on, and I will tell you plainly whether it is a fit and what a sensible first step would be.</p>
          {book_link("freeChat", "Book a free 15-minute call", "../")}
        </section>
        <section class="offer">
          <p class="offer-meta">60 minutes · online · {HOURLY_RATE}</p>
          <h2>Consulting hour</h2>
          <p>One working session on a decision you are stuck on: a model that will not hold up, a metric nobody trusts, an AI use case you are not sure is worth building, or a hiring bar for a data team.</p>
          <ul>
            <li>Live session on Zoom or Google Meet</li>
            <li>A one-page written recommendation within two business days</li>
            <li data-live-text="Paid when you book">Invoiced before we meet</li>
          </ul>
          {book_link("paidHour", "Book a consulting hour", "../")}
        </section>
      </div>

      <h2>Which option fits</h2>
      <ul class="prose-width">
        <li><strong>Not sure yet?</strong> Start with the intro call. It is free, and by the end you will know whether you need anything more.</li>
        <li><strong>One specific decision or blocker?</strong> A consulting hour is usually enough.</li>
        <li><strong>Training for a team, or a project that needs weeks?</strong> Book the intro call and we will scope <a href="../consult/#education">custom education</a> or <a href="../consult/#ai-data">AI and data consulting</a>.</li>
      </ul>

      <p class="prose-width">Prefer email? Write to <a href="mailto:{BOOK_EMAIL}">{BOOK_EMAIL}</a>.</p>
"""
    write(
        "book/index.html",
        page(
            "../",
            "book",
            "Book a call · Ben Collier",
            "Book a free 15-minute intro chat or a consulting hour with Ben Collier.",
            "book/",
            body,
        ),
    )

def build_news():
    body = f"""
      <p class="kicker">Teaching and practice</p>
      <h1>News</h1>
      <p class="lede">A dated log of teaching, advising, and practice.</p>
      {news_items()}
      <h2>On LinkedIn</h2>
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
      <h1>Contact</h1>
      <p class="lede">Email is the most reliable way to reach me. Students, please put the course number in the subject line.</p>
      <ul class="contact-list">
        <li><span>CMU email</span><div><a href="mailto:bcollier@andrew.cmu.edu">bcollier@andrew.cmu.edu</a></div></li>
        <li><span>Personal</span><div><a href="mailto:ben@collier.phd">ben@collier.phd</a></div></li>
{'        <li><span>Site</span><div><a href="../">' + DOMAIN_LABEL + '</a></div></li>' + chr(10) if SITE.get("domain_live") else ""}        <li><span>Office</span><div>Tepper School of Business<br>Carnegie Mellon University<br>5000 Forbes Avenue<br>Pittsburgh, PA 15213</div></li>
        <li><span>Consulting</span><div>{book_call("../", "")} · <a href="../consult/">Consulting and custom education</a></div></li>
        <li><span>Students</span><div><a data-book="studentHours" data-live-label="Book a 30-minute appointment" href="mailto:bcollier@andrew.cmu.edu">Email me</a> two times that work for office hours and I will confirm one.</div></li>
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
      <p><a href="./">Home</a> · <a href="./courses/">Courses</a> · <a href="./projects/">Coding with AI Projects</a> · <a href="./cv/">CV</a></p>
"""
    write(
        "404.html",
        page("", "home", "Not found · Ben Collier", "Page not found.", "404.html", body),
    )


def site_paths():
    """Every canonical URL path on the site, in navigation order."""
    paths = ["", "consult/", "book/", "advising/", "courses/", "projects/", "cv/", "news/", "contact/"]
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
    for iso, text, *link in NEWS:
        stamp = rfc3339(iso)
        href = link[0] if link else f"{HOST}/news/"
        entries.append(
            "  <entry>\n"
            f"    <title>{esc(text)}</title>\n"
            f'    <link href="{esc(href)}"/>\n'
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
    build_practice()
    build_consult()
    build_book()
    build_advising()
    build_news()
    build_contact()
    build_404()
    build_sitemap()
    build_robots()
    build_feed()
    print(f"done: absolute URLs point at {HOST}")


if __name__ == "__main__":
    main()
