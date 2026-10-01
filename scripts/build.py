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
    ("2026-09-29", "Led the information session for MBA students considering the Business Analytics track.", "https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics", "About the track"),
    ("2026-09-24", "Opened the 70-445 agent lab with how fast this is moving. A year earlier, superforecasters put the chance of AI solving a Millennium Prize problem by this fall at 1.7 percent, and industry experts at 4.6 percent. Two weeks before class, it happened.", "https://forecastingresearch.substack.com/p/ai-progress-forecasts-accuracy", "The forecasts"),
    ("2026-09-24", "Same class: Dartmouth's provost defended having used AI on his published writing since 2022, after a detector flagged it as almost entirely AI-written. We talked about where assistance ends and authorship begins.", "https://www.thedartmouth.com/article/2026/09/schnell-ai-writing", "The story"),
    ("2026-09", "Became faculty coordinator of the MBA Business Analytics track at Tepper.", "https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics", "About the track"),
    ("2026-09-10", "Opened 70-445 with OpenAI's proof of the Navier-Stokes problem, one of the seven $1 million Millennium Prize problems, announced a few hours after our previous class. By our rough math in class, it took about $100 million of compute to win a $1 million prize.", "https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/", "The story"),
    ("2026-09-10", "Same class, darker headline: an Anthropic alignment lead put the chance that AI kills all humans within a decade at more than 10 percent. We set it next to the p(doom) numbers other AI leaders have given, and a week later the class gave its own. The median was 20 percent.", "https://www.forbes.com/sites/siladityaray/2026/09/09/anthropic-alignment-lead-warns-ai-could-kill-all-humans-as-researcher-quits/", "The story"),
    ("2026-09-08", "Started 70-445 on the GPT-6 Astra launch, which reached the human baseline on ARC-AGI-3 the evening after our last class. Jensen Huang posted that AGI has arrived. We put his claim next to Yann LeCun's skepticism.", "https://www.foxbusiness.com/technology/nvidia-ceo-jensen-huang-declares-agi-has-arrived-after-openai-unveils-gpt-6-astra", "The story"),
    ("2026-08-27", "Opened the history of AI in 70-445 with the Mechanical Turk, the 1770 chess machine with a person hidden inside, and the news from the day before: Amazon is shutting down its Mechanical Turk marketplace after 21 years, the human workforce that labeled data for a generation of machine learning.", "https://techstartups.com/2026/08/26/top-tech-news-today-august-26-2026-amazon-anthropic-google-microsoft-waymo-more/", "The story"),
    ("2026-08-25", "Taught the first class of 70-445 Artificial Intelligence for Business Leaders, a new undergraduate course I built. Students learn how AI works, work hands-on with AI agents, and then judge where AI creates value across marketing, finance, operations, and strategy, and how to defend that judgment to executives."),
    ("2026-08-24", "Started the third run of 45-884 AI Methods for Social and Visual Data, with agents moved earlier in the term and a summary and cleaned transcript for students after every class."),
    ("2026-08-07", "Led a discussion at the Tepper AI-Exchange on what I learned building two new AI courses: what worked in the MBA course AI Methods for Social and Visual Data, and what I was changing for the new undergraduate course, Artificial Intelligence for Business Leaders.", "talks/", "Slides and summary"),
    ("2026-08", "Finished recording the MS in Business Analytics Math Skills Workshop, a self-paced course for incoming MS in Business Analytics students that runs from algebra through gradient descent, PCA, and statistical inference."),
    ("2026-05-09", "Received the George Leland Bach Excellence in Teaching Award, voted by the MBA Class of 2026 and presented at the MBA diploma ceremony.", "https://www.youtube.com/watch?v=wkVLIOVPTbU&t=2890s", "Watch the presentation"),
    ("2026-06", "Really proud of this summer's AI Methods final projects. Three of the nineteen are already in use, and they range from social listening on an aircraft maker's safety crisis to an offline tool that helps bomb-disposal teams identify ordnance."),
    ("2026-05-04", "Taught AI Methods for Social and Visual Data for the second time, rebuilt for the summer with one live session a week and hands-on Python videos for every module."),
    ("2026-04-30", "Talked with Tepper for a Faculty Spotlight on what students learn in the MS in Business Analytics, and why I describe business analytics as a decathlon.", "https://www.youtube.com/watch?v=UxBPkez6Mc4"),
    ("2026-03-11", "Started teaching 46-887 Machine Learning for Business Applications to the in-person MS in Business Analytics cohort, redesigned around AWS. Students take a model from S3 through SageMaker to a database they run themselves and a live dashboard."),
    ("2026-02-19", "Made a cameo in a Tepper reel for the end of Mini 3: your professor tells a joke that is not funny, but finals are next week. For the record, the jokes are funny.", "https://www.instagram.com/p/DU86OS8Echk/", "Watch on Instagram"),
    ("2026-01-13", "Started teaching 90-803 Machine Learning Foundations with Python at Heinz College, rebuilt around four applied projects on policy questions, from broadband subsidies to student loan complaints."),
    ("2026-01", "Advising two MS in Business Analytics capstone teams this spring."),
    ("2025-10-22", "Taught 70-377 Managing and Assessing Tech Talent and Organizations for CMU Qatar, my first course in Doha since 2016: mock technical interviews on Zoom, then an in-person week on teams and culture."),
    ("2025-10", "Taught Data Mining in person and online hybrid in the same seven-week term, and added principal component analysis to the course."),
    ("2025-08-26", "Taught the first class of 45-884 AI Methods for Social and Visual Data, a course I built for MBA and master's students on text, images, and AI agents, using foundation models rather than training them."),
    ("2025-05", "Joined gAIm Systems as Senior Director of AI and Data Science."),
    ("2025-05", "Proud of this spring's Data Mining final projects: teams brought their own questions, from predicting baseball Hall of Fame induction to siting EV chargers in Pennsylvania."),
    ("2025-03", "This spring's Data Visualization final projects were 29 recorded data stories, from Netflix's global catalog to city-by-city warming and public-sector dashboards."),
    ("2025-01-10", "Poets & Quants profiled Tepper's MBA Class of 2026, and Tepper's director of masters admissions named me as the new professor teaching business analytics in the MBA program.", "https://poetsandquants.com/2025/01/10/meet-carnegie-mellon-teppers-mba-class-of-2026/2/", "Read the profile"),
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
    <header class="site{' home' if active == 'home' and canon == '' else ''}">
      <a class="wordmark" href="{root}"><img class="mini-portrait" src="{root}assets/portrait-hedcut.png" width="360" height="360" alt=""><span>Ben Collier, PhD</span></a>
      <nav class="primary" aria-label="Primary">
        {item("courses/", "courses", "courses")}
        {item("projects/", "coding with AI projects", "projects")}
        {item("advising/", "advising", "advising")}
        {item("consult/", "consulting", "consult")}
        {item("cv/", "cv", "cv")}
        {item("talks/", "talks", "talks")}
        {item("travel/", "travel", "travel")}
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
      <div><a href="{root}consult/">Consulting</a> · <a href="{root}contact/">Contact</a></div>
    </footer>
  </div>
  <script src="{root}js/config.js"></script>
  <script src="{root}js/site.js"></script>
  <script src="{root}js/course-hero.js" defer></script>
  <script src="{root}js/course-schedule.js" defer></script>
  <script src="{root}js/news-visuals.js" defer></script>
  <script src="{root}js/portrait-dock.js" defer></script>
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
    # 24x24 line icons, stroked in the tile's text color.
    "track": '<path d="M4 19c4-1 5-6 8-7s6 1 8-3"/><circle cx="4" cy="19" r="1.6"/><circle cx="20" cy="9" r="1.6"/><path d="M14 4l6 5-6 0"/>',
    "capstone": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/><path d="M22 9v6"/>',
    "role": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2"/><path d="M3 13h18"/>',
    "summit": '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
}
ICON_COLORS = {"track": "c-navy", "capstone": "c-pine", "role": "c-ink", "summit": "c-clay"}


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
    spec = next((v for k, v in NEWS_VISUALS.items() if k in text), None)
    if spec and spec.get("img"):
        play = '<span class="play" aria-hidden="true"></span>' if spec.get("video") else ""
        inner = f'<img src="{root}{spec["img"]}" alt="{esc(spec["alt"])}" width="480" height="270" loading="lazy">{play}'
        return f'<a class="news-vis photo" href="{esc(href or "#")}" tabindex="-1">{inner}</a>' if href else f'<div class="news-vis photo">{inner}</div>'
    if not spec and slugs:
        slides = course_visual_slides(slugs[0], index * 2)
        if slides:
            c = next(c for c in linkable_courses() if c["slug"] == slugs[0])
            imgs = "".join(
                f'<img src="{root}{thumb_src(s["src"])}" alt="{esc(s["caption"]) if i == 0 else ""}" width="320" height="180" loading="lazy" decoding="async"{" class=on" if i == 0 else ""}>'
                for i, s in enumerate(slides)
            )
            return (f'<a class="news-vis slides" href="{root}courses/{c["slug"]}/" tabindex="-1" aria-label="Slides from {esc(course_name(c))}">'
                    f'{imgs}<span class="tag {c["color"]}">{esc(course_label(c))}</span></a>')
    if spec and spec.get("icon"):
        icon = spec["icon"]
        return (f'<div class="news-vis icon {ICON_COLORS[icon]}" aria-hidden="true">'
                f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{NEWS_ICONS[icon]}</svg>'
                f'<span>{esc(spec["label"])}</span></div>')
    return ""


