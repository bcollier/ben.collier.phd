# ben.collier.phd

Faculty site for [Ben Collier](https://www.linkedin.com/in/bcollierphd), Assistant Teaching Professor of Business Analytics at the Tepper School of Business, Carnegie Mellon University.

Static HTML/CSS/JS. No build step for content edits, no CMS.

- **Host:** GitHub Pages, from `main` at the repo root
- **Course URL:** `https://<user>.github.io/ben.collier.phd/`
- **Final URL:** `https://ben.collier.phd` (attach later — see below)
- **Apex:** `collier.phd` redirects to `ben.collier.phd`

## Local preview

```bash
python3 scripts/build.py        # regenerate HTML after editing data/ or scripts/build.py
python3 -m http.server 43217    # or: npm start
```

Open [http://127.0.0.1:43217](http://127.0.0.1:43217).

## Put it on GitHub

The repo should live at **`github.com/bcollier/ben.collier.phd`**.

```bash
gh auth login                   # or: export GITHUB_TOKEN=...
./scripts/setup_github.sh       # creates the repo, pushes main, turns on Pages
```

Override the defaults with `./scripts/setup_github.sh <owner> <repo>`.

**Token permissions.** Creating a repository needs more than you might expect. A fine-grained token must have **Administration: Read and write** — `POST /user/repos` rejects Contents and Pages alone with `Resource not accessible by personal access token`. A classic token needs the whole `repo` scope. Simplest alternative: create the repo in the browser first, then re-run the script, which detects the existing repo and just pushes. For pushing and configuring Pages afterward, a fine-grained token only needs **Contents: write** and **Pages: write**.

Prefer clicking through it? Create `ben.collier.phd` at [github.com/new](https://github.com/new), then:

```bash
git remote add github https://github.com/bcollier/ben.collier.phd.git
git push -u github main
```

Then **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**. `.nojekyll` is committed, so GitHub serves the files as-is. All internal links are relative, so the site works both at a domain root and under `/ben.collier.phd/`.

Hand in the `github.io` URL that Settings → Pages shows.

## Custom domain (do this second)

There is deliberately **no `CNAME` file in the repo yet**. Attaching a custom domain makes GitHub Pages redirect the `github.io` URL to that domain — which would break the link you turn in for class. Ship on `github.io` first.

When you are ready, add DNS at your registrar for `collier.phd`:

| Type | Name | Value |
| --- | --- | --- |
| `CNAME` | `ben` | `bcollier.github.io` |

and a permanent (301) redirect: `collier.phd` → `https://ben.collier.phd/`. A Cloudflare Redirect Rule does this in one step. GitHub Pages only supports one custom domain per site, which is why the apex is a DNS-level redirect rather than a second `CNAME` file.

Then:

```bash
./scripts/enable_domain.sh
```

That writes `CNAME`, pushes, sets the Pages domain, and enables HTTPS enforcement.

## Paste / update content

| What | Where |
| --- | --- |
| Full CV | `data/cv.md`, then `python3 scripts/build.py` |
| Students, advised papers | `data/students.json` |
| Course sample projects | `data/projects.json` |
| LinkedIn shout-outs | `data/linkedin.json` or `scripts/add_linkedin_post.py` |
| Student photos | `assets/students/<slug>.jpg` or `scripts/fetch_linkedin_photo.py` |
| Paper PDFs | `papers/` |
| Calendly | `js/config.js` |

### Import a LinkedIn post

```bash
python3 scripts/add_linkedin_post.py \
  --url 'https://www.linkedin.com/posts/...' \
  --date 2026-08-30 \
  --text 'Proud of this capstone team for ...' \
  --people 'Student Name' \
  --tags students teaching
```

LinkedIn has no public RSS feed, so posts are stored as a static copy in `data/linkedin.json` and rendered on `/students/` and `/news/`.

### Fetch a LinkedIn photo

```bash
python3 scripts/fetch_linkedin_photo.py --slug michelle-min --linkedin michelle-de-min
```

Then point `"photo"` at it in `data/students.json`. Headshots render as circles, so square source images work best — anything non-square is center-cropped by CSS. Use `assets/students/placeholder.svg` for someone without a photo.

### Add an advised paper

In `data/students.json` → `papers`, replace a placeholder:

```json
{
  "id": "capstone-2026-retail",
  "title": "Pricing segments for a regional grocer",
  "students": ["Ada Example", "Grace Example"],
  "year": "2026",
  "kind": "capstone",
  "summary": "Two-paragraph abstract of the project.",
  "link": "papers/capstone-2026-retail.pdf",
  "status": "public"
}
```

## Site map

- **Home** — portrait, bio, courses built, student project strip
- **Courses** — built and taught, each with sample student projects
- **Students** — photos, advised papers, capstone log, LinkedIn highlights
- **Materials** — notebooks, video, workshops
- **Practice** — Hot Metal Data, gAIm Systems
- **CV** — generated from `data/cv.md`
- **News** — dated log
- **Contact** — email, office, Calendly hook
