# Prompt log

Required by 15-113 Project 1: "a text document that contains the prompts you
used (simply copy-pasted) and the replies you received."

**Tool used:** Claude Code (Anthropic's CLI), running Claude Opus 5. One
continuous session on 5 September 2026. I worked in the terminal rather than a
browser chat, which matters for reading this log: the model could read and edit
files in the repository directly, so its "replies" are often a description of
edits it made rather than a block of code for me to paste.

**How to read this.** My prompts are quoted verbatim. The replies were long
(the model narrates as it works), so I have summarised what each one actually
produced and, more usefully, recorded **what I rejected or changed**. The
rejections are the honest part. Anyone can get a model to emit a page; the
work is knowing which parts to throw away.

---

## Session 1 — review the existing site

### Prompt 1

> review the code here, and walk me through the rest of setting up an incredible website for me

**Reply, summarised.** It read every file in the repository, ran the build
script, checked the live GitHub Pages deployment, resolved the DNS for my
domain, and computed WCAG contrast ratios for every colour pair in the
stylesheet. Then it reported findings and opened a pull request.

The findings I would not have caught on my own:

1. **The site was publishing its own editing instructions.** The CV page's
   lede, in large serif type, read "Paste updates into `data/cv.md`, then run
   `python3 scripts/build.py`." Four other pages did the same thing. I had
   written those strings as notes to myself inside the build script and never
   registered that they were being rendered to visitors.
2. **Three "capstone" entries were placeholders** whose published summaries
   read "Paste the project summary here once the team opts in."
3. **Every canonical tag pointed at `https://ben.collier.phd`**, which has no
   DNS record. A canonical tag aimed at a domain that does not resolve tells
   Google the real page is a dead link.
4. **`collier.phd` was serving a default nginx page** over plain HTTP, and
   failing entirely over HTTPS. I did not know this. It also found the SPF
   record showing that domain carries my Google Workspace email, and warned me
   not to touch the MX and TXT records when I repoint the A record.
5. Link hover *lowered* contrast to 4.16:1, under the 4.5:1 floor.

**What I changed in its work.** It initially wanted to delete
`assets/portrait.webp` because the file is unreferenced and larger than the
JPEG. I told it to leave my assets alone and just flag the file. It also left
`https://ben.collier.phd` in the CV body text rather than rewriting my CV,
which was the right call and it said so explicitly.

### Prompt 2

> merge the PR, I will take a look, but the existing site looks quite boring and vanilla. I want to build a site that catches someones attention and looks personal. this website is fulfilling two things, first I need a site as my main page for people finding me and especially booking any consulting work. I would like to have a way for people to have a paid consultation with me through Hot Metal.AI through the site. I want to show off student projects and my work etc. but this site is also for a class,
>
> https://www.cs.cmu.edu/~113/project1.html
>
> take inspiration from some of these student portfolios https://www.cs.cmu.edu/~113/students.html
>
> I want 5 different designs, all of them with a completely different design idea. make at least one very AI heavy, maybe looking like a neural network or robot or something. maybe just a small touch of having a cute robot follow your mouse around the screen every once in a while.
>
> give me the link to see the site when it's ready, give me a way to see the 5 different versions

**Reply, summarised.** It merged the pull request, fetched and parsed the
assignment page, and then flagged something I had lost track of: the project
was due **that same day at 8:00 PM**, roughly six hours out. It also checked
`hotmetal.ai` and found it returning a Wix domain-connection error, which is
why the consulting section lives on this site rather than linking out.

It then built five complete designs plus a picker page.

---

## What I directed, and what I rejected

This is the part that matters for the interview, so it is specific.

### The five designs were my brief, not the model's

I asked for five *different design arguments*, not five colour schemes. The
first thing the model proposed was five variations on the same single-page
scroll layout with different palettes. I rejected that. The five that shipped
have genuinely different **structures**:

| Design | The structural idea |
| --- | --- |
| Neural | Full-bleed canvas simulation behind everything; content floats over it |
| Broadsheet | Real CSS multi-column newsprint, drop cap, classified-ad pricing |
| Steel | Full-width horizontal bands with riveted dividers |
| Notebook | Jupyter cells with execution counters and dataframe outputs |
| Studio | Strict Swiss grid, fixed numbered rail, enormous display type |

### Neural: the network background

The first version compared every node against every other node each frame.
At 230 nodes that is about 26,000 distance checks per frame and it dropped
frames on a laptop. I asked for spatial hashing: file each node into a grid
bucket the size of the link radius, then only search the nine surrounding
buckets. That is `buildGrid()` in `designs/neural/index.html`, and it is the
one thing on the page I would call a real optimisation.

I also rejected the palette. Its first pass was cyan-on-black, which is the
default "AI website" look and appears in roughly every template. I replaced it
with the warm rust already used across the rest of my site.

### The robot was my idea and I had to argue for the timing

The model built a cursor-following robot that was on screen permanently. That
is a novelty toy and it gets annoying in about fifteen seconds. My note was
"occasional, not a permanent cursor pet." It now arrives, trails the cursor
with easing so it reads as catching up rather than being glued on, says one
short line, and leaves for 25 to 55 seconds. It is also disabled entirely
under `prefers-reduced-motion` and on touch pointers.

### Notebook: I cut a fake Python interpreter

The model offered to build something that looked like it was executing the
Python in the cells. I cut it. The entire argument of my teaching is that you
should be able to say what a model did and where it fails; a page that
pretends to run code it is not running fails that on its own terms. The
notebook design now says so in its footer, in plain words.

What I kept is the execution counter. `In [n]` in Jupyter reflects the order
you *ran* cells, not their position in the file, so a visitor who runs cell 7
first sees `In [1]` there. The model had numbered them statically, which
misses the whole joke.

### Broadsheet: fake columns

Its first draft faked newspaper columns with a CSS grid, which breaks reading
order — you finish a box and have to jump back up. I asked for real
`column-count` so text flows the way newsprint does.

### Steel: eighty divs of decoration

The rivets along each band divider were originally eighty individual `<div>`
elements. I replaced them with one repeating radial-gradient background: one
paint instead of eighty DOM nodes. I also cut a suggested hero video. Loading
several megabytes to communicate "industrial" is a bad trade on a page whose
argument is that I understand cost.

### Studio: restraint has to be real

The first draft was dense, because that is what most training data looks
like. I roughly doubled every vertical rhythm value and cut about a third of
the words. I also cut a fade-in on every element down to a single clip-path
reveal on the portrait, so one thing moves instead of forty.

### Contrast, everywhere

I asked it to measure rather than guess. It computed WCAG ratios and several
colours failed:

| Element | Before | After |
| --- | --- | --- |
| Link hover (main site) | 4.16:1 | 6.82:1 |
| `.c-rust` course tile label | 4.51:1 | 5.78:1 |
| Steel's molten orange on steel | 3.1:1 | 6.2:1 |

It also found a dark-mode bug I would never have seen: the course-tile label
text read from a `--white` token that inverts in dark mode, so the labels went
dark-on-colour while the tiles stayed light. It now has its own token.

### The consulting pricing

The model wanted a "Contact for pricing" button. I told it to publish the
numbers, because making somebody ask for a price is a tax on their time and it
filters out exactly the direct people I want to work with. All five designs
read the same rate card from one shared file, `designs/shared/booking.js`.

I also insisted the page never imply it can take a card when it cannot. Until
a Stripe payment link is pasted in, every button says "Request this" and opens
a prefilled email, and each design prints a line saying card payment is not
connected yet.

---

## What I would tell a TA about using AI here

The model is very fast at producing a plausible page and genuinely bad at
knowing when to stop. Almost every edit I made was a **subtraction**: the fake
interpreter, the permanent robot, the eighty rivet divs, the fade-in on
everything, a third of the words in Studio. Left alone it adds.

Where it was better than me: measuring things. It computed every contrast
ratio, checked every internal link across twenty pages, parsed the sitemap and
feed as XML, and caught that my canonical tags pointed at a dead domain and
that my apex domain was serving a stock nginx page. I had been looking at that
site for a week and had not noticed any of it.

The division that worked: **it measures and drafts, I decide and cut.**

---

## Files where the AI usage is documented in code

Each design carries an `AI USAGE NOTE` comment block at the top of its
stylesheet listing what was drafted, what I changed, and why:

- `designs/neural/index.html`
- `designs/broadsheet/index.html`
- `designs/steel/index.html`
- `designs/notebook/index.html`
- `designs/studio/index.html`
- `designs/index.html` (the picker)
- `scripts/build.py` and `css/site.css` for the multi-page version

## Credits

Every design footer names its typefaces and their designers, all under the SIL
Open Font License via Google Fonts, and credits the portrait photograph to
Carnegie Mellon University. All project thumbnails are original SVG drawings
made for this site. No templates and no stock photography were used.