def news_items(limit=None, root=""):
    items = NEWS if limit is None else NEWS[:limit]
    out = ['<ol class="feed news">']
    for index, (iso, text, *rest) in enumerate(items):
        more = ""
        href = ""
        if rest:
            label = rest[1] if len(rest) > 1 else "Watch the video"
            href = news_link(rest[0], root)
            more = f' <a href="{esc(href)}">{label}</a>'
        slugs = []
        body = link_courses(text, root, slugs)
        visual = news_visual(text, slugs, root, index, href)
        out.append(
            f'<li{" class=has-vis" if visual else ""}><time datetime="{iso}">{human_date(iso)}</time>'
            f'<div class="post"><p>{body}{more}</p></div>{visual}</li>'
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
        <div class="portrait-morph">
          <img class="portrait" src="assets/portrait.jpg" width="500" height="500" alt="Portrait of Ben Collier" fetchpriority="high">
          <img class="portrait hedcut" src="assets/portrait-hedcut.png" width="360" height="360" alt="">
        </div>
        <div>
          <p class="kicker">Assistant Teaching Professor of Business Analytics</p>
          <h1>Ben Collier</h1>
          <p class="lede">I teach AI and business analytics at Carnegie Mellon's Tepper School, and help companies put them to work.</p>
        </div>
      </section>

      <div class="bio">
        <p>Most of my teaching is at <a href="https://www.cmu.edu/tepper/">Tepper</a>, in the <a href="https://www.cmu.edu/tepper/programs/mba/">MBA</a>, the <a href="https://www.cmu.edu/tepper/programs/master-business-analytics/">MS in Business Analytics</a>, and the <a href="https://www.cmu.edu/tepper/programs/undergraduate-programs/">undergraduate program</a>. I also teach at <a href="https://www.heinz.cmu.edu/">Heinz College</a>. The courses are hands-on. Students write Python, reason about uncertainty, and decide what a model should and should not be used for once it leaves the notebook.</p>
        <p>Before joining Tepper I was a staff data scientist at <a href="https://www.duolingo.com/">Duolingo</a> and Senior Director of Data Science at <a href="https://www.upmc.com/">UPMC</a>'s Pensiamo, where I was the founding data scientist on a joint venture with <a href="https://en.wikipedia.org/wiki/IBM_Watson_Health">IBM Watson Health</a>. I still do that work, as Senior Director of AI and Data Science at <a href="https://www.gaimsystems.com/">gAIm Systems</a> and through my consulting practice, Hot Metal AI. The problems I bring into class come from that work. I also advise MS in Business Analytics capstone teams. Since September 2026 I have been the faculty coordinator of Tepper's <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>, and starting in Spring 2027 I also advise its capstone teams.</p>
      </div>

      <div class="book-row">
        {book_call("")}
        <a class="btn" href="consult/">Consulting and custom education</a>
      </div>

      <ul class="stats linked">
        <li><a href="courses/#built"><strong>{sum(1 for c in COURSES if c["built"])}</strong><span>courses I designed from scratch</span></a></li>
        <li><a href="courses/"><strong>{len(COURSES)}</strong><span>courses taught at Carnegie Mellon since 2023</span></a></li>
        <li><a href="advising/"><strong>{len(load_json("advising.json")["projects"])}</strong><span>capstones and independent studies advised since 2024</span></a></li>
        <li><a href="cv/#honors-and-awards"><strong>2026</strong><span>George Leland Bach Teaching Award, voted by the MBA class</span></a></li>
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


def education_sections(root: str) -> str:
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
            f'<li><strong>{esc(n)}</strong><span>{esc(label)}</span></li>' for n, label in stats.get("stats", [])
        )
        cards = "\n".join(course_card(c, root) for c in execs)
        out += f"""
      <section class="edu-band" id="executive">
        <p class="kicker">For organizations</p>
        <h2>Executive and custom education</h2>
        <p class="prose-width">{stats.get("intro", "Programs I have designed and taught for executives and company teams.")}</p>
        {f'<ul class="stats">{tiles}</ul>' if tiles else ""}
        <div class="grid">{cards}</div>
        <p class="edu-cta"><a class="btn primary" href="{root}consult/#education">Plan a program for your team</a></p>
      </section>
"""
    if cmuq:
        cards = "\n".join(course_card(c, root) for c in cmuq)
        out += f"""
      <section class="era" id="cmu-qatar">
        <p class="kicker">Earlier teaching</p>
        <h2>Organizational behavior at CMU Qatar, 2012 to 2016</h2>
        <p class="prose-width">My first appointment at Carnegie Mellon was as Assistant Teaching Professor of Organizational Behavior at the Qatar campus, where I also co-directed executive and continuing education. These are the undergraduate courses I taught there, each with its full schedule and slides.</p>
        <div class="grid">{cards}</div>
      </section>
"""
    return out


