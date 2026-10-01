// Week-by-week schedule on course pages. The session nearest the middle of the
// window becomes active, and the stage plays its five slides. Every image is
// decoded before it is shown, so a crossfade never lands on a half-loaded
// frame. Without JavaScript the rows keep their thumbnail strips and the
// stage shows the first slide.
(function () {
  const section = document.querySelector("[data-schedule]");
  if (!section) return;
  const stage = section.querySelector(".stage");
  const rows = Array.from(section.querySelectorAll(".sched-row.has-slides"));
  if (!stage || !rows.length) return;

  const imgs = stage.querySelectorAll(".stage-img");
  const whenEl = stage.querySelector(".stage-when");
  const topicEl = stage.querySelector(".stage-topic");
  const captionEl = stage.querySelector(".stage-caption");
  const pipsEl = stage.querySelector(".stage-pips");
  const still = window.matchMedia("(prefers-reduced-motion: reduce)");
  const HOLD = 3200;

  const decks = rows.map(function (row) {
    return Array.from(row.querySelectorAll(".sched-strip img")).map(function (t) {
      return { src: t.dataset.full, caption: t.dataset.caption, thumb: t };
    });
  });

  // Each full-size slide is fetched and decoded once, then reused.
  const ready = new Map();
  function load(src) {
    if (!ready.has(src)) {
      const im = new Image();
      // decode() can stall in a background tab, so a plain load (or a short
      // timeout) is allowed to win the race.
      const loaded = new Promise(function (res) {
        im.onload = im.onerror = function () { setTimeout(res, 120); };
        setTimeout(res, 2500);
      });
      im.src = src;
      const decoded = im.decode ? im.decode().catch(function () {}) : loaded;
      ready.set(src, Promise.race([decoded, loaded]).then(function () { return src; }));
    }
    return ready.get(src);
  }
  function warm(i) {
    if (decks[i]) decks[i].forEach(function (s) { load(s.src); });
  }

  let active = -1, slide = 0, front = 0, timer = null, paused = false, token = 0;

  function pips(n) {
    pipsEl.innerHTML = "";
    for (let i = 0; i < n; i++) {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Slide " + (i + 1) + " of " + n);
      b.addEventListener("click", function () { show(i, true); });
      pipsEl.appendChild(b);
    }
  }

  function mark() {
    pipsEl.querySelectorAll("button").forEach(function (b, i) {
      b.classList.toggle("is-on", i === slide);
      b.setAttribute("aria-current", i === slide ? "true" : "false");
    });
    decks[active].forEach(function (s, i) { s.thumb.classList.toggle("is-on", i === slide); });
    stage.style.setProperty("--hold", HOLD + "ms");
    pipsEl.classList.remove("run");
    void pipsEl.offsetWidth; // restart the progress fill on the current pip
    if (!paused && !still.matches) pipsEl.classList.add("run");
  }

  function show(i, byHand) {
    const deck = decks[active];
    slide = (i + deck.length) % deck.length;
    const s = deck[slide];
    const mine = ++token;
    load(s.src).then(function () {
      if (mine !== token) return; // a newer request already won
      const next = imgs[1 - front], cur = imgs[front];
      next.src = s.src;
      next.alt = s.caption;
      next.removeAttribute("aria-hidden");
      cur.setAttribute("aria-hidden", "true");
      cur.alt = "";
      next.classList.add("is-on");
      cur.classList.remove("is-on");
      front = 1 - front;
      captionEl.textContent = s.caption;
      mark();
      load(deck[(slide + 1) % deck.length].src);
    });
    schedule(byHand ? HOLD * 1.5 : HOLD);
  }

  function schedule(ms) {
    clearTimeout(timer);
    if (paused || still.matches) return;
    timer = setTimeout(function () { show(slide + 1); }, ms);
  }

  function activate(i) {
    if (i === active || i < 0) return;
    if (active >= 0) rows[active].classList.remove("is-active");
    active = i;
    const row = rows[i];
    row.classList.add("is-active");
    whenEl.textContent = row.querySelector("time").textContent + " · " + row.querySelector(".sched-when span").textContent;
    topicEl.textContent = row.querySelector(".sched-topic").textContent;
    pips(decks[i].length);
    stage.classList.remove("swap");
    void stage.offsetWidth;
    stage.classList.add("swap");
    show(0);
    warm(i + 1);
    warm(i - 1);
  }

  // The active session is the one under a focus line: mid-window on wide
  // screens, and mid-way through the space left below the pinned stage on
  // phones, where the stage sits on top of the list.
  const header = document.querySelector("header.site");
  const stacked = window.matchMedia("(max-width: 56rem)");
  function pin() {
    const h = header ? header.getBoundingClientRect().height : 0;
    section.style.setProperty("--stage-top", Math.round(h + 8) + "px");
  }
  let queued = false;
  function pick() {
    queued = false;
    let line = window.innerHeight / 2;
    if (stacked.matches) {
      const bottom = stage.getBoundingClientRect().bottom;
      line = bottom + (window.innerHeight - bottom) / 2;
    }
    let best = -1, dist = Infinity;
    rows.forEach(function (r, i) {
      const b = r.getBoundingClientRect();
      const d = line < b.top ? b.top - line : line > b.bottom ? line - b.bottom : 0;
      if (d < dist) { dist = d; best = i; }
    });
    const box = section.querySelector(".sched-list").getBoundingClientRect();
    if (box.bottom > 0 && box.top < window.innerHeight) activate(best);
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(pick); } }
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", function () { pin(); queue(); });
  pin();

  rows.forEach(function (r, i) {
    r.addEventListener("mouseenter", function () { activate(i); });
    r.addEventListener("focus", function () { activate(i); });
    r.querySelectorAll(".sched-strip img").forEach(function (t, k) {
      t.addEventListener("click", function () { activate(i); show(k, true); });
    });
  });

  function pause(on) {
    paused = on;
    stage.classList.toggle("is-paused", on);
    if (on) { clearTimeout(timer); pipsEl.classList.remove("run"); }
    else if (active >= 0) { mark(); schedule(HOLD); }
  }
  stage.addEventListener("mouseenter", function () { pause(true); });
  stage.addEventListener("mouseleave", function () { pause(false); });
  stage.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { show(slide + 1, true); e.preventDefault(); }
    if (e.key === "ArrowLeft") { show(slide - 1, true); e.preventDefault(); }
  });
  document.addEventListener("visibilitychange", function () { pause(document.hidden); });

  // Mark where the term is today: past sessions dim slightly, and the next
  // class gets a label. Computed in the browser so it never goes stale.
  const now = new Date();
  const today = [now.getFullYear(), String(now.getMonth() + 1).padStart(2, "0"), String(now.getDate()).padStart(2, "0")].join("-");
  let upcoming = null;
  section.querySelectorAll(".sched-row").forEach(function (r) {
    if (r.dataset.date < today) r.classList.add("is-past");
    else if (!upcoming && !r.classList.contains("break")) upcoming = r;
  });
  const anyPast = section.querySelector(".sched-row.is-past");
  if (upcoming && anyPast) {
    const tag = document.createElement("span");
    tag.className = "sched-next";
    tag.textContent = "Next class";
    upcoming.querySelector(".sched-when").appendChild(tag);
  }

  // Start on the most recent session with slides, or the first one.
  let start = 0;
  rows.forEach(function (r, i) { if (r.dataset.date <= today) start = i; });
  activate(start);
  warm(start);
})();
