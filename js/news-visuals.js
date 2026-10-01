// News: items that mention a course carry five slide thumbnails. The item in
// the middle of the window, or under the pointer, crossfades through them;
// the rest hold still on their first slide.
(function () {
  const boxes = Array.from(document.querySelectorAll(".news-vis.slides"));
  if (!boxes.length || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let active = null, timer = null;

  function step(box) {
    const imgs = box.querySelectorAll("img");
    const i = Array.from(imgs).findIndex(function (im) { return im.classList.contains("on"); });
    const next = imgs[(i + 1) % imgs.length];
    const go = function () {
      imgs[i].classList.remove("on");
      next.classList.add("on");
    };
    if (next.decode) next.decode().then(go, go); else go();
  }

  function play(box) {
    if (box === active) return;
    active = box;
    clearInterval(timer);
    if (!box) return;
    box.querySelectorAll("img").forEach(function (im) { im.loading = "eager"; });
    timer = setInterval(function () { step(box); }, 1700);
  }

  let queued = false;
  function pick() {
    queued = false;
    const mid = window.innerHeight / 2;
    let best = null, dist = Infinity;
    boxes.forEach(function (b) {
      const r = b.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      const d = Math.abs((r.top + r.bottom) / 2 - mid);
      if (d < dist) { dist = d; best = b; }
    });
    play(best);
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(pick); } }
  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue);
  boxes.forEach(function (b) {
    b.addEventListener("mouseenter", function () { play(b); });
    b.addEventListener("mouseleave", queue);
  });
  document.addEventListener("visibilitychange", function () { if (document.hidden) play(null); else queue(); });
  queue();
})();