def build_courses_index():
    built = "\n".join(course_card(c, "../") for c in COURSES if c["built"])
    taught = "\n".join(course_card(c, "../") for c in COURSES if not c["built"])
    body = f"""
      <p class="kicker">Teaching</p>
      <h1>Courses</h1>
      <p class="lede">Courses I designed from scratch, then courses I took over and rebuilt.</p>

      <h2 id="built">Courses I built</h2>
      <div class="grid">{built}</div>

      <h2>Courses I took over and rebuilt</h2>
      <div class="grid">{taught}</div>
{education_sections("../")}
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
    return f'<p class="scale-note">{esc(c["scale"])}</p>\n        ' if c.get("scale") else ""


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


def schedule_section(s, root: str) -> str:
    """The week-by-week table, with a slide stage that js/course-schedule.js
    plays for whichever session is in view. Every row with slides also carries
    its own thumbnail strip, so the page reads fine without JavaScript."""
    unit = s.get("unit_label", "Week")
    rows = []
    for r in s["schedule"]:
        if "part" in r:
            rows.append(f'<li class="sched-part">{esc(r["part"])}</li>')
            continue
        kind = r.get("kind", "lecture")
        tag = KIND_TAGS.get(kind)
        tag_html = f' <span class="sched-tag {kind}">{tag}</span>' if tag else ""
        note = f'<span class="sched-note">{esc(r["note"])}</span>' if r.get("note") else ""
        when = esc(r.get("label") or short_date(r["date"]))
        week = f'{unit} {r["week"]}' if r.get("week") else ""
        strip = ""
        if r.get("slides"):
            imgs = "".join(
                f'<img src="{root}{thumb_src(sl["src"])}" data-full="{root}{sl["src"]}" data-caption="{esc(sl["caption"])}" '
                f'alt="{esc(sl["caption"])}" width="320" height="180" loading="lazy" decoding="async">'
                for sl in r["slides"]
            )
            strip = f'<div class="sched-strip">{imgs}</div>'
        cls = f"sched-row {kind}" + (" has-slides" if r.get("slides") else "")
        tab = ' tabindex="0"' if r.get("slides") else ""
        rows.append(
            f'<li class="{cls}" data-date="{r["date"]}"{tab}>'
            f'<div class="sched-when"><time datetime="{r["date"]}">{when}</time><span>{week}</span></div>'
            f'<div class="sched-what"><span class="sched-topic">{esc(r["topic"])}</span>{tag_html}{note}{strip}</div>'
            f"</li>"
        )
    first = next((r for r in s["schedule"] if r.get("slides")), None)
    stage = ""
    if first:
        sl = first["slides"][0]
        stage = f"""<figure class="stage" aria-label="Slides from the session in view">
          <div class="stage-frame">
            <img class="stage-img is-on" src="{root}{sl['src']}" alt="{esc(sl['caption'])}" width="1280" height="720">
            <img class="stage-img" alt="" width="1280" height="720" aria-hidden="true">
          </div>
          <figcaption>
            <span class="stage-when">{esc(short_date(first['date']))}</span>
            <strong class="stage-topic">{esc(first['topic'])}</strong>
            <span class="stage-caption" aria-live="polite">{esc(sl['caption'])}</span>
            <span class="stage-pips" role="group" aria-label="Choose a slide"></span>
          </figcaption>
        </figure>"""
    return f"""
      <section class="schedule" data-schedule>
        <h2>Week by week</h2>
        <p class="muted">{esc(s['term'])} · {esc(s['meets'])}. Scroll the schedule and the slides follow along: five from each session, picked from the decks I taught from.</p>
        <div class="sched-grid">
          <ol class="sched-list">{''.join(rows)}</ol>
          {stage}
        </div>
      </section>
