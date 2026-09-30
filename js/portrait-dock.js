/* Home page: as the visitor scrolls, the colour portrait shrinks, turns grey,
   dissolves into the stippled hedcut, and settles into the header beside the
   wordmark. On every other page the hedcut simply sits in the header.

   The portrait keeps its place in the layout; only a transform moves it, so
   nothing below it shifts. Progress runs from 0 (at rest) to 1 (docked). */
(function () {
  const morph = document.querySelector(".portrait-morph");
  const header = document.querySelector("header.site");
  if (!morph || !header) return;

  const colour = morph.querySelector(".portrait:not(.hedcut)");
  const hedcut = morph.querySelector(".hedcut");
  const wordmark = header.querySelector(".wordmark");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  let natural = null; // the portrait's untransformed box, in page coordinates
  let queued = false;

  function measure() {
    morph.style.transform = "none";
    const r = morph.getBoundingClientRect();
    natural = { left: r.left, top: r.top + window.scrollY, size: r.width };
    render();
  }

  function miniSize() {
    return parseFloat(getComputedStyle(header).getPropertyValue("--mini")) *
      parseFloat(getComputedStyle(document.documentElement).fontSize);
  }

  function render() {
    queued = false;
    if (!natural) return;
    // Docked by the time the whole portrait would have scrolled under the
    // header, so the flight takes about one portrait height of scrolling.
    const end = Math.max(120, natural.top + natural.size - header.offsetHeight * 0.5);
    const p = Math.min(1, Math.max(0, window.scrollY / end));

    if (reduce.matches) {
      morph.style.transform = "none";
      colour.style.filter = "";
      hedcut.style.opacity = 0;
      morph.style.visibility = "";
      header.style.setProperty("--dock", p >= 1 ? 1 : 0);
      header.classList.toggle("docked", p >= 1);
      return;
    }

    const e = p * p * (3 - 2 * p); // smoothstep
    header.style.setProperty("--dock", e);
    const mini = miniSize();
    const hr = header.getBoundingClientRect();
    const targetLeft = wordmark.getBoundingClientRect().left;
    const targetTop = hr.top + (hr.height - mini) / 2;
    const fromTop = natural.top - window.scrollY;

    const size = natural.size + (mini - natural.size) * e;
    const x = (targetLeft - natural.left) * e;
    const y = (targetTop - fromTop) * e;
    morph.style.transform =
      "translate(" + x + "px," + y + "px) scale(" + size / natural.size + ")";
    colour.style.filter = "grayscale(" + Math.min(1, p * 1.6) + ") contrast(" + (1 + 0.15 * e) + ")";
    hedcut.style.opacity = Math.min(1, Math.max(0, (p - 0.2) / 0.6));

    const docked = p >= 1;
    header.classList.toggle("docked", docked);
    morph.style.visibility = docked ? "hidden" : "";
  }

  function queue() {
    if (!queued) {
      queued = true;
      window.requestAnimationFrame(render);
    }
  }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", measure);
  reduce.addEventListener("change", measure);
  if (document.readyState === "complete") measure();
  else window.addEventListener("load", measure);
})();
