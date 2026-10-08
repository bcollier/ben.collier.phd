/* The course-assistant launcher: a legal-pad note that peels off the page and
   opens into a full legal pad, then hands the visitor to Faculty Twin.

   Any <a data-handoff> works. Without this script it is a plain link. With it:
   the note lifts and straightens (0 to 200ms), grows to fill the screen
   (200 to 650ms) while the pad's margin, rules and "Opening the course
   assistant..." are written in, then the browser goes to the link. The last
   frame is the HANDOFF FRAME in css/handoff.css, which Faculty Twin paints
   first on arrival, so the two pages meet without a seam.

   Reduced motion: no movement, the finished frame fades in over 150ms.
   Back button (page restored from the back/forward cache): the note is put
   back. Ctrl, Cmd, Shift and middle clicks open the link the usual way. */
(function () {
  "use strict";
  var notes = document.querySelectorAll("a[data-handoff]");
  if (!notes.length || !Element.prototype.animate) return;

  var MS = 650;
  var EASE = "cubic-bezier(.2,.8,.2,1)";
  var busy = false, layer = null, lifted = null;
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)");
  var root = document.documentElement;
  // The words on the pad, as the same outlined Kalam glyphs the twin paints,
  // so the two frames match to the pixel. Fetched only once a visitor points
  // at or focuses the note; until it arrives, real Kalam text stands in.
  var SVG_URL = new URL("../assets/handoff-text.svg", document.currentScript.src).href;
  var svgText = null, svgReq = null, live = null;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  // The note's current angle and scale, read from its live transform, so the
  // lift starts from exactly what is on screen (hovered notes are straight).
  function pose(a) {
    var m = getComputedStyle(a).transform, rot = 0, s = 1;
    if (m && m !== "none") {
      var v = m.slice(m.indexOf("(") + 1, -1).split(",").map(parseFloat);
      rot = Math.atan2(v[1], v[0]) * 180 / Math.PI;
      s = Math.sqrt(v[0] * v[0] + v[1] * v[1]);
    }
    var r = a.getBoundingClientRect();
    return { cx: r.left + r.width / 2, cy: r.top + r.height / 2, w: a.offsetWidth, h: a.offsetHeight, rot: rot, s: s };
  }

  // Hold the page still under the sheet. The scrollbar's width goes back in
  // as padding so nothing behind the note shifts sideways.
  function lockScroll() {
    var bar = window.innerWidth - root.clientWidth;
    if (bar > 0) document.body.style.paddingRight = bar + "px";
    root.style.overflow = "hidden";  // html only: hiding body's too would unstick the header
  }

  function reset() {
    if (layer) { layer.remove(); layer = null; }
    live = null;
    if (lifted) { lifted.classList.remove("ca-lifted"); lifted = null; }
    root.style.overflow = "";
    document.body.style.paddingRight = "";
    busy = false;
  }

  // The HANDOFF FRAME, in the markup css/handoff.css (shared with the twin) expects.
  function outlined() {
    var t = document.createElement("template");
    t.innerHTML = svgText.trim();
    var svg = t.content.firstElementChild;
    return svg && svg.classList.contains("handoff-text") ? svg : null;
  }

  function loadSvg() {
    if (svgReq || !window.fetch) return;
    svgReq = fetch(SVG_URL).then(function (r) { return r.ok ? r.text() : null; }).then(function (t) {
      if (!t) return;
      svgText = t;
      // Arrived mid-animation: swap it in at the same moment of the fade.
      if (live && live.text.tagName !== "svg") {
        var svg = outlined();
        if (!svg) return;
        if (live.textFrames) {
          var a = svg.animate(live.textFrames, live.timing);
          a.currentTime = live.anims[0].currentTime;
          if (live.anims[0].playState === "paused") a.pause();
          live.anims.push(a);
        }
        live.text.replaceWith(svg);
        live.text = svg;
      }
    }).catch(function () {});
  }

  function frame() {
    var f = el("div", "handoff-frame");
    f.setAttribute("aria-hidden", "true");
    var ink = el("div", "handoff-ink");
    var text = (svgText && outlined()) || el("span", "handoff-text", "Opening the course assistant...");
    var pen = el("span", "handoff-underline");
    ink.appendChild(text); ink.appendChild(pen); f.appendChild(ink);
    return { f: f, ink: ink, text: text, pen: pen };
  }

  function go(a) {
    if (busy) return;
    busy = true;
    warm();
    var href = a.href;
    var p = pose(a), fr = frame();
    layer = fr.f;

    if (reduce && reduce.matches) {
      layer.style.opacity = "0";
      document.body.appendChild(layer);
      lockScroll();
      var fade = layer.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 150, easing: "linear", fill: "forwards" });
      live = { text: fr.text, textFrames: null, anims: [fade] };
      window.__handoff = [fade];
      fade.finished.then(function () { layer.style.opacity = ""; fade.cancel(); location.assign(href); }, function () {});
      return;
    }

    // The face of the note, carried on the growing sheet until it fades.
    var face = el("div", a.className.replace(/\bland\b/, "") + " ca-face");
    face.innerHTML = a.innerHTML;
    var tape = face.querySelector(".tape");
    if (tape) tape.remove();
    face.style.width = p.w + "px";
    face.style.height = p.h + "px";
    layer.insertBefore(face, fr.ink);

    var x0 = p.cx - p.w / 2, y0 = p.cy - p.h / 2;
    var start = { left: x0 + "px", top: y0 + "px", width: p.w + "px", height: p.h + "px" };
    function at(geo, t, shadow, offset, easing) {
      var k = { left: geo.left, top: geo.top, width: geo.width, height: geo.height, transform: t, boxShadow: shadow, offset: offset };
      if (easing) k.easing = easing;
      return k;
    }
    var rest = "0 1px 1px rgba(0,0,0,.12), 0 16px 22px -12px rgba(0,0,0,.4)";
    var up = "0 2px 4px rgba(0,0,0,.14), 0 34px 44px -14px rgba(0,0,0,.5)";
    var flat = "0 0 0 rgba(0,0,0,0), 0 0 0 -14px rgba(0,0,0,0)";
    var s = p.s.toFixed(4), r = p.rot.toFixed(3);
    var sheet = [
      at(start, "translateY(0px) rotate(" + r + "deg) scale(" + s + ")", rest, 0, "cubic-bezier(.3,.7,.4,1)"),
      at(start, "translateY(-10px) rotate(" + (p.rot * 0.45).toFixed(3) + "deg) scale(1.06)", up, 0.17, "ease-in-out"),
      at(start, "translateY(-10px) rotate(0deg) scale(1.06)", up, 0.31, EASE),
      at({ left: "0px", top: "0px", width: "100%", height: "100%" }, "translateY(0px) rotate(0deg) scale(1)", flat, 1)
    ];
    var timing = { duration: MS, easing: "linear", fill: "forwards" };

    Object.assign(layer.style, start, { transform: sheet[0].transform, boxShadow: rest });
    document.body.appendChild(layer);
    lifted = a;
    a.classList.add("ca-lifted");
    lockScroll();

    var textFrames = [{ opacity: 0, offset: 0 }, { opacity: 0, offset: 0.5 }, { opacity: 1, offset: 0.78 }, { opacity: 1, offset: 1 }];
    var anims = [
      layer.animate(sheet, timing),
      face.animate([{ opacity: 1, offset: 0 }, { opacity: 1, offset: 0.31 }, { opacity: 0, offset: 0.52 }, { opacity: 0, offset: 1 }], timing),
      fr.text.animate(textFrames, timing),
      fr.pen.animate([{ transform: "scaleX(0)", offset: 0 }, { transform: "scaleX(0)", offset: 0.6, easing: "cubic-bezier(.5,0,.3,1)" }, { transform: "scaleX(1)", offset: 1 }], timing)
    ];
    live = { text: fr.text, textFrames: textFrames, timing: timing, anims: anims };
    window.__handoff = anims;  // lets the screenshot script pause on a frame
    anims[0].finished.then(function () { settle(fr, face, anims); location.assign(href); }, function () {});
  }

  // At 650ms, swap the animated sheet for the plain, static HANDOFF FRAME,
  // the exact markup and styles the twin paints first, so the two match to
  // the device pixel while the next page loads.
  function settle(fr, face, anims) {
    anims.forEach(function (a) { a.cancel(); });  // includes a late SVG swap
    face.remove();
    ["left", "top", "width", "height", "transform", "boxShadow"].forEach(function (k) { fr.f.style[k] = ""; });
  }

  function warm() {
    // Open the connection to the twin while the visitor is still deciding.
    if (warm.done) return;
    warm.done = true;
    var l = document.createElement("link");
    l.rel = "preconnect";
    l.href = new URL(notes[0].href).origin;
    document.head.appendChild(l);
    if (document.fonts && document.fonts.load) document.fonts.load('400 32px "Kalam"').catch(function () {});
    loadSvg();
  }

  Array.prototype.forEach.call(notes, function (a) {
    a.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      go(a);
    });
    a.addEventListener("keydown", function (e) {
      if (e.key === " " || e.key === "Spacebar") { e.preventDefault(); go(a); }
    });
    a.addEventListener("pointerenter", warm);
    a.addEventListener("focus", warm);
  });

  // Coming back with the back button can restore this page exactly as it was
  // left, mid-handoff. Put the note back on the page.
  window.addEventListener("pageshow", function (e) { if (e.persisted || busy) reset(); });
})();