"""


def assignments_section(s) -> str:
    if not s or not s.get("assignments"):
        return ""
    items = "".join(
        f'<li><div class="asg-head"><strong>{esc(a["name"])}</strong>'
        + (f'<span class="asg-weight">{esc(a["weight"])}</span>' if a.get("weight") else "")
        + f'</div><p>{esc(a["description"])}</p></li>'
        for a in s["assignments"]
    )
    return f'        <h2>Major assignments</h2>\n        <ul class="assignments">{items}</ul>\n'


def project_list(s) -> str:
    """Every final project, grouped by term. No student names: subject, approach, one line."""
    groups = (s or {}).get("projects") or []
    if not groups:
        return ""
    out = []
    for i, g in enumerate(groups):
        items = "".join(
            f'<li><strong>{esc(p["subject"])}</strong>'
            + (f'. {esc(p["description"])}' if p.get("description") else "")
            + (f' <span class="proj-approach">{esc(p["approach"])}</span>' if p.get("approach") else "")
            + "</li>"
            for p in g["items"]
        )
        open_attr = " open" if i == 0 else ""
        out.append(
            f'<details class="proj-term"{open_attr}><summary>{esc(g["term"])} '
            f'<span class="count">{len(g["items"])} projects</span></summary><ul>{items}</ul></details>'
        )
    return '        <p class="muted">Every project, by term.</p>\n        ' + "\n        ".join(out) + "\n"


def build_course_pages():
    for c in ALL_COURSES:
        sched = load_schedule(c["slug"])

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
            projects = f"        <h2>Final projects</h2>\n        <p>{pj['intro']}</p>\n{lst}{project_list(sched)}"
        if not pj and project_list(sched):
            projects = f"        <h2>Student work</h2>\n{project_list(sched)}"
        topics = ""
        if c.get("topics") and not sched:
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
        # With a schedule, the hero article closes so the week-by-week section
        # can use the full page width, then the prose column picks up again.
        split = ""
        if sched:
            split = f"""      </article>
{schedule_section(sched, "../../")}
      <article class="course-more prose-width">
