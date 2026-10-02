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
        "blurb": "The MS in Business Analytics counterpart to the MBA course Data Visualization: seven weekly modules in Tableau, with the same labs, weekly data stories, and AI coach as the MBA course, ending on explainable AI and visualization for machine learning.",
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
    ("2026-09-29", "Led the information session for MBA students considering the Business Analytics track.", "https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics", "About the track"),
    ("2026-09-24", "Opened the Artificial Intelligence for Business Leaders agent lab with how fast this is moving. A year earlier, superforecasters put the chance of AI solving a Millennium Prize problem by this fall at 1.7 percent, and industry experts at 4.6 percent. Two weeks before class, it happened.", "https://forecastingresearch.substack.com/p/ai-progress-forecasts-accuracy", "The forecasts"),
    ("2026-09-24", "Same class: Dartmouth's provost defended having used AI on his published writing since 2022, after a detector flagged it as almost entirely AI-written. We talked about where assistance ends and authorship begins.", "https://www.thedartmouth.com/article/2026/09/schnell-ai-writing", "The story"),
    ("2026-09", "Became faculty coordinator of the MBA Business Analytics track at Tepper.", "https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics", "About the track"),
    ("2026-09-10", "Opened Artificial Intelligence for Business Leaders with OpenAI's proof of the Navier-Stokes problem, one of the seven $1 million Millennium Prize problems, announced a few hours after our previous class. By our rough math in class, it took about $100 million of compute to win a $1 million prize.", "https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/", "The story"),
    ("2026-09-10", "Same class, darker headline: an Anthropic alignment lead put the chance that AI kills all humans within a decade at more than 10 percent. We set it next to the p(doom) numbers other AI leaders have given, and a week later the class gave its own. The median was 20 percent.", "https://www.forbes.com/sites/siladityaray/2026/09/09/anthropic-alignment-lead-warns-ai-could-kill-all-humans-as-researcher-quits/", "The story"),
    ("2026-09-08", "Started Artificial Intelligence for Business Leaders on the GPT-6 Astra launch, which reached the human baseline on ARC-AGI-3 the evening after our last class. Jensen Huang posted that AGI has arrived. We put his claim next to Yann LeCun's skepticism.", "https://www.foxbusiness.com/technology/nvidia-ceo-jensen-huang-declares-agi-has-arrived-after-openai-unveils-gpt-6-astra", "The story"),
    ("2026-08-27", "Opened the history of AI in Artificial Intelligence for Business Leaders with the Mechanical Turk, the 1770 chess machine with a person hidden inside, and the news from the day before: Amazon is shutting down its Mechanical Turk marketplace after 21 years, the human workforce that labeled data for a generation of machine learning.", "https://techstartups.com/2026/08/26/top-tech-news-today-august-26-2026-amazon-anthropic-google-microsoft-waymo-more/", "The story"),
    ("2026-08-25", "Taught the first class of Artificial Intelligence for Business Leaders, a new undergraduate course I built. Students learn how AI works, work hands-on with AI agents, and then judge where AI creates value across marketing, finance, operations, and strategy, and how to defend that judgment to executives."),
    ("2026-08-24", "Started the third run of AI Methods for Social and Visual Data, with agents moved earlier in the term and a summary and cleaned transcript for students after every class."),
    ("2026-08-07", "Led a discussion at the Tepper AI-Exchange on what I learned building two new AI courses: what worked in the MBA course AI Methods for Social and Visual Data, and what I was changing for the new undergraduate course, Artificial Intelligence for Business Leaders.", "talks/", "Slides and summary"),
    ("2026-08", "Finished recording the MS in Business Analytics Math Skills Workshop, a self-paced course for incoming MS in Business Analytics students that runs from algebra through gradient descent, PCA, and statistical inference."),
    ("2026-05-09", "Received the George Leland Bach Excellence in Teaching Award, voted by the MBA Class of 2026 and presented at the MBA diploma ceremony.", "https://www.youtube.com/watch?v=wkVLIOVPTbU&t=2890s", "Watch the presentation"),
    ("2026-06", "Really proud of this summer's AI Methods final projects. Three of the nineteen are already in use, and they range from social listening on an aircraft maker's safety crisis to an offline tool that helps bomb-disposal teams identify ordnance."),
    ("2026-05-04", "Taught AI Methods for Social and Visual Data for the second time, rebuilt for the summer with one live session a week and hands-on Python videos for every module."),
    ("2026-04-30", "Talked with Tepper for a Faculty Spotlight on what students learn in the MS in Business Analytics, and why I describe business analytics as a decathlon.", "https://www.youtube.com/watch?v=UxBPkez6Mc4"),
    ("2026-03-11", "Started teaching Machine Learning for Business Applications to the in-person MS in Business Analytics cohort, redesigned around AWS. Students take a model from S3 through SageMaker to a database they run themselves and a live dashboard."),
    ("2026-02-19", "Made a cameo in a Tepper reel for the end of Mini 3: your professor tells a joke that is not funny, but finals are next week. For the record, the jokes are funny.", "https://www.instagram.com/p/DU86OS8Echk/", "Watch on Instagram"),
    ("2026-01-13", "Started teaching Machine Learning Foundations with Python at Heinz College, rebuilt around four applied projects on policy questions, from broadband subsidies to student loan complaints."),
    ("2026-01", "Advising two MS in Business Analytics capstone teams this spring."),
    ("2025-10-22", "Taught Managing and Assessing Tech Talent and Organizations for CMU Qatar, my first course in Doha since 2016: mock technical interviews on Zoom, then an in-person week on teams and culture."),
    ("2025-10", "Taught Data Mining in person and online hybrid in the same seven-week term, and added principal component analysis to the course."),
    ("2025-08-26", "Taught the first class of AI Methods for Social and Visual Data, a course I built for MBA and master's students on text, images, and AI agents, using foundation models rather than training them."),
    ("2025-05", "Joined gAIm Systems as Senior Director of AI and Data Science."),
    ("2025-05", "Proud of this spring's Data Mining final projects: teams brought their own questions, from predicting baseball Hall of Fame induction to siting EV chargers in Pennsylvania."),
    ("2025-03", "This spring's Data Visualization final projects were 29 recorded data stories, from Netflix's global catalog to city-by-city warming and public-sector dashboards."),
    ("2025-01-10", "Poets & Quants profiled Tepper's MBA Class of 2026, and Tepper's director of masters admissions named me as the new professor teaching business analytics in the MBA program.", "https://poetsandquants.com/2025/01/10/meet-carnegie-mellon-teppers-mba-class-of-2026/2/", "Read the profile"),
    ("2025-01-13", "Rebuilt Data Visualization entirely in Tableau for its second run, added clustering, network graphs, and explainable AI, and recorded about fifty short screencast lessons. Also started teaching its MS in Business Analytics counterpart, Data Exploration and Visualization."),
    ("2025-01", "Advised five MS in Business Analytics capstone projects."),
    ("2024-10", "Taught Data Mining for the third time and moved it from R to Python, adding time series forecasting and a session on building data-driven products to clustering, regression, classification, and text mining."),
    ("2024-08-26", "Started teaching Introduction to Probability and Statistics, the first quantitative course in the full-time MS in Business Analytics, pairing every distribution with its Excel formula and its Python call."),
    ("2024-08", "Joined Tepper as Assistant Teaching Professor of Business Analytics."),
    ("2024-06", "Taught in the Business Analytics Summer Summit."),
    ("2024-05", "Proud of the first Data Mining final projects: sixteen online hybrid MBA teams, many working on data from their own employers."),
    ("2024-03-13", "Started teaching Data Visualization with an evening MBA section, mixing Tableau with R and ggplot2."),
    ("2024-03", "Taught Data Mining for the second time, rebuilt for the online hybrid MBA with a recorded video module for each topic and a self-directed final project in place of the exam."),
    ("2024-01", "Advising three MS in Business Analytics capstone teams this spring, with Tindoori Labs, Marinus Analytics, and 412 Food Rescue."),
    ("2023-10-25", "Started teaching Data Mining to full-time MBA students as an adjunct, redesigning it around business questions, with labs in R and tidymodels."),
]


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


