// Place popovers on the CV header: the office chip opens a campus map that
// draws itself in, the street address opens a photo of the building. Hover
// opens them with a short delay; a click or tap toggles; Escape closes.
(function () {
  const pops = Array.from(document.querySelectorAll(".place-pop"));
  if (!pops.length) return;
  function close(li) {
    li.classList.remove("open");
    li.querySelector(".pp-trigger").setAttribute("aria-expanded", "false");
  }
  function open(li) {
    pops.forEach(function (o) { if (o !== li) close(o); });
    if (li.classList.contains("open")) return;
    const card = li.querySelector(".pp-card");
    card.classList.remove("play"); void card.offsetWidth; card.classList.add("play");
    li.classList.add("open");
    li.querySelector(".pp-trigger").setAttribute("aria-expanded", "true");
    // Keep the card on screen: flip it to the left edge of the chip if needed.
    li.classList.remove("flip");
    const r = card.getBoundingClientRect();
    if (r.right > window.innerWidth - 8) li.classList.add("flip");
  }
  pops.forEach(function (li) {
    let t = null;
    const btn = li.querySelector(".pp-trigger");
    li.addEventListener("pointerenter", function (e) {
      if (e.pointerType !== "mouse") return;
      clearTimeout(t); t = setTimeout(function () { open(li); }, 120);
    });
    li.addEventListener("pointerleave", function (e) {
      if (e.pointerType !== "mouse") return;
      clearTimeout(t); t = setTimeout(function () { close(li); }, 260);
    });
    btn.addEventListener("click", function () { li.classList.contains("open") ? close(li) : open(li); });
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") pops.forEach(close); });
  document.addEventListener("click", function (e) { pops.forEach(function (li) { if (!li.contains(e.target)) close(li); }); });
})();
