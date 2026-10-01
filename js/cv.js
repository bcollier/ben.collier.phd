/* CV page: highlight the section in view in the side index, and let the
   print button produce the paper version (styled by the print rules). */
(function () {
  const links = Array.from(document.querySelectorAll(".cv-toc a"));
  const byId = new Map(links.map(function (a) { return [a.hash.slice(1), a]; }));
  const visible = new Set();

  function mark() {
    // The first section (in page order) that is on screen is the current one.
    let current = null;
    for (const a of links) {
      if (visible.has(a.hash.slice(1))) { current = a; break; }
    }
    links.forEach(function (a) {
      if (a === current) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  }

  if ("IntersectionObserver" in window && links.length) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible.add(e.target.id);
        else visible.delete(e.target.id);
      });
      mark();
    }, { rootMargin: "-90px 0px -55% 0px" });
    byId.forEach(function (_, id) {
      const el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  document.querySelectorAll("[data-print]").forEach(function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
})();