"""
        body = f"""
      <article class="course-hero prose-width">
        <p class="kicker">{course_kicker(c)}</p>
        <h1>{course_name(c)}</h1>
        <p>{built}</p>
        <div class="thumb hero {c['color']}"><canvas data-hero="{c['hero']}" role="img" aria-label="{esc(HERO_ALT[c['hero']])}"></canvas><span>{course_label(c)}</span></div>
        <p class="lede">{c['one_liner']}</p>
        {scale_note(c)}<p>{c['blurb']}</p>
        {c.get('panel', '')}
{split}{topics}{assignments_section(sched)}{story}{projects}{history}        <h2>Offerings</h2>
        <ul class="chips">{offerings}</ul>
        {f'<p class="muted">{c["materials"]}</p>' if c.get("materials") else ""}
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
        name = course_name(c)
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
      <header class="cv-head">
        <img class="cv-portrait" src="../assets/portrait.jpg" width="500" height="500" alt="Portrait of Ben Collier">
        <div>
          <p class="kicker">Curriculum vitae</p>
          <h1>Ben Collier, PhD</h1>
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
      {_cv_glance()}
      <div class="cv-layout">
        <nav class="cv-toc" aria-label="CV sections"><ol>{toc}</ol></nav>
        <article class="cv">
          {"".join(html for _, html in rendered)}
        </article>
      </div>
      <script src="../js/cv.js" defer></script>
      <script src="../js/place-pop.js" defer></script>
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
      <p class="lede lede-wide">Working projects I built with AI coding tools, several of them for 15-113 Effective Coding with AI. Each repo includes the prompts and build log, and I use them as examples in class.</p>
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
        f"<li><span>{esc(e['term'])}</span><div>{esc(e['title'])}. <em>{esc(e['place'])}</em></div></li>" for e in data["earlier"]
    )
    n = len(data["projects"])
    body = f"""
      <p class="kicker">Advising</p>
      <h1>Capstones and independent studies</h1>
      <p class="lede">Since 2024 I have advised MS in Business Analytics capstone teams working with companies and nonprofits, and students doing independent studies. {n} projects so far, described here without the students' names and without the partners' data. Starting in Spring 2027 I also advise capstone teams in the <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>.</p>
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
      <p class="lede">I help organizations choose which AI and analytics projects to fund, check the models before they carry a real decision, and train their teams to run the work themselves. I do this through my practice, Hot Metal AI.</p>

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
            <li>Three-day executive programs at Carnegie Mellon University in Qatar on <a href="../courses/exec-negotiation/">negotiation</a>, <a href="../courses/exec-decision-making/">decision making</a>, <a href="../courses/exec-teams/">managing teams</a>, and <a href="../courses/exec-leadership/">leadership</a>, with up to 114 managers in the room from ministries, energy, banking, telecom, aviation, and media.</li>
            <li><a href="../courses/exec-custom/">Workshops built for one organization</a>: RasGas, a Carnegie Mellon senior staff retreat in Munich, and Qatar's Civil Service Bureau.</li>
            <li>Professional development courses for technology leaders and executives at Optum, AT&amp;T, Cox Communications, and RapidScale.</li>
            <li>At Carnegie Mellon in Qatar I co-directed executive and professional education. In 2014 to 2015 the program taught 755 participants from more than 30 government and private-sector organizations across Qatar. <a href="https://www.qatar.cmu.edu/news/more-than-700-participants-complete-cmu-qs-executive-and-professional-education-program/">CMU-Q news</a></li>
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
          <h3>Through Hot Metal AI</h3>
          <ul>
            <li>A recommendation engine for healthcare specialist referrals, built for a healthcare client.</li>
          </ul>
          <h3>In industry roles</h3>
          <ul>
            <li>At <a href="https://www.upmc.com/">UPMC</a>'s Pensiamo, as founding data scientist on a joint venture with <a href="https://en.wikipedia.org/wiki/IBM_Watson_Health">IBM Watson Health</a>, I did the machine learning research and built the production pipelines for CognitiveRx, a drug price and shortage tool for a 40-hospital system buying $1.5 billion of pharmaceuticals a year. <a href="https://premierinc.com/">Premier</a> later acquired it.</li>
            <li>At <a href="https://www.duolingo.com/">Duolingo</a>, experimentation, monetization analytics, and forecasting through the IPO and the launch of Duolingo Max.</li>
            <li>At <a href="https://www.gaimsystems.com/">gAIm Systems</a>, AI tools and research studies that help sports teams recruit players, develop them, and build rosters.</li>
          </ul>
        </section>
      </div>

      <p class="prose-width">I also advise MS in Business Analytics capstone teams working with companies such as Westinghouse, RBC Wealth Management, and Swank Construction, and starting in Spring 2027, capstone teams in the <a href="https://www.cmu.edu/tepper/programs/mba/curriculum/tracks/business-analytics">MBA Business Analytics track</a>. <a href="../advising/">See those projects</a>.</p>

      <div class="book-row">
        <a class="btn primary" href="../book/">Book time</a>
        <span class="muted">Most engagements start with a free 15-minute call.</span>
      </div>

      <h2 id="background">Background</h2>
      <ol class="timeline">
        <li><span>2025 to now</span><strong>gAIm Systems</strong> Senior Director of AI and Data Science</li>
        <li><span>2023 to now</span><strong>Tepper School of Business, Carnegie Mellon</strong> Assistant Teaching Professor of Business Analytics, after starting as an adjunct in Fall 2023</li>
        <li><span>2020 to 2023</span><strong>Duolingo</strong> Staff Data Scientist, on monetization</li>
        <li><span>2018 to now</span><strong>Hot Metal AI</strong> Founder. Analytics consulting and corporate training, alongside everything else</li>
        <li><span>2016 to 2020</span><strong>UPMC's Pensiamo</strong> Senior Director of Data Science</li>
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
      {news_items(root="../")}
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


# Slides from the August 2026 AI-Exchange talk, rendered from Ben's own deck.
# Only his text slides: no student names or work, no third-party figures.
TALK_SLIDES = {
    "ai-exchange-2026": [
        ("45884-vit", "From 45-884: MBA students learn how Vision Transformers apply attention to image patches."),
        ("45884-embedding", "From 45-884: a joint embedding space where images and text sit side by side."),
        ("45884-waymo", "From 45-884: the Tesla Vision versus Waymo case, cameras against lidar and radar."),
        ("blooms", "How 45-884 maps to Bloom's taxonomy: quizzes for remembering, labs for applying, the final project and AI in the News for creating."),
        ("70445-muffin", "From 70-445: muffin or chihuahua? You can spot it. Now write the rule."),
        ("70445-harness", "From 70-445: agent = model + harness, the idea behind the course's agent unit."),
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


def talk_slide(talk: str, name: str, cap: str) -> str:
    src = f"../assets/talks/{talk}-{name}.jpg"
    return (
        f'          <figure>\n'
        f'            <a href="{src}"><img src="{src}" width="1200" height="675" loading="lazy" alt="Slide: {esc(cap)}"></a>\n'
        f'            <figcaption>{cap}</figcaption>\n'
        f'          </figure>'
    )


def talk_slides(talk: str) -> str:
    return "\n".join(talk_slide(talk, n, c) for n, c in TALK_SLIDES[talk])


def build_talks():
    slides = talk_slides("ai-exchange-2026")
    body = f"""
      <p class="kicker">Talks</p>
      <h1>Talks</h1>
      <p class="lede">Talks and workshops on building AI courses, teaching with AI, and putting analytics to work.</p>

      <article class="talk">
        <p class="meta">August 7, 2026 · Tepper AI-Exchange · Carnegie Mellon University, Pittsburgh</p>
        <h2>Lessons Learned from Developing New AI Courses for MBA and Undergraduate Business Students</h2>
        <div class="prose-width">
          <p>Over the past year I designed and taught a new MBA elective, <a href="../courses/45-884/">AI Methods for Social and Visual Data</a>, and I was developing an undergraduate course, <a href="../courses/70-445/">Artificial Intelligence for Business Leaders</a>, launching that fall. In this talk I shared what has worked well in the MBA classroom, from assignment design to helping students build hands-on skills with modern AI tools, along with what I was changing or trying differently in the new undergraduate course. I also gave a brief introduction to a large randomized controlled trial of AI in the classroom that I am taking part in, and what we hope to learn from it about how AI actually affects student outcomes.</p>
          <p>The session closed as a discussion with the faculty in the room: what they would add to the undergraduate course, what did not fit, and how Tepper should approach a flagship AI course for undergraduates.</p>
        </div>
        <h3>Selected slides</h3>
        <div class="slides">
{slides}
        </div>
      </article>

      <article class="talk">
        <p class="meta">June 5, 2025 · Teaching with AI Summer Workshop · Kellogg School of Management, Northwestern University</p>
        <h2>AI Data Visualization Coach</h2>
        <div class="prose-width">
          <p>A flash talk with my colleague Zoey Jiang on the custom GPT we built for <a href="../courses/45-885/">Data Visualization</a>. Before presenting a chart redesign, teams test it with the coach. It will not hand over a redesign. It questions the team from three seats: a journalist, a chart designer, and a business stakeholder.</p>
          <p><a href="https://www.kellogg.northwestern.edu/events/conference/teaching-with-ai/">Workshop program</a></p>
        </div>
        <h3>Selected slides</h3>
        <div class="slides">
{talk_slides("kellogg-2025")}
        </div>
      </article>

      <article class="talk">
        <p class="meta">April 30, 2026 · Tepper School of Business</p>
        <h2>Faculty Spotlight: what students learn in the MS in Business Analytics</h2>
        <div class="prose-width">
          <p>A conversation for Tepper about the MS in Business Analytics curriculum, and why I describe business analytics as a decathlon.</p>
          <a class="video-thumb" href="https://www.youtube.com/watch?v=UxBPkez6Mc4">
            <img src="../assets/talks/faculty-spotlight-2026.jpg" width="1280" height="720" loading="lazy" alt="Ben Collier explaining a point during the Tepper Faculty Spotlight conversation">
            <span class="play" aria-hidden="true"></span>
            <span class="duration">11 min</span>
          </a>
          <p><a href="https://www.youtube.com/watch?v=UxBPkez6Mc4">Watch on YouTube</a></p>
        </div>
      </article>

      <h2>Earlier talks</h2>
      <ul class="earlier-list">
        <li><span>Sep 2026</span><div>Business Analytics track information session. <em>Tepper MBA program</em></div></li>
        <li><span>2025, 2026</span><div>Perspectives on Analytics. <em>BaseCamp orientation for incoming part-time MS in Business Analytics students, Tepper School of Business</em></div></li>
        <li><span>Nov 2025</span><div>Managing groups and teams: strategies for collaborative excellence. <em>Community partner workshop, Carnegie Mellon University in Qatar</em></div></li>
        <li><span>Mar 2025</span><div>Traditional AI: data mining and data visualization, and AI tools for research. <em>Colloquium on AI for Business, Tepper School of Business</em></div></li>
        <li><span>2024, 2025</span><div>Using statistics to solve business problems, and to estimate the unknown. <em>Business Analytics Summer Summit, Tepper School of Business</em></div></li>
        <li><span>2015</span><div>Creating a culture for innovation in teams. <em>RasGas Company, Doha</em></div></li>
        <li><span>2014</span><div>Digital marketing for entrepreneurs. <em>International Telecommunication Union World Conference</em></div></li>
        <li><span>2014</span><div>Leadership in groups and organizations. <em>Cultivate Leadership Workshop, Hamad Bin Khalifa University</em></div></li>
      </ul>

      <div class="book-row">
        <a class="btn primary" href="../book/">Ask about a talk or workshop</a>
        <span class="muted">I speak to faculty, executive, and industry audiences about AI in business and in the classroom.</span>
      </div>
