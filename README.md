# Ben Collier — ben.collier.phd

Faculty site for [Ben Collier](https://www.linkedin.com/in/bcollierphd), Assistant Teaching Professor of Business Analytics at the Tepper School of Business, Carnegie Mellon University.

Static HTML/CSS/JS. No CMS. **GitHub Pages** hosts the files (required for class). The public hostname is **https://ben.collier.phd**. The apex **collier.phd** should redirect there.

## Local preview

```bash
python3 scripts/build.py
python3 -m http.server 43217 --bind 0.0.0.0
# or: npm start
```

Open [http://127.0.0.1:43217](http://127.0.0.1:43217).

## GitHub Pages (course URL)

1. Push this repo to GitHub (`bcollier.github.io` → `https://bcollier.github.io/`, or any repo → `https://<user>.github.io/<repo>/`).
2. Settings → Pages → Deploy from branch → `main` → `/ (root)`.
3. Turn in the `*.github.io` URL GitHub shows.

`.nojekyll` is present. Links are relative so project pages and user pages both work.

## Domains: ben.collier.phd + collier.phd redirect

The `CNAME` file is `ben.collier.phd` — that is the GitHub Pages custom domain and the canonical site.

### DNS for the site itself

| Type | Name | Value |
| --- | --- | --- |
| `CNAME` | `ben` | `bcollier.github.io` |

(If the GitHub Pages site is a project page, the CNAME target is still `bcollier.github.io`.)

### Redirect apex → subdomain

GitHub Pages only attaches **one** custom domain per site. Put the site on `ben.collier.phd`, then redirect the apex at your DNS host (Cloudflare, Namecheap, Google Domains, etc.):

- `collier.phd` → `https://ben.collier.phd/` (301 / permanent URL redirect)
- `www.collier.phd` → `https://ben.collier.phd/` (optional)

In Cloudflare, a Redirect Rule is enough. Do **not** put `collier.phd` in the repo `CNAME` file; that would make the apex the primary host.

After DNS checks green in GitHub → Settings → Pages, enable **Enforce HTTPS**.

Until DNS is live, graders should use the `github.io` URL. If GitHub starts redirecting `github.io` to `ben.collier.phd` before DNS works, temporarily remove `CNAME`.

## Paste / update content

| What | Where |
| --- | --- |
| Full CV | `data/cv.md` → then `python3 scripts/build.py` |
| Student roster + advised papers | `data/students.json` |
| Course sample projects | `data/projects.json` |
| LinkedIn shout-outs | `data/linkedin.json` or `scripts/add_linkedin_post.py` |
| Student photos | `assets/students/<slug>.jpg` or `scripts/fetch_linkedin_photo.py` |
| Calendly | `js/config.js` |

### Import a LinkedIn post (student highlights)

```bash
python3 scripts/add_linkedin_post.py \
  --url 'https://www.linkedin.com/posts/...' \
  --date 2026-08-30 \
  --text 'Proud of this capstone team for ...' \
  --people 'Student Name' \
  --tags students teaching
```

### Fetch a LinkedIn photo

```bash
python3 scripts/fetch_linkedin_photo.py \
  --slug michelle-min \
  --linkedin michelle-de-min
```

Then set `"photo": "assets/students/michelle-min.jpg"` in `data/students.json` and rebuild if needed.

### Advised paper / project summary

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

Put PDFs in `papers/`.

## Site map

- **Home** — photo, bio, courses built, student project strip
- **Courses** — built / taught, with sample studio projects on each course page
- **Students** — photos, advised papers, capstone log, LinkedIn highlights
- **Materials** — notebooks, video, workshops
- **Practice** — Hot Metal Data, gAIm Systems
- **CV** — full vita from `data/cv.md`
- **News** — dated log
- **Contact** — email, office, Calendly hook