# Index tabs across the top of every page, in order, each with its own colour.
NAV = [
    ("courses/", "courses", "courses", "#f6c453"),
    ("projects/", "coding with AI projects", "projects", "#9ccbea"),
    ("advising/", "advising", "advising", "#a9d8a1"),
    ("consult/", "consulting", "consult", "#f3a391"),
    ("cv/", "cv", "cv", "#cdb8e8"),
    ("strengths/", "strengths", "strengths", "#ffd2a8"),
    ("talks/", "talks", "talks", "#8ed3c7"),
    ("travel/", "travel", "travel", "#c9dd92"),
    ("news/", "news", "news", "#f5b5c8"),
    ("contact/", "contact", "contact", "#e9dfc4"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600"
         "&family=Kalam:wght@400;700&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400"
         "&family=Young+Serif&display=swap")

# Runs before first paint. It arms the scroll-in drawing only when the page
# can actually play it, and disarms it if js/notebook.js never arrives, so the
# page is never left blank.
ARM = ('<script>(function(d){var c=d.classList,r=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;'
       'c.add("nb");if(r||!("IntersectionObserver" in window)){c.add("static")}else{c.add("js-anim")}'
       'setTimeout(function(){if(!window.__nb){c.remove("js-anim");c.remove("nb")}},4000)})(document.documentElement)</script>')


def sheet_head(root: str, crumbs) -> str:
    """The notebook page's header fields: subject, and where the page is filed.
    crumbs is a list of (label, href or None). Two or more become a breadcrumb."""
    if not crumbs:
        crumbs = [("teaching and practice", None)]
    parts = [f'<a href="{root}{h}">{esc(l)}</a>' if h is not None else esc(l) for l, h in crumbs]
    trail = " / ".join(parts)
    filed = (f'<nav class="field crumbs" aria-label="Breadcrumb">Filed under <span class="val">{trail}</span></nav>'
             if len(crumbs) > 1 else f'<span class="field" aria-hidden="true">Filed under <span class="val">{trail}</span></span>')
    return f"""  <div class="sheet-head">
    <span class="field" aria-hidden="true">Subject <span class="val">AI and business analytics</span></span>
    {filed}
  </div>
"""


def header(root: str, active: str, title: str, desc: str, canon: str, jsonld: str,
           crumbs=None, body_class: str = "") -> str:
    def item(href, label, key, color):
        current = ' aria-current="page"' if active == key else ""
        return f'<li style="--c:{color}"><a href="{root}{href}"{current}>{label}</a></li>'

    url = f"{HOST}/{canon}"
    ld = (
        f'\n  <script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    )
    tabs = "\n        ".join(item(*n) for n in NAV)
    book_current = ' aria-current="page"' if active == "book" else ""
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{root}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="author" content="{esc(SITE['author'])}">
  <meta name="theme-color" content="#22302b">
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
  {ARM}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" media="print" onload="this.media='all'" href="{FONTS}">
  <noscript><link rel="stylesheet" href="{FONTS}"></noscript>
  <link rel="stylesheet" href="{root}css/site.css">{ld}
</head>
<body{cls}>
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="{root or './'}" aria-label="Ben Collier, PhD, home">
      <span class="badge"><img src="{root}assets/portrait-hedcut.png" alt="" width="46" height="46" loading="lazy"><svg data-chart="ring"></svg></span>
      <span>Ben Collier, PhD</span>
    </a>
    <nav aria-label="Main">
      <ul class="tabs">
        {tabs}
      </ul>
    </nav>
    <a class="sticky-cta" href="{root}book/"{book_current}><span class="nw">Book a call &rarr;</span><small>free, 15 minutes</small></a>
  </div>
</header>

<main id="main" class="sheet">
{sheet_head(root, crumbs)}"""


def footer(root: str, scripts: str = "") -> str:
    return f"""</main>

<footer class="foot">
  <p><span class="sign">thanks for reading!</span><br>&copy; {date.today().year} Ben Collier</p>
  <nav aria-label="Footer">
    <a href="{root}consult/">Consulting</a>
    <a href="{root}contact/">Contact</a>
    <a href="{root}feed.xml">RSS</a>
  </nav>
</footer>
<script src="{root}js/config.js"></script>
<script src="{root}js/site.js"></script>
<script src="{root}js/notebook.js" defer></script>{scripts}
</body>
</html>
"""


def page(root, active, title, desc, canon, body, jsonld="", crumbs=None, body_class="", scripts="") -> str:
    """crumbs: where the page is filed, for the sheet header. scripts: extra
    page-specific <script> tags, appended after the shared ones."""
    if crumbs is None and active not in ("home", ""):
        label = next((n[1] for n in NAV if n[2] == active), active)
        crumbs = [(label, None)]
    return (header(root, active, title, desc, canon, jsonld, crumbs, body_class)
            + body + footer(root, scripts))


# ---------------------------------------------------------------------------
# Notebook pieces shared by every page: hand-drawn underlines, numbered
# sections, piles of taped slide prints.
# ---------------------------------------------------------------------------

def u_last(text: str, d: float = 0.3, cls: str = "u") -> str:
    """Escape a heading and put a hand-drawn underline under its last word."""
    head, _, last = text.rpartition(" ")
    span = f'<span class="{cls}" data-d="{d}">{esc(last)}</span>'
    return f"{esc(head)} {span}" if head else span


def sec(no: int, sid: str, kicker: str, title: str, inner: str, cls: str = "", title_html: str = "") -> str:
    """A numbered notebook section with a kicker and an underlined heading."""
    kick = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return (f'\n  <section class="sec reveal{(" " + cls) if cls else ""}" aria-labelledby="{sid}">'
            f'<span class="sec-no" aria-hidden="true">No. {no:02d}</span>{kick}'
            f'<h2 id="{sid}">{title_html or u_last(title)}</h2>\n{inner}\n  </section>\n')


def page_head(kicker: str, title: str, lede: str = "", extra: str = "", stamp: str = "") -> str:
    """The opening block of an inside page: kicker, big underlined title, lede."""
    st = f'<p class="stamp thunk" style="--d:.15s">{stamp}</p>' if stamp else ""
    kick = f'<p class="kicker">{kicker}</p>' if kicker else ""
    led = f'<p class="lede">{lede}</p>' if lede else ""
    return (f'\n  <section class="page-head reveal">{st}{kick}<h1>{u_last(title, 0.4, "u u2")}</h1>'
            f'{led}{extra}</section>\n')


PRINT_ROT = [-2.5, 2, -1, 3, -3]


def stack(srcs, label: str, tag: str = "", cls: str = "stack") -> str:
    """A pile of taped prints. js/notebook.js lifts the top one off every few
    seconds; without it the pile simply rests with the first print on top."""
    prints = "".join(
        f'<span class="print" style="--r:{PRINT_ROT[i % 5]}deg"><img src="{s}" alt="" width="320" height="180" loading="lazy" decoding="async"></span>'
        for i, s in enumerate(srcs)
    )
    t = f'<span class="stack-tag">{esc(tag)}</span>' if tag else ""
    return f'<span class="{cls}" role="img" aria-label="{esc(label)}"><span class="stack-tape"></span>{prints}{t}</span>'


def sticky(href: str, big: str, sub: str = "", cls: str = "", rot: float = -3, d: float = 1, tape: bool = False) -> str:
    """A sticky note that is a link. Lands with a small bounce when drawn."""
    s = f'<span class="sub">{sub}</span>' if sub else ""
    t = '<span class="tape tc"></span>' if tape else ""
    return (f'<a class="sticky land{(" " + cls) if cls else ""}" href="{href}" style="--rot:{rot}deg;--d:{d}s">'
            f'{t}<span class="big">{big}</span>{s}</a>')


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


# Readers do not know catalog numbers, so labels use a short course name.
# The number appears only as a fact on the course page and on the CV.
SHORT_NAMES = {
    "70-445": "AI for Leaders", "45-884": "AI Methods", "70-377": "Tech Talent", "45-851": "Data Mining",
    "45-885": "Data Viz", "46-885": "Explore & Viz", "46-880": "Prob & Stats", "46-887": "ML in Business",
    "90-803": "ML Foundations", "70-311": "Org Behavior", "70-321": "Negotiation", "70-342": "Cultures",
    "70-453": "Consulting", "70-443": "Social Media", "70-323": "Research",
}


def course_label(c) -> str:
    """Short text for a course thumbnail: a short name, never the catalog number."""
    return SHORT_NAMES.get(c["slug"]) or c.get("label") or c["program"]


def course_name(c) -> str:
    """The course's full title. Catalog numbers are not used as names."""
    return c["title"]


# The pen doodle in the corner of each course's index card.
HERO_ICON = {"agents": "agent", "network": "net", "vit": "vision", "teams": "org", "descent": "bowl",
             "kmeans": "scatter", "charts": "bars", "brush": "explore", "galton": "bell", "pipeline": "flow"}
CARD_ROT = [-1.4, 1, -0.7, 1.6, -1.1, 0.8, -1.6, 1.2]


def course_level(c) -> str:
    bits = [b for b in (c.get("program"), c.get("school")) if b]
    return " · ".join(bits) or ERA_KICKER.get(c.get("era"), "")


def course_card(c, root, i: int = 0):
    """An index card for a course: number, level, a pile of its slides, title, one line."""
    slides = course_visual_slides(c["slug"], 0)
    pile = ""
    if slides:
        pile = stack([root + thumb_src(sl["src"]) for sl in slides],
                     f"Slides from {course_name(c)}, starting with: {slides[0]['caption']}")
    icon = HERO_ICON.get(c.get("hero"), "net")
    doodle = f'<svg class="ic-doodle{" corner" if pile else ""}" data-chart="icon" data-icon="{icon}" data-d="{0.8 + 0.2 * (i % 4):.1f}"></svg>'
    return f"""<a class="icard deal" href="{root}courses/{c['slug']}/" style="--rot:{CARD_ROT[i % len(CARD_ROT)]}deg;--d:{0.2 + 0.15 * (i % 4):.2f}s">
  <span class="tape tc"></span>
  <span class="ic-top"><span class="code">{esc(course_label(c))}</span><span class="lvl">{esc(course_level(c))}</span></span>
  {pile}
  <h3>{c['title']}</h3>
  <p>{c['one_liner']}</p>
  {doodle}
  <span class="go">course page</span>
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


def news_link(link: str, root: str) -> str:
    """News links are absolute URLs or site paths like "talks/"."""
    return link if link.startswith("http") else root + link


# Short names news items use for a course, beyond its catalog title.
COURSE_ALIASES = {"45-884": ["AI Methods"], "msba-math-skills-workshop": ["Math Skills Workshop"]}


def linkable_courses():
    return globals().get("ALL_COURSES", COURSES)


def link_courses(text: str, root: str, found=None) -> str:
    """Link the first mention of each course in a news item to its page.
    Longer names win, so "45-885 Data Visualization" links as one phrase.
    Pass a list as found to collect the slugs mentioned, in order."""
    names = {}
    for c in linkable_courses():
        for name in [course_name(c), c["title"], c.get("number", ""), *COURSE_ALIASES.get(c["slug"], [])]:
            if len(name) >= 6:
                names.setdefault(name, c["slug"])
    if not names:
        return text
    pattern = re.compile("|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)))
    done = set()

    def sub(m):
        slug = names[m.group(0)]
        if slug in done:
            return m.group(0)
        done.add(slug)
        if found is not None:
            found.append(slug)
        return f'<a href="{root}courses/{slug}/">{m.group(0)}</a>'

    return pattern.sub(sub, text)


# A picture for news items that are not about one course. Keyed by a phrase
# unique to the item. "video" puts a play button on the still.
NEWS_VISUALS = {
    "Mechanical Turk marketplace": {"img": "assets/news/class-mturk.jpg", "alt": "Slide: Amazon is shutting Mechanical Turk after 21 years"},
    "GPT-6 Astra launch": {"img": "assets/news/class-jensen.jpg", "alt": "Jensen Huang on stage"},
    "Navier-Stokes": {"img": "assets/news/class-navier.jpg", "alt": "Quanta Magazine illustration of turbulent fluid for the Navier-Stokes story"},
    "alignment lead": {"img": "assets/news/class-pdoom.jpg", "alt": "The Claude app on a phone"},
    "superforecasters": {"img": "assets/news/class-forecast.jpg", "alt": "Chart of forecasts against actual AI progress"},
    "Dartmouth's provost": {"img": "assets/news/class-dartmouth.jpg", "alt": "Illustration from The Dartmouth's story on the provost's writing"},
    "George Leland Bach": {"img": "assets/news/bach-ceremony.jpg", "video": True, "alt": "The stage at the 2026 Tepper MBA diploma ceremony"},
    "Faculty Spotlight": {"img": "assets/talks/faculty-spotlight-2026.jpg", "video": True, "alt": "Ben Collier in the Tepper Faculty Spotlight video"},
    "Tepper reel": {"img": "assets/news/tepper-reel.jpg", "video": True, "alt": "Ben Collier and a colleague on the Tepper Quad stairs in the end-of-Mini-3 reel"},
    "Tepper AI-Exchange": {"img": "assets/talks/ai-exchange-2026-blooms.jpg", "alt": "Slide from the AI-Exchange talk: how 45-884 maps to Bloom's taxonomy"},
    "information session": {"img": "assets/news/ba-track-info-session-2026.jpg", "alt": "Slide from the Business Analytics track information session: 3 core courses, 4 application courses, 1 capstone project"},
    "faculty coordinator": {"img": "assets/news/ba-track-objectives-2026.jpg", "alt": "Slide from the Business Analytics track information session: what managers need to know about analytics"},
    "capstone": {"icon": "capstone", "label": "Capstones"},
    "gAIm Systems": {"icon": "role", "label": "gAIm"},
    "Joined Tepper": {"icon": "role", "label": "Tepper"},
    "Summer Summit": {"icon": "summit", "label": "BASS"},
}

NEWS_ICONS = {
    # 24x24 line icons, drawn in pen on a small index card.
    "track": '<path d="M4 19c4-1 5-6 8-7s6 1 8-3"/><circle cx="4" cy="19" r="1.6"/><circle cx="20" cy="9" r="1.6"/><path d="M14 4l6 5-6 0"/>',
    "capstone": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/>',
    "role": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2"/><path d="M3 13h18"/>',
    "summit": '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
}

# Phrases in news items that get a highlighter swipe.
NEWS_MARKS = {"1.7 percent": "p", "$100 million of compute": "p", "The median was 20 percent": "p"}

THUMB_ROT = [2, -2, 1.5, -1.5, 2.5, -1]


def course_visual_slides(slug: str, offset: int):
    """Five slides spread across a course, starting at a different session for
    each news item so repeated mentions do not show the same five."""
    s = load_schedule(slug)
    if not s:
        return []
    rows = [r for r in s["schedule"] if r.get("slides")]
    picks = []
    for i in range(min(5, len(rows))):
        r = rows[(offset + i * max(1, len(rows) // 5)) % len(rows)]
        picks.append(r["slides"][(offset + i) % len(r["slides"])])
    return picks


def news_visual(text: str, slugs, root: str, index: int, href: str) -> str:
    """A taped picture beside a news item: the story's own image, a pile of
    slides from the course it mentions (with the story image on top when there
    is one), a video still, or a small pen icon card."""
    spec = next((v for k, v in NEWS_VISUALS.items() if k in text), None)
    rot = THUMB_ROT[index % len(THUMB_ROT)]
    course = next((c for c in linkable_courses() if slugs and c["slug"] == slugs[0]), None)
    slides = course_visual_slides(course["slug"], index * 2) if course else []
    tag_attrs = f'href="{esc(href)}" tabindex="-1"' if href else ""
    if spec and spec.get("img") and slides and not spec.get("video"):
        srcs = [root + spec["img"]] + [root + thumb_src(sl["src"]) for sl in slides[:4]]
        pile = stack(srcs, f'{spec["alt"]}, then slides from {course_name(course)}', course_label(course), "stack news-stack")
        el = "a" if href else "span"
        return f'<{el} class="thumb has-stack" {tag_attrs} style="--rot:{rot}deg">{pile}</{el}>'
    if spec and spec.get("img"):
        play = '<span class="vplay" aria-hidden="true"></span>' if spec.get("video") else ""
        inner = f'<img src="{root}{spec["img"]}" alt="{esc(spec["alt"])}" width="480" height="270" loading="lazy">{play}'
        el = "a" if href else "span"
        return f'<{el} class="thumb" {tag_attrs} style="--rot:{rot}deg">{inner}</{el}>'
    if slides:
        srcs = [root + thumb_src(sl["src"]) for sl in slides]
        pile = stack(srcs, f"Slides from {course_name(course)}", course_label(course), "stack news-stack")
        return (f'<a class="thumb has-stack" href="{root}courses/{course["slug"]}/" tabindex="-1" style="--rot:{rot}deg">{pile}</a>')
    if spec and spec.get("icon"):
        icon = spec["icon"]
        return (f'<span class="thumb icon" aria-hidden="true" style="--rot:{rot}deg">'
                f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{NEWS_ICONS[icon]}</svg>'
                f'<span>{esc(spec["label"])}</span></span>')
    return ""


SHORT_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def log_date(iso: str) -> str:
    """2026-06-10 -> Jun 10, 2026. 2026-03 -> Mar 2026."""
    parts = iso.split("-")
    if len(parts) == 3:
        return f"{SHORT_MONTHS[int(parts[1]) - 1]} {int(parts[2])}, {parts[0]}"
    if len(parts) == 2:
        return f"{SHORT_MONTHS[int(parts[1]) - 1]} {parts[0]}"
    return iso


def news_items(limit=None, root=""):
    """The dated log: date in red pen, the note, a taped picture on the right."""
    items = NEWS if limit is None else NEWS[:limit]
    out = ['<ol class="log">']
    for index, (iso, text, *rest) in enumerate(items):
        more = ""
        href = ""
        if rest:
            label = rest[1] if len(rest) > 1 else "Watch the video"
            href = news_link(rest[0], root)
            more = f' <a href="{esc(href)}">{label}</a>'
        slugs = []
        body = link_courses(text, root, slugs)
        for phrase, colour in NEWS_MARKS.items():
            body = body.replace(phrase, f'<mark class="{colour}">{phrase}</mark>', 1)
        visual = news_visual(text, slugs, root, index, href)
        d = f' style="--d:{0.3 + 0.15 * index:.2f}s"' if index < 8 else ""
        out.append(
            f'<li class="fade"{d}><time datetime="{iso}">{log_date(iso)}</time>'
            f'<p>{body}{more}</p>{visual}</li>'
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


# Where the problems come from: the sketched career timeline on the home page.
# (label, start, end or 0 for ongoing, colour, full name for the table version)
CAREER = [
    ("CMU Qatar, teaching + exec ed", 2012, 2016, "#cdb8e8", "Carnegie Mellon University in Qatar, Assistant Teaching Professor and co-director of executive education"),
    ("UPMC's Pensiamo", 2016, 2020, "#f3a391", "UPMC's Pensiamo, Senior Director of Data Science"),
    ("Hot Metal AI, my practice", 2018, 0, "#f6c453", "Hot Metal AI, founder"),
    ("Duolingo", 2020, 2023, "#a9d8a1", "Duolingo, Staff Data Scientist"),
    ("Tepper, Carnegie Mellon", 2023, 0, "#9ccbea", "Tepper School of Business, Carnegie Mellon"),
    ("gAIm Systems", 2025, 0, "#8ed3c7", "gAIm Systems, Senior Director of AI and Data Science"),
]

NUMBER_WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def number_word(n: int) -> str:
    return NUMBER_WORDS[n] if 0 <= n < len(NUMBER_WORDS) else str(n)


def season_of(iso: str):
    y, *rest = iso.split("-")
    if not rest:
        return None
    m = int(rest[0])
    return y, "spring" if m <= 5 else "summer" if m <= 8 else "fall"


def news_note(items) -> str:
    """A margin note when the latest items all come from one term."""
    seasons = {season_of(i[0]) for i in items}
    if len(seasons) != 1 or None in seasons:
        return ""
    (y, term), = seasons
    when = f"this {term}" if season_of(BUILT[:7]) == (y, term) else f"{term} {y}"
    return f'<p class="note news-note fade" style="--d:.8s">all from {when}</p>'


def build_home():
    built = [c for c in COURSES if c["built"]]
    cards = "\n".join(course_card(c, "", i) for i, c in enumerate(built))
    n_built, n_taught = len(built), len(COURSES)
    n_adv = len(load_json("advising.json")["projects"])
    rows = json.dumps([[a, b, c, d] for a, b, c, d, _ in CAREER])
    table = "".join(f"<tr><th>{esc(full)}</th><td>{a} to {b or 'now'}</td></tr>" for _, a, b, _, full in CAREER)
    latest = NEWS[:5]
    body = f"""
  <section class="hero reveal" aria-labelledby="hero-title">
    <div class="hero-text">
      <p class="stamp thunk" style="--d:.15s">Assistant Teaching Professor of Business Analytics</p>
      <h1 id="hero-title">Ben Collier</h1>
      <p class="lede">I teach <mark style="--d:.5s">AI and business analytics</mark> at Carnegie Mellon's Tepper School, and help companies <span class="u u2" data-d="1.2">put them to work</span>.</p>
      <p class="hero-more">My students learn to build with AI, and to <span class="u" data-d="1.7">doubt it</span>: they compare the models, question the headline number, and defend the call.</p>
      <div class="cta-row">
        {sticky("book/", 'Book a free <span class="nw">15-minute call &rarr;</span>', rot=-3, d=1)}
        <a class="go" href="consult/">Consulting and custom education</a>
      </div>
    </div>

    <div class="hero-art">
      <figure class="polaroid portrait-morph" style="--rot:3deg">
        <span class="tape tl"></span><span class="tape tr"></span>
        <div class="ph">
          <img class="photo" src="assets/portrait.jpg" alt="Ben Collier, smiling, in a tweed jacket and red tie" width="500" height="500" fetchpriority="high">
          <img class="hedcut" src="assets/portrait-hedcut.png" alt="" width="360" height="360" loading="lazy">
        </div>
        <figcaption>hi, I'm Ben!</figcaption>
      </figure>
      <figure class="figcard needs-js" style="--rot:-3.5deg">
        <span class="tape tc"></span>
        <svg data-chart="kmeans" data-d="0.8"></svg>
        <figcaption class="figcap">fig. 1 &middot; k-means clustering, from Data Mining</figcaption>
      </figure>
      <p class="note hero-note fade needs-js" style="--d:3.4s">&uarr; k-means found these 3 groups on its own</p>
    </div>
  </section>

  <section class="sec bio reveal" aria-labelledby="bio-title">
    <span class="sec-no" aria-hidden="true">No. 02</span>
    <p class="kicker">About</p>
    <h2 id="bio-title">From industry to the <span class="u" data-d=".3">classroom</span>, and back</h2>
    <div class="bio-grid">
      <div class="prose">
        <p>Most of my teaching is at <a href="https://www.cmu.edu/tepper/">Tepper</a>, in the <a href="https://www.cmu.edu/tepper/programs/mba/">MBA</a>, the <a href="https://www.cmu.edu/tepper/programs/master-business-analytics/">MS in Business Analytics</a>, and the <a href="https://www.cmu.edu/tepper/programs/undergraduate-programs/">undergraduate program</a>. I also teach at <a href="https://www.heinz.cmu.edu/">Heinz College</a>.</p>
        <p>Before joining Tepper I was a staff data scientist at <a href="https://www.duolingo.com/">Duolingo</a> and Senior Director of Data Science at <a href="https://www.upmc.com/">UPMC</a>'s Pensiamo, where I was the <mark class="b" style="--d:.6s">founding data scientist</mark> on a joint venture with <a href="https://en.wikipedia.org/wiki/IBM_Watson_Health">IBM Watson Health</a>. I still do that work, as Senior Director of AI and Data Science at <a href="https://www.gaimsystems.com/">gAIm Systems</a> and through my consulting practice, Hot Metal AI. <mark class="g" style="--d:1s">The problems I bring into class come from that work.</mark></p>
        <p>I also advise MS in Business Analytics capstone teams. Since September 2026 I have been the faculty coordinator of Tepper's <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>, and starting in Spring 2027 I also advise its capstone teams.</p>
      </div>
      <figure class="tl-fig">
        <svg data-chart="timeline" data-d="0.5" data-rows="{esc(rows)}"></svg>
        <figcaption class="figcap needs-js">fig. 2 &middot; where the problems come from, 2012 to now</figcaption>
        <table class="tl-table"><caption>Career timeline</caption>{table}</table>
      </figure>
    </div>
  </section>

  <section class="sec reveal" aria-labelledby="stats-title">
    <span class="sec-no" aria-hidden="true">No. 03</span>
    <p class="kicker">By the numbers</p>
    <h2 id="stats-title">So far, in <span class="u" data-d=".3">tally marks</span></h2>
    <div class="stats">
      <a class="stat" href="courses/#built">
        <span class="n"><span class="count" data-to="{n_built}" data-d=".2">{n_built}</span></span>
        <svg data-chart="tally" data-n="{n_built}" data-d="0.3"></svg>
        <span class="l">courses I designed from scratch</span>
        <span class="more">see them</span>
      </a>
      <a class="stat" href="courses/">
        <span class="n"><span class="count" data-to="{n_taught}" data-d=".35">{n_taught}</span></span>
        <svg data-chart="tally" data-n="{n_taught}" data-d="0.6"></svg>
        <span class="l">courses taught at Carnegie Mellon since 2023</span>
        <span class="more">all courses</span>
      </a>
      <a class="stat" href="advising/">
        <span class="n"><span class="count" data-to="{n_adv}" data-d=".5">{n_adv}</span></span>
        <svg data-chart="tally" data-n="{n_adv}" data-d="1.1"></svg>
        <span class="l">capstones and independent studies advised since 2024</span>
        <span class="more">advising</span>
      </a>
      <a class="stat award" href="cv/#honors-and-awards">
        <span class="n"><span class="thunk yr" style="--d:1.6s">2026</span></span>
        <svg data-chart="award" data-d="1.8"></svg>
        <span class="l">George Leland Bach Teaching Award, voted by the MBA class</span>
        <span class="more">on the cv</span>
      </a>
    </div>
    <div class="mnote stat-note hide-sm fade" style="--d:2.6s">
      <p class="note red">voted by students!</p>
      <svg class="arrow" width="70" height="60" data-arrow="8 6 52 50 -14 10" data-d="2.8" style="left:150px;top:6px;color:var(--red)"></svg>
    </div>
  </section>

  <section class="sec reveal" aria-labelledby="courses-title">
    <span class="sec-no" aria-hidden="true">No. 04</span>
    <p class="kicker">Teaching</p>
    <h2 id="courses-title">Courses I <span class="u" data-d=".3">built</span></h2>
    <div class="mnote courses-note fade" style="--d:.9s">
      <p class="note">all {number_word(n_built)} designed<br>from scratch</p>
      <svg class="arrow" width="90" height="70" data-arrow="10 10 70 58 -18 11" data-d="1.1"></svg>
    </div>
    <div class="cards">
{cards}
    </div>
    <p class="after"><a class="go" href="courses/">All courses</a></p>
  </section>

  <section class="sec reveal" aria-labelledby="work-title">
    <span class="sec-no" aria-hidden="true">No. 05</span>
    <div class="pad">
      <p class="kicker">Consulting and custom education</p>
      <h2 id="work-title">Work with <span class="u" data-d=".3">me</span></h2>
      <p class="pad-intro">I help organizations choose which AI and analytics projects to fund, check the models before they carry a real decision, and train their teams to run the work themselves. I do this through my practice, <mark style="--d:.7s">Hot Metal AI</mark>.</p>
      <div class="pad-grid">
        <div>
          <h3>Reviews and builds</h3>
          <ul class="checks">
            <li><svg data-chart="check" data-d="0.9"></svg><span><b>AI use-case review.</b> About two weeks. A written go or no-go on the projects you are considering, with a build plan for the ones worth doing.</span></li>
            <li><svg data-chart="check" data-d="1.2"></svg><span><b>Model or metric review.</b> About one week. I read the code, data, and evaluation, and tell you where it breaks.</span></li>
            <li><svg data-chart="check" data-d="1.5"></svg><span><b>Hands-on build.</b> Scoped with you: a prototype, a pipeline, or an evaluation harness your team can keep running.</span></li>
          </ul>
        </div>
        <div>
          <h3>Training built on your data</h3>
          <p>Workshops and courses for technical teams and executives, built around your own data and problems. Most of the time is spent in hands-on labs.</p>
          <ul class="dashes">
            <li>One- to three-day workshops, on site or online</li>
            <li>Multi-week programs for technology leaders and executives</li>
            <li>Recorded, self-paced courses</li>
          </ul>
          <p class="small">Professional development courses for technology leaders and executives at Optum, AT&amp;T, Cox Communications, and RapidScale.</p>
        </div>
        <div class="pad-cta">
          {sticky("book/", "Book a call &rarr;", "Most engagements start with a free 15-minute call.", "pink", 3, 1.4, True)}
          <a class="go" href="consult/">More on consulting</a>
        </div>
      </div>
    </div>
  </section>

  <section class="sec reveal" aria-labelledby="news-title">
    <span class="sec-no" aria-hidden="true">No. 06</span>
    <p class="kicker">News</p>
    <h2 id="news-title">Recent <span class="u" data-d=".3">entries</span></h2>
    {news_note(latest)}
    {news_items(5)}
    <p class="after"><a class="go" href="news/">All news</a> &nbsp; <a class="go" href="cv/">Full CV</a></p>
  </section>

  <section class="sec talks reveal" aria-labelledby="talks-title">
    <span class="sec-no" aria-hidden="true">No. 07</span>
    <div class="talks-grid">
      <a class="video polaroid drop" href="https://www.youtube.com/watch?v=UxBPkez6Mc4" style="--rot:-1.8deg;--d:.2s" aria-label="Watch the Faculty Spotlight video on YouTube, 11 minutes">
        <span class="tape tl"></span><span class="tape br"></span>
        <span class="ph"><img src="assets/talks/faculty-spotlight-2026.jpg" alt="Ben Collier in conversation on a bench in Tepper's atrium, gesturing as he explains" width="1280" height="720" loading="lazy"><span class="vplay big" aria-hidden="true"></span><svg class="play" data-chart="play" data-d="0.9"></svg></span>
        <span class="cap">Faculty Spotlight &middot; April 30, 2026 &middot; 11 min</span>
      </a>
      <div class="talks-text">
        <p class="kicker">Talks</p>
        <h2 id="talks-title">Business analytics as a <span class="u u2" data-d=".5">decathlon</span></h2>
        <p>A conversation for Tepper about the MS in Business Analytics curriculum, and why I describe business analytics as a decathlon.</p>
        <p><a class="go" href="https://www.youtube.com/watch?v=UxBPkez6Mc4">Watch on YouTube</a></p>
        <div class="also">
          <p class="note">also on the talks page</p>
          <ul>
            <li><span class="when">Aug 2026 &middot; Tepper AI-Exchange</span>Lessons Learned from Developing New AI Courses for MBA and Undergraduate Business Students</li>
            <li><span class="when">Jun 2025 &middot; Kellogg, Northwestern</span>AI Data Visualization Coach</li>
          </ul>
          <p><a class="go" href="talks/">All talks</a></p>
        </div>
      </div>
    </div>
  </section>
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
            body_class="home",
        ),
    )


