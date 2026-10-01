/* Field Notebook: hand-drawn ink, scroll choreography, the docking portrait, slide piles,
   and a small robot. No libraries. Every stroke is generated with a seeded wobble so the
   page looks drawn by hand but renders the same way on every visit.

   Everything on the page is visible without this script. When it runs it marks the page
   with html.nb (so the plain-text stand-ins for charts step aside; the head script sets it
   early and takes it back if this file never arrives), draws the charts, and,
   unless the visitor prefers reduced motion, holds each .reveal block back until it
   scrolls into view. */
(function () {
  "use strict";
  window.__nb = true;
  var doc = document.documentElement;
  doc.classList.add("nb");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var STATIC = doc.classList.contains("static");
  var NS = "http://www.w3.org/2000/svg";

  /* ---------- seeded wobble ---------- */
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  var R = rng(1);
  function seed(s) { R = rng(s * 9973 + 17); }
  function J(a) { return (R() * 2 - 1) * a; }
  function f(n) { return Math.round(n * 10) / 10; }

  function E(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function lineD(x1, y1, x2, y2, w) {
    w = w == null ? 1 : w;
    var dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    var b = Math.min(5, L * 0.025) * Math.max(w, 0.4);
    return "M" + f(x1 + J(w)) + " " + f(y1 + J(w)) +
      "C" + f(x1 + dx * 0.33 + nx * J(b)) + " " + f(y1 + dy * 0.33 + ny * J(b)) + " " +
      f(x1 + dx * 0.66 + nx * J(b)) + " " + f(y1 + dy * 0.66 + ny * J(b)) + " " +
      f(x2 + J(w)) + " " + f(y2 + J(w));
  }
  function curve(pts) {
    var d = "M" + f(pts[0][0]) + " " + f(pts[0][1]);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += "C" + f(p1[0] + (p2[0] - p0[0]) / 6) + " " + f(p1[1] + (p2[1] - p0[1]) / 6) + " " +
        f(p2[0] - (p3[0] - p1[0]) / 6) + " " + f(p2[1] - (p3[1] - p1[1]) / 6) + " " + f(p2[0]) + " " + f(p2[1]);
    }
    return d;
  }
  function loopD(cx, cy, rx, ry, over, jit) {
    over = over == null ? 0.45 : over; jit = jit == null ? 0.05 : jit;
    var a0 = -2.2 + J(0.5), n = 18, pts = [], tot = Math.PI * 2 + over;
    for (var i = 0; i <= n; i++) {
      var t = a0 + (tot * i) / n, k = 1 + J(jit) + (i / n) * 0.07;
      pts.push([cx + Math.cos(t) * rx * k, cy + Math.sin(t) * ry * k]);
    }
    return curve(pts);
  }
  function arrowD(x1, y1, x2, y2, bend, head) {
    bend = bend || 0; head = head || 12;
    var mx = (x1 + x2) / 2, my = (y1 + y2) / 2, dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy) || 1;
    var cx = mx + (-dy / L) * bend, cy = my + (dx / L) * bend;
    var body = "M" + f(x1) + " " + f(y1) + "Q" + f(cx) + " " + f(cy) + " " + f(x2) + " " + f(y2);
    var ang = Math.atan2(y2 - cy, x2 - cx), a1 = ang + Math.PI * 0.8, a2 = ang - Math.PI * 0.8;
    var h = "M" + f(x2 + Math.cos(a1) * head) + " " + f(y2 + Math.sin(a1) * head) + "L" + f(x2) + " " + f(y2) +
      "L" + f(x2 + Math.cos(a2) * head * 0.85) + " " + f(y2 + Math.sin(a2) * head * 0.85);
    return [body, h];
  }
  function zigzag(x, y, w, h, step) {
    step = step || 7;
    var d = "M" + f(x + 2) + " " + f(y + h - 2), up = true;
    for (var xx = x + step * 0.5; xx < x + w - 1; xx += step * 0.5) {
      d += "L" + f(Math.min(xx, x + w - 2) + J(0.8)) + " " + f(up ? y + 2 + J(1.2) : y + h - 2 + J(1.2));
      up = !up;
    }
    return d;
  }
  function ink(svg, d, o) {
    o = o || {};
    var p = E("path", { d: d, class: "ink" + (o.cls ? " " + o.cls : ""), "stroke-width": o.w || 2.2 }, svg);
    if (o.color) p.style.color = o.color;
    if (o.op) p.setAttribute("stroke-opacity", o.op);
    if (o.cap) p.style.strokeLinecap = o.cap;
    p.style.setProperty("--d", (o.d || 0) + "s");
    if (o.dur) p.style.setProperty("--dur", o.dur + "s");
    return p;
  }
  function measure(root) {
    var ps = root.querySelectorAll(".ink");
    for (var i = 0; i < ps.length; i++) {
      var L = Math.ceil(ps[i].getTotalLength()) + 2;
      ps[i].style.setProperty("--len", L);
    }
  }
  function text(svg, x, y, str, o) {
    o = o || {};
    var t = E("text", { x: x, y: y, class: "fade" }, svg);
    t.textContent = str;
    t.style.font = o.font || "700 18px Kalam, cursive";
    t.style.fill = o.color || "currentColor";
    if (o.anchor) t.setAttribute("text-anchor", o.anchor);
    t.style.setProperty("--d", (o.d || 0) + "s");
    return t;
  }
  function svgFor(el, w, h) {
    el.innerHTML = "";
    el.setAttribute("viewBox", "0 0 " + w + " " + h);
    el.setAttribute("aria-hidden", "true");
    el.setAttribute("focusable", "false");
    return el;
  }
  function num(el, k, dflt) { var v = parseFloat(el.dataset[k]); return isNaN(v) ? dflt : v; }

  /* ---------- text overlays: underlines and circles ---------- */
  function overlays() {
    var us = document.querySelectorAll(".u");
    for (var i = 0; i < us.length; i++) {
      var el = us[i], old = el.querySelector(":scope > svg.ov");
      if (old) old.remove();
      seed(200 + i);
      var w = el.offsetWidth, h = el.offsetHeight, sw = num(el, "w", 3), dl = num(el, "d", 0.3);
      var svg = E("svg", { class: "ov", width: w + 10, height: 16, viewBox: "0 0 " + (w + 10) + " 16", "aria-hidden": "true" });
      svg.style.left = "-5px"; svg.style.bottom = "-0.42em";
      if (el.dataset.color) svg.style.color = el.dataset.color;
      ink(svg, lineD(3, 6 + J(1), w + 7, 5 + J(2), 0.8), { w: sw, d: dl, dur: 0.6 });
      if (el.classList.contains("u2")) ink(svg, lineD(10, 11 + J(1), w - 4, 10 + J(1.5), 0.8), { w: sw * 0.8, d: dl + 0.45, dur: 0.5 });
      el.appendChild(svg); measure(svg);
    }
    var cs = document.querySelectorAll(".circ");
    for (var j = 0; j < cs.length; j++) {
      var c = cs[j], o2 = c.querySelector(":scope > svg.ov");
      if (o2) o2.remove();
      seed(400 + j);
      var cw = c.offsetWidth + 18, ch = c.offsetHeight + 14;
      var s2 = E("svg", { class: "ov", width: cw, height: ch, viewBox: "0 0 " + cw + " " + ch, "aria-hidden": "true" });
      s2.style.left = "-9px"; s2.style.top = "-7px";
      if (c.dataset.color) s2.style.color = c.dataset.color;
      ink(s2, loopD(cw / 2, ch / 2, cw / 2 - 3, ch / 2 - 3, 0.5, 0.04), { w: num(c, "w", 2.4), d: num(c, "d", 0.5), dur: 0.9 });
      c.appendChild(s2); measure(s2);
    }
    var as = document.querySelectorAll("svg[data-arrow]");
    for (var k = 0; k < as.length; k++) {
      var a = as[k], v = a.dataset.arrow.split(/[ ,]+/).map(Number);
      seed(600 + k);
      var W = +a.getAttribute("width"), H = +a.getAttribute("height");
      svgFor(a, W, H);
      var ad = arrowD(v[0], v[1], v[2], v[3], v[4] || 0, v[5] || 11), dl2 = num(a, "d", 0.6);
      ink(a, ad[0], { w: num(a, "w", 2.2), d: dl2, dur: 0.6 });
      ink(a, ad[1], { w: num(a, "w", 2.2), d: dl2 + 0.55, dur: 0.25 });
      measure(a);
    }
  }

  /* ---------- charts ---------- */
  var charts = {
    tally: function (svg) {
      var n = num(svg, "n", 4), g = Math.floor(n / 5), r = n % 5, base = num(svg, "d", 0.3);
      var W = g * 64 + r * 13 + 10, H = 62, x = 8, k = 0;
      svgFor(svg, W, H);
      svg.style.width = (W * 0.82) + "px";
      function stroke(x1, y1, x2, y2) { ink(svg, lineD(x1, y1, x2, y2, 0.9), { w: 3, d: base + k++ * 0.09, dur: 0.22 }); }
      for (var i = 0; i < g; i++) {
        for (var s = 0; s < 4; s++) stroke(x + s * 12 + J(1.5), 6 + J(2), x + s * 12 + J(2), 56 + J(2));
        stroke(x - 6, 44 + J(2), x + 44, 14 + J(2));
        x += 64;
      }
      for (var t = 0; t < r; t++) stroke(x + t * 13 + J(1.5), 6 + J(2), x + t * 13 + J(2), 56 + J(2));
    },
    award: function (svg) {
      svgFor(svg, 96, 70);
      svg.style.width = "80px";
      var b = num(svg, "d", 0.3), cx = 34, cy = 30, pts = [];
      ink(svg, loopD(cx, cy, 25, 25, 0.4, 0.04), { w: 2.6, d: b, dur: 0.7, color: "var(--red)" });
      for (var i = 0; i <= 10; i++) {
        var a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? 6.5 : 15;
        pts.push((i ? "L" : "M") + f(cx + Math.cos(a) * rr + J(0.8)) + " " + f(cy + Math.sin(a) * rr + J(0.8)));
      }
      ink(svg, pts.join(""), { w: 2.2, d: b + 0.6, dur: 0.6, color: "var(--red)" });
      ink(svg, lineD(24, 52, 16, 68, 0.6), { w: 2.6, d: b + 1.1, dur: 0.2, color: "var(--red)" });
      ink(svg, lineD(44, 52, 52, 68, 0.6), { w: 2.6, d: b + 1.2, dur: 0.2, color: "var(--red)" });
      text(svg, 66, 20, "!", { d: b + 1.3, color: "var(--red)", font: "700 26px Kalam, cursive" });
    },
    kmeans: function (svg) {
      var W = 420, H = 300; svgFor(svg, W, H); seed(42);
      var b = num(svg, "d", 0.5);
      var ax = arrowD(34, 272, 404, 270, 2, 10), ay = arrowD(34, 272, 32, 22, -2, 10);
      ink(svg, ax[0], { w: 2, d: b, dur: 0.6 }); ink(svg, ax[1], { w: 2, d: b + 0.5, dur: 0.2 });
      ink(svg, ay[0], { w: 2, d: b, dur: 0.6 }); ink(svg, ay[1], { w: 2, d: b + 0.5, dur: 0.2 });
      var C = [[112, 196, "var(--pen)"], [226, 92, "var(--red)"], [326, 204, "#2e7d4f"]], pts = [];
      C.forEach(function (c, ci) {
        for (var i = 0; i < 13; i++) {
          var u = R() || 0.01, v = R(), m = Math.sqrt(-2 * Math.log(u)) * 22;
          pts.push([c[0] + m * Math.cos(2 * Math.PI * v), c[1] + m * Math.sin(2 * Math.PI * v) * 0.85, c[2]]);
        }
      });
      pts.sort(function (a, b2) { return a[0] - b2[0]; });
      pts.forEach(function (p, i) {
        var d = E("circle", { cx: f(p[0]), cy: f(p[1]), r: 5, class: "dot" }, svg);
        d.style.fill = p[2]; d.style.fillOpacity = 0.85;
        d.style.setProperty("--d", (b + 0.7 + i * 0.035) + "s");
      });
      var t0 = b + 0.8 + pts.length * 0.035;
      C.forEach(function (c, i) {
        ink(svg, loopD(c[0], c[1] - 2, 58, 48, 0.5, 0.06), { w: 2, d: t0 + i * 0.35, dur: 0.7, color: c[2], op: 0.9 });
        ink(svg, lineD(c[0] - 8, c[1] - 8, c[0] + 8, c[1] + 8, 0.5), { w: 3.4, d: t0 + 1.2 + i * 0.1, dur: 0.15 });
        ink(svg, lineD(c[0] + 8, c[1] - 8, c[0] - 8, c[1] + 8, 0.5), { w: 3.4, d: t0 + 1.3 + i * 0.1, dur: 0.15 });
      });
      text(svg, 312, 74, "k = 3", { d: t0 + 1.6, color: "var(--pen)", font: "700 28px Kalam, cursive" });
      var ar = arrowD(318, 84, 286, 112, 8, 9);
      ink(svg, ar[0], { w: 2, d: t0 + 1.8, dur: 0.3, color: "var(--pen)" });
      ink(svg, ar[1], { w: 2, d: t0 + 2.1, dur: 0.15, color: "var(--pen)" });
    },
    timeline: function (svg) {
      var W = Math.max(280, svg.parentNode.clientWidth), narrow = W < 520;
      var rows = JSON.parse(svg.dataset.rows), y0 = 2012, y1 = 2026.9, rowH = narrow ? 50 : 52;
      var L = 6, Rr = 26, H = rows.length * rowH + 52;
      svgFor(svg, W, H); seed(77);
      svg.setAttribute("width", W); svg.setAttribute("height", H);
      function X(y) { return L + ((y - y0) / (y1 - y0)) * (W - L - Rr); }
      var b = num(svg, "d", 0.4);
      rows.forEach(function (r, i) {
        var y = 14 + i * rowH, xs = X(r[1]), xe = X(r[2] || 2026.75), now = !r[2];
        var d = b + i * 0.32, fs = narrow ? 16 : 17.5;
        var tw = r[0].length * fs * 0.47, tx = xs, anchor = "start";
        if (tx + tw > W - 4) { tx = Math.min(xe, W - 6); anchor = "end"; }
        text(svg, tx, y + 13, r[0], { d: d, font: "700 " + fs + "px Kalam, cursive", color: "var(--ink)", anchor: anchor });
        ink(svg, lineD(xs + 4, y + 30, xe - (now ? 6 : 4), y + 30 + J(1.5), 0.6), { w: 13, d: d + 0.1, dur: 0.7, color: r[3], op: 0.75 });
        if (now) {
          var a = arrowD(xe - 8, y + 30, xe + 14, y + 30, 0, 8);
          ink(svg, a[0], { w: 2.2, d: d + 0.75, dur: 0.15 }); ink(svg, a[1], { w: 2.2, d: d + 0.85, dur: 0.15 });
        }
      });
      var ay = H - 30;
      ink(svg, lineD(L, ay, W - 8, ay, 0.6), { w: 2, d: b - 0.2, dur: 0.8 });
      for (var yr = y0; yr <= 2026; yr++) {
        var x = X(yr), major = (yr - y0) % (narrow ? 4 : 2) === 0;
        ink(svg, lineD(x, ay - (major ? 7 : 4), x, ay + (major ? 7 : 4), 0.3), { w: 1.6, d: b + (yr - y0) * 0.03, dur: 0.1 });
        if (major) text(svg, x, ay + 24, String(yr), { anchor: "middle", d: b + 0.3, font: "500 12px 'IBM Plex Mono', monospace", color: "var(--ink-2)" });
      }
      text(svg, W - 2, ay - 12, "now", { anchor: "end", d: b + 2.2, font: "700 16px Kalam, cursive", color: "var(--red)" });
    },
    bar: function (svg) {
      var W = Math.max(60, svg.getBoundingClientRect().width || svg.parentNode.clientWidth), H = 34, v = num(svg, "v", 1), max = num(svg, "max", 1);
      svgFor(svg, W, H); svg.setAttribute("width", W); svg.setAttribute("height", H);
      seed(900 + Math.round(v * 13) + (svg.dataset.i | 0) * 7);
      var lab = (svg.dataset.label || v) + "", pad = lab.length * 11 + 14;
      var bw = Math.max(10, (W - pad) * (v / max)), d = num(svg, "d", 0.3), color = svg.dataset.color || "var(--pen)";
      ink(svg, zigzag(3, 6, bw - 4, H - 12, 7), { w: 2.4, d: d + 0.25, dur: 0.6 + bw / 900, color: color, op: 0.55 });
      ink(svg, lineD(2, 5, bw, 4 + J(1), 0.5) + lineD(bw, 4, bw + J(1), H - 4, 0.5).replace("M", "L") +
        lineD(bw, H - 4, 2, H - 5, 0.5).replace("M", "L") + "Z", { w: 2, d: d, dur: 0.5 });
      text(svg, bw + 10, H / 2 + 8, lab, { d: d + 0.6, color: "var(--red)", font: "700 22px Kalam, cursive" });
    },
    icon: function (svg) {
      var kind = svg.dataset.icon, b = num(svg, "d", 0.4); svgFor(svg, 120, 80); seed(kind.length * 31);
      var o = function (dd, w) { return { w: w || 2, d: b + dd, dur: 0.35 }; };
      if (kind === "net") {
        var L1 = [18, 40, 62], L2 = [12, 31, 49, 68], L3 = [28, 52], k = 0;
        L1.forEach(function (a) { L2.forEach(function (c) { ink(svg, lineD(22, a, 56, c, 0.3), o(0.02 * k++, 1.1)); }); });
        L2.forEach(function (a) { L3.forEach(function (c) { ink(svg, lineD(64, a, 96, c, 0.3), o(0.02 * k++, 1.1)); }); });
        L1.forEach(function (y, i) { ink(svg, loopD(18, y, 5, 5, 0.3), o(0.5 + i * 0.05)); });
        L2.forEach(function (y, i) { ink(svg, loopD(60, y, 5, 5, 0.3), o(0.6 + i * 0.05)); });
        L3.forEach(function (y, i) { ink(svg, loopD(100, y, 6, 6, 0.3), o(0.75 + i * 0.05, 2.4)); });
      } else if (kind === "vision") {
        ink(svg, lineD(8, 10, 70, 9) + lineD(70, 9, 71, 66).replace("M", "L") + lineD(71, 66, 8, 67).replace("M", "L") + "Z", o(0, 2));
        ink(svg, "M12 60 L30 34 L42 48 L52 38 L67 60", o(0.4, 2));
        ink(svg, loopD(54, 22, 6, 6, 0.3), o(0.6));
        [[88, 18], [108, 30], [92, 50], [110, 62]].forEach(function (p, i, A) {
          if (i) ink(svg, lineD(A[i - 1][0], A[i - 1][1], p[0], p[1], 0.3), o(0.7 + i * 0.08, 1.4));
          ink(svg, loopD(p[0], p[1], 4.5, 4.5, 0.3), o(0.8 + i * 0.08));
        });
        ink(svg, lineD(108, 30, 110, 62, 0.3), o(1.1, 1.4));
      } else if (kind === "org") {
        var box = function (x, y, w, h, dd) {
          ink(svg, lineD(x, y, x + w, y) + lineD(x + w, y, x + w, y + h).replace("M", "L") + lineD(x + w, y + h, x, y + h).replace("M", "L") + "Z", o(dd));
        };
        box(44, 6, 32, 20, 0);
        ink(svg, lineD(60, 26, 60, 38, 0.3), o(0.3)); ink(svg, lineD(18, 38, 102, 38, 0.4), o(0.35));
        [18, 60, 102].forEach(function (x, i) { ink(svg, lineD(x, 38, x, 48, 0.3), o(0.5 + i * 0.05)); box(x - 14, 48, 28, 20, 0.6 + i * 0.1); });
        ink(svg, "M51 16 l4 4 l9 -9", o(1, 2.4)).style.color = "var(--red)";
      } else if (kind === "scatter") {
        ink(svg, lineD(10, 72, 112, 71, 0.4), o(0, 1.6)); ink(svg, lineD(10, 72, 11, 6, 0.4), o(0.1, 1.6));
        [[30, 52, 0], [36, 44, 0], [26, 40, 0], [70, 26, 1], [78, 34, 1], [66, 20, 1], [96, 54, 2], [90, 60, 2], [102, 48, 2]].forEach(function (p, i) {
          var c = E("circle", { cx: p[0], cy: p[1], r: 3.6, class: "dot" }, svg);
          c.style.fill = ["var(--pen)", "var(--red)", "#2e7d4f"][p[2]]; c.style.setProperty("--d", (b + 0.3 + i * 0.06) + "s");
        });
        ink(svg, loopD(72, 27, 16, 14, 0.4), o(1, 1.6)).style.color = "var(--red)";
      } else if (kind === "bars") {
        ink(svg, lineD(8, 72, 112, 72, 0.4), o(0, 1.8));
        [[14, 40], [36, 22], [58, 50], [80, 12], [100, 30]].forEach(function (r, i) {
          ink(svg, lineD(r[0], 72, r[0], r[1], 0.3) + lineD(r[0], r[1], r[0] + 14, r[1], 0.3).replace("M", "L") + lineD(r[0] + 14, r[1], r[0] + 14, 72, 0.3).replace("M", "L"), o(0.2 + i * 0.1, 1.8));
        });
        ink(svg, "M80 8 l7 -6 l7 6", o(0.9, 2)).style.color = "var(--red)";
      } else if (kind === "agent") {
        // a chat bubble with an agent at work, and a spark where it acts
        ink(svg, "M14 12 Q10 12 10 18 L10 46 Q10 52 16 52 L30 52 L24 68 L44 52 L76 52 Q82 52 82 46 L82 18 Q82 12 76 12 Z", o(0, 2));
        [30, 46, 62].forEach(function (x, i) {
          var c = E("circle", { cx: x, cy: 32, r: 3.6, class: "dot" }, svg);
          c.style.fill = "var(--ink)"; c.style.setProperty("--d", (b + 0.6 + i * 0.15) + "s");
        });
        var ar = arrowD(86, 30, 102, 22, 6, 6); ink(svg, ar[0], o(0.9, 1.8)); ink(svg, ar[1], o(1.05, 1.8));
        ink(svg, "M108 4 L108 20 M100 12 L116 12 M102.5 6.5 L113.5 17.5 M113.5 6.5 L102.5 17.5", o(1.2, 2)).style.color = "var(--red)";
      } else if (kind === "explore") {
        // a line chart with a magnifying glass over the interesting bit
        ink(svg, lineD(6, 72, 112, 71, 0.4), o(0, 1.6)); ink(svg, lineD(6, 72, 7, 8, 0.4), o(0.1, 1.6));
        ink(svg, curve([[10, 60], [24, 52], [36, 56], [48, 40], [58, 44], [70, 22], [82, 34], [96, 30], [110, 38]]), o(0.25, 2));
        ink(svg, loopD(70, 30, 15, 15, 0.4), o(0.8, 2.4)).style.color = "var(--red)";
        ink(svg, lineD(81, 41, 96, 58, 0.3), o(1.1, 3.6)).style.color = "var(--red)";
      } else if (kind === "bell") {
        var bp = []; for (var bi = 0; bi <= 24; bi++) { var bx = 8 + bi * 4.4; bp.push([bx, 70 - 56 * Math.exp(-Math.pow((bx - 60) / 18, 2)) + J(0.5)]); }
        ink(svg, lineD(6, 71, 114, 71, 0.4), o(0, 1.6));
        ink(svg, curve(bp), o(0.2, 2.2));
        [36, 48, 60, 72, 84].forEach(function (x, i) {
          var c = E("circle", { cx: x, cy: 70 - 56 * Math.exp(-Math.pow((x - 60) / 18, 2)) - 7, r: 3.4, class: "dot" }, svg);
          c.style.fill = "var(--red)"; c.style.setProperty("--d", (b + 0.6 + i * 0.12) + "s");
        });
      } else if (kind === "flow") {
        var bx2 = function (x, dd) { ink(svg, lineD(x, 26, x + 22, 26) + lineD(x + 22, 26, x + 22, 50).replace("M", "L") + lineD(x + 22, 50, x, 50).replace("M", "L") + "Z", o(dd)); };
        bx2(4, 0); bx2(48, 0.3); bx2(92, 0.6);
        [[28, 46], [72, 90]].forEach(function (a, i) { var ar = arrowD(a[0], 38, a[1], 38, 0, 6); ink(svg, ar[0], o(0.2 + i * 0.3, 1.8)); ink(svg, ar[1], o(0.3 + i * 0.3, 1.8)); });
        ink(svg, "M98 44 L103 34 L108 40 L112 30", o(0.9, 2)).style.color = "var(--red)";
      } else if (kind === "bowl") {
        var pts = []; for (var i = 0; i <= 20; i++) { var x = 8 + i * 5.2; pts.push([x, 72 - Math.pow((x - 60) / 52, 2) * 60 + J(0.6)]); }
        ink(svg, curve(pts), o(0, 2.2));
        var steps = [16, 30, 42, 51, 57];
        steps.forEach(function (x, i) {
          var y = 72 - Math.pow((x - 60) / 52, 2) * 60 - 6;
          var c = E("circle", { cx: x, cy: y, r: 4, class: "dot" }, svg); c.style.fill = "var(--red)"; c.style.setProperty("--d", (b + 0.5 + i * 0.18) + "s");
        });
        text(svg, 76, 22, "∇", { d: b + 1.4, color: "var(--pen)", font: "700 22px Kalam, cursive" });
      }
    },
    play: function (svg) {
      svgFor(svg, 120, 120); seed(5); var b = num(svg, "d", 0.6);
      var tri = E("path", { d: "M50 38 L86 60 L50 84 Z", class: "fade" }, svg);
      tri.style.fill = "var(--red)"; tri.style.fillOpacity = 0.92; tri.style.setProperty("--d", (b + 0.9) + "s");
      ink(svg, loopD(62, 61, 48, 46, 0.5, 0.04), { w: 4, d: b, dur: 0.8, color: "var(--red)" });
      ink(svg, lineD(50, 38, 87, 60, 0.6) + lineD(87, 60, 50, 84, 0.6).replace("M", "L") + lineD(50, 84, 50, 38, 0.6).replace("M", "L"), { w: 3, d: b + 0.5, dur: 0.5, color: "var(--ink)" });
    },
    gens: function (svg) {
      var W = 540, H = 190; svgFor(svg, W, H); seed(8);
      var b = num(svg, "d", 0.4), fw = 140, fh = 100, xs = [8, 200, 392], labels = ["YOLO boxes", "ResNet labels", "multimodal JSON"];
      function rect(x, y, w, h, o) { return ink(svg, lineD(x, y, x + w, y, 0.6) + lineD(x + w, y, x + w, y + h, 0.6).replace("M", "L") + lineD(x + w, y + h, x, y + h, 0.6).replace("M", "L") + "Z", o); }
      xs.forEach(function (x, i) {
        var d = b + i * 0.7, y = 22;
        rect(x, y, fw, fh, { w: 2.2, d: d, dur: 0.5 });
        if (i < 2) {
          ink(svg, lineD(x + 10, y + 50, x + fw - 10, y + 50, 0.4), { w: 1.6, d: d + 0.2, dur: 0.25 });
          ink(svg, lineD(x + 10, y + 86, x + fw - 10, y + 86, 0.4), { w: 1.6, d: d + 0.25, dur: 0.25 });
          [[18, 28, 18, 22], [44, 22, 16, 28], [66, 30, 22, 20], [96, 24, 16, 26], [20, 66, 24, 20], [52, 60, 16, 26], [80, 64, 26, 22], [112, 62, 14, 24]].forEach(function (r, k) {
            rect(x + r[0], y + r[1], r[2], r[3], { w: 1.4, d: d + 0.3 + k * 0.04, dur: 0.2 });
          });
        }
        if (i === 0) {
          rect(x + 40, y + 16, 22, 38, { w: 2.4, d: d + 0.7, dur: 0.3, color: "var(--red)" });
          rect(x + 76, y + 54, 34, 36, { w: 2.4, d: d + 0.8, dur: 0.3, color: "var(--red)" });
        } else if (i === 1) {
          ink(svg, "M" + (x + 84) + " " + (y + 8) + "h46v18h-46l-8 -9z", { w: 2.2, d: d + 0.7, dur: 0.4, color: "var(--pen)" });
          text(svg, x + 106, y + 22, "label", { anchor: "middle", d: d + 0.9, color: "var(--pen)", font: "700 13px Kalam, cursive" });
        } else {
          text(svg, x + 14, y + 30, "{", { d: d + 0.3, color: "var(--ink)", font: "500 18px 'IBM Plex Mono', monospace" });
          ["\"restock\": [", "  \"...\"", "]"].forEach(function (l, k) {
            text(svg, x + 24, y + 50 + k * 18, l, { d: d + 0.4 + k * 0.15, color: k === 0 ? "var(--red)" : "var(--ink-2)", font: "500 13px 'IBM Plex Mono', monospace" });
          });
          text(svg, x + 14, y + 96, "}", { d: d + 0.8, color: "var(--ink)", font: "500 18px 'IBM Plex Mono', monospace" });
        }
        text(svg, x + fw / 2, y + fh + 30, labels[i], { anchor: "middle", d: d + 0.5, color: "var(--ink)", font: "700 18px Kalam, cursive" });
        if (i < 2) {
          var a = arrowD(x + fw + 10, y + 50, x + fw + 44, y + 48, -6, 9);
          ink(svg, a[0], { w: 2.2, d: d + 0.6, dur: 0.25, color: "var(--red)" }); ink(svg, a[1], { w: 2.2, d: d + 0.8, dur: 0.15, color: "var(--red)" });
        }
      });
    },
    check: function (svg) {
      svgFor(svg, 34, 34); seed(+svg.dataset.d * 10);
      var b = num(svg, "d", 0.5);
      ink(svg, lineD(4, 8, 28, 7, 0.5) + lineD(28, 7, 29, 30, 0.5).replace("M", "L") + lineD(29, 30, 5, 29, 0.5).replace("M", "L") + "Z", { w: 2, d: b, dur: 0.4 });
      ink(svg, "M8 16 Q12 20 15 26 Q22 10 34 0", { w: 3.2, d: b + 0.35, dur: 0.35, color: "var(--red)" });
    },
    ring: function (svg) {
      svgFor(svg, 60, 60); seed(3);
      ink(svg, loopD(30, 30, 27, 27, 0.6, 0.03), { w: 2.2, d: 0, dur: 0.6 });
    }
  };

  function drawCharts(onlyResponsive) {
    var els = document.querySelectorAll("svg[data-chart]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i], kind = el.dataset.chart;
      if (onlyResponsive && kind !== "timeline" && kind !== "bar") continue;
      seed(i + 1);
      if (charts[kind]) { charts[kind](el); measure(el); }
    }
  }

  /* ---------- count-ups ---------- */
  function countUp(el) {
    var to = parseInt(el.dataset.to, 10), from = parseInt(el.dataset.from || "0", 10);
    if (STATIC || isNaN(to)) { el.textContent = el.dataset.final || to; return; }
    var t0 = null, dur = 1100 + Math.min(900, Math.abs(to - from) * 60), delay = parseFloat(el.dataset.d || "0.3") * 1000;
    function step(ts) {
      if (t0 === null) t0 = ts + delay;
      var p = Math.max(0, Math.min(1, (ts - t0) / dur)), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    // never leave a wrong number on the page if frames are throttled
    setTimeout(function () { el.textContent = to; }, delay + dur + 400);
  }

  /* ---------- reveal choreography ---------- */
  function reveal(el) {
    el.classList.add("drawn");
    var cs = el.querySelectorAll(".count");
    for (var i = 0; i < cs.length; i++) if (!cs[i].dataset.done) { cs[i].dataset.done = 1; countUp(cs[i]); }
  }
  function arm() {
    var rs = document.querySelectorAll(".reveal");
    if (STATIC || !("IntersectionObserver" in window)) {
      for (var i = 0; i < rs.length; i++) rs[i].classList.add("drawn");
      return;
    }
    var cs = document.querySelectorAll(".reveal .count");
    for (var c = 0; c < cs.length; c++) cs[c].textContent = cs[c].dataset.from || "0";
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -14% 0px", threshold: 0 });
    for (var j = 0; j < rs.length; j++) io.observe(rs[j]);
    // Belt and braces: a plain geometry sweep, so nothing can stay hidden if the observer
    // never fires. Anything in view (or already scrolled past) gets drawn.
    function sweep() {
      var vh = window.innerHeight, left = document.querySelectorAll(".reveal:not(.drawn)");
      for (var k = 0; k < left.length; k++) {
        var r = left[k].getBoundingClientRect();
        if (r.top < vh * 0.86 && left[k].offsetParent !== null) { reveal(left[k]); io.unobserve(left[k]); }
      }
    }
    var st = null;
    window.addEventListener("scroll", function () { if (!st) st = setTimeout(function () { st = null; sweep(); }, 120); }, { passive: true });
    window.addEventListener("load", sweep);
    setTimeout(sweep, 1200);
  }

  /* ---------- the portrait peels off and docks in the header ---------- */
  function dock() {
    var bar = document.querySelector(".topbar");
    var morph = document.querySelector(".portrait-morph");
    if (!bar) return;
    if (!morph) {
      var tick = function () { bar.classList.toggle("docked", window.scrollY > 40); };
      window.addEventListener("scroll", tick, { passive: true }); tick();
      return;
    }
    var badge = bar.querySelector(".badge"), photo = morph.querySelector(".photo"), hed = morph.querySelector(".hedcut");
    var peel = morph.querySelectorAll(".tape, figcaption"), cap = morph.querySelector("figcaption");
    var baseRot = parseFloat(getComputedStyle(morph).getPropertyValue("--rot")) || 3;
    var nat = null, queued = false;
    function measureM() {
      morph.style.transform = "none"; morph.style.clipPath = "";
      var r = morph.getBoundingClientRect();
      nat = { left: r.left, top: r.top + window.scrollY, w: r.width, h: r.height };
      morph.style.transform = "";
      render();
    }
    function render() {
      queued = false;
      if (!nat) return;
      var end = Math.max(160, nat.top + nat.h * 0.55 - bar.offsetHeight);
      var p = Math.min(1, Math.max(0, window.scrollY / end));
      var docked = p >= 1;
      bar.classList.toggle("docked", docked);
      if (reduce || STATIC) { morph.style.visibility = ""; return; }
      var e = p * p * (3 - 2 * p);
      var br = badge.getBoundingClientRect(), mini = br.width || 46;
      var tx = br.left + br.width / 2 - mini / 2, ty = br.top + br.height / 2 - mini / 2;
      var s = 1 + (mini / nat.w - 1) * e;
      var x = (tx - nat.left) * e, y = (ty - (nat.top - window.scrollY)) * e;
      var rot = baseRot * (1 - e) - 10 * Math.sin(Math.PI * Math.min(1, e * 1.4));
      morph.style.transform = "translate(" + f(x) + "px," + f(y) + "px) rotate(" + f(rot) + "deg) scale(" + s.toFixed(4) + ")";
      var clipB = Math.max(0, nat.h - nat.w) * e;
      morph.style.clipPath = "inset(0 0 " + f(clipB) + "px 0 round " + f((nat.w / 2) * e) + "px)";
      morph.style.boxShadow = "0 " + f(18 + 30 * Math.sin(Math.PI * e)) + "px " + f(30 + 30 * Math.sin(Math.PI * e)) + "px -14px rgba(0,0,0," + (0.45 + 0.2 * Math.sin(Math.PI * e)).toFixed(2) + ")";
      photo.style.filter = "grayscale(" + Math.min(1, p * 1.6).toFixed(2) + ") contrast(" + (1 + 0.15 * e).toFixed(2) + ")";
      hed.style.opacity = Math.min(1, Math.max(0, (p - 0.2) / 0.6)).toFixed(2);
      for (var i = 0; i < peel.length; i++) peel[i].style.opacity = Math.max(0, 1 - p * 3).toFixed(2);
      morph.style.visibility = docked ? "hidden" : "";
    }
    function queue() {
      if (queued) return;
      queued = true; requestAnimationFrame(render);
      setTimeout(function () { if (queued) render(); }, 80);
    }
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", measureM);
    measureM();
    if (document.readyState !== "complete") window.addEventListener("load", measureM);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureM);
  }

  /* ---------- a small robot pops up to say hi, once per visit ----------
     It asks for nothing and links nowhere: it bounces up, says hello, waves, blinks,
     and tucks itself back out of view. A click makes it hop and wave again. The whole
     figure is decorative, so it is hidden from assistive technology. */
  function robot() {
    if (reduce) return;
    var seen = false;
    try { seen = sessionStorage.getItem("nb-robot") === "1"; } catch (e) { /* storage blocked */ }
    if (seen) return;
    var bot = document.createElement("div");
    bot.className = "bot reveal"; bot.hidden = true;
    bot.setAttribute("aria-hidden", "true");
    bot.innerHTML =
      '<p class="bubble">Hi!</p>' +
      '<svg viewBox="0 0 132 150" aria-hidden="true">' +
      '<g class="body-fill fade" style="--d:.35s">' +
      '<rect x="40" y="78" width="54" height="72" rx="12" fill="#f6c453"/>' +
      '<rect x="32" y="22" width="68" height="52" rx="16" fill="#9ccbea"/>' +
      '<circle cx="66" cy="8" r="6" fill="#b8352a"/><circle cx="52" cy="62" r="4" fill="#f5b5c8"/><circle cx="82" cy="62" r="4" fill="#f5b5c8"/>' +
      '<rect x="50" y="92" width="34" height="24" rx="4" fill="#fffefa"/>' +
      '</g>' +
      '<g class="eyes fade" style="--d:.5s"><g class="eye"><circle cx="54" cy="46" r="7" fill="#fff" stroke="#1d2633" stroke-width="2.5"/><circle cx="56" cy="47" r="3.4" fill="#1d2633"/></g>' +
      '<g class="eye"><circle cx="80" cy="46" r="7" fill="#fff" stroke="#1d2633" stroke-width="2.5"/><circle cx="82" cy="47" r="3.4" fill="#1d2633"/></g></g>' +
      '<g class="lines" style="color:#1d2633"></g>' +
      '<g class="arm"><g class="arm-lines" style="color:#1d2633"></g><circle class="fade" style="--d:.5s" cx="122" cy="54" r="8" fill="#9ccbea"/></g>' +
      "</svg>" +
      '<span class="bot-hit"></span>';
    document.body.appendChild(bot);
    var g = bot.querySelector(".lines"), arm = bot.querySelector(".arm-lines");
    seed(11);
    var rr = function (x, y, w, h, r) { return "M" + (x + r) + " " + y + "H" + (x + w - r) + "Q" + (x + w) + " " + y + " " + (x + w) + " " + (y + r) + "V" + (y + h - r) + "Q" + (x + w) + " " + (y + h) + " " + (x + w - r) + " " + (y + h) + "H" + (x + r) + "Q" + x + " " + (y + h) + " " + x + " " + (y + h - r) + "V" + (y + r) + "Q" + x + " " + y + " " + (x + r) + " " + y + "Z"; };
    ink(g, rr(32, 22, 68, 52, 16), { w: 3, d: 0, dur: 0.6 });
    ink(g, lineD(66, 22, 66, 14, 0.4), { w: 3, d: 0.1, dur: 0.15 });
    ink(g, loopD(66, 8, 6, 6, 0.3, 0.02), { w: 2.6, d: 0.2, dur: 0.25 });
    ink(g, "M56 64 Q66 71 76 64", { w: 2.6, d: 0.45, dur: 0.25 });
    ink(g, rr(40, 78, 54, 80, 12), { w: 3, d: 0.15, dur: 0.6 });
    ink(g, rr(50, 92, 34, 24, 4), { w: 2.2, d: 0.4, dur: 0.3 });
    ink(g, "M54 110 L60 103 L66 106 L73 98 L80 100", { w: 2.2, d: 0.6, dur: 0.3, color: "#b8352a" });
    ink(g, "M40 96 Q26 104 24 120", { w: 3, d: 0.35, dur: 0.3 });
    ink(g, loopD(24, 124, 6, 6, 0.3, 0.02), { w: 2.6, d: 0.5, dur: 0.2 });
    ink(arm, "M94 94 Q118 88 121 62", { w: 3.4, d: 0.35, dur: 0.3 });
    ink(arm, loopD(122, 54, 8, 8, 0.3, 0.02), { w: 2.6, d: 0.5, dur: 0.2 });
    measure(bot);
    function tuck() {
      bot.classList.remove("out"); bot.classList.add("tuck");
      setTimeout(function () { bot.remove(); }, 700);
    }
    var leave = null;
    // A click: a happy hop and another wave, and a little more time on stage.
    bot.addEventListener("click", function () {
      if (!bot.classList.contains("out")) return;
      bot.classList.remove("hop", "rewave"); void bot.offsetWidth;
      bot.classList.add("hop", "rewave");
      clearTimeout(leave); leave = setTimeout(tuck, 4200);
    });
    // Pick a corner that does not cover the nav or any call to action; if both are
    // busy, try again a little later, and give up quietly after a few tries.
    var CTA = "nav a, .sticky, .sticky-cta, .go, .btn, .stat, .icard, .video, .thumb, .proj-strip button, summary, .country-list button, .map-pop, .tprint";
    function freeCorner() {
      var vw = window.innerWidth, vh = window.innerHeight, phone = vw < 761;
      var zw = phone ? 270 : 360, zh = phone ? 190 : 230;
      var zones = { br: [vw - zw, vh - zh, vw, vh], bl: [0, vh - zh, zw, vh] };
      var order = ["br", "bl"], els = document.querySelectorAll(CTA);
      for (var i = 0; i < order.length; i++) {
        var z = zones[order[i]], hit = false;
        for (var k = 0; k < els.length && !hit; k++) {
          var r = els[k].getBoundingClientRect();
          if (r.width && r.right > z[0] && r.left < z[2] && r.bottom > z[1] && r.top < z[3]) hit = true;
        }
        if (!hit) return order[i];
      }
      return null;
    }
    var tries = 0;
    function show() {
      var pos = freeCorner();
      if (!pos) { if (++tries < 6) setTimeout(show, 2500); return; }
      bot.classList.add("pos-" + pos);
      bot.hidden = false;
      requestAnimationFrame(function () { requestAnimationFrame(function () { bot.classList.add("out", "drawn"); }); });
      try { sessionStorage.setItem("nb-robot", "1"); } catch (e) { /* ignore */ }
      leave = setTimeout(tuck, 6200);
    }
    setTimeout(show, 6500);
  }


  /* ---------- slide stacks: the top print lifts off and goes to the back of the pile ---------- */
  function stacks() {
    var all = document.querySelectorAll(".stack");
    var still = reduce || STATIC;
    Array.prototype.forEach.call(all, function (st, si) {
      var prints = Array.prototype.slice.call(st.querySelectorAll(".print"));
      prints.forEach(function (p, i) { p.dataset.k = i; });
      if (still || prints.length < 2) return;
      var visible = false, busy = false, timer = null;
      function flip() {
        if (busy || !visible || document.hidden) return;
        busy = true;
        var top = prints[0], next = prints[1], img = next.querySelector("img");
        var go = function () {
          top.classList.add("lift");
          setTimeout(function () {
            prints.push(prints.shift());
            top.classList.remove("lift");
            prints.forEach(function (p, i) { p.dataset.k = i; });
            busy = false;
          }, 480);
        };
        if (img && img.decode) img.decode().then(go, go); else go();
      }
      function start() { if (!timer) timer = setInterval(flip, 3400); }
      function stop() { clearInterval(timer); timer = null; }
      // stagger the piles so neighbours never flip together
      setTimeout(function () {
        if ("IntersectionObserver" in window) {
          new IntersectionObserver(function (es) {
            visible = es[0].isIntersecting;
            if (visible) start(); else stop();
          }, { threshold: 0.4 }).observe(st);
        } else { visible = true; start(); }
      }, 600 + si * 850);
      var card = st.closest("a");
      if (card) card.addEventListener("mouseenter", function () { flip(); });
    });
  }

  /* ---------- advising prints: the diagram inks itself in, and a click turns the print over ---------- */
  function prints() {
    var arts = document.querySelectorAll(".art-print .advising-art");
    Array.prototype.forEach.call(arts, function (svg) {
      var els = svg.querySelectorAll("line, polyline, path, circle, rect, ellipse, polygon, text"), k = 0;
      Array.prototype.forEach.call(els, function (el, i) {
        if (el.closest("defs")) return;
        if (el.tagName === "rect" && el.getAttribute("width") === svg.viewBox.baseVal.width + "") return;  // the print's background
        var d = Math.min(0.55 + k++ * 0.035, 1.9);
        var stroke = el.getAttribute("stroke"), fill = el.getAttribute("fill");
        var line = stroke && stroke !== "none" && (!fill || fill === "none") && el.tagName !== "text" &&
          !el.getAttribute("stroke-dasharray") && !el.getAttribute("marker-end") && el.getTotalLength;
        if (line) {
          el.classList.add("trace");
          el.style.setProperty("--len", Math.ceil(el.getTotalLength()) + 2);
        } else el.classList.add("pop");
        el.style.setProperty("--d", d + "s");
      });
    });
    var flips = document.querySelectorAll(".art-print .flip");
    Array.prototype.forEach.call(flips, function (b) {
      b.addEventListener("click", function () {
        var fig = b.parentNode, on = !fig.classList.contains("flipped");
        fig.classList.toggle("flipped", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.setAttribute("aria-label", on ? "Turn the print back" : "Turn the print over");
      });
    });
  }

  /* ---------- on phones the tabs scroll sideways: bring the current one into view ---------- */
  function currentTab() {
    var tabs = document.querySelector(".tabs"), cur = tabs && tabs.querySelector("a[aria-current]");
    if (!cur || tabs.scrollWidth <= tabs.clientWidth) return;
    var li = cur.parentNode;
    tabs.scrollLeft = Math.max(0, li.offsetLeft - tabs.offsetLeft - (tabs.clientWidth - li.offsetWidth) / 2);
  }

  /* ---------- boot ---------- */
  function boot() {
    currentTab();
    drawCharts(false);
    overlays();
    prints();
    arm();
    dock();
    stacks();
    robot();
    var lastW = window.innerWidth, t;
    window.addEventListener("resize", function () {
      clearTimeout(t);
      t = setTimeout(function () {
        if (window.innerWidth === lastW) return;
        lastW = window.innerWidth; drawCharts(true); overlays();
      }, 150);
    });
  }
  boot();
  function refit() { drawCharts(true); overlays(); }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(refit);
    var ft = null;
    if (document.fonts.addEventListener) document.fonts.addEventListener("loadingdone", function () { clearTimeout(ft); ft = setTimeout(refit, 60); });
  }
  window.addEventListener("load", refit);
})();
