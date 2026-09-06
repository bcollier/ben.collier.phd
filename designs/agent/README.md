# ben-collier — agent session

Design 6 of 6 for `ben.collier.phd`. A single static page: `index.html`,
`style.css`, `script.js`, and one portrait. Open `index.html` and it runs. No
build step, no framework, no dependency except one webfont.

## The concept

Ben teaches and works on agentic AI. So the portfolio presents him as the agent
being run: a session that starts, a task queue with live status, a run history
with exit codes, and a log.

```
$ agent run ben-collier --semester fall-2026
session started. 4 tasks active, 1 blocked.
```

The joke is structural rather than written. Nothing on the page nudges you and
says "get it" — the humour is in the framing and in the accuracy of the details.
The line that makes it work is `RUNNING  Enrolled as a student in 15-113 Coding
with AI · Mon/Wed · yes, at the same time`, which is true, and the line that
keeps it from being pleased with itself is `BLOCKED  Selling a house`, which is
stated once and never explained.

Three sections, in this order:

| Section | What it is |
| --- | --- |
| The live session | Active task queue. The landing view. |
| Previous runs | Ventures and courses as processes with status, elapsed time, exit codes. |
| How I got here | The log, reverse chronological, year-prefixed. |

## Decisions

**No fake shell.** The obvious version of this idea gives you a prompt and lets
you type `help`. That version buries the content behind an interaction almost
nobody wants and turns a portfolio into a puzzle. The terminal here is the
page's structural language, not a toy. The only commands you can press are the
two booking lines, which is the one place the metaphor does real work: a
consulting rate is exactly the kind of thing you want to invoke.

**Amber on near-black.** Every colour was measured, not eyeballed, against the
`#0C0C0C` ground:

| Role | Colour | Contrast |
| --- | --- | --- |
| Body text | `#FFB000` | 10.68:1 |
| `RUNNING` | `#FFD166` | 13.57:1 |
| `BLOCKED` | `#DE7C2C` | 6.54:1 |
| `DONE` | `#B98A34` | 6.29:1 |
| Metadata | `#A87F31` | 5.35:1 |
| Rules and borders | `#3A2E17` | never carries text |

All text passes WCAG AA comfortably. The three status keywords each read
differently at a glance, and the differentiator is the word itself, so the
colour is reinforcement rather than the whole signal.

There is a reason this palette and no other, and it is a local one. It is left
visual and unstated: the page never names it. Amber phosphor happens to be the
colour of a pour, and the city this practice is named after used to make a lot
of both. That is the entire reference. No bridges, no skyline, no textures.

**A real measure.** The content column is 76 characters wide on desktop, inside
the 70–80 the brief asked for. This is what most terminal-themed sites get
wrong: they run full-bleed, and a 160-character line is the tell that you are
looking at a website in costume rather than a terminal. Below 560px the measure
relaxes and the status column stacks above its task, so nothing scrolls
sideways. Verified at 320, 360, 375, 390, 768, 1024 and 1440 pixels.

**One animated thing.** The session block types itself out once, on load, in
about 1.6 seconds. Nothing else on the page moves. Under
`prefers-reduced-motion` it renders instantly and the cursor stops blinking.

**The portrait is duotoned into the palette** with a CSS filter, so it belongs
to the page rather than sitting on top of it as a photograph. It appears as the
output of `$ whoami`, which is where a photograph belongs in this metaphor.

**Scanlines at 0.022 alpha over a 3px period.** An earlier pass had them at
0.06 over 2px, which moirés against the line height and reads as a Halloween
filter. They are now the kind of thing you notice only if you go looking, and
they disappear entirely under `prefers-reduced-transparency`.

## The part worth reading if you are grading this

The first version hid the task queue and the command line behind the typing
animation. Rendering the page from `file://` in headless Chrome starved
`requestAnimationFrame`, the animation never ran, and the page showed an empty
box where the content should be. The brief said it must run by opening
`index.html`, and it did not.

Three changes came out of that, and they are the most useful thing in this
directory:

1. **The animation no longer owns the content.** The command line reveals by
   widening a clip in whole `ch` units, which in a monospace face is literally
   character-by-character typing. The full string stays in the DOM the entire
   time. The earlier version emptied `textContent` and refilled it, so a
   stalled animation destroyed the text permanently.
2. **The fallback lives outside the thing that can fail.** A dead man's switch
   in the inline `<head>` script strips the hiding class after 2.8 seconds, and
   the stylesheet carries its own 2.6 second reveal. A fallback inside
   `script.js` is not a fallback if `script.js` is what stalled.
3. **The starting clip is written by the first frame, not at setup.** An inline
   style written before the loop proves it can run will outlive a stall and
   keep the content hidden forever.

The page is fully readable with JavaScript disabled, blocked, or broken.

Timers were the other lesson. The first implementation chained about 45
`setTimeout` calls. Browsers clamp those to roughly 1Hz in a tab that is not in
the foreground, which stretched a 1.6 second animation to eleven seconds in
testing. It is now a single `requestAnimationFrame` loop that derives its state
from elapsed time, so a throttled tab lands on the finished state instead of
crawling through it.

## Deliberately left out

- **A postal address.** The brief banned a particular word outright and the
  office address is the only place it appears. It is also the least
  terminal-native line in a contact block, so it went rather than got
  abbreviated. Email, LinkedIn, GitHub and ORCID remain.
- **Publications, awards, the full course list, the CV.** This design argues
  for a narrow column and a short page. The multi-page site carries the
  complete record and this links to it.
- **A dark/light toggle.** Amber phosphor on white is not a design, it is a
  mistake.
- **Live booking.** The two commands open a prefilled email and the page says
  so in plain words. See the TODO at the top of `script.js`: paste a Calendly
  URL in and the copy changes itself. The paid tier will likely want its own
  event type with payment collection attached.

## Credits

Written, designed, and coded by Ben Collier. Drafted with Claude (Anthropic) in
Claude Code, then edited by hand; each file carries an `AI USAGE NOTE` comment
recording what the model produced and what was changed, and the full prompt log
is at [`../../PROMPTS.md`](../../PROMPTS.md).

Typeface [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) by
Philipp Nurullin and Konstantin Bulenkov for JetBrains, SIL Open Font License,
served by Google Fonts. Portrait photograph courtesy Carnegie Mellon University.

No analytics, no trackers, no cookies, and no network requests beyond the
webfont.
