// Week by week on course pages. The schedule runs down the left; the projector
// on the right stays in view and shows the slides of whichever session is in
// the middle of the window, or under the pointer, or focused. Its strip of
// five thumbnails picks a slide, and it steps through them on its own unless
// the visitor prefers reduced motion or is pointing at it.
//
// Without this script every row keeps its own thumbnail strip, and the
// projector shows the first session's first slide.
(function () {
  "use strict";
  var list = document.querySelector(".weeks");
  var view = document.querySelector(".projector");
  if (!list || !view) return;

  var main = view.querySelector(".proj-main");
  var topic = view.querySelector(".proj-topic");
  var when = view.querySelector(".proj-cap b");
  var say = view.querySelector(".proj-say");
  var strip = view.querySelector(".proj-strip");
  var rows = Array.prototype.slice.call(list.querySelectorAll(".wk.has-slides"));
  if (!rows.length) return;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var HOLD = 3600;

  var decks = rows.map(function (row) {
    return Array.prototype.map.call(row.querySelectorAll(".wk-strip img"), function (t) {
      return { full: t.getAttribute("data-full"), thumb: t.getAttribute("src"), caption: t.getAttribute("data-caption") || "", el: t };
    });
  });

  var active = -1, slide = 0, timer = null, paused = false, token = 0, visible = true;

  // Each full-size slide is fetched and decoded once before it is shown, so
  // the projector never lands on a half-loaded frame.
  var ready = {};
  function load(src) {
    if (!ready[src]) {
      ready[src] = new Promise(function (res) {
        var im = new Image();
        var done = function () { res(src); };
        im.onload = im.onerror = done;
        setTimeout(done, 2500);
        im.src = src;
        if (im.decode) im.decode().then(done, function () {});
      });
    }
    return ready[src];
  }

  function buildStrip(i) {
    strip.innerHTML = "";
    decks[i].forEach(function (s, k) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("aria-label", "Slide " + (k + 1) + " of " + decks[i].length + ": " + s.caption);
      b.innerHTML = '<img src="' + s.thumb + '" alt="" width="160" height="90">';
      b.addEventListener("click", function () { pick(k, true); });
      strip.appendChild(b);
    });
  }

  function mark() {
    Array.prototype.forEach.call(strip.querySelectorAll("button"), function (b, k) {
      b.setAttribute("aria-pressed", String(k === slide));
    });
    decks[active].forEach(function (s, k) { s.el.classList.toggle("is-on", k === slide); });
  }

  function pick(k, byHand) {
    var deck = decks[active];
    slide = (k + deck.length) % deck.length;
    var s = deck[slide], mine = ++token;
    mark();
    say.textContent = s.caption;
    main.classList.add("fading");
    load(s.full).then(function () {
      if (mine !== token) return;
      main.src = s.full;
      main.alt = s.caption;
      main.removeAttribute("loading");
      main.classList.remove("fading");
      load(deck[(slide + 1) % deck.length].full);
    });
    schedule(byHand ? HOLD * 1.6 : HOLD);
  }

  function schedule(ms) {
    clearTimeout(timer);
    if (paused || still || !visible) return;
    timer = setTimeout(function () { pick(slide + 1); }, ms);
  }

  function activate(i) {
    if (i === active || i < 0) return;
    if (active >= 0) rows[active].classList.remove("on");
    active = i;
    var row = rows[i];
    row.classList.add("on");
    when.textContent = row.querySelector("time").textContent;
    topic.textContent = row.querySelector(".wk-t").textContent;
    buildStrip(i);
    pick(0);
    if (decks[i + 1]) load(decks[i + 1][0].full);
  }

  rows.forEach(function (r, i) {
    r.addEventListener("mouseenter", function () { activate(i); });
    r.addEventListener("focus", function () { activate(i); });
    r.addEventListener("click", function () { activate(i); });
  });

  // Scrolling: the session crossing the middle band of the window takes over.
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) activate(rows.indexOf(e.target)); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    rows.forEach(function (r) { io.observe(r); });
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible) schedule(HOLD); else clearTimeout(timer);
    }).observe(view);
  }

  function pause(on) {
    paused = on;
    if (on) clearTimeout(timer); else schedule(HOLD);
  }
  view.addEventListener("mouseenter", function () { pause(true); });
  view.addEventListener("mouseleave", function () { pause(false); });
  view.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") { pick(slide + 1, true); e.preventDefault(); }
    if (e.key === "ArrowLeft") { pick(slide - 1, true); e.preventDefault(); }
  });
  document.addEventListener("visibilitychange", function () { pause(document.hidden); });

  // Where the term is today: past dates dim a little, and today's session (or
  // the next one, mid-term) gets a note in the margin. Worked out in the
  // browser so it never goes stale.
  var now = new Date();
  var today = [now.getFullYear(), ("0" + (now.getMonth() + 1)).slice(-2), ("0" + now.getDate()).slice(-2)].join("-");
  var all = list.querySelectorAll(".wk"), upcoming = null, anyPast = false, todayRow = null;
  Array.prototype.forEach.call(all, function (r) {
    var d = r.getAttribute("data-date") || "";
    if (d === today) todayRow = r;
    if (d < today) { r.classList.add("is-past"); anyPast = true; }
    else if (!upcoming && !r.classList.contains("off")) upcoming = r;
  });
  var flag = todayRow || (anyPast && upcoming);
  if (flag) {
    var tn = document.createElement("span");
    tn.className = "note today-note";
    tn.setAttribute("aria-hidden", "true");
    tn.textContent = flag === todayRow ? "← today!" : "← next class";
    flag.appendChild(tn);
  }

  // Start on the most recent session with slides, or the first one.
  var start = 0;
  rows.forEach(function (r, i) { if ((r.getAttribute("data-date") || "") <= today) start = i; });
  activate(start);
})();