"""
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
    body = f"""
      <h1>Contact</h1>
      <p class="lede">Email is the most reliable way to reach me. Students, please put the course number in the subject line.</p>
      <ul class="contact-list">
        <li><span>CMU email</span><div><a href="mailto:bcollier@cmu.edu">bcollier@cmu.edu</a></div></li>
        <li><span>Personal</span><div><a href="mailto:ben@collier.phd">ben@collier.phd</a></div></li>
{'        <li><span>Site</span><div><a href="../">' + DOMAIN_LABEL + '</a></div></li>' + chr(10) if SITE.get("domain_live") else ""}        <li><span>Office</span><div>Office 5135, Tepper Quad<br>Tepper School of Business, Carnegie Mellon University<br>4765 Forbes Avenue<br>Pittsburgh, PA 15213</div></li>
        <li><span>Consulting</span><div>{book_call("../", "")} · <a href="../consult/">Consulting and custom education</a></div></li>
        <li><span>Students</span><div><a data-book="studentHours" data-live-label="Book a 30-minute appointment" href="mailto:bcollier@cmu.edu">Email me</a> two times that work for office hours and I will confirm one.</div></li>
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


def build_travel():
    data = load_json("travel.json")
    places = data["countries"]
    chips = "".join(
        f'<li><button type="button" data-cc="{p["cc"]}">{esc(p["name"])}</button></li>' for p in sorted(places, key=lambda p: p["name"])
    )
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    body = f"""
      <p class="kicker">Travel</p>
      <h1>Places I have been</h1>
      <p class="lede lede-wide">{len(places)} countries so far, mapped from my own photo library. Hover a dot or a highlighted country to see what I saw there, or pick one from the list.</p>
      <div class="view-tabs" role="tablist" aria-label="Map or globe">
        <button type="button" role="tab" aria-selected="true" data-view="map">Map</button>
        <button type="button" role="tab" aria-selected="false" data-view="globe">Globe</button>
      </div>
      <div id="view-map" class="worldmap-wrap">
        <div id="worldmap" class="worldmap"></div>
        <div id="map-pop" class="map-pop" hidden></div>
      </div>
      <div id="view-globe" class="travel" hidden>
        <div id="globe" class="globe"></div>
        <aside id="globe-card" class="globe-card" aria-live="polite" hidden></aside>
      </div>
      <dialog id="photo-view" class="photo-view"><img alt=""><p></p><button type="button" aria-label="Close">×</button></dialog>
      <ul class="country-list">{chips}</ul>
      <script type="application/json" id="travel-data">{blob}</script>
      <script src="../assets/vendor/d3.min.js" defer></script>
      <script src="../assets/vendor/topojson-client.min.js" defer></script>
      <script src="../js/travel.js" defer></script>
      <script src="../js/travel-map.js" defer></script>
"""
    write(
        "travel/index.html",
        page("../", "travel", "Travel · Ben Collier", f"{len(places)} countries, mapped from my photos.", "travel/", body),
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
    paths = ["", "consult/", "book/", "advising/", "courses/", "projects/", "talks/", "cv/", "news/", "contact/", "travel/"]
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
    build_404()
    build_sitemap()
    build_robots()
    build_feed()
    print(f"done: absolute URLs point at {HOST}")


if __name__ == "__main__":
    main()
