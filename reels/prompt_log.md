# Prompt log: Reels, Me Over the Years

CMU 15-113, Project 2. Prompts are verbatim, typos included. Notes under each prompt say what happened.

## Tools, and which job each did

- **Claude Code with Claude Opus 5.5 (terminal agent):** all of the coding, running the scripts on my Mac, and the git workflow (branch, PR, squash-merge). I used an agent rather than a chat window because the work needed my local Photos library, Apple Vision and a headless browser for screenshots.
- **OpenCLIP (ViT-B-32) and Apple Vision, both running locally:** the image judgement. CLIP sorts work from casual and flags screens, posters and "more than one person"; Vision finds faces, bodies and text. Both run on my Mac because my photos may not go to any online service.
- **Me:** the spec and its rules, the creative direction (home photos stay, K-pop style), and the calls after watching it (fewer office shots). Claude did the first photo-by-photo review of the contact sheets.
- **(Ben: add anything else you used, such as ChatGPT or Claude.ai for brainstorming.)**

## Development process

| When | What |
|---|---|
| Thu 10/2, 2:45 pm | Spec written; pipeline v1 built and dry-run |
| Thu 10/2, 3:00 to 3:30 pm | Home rule changed; three review passes over contact sheets; overrides file |
| Thu 10/2, 3:30 to 3:50 pm | Second-look face check added; v1 page, music, README; PR #118 merged |
| Thu 10/2, 4:03 to 4:30 pm | Version 2: music analysis, b-roll, director, WebGL player, MP4 render; PR #119 merged |
| Thu 10/2, 7:23 pm | Office repeats removed; PR #121 merged |
| Sun 10/4, 2:15 pm | Check-in prep; this log, the README draft and the Projects link |
| **(Ben: add your own work sessions here, e.g. watching and reviewing the video, your code edits, recording the demo.)** | |

## What I wrote or changed myself

- **(Ben: list your own edits here, with the file and why. For example: renamed the "STILL BEN" title in `scripts/make_reels_v2.py`; changed a bar pattern; skipped a photo in `scripts/reels_overrides.json` and reran the build.)**

## One place the AI got it wrong