def education_sections(root: str, no: int) -> str:
    """Executive education first, as the selling section, then the CMU Qatar
    archive. Both come from data/course_schedules files with a meta block, and
    the headline numbers from data/education_stats.json when it exists."""
    cmuq = [c for c in EXTRA_COURSES if c["era"] == "cmuq"]
    execs = [c for c in EXTRA_COURSES if c["era"] in ("exec-ed", "corporate")]
    out = ""
    stats_file = ROOT / "data" / "education_stats.json"
    stats = json.loads(stats_file.read_text(encoding="utf-8")) if stats_file.exists() else {}
    if execs or stats:
        tiles = "".join(
            f'<li class="stat"><span class="n">{esc(n)}</span><span class="l">{esc(label)}</span></li>' for n, label in stats.get("stats", [])
        )
        cards = "\n".join(course_card(c, root, i) for i, c in enumerate(execs))
        inner = f"""    <p class="prose">{stats.get("intro", "Programs I have designed and taught for executives and company teams.")}</p>
    {f'<ul class="stats static-stats">{tiles}</ul>' if tiles else ""}
    <div class="cards">{cards}</div>
    <div class="cta-row">{sticky(f"{root}consult/#education", "Plan a program for your team &rarr;", rot=-2, d=.4)}</div>"""
        out += sec(no, "executive", "For organizations", "Executive and custom education", inner)
        no += 1
    if cmuq:
        cards = "\n".join(course_card(c, root, i) for i, c in enumerate(cmuq))
        inner = f"""    <p class="prose">My first appointment at Carnegie Mellon was as Assistant Teaching Professor of Organizational Behavior at the Qatar campus, where I also co-directed executive and continuing education. These are the undergraduate courses I taught there, each with its full schedule and slides.</p>
    <div class="cards era">{cards}</div>"""
        out += sec(no, "cmu-qatar", "Earlier teaching", "Organizational behavior at CMU Qatar, 2012 to 2016", inner)
    return out


def build_courses_index():
    built = "\n".join(course_card(c, "../", i) for i, c in enumerate(c for c in COURSES if c["built"]))
    taught = "\n".join(course_card(c, "../", i) for i, c in enumerate(c for c in COURSES if not c["built"]))
    body = page_head("Teaching", "Courses", "Courses I designed from scratch, then courses I took over and rebuilt.")
    body += sec(2, "built", "Designed from scratch", "Courses I built", f'    <div class="cards">{built}</div>')
    body += sec(3, "taught", "Taken over and rebuilt", "Courses I took over and rebuilt", f'    <div class="cards">{taught}</div>')
    body += education_sections("../", 4)
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


# Courses taught before the current appointment, executive programs, and
# corporate workshops are defined entirely by their data/course_schedules file
# (its "meta" block), so adding one needs no edit here.
ERA_HERO = {"negotiat": "teams", "consult": "pipeline", "research": "galton", "marketing": "charts",
            "social media": "charts", "decision": "descent", "data": "kmeans", "cloud": "pipeline",
            "chatbot": "agents", "agile": "pipeline"}


def data_courses():
    out = []
    folder = ROOT / "data" / "course_schedules"
    for f in sorted(folder.glob("*.json")) if folder.exists() else []:
        s = json.loads(f.read_text(encoding="utf-8"))
        m = s.get("meta")
        if not m:
            continue
        title = m["title"]
        hero = next((h for k, h in ERA_HERO.items() if k in title.lower()), "teams")
        out.append({
            "slug": s["slug"], "number": m.get("number", ""), "label": m.get("label", ""),
            "title": title, "program": m.get("program", ""), "school": m.get("school", ""),
            "built": False, "color": m.get("color", "c-wine"), "hero": hero,
            "one_liner": m["one_liner"], "blurb": m["blurb"], "offerings": m.get("offerings", []),
            "materials": m.get("materials", ""), "era": m["era"], "scale": m.get("scale", ""),
            "order": m.get("order", 50),
        })
    return sorted(out, key=lambda c: (c["order"], c["title"]))


EXTRA_COURSES = data_courses()
ALL_COURSES = COURSES + EXTRA_COURSES

# Courses with an obvious version for company teams get a closing prompt.
CORPORATE_VERSIONS = {"70-445", "45-884", "45-851", "45-885", "46-887"}

# A row's kind becomes a small tag next to its topic. Lectures carry no tag.
KIND_TAGS = {
    "exercise": "In-class exercise",
    "case": "Case",
    "break": "No class",
    "presentations": "Presentations",
}

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


ERA_KICKER = {
    "cmuq": "Carnegie Mellon University in Qatar · 2012 to 2016",
    "exec-ed": "Executive education",
    "corporate": "Corporate training · Hot Metal AI",
}


def course_kicker(c) -> str:
    era = ERA_KICKER.get(c.get("era"))
    if era:
        return f"{era} · {c['program']}" if c.get("program") and c["era"] == "cmuq" else era
    return f"{c['school']} · {c['program']}"


def scale_note(c) -> str:
    return f'<p class="scale-note note red">{esc(c["scale"])}</p>\n      ' if c.get("scale") else ""


