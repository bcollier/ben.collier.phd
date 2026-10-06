# Roadmap

Ideas and next steps for ben.collier.phd that are agreed but not built yet. Newest first.
When an item ships, delete it here and describe it in the README.

## Cloudflare Web Analytics, as a second count

Google Analytics 4 is the main analytics (README, "Analytics"). Cloudflare Web Analytics
would run beside it as a cookie-free count:

- Free, in the same Cloudflare account as the reels video storage. No cookies, so no
  consent question in any country.
- Counts page views, visits, referrers, countries, devices and page speed (Core Web Vitals).
  It does not measure time on site or individual clicks; GA4 keeps doing that.
- Ad blockers block it less often than GA4, so comparing the two shows roughly how many
  visitors GA4 misses.
- Setup: Cloudflare dashboard, Analytics & Logs, Web Analytics, add site `ben.collier.phd`,
  copy the site token (public, like the GA4 ID), add a `cf_beacon_token` to `data/site.json`,
  and have `build.py` write Cloudflare's beacon script next to the GA4 loader when it is set.
  Keep it off localhost, as `js/analytics.js` does.

## Reels version 2: folk recut

Recut the music video to a gentle CC0 folk track, with fewer and slower cuts and without the
goofy faces, then render it to MP4 and store it in R2 (`drafts/` first, `published/` after
Ben approves the cut).

## Booking links

The Book a call buttons fall back to e-mail until the Cal.com events exist (a free
15-minute call and a paid hour). Their links go in `js/config.js`.

## A media address on collier.phd

Videos are served from `reels-media.ben-b77.workers.dev`. A `media.collier.phd` address
needs the collier.phd DNS moved from Squarespace to Cloudflare (free, but it touches the
live site's DNS), then a custom domain on the Worker.

## A course chatbot

A small assistant on the site that answers questions about Ben's courses from the course
pages and syllabi. Needs a free or cheap backend for the model call.
