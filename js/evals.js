/* The evaluations page: hand-drawn charts of Ben's course evaluations, drawn with
   the same pen as js/notebook.js (window.NB). The data is inlined in #ev-data by
   the build. Every chart has a plain table twin in the page, so nothing here is
   the only way to read a number. */
(function () {
  "use strict";
  var NB = window.NB, dataEl = document.getElementById("ev-data");
  if (!NB || !dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var ITEMS = D.items, SECS = D.sections, COURSES = D.courses, NS = "http://www.w3.org/2000/svg";
  var COLOR = { MBA: "#2447a6", MSBA: "#b8352a", Undergraduate: "#6b3fa0", Heinz: "#c47a12" };
  var LABEL = { MBA: "MBA", MSBA: "MS in Business Analytics", Undergraduate: "Undergraduate", Heinz: "Heinz College" };
  var PAPER = "#fbf8f1";
  var state = { item: "9", prog: "all" };
  var E = NB.E, ink = NB.ink, lineD = NB.lineD, curve = NB.curve, loopD = NB.loopD, J = NB.J;

  function fmt(x, d) { return (Math.round(x * Math.pow(10, d == null ? 2 : d)) / Math.pow(10, d == null ? 2 : d)).toFixed(d == null ? 2 : d); }
  function shortTerm(t) { return t.replace(/(\w+) 20(\d\d)/, "$1 '$2"); }
  function wmean(list, key) {
    var s = 0, n = 0;
    list.forEach(function (x) { s += key(x) * x.n; n += x.n; });
    return n ? s / n : NaN;
  }
  function val(s) { return s.avg[state.item]; }
  function visible() { return SECS.filter(function (s) { return state.prog === "all" || s.program === state.prog; }); }
  function uniq(arr) { return arr.filter(function (x, i) { return arr.indexOf(x) === i; }); }
  function svgFor(el, w, h) {
    el.innerHTML = ""; el.setAttribute("viewBox", "0 0 " + w + " " + h); el.setAttribute("width", w); el.setAttribute("height", h);
    return el;
  }
  function kalam(svg, x, y, str, o) {
    o = o || {};
    var t = NB.text(svg, x, y, str, { font: o.font || "400 15px Kalam, cursive", color: o.color || "#4a5463", anchor: o.anchor, d: o.d || 0.2 });
    return t;
  }
  function mono(svg, x, y, str, o) {
    o = o || {};
    var t = E("text", { x: x, y: y, class: "ev-mono", "text-anchor": o.anchor || "start" }, svg);
    t.textContent = str; if (o.color) t.style.fill = o.color; if (o.size) t.style.fontSize = o.size + "px";
    return t;
  }
  function hair(svg, x1, y1, x2, y2) {
    var p = E("path", { d: "M" + x1 + " " + y1 + "L" + x2 + " " + y2, class: "ev-grid" }, svg);
    return p;
  }

  /* ---------- the sticky-note tooltip ---------- */
  var tip = document.createElement("div");
  tip.className = "ev-tip"; tip.hidden = true; tip.setAttribute("role", "status"); document.body.appendChild(tip);
  function showTip(lines, x, y) {
    tip.textContent = "";
    lines.forEach(function (l, i) {
      var p = document.createElement(i === 0 ? "strong" : "span"); p.textContent = l; tip.appendChild(p);
    });
    tip.hidden = false;
    var w = tip.offsetWidth, h = tip.offsetHeight, vw = window.innerWidth;
    var left = x + 16; if (left + w > vw - 8) left = x - w - 16;
    var top = y - h - 12; if (top < 8) top = y + 18;
    tip.style.left = left + "px"; tip.style.top = top + "px";
  }
  function hideTip() { tip.hidden = true; clearTimeout(tipTimer); }
  // The note is pinned to the window, so it must never outlive the tap or the
  // scroll that produced it: on phones a tap leaves focus on the mark and no
  // pointerleave ever fires.
  var tipTimer = null;
  window.addEventListener("scroll", hideTip, { passive: true });
  document.addEventListener("pointerdown", function () { hideTip(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideTip(); });
  function touchTip() { clearTimeout(tipTimer); tipTimer = setTimeout(hideTip, 2600); }
  function hit(svg, cx, cy, r, lines, label) {
    var h = E("circle", { cx: cx, cy: cy, r: Math.max(r + 8, 14), class: "ev-hit", tabindex: "0", role: "img", "aria-label": label }, svg);
    h.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") showTip(lines, e.clientX, e.clientY); });
        h.addEventListener("pointerup", function (e) { if (e.pointerType !== "mouse") { showTip(lines, e.clientX, e.clientY); touchTip(); } });
    h.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hideTip(); });
    h.addEventListener("focus", function () { if (!h.matches(":focus-visible")) return; var b = h.getBoundingClientRect(); showTip(lines, b.left + b.width / 2, b.top); });
    h.addEventListener("blur", hideTip);
    return h;
  }
  function dot(svg, cx, cy, r, color, d) {
    var ring = E("circle", { cx: cx, cy: cy, r: r + 2, class: "dot ev-ring" }, svg); ring.style.fill = PAPER; ring.style.setProperty("--d", d + "s");
    var c = E("circle", { cx: cx, cy: cy, r: r, class: "dot ev-dot" }, svg); c.style.fill = color; c.style.setProperty("--d", d + "s");
    return c;
  }

  /* ---------- fig. 1: every section on a timeline ---------- */
  function timeline(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640, H = narrow ? 340 : 420;
    var L = 44, R = 16, T = 22, B = narrow ? 54 : 46;
    svgFor(svg, W, H); NB.seed(11);
    var list = visible(), terms = uniq(SECS.map(function (s) { return s.term; }));
    var lo = 0, hi = 5;
    list.forEach(function (s) { if (val(s) < lo) lo = Math.floor(val(s) * 2) / 2; });
    function X(i) { return L + 18 + (i / Math.max(1, terms.length - 1)) * (W - L - R - 36); }
    function Y(v) { return T + (hi - v) / (hi - lo) * (H - T - B); }
    for (var v = lo; v <= hi + 0.001; v += 1) {
      hair(svg, L, Y(v), W - R, Y(v));
      mono(svg, L - 8, Y(v) + 4, v.toFixed(0), { anchor: "end", size: 11.5 });
    }
    ink(svg, lineD(L, Y(lo), L, Y(hi), 0.5), { w: 2, d: 0.1, dur: 0.5, color: "#1d2633" });
    ink(svg, lineD(L, Y(lo), W - R, Y(lo), 0.5), { w: 2, d: 0.1, dur: 0.7, color: "#1d2633" });
    terms.forEach(function (t, i) {
      var lab = narrow ? t.replace(/(\w)\w+ 20(\d\d)/, "$1'$2") : shortTerm(t);
      kalam(svg, X(i), H - B + 22, lab, { anchor: "middle", d: 0.3 + i * 0.05, font: "400 14px Kalam, cursive" });
    });
    // the running mean, term by term
    var pts = [], k = 0;
    terms.forEach(function (t, i) {
      var inT = list.filter(function (s) { return s.term === t; });
      if (inT.length) pts.push([X(i), Y(wmean(inT, val))]);
    });
    if (pts.length > 1) ink(svg, curve(pts), { w: 2.4, d: 0.5, dur: 1.4, color: "#1d2633", op: 0.5 });
    // one dot per section
    terms.forEach(function (t, i) {
      var inT = list.filter(function (s) { return s.term === t; });
      inT.forEach(function (s, j) {
        var spread = inT.length > 1 ? (j - (inT.length - 1) / 2) * (narrow ? 9 : 13) : 0;
        var cx = X(i) + spread, cy = Y(val(s)), r = 3.5 + Math.sqrt(s.n) * (narrow ? 0.7 : 0.9);
        var c = dot(svg, cx, cy, r, COLOR[s.program], 0.6 + k * 0.045);
        var name = COURSES[s.course].name;
        hit(svg, cx, cy, r, [fmt(val(s)) + " " + ITEMS[state.item].toLowerCase(), name + " (" + s.section + ")", s.term + " · " + LABEL[s.program], s.n + " of " + s.possible + " students responded"],
          name + ", " + s.term + ", " + fmt(val(s)) + " of 5");
        k++;
      });
    });
    // end label on the running mean
    if (pts.length > 1) {
      var last = pts[pts.length - 1];
      kalam(svg, last[0] - 6, last[1] - 22, fmt(wmean(list.filter(function (s) { return s.term === terms[terms.length - 1]; }), val), 2), { anchor: "end", color: "#1d2633", font: "700 17px Kalam, cursive", d: 1.6 });
    }
    // where it started
    if (state.prog === "all" && state.item === "9" && !narrow) {
      kalam(svg, X(0) + 26, Y(3.72), "first mini as an adjunct", { d: 1.2, font: "400 14px Kalam, cursive", color: "#2447a6" });
      var a = NB.arrowD(X(0) + 24, Y(3.76), X(0) + 10, Y(3.86), -6, 7);
      ink(svg, a[0], { w: 1.6, d: 1.4, dur: 0.4, color: "#2447a6" }); ink(svg, a[1], { w: 1.6, d: 1.75, dur: 0.2, color: "#2447a6" });
    }
    NB.measure(svg);
  }

  /* ---------- fig. 2: by course, every section along a line ---------- */
  function courses(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640;
    var list = visible(), nums = uniq(list.map(function (s) { return s.course; }));
    var rows = nums.map(function (c) {
      var inC = list.filter(function (s) { return s.course === c; });
      return { c: c, name: COURSES[c].name, m: wmean(inC, val), secs: inC, n: inC.reduce(function (a, s) { return a + s.n; }, 0) };
    }).sort(function (a, b) { return b.m - a.m; });
    var rowH = narrow ? 58 : 44, L = narrow ? 16 : 300, R = 60, T = narrow ? 8 : 30, labelTop = narrow ? 16 : 0;
    var H = T + rows.length * rowH + 30;
    svgFor(svg, W, H); NB.seed(23);
    var lo = 0, hi = 5;
    list.forEach(function (s) { if (val(s) < lo) lo = Math.floor(val(s) * 2) / 2; });
    function X(v) { return L + (v - lo) / (hi - lo) * (W - L - R); }
    for (var v = lo; v <= hi + 0.001; v += 1) {
      hair(svg, X(v), T - 4, X(v), H - 22);
      mono(svg, X(v), H - 6, v.toFixed(0), { anchor: "middle", size: 11.5 });
    }
    rows.forEach(function (r, i) {
      var y = T + i * rowH + rowH / 2 + labelTop;
      if (narrow) kalam(svg, L, y - 16, r.name, { font: "400 14px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.06 });
      else kalam(svg, L - 14, y + 5, r.name, { anchor: "end", font: "400 16px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.06 });
      var xs = r.secs.map(function (s) { return X(val(s)); });
      var xmin = Math.min.apply(null, xs), xmax = Math.max.apply(null, xs);
      if (r.secs.length > 1) ink(svg, lineD(xmin, y, xmax, y, 0.3), { w: 2, d: 0.3 + i * 0.08, dur: 0.5, color: COLOR[COURSES[r.c].program], op: 0.45 });
      r.secs.forEach(function (s, j) {
        var c = dot(svg, X(val(s)), y, 4, COLOR[s.program], 0.5 + i * 0.08 + j * 0.03);
        hit(svg, X(val(s)), y, 4, [fmt(val(s)) + " " + ITEMS[state.item].toLowerCase(), r.name + " (" + s.section + ")", s.term, s.n + " of " + s.possible + " responded"], r.name + " " + s.term + " " + fmt(val(s)));
      });
      // the course mean: a pen ring
      ink(svg, loopD(X(r.m), y, 8, 8, 0.4, 0.06), { w: 2.4, d: 0.8 + i * 0.08, dur: 0.5, color: "#1d2633" });
      kalam(svg, Math.max(X(r.m), xmax) + 14, y + 6, fmt(r.m), { font: "700 16px Kalam, cursive", color: "#1d2633", d: 1 + i * 0.08 });
    });
    NB.measure(svg);
  }

  /* ---------- fig. 3: the courses taught again and again ---------- */
  function multiples(wrap) {
    wrap.innerHTML = "";
    var nums = uniq(SECS.map(function (s) { return s.course; })).filter(function (c) { return SECS.filter(function (s) { return s.course === c; }).length >= 3; });
    nums.forEach(function (c, ci) {
      var inC = SECS.filter(function (s) { return s.course === c; }), terms = uniq(inC.map(function (s) { return s.term; }));
      var fig = document.createElement("figure"); fig.className = "ev-multiple";
      var h = document.createElement("h3"); h.textContent = COURSES[c].name; fig.appendChild(h);
      var svg = document.createElementNS(NS, "svg"); fig.appendChild(svg); wrap.appendChild(fig);
      var W = Math.max(260, fig.clientWidth), H = 220, L = 36, R = 44, T = 26, B = 40;
      svgFor(svg, W, H); NB.seed(31 + ci);
      var lo = 0, hi = 5;
      inC.forEach(function (s) { if (val(s) < lo) lo = Math.floor(val(s) * 2) / 2; });
      function X(i) { return L + 12 + (i / Math.max(1, terms.length - 1)) * (W - L - R - 24); }
      function Y(v) { return T + (hi - v) / (hi - lo) * (H - T - B); }
      for (var v = lo; v <= hi + 0.001; v += 1) { hair(svg, L, Y(v), W - R, Y(v)); mono(svg, L - 6, Y(v) + 4, v.toFixed(0), { anchor: "end", size: 11 }); }
      ink(svg, lineD(L, Y(lo), W - R, Y(lo), 0.4), { w: 1.8, d: 0.1, dur: 0.5, color: "#1d2633" });
      terms.forEach(function (t, i) { kalam(svg, X(i), H - B + 20, t.replace(/(\w)\w+ 20(\d\d)/, "$1'$2"), { anchor: "middle", font: "400 13px Kalam, cursive", d: 0.2 + i * 0.05 }); });
      var pts = terms.map(function (t, i) { return [X(i), Y(wmean(inC.filter(function (s) { return s.term === t; }), val))]; });
      ink(svg, curve(pts), { w: 2.4, d: 0.4, dur: 1.2, color: COLOR[COURSES[c].program] });
      inC.forEach(function (s, j) {
        var cx = X(terms.indexOf(s.term)), cy = Y(val(s));
        dot(svg, cx, cy, 4.5, COLOR[s.program], 0.6 + j * 0.08);
        hit(svg, cx, cy, 4.5, [fmt(val(s)) + " " + ITEMS[state.item].toLowerCase(), COURSES[c].name + " (" + s.section + ")", s.term, s.n + " of " + s.possible + " responded"], s.term + " " + fmt(val(s)));
      });
      var first = pts[0][1], last = pts[pts.length - 1][1];
      var d = wmean(inC.filter(function (s) { return s.term === terms[terms.length - 1]; }), val) - wmean(inC.filter(function (s) { return s.term === terms[0]; }), val);
      kalam(svg, pts[pts.length - 1][0] + 8, last + 5, fmt(wmean(inC.filter(function (s) { return s.term === terms[terms.length - 1]; }), val)), { font: "700 15px Kalam, cursive", color: "#1d2633", d: 1.3 });
      kalam(svg, pts[0][0] - 2, first + 30, (d >= 0 ? "+" : "") + fmt(d, 1) + " since " + terms[0].replace(/(\w+) 20(\d\d)/, "$1 '$2"), { font: "400 13px Kalam, cursive", color: "#b8352a", d: 1.5 });
      NB.measure(svg);
    });
  }

  /* ---------- fig. 4: item by item, first year against the latest ---------- */
  function dumbbell(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640;
    var first = SECS.filter(function (s) { return s.t < 2024.5; }), latest = SECS.filter(function (s) { return s.t >= 2025.5; });
    var keys = Object.keys(ITEMS), rowH = narrow ? 52 : 40, L = narrow ? 16 : 250, R = 52, T = 26;
    var H = T + keys.length * rowH + 28, lo = 0, hi = 5;
    svgFor(svg, W, H); NB.seed(41);
    function X(v) { return L + (v - lo) / (hi - lo) * (W - L - R); }
    for (var v = lo; v <= hi + 0.001; v += 1) { hair(svg, X(v), T - 6, X(v), H - 22); mono(svg, X(v), H - 6, v.toFixed(0), { anchor: "middle", size: 11.5 }); }
    keys.forEach(function (k, i) {
      var y = T + i * rowH + rowH / 2 + (narrow ? 10 : 0);
      var a = wmean(first, function (s) { return s.avg[k]; }), b = wmean(latest, function (s) { return s.avg[k]; });
      if (narrow) kalam(svg, L, y - 14, ITEMS[k], { font: "400 13px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      else kalam(svg, L - 14, y + 5, ITEMS[k], { anchor: "end", font: (k === "9" ? "700 " : "400 ") + "15px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      ink(svg, lineD(X(a), y, X(b), y, 0.3), { w: 2.2, d: 0.4 + i * 0.07, dur: 0.5, color: "#1d2633", op: 0.35 });
      dot(svg, X(a), y, 5, "#9aa3ad", 0.3 + i * 0.07);
      dot(svg, X(b), y, 6, "#2447a6", 0.9 + i * 0.07);
      kalam(svg, X(b) + 12, y + 5, fmt(b), { font: "700 14px Kalam, cursive", color: "#1d2633", d: 1.1 + i * 0.07 });
      hit(svg, X(a), y, 5, [fmt(a) + " in 2023-24", ITEMS[k], first.reduce(function (s, x) { return s + x.n; }, 0) + " responses"], ITEMS[k] + " 2023-24 " + fmt(a));
      hit(svg, X(b), y, 6, [fmt(b) + " in 2025-26", ITEMS[k], latest.reduce(function (s, x) { return s + x.n; }, 0) + " responses"], ITEMS[k] + " 2025-26 " + fmt(b));
    });
    NB.measure(svg);
  }

  /* ---------- fig. 5: the share of students who chose "excellent" ---------- */
  function excellent(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640, rows = D.excellent;
    var rowH = narrow ? 56 : 40, L = narrow ? 16 : 300, R = 24, T = 8;
    var H = T + rows.length * rowH + 20;
    svgFor(svg, W, H); NB.seed(53);
    var ramp = ["#2447a6", "#9bb5e6", "#ddd6c6", "#e8b4ad", "#c96a5f"];
    rows.forEach(function (r, i) {
      var y = T + i * rowH + (narrow ? 22 : 8), h = 22, x = L, w = W - L - R;
      var lab = COURSES[r.course].name + " (" + r.section + "), " + shortTerm(r.term);
      if (narrow) kalam(svg, L, y - 6, lab, { font: "400 13px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      else kalam(svg, L - 14, y + 16, lab, { anchor: "end", font: "400 14.5px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      var acc = 0;
      r.teaching_dist.forEach(function (p, k) {
        if (!p) return;
        var sw = w * p / 100, seg = E("rect", { x: x + acc + 1, y: y, width: Math.max(0, sw - 2), height: h, rx: 3, class: "fade ev-seg" }, svg);
        seg.style.fill = ramp[k]; seg.style.setProperty("--d", (0.3 + i * 0.08 + k * 0.1) + "s");
        if (k === 0 && sw > 44) { var t = mono(svg, x + acc + sw / 2, y + 15, p + "%", { anchor: "middle", size: 12, color: "#fff" }); t.style.fontWeight = "600"; }
        var names = ["excellent", "above average", "average", "below average", "poor"];
        var hh = E("rect", { x: x + acc, y: y - 4, width: sw, height: h + 8, class: "ev-hit", tabindex: "0", role: "img", "aria-label": p + "% " + names[k] }, svg);
        hh.style.fill = "transparent";
        var lines = [p + "% rated the teaching " + names[k], lab, r.n + " students responded"];
        hh.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") showTip(lines, e.clientX, e.clientY); });
        hh.addEventListener("pointerup", function (e) { if (e.pointerType !== "mouse") { showTip(lines, e.clientX, e.clientY); touchTip(); } });
        hh.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hideTip(); });
        hh.addEventListener("focus", function () { if (!hh.matches(":focus-visible")) return; var b = hh.getBoundingClientRect(); showTip(lines, b.left + b.width / 2, b.top); });
        hh.addEventListener("blur", hideTip);
        acc += sw;
      });
    });
    NB.measure(svg);
  }

  /* ---------- fig. 6: what comes up in the comments ---------- */
  function themes(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640, rows = D.themes.slice(0, narrow ? 8 : 12);
    var rowH = 34, L = narrow ? 16 : 150, R = 50, T = 6, H = T + rows.length * rowH + 8, max = rows[0].count;
    svgFor(svg, W, H); NB.seed(67);
    var names = { "practical": "practical, useful at work", "pace": "pace", "engaging": "engaging", "clarity": "clear explanations", "care": "cares about students",
      "labs": "the labs", "projects": "the projects", "structure": "course structure", "recordings": "the videos", "workload": "workload", "tableau": "Tableau",
      "organization": "well organized", "assessment": "quizzes and grading", "content-timing": "release content earlier", "expertise": "knows the field", "accessibility": "for non-coders too" };
    rows.forEach(function (r, i) {
      var y = T + i * rowH, bw = Math.max(12, (W - L - R) * r.count / max), h = 20;
      kalam(svg, L - 10, y + 15, names[r.tag] || r.tag, { anchor: "end", font: "400 14px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      if (narrow) kalam(svg, L, y + 15, names[r.tag] || r.tag, { font: "400 13px Kalam, cursive", color: "#1d2633", d: 0.2 + i * 0.05 });
      ink(svg, NB.zigzag(L, y, bw, h, 7), { w: 2.2, d: 0.3 + i * 0.07, dur: 0.5 + bw / 900, color: r.tag === "pace" || r.tag === "workload" || r.tag === "content-timing" ? "#b8352a" : "#2447a6", op: 0.5 });
      ink(svg, lineD(L, y + 1, L + bw, y + J(1), 0.5) + lineD(L + bw, y, L + bw + J(1), y + h, 0.5).replace("M", "L") + lineD(L + bw, y + h, L, y + h - 1, 0.5).replace("M", "L") + "Z", { w: 1.8, d: 0.3 + i * 0.07, dur: 0.5, color: "#1d2633" });
      mono(svg, L + bw + 8, y + 15, r.count, { size: 12.5 });
      var lines = [r.count + " comments mention " + (names[r.tag] || r.tag)]; if (r.example) lines.push("“" + r.example + "”");
      var hh = E("rect", { x: L, y: y - 4, width: bw + 40, height: h + 8, class: "ev-hit", tabindex: "0", role: "img", "aria-label": lines[0] }, svg);
      hh.style.fill = "transparent";
      hh.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") showTip(lines, e.clientX, e.clientY); });
        hh.addEventListener("pointerup", function (e) { if (e.pointerType !== "mouse") { showTip(lines, e.clientX, e.clientY); touchTip(); } });
      hh.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") hideTip(); });
      hh.addEventListener("focus", function () { if (!hh.matches(":focus-visible")) return; var b = hh.getBoundingClientRect(); showTip(lines, b.left + 40, b.top); });
      hh.addEventListener("blur", hideTip);
    });
    NB.measure(svg);
  }

  /* ---------- fig. 7: before Tepper, 2012 to 2016 ---------- */
  function earlier(svg) {
    var W = Math.max(320, svg.parentNode.clientWidth), narrow = W < 640, H = narrow ? 260 : 300, rows = D.earlier;
    var L = 44, R = 16, T = 20, B = 44, terms = uniq(rows.map(function (s) { return s.term; }));
    svgFor(svg, W, H); NB.seed(79);
    var lo = 0, hi = 5;
    function X(i) { return L + 16 + (i / Math.max(1, terms.length - 1)) * (W - L - R - 32); }
    function Y(v) { return T + (hi - v) / (hi - lo) * (H - T - B); }
    for (var v = lo; v <= hi + 0.001; v += 1) { hair(svg, L, Y(v), W - R, Y(v)); mono(svg, L - 8, Y(v) + 4, v.toFixed(0), { anchor: "end", size: 11.5 }); }
    ink(svg, lineD(L, Y(lo), W - R, Y(lo), 0.5), { w: 2, d: 0.1, dur: 0.7, color: "#1d2633" });
    terms.forEach(function (t, i) { kalam(svg, X(i), H - B + 22, t.replace(/(\w)\w+ 20(\d\d)/, "$1'$2"), { anchor: "middle", font: "400 13px Kalam, cursive", d: 0.2 + i * 0.04 }); });
    var pts = terms.map(function (t, i) { var inT = rows.filter(function (s) { return s.term === t; }); return [X(i), Y(wmean(inT, function (s) { return s.teaching; }))]; });
    ink(svg, curve(pts), { w: 2.2, d: 0.4, dur: 1.4, color: "#1d2633", op: 0.5 });
    var k = 0;
    terms.forEach(function (t, i) {
      var inT = rows.filter(function (s) { return s.term === t; });
      inT.forEach(function (s, j) {
        var cx = X(i) + (inT.length > 1 ? (j - (inT.length - 1) / 2) * 10 : 0), cy = Y(s.teaching), r = 3 + Math.sqrt(s.n) * 0.8;
        dot(svg, cx, cy, r, COLOR.Undergraduate, 0.5 + k * 0.05);
        hit(svg, cx, cy, r, [fmt(s.teaching) + " overall teaching", COURSES[s.course].name + " (" + s.section + ")", s.term + " · Carnegie Mellon Qatar", s.n + " of " + s.possible + " responded"], COURSES[s.course].name + " " + s.term + " " + fmt(s.teaching));
        k++;
      });
    });
    var all = wmean(rows, function (s) { return s.teaching; });
    kalam(svg, W - R - 4, Y(all) - 10, "avg " + fmt(all), { anchor: "end", font: "700 15px Kalam, cursive", color: "#1d2633", d: 1.6 });
    NB.measure(svg);
  }

  /* ---------- the little sparkline in the headline tile ---------- */
  function spark(svg) {
    var terms = uniq(SECS.map(function (s) { return s.term; })), W = 150, H = 44;
    svgFor(svg, W, H); NB.seed(5);
    var pts = terms.map(function (t, i) { var inT = SECS.filter(function (s) { return s.term === t; }); return [6 + i / (terms.length - 1) * (W - 12), 6 + (5 - wmean(inT, function (s) { return s.avg["9"]; })) / 1.4 * (H - 12)]; });
    ink(svg, curve(pts), { w: 2.2, d: 0.8, dur: 1.2, color: "#2447a6" });
    var l = pts[pts.length - 1]; var c = E("circle", { cx: l[0], cy: l[1], r: 4, class: "dot" }, svg); c.style.fill = "#b8352a"; c.style.setProperty("--d", "2s");
    NB.measure(svg);
  }

  /* ---------- decimal count-up for the headline number ---------- */
  function countDec(el) {
    var to = parseFloat(el.dataset.to), from = 3.0, t0 = null, dur = 1600;
    if (NB.STATIC || NB.reduce || isNaN(to)) { el.textContent = to.toFixed(2); return; }
    function step(ts) {
      if (t0 === null) t0 = ts + 500;
      var p = Math.max(0, Math.min(1, (ts - t0) / dur)), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (from + (to - from) * e).toFixed(2);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    setTimeout(function () { el.textContent = to.toFixed(2); }, dur + 900);
  }

  /* ---------- controls: one row that scopes the charts below it ---------- */
  function controls() {
    var chips = document.querySelectorAll(".ev-chip"), sel = document.getElementById("ev-item");
    Array.prototype.forEach.call(chips, function (ch) {
      ch.addEventListener("click", function () {
        state.prog = ch.dataset.prog;
        Array.prototype.forEach.call(chips, function (c) { c.setAttribute("aria-pressed", c === ch ? "true" : "false"); });
        draw(["timeline", "courses"]);
      });
    });
    if (sel) sel.addEventListener("change", function () { state.item = sel.value; draw(["timeline", "courses", "multiples"]); });
    var tb = document.querySelector("[data-ev-table]");
    if (tb) {
      var tbl = document.getElementById(tb.dataset.evTable);
      tbl.hidden = true;
      tb.addEventListener("click", function () { tbl.hidden = !tbl.hidden; tb.setAttribute("aria-expanded", tbl.hidden ? "false" : "true"); tb.textContent = tbl.hidden ? "show the table" : "hide the table"; });
    }
  }

  var DRAW = { timeline: timeline, courses: courses, dumbbell: dumbbell, excellent: excellent, themes: themes, earlier: earlier, spark: spark };
  function draw(only) {
    var els = document.querySelectorAll("svg[data-ev]");
    Array.prototype.forEach.call(els, function (el) {
      var k = el.dataset.ev;
      if (only && only.indexOf(k) < 0) return;
      if (DRAW[k]) DRAW[k](el);
    });
    var m = document.querySelector("[data-ev-multiples]");
    if (m && (!only || only.indexOf("multiples") >= 0)) multiples(m);
    // sections already in view: mark drawn so fresh ink animates in rather than hiding
    var caps = document.querySelectorAll(".ev-fig");
    Array.prototype.forEach.call(caps, function (c) { if (!only) return; var sec = c.closest(".reveal"); if (sec && !sec.classList.contains("drawn")) sec.classList.add("drawn"); });
  }

  controls();
  draw();
  var dec = document.querySelector(".count-dec"); if (dec) countDec(dec);
  var lastW = window.innerWidth, t;
  window.addEventListener("resize", function () {
    clearTimeout(t);
    t = setTimeout(function () { if (window.innerWidth !== lastW) { lastW = window.innerWidth; draw(); } }, 160);
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { draw(); });
})();
