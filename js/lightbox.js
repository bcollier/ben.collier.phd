// lightbox.js
// Portfolio screenshots open in a layer over the page instead of navigating to
// the image file. Any link marked data-lightbox opens; close with the X, Escape,
// or a click outside the picture. With several on a page, the arrow keys and
// the side buttons step through them. Without this script the links still open
// the full-size image, so nothing is lost.
(function () {
  const links = Array.from(document.querySelectorAll("a[data-lightbox]"));
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  const box = document.createElement("dialog");
  box.className = "lightbox";
  box.setAttribute("aria-label", "Screenshot");
  box.innerHTML =
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-close" aria-label="Close">&times;</button>' +
    '<button type="button" class="lb-step lb-prev" aria-label="Previous screenshot">&larr;</button>' +
    '<button type="button" class="lb-step lb-next" aria-label="Next screenshot">&rarr;</button>';
  document.body.appendChild(box);
  const img = box.querySelector("img");
  const caption = box.querySelector("figcaption");
  let current = 0;

  function show(i) {
    current = (i + links.length) % links.length;
    const link = links[current];
    const thumb = link.querySelector("img");
    const text = link.closest("figure")?.querySelector("figcaption")?.textContent || "";
    img.src = link.href;
    img.alt = thumb ? thumb.alt : "";
    caption.textContent = text;
    caption.hidden = !text;
    box.classList.toggle("single", links.length < 2);
  }

  links.forEach((link, i) => {
    link.addEventListener("click", (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return; // new tab still works
      event.preventDefault();
      show(i);
      if (!box.open) box.showModal();
    });
  });

  box.querySelector(".lb-close").addEventListener("click", () => box.close());
  box.querySelector(".lb-prev").addEventListener("click", () => show(current - 1));
  box.querySelector(".lb-next").addEventListener("click", () => show(current + 1));
  // A click on the backdrop lands on the dialog itself, not on its contents.
  box.addEventListener("click", (event) => {
    if (event.target === box) box.close();
  });
  box.addEventListener("keydown", (event) => {
    if (links.length < 2) return;
    if (event.key === "ArrowRight") show(current + 1);
    if (event.key === "ArrowLeft") show(current - 1);
  });
  // Escape closes a modal dialog natively.
  box.addEventListener("close", () => img.removeAttribute("src"));
})();