def load_schedule(slug: str):
    """data/course_schedules/<slug>.json, or None for a course without one yet."""
    path = ROOT / "data" / "course_schedules" / f"{slug}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def short_date(iso: str) -> str:
    """2026-09-08 -> Tue, Sep 8."""
    d = date.fromisoformat(iso)
    return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1][:3]} {d.day}"


def thumb_src(src: str) -> str:
    return src[: -len(".webp")] + "-t.webp"


# Notebook touches for particular course pages. Every phrase here is already
# in the course's own copy above; this only says which words get a highlighter
# or an underline, which slides are taped into the hero, and which figure sits
# beside "How the course works".
COURSE_INK = {
    "45-884": {
        "mark": "knowing when the output is ready for a decision",
        "u": "measuring instrument",
        "facts": ["No prerequisites", "No model training", "Labs in Python"],
        "note": "treat the model as an instrument:<br>what did it measure?",
        "hero": ["s01-1", "s06-3", "s10-1"],
        "fig": "gens",
        "fig_cap": "one photograph, three generations of vision",
        "story_mark": "Every lab compares models.",
        "labs_note": "all in Python",
        "projects_mark": "seven of the nineteen projects were built with real companies or organizations, and three are already in use.",
        "history_intro": 'It covers the data most business analytics courses skip: <mark class="b" style="--d:.5s">text, images, and the output of language models.</mark>',
        "timeline": [
            ("Dec 2024", "Began building the course."),
            ("Fall 2025", "First taught, to MBA and other master's students."),
            ("Summer 2026", "Rebuilt for a part-time format, with one live session a week and a set of hands-on videos I recorded for each module. They run from a first Python lesson through retrieval over company filings, computer vision, and agent workflows."),
            ("Fall 2026", "Moved agentic AI earlier in the term. Students now get a summary and a cleaned transcript after each class."),
        ],
    },
    "70-445": {"mark": "how to explain the difference to the people paying for it", "u": "AI agents",
               "story_mark": "Students build a customer support team of AI agents"},
    "70-377": {"mark": "using evidence instead of instinct", "u": "OKRs"},
    "msba-math-skills-workshop": {"mark": "before the quantitative core begins", "u": "already in place"},
    "45-851": {"mark": "deciding whether to trust it", "u": "workflow"},
    "45-885": {"mark": "designed to change a decision", "u": "spot a graphic that misleads"},
}

KIND_CLASS = {"exercise": "ex", "case": "case", "break": "off", "presentations": "pres"}
SLIDE_ROT = [-5, 4, -1.5]
LAZY = ' loading="lazy"'


def ink_phrase(html: str, phrase, tag: str) -> str:
    """Wrap the first occurrence of phrase in a highlighter or underline."""
    if not phrase or phrase not in html:
        return html
    if tag == "mark":
        return html.replace(phrase, f'<mark style="--d:.7s">{phrase}</mark>', 1)
    if tag == "mark-g":
        return html.replace(phrase, f'<mark class="g" style="--d:.6s">{phrase}</mark>', 1)
    return html.replace(phrase, f'<span class="u" data-d="1.3">{phrase}</span>', 1)


def session_rows(s):
    return [r for r in (s or {}).get("schedule", []) if r.get("slides")]


