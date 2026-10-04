# The build prompt for the reels (version 1)

This is the prompt Claude Code wrote from Ben's question, which Ben pasted into a second Claude Code session on his laptop, where the Photos library lives. It is reproduced as written. See [the pipeline](../reels-pipeline.md) for what happened next.

````text
Build a re-runnable pipeline that turns my Apple Photos library into two short "movies" of my face over the years, and a page on my site that plays them.

## Setup
- The site repo is https://github.com/bcollier/ben.collier.phd. Clone or pull it, then read AGENTS.md and README.md first and follow them:
  - Work on a branch, open a PR, squash-merge it yourself, then pull main.
  - Run `python3 scripts/build.py` after any data change.
  - Public copy has no em dashes.
  - Every chart and visual follows the Field Notebook design.
- Read the Photos library with osxphotos (`pip install osxphotos`, in a venv). Read only; never modify the library. If macOS blocks access, tell me which app needs Full Disk Access and stop.

## Step 1: find me
- Photos has me as a named person. Find which name (search People; "Ben" or "Ben Collier") and confirm it with me before going on.
- Collect every photo where I am a detected face.
- Skip: screenshots, documents, photos of screens, very blurry or very dark shots, near-duplicates (keep the best of a burst or a series taken within a minute), and anything taken within 1 km of my home.

## Step 2: pick about 150 per reel, spread out
Make two reels:
- **Professional Ben:** suits, ties, podiums, classrooms, conferences, graduations, campus, headshots, talks.
  - Use Photos' own labels (osxphotos `labels`/`search_info`: e.g. Suit, Tie, Conference, Stage, Classroom, Office) and albums.
  - If the labels are thin, add a local image classifier: CLIP via `open_clip` is fine. Never use a cloud service.
- **Casual Ben:** travel, outdoors, family days, food, hobbies.

For both reels:
- Spread the picks evenly across years, back to the start of the library, and across places. Don't let one trip or one year dominate (cap each place-month).
- Prefer photos where I'm the only face.

## Step 3: other people's faces
Nobody else's face may appear.
1. If other faces are in the photo, try to crop to a frame (at least 1080px tall, 16:9 or 4:5) that contains my face and no other face box. Use osxphotos face regions, plus a local detector (Apple Vision via pyobjc, or OpenCV) to catch untagged faces.
2. If no clean crop exists, skip the photo. Don't blur, because blurred faces look bad in a slideshow.
3. Children: always skip if a child's face can't be fully cropped out.

## Step 4: export
- **Images:**
  - Export each pick as WebP, about 1600px on the long side, plus a small thumbnail.
  - Path: `assets/reels/<pro|casual>/<nn>.webp`.
  - Strip ALL metadata: no EXIF, no GPS, no dates, no camera info.
  - Filenames are just numbers.
- **Data:** `data/reels.json` with, per reel, an ordered list:
  - `{src, w, h, place}` only.
  - `place` is coarse: "Pittsburgh", "Doha, Qatar", "Thailand", "San Francisco". City for well-known cities, otherwise region or country.
  - No dates, no coordinates, no names.
  - Order photos oldest to newest, but don't store the dates.
- **Report:** write a private summary (not committed) with counts per year and place, and what was skipped and why.

## Step 5: the page
New page **/reels/**, added to the nav after "travel", built by `scripts/build.py`:
- **Layout:** two reels side by side on desktop, stacked on phones, each with a title ("Professional Ben", "Casual Ben"), a play button, and a poster frame.
- **Playback** is a browser slideshow, not a video file:
  - each photo shows about 1.2s with a slow Ken Burns pan and zoom and a quick crossfade
  - the place name appears in the Kalam handwriting font in a corner as a small taped label
  - a thin progress bar and a counter
  - pause, resume and mute controls
  - keyboard accessible
- **Music:** simple, upbeat, truly free music.
  - Use a CC0 / public-domain track (Free Music Archive CC0, OpenGameArt CC0, or a public-domain recording). Commit it as `assets/reels/music.mp3`, under 4 MB.
  - Credit it in small text under the reels and in the README.
  - Don't use anything that needs a paid licence or forbids redistribution.
- **Sound** starts only when the visitor presses play. Browsers block autoplay with sound, and so should we.
- **Reduced motion:** with `prefers-reduced-motion`, no pan or zoom; just a simple fade, or a grid of the photos.
- **Performance:** preload a few images ahead, lazy-load the rest; must run smoothly on a phone.

## Step 6: make it a pipeline
- Put all of this in `scripts/make_reels.py`, so I can run `python3 scripts/make_reels.py` any time and get a fresh selection.
  - Keep it deterministic: the same library gives the same reels.
  - Give it a `--per-reel 150` option and a `--dry-run` that only prints the picks.
  - It writes `assets/reels/` and `data/reels.json`, then I run the build.
- Document it in README.md: a short section with a flow diagram (Photos, then filter, then crop, then export, then build, then page), consistent with the rest of the README.

## Step 7: check and ship
- Serve locally with `python3 -m http.server`. Screenshot /reels/ at 1440px and 390px in headless Chrome, before and during playback.
- Look at every exported image once by eye for any other person's face and remove any you find.
- Branch `feat/photo-reels`. The PR body gives the counts per reel, years covered, number of places, the music track and its licence, and how many photos were skipped for faces.
- Merge, and confirm https://ben.collier.phd/reels/ plays.

Don't upload my photos anywhere except this repo, and don't send them to any online service.
````
