## What it teaches
- Test retrieval with questions that share no words with the answer, so you measure meaning and not word overlap.
- Store each kind of evidence (narration, image description, slide text, keywords) as its own embedded item instead of one long blob of text.
- Score every ranking idea against labeled questions before keeping it, and drop the ones that lose, even when they felt right.
- Make each search result explain why it ranked, so you can debug the ranking by looking at it.
- Push back when an AI agent invents a constraint or keeps adding scope, and switch models when its advice keeps going wrong.

## What it is
Slide Finder is a technical project on one question: how do you match a question to a slide? I type a question the way a student would ask it, and it finds the slides where I taught that idea, from every slide I have taught since Fall 2023 across five courses.

![The landing page's fig. 1: the question "how does a computer read a photo" is compared with four texts attached to one slide, and the slide whose closest text wins comes back first](how-it-matches.webp "one question, four texts")

Every slide is stored as several searchable items, each with its own embedding: what I said in class while it was on screen, an AI's description of its picture, the slide's own text and speaker notes, and the keywords stemmed from all of that. A question is embedded once and compared with all of them. Meaning matches and keyword matches are fused into one ranking, and each slide is ranked by its best item.

The same slide comes back year after year, often in a new deck template. Repeats are recognised by the pictures embedded in them, not by how the page looks. 5,623 deck pages became 2,801 unique slides, and each one lists every session that used it.

It is my own tool, not a student-facing one. I use it when I build a new deck and want the slide where I already explained something, whatever course or term it was in.

![Results for "how does a computer read a photo": Images are Numbers first, then the attention visualization and the lion slide, each taped to the page with a red-pen rank](results-photo-question.webp "how does a computer read a photo")

## A tour
Open a slide and you see the full image, the exact text that was embedded for it, and on the right why it was chosen. For "how does a computer read a photo", the winner was a chunk of my narration: "Ultimately, images are numbers." None of the question's words are on the slide.

![The slide view for Images are Numbers: the slide, what is indexed for it, and why it was chosen](slide-images-are-numbers.webp "why this one won")

The "why" panel has a sentence that names the item that ranked the slide, a bar that splits the score into meaning and keywords, a distance gauge with a red line at 0.55 where matches stop being trusted, and a ledger with one row per matched item. The landing page explains the four kinds of item.

![Why this slide was chosen: the score split, the distance gauge from 0.3 to 0.7, the best sentence, and one bar per matched item](why-this-slide.webp "the evidence ledger")
![Four index cards for the four ways a slide can match: narration, image description, slide text and notes, keywords](four-ways.webp "four ways to match")

Three searches show the edges. A question about overfitting in plain words finds the bias and variance slide through my narration. A question I never taught gets a warning. A short exact term like `mtry` is found by keywords, even though nothing is close by meaning.

![The bias and variance slide opened for "it fits the data it has seen perfectly and falls apart on anything new", matched through my narration at distance 0.50](slide-bias-variance.webp "no shared words")
![The "not sure I taught this" warning for "how do I bake sourdough bread", over weak matches](weak-match-sourdough.webp "never taught this")
![Results for "mtry": the random forest slide first, found by keyword, under the weak-match warning](keyword-mtry.webp "keywords still help")

## How I built it
I built it in Claude Code on October 26, in about six hours. I described the project in my own words first and only gave the agent the assignment page after the spec was drafted. Then it built one step at a time: spec, install and a five-line check, a smoke test that found the slides again in a second process, my real data, a look at the distances, runtime adds, deploy, evaluate. I tested each deployed version in my browser and sent back screenshots when something was wrong.

The stack: Supabase Postgres with pgvector, Voyage AI embeddings, FastAPI and a static page on Vercel. Claude Haiku wrote the image descriptions and read titles off slides whose heading was inside a picture. That runs offline, never in the web app.

About two hours in I switched models. The agent kept recommending Chroma and then wanted to keep it as a second backend "for graders", a constraint nobody gave it. I already pay for Supabase. I told it the recommendations were bad, switched from Claude Opus 5.5 to Claude Fable 5.1, and asked why. Its answer: it had invented a grading rule, kept Chroma out of sunk cost, and kept adding scope instead of cutting it. The design became one backend.

Other things that went wrong, all in the prompt log:
- Appending the image description to each slide's card made results worse. Long cards dilute the slide's own words. Descriptions became their own item.
- pgvector's HNSW index returns at most 40 candidates, so "show 100" gave 24 slides. The vector side became an exact scan, which takes a few milliseconds at under 10,000 items.
- The first duplicate grouping merged different slides that shared a template, then split one slide into a copy per term. Hashing the embedded pictures fixed both.
- The vision pass returned a sentence of prose instead of a title for 32 slides, and the cleanup then shortened 38 real titles that had to be restored.

To check it, I wrote 28 questions the way a student would ask them, each labeled with the slide that answers it. The hybrid search puts a right slide first for 19 of 28 (hit@1 0.68). Keywords alone get 1 of 28. A 15% bonus I added by intuition, for slides matched two ways, dropped hit@1 to 0.57, so it came out. Measuring it was the point. All six off-topic questions got the warning.

Some questions still miss. "It aced the practice problems but bombed the real test" means overfitting, but the embedding reads it as being about exams. Metaphors two steps away from the concept don't land.

The project started because retrieval in my earlier project, [Faculty Twin](https://github.com/bcollier/faculty-twin), missed too often, and I wanted to work out how to get it right and prove it with numbers.