def hero_slides(c, s):
    """Three slides for the course hero: from the start, the middle, and the end of the term."""
    rows = session_rows(s)
    every = {sl["src"].rsplit("/", 1)[-1][:-5]: sl for r in rows for sl in r["slides"]}
    want = COURSE_INK.get(c["slug"], {}).get("hero")
    if want:
        return [every[k] for k in want if k in every]
    if not rows:
        return []
    picks, seen = [], set()
    for ri, si in ((0, 0), (len(rows) // 2, 2), (len(rows) - 1, 0), (0, 2), (0, 4)):
        r = rows[ri]["slides"]
        sl = r[min(si, len(r) - 1)]
        if sl["src"] not in seen:
            seen.add(sl["src"])
            picks.append(sl)
        if len(picks) == 3:
            break
    return picks


def schedule_section(s, root: str, no: int) -> str:
    """The week-by-week list, with a projector that js/course-schedule.js keeps
    on whichever session is in view. Every row with slides carries its own
    thumbnail strip, shown on phones and whenever the script is not running."""
    unit = s.get("unit_label", "Week")
    title = {"Day": "Day by day", "Session": "Session by session"}.get(unit, "Week by week")
    rows, prev, k = [], object(), 0
    for r in s["schedule"]:
        if "part" in r:
            rows.append(f'<li class="wk-part">{esc(r["part"])}</li>')
            continue
        kind = r.get("kind", "lecture")
        tag = KIND_TAGS.get(kind)
        tag_html = f'<span class="wk-tag {KIND_CLASS.get(kind, "")}">{tag}</span>' if tag else ""
        note = f'<span class="wk-note">{esc(r["note"])}</span>' if r.get("note") else ""
        when = esc(r.get("label") or short_date(r["date"]))
        week = r.get("week")
        mod = f'{unit[0]}{week}' if week else ""
        newmod = week != prev
        prev = week
        strip = has = ""
        if r.get("slides"):
            imgs = "".join(
                f'<img src="{root}{thumb_src(sl["src"])}" data-full="{root}{sl["src"]}" data-caption="{esc(sl["caption"])}" '
                f'alt="{esc(sl["caption"])}" width="320" height="180" loading="lazy" decoding="async">'
                for sl in r["slides"]
            )
            strip = f'<span class="wk-strip">{imgs}</span>'
            has = f'<span class="wk-has" aria-hidden="true">{len(r["slides"])} slides</span>'
        cls = "wk fade" + (" newmod" if newmod else "") + (" off" if kind == "break" else "") + (" has-slides" if r.get("slides") else "")
        tab = ' tabindex="0"' if r.get("slides") else ""
        rows.append(
            f'<li class="{cls}" style="--d:{min(1.2, 0.1 + 0.05 * k):.2f}s" data-date="{r["date"]}"{tab}>'
            f'<time datetime="{r["date"]}">{when}</time><span class="wk-m">{mod}</span>'
            f'<span class="wk-body"><span class="wk-t">{esc(r["topic"])}</span>{tag_html}{has}{note}{strip}</span></li>'
        )
        k += 1
    first = next(iter(session_rows(s)), None)
    projector, intro = "", ""
    if first:
        sl = first["slides"][0]
        when = esc(first.get("label") or short_date(first["date"]))
        projector = f"""      <aside class="projector" aria-label="Slides from the selected session">
        <div class="proj-frame">
          <span class="tape tr"></span>
          <img class="proj-main" src="{root}{sl['src']}" alt="{esc(sl['caption'])}" width="1280" height="720" loading="lazy">
        </div>
        <p class="proj-cap"><b>{when}</b> <span class="proj-topic">{esc(first['topic'])}</span></p>
        <p class="proj-say" aria-live="polite">{esc(sl['caption'])}</p>
        <div class="proj-strip" role="group" aria-label="Choose a slide"></div>
        <p class="note proj-note">hover a session,<br>or just keep scrolling</p>
      </aside>"""
        intro = '    <p class="prose muted">Scroll the schedule and the slides follow along: five from each session, picked from the decks I taught from.</p>\n'
    inner = f"""{intro}    <div class="sched{'' if first else ' solo'}" data-schedule>
      <ol class="weeks">{''.join(rows)}</ol>
{projector}
    </div>"""
    return sec(no, "wk-title", f"{esc(s['term'])} &middot; {esc(s['meets'])}", title, inner)


PCT = re.compile(r"^(?:(.+?)\s)?(\d+)%$")


def assignments_section(s, no: int, fig: int, labs_note: str = "") -> str:
    """Weights as a hand-drawn bar chart, the weighted pieces as index cards,
    and any group (Labs 20%, Projects 40%) as a row of cards of its own."""
    items = (s or {}).get("assignments") or []
    if not items:
        return ""
    groups, singles, bars, cur = [], [], [], None
    for a in items:
        w = (a.get("weight") or "").strip()
        m = PCT.match(w)
        if m and m.group(1):
            cur = {"name": m.group(1), "pct": int(m.group(2)), "items": [a]}
            groups.append(cur)
            bars.append((cur["name"], int(m.group(2))))
            continue
        if not w and cur is not None:
            cur["items"].append(a)
            continue
        cur = None
        if m:
            bars.append((a["name"], int(m.group(2))))
        singles.append((a, w))
    rots = [-1, 0.8, -0.5, 1.1, -0.9, 0.6]
    cards = "".join(
        f'<article class="acard deal" style="--rot:{rots[i % 6]}deg;--d:{0.3 + 0.15 * (i % 6):.2f}s"><h3><span>{esc(a["name"])}</span>'
        + (f' <span class="pct{"" if PCT.match(w) else " soft"}">{esc(w)}</span>' if w else "")
        + f'</h3><p>{esc(a["description"])}</p></article>'
        for i, (a, w) in enumerate(singles)
    )
    chart = ""
    if len(bars) >= 2:
        top = max(v for _, v in bars)
        rows = "".join(
            f'<li class="bar-row"><span class="bl"><b>{esc(n)}</b></span><span class="bar-val">{v}%</span>'
            f'<svg class="bar" data-chart="bar" data-v="{v}" data-max="{top}" data-label="{v}%" data-i="{20 + i}" data-d="{0.3 + 0.2 * i:.2f}" data-color="var(--red)"></svg></li>'
            for i, (n, v) in enumerate(bars)
        )
        chart = (f'<figure class="weights"><ul class="bars">{rows}</ul>'
                 f'<figcaption class="figcap">fig. {fig} &middot; weight of each major assignment in the grade</figcaption></figure>')
    top_part = ""
    if chart or cards:
        top_part = (f'    <div class="as-grid">{chart}<div class="as-cards">{cards}</div></div>' if chart
                    else f'    <div class="as-cards wide">{cards}</div>')
    group_html = ""
    for g in groups:
        labs = ""
        for i, a in enumerate(g["items"]):
            head, sep, rest = a["name"].partition(": ")
            no_html, h4 = (f'<span class="lab-no">{esc(head)}</span>', rest) if sep else ("", a["name"])
            labs += (f'<article class="lab deal" style="--rot:{[-1.2, 0.9, -0.6, 1.3][i % 4]}deg;--d:{0.3 + 0.15 * i:.2f}s">'
                     f'{no_html}<h4>{esc(h4)}</h4><p>{esc(a["description"])}</p></article>')
        n = len(g["items"])
        note = f'{number_word(n)} {g["name"].lower()}' + (f", {labs_note}" if labs_note else "")
        group_html += (f'\n    <h3 class="labs-h">{esc(g["name"])} <span class="pct">{g["pct"]}%</span> <span class="note">{note}</span></h3>'
                       f'\n    <div class="labs">{labs}</div>')
    return sec(no, "as-title", "What students hand in", "Major assignments", top_part + group_html)


def project_list(s) -> str:
    """Every final project, grouped by term. No student names: subject, approach, one line."""
    groups = (s or {}).get("projects") or []
    if not groups:
        return ""
    out = []
    for g in groups:
        items = "".join(
            f'<li><strong>{esc(p["subject"])}</strong>'
            + (f'. {esc(p["description"])}' if p.get("description") else "")
            + (f' <span class="proj-approach">{esc(p["approach"])}</span>' if p.get("approach") else "")
            + "</li>"
            for p in g["items"]
        )
        n = len(g["items"])
        out.append(
            f'<details class="proj-term"><summary><span class="term">{esc(g["term"])}</span> '
            f'<span class="pcount">{n} project{"" if n == 1 else "s"}</span></summary><ul>{items}</ul></details>'
        )
    return '    <p class="muted every">Every project, by term.</p>\n    <div class="terms">' + "".join(out) + "</div>\n"


BAR_COLORS = ["var(--pen)", "var(--red)", "#2e7d4f", "#7a4fb0"]


def course_figure(c, s, fig: int, root: str) -> str:
    """The figure beside "How the course works": a drawn diagram where there is
    one, the course's worked exercise, or one slide taped to the page."""
    ink = COURSE_INK.get(c["slug"], {})
    if ink.get("fig"):
        return (f'<figure class="figcard gens-card needs-js" style="--rot:1.5deg"><span class="tape tc"></span>'
                f'<svg data-chart="{ink["fig"]}" data-d="0.5"></svg>'
                f'<figcaption class="figcap">fig. {fig} &middot; {ink["fig_cap"]}</figcaption></figure>')
    if c.get("panel"):
        return f'<div class="figcard panel-card" style="--rot:1.2deg"><span class="tape tc"></span>{c["panel"]}</div>'
    rows = session_rows(s)
    if not rows:
        return ""
    used = {sl["src"] for sl in hero_slides(c, s)}
    pick = next((sl for r in rows[len(rows) // 3:] + rows for sl in r["slides"][1:] + r["slides"][:1] if sl["src"] not in used), None)
    if not pick:
        return ""
    return (f'<figure class="slide-fig drop" style="--rot:1.5deg;--d:.3s"><span class="tape tr"></span>'
            f'<img src="{root}{pick["src"]}" alt="{esc(pick["caption"])}" width="1280" height="720" loading="lazy">'
            f'<figcaption class="figcap">fig. {fig} &middot; {esc(pick["caption"])}</figcaption></figure>')


def build_course_pages():
    root = "../../"
    for c in ALL_COURSES:
        sched = load_schedule(c["slug"])
        ink = COURSE_INK.get(c["slug"], {})
        no, fig = 2, 1
        body = ""

        # Hero: stamps, the course number in outline, the title, three taped slides.
        slides = hero_slides(c, sched)
        art = ""
        if slides:
            figs = "".join(
                f'<figure class="slide drop s{i + 1}" style="--rot:{SLIDE_ROT[i]}deg;--d:{0.2 + 0.25 * i:.2f}s"><span class="tape tr"></span>'
                f'<img src="{root}{sl["src"]}" alt="Slide: {esc(sl["caption"])}" width="1280" height="720"{LAZY if i else ""}></figure>'
                for i, sl in enumerate(slides)
            )
            note = ink.get("note", "slides from the decks<br>I taught from")
            art = (f'<div class="c-hero-art n{len(slides)}">{figs}'
                   f'<p class="note c-note fade" style="--d:1.9s">{note}</p></div>')
        label = course_label(c)
        seal = '<span class="seal thunk" style="--d:.35s;--rot:8deg">Course<br>I built</span>' if c["built"] else ""
        sr = ""
        facts = ([sched["term"], sched["meets"]] if sched else []) + ink.get("facts", [])
        if c.get("number"):
            facts.append(f"Course number {c['number']}")
        facts_html = "".join(f'<li class="fade" style="--d:{1.2 + 0.1 * i:.1f}s">{esc(f)}</li>' for i, f in enumerate(facts))
        panel = c.get("panel", "") if not c.get("story") else ""
        body += f"""
  <section class="c-hero reveal{'' if art else ' noart'}" aria-labelledby="c-title">
    <div class="c-hero-text">
      <p class="c-stamps"><span class="stamp thunk" style="--d:.1s">{course_kicker(c)}</span> {seal}</p>
      <h1 id="c-title">{sr}{c['title']}</h1>
      <p class="lede">{ink_phrase(c['one_liner'], ink.get('mark'), 'mark')}</p>
      {scale_note(c)}<p class="c-intro">{ink_phrase(c['blurb'], ink.get('u'), 'u')}</p>
      {f'<ul class="facts">{facts_html}</ul>' if facts_html else ''}
      {panel}
    </div>
    {art}
  </section>
"""
        if sched:
            body += schedule_section(sched, root, no)
            no += 1
        elif c.get("topics"):
            items = "".join(f"<li>{t}</li>" for t in c["topics"])
            body += sec(no, "topics-title", "Syllabus", "Topics", f'    <ol class="topics">{items}</ol>')
            no += 1

        if c.get("story"):
            paras = "".join(f"<p>{ink_phrase(p, ink.get('story_mark'), 'mark-g')}</p>" for p in c["story"])
            figure = course_figure(c, sched, fig, root)
            if figure and "figcap" in figure:
                fig += 1
            inner = (f'    <div class="how-grid"><div class="prose">{paras}</div>{figure}</div>' if figure
                     else f'    <div class="prose">{paras}</div>')
            body += sec(no, "how-title", "Method", "How the course works", inner)
            no += 1

        asg = assignments_section(sched, no, fig, ink.get("labs_note", ""))
        if asg:
            body += asg
            no += 1
            if "fig. " in asg:
                fig += 1

        pj = c.get("projects")
        plist = project_list(sched)
        if pj:
            rows = ""
            if pj["types"]:
                top = max(n for _, n, _ in pj["types"])
                rows = "".join(
                    f'<li class="bar-row"><span class="bl"><b>{t}</b><span>{ex}</span></span><span class="bar-val">{n}</span>'
                    f'<svg class="bar" data-chart="bar" data-v="{n}" data-max="{top}" data-i="{i}" data-d="{0.3 + 0.15 * i:.2f}" data-color="{BAR_COLORS[i % 4]}"></svg></li>'
                    for i, (t, n, ex) in enumerate(pj["types"])
                )
                rows = (f'\n    <figure class="cats"><ul class="bars">{rows}</ul>'
                        f'<figcaption class="figcap">fig. {fig} &middot; projects by type, with one example each</figcaption></figure>\n')
                fig += 1
            intro = ink_phrase(pj["intro"], ink.get("projects_mark"), "mark")
            body += sec(no, "fp-title", "What students built", "Final projects", f'    <p class="prose">{intro}</p>{rows}{plist}')
            no += 1
        elif plist:
            body += sec(no, "fp-title", "What students built", "Student work", plist)
            no += 1

        # Revision history, then every offering as a chip.
        hist = ""
        if ink.get("timeline"):
            steps = "".join(
                f'<li class="fade" style="--d:{0.4 + 0.3 * i:.1f}s"><span class="when">{esc(w)}</span><span class="dot-i" aria-hidden="true"></span><p>{t}</p></li>'
                for i, (w, t) in enumerate(ink["timeline"])
            )
            hist = f'    <p class="prose">{ink["history_intro"]}</p>\n    <ol class="hist">{steps}</ol>\n'
        elif c.get("history"):
            hist = "".join(f"    <p class=\"prose\">{p}</p>\n" for p in c["history"])

        def chip(o, last):
            kind = " hy" if "hybrid" in o else ""
            now = " now" if last and re.search(r"20(2[6-9]|[3-9]\d)", o) else ""
            return f'<li class="chip{kind}{now}">{esc(o)}</li>'
        chips = "".join(chip(o, i == len(c["offerings"]) - 1) for i, o in enumerate(c["offerings"]))
        mats = f'<p class="muted">{c["materials"]}</p>' if c.get("materials") else ""
        offer_h = "<h3>Offerings</h3>" if hist else ""
        offer = f'    <div class="offer">{offer_h}<ul class="chips">{chips}</ul>{mats}</div>' if chips or mats else ""
        if hist:
            body += sec(no, "hist-title", "Revision history", "How the course developed", hist + offer)
        elif offer:
            body += sec(no, "hist-title", "Offerings", "When I taught it", offer)

        cta = ""
        if c["slug"] in CORPORATE_VERSIONS:
            cta = f"""    <div class="c-cta-in">
      <p class="c-cta-text">I also teach versions of this material to company teams, using their own data. <a href="{root}consult/#education">Custom education</a></p>
      {sticky(f"{root}book/", 'Book a free <span class="nw">15-minute call &rarr;</span>', rot=-2.5, d=.3, tape=True)}
    </div>
"""
        body += f"""
  <section class="sec c-cta reveal" aria-label="{'Custom education' if cta else 'More courses'}">
{cta}    <p class="after"><a class="go" href="../">All courses</a></p>
  </section>
"""
        scripts = f'\n<script src="{root}js/course-schedule.js" defer></script>' if session_rows(sched) else ""
        write(
            f"courses/{c['slug']}/index.html",
            page(
                root,
                "courses",
                f"{course_name(c)} · Ben Collier",
                c["one_liner"],
                f"courses/{c['slug']}/",
                body,
                course_jsonld(c),
                crumbs=[("courses", "courses/"), (course_label(c), None)],
                body_class="course",
                scripts=scripts,
            ),
        )


# ---------------------------------------------------------------------------
# CV. data/cv.md stays plain Markdown; this turns it into a structured page:
# a header card, a career timeline, a section index, and section layouts
# chosen by section (timeline, cards, citations, columns). Every word of the
# CV is still real text in the HTML, so the page reads and indexes as a CV.
# ---------------------------------------------------------------------------

_MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
_SEASON = r"(?:Spring|Summer|Fall|Winter)"
_POINT = rf"(?:(?:{_MON}|{_SEASON})\s+)?(?:\d{{1,2}},\s+)?\d{{4}}"
_RANGE = rf"(?:{_MON}\s*–\s*{_MON}\s+\d{{4}}|{_POINT}(?:\s*[–-]\s*(?:{_POINT}|present))?–?)"
_WHEN = rf"{_RANGE}(?:(?:,\s*|\s+and\s+){_RANGE})*"
_ENTRY = re.compile(rf"^(?P<head>.+?),\s*(?P<when>{_WHEN})(?P<rest>(?:[.,]\s.*)?|\.?)$")

# Section layouts, by section id (the slug of its "## " heading).
CV_LAYOUT = {
    "academic-appointments": "timeline",
    "industry-experience": "timeline",
    "education": "cards",
    "honors-and-awards": "cards",
    "teaching": "columns",
    "publications-and-presentations": "citations",
    "invited-talks-and-media": "timeline",
    "academic-service": "columns",
    "professional-affiliations": "compact",
    "community": "compact",
    "links": "links",
}

# Career at a glance: (lane, label, start, end, section it jumps to).
CV_NOW = 2026.8
CV_BANDS = [
    ("Academia", "PhD, Carnegie Mellon", 2007.6, 2012.4, "education"),
    ("Academia", "CMU Qatar faculty", 2012.6, 2016.95, "academic-appointments"),
    ("Academia", "Tepper faculty", 2023.8, CV_NOW, "academic-appointments"),
    ("Industry", "UPMC Pensiamo", 2016.7, 2020.1, "industry-experience"),
    ("Industry", "Duolingo", 2020.1, 2023.45, "industry-experience"),
    ("Industry", "gAIm", 2025.35, CV_NOW, "industry-experience"),
    ("Consulting", "Hot Metal AI", 2018.8, CV_NOW, "industry-experience"),
]
CV_DEGREES = [("BBA", 2004.4), ("MBA", 2007.4), ("MS", 2009.4), ("PhD", 2012.4)]
CV_SPAN = (2004.0, 2027.0)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _course_links(html: str) -> str:
    """Link course names in the CV to their course pages."""
    for c in COURSES:
        name = f"{c['number']} {c['title']}".strip()
        html = html.replace(f"<strong>{name}</strong>",
                            f'<strong><a href="../courses/{c["slug"]}/">{name}</a></strong>')
    return html


def _doi_buttons(html: str) -> str:
    """Bare DOI and arXiv links become small labelled buttons."""
    return re.sub(r'<a href="(https://doi\.org/[^"]+)">[^<]+</a>',
                  r'<a class="pill" href="\1">DOI</a>', html)


def _cv_items(lines):
    """Group "- " list lines with their indented continuation lines."""
    items = []
    for line in lines:
        if line.startswith("- "):
            items.append([line[2:].rstrip()])
        elif line.startswith("  ") and items and line.strip():
            items[-1].append(line.strip())
    return items


# Course lists carry their own term lists ("Fall 2025, Summer 2026"); pulling
# a date column out of those would split them mid-list.
CV_NO_DATES = {"courses-built", "mba-courses", "ms-in-business-analytics-courses",
               "heinz-college", "undergraduate-courses",
               "executive-education-carnegie-mellon-university-in-qatar"}


def _cv_entry(parts, layout, dates=True):
    first, more = parts[0], parts[1:]
    m = _ENTRY.match(first) if dates else None
    when, head, desc = "", first, ""
    if m and layout != "citations":
        head, when = m.group("head"), m.group("when")
        rest = m.group("rest").lstrip(".,").strip()
        desc = rest
    body = [inline(d) for d in ([desc] if desc else []) + more]
    tm = re.match(r"^\*\*(.+?)\*\*,\s*(.+)$", head) if layout in ("timeline", "cards") else None
    if tm:
        # "**Role**, Organization" reads as a title line and an organization line.
        head_html = (f'<strong class="title">{inline(tm.group(1))}</strong>'
                     f'<span class="org">{inline(tm.group(2))}</span>')
    else:
        head_html = _doi_buttons(_course_links(inline(head)))
    desc_html = "".join(f"<p>{_doi_buttons(b)}</p>" for b in body)
    if layout == "citations":
        head_html = head_html.replace("Collier, B.", "<b>Collier, B.</b>")
    when_html = f'<span class="when">{esc(when)}</span>' if when else ""
    return f'<li class="entry{" dated" if when else ""}">{when_html}<div class="what"><div class="head">{head_html}</div>{desc_html}</div></li>'


def _cv_list(lines, layout, dates=True):
    items = _cv_items(lines)
    if not items:
        return ""
    return f'<ul class="cv-list {layout}">' + "".join(_cv_entry(i, layout, dates) for i in items) + "</ul>"


def _cv_section(title, lines):
    sid = _slug(title)
    layout = CV_LAYOUT.get(sid, "plain")
    # Split into an intro list and "### " subsections.
    subs, cur, intro = [], None, []
    for line in lines:
        if line.startswith("### "):
            cur = [line[4:].strip(), []]
            subs.append(cur)
        elif cur is not None:
            cur[1].append(line)
        else:
            intro.append(line)
    sub_layout = {"columns": "plain", "citations": "citations"}.get(layout, layout)
    inner = _cv_list(intro, layout)
    if subs:
        blocks = "".join(
            f'<div class="cv-sub"><h3 id="{_slug(h)}">{inline(h)}</h3>{_cv_list(ls, sub_layout, _slug(h) not in CV_NO_DATES)}</div>'
            for h, ls in subs
        )
        inner += f'<div class="cv-subs {layout}">{blocks}</div>'
    return sid, f'<section class="cv-sec" id="{sid}" aria-labelledby="h-{sid}"><h2 id="h-{sid}">{inline(title)}</h2>{inner}</section>'


def _cv_glance():
    lo, hi = CV_SPAN
    pct = lambda y: round(100 * (y - lo) / (hi - lo), 2)
    lanes = []
    for lane in ["Academia", "Industry", "Consulting"]:
        bars = "".join(
            f'<a class="band {_slug(lane)}" href="#{sec}" style="left:{pct(a)}%;width:{pct(b) - pct(a)}%" '
            f'title="{esc(label)}, {int(a)} to {"now" if b >= CV_NOW else int(b)}"><span>{esc(label)}</span></a>'
            for ln, label, a, b, sec in CV_BANDS if ln == lane
        )
        lanes.append(f'<div class="lane"><span class="lane-name">{lane}</span><div class="track">{bars}</div></div>')
    dots = "".join(
        f'<a class="degree" href="#education" style="left:{pct(y)}%" title="{d}, {int(y)}"><span>{d}</span></a>'
        for d, y in CV_DEGREES
    )
    lanes.append(f'<div class="lane"><span class="lane-name">Degrees</span><div class="track degrees">{dots}</div></div>')
    ticks = "".join(f'<span style="left:{pct(y)}%">{y}</span>' for y in range(2004, 2027, 4))
    return (
        '<figure class="cv-glance" aria-label="Career at a glance, 2004 to now">'
        '<figcaption>Career at a glance</figcaption>'
        f'<div class="glance-scroll"><div class="glance">{"".join(lanes)}'
        f'<div class="lane axis"><span class="lane-name"></span><div class="track ticks">{ticks}</div></div></div></div>'
        '</figure>'
    )


DIRECTIONS = "https://www.google.com/maps/dir/?api=1&destination=" + "Tepper+School+of+Business,+4765+Forbes+Ave,+Pittsburgh,+PA+15213"


def office_pop(root: str, label: str) -> str:
    """The office chip opens an animated map of campus with Tepper Quad marked.
    The SVG is drawn once by scripts/make_campus_map.py from OpenStreetMap."""
    svg = (ROOT / "assets" / "campus" / "campus-map.svg").read_text(encoding="utf-8")
    return (f'<li class="place-pop"><button type="button" class="pp-trigger" aria-expanded="false">{esc(label)}</button>'
            f'<div class="pp-card pp-map" role="dialog" aria-label="Campus map">{svg}'
            f'<p class="pp-note">Tepper Quad is on Forbes Avenue. Office 5135 is on the fifth floor. '
            f'<a href="{DIRECTIONS}">Directions</a></p></div></li>')


def address_pop(root: str, label: str) -> str:
    """The street address opens a photo of the building and a directions link."""
    return (f'<li class="place-pop"><button type="button" class="pp-trigger" aria-expanded="false">{esc(label)}</button>'
            f'<div class="pp-card pp-photo" role="dialog" aria-label="Tepper Quad">'
            f'<img src="{root}assets/campus/tepper-quad.webp" width="720" height="450" alt="Tepper Quad, the glass-fronted home of the Tepper School of Business on Forbes Avenue" loading="lazy">'
            f'<p class="pp-note"><strong>Tepper Quad</strong>, 4765 Forbes Avenue. <a href="{DIRECTIONS}">Get directions in Google Maps</a></p>'
            f'<p class="pp-credit">Photo: Tony Webster, <a href="https://commons.wikimedia.org/wiki/File:Carnegie_Mellon_University_Tepper_School_of_Business.jpg">CC BY-SA 2.0</a></p></div></li>')


PLACE_POPS = {"Tepper Quad, Office 5135": office_pop, "4765 Forbes Avenue": address_pop}


def _cv_header(lines):
    groups, cur = [], []
    for line in lines:
        if line.startswith("# "):
            continue
        if not line.strip():
            if cur:
                groups.append(cur)
                cur = []
            continue
        cur.append(line.rstrip())
    if cur:
        groups.append(cur)
    roles = "<br>".join(inline(l) for l in groups[0]) if groups else ""
    chips = []
    for g in groups[1:]:
        for line in g:
            for part in line.split(" · "):
                part = part.strip()
                if part.startswith("http"):
                    label = re.sub(r"^https?://(www\.)?", "", part).rstrip("/")
                    chips.append(f'<li><a href="{esc(part)}">{esc(label)}</a></li>')
                elif part in PLACE_POPS:
                    chips.append(PLACE_POPS[part]("../", part))
                else:
                    chips.append(f"<li>{inline(part)}</li>")
    return f"""
  <header class="cv-head reveal">
    <figure class="polaroid cv-portrait" style="--rot:-3deg"><span class="tape tc"></span><img src="../assets/portrait.jpg" width="500" height="500" alt="Portrait of Ben Collier" loading="lazy"></figure>
    <div class="cv-card">
      <p class="stamp thunk" style="--d:.15s">Curriculum vitae</p>
      <h1>Ben Collier, <span class="u u2" data-d=".4">PhD</span></h1>
      <p class="cv-roles">{roles}</p>
      <ul class="cv-contact">{"".join(chips)}</ul>
      <p class="cv-actions"><button type="button" class="btn" data-print>Print or save as PDF</button></p>
    </div>
  </header>"""


def cv_jsonld() -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "url": f"{HOST}/cv/",
        "name": "Ben Collier, PhD: curriculum vitae",
        "mainEntity": {
            "@type": "Person",
            "@id": f"{HOST}/#person",
            "name": SITE["author"],
            "honorificSuffix": "PhD",
            "jobTitle": SITE["job_title"],
            "worksFor": {"@type": "CollegeOrUniversity", "name": "Carnegie Mellon University"},
            "alumniOf": [
                {"@type": "CollegeOrUniversity", "name": "Carnegie Mellon University"},
                {"@type": "CollegeOrUniversity", "name": "University of Wisconsin–Madison"},
                {"@type": "CollegeOrUniversity", "name": "University of Wisconsin–Whitewater"},
            ],
            "award": ["George Leland Bach Teaching Award, Tepper School of Business, 2026"],
            "sameAs": SITE["same_as"],
        },
    }
    return json.dumps(data, indent=2)


def build_cv():
    md = (ROOT / "data" / "cv.md").read_text(encoding="utf-8")
    lines = md.splitlines()
    first = next(i for i, l in enumerate(lines) if l.startswith("## "))
    header = _cv_header(lines[:first])
    sections, cur = [], None
    for line in lines[first:]:
        if line.startswith("## "):
            cur = [line[3:].strip(), []]
            sections.append(cur)
        elif cur is not None:
            cur[1].append(line)
    rendered = [_cv_section(title, ls) for title, ls in sections]
    toc = "".join(f'<li><a href="#{sid}">{inline(title)}</a></li>' for (title, _), (sid, _) in zip(sections, rendered))
    body = f"""{header}
  <section class="sec glance-sec reveal" aria-label="Career at a glance">{_cv_glance()}</section>
  <div class="cv-layout">
    <nav class="cv-toc" aria-label="CV sections"><p class="note">sections</p><ol>{toc}</ol></nav>
    <article class="cv">
      {"".join(html for _, html in rendered)}
    </article>
  </div>
"""
    write(
        "cv/index.html",
        page(
            "../",
            "cv",
            "CV · Ben Collier, PhD",
            "Curriculum vitae for Ben Collier, PhD, Assistant Teaching Professor of Business Analytics at Carnegie Mellon's Tepper School of Business: appointments, teaching, advising, awards, industry experience, publications, and talks.",
            "cv/",
            body,
            cv_jsonld(),
            body_class="cv-page",
            scripts='\n<script src="../js/cv.js" defer></script>\n<script src="../js/place-pop.js" defer></script>',
        ),
    )


def portfolio_card(p, root, i=0):
    links = " ".join(f'<a class="go" href="{esc(l["href"])}">{esc(l["label"])}</a>' for l in p["links"])
    # Optional aside: context that is not the project itself, such as related
    # private work. Rendered as a margin note so it reads as a footnote to the card.
    note = f'    <p class="aside">{p["note"]}</p>\n' if p.get("note") else ""
    stats = ""
    if p.get("stats"):
        stats = '<ul class="mini-stats">' + "".join(f'<li><b>{v}</b><span>{k}</span></li>' for k, v in p["stats"]) + "</ul>"
    tall = int(p["image_height"]) > int(p["image_width"])
    rot = [-2, 1.6, -1.2, 2.2][i % 4]
    decisions = ('<ul class="dashes">' + "".join(f"<li>{d}</li>" for d in p["decisions"]) + "</ul>") if p.get("decisions") else f"<p>{p['process']}</p>"
    return f"""  <article class="pf reveal{' tall' if tall else ''}" id="{p['id']}">
    <a class="pf-shot polaroid drop" href="{esc(p['links'][0]['href'])}" style="--rot:{rot}deg;--d:.2s" tabindex="-1"><span class="tape tc"></span><img src="{root}{p['image']}" alt="{esc(p['image_alt'])}" width="{p['image_width']}" height="{p['image_height']}" loading="lazy"></a>
    <div class="pf-body">
      <p class="kicker">{esc(p['kind'])} &middot; {esc(p['date'])}</p>
      <h2>{esc(p['title'])}</h2>
      <p class="pf-tools">{esc(p['tools'])}</p>
      {stats}
      <p>{p['summary']}</p>
      {decisions}
{note}      <p class="pf-links">{links}</p>
    </div>
  </article>"""


def build_portfolio(portfolio):
    items = "\n".join(portfolio_card(p, "../", i) for i, p in enumerate(portfolio))
    body = page_head("Portfolio", "Coding with AI Projects",
                     "Working projects I built with AI coding tools, several of them for Effective Coding with AI, a Carnegie Mellon course. Each repo includes the prompts and build log, and I use them as examples in class.")
    body += f'  <div class="portfolio">\n{items}\n  </div>\n'
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
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Consulting · Ben Collier</title>'
        f'<link rel="canonical" href="{HOST}/consult/">'
        '<meta http-equiv="refresh" content="0; url=../consult/#background">'
        '<link rel="stylesheet" href="../css/site.css">'
        '</head><body><main class="sheet moved"><p class="note">This page moved to '
        '<a href="../consult/#background">Consulting</a>.</p></main></body></html>\n',
    )


def build_advising():
    data = load_json("advising.json")
    terms = []
    for pj in data["projects"]:
        if pj["term"] not in terms:
            terms.append(pj["term"])
    n = len(data["projects"])
    first = min(int(pj["term"].split()[-1]) for pj in data["projects"])
    partners = ["Westinghouse", "RBC Wealth Management", "Swank Construction", "SaratogaRIM", "Confirmed",
                "Marinus Analytics", "412 Food Rescue", "Tindoori Labs"]
    hl = ["", " g", " b", " p"]
    marked = ", ".join(f'<mark class="{hl[i % 4].strip()}" style="--d:{0.5 + 0.18 * i:.2f}s">{esc(x)}</mark>'
                       for i, x in enumerate(partners))
    tally = (f'<aside class="adv-tally sticky land" style="--rot:3deg;--d:.5s" aria-label="{n} projects since {first}">'
             f'<span class="tape tc"></span><span class="big"><span class="count" data-to="{n}" data-d=".8">{n}</span> projects</span>'
             f'<svg data-chart="tally" data-n="{n}" data-d="1"></svg><span class="since">and counting, since {first}</span></aside>')
    body = page_head(
        "Advising", "Capstones and independent studies",
        f'Since 2024 I have advised MS in Business Analytics capstone teams working with companies and nonprofits, and students doing independent studies. {n} projects so far, described here without the students\' names and without the partners\' data. Starting in Spring 2027 I also advise capstone teams in the <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>.',
        f'<p class="partners">Partners include {marked}, and a large consulting firm.</p>{tally}')
    no = 2
    for term in terms:
        cards = []
        for i, pj in enumerate(x for x in data["projects"] if x["term"] == term):
            art = draw_art(pj["art"], f"Diagram representing the project: {esc(pj['title'])}", i)
            rot = [-2, 1.5, -1, 2.4][i % 4]
            methods = "".join(f'<li style="--d:{0.9 + 0.12 * k:.2f}s">{esc(m)}</li>' for k, m in enumerate(pj["methods"]))
            srot = [-3, 2, -1.5, 2.5][i % 4]
            logo = (f'<img class="b-logo" src="../assets/partners/{pj["logo"]}" alt="" loading="lazy" decoding="async">'
                    if pj.get("logo") else "")
            cards.append(f"""    <article class="advised reveal">
      <figure class="art-print drop" style="--rot:{rot}deg;--d:.1s"><span class="tape tr"></span><button type="button" class="flip" aria-pressed="false" aria-label="Turn the print over"><span class="flipper"><span class="face">{art}</span><span class="back{" has-logo" if pj.get("logo") else ""}" aria-hidden="true">{logo}<span class="b-who">{esc(pj['partner'])}</span><span class="b-when">{esc(term)} &middot; {esc(pj['industry'].lower())}</span><span class="b-turn">&#8634; turn back</span></span></span></button></figure>
      <div class="body">
        <p class="meta"><span class="kind stamp thunk" style="--rot:{srot}deg;--d:.45s">{esc(pj['kind'])}</span> <span class="fade" style="--d:.6s">{esc(pj['partner'])} &middot; {esc(pj['industry'])}</span></p>
        <h3>{esc(pj['title'])}</h3>
        <p>{esc(pj['summary'])}</p>
        <ul class="methods">{methods}</ul>
      </div>
    </article>""")
        body += sec(no, f"t-{_slug(term)}", "Advised", term, "\n".join(cards))
        no += 1
    earlier = "".join(
        f'<li class="fade" style="--d:{0.3 + 0.12 * k:.2f}s"><span>{esc(e["term"])}</span><div>{esc(e["title"])}. <em>{esc(e["place"])}</em></div></li>'
        for k, e in enumerate(data["earlier"])
    )
    body += sec(no, "earlier", "Before Tepper", "Earlier advising",
                f'    <p class="prose">Independent studies I advised while teaching organizational behavior, mostly at Carnegie Mellon\'s campus in Qatar.</p>\n    <ul class="earlier-list">{earlier}</ul>')
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
    body = page_head(
        "Consulting", "Consulting and custom education",
        'I help organizations choose which AI and analytics projects to fund, check the models before they carry a real decision, and train their teams to run the work themselves. I do this through my practice, <mark style="--d:.7s">Hot Metal AI</mark>.',
        f'<div class="cta-row">{sticky("../book/", "Book a call &rarr;", "Most engagements start with a free 15-minute call.", "pink", -2.5, .8, True)}</div>')
    body += """
  <div class="kinds reveal">
    <section class="kind deal" id="education" style="--rot:-.8deg;--d:.2s">
      <span class="tape tc"></span>
      <p class="kicker">Custom education</p>
      <h2>Training built on your data</h2>
      <p>Workshops and courses for technical teams and executives, built around your own data and problems. Most of the time is spent in hands-on labs.</p>
      <h3>Formats</h3>
      <ul class="dashes">
        <li>One- to three-day workshops, on site or online</li>
        <li>Multi-week programs for technology leaders and executives</li>
        <li>Recorded, self-paced courses</li>
      </ul>
      <h3>Examples</h3>
      <ul class="dashes">
        <li>Three-day executive programs at Carnegie Mellon University in Qatar on <a href="../courses/exec-negotiation/">negotiation</a>, <a href="../courses/exec-decision-making/">decision making</a>, <a href="../courses/exec-teams/">managing teams</a>, and <a href="../courses/exec-leadership/">leadership</a>, with up to 114 managers in the room from ministries, energy, banking, telecom, aviation, and media.</li>
        <li><a href="../courses/exec-custom/">Workshops built for one organization</a>: RasGas, a Carnegie Mellon senior staff retreat in Munich, and Qatar's Civil Service Bureau.</li>
        <li>Professional development courses for technology leaders and executives at Optum, AT&amp;T, Cox Communications, and RapidScale.</li>
        <li>At Carnegie Mellon in Qatar I co-directed executive and professional education. In 2014 to 2015 the program taught 755 participants from more than 30 government and private-sector organizations across Qatar. <a href="https://www.qatar.cmu.edu/news/more-than-700-participants-complete-cmu-qs-executive-and-professional-education-program/">CMU-Q news</a></li>
        <li>Workshops on chatbot development, data programming, SQL and NoSQL, data mining, cloud infrastructure, and agile development.</li>
        <li>The kind of recorded course I can build for a team: the <a href="../courses/msba-math-skills-workshop/">MS in Business Analytics Math Skills Workshop</a>, about thirty short videos I scripted and recorded for incoming Carnegie Mellon MS in Business Analytics students.</li>
      </ul>
    </section>

    <section class="kind deal" id="ai-data" style="--rot:.7deg;--d:.4s">
      <span class="tape tc"></span>
      <p class="kicker">AI and data consulting</p>
      <h2>Reviews and builds</h2>
      <p>From deciding which AI projects are worth funding to reviewing a model before it carries a real decision.</p>
      <h3>Formats</h3>
      <ul class="checks">
        <li><svg data-chart="check" data-d="0.6"></svg><span><b>AI use-case review.</b> About two weeks. A written go or no-go on the projects you are considering, with a build plan for the ones worth doing.</span></li>
        <li><svg data-chart="check" data-d="0.9"></svg><span><b>Model or metric review.</b> About one week. I read the code, data, and evaluation, and tell you where it breaks.</span></li>
        <li><svg data-chart="check" data-d="1.2"></svg><span><b>Hands-on build.</b> Scoped with you: a prototype, a pipeline, or an evaluation harness your team can keep running.</span></li>
      </ul>
      <h3>Through Hot Metal AI</h3>
      <ul class="dashes">
        <li>A recommendation engine for healthcare specialist referrals, built for a healthcare client.</li>
      </ul>
      <h3>In industry roles</h3>
      <ul class="dashes">
        <li>At <a href="https://www.upmc.com/">UPMC</a>'s Pensiamo, as founding data scientist on a joint venture with <a href="https://en.wikipedia.org/wiki/IBM_Watson_Health">IBM Watson Health</a>, I did the machine learning research and built the production pipelines for CognitiveRx, a drug price and shortage tool for a 40-hospital system buying $1.5 billion of pharmaceuticals a year. <a href="https://premierinc.com/">Premier</a> later acquired it.</li>
        <li>At <a href="https://www.duolingo.com/">Duolingo</a>, experimentation, monetization analytics, and forecasting through the IPO and the launch of Duolingo Max.</li>
        <li>At <a href="https://www.gaimsystems.com/">gAIm Systems</a>, AI tools and research studies that help sports teams recruit players, develop them, and build rosters.</li>
      </ul>
    </section>
  </div>

  <section class="sec reveal" aria-label="Advising">
    <p class="prose">I also advise MS in Business Analytics capstone teams working with companies such as Westinghouse, RBC Wealth Management, and Swank Construction, and starting in Spring 2027, capstone teams in the <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>. <a href="../advising/">See those projects</a>.</p>
    <div class="cta-row">
      <a class="btn primary" href="../book/">Book time</a>
      <span class="muted">Most engagements start with a free 15-minute call.</span>
    </div>
  </section>
"""
    bg = [
        ("2025 to now", "gAIm Systems", "Senior Director of AI and Data Science"),
        ("2023 to now", "Tepper School of Business, Carnegie Mellon", "Assistant Teaching Professor of Business Analytics, after starting as an adjunct in Fall 2023"),
        ("2020 to 2023", "Duolingo", "Staff Data Scientist, on monetization"),
        ("2018 to now", "Hot Metal AI", "Founder. Analytics consulting and corporate training, alongside everything else"),
        ("2016 to 2020", "UPMC's Pensiamo", "Senior Director of Data Science"),
        ("2012 to 2016", "Carnegie Mellon University in Qatar", "Assistant Teaching Professor of Organizational Behavior, and co-director of executive education"),
    ]
    items = "".join(
        f'<li class="fade" style="--d:{0.2 + 0.15 * i:.2f}s"><span class="when">{w}</span><span class="dot-i" aria-hidden="true"></span><p><strong>{o}</strong> {r}</p></li>'
        for i, (w, o, r) in enumerate(bg)
    )
    body += sec(3, "background", "Background", "Background",
                f'    <ol class="vtl">{items}</ol>\n    <p class="after"><a class="go" href="../cv/">Full CV</a></p>')
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
    body = page_head(
        "Book time", "Book a call",
        'Start with a free intro call, or book a working hour on a specific problem. Not sure what you need? See the kinds of <a href="../consult/">consulting and custom education</a> I do.')
    body += f"""
  <div class="offers reveal">
    <section class="offer sticky-card land" style="--rot:-2deg;--d:.2s">
      <span class="tape tc"></span>
      <p class="kicker">15 minutes &middot; online &middot; free</p>
      <h2>Intro call</h2>
      <p>A short call to see whether I can help. Tell me what you are working on, and I will tell you plainly whether it is a fit and what a sensible first step would be.</p>
      {book_link("freeChat", "Book a free 15-minute call", "../")}
    </section>
    <section class="offer sticky-card pink land" style="--rot:1.6deg;--d:.45s">
      <span class="tape tc"></span>
      <p class="kicker">60 minutes &middot; online &middot; {HOURLY_RATE}</p>
      <h2>Consulting hour</h2>
      <p>One working session on a decision you are stuck on: a model that will not hold up, a metric nobody trusts, an AI use case you are not sure is worth building, or a hiring bar for a data team.</p>
      <ul class="dashes">
        <li>Live session on Zoom or Google Meet</li>
        <li>A one-page written recommendation within two business days</li>
        <li data-live-text="Paid when you book">Invoiced before we meet</li>
      </ul>
      {book_link("paidHour", "Book a consulting hour", "../")}
    </section>
  </div>
"""
    body += sec(2, "fit", "Choosing", "Which option fits", f"""    <ul class="checks prose">
      <li><svg data-chart="check" data-d="0.4"></svg><span><strong>Not sure yet?</strong> Start with the intro call. It is free, and by the end you will know whether you need anything more.</span></li>
      <li><svg data-chart="check" data-d="0.7"></svg><span><strong>One specific decision or blocker?</strong> A consulting hour is usually enough.</span></li>
      <li><svg data-chart="check" data-d="1.0"></svg><span><strong>Training for a team, or a project that needs weeks?</strong> Book the intro call and we will scope <a href="../consult/#education">custom education</a> or <a href="../consult/#ai-data">AI and data consulting</a>.</span></li>
    </ul>
    <p class="prose">Prefer email? Write to <a href="mailto:{BOOK_EMAIL}">{BOOK_EMAIL}</a>.</p>""")
    write(
        "book/index.html",
        page(
            "../",
            "book",
            "Book a call · Ben Collier",
            "Book a free 15-minute intro chat or a consulting hour with Ben Collier.",
            "book/",
            body,
            crumbs=[("book a call", None)],
        ),
    )


def build_news():
    body = page_head("Teaching and practice", "News", "A dated log of teaching, advising, and practice.")
    body += f"""
  <section class="sec reveal headless" aria-label="News log">
    {news_items(root="../")}
  </section>
"""
    body += sec(2, "linkedin", "Shared elsewhere", "On LinkedIn", '    <ol class="feed log" id="linkedin-all"></ol>')
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


# Slides from the August 2026 AI-Exchange talk, rendered from Ben's own deck.
# Only his text slides: no student names or work, no third-party figures.
TALK_SLIDES = {
    "ai-exchange-2026": [
        ("45884-vit", "From AI Methods for Social and Visual Data: MBA students learn how Vision Transformers apply attention to image patches."),
        ("45884-embedding", "From AI Methods for Social and Visual Data: a joint embedding space where images and text sit side by side."),
        ("45884-waymo", "From AI Methods for Social and Visual Data: the Tesla Vision versus Waymo case, cameras against lidar and radar."),
        ("blooms", "How AI Methods for Social and Visual Data maps to Bloom's taxonomy: quizzes for remembering, labs for applying, the final project and AI in the News for creating."),
        ("70445-muffin", "From Artificial Intelligence for Business Leaders: muffin or chihuahua? You can spot it. Now write the rule."),
        ("70445-harness", "From Artificial Intelligence for Business Leaders: agent = model + harness, the idea behind the course's agent unit."),
    ],
    "kellogg-2025": [
        ("setup", "The experiment: treatment teams revise news charts with the AI coach before presenting; control teams revise without it."),
        ("feedback-theory", "Why feedback can backfire: Kluger and DeNisi's model of where feedback helps and where it hurts."),
        ("original-pie", "A chart a team brought in, with the strengths and problems they found."),
        ("coach-suggestions", "The same data after the coach's questions: a diverging bar, direct labels, and color that carries meaning."),
        ("recommendation", "The coach's recommendation on another team's chart, with what improved and what still needs work."),
        ("results", "What students reported: 97 percent said the coach gave them incorrect or conflicting feedback at least once, which is part of the lesson."),
    ],
}


def talk_slide(talk: str, name: str, cap: str, i: int) -> str:
    src = f"../assets/talks/{talk}-{name}.jpg"
    rot = [-1.8, 1.4, -0.9, 2, -1.4, 1][i % 6]
    return (
        f'      <figure class="tprint drop" style="--rot:{rot}deg;--d:{0.15 + 0.12 * i:.2f}s">\n'
        f'        <span class="tape tc"></span><a href="{src}"><img src="{src}" width="1200" height="675" loading="lazy" alt="Slide: {esc(cap)}"></a>\n'
        f'        <figcaption>{cap}</figcaption>\n'
        f'      </figure>'
    )


def talk_slides(talk: str) -> str:
    return "\n".join(talk_slide(talk, n, c, i) for i, (n, c) in enumerate(TALK_SLIDES[talk]))


def talk_card(when: str, event: str, where: str, fmt: str, rot: float = 2) -> str:
    """The index card pinned beside a talk's write-up: when, where, and what kind of session."""
    rows = "".join(f'<span class="tc-k">{k}</span><span class="tc-v">{esc(v)}</span>'
                   for k, v in (("when", when), ("at", event), ("where", where), ("format", fmt)))
    return (f'<aside class="talk-card land" style="--rot:{rot}deg;--d:.35s" aria-label="Talk details">'
            f'<span class="tape tc"></span>{rows}</aside>')


def build_talks():
    body = page_head("Talks", "Talks", "Talks and workshops on building AI courses, teaching with AI, and putting analytics to work.")
    body += sec(2, "talk-aix", "August 7, 2026 &middot; Tepper AI-Exchange &middot; Carnegie Mellon University, Pittsburgh",
                "Lessons Learned from Developing New AI Courses for MBA and Undergraduate Business Students", f"""    <div class="talk-row">
    <div class="prose">
      <p>Over the past year I designed and taught a new MBA elective, <a href="../courses/45-884/">AI Methods for Social and Visual Data</a>, and I was developing an undergraduate course, <a href="../courses/70-445/">Artificial Intelligence for Business Leaders</a>, launching that fall. In this talk I shared what has worked well in the MBA classroom, from assignment design to helping students build hands-on skills with modern AI tools, along with what I was changing or trying differently in the new undergraduate course. I also gave a brief introduction to a large randomized controlled trial of AI in the classroom that I am taking part in, and what we hope to learn from it about how AI actually affects student outcomes.</p>
      <p>The session closed as a discussion with the faculty in the room: what they would add to the undergraduate course, what did not fit, and how Tepper should approach a flagship AI course for undergraduates.</p>
    </div>
    {talk_card("August 7, 2026", "Tepper AI-Exchange", "Carnegie Mellon University, Pittsburgh", "Faculty talk, then an open discussion", rot=2.2)}
    </div>
    <h3 class="sub-h">Selected slides</h3>
    <div class="tslides">
{talk_slides("ai-exchange-2026")}
    </div>""", cls="talk")
    body += sec(3, "talk-kellogg", "June 5, 2025 &middot; Teaching with AI Summer Workshop &middot; Kellogg School of Management, Northwestern University",
                "AI Data Visualization Coach", f"""    <div class="talk-row">
    <div class="prose">
      <p>A flash talk with my colleague Zoey Jiang on the custom GPT we built for <a href="../courses/45-885/">Data Visualization</a>. Before presenting a chart redesign, teams test it with the coach. It will not hand over a redesign. It questions the team from three seats: a journalist, a chart designer, and a business stakeholder.</p>
      <p><a class="go" href="https://www.kellogg.northwestern.edu/events/conference/teaching-with-ai/">Workshop program</a></p>
    </div>
    {talk_card("June 5, 2025", "Teaching with AI Summer Workshop", "Kellogg School of Management, Evanston", "Flash talk, with Zoey Jiang", rot=-2.4)}
    </div>
    <h3 class="sub-h">Selected slides</h3>
    <div class="tslides">
{talk_slides("kellogg-2025")}
    </div>""", cls="talk")
    body += sec(4, "talk-spotlight", "April 30, 2026 &middot; Tepper School of Business",
                "Faculty Spotlight: what students learn in the MS in Business Analytics", """    <div class="talks-grid">
      <a class="video polaroid drop" href="https://www.youtube.com/watch?v=UxBPkez6Mc4" style="--rot:-1.8deg;--d:.2s" aria-label="Watch the Faculty Spotlight video on YouTube, 11 minutes">
        <span class="tape tl"></span><span class="tape br"></span>
        <span class="ph"><img src="../assets/talks/faculty-spotlight-2026.jpg" width="1280" height="720" loading="lazy" alt="Ben Collier explaining a point during the Tepper Faculty Spotlight conversation"><span class="vplay big" aria-hidden="true"></span><svg class="play" data-chart="play" data-d="0.9"></svg></span>
        <span class="cap">Faculty Spotlight &middot; 11 min</span>
      </a>
      <div class="prose">
        <p>A conversation for Tepper about the MS in Business Analytics curriculum, and why I describe business analytics as a decathlon.</p>
        <p><a class="go" href="https://www.youtube.com/watch?v=UxBPkez6Mc4">Watch on YouTube</a></p>
      </div>
    </div>""", cls="talk")
    body += sec(5, "earlier-talks", "Before that", "Earlier talks", """    <ul class="earlier-list">
      <li><span>Sep 2026</span><div>Business Analytics track information session. <em>Tepper MBA program</em></div></li>
      <li><span>2025, 2026</span><div>Perspectives on Analytics. <em>BaseCamp orientation for incoming part-time MS in Business Analytics students, Tepper School of Business</em></div></li>
      <li><span>Nov 2025</span><div>Managing groups and teams: strategies for collaborative excellence. <em>Community partner workshop, Carnegie Mellon University in Qatar</em></div></li>
      <li><span>Mar 2025</span><div>Traditional AI: data mining and data visualization, and AI tools for research. <em>Colloquium on AI for Business, Tepper School of Business</em></div></li>
      <li><span>2024, 2025</span><div>Using statistics to solve business problems, and to estimate the unknown. <em>Business Analytics Summer Summit, Tepper School of Business</em></div></li>
      <li><span>2015</span><div>Creating a culture for innovation in teams. <em>RasGas Company, Doha</em></div></li>
      <li><span>2014</span><div>Digital marketing for entrepreneurs. <em>International Telecommunication Union World Conference</em></div></li>
      <li><span>2014</span><div>Leadership in groups and organizations. <em>Cultivate Leadership Workshop, Hamad Bin Khalifa University</em></div></li>
    </ul>
    <div class="cta-row">
      <a class="btn primary" href="../book/">Ask about a talk or workshop</a>
      <span class="muted">I speak to faculty, executive, and industry audiences about AI in business and in the classroom.</span>
    </div>""")
    write(
        "talks/index.html",
        page(
            "../",
            "talks",
            "Talks · Ben Collier",
            "Talks by Ben Collier on building AI courses, teaching with AI, and business analytics, with slides.",
            "talks/",
            body,
        ),
    )


def build_contact():
    site_row = ('        <li><span>Site</span><div><a href="../">' + DOMAIN_LABEL + '</a></div></li>\n') if SITE.get("domain_live") else ""
    body = page_head("", "Contact", "Email is the most reliable way to reach me. Students, please put the course number in the subject line.")
    body += f"""
  <section class="sec reveal" aria-label="Contact details">
    <div class="contact-grid">
      <ul class="contact-list card-lined deal" style="--rot:-.6deg;--d:.2s">
        <li><span>CMU email</span><div><a href="mailto:bcollier@cmu.edu">bcollier@cmu.edu</a></div></li>
        <li><span>Personal</span><div><a href="mailto:ben@collier.phd">ben@collier.phd</a></div></li>
{site_row}        <li><span>Office</span><div>Office 5135, Tepper Quad<br>Tepper School of Business, Carnegie Mellon University<br>4765 Forbes Avenue<br>Pittsburgh, PA 15213</div></li>
        <li><span>Consulting</span><div>{book_call("../", "")} &middot; <a href="../consult/">Consulting and custom education</a></div></li>
        <li><span>Students</span><div><a data-book="studentHours" data-live-label="Book a 30-minute appointment" href="mailto:bcollier@cmu.edu">Email me</a> two times that work for office hours and I will confirm one.</div></li>
        <li><span>LinkedIn</span><div><a href="https://www.linkedin.com/in/bcollierphd">linkedin.com/in/bcollierphd</a></div></li>
        <li><span>GitHub</span><div><a href="https://github.com/bcollier">github.com/bcollier</a></div></li>
        <li><span>ORCID</span><div><a href="https://orcid.org/0000-0002-4651-7684">0000-0002-4651-7684</a></div></li>
        <li><span>CV</span><div><a href="../cv/">Full CV</a></div></li>
      </ul>
      <div class="contact-side">
        {sticky("../book/", 'Book a free <span class="nw">15-minute call &rarr;</span>', rot=3, d=.6, tape=True)}
      </div>
    </div>
  </section>
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


# ---------------------------------------------------------------------------
# Strengths: what two Gallup StrengthsFinder results (2009, 2014) say about
# how I work, checked against what I have actually done. Theme definitions
# are paraphrased; the reports themselves stay private.
# ---------------------------------------------------------------------------

SF_DOMAIN = {"Intellection": "think", "Learner": "think", "Input": "think", "Futuristic": "think",
             "Achiever": "exec", "Individualization": "rel"}
SF_DOMAIN_NAME = {"think": "Strategic thinking", "exec": "Executing", "rel": "Relationship building", "infl": "Influencing"}
SF_RANKS = [  # theme, 2009 rank, 2014 rank (None = outside the top five)
    ("Input", 1, 4), ("Learner", 2, 3), ("Individualization", 3, None),
    ("Intellection", 4, 1), ("Achiever", 5, 2), ("Futuristic", None, 5),
]


def strengths_chart() -> str:
    """Slope chart of the two top-five rankings, drawn as notebook ink."""
    x0, x1, y = 150, 430, lambda r: 64 + (r - 1) * 44 if r else 300
    out = ['<svg class="sf-chart" viewBox="0 0 580 330" role="img" aria-label="How my top five themes moved between 2009 and 2014. '
           'Intellection rose from fourth to first, Achiever from fifth to second, Learner slipped from second to third, Input from first to fourth. '
           'Individualization left the top five and Futuristic entered it at fifth.">',
           f'<text class="sf-yr" x="{x0}" y="30" text-anchor="middle">2009</text>',
           f'<text class="sf-yr" x="{x1}" y="30" text-anchor="middle">2014</text>',
           f'<line class="sf-out" x1="40" x2="540" y1="282" y2="282"/>',
           f'<text class="sf-outlab" x="290" y="320" text-anchor="middle">outside the top five</text>']
    for i, (name, a, b) in enumerate(SF_RANKS):
        dom = SF_DOMAIN[name]
        ya, yb = y(a), y(b)
        d = 0.3 + 0.25 * i
        out.append(f'<path class="ink sf-line {dom}" pathLength="1000" style="--d:{d:.2f}s;--dur:1.1s" '
                   f'd="M{x0},{ya} C{x0 + 110},{ya} {x1 - 110},{yb} {x1},{yb}"/>')
        for x, r, side in ((x0, a, "end"), (x1, b, "start")):
            yy = y(r)
            out.append(f'<circle class="dot sf-pt {dom}{" ghost" if not r else ""}" cx="{x}" cy="{yy}" r="6" style="--d:{d + 0.2:.2f}s"/>')
            if r:
                lx = x - 16 if side == "end" else x + 16
                out.append(f'<text class="sf-name fade" x="{lx}" y="{yy + 5}" text-anchor="{side}" style="--d:{d + 0.3:.2f}s">'
                           f'<tspan class="sf-rk">{r}</tspan> {name}</text>')
    out.append("</svg>")
    return "".join(out)


SF_THEMES = [
    ("Intellection", 4, 1, "I like to think, and I need time alone to do it.",
     "Gallup describes Intellection as a constant mental hum: people who need room to reflect, who argue with themselves to test an idea, and who would rather be in at the start of a project than handed it at the end.",
     ["It was my top theme in 2014, the year I was teaching organizational behavior and running executive programs in Doha.",
      "The part of building a course I enjoy most is the design: deciding what students should be able to do at the end, then working backward to each session.",
      "My PhD was a long reflection on how leaders emerge in open communities like Wikipedia, which still shapes how I think about teams."]),
    ("Achiever", 5, 2, "Every day starts at zero, and I need to finish something by the end of it.",
     "Achievers measure a good day by what got done. The drive restarts every morning, which brings stamina and a steady whisper of discontent.",
     ["I rebuild courses on almost every run: Data Visualization moved entirely into Tableau with about fifty short screencast lessons, and Data Mining moved from R to Python.",
      "At CMU Qatar I taught a full undergraduate load while co-directing executive education, including three-day programs for up to 114 managers.",
      "In 2009, writing about my first results, I joked that a PhD student needed a strength called EnjoysWorkingVeryHardForLittlePay."]),
    ("Learner", 2, 3, "The trip from not knowing to knowing is the part I enjoy.",
     "Learners are drawn to the process of getting good at something more than to the credential at the end. New subjects and fast-changing fields energize them.",
     ["When I moved from teaching organizational behavior into data science, I did it by taking the ten-course Data Science Specialization in 2015.",
      "I took graduate computer science courses through Georgia Tech's online program in 2018 and 2019, while working full time.",
      "In 2026 I took Effective Coding with AI as a student. Several of the projects on this site came out of it."]),
    ("Input", 1, 4, "I collect things: books, articles, data, examples.",
     "People strong in Input are curious collectors who keep things because one day they might be useful. The test's own warning is that input without output goes stale.",
     ["My reading library has more than a thousand ebooks, and I have kept a dated folder for every project since 2012.",
      "I save AI news as I read it. That habit turned into AI in the News, the student briefings that open my classes.",
      "This website is partly an answer to the warning: a place to turn what I have collected into something other people can use."]),
    ("Futuristic", None, 5, "I spend a lot of time thinking about what comes next.",
     "Futuristic people are pulled forward by a detailed picture of what could be, and they use that picture to energize the people around them.",
     ["It entered my top five in 2014. Two years later I left academia for data science at UPMC and then Duolingo, and came back to teach AI.",
      "My newest courses, AI Methods for Social and Visual Data and Artificial Intelligence for Business Leaders, are built around what is changing.",
      "I ask each class for its odds on AI going very well and very badly. This fall's median answers were 30 percent and 20 percent."]),
    ("Individualization", 3, None, "Everyone is different, and the differences are the point.",
     "Individualization is a gift for noticing what is distinct about each person and how different people can fit together.",
     ["It was third in 2009 and outside the top five in 2014, but I do not think it went anywhere. My 2014 Achiever description was mostly about listening and recognizing other people.",
      "My executive programs in Doha drew managers from 25 organizations, from ministries to banks to an airline, and the work was making one room useful to all of them.",
      "Advising capstones is the same skill: every team, partner, and question is different."]),
]


def strengths_rank_tag(a, b) -> str:
    fmt = lambda r: f"#{r}" if r else "not top 5"
    return f'<span class="sf-tag">2009 {fmt(a)} &rarr; 2014 {fmt(b)}</span>'


def build_strengths():
    body = page_head("Strengths", "Strengths",
                     "I have taken Gallup's StrengthsFinder twice: in 2009 as a PhD student in Pittsburgh, and in 2014 as a professor in Doha. "
                     "Four of the same five themes came back both times. This page is what they say about how I work, checked against what I have actually done.",
                     stamp="Two tests &middot; five years apart")
    domains = "".join(
        f'<li class="{k}"><span class="sf-n">{n}</span><span class="sf-dl">{SF_DOMAIN_NAME[k]}</span></li>'
        for k, n in (("think", "4 of 5"), ("exec", "1 of 5"), ("rel", "1 in 2009"), ("infl", "none"))
    )
    body += sec(2, "sf-snap", "2009 and 2014", "Two snapshots", f"""    <div class="sf-snap">
      <figure class="sf-fig fade">{strengths_chart()}</figure>
      <div class="prose">
        <p>StrengthsFinder ranks 34 themes of talent for each person and reports the top five. My two lists share four themes: <strong>Input, Learner, Intellection, and Achiever</strong>. What moved is the order and one name at the edge.</p>
        <p>In 2009 my profile led with collecting and learning. By 2014 it led with thinking and finishing, <strong>Futuristic</strong> had arrived, and <strong>Individualization</strong> had dropped out.</p>
        <p>Gallup groups the themes into four domains. Mine sit almost entirely in one of them.</p>
        <ul class="sf-domains">{domains}</ul>
        <p class="note">no influencing themes, either time &darr;</p>
      </div>
    </div>""")
    stick = [
        ("Collect, then think", "Input and Intellection: I gather widely, then go quiet and work out what it means.", "", -2.5),
        ("Learning is the work", "Learner and Achiever: getting good at something new is how I make progress.", "pink", 2),
        ("Then look ahead", "Futuristic: once I understand something, I want to know where it is going.", "", -1.5),
    ]
    notes = "".join(
        f'<div class="sticky land sf-stick{(" " + c) if c else ""}" style="--rot:{r}deg;--d:{0.2 + 0.2 * i:.1f}s"><span class="big">{h}</span><span class="sub">{s}</span></div>'
        for i, (h, s, c, r) in enumerate(stick)
    )
    body += sec(3, "sf-short", "If you only read one part", "The short version", f'    <div class="sf-sticks">{notes}</div>')
    cards = ""
    for i, (name, a, b, line, gallup, evidence) in enumerate(SF_THEMES):
        dom = SF_DOMAIN[name]
        ev = "".join(f"<li>{e}</li>" for e in evidence)
        cards += f"""      <article class="sf-card {dom} deal" style="--rot:{CARD_ROT[i % len(CARD_ROT)] * 0.5}deg;--d:{0.15 + 0.1 * i:.2f}s">
        <span class="tape tc"></span>
        <p class="sf-dom">{SF_DOMAIN_NAME[dom]}</p>
        <h3>{name}</h3>
        {strengths_rank_tag(a, b)}
        <p class="sf-line">{line}</p>
        <p class="sf-gallup">{gallup}</p>
        <ul class="dashes">{ev}</ul>
      </article>
"""
    body += sec(4, "sf-themes", "Each theme, with evidence", "Theme by theme", f'    <div class="sf-cards">\n{cards}    </div>')
    work = [
        ("Ask me a question and you may get a reading list.", "Input and Learner"),
        ("Bring me in early. I am most useful when we are still deciding what problem we are solving.", "Intellection"),
        ("I like to finish something every day, and I keep improving things after they ship.", "Achiever"),
        ("I will talk about where things are going. Hold me to the concrete next step.", "Futuristic"),
        ("I persuade with evidence and examples, not force of personality.", "no influencing themes"),
    ]
    items = "".join(f'<li><span>{w}</span><em>{why}</em></li>' for w, why in work)
    body += sec(5, "sf-work", "For students, colleagues, and clients", "Working with me", f'    <ul class="sf-work">{items}</ul>')
    body += sec(6, "sf-test", "Read with care", "What the test can and cannot tell you", """    <div class="prose">
      <p>StrengthsFinder ranks your themes against each other, not against other people. A theme at number six is still strong; it just did not make the list. Themes near the cut line can trade places between sittings, so Individualization slipping out in 2014 is partly a real change and partly the noise you would expect from any self-report measure.</p>
      <p>I teach organizational behavior and statistics, so I hold both of those thoughts at once. I used StrengthsFinder with my own students at CMU Qatar in 2014, as a starting point for a leadership assignment rather than a verdict. That is how I read my own results too.</p>
      <p class="muted">Theme descriptions on this page are my paraphrases of Gallup's. CliftonStrengths and StrengthsFinder are trademarks of Gallup, Inc. I wrote about my first results in <a href="https://ocis.wordpress.com/2009/03/10/strengthsfinder/">a short post in 2009</a>.</p>
    </div>""")
    write("strengths/index.html", page("../", "strengths", "Strengths · Ben Collier",
                                       "What two StrengthsFinder results, five years apart, say about how I work.", "strengths/", body))


def build_travel():
    data = load_json("travel.json")
    places = data["countries"]
    chips = "".join(
        f'<li><button type="button" data-cc="{p["cc"]}">{esc(p["name"])}</button></li>' for p in sorted(places, key=lambda p: p["name"])
    )
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    body = page_head("Travel", "Places I have been",
                     f"{len(places)} countries so far, mapped from my own photo library. Hover a dot or a highlighted country to see what I saw there, or pick one from the list.")
    body += f"""
  <section class="sec travel-sec" aria-label="Map of places visited">
    <div class="view-tabs" role="tablist" aria-label="Map or globe">
      <button type="button" role="tab" aria-selected="true" data-view="map">Map</button>
      <button type="button" role="tab" aria-selected="false" data-view="globe">Globe</button>
    </div>
    <div class="map-card">
      <span class="tape tr"></span>
      <div id="view-map" class="worldmap-wrap">
        <div id="worldmap" class="worldmap"></div>
        <div id="map-pop" class="map-pop" hidden></div>
      </div>
      <div id="view-globe" class="travel" hidden>
        <div id="globe" class="globe"></div>
        <aside id="globe-card" class="globe-card" aria-live="polite" hidden></aside>
      </div>
    </div>
    <dialog id="photo-view" class="photo-view"><img alt=""><p></p><button type="button" aria-label="Close">×</button></dialog>
    <p class="note list-note">or pick a country</p>
    <ul class="country-list">{chips}</ul>
    <script type="application/json" id="travel-data">{blob}</script>
  </section>
"""
    scripts = ('\n<script src="../assets/vendor/d3.min.js" defer></script>'
               '\n<script src="../assets/vendor/topojson-client.min.js" defer></script>'
               '\n<script src="../js/travel.js" defer></script>'
               '\n<script src="../js/travel-map.js" defer></script>')
    write(
        "travel/index.html",
        page("../", "travel", "Travel · Ben Collier", f"{len(places)} countries, mapped from my photos.", "travel/", body, scripts=scripts),
    )


def build_404():
    body = page_head("Error 404", "Page not found", "That URL is not on this site.",
                     '<p class="links-404"><a class="go" href="./">Home</a> <a class="go" href="./courses/">Courses</a> <a class="go" href="./projects/">Coding with AI Projects</a> <a class="go" href="./cv/">CV</a></p>'
                     '<p class="note red big-note">this page is missing from the notebook</p>')
    write(
        "404.html",
        page("", "404", "Not found · Ben Collier", "Page not found.", "404.html", body, crumbs=[("missing pages", None)]),
    )


def site_paths():
    """Every canonical URL path on the site, in navigation order."""
    paths = ["", "consult/", "book/", "advising/", "courses/", "projects/", "talks/", "cv/", "news/", "contact/", "travel/", "strengths/"]
    paths += [f"courses/{c['slug']}/" for c in ALL_COURSES]
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
    for iso, text, *rest in NEWS:
        stamp = rfc3339(iso)
        href = news_link(rest[0], f"{HOST}/") if rest else f"{HOST}/news/"
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
    build_talks()
    build_contact()
    build_travel()
    build_strengths()
    build_404()
    build_sitemap()
    build_robots()
    build_feed()
    print(f"done: absolute URLs point at {HOST}")


if __name__ == "__main__":
    main()