**(Ben: rewrite in your own words.)** Three candidates:
1. **A confident wrong explanation.** Claude told me 2002 and 2003 were "almost all excluded by the home-radius rule". The rule had never been applied. It corrected itself when I asked.
2. **The face detector missed people.** Apple Vision found only one face in a photo of me holding a toddler, in a wedding kiss, and in a sunset shot with a second person, and Photos had tagged someone else as me. The pipeline had passed all four. The fix was a second, independent check on the exact frame being published (Vision's newer face model plus a local CLIP "more than one person" vote), plus my eyes on every photo.
3. **The wrong tempo.** The first beat detector read the track as 92 BPM. Splitting the analysis by frequency band showed the kick drum at 140 BPM; 92 was a dotted hi-hat pattern. Cutting at 92 would have put every cut off the beat.

## Prompts

### Thu 10/2, 2:45 pm: The spec (Claude Code, Opus 5.5)

> Build a re-runnable pipeline that turns my Apple Photos library into two short "movies" of my face over the years, and a page on my site that plays them.
>
> ## Setup
> - The site repo is https://github.com/bcollier/ben.collier.phd. Clone or pull it, then read AGENTS.md and README.md first and follow them:
>   - Work on a branch, open a PR, squash-merge it yourself, then pull main.
>   - Run `python3 scripts/build.py` after any data change.
>   - Public copy has no em dashes.
>   - Every chart and visual follows the Field Notebook design.
> - Read the Photos library with osxphotos (`pip install osxphotos`, in a venv). Read only; never modify the library. If macOS blocks access, tell me which app needs Full Disk Access and stop.
>
> ## Step 1: find me
> - Photos has me as a named person. Find which name (search People; "Ben" or "Ben Collier") and confirm it with me before going on.
> - Collect every photo where I am a detected face.
> - Skip: screenshots, documents, photos of screens, very blurry or very dark shots, near-duplicates (keep the best of a burst or a series taken within a minute), and anything taken within 1 km of my home.
>
> ## Step 2: pick about 150 per reel, spread out
> Make two reels:
> - **Professional Ben:** suits, ties, podiums, classrooms, conferences, graduations, campus, headshots, talks.
>   - Use Photos' own labels (osxphotos `labels`/`search_info`: e.g. Suit, Tie, Conference, Stage, Classroom, Office) and albums.
>   - If the labels are thin, add a local image classifier: CLIP via `open_clip` is fine. Never use a cloud service.
> - **Casual Ben:** travel, outdoors, family days, food, hobbies.
>
> For both reels:
> - Spread the picks evenly across years, back to the start of the library, and across places. Don't let one trip or one year dominate (cap each place-month).
> - Prefer photos where I'm the only face.
>
> ## Step 3: other people's faces
> Nobody else's face may appear.
> 1. If other faces are in the photo, try to crop to a frame (at least 1080px tall, 16:9 or 4:5) that contains my face and no other face box. Use osxphotos face regions, plus a local detector (Apple Vision via pyobjc, or OpenCV) to catch untagged faces.
> 2. If no clean crop exists, skip the photo. Don't blur, because blurred faces look bad in a slideshow.
> 3. Children: always skip if a child's face can't be fully cropped out.
>
> ## Step 4: export
> - **Images:**
>   - Export each pick as WebP, about 1600px on the long side, plus a small thumbnail.
>   - Path: `assets/reels/<pro|casual>/<nn>.webp`.
>   - Strip ALL metadata: no EXIF, no GPS, no dates, no camera info.
>   - Filenames are just numbers.
> - **Data:** `data/reels.json` with, per reel, an ordered list:
>   - `{src, w, h, place}` only.
>   - `place` is coarse: "Pittsburgh", "Doha, Qatar", "Thailand", "San Francisco". City for well-known cities, otherwise region or country.
>   - No dates, no coordinates, no names.
>   - Order photos oldest to newest, but don't store the dates.
> - **Report:** write a private summary (not committed) with counts per year and place, and what was skipped and why.
>
> ## Step 5: the page
> New page **/reels/**, added to the nav after "travel", built by `scripts/build.py`:
> - **Layout:** two reels side by side on desktop, stacked on phones, each with a title ("Professional Ben", "Casual Ben"), a play button, and a poster frame.
> - **Playback** is a browser slideshow, not a video file:
>   - each photo shows about 1.2s with a slow Ken Burns pan and zoom and a quick crossfade
>   - the place name appears in the Kalam handwriting font in a corner as a small taped label
>   - a thin progress bar and a counter
>   - pause, resume and mute controls
>   - keyboard accessible
> - **Music:** simple, upbeat, truly free music.
>   - Use a CC0 / public-domain track (Free Music Archive CC0, OpenGameArt CC0, or a public-domain recording). Commit it as `assets/reels/music.mp3`, under 4 MB.
>   - Credit it in small text under the reels and in the README.
>   - Don't use anything that needs a paid licence or forbids redistribution.
> - **Sound** starts only when the visitor presses play. Browsers block autoplay with sound, and so should we.
> - **Reduced motion:** with `prefers-reduced-motion`, no pan or zoom; just a simple fade, or a grid of the photos.
> - **Performance:** preload a few images ahead, lazy-load the rest; must run smoothly on a phone.
>
> ## Step 6: make it a pipeline
> - Put all of this in `scripts/make_reels.py`, so I can run `python3 scripts/make_reels.py` any time and get a fresh selection.
>   - Keep it deterministic: the same library gives the same reels.
>   - Give it a `--per-reel 150` option and a `--dry-run` that only prints the picks.
>   - It writes `assets/reels/` and `data/reels.json`, then I run the build.
> - Document it in README.md: a short section with a flow diagram (Photos, then filter, then crop, then export, then build, then page), consistent with the rest of the README.
>
> ## Step 7: check and ship
> - Serve locally with `python3 -m http.server`. Screenshot /reels/ at 1440px and 390px in headless Chrome, before and during playback.
> - Look at every exported image once by eye for any other person's face and remove any you find.
> - Branch `feat/photo-reels`. The PR body gives the counts per reel, years covered, number of places, the music track and its licence, and how many photos were skipped for faces.
> - Merge, and confirm https://ben.collier.phd/reels/ plays.
>
> Don't upload my photos anywhere except this repo, and don't send them to any online service.

*What happened:* I wrote this spec before any code: the rules first (read-only library, no cloud, nobody else's face, no blurring, children always out), then the steps. Claude found my named person in Photos, wrote `scripts/make_reels.py`, and ran a dry run.

### Thu 10/2, ~3:00 pm: Confirming who I am in Photos

> yes that is me you can remember that Benjamin Collier is you

*What happened:* Claude asked which named person was me before going on, as the spec required. (Quoted from the session summary; the original message is in an earlier part of the session.)

### Thu 10/2, 3:00 pm: Changing the home rule

> what is this about are almost all excluded by the home-radius rule. ,  can you just scrape the location for home radius? this would remove two years of my life from the demo

*What happened:* My spec said to skip photos within 1 km of home. That would have cut two years of my life, so I changed the rule: keep home photos, label them only "Pittsburgh", and drop any that shows a house or street number (Apple Vision text recognition).

### Thu 10/2, 3:15 to 3:25 pm: Claude reviews the contact sheets

> (No prompt from me. My spec told Claude to look at every exported image by eye, so it rendered numbered contact sheets and went through them.)

*What happened:* 41 photos were removed on review: other people at the edges, children, sideways shots, a house number, a shirtless shot, and an ID card read as "professional". Each became an entry in `scripts/reels_overrides.json`.

### Thu 10/2, 3:53 pm: Reading the private report on my phone

> How do I see this on my phone link directly Library/Caches/ben-reels/report.md

*What happened:* The report stays out of the repo, so Claude sent it to me directly instead of publishing it.

### Thu 10/2, 3:55 pm: Checking before going public

> Ok give me what to do to get these checked before going public with anything I want to see the photos and tv animation where are they

*What happened:* I learned that v1 was already live, because my spec said to merge. Claude sent numbered contact sheets of all 179 photos and offered to take the page down.

### Thu 10/2, 4:03 pm: Version 2

> Give notes on the creation method . Mark this as version 1. Make a version two of this video that is twice as good. Kpop demon hunters style . So much animation. Colors distortions. Direct this and splice it with b-roll from safe for work places . Post as version 2. It should really be much better since it does not have to find the pictures use these
> Exact pictures

*What happened:* Claude tagged v1 as `reels-v1`, picked a CC0 track by analysing tempo and energy (it cannot listen), chose 48 already-public place photos with nobody in them as b-roll, wrote the director script and the WebGL player, rendered an MP4, and posted v2.

### Thu 10/2, 7:23 pm: Too many office shots

> the professional ben has too many pictures of my clearly in my office, they are the same background over and over, reduce number of pictures

*What happened:* I sent a screenshot. Seven photos with the same backdrop came out (29 to 22), and the v2 professional section was re-timed to fit.

### Sun 10/4, 2:16 pm: Check-in prep

> ok we have a required thing for a check in for this project. it is frpm 2-5pm it takes 15 miniutes to get there and it is now 2:15 pm. I want to check in with progress giv eme top 10 ideas on next steps https://www.cs.cmu.edu/~113/project2.html

*What happened:* Claude read the Project 2 page and listed next steps against it.

### Sun 10/4, 2:18 pm: This log and the README

> do all this When you're back I can set up the README and prompt-log skeletons with your real prompts pulled from this session. You'd then rewrite the README in your own words.

*What happened:* Claude added this folder's README draft (for me to rewrite) and this log, and linked the project from my Projects page.
