/* Course hero visuals.
   Each course page gets a small animated diagram of what the course is about,
   drawn on a canvas over the course's colour: <canvas data-hero="kmeans">.
   Cards use data-static to draw one frame. Animation pauses off-screen and
   respects prefers-reduced-motion. */
(function () {
  "use strict";

  const INK = "251,248,242";   // --thumb-ink
  const WARM = "240,169,127";  // --accent (dark theme), reads on every tile colour
  const ink = (a) => `rgba(${INK},${a})`;
  const warm = (a) => `rgba(${WARM},${a})`;
  const TAU = Math.PI * 2;
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const ease = (x) => x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
  const lerp = (a, b, t) => a + (b - a) * t;
  let MINI = false;  // card thumbnails: shapes only, no text

  function rng(seed) {
    let s = seed >>> 0;
    return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }
  function gauss(r) { return Math.sqrt(-2 * Math.log(r() + 1e-9)) * Math.cos(TAU * r()); }

  function label(ctx, text, x, y, size, alpha, align) {
    if (MINI) return;
    ctx.font = `600 ${size}px "Source Sans 3", system-ui, sans-serif`;
    ctx.fillStyle = ink(alpha == null ? 0.7 : alpha);
    ctx.textAlign = align || "left";
    ctx.textBaseline = "middle";
    ctx.fillText(text, x, y);
  }
  function mono(ctx, text, x, y, size, alpha, align) {
    if (MINI) return;
    ctx.font = `500 ${size}px ui-monospace, Menlo, Consolas, monospace`;
    ctx.fillStyle = ink(alpha == null ? 0.55 : alpha);
    ctx.textAlign = align || "left";
    ctx.textBaseline = "middle";
    ctx.fillText(text, x, y);
  }
  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function node(ctx, x, y, w, h, text, glow, small) {
    roundRect(ctx, x - w / 2, y - h / 2, w, h, 6);
    ctx.fillStyle = glow > 0 ? warm(0.15 + 0.35 * glow) : ink(0.08);
    ctx.fill();
    ctx.strokeStyle = glow > 0 ? warm(0.5 + 0.5 * glow) : ink(0.45);
    ctx.lineWidth = 1.2;
    ctx.stroke();
    label(ctx, text, x, y, small || 12, 0.9, "center");
  }

  /* ---------- 45-851 Data Mining: k-means converging ---------- */
  const kmeans = (() => {
    const r = rng(851);
    const centers = [[0.22, 0.38], [0.52, 0.7], [0.8, 0.34], [0.62, 0.22]];
    const pts = [];
    centers.forEach((c) => { for (let i = 0; i < 34; i++) pts.push([c[0] + gauss(r) * 0.065, c[1] + gauss(r) * 0.09]); });
    const K = 4;
    // Precompute the iterations from a deliberately poor start.
    const iters = [];
    let cent = [[0.1, 0.8], [0.3, 0.75], [0.45, 0.85], [0.95, 0.9]];
    for (let it = 0; it < 7; it++) {
      const asg = pts.map((p) => {
        let best = 0, bd = 1e9;
        cent.forEach((c, k) => { const d = (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2; if (d < bd) { bd = d; best = k; } });
        return best;
      });
      iters.push({ cent: cent.map((c) => c.slice()), asg });
      cent = cent.map((c, k) => {
        const mine = pts.filter((_, i) => asg[i] === k);
        if (!mine.length) return c;
        return [mine.reduce((s, p) => s + p[0], 0) / mine.length, mine.reduce((s, p) => s + p[1], 0) / mine.length];
      });
    }
    const tints = [warm(0.95), ink(0.95), "rgba(160,215,200,0.95)", "rgba(214,190,255,0.95)"];
    return function (ctx, w, h, t) {
      const step = 1.4, n = iters.length;
      const cyc = (t / step) % (n + 2);
      const i = Math.min(Math.floor(cyc), n - 1);
      const f = cyc >= n ? 1 : ease(clamp(cyc - Math.floor(cyc), 0, 1));
      const cur = iters[i], nxt = iters[Math.min(i + 1, n - 1)];
      const pad = 18, X = (x) => pad + x * (w - 2 * pad), Y = (y) => pad + y * (h - 2 * pad);
      const cent = cur.cent.map((c, k) => [lerp(c[0], nxt.cent[k][0], f), lerp(c[1], nxt.cent[k][1], f)]);
      pts.forEach((p, j) => {
        const k = cur.asg[j];
        ctx.strokeStyle = ink(0.08);
        ctx.beginPath(); ctx.moveTo(X(p[0]), Y(p[1])); ctx.lineTo(X(cent[k][0]), Y(cent[k][1])); ctx.stroke();
      });
      pts.forEach((p, j) => {
        ctx.fillStyle = tints[cur.asg[j]];
        ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 2.6, 0, TAU); ctx.fill();
      });
      cent.forEach((c, k) => {
        const x = X(c[0]), y = Y(c[1]);
        ctx.strokeStyle = tints[k]; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x - 7, y - 7); ctx.lineTo(x + 7, y + 7); ctx.moveTo(x + 7, y - 7); ctx.lineTo(x - 7, y + 7); ctx.stroke();
      });
      ctx.lineWidth = 1;
      mono(ctx, `k = ${K}   iteration ${i + 1}`, w - pad, pad, 11, 0.6, "right");
    };
  })();

  /* ---------- 45-884 AI Methods: vision transformer ---------- */
  const vit = (() => {
    const r = rng(884);
    const patch = Array.from({ length: 16 }, () => [r(), r(), r()]);
    const words = ["a", "dog", "catches", "a", "frisbee"];
    const layers = ["Patch embedding", "Multi-head attention", "Feed forward", "Multi-head attention", "Feed forward"];
    return function (ctx, w, h, t) {
      const narrow = w < 520;
      const gx = 22, cell = narrow ? 18 : 24, gy = 18;
      // image as 4x4 patches
      for (let i = 0; i < 16; i++) {
        const cx = gx + (i % 4) * (cell + 3), cy = gy + Math.floor(i / 4) * (cell + 3);
        const p = patch[i], lit = (Math.floor(t * 3) % 16) === i;
        ctx.fillStyle = `rgba(${Math.round(150 + 90 * p[0])},${Math.round(150 + 80 * p[1])},${Math.round(160 + 80 * p[2])},${lit ? 0.95 : 0.55})`;
        ctx.fillRect(cx, cy, cell, cell);
        if (lit) { ctx.strokeStyle = warm(1); ctx.lineWidth = 2; ctx.strokeRect(cx - 1, cy - 1, cell + 2, cell + 2); ctx.lineWidth = 1; }
      }
      mono(ctx, "image as 16 patches", gx, gy + 4 * (cell + 3) + 12, 10, 0.55);
      // transformer stack
      const sx = narrow ? w * 0.5 : w * 0.45, bw = narrow ? 128 : 170, bh = 22, top = 16;
      const gap = (h - 2 * top - layers.length * bh) / (layers.length - 1);
      const pulse = (t * 0.9) % 1.4;
      layers.slice().reverse().forEach((name, i) => {
        const y = top + i * (bh + gap) + bh / 2;
        const level = (layers.length - 1 - i) / (layers.length - 1);
        const glow = Math.max(0, 1 - Math.abs(pulse - level) * 5);
        node(ctx, sx, y, bw, bh, name, glow, narrow ? 10 : 11);
      });
      ctx.strokeStyle = ink(0.35);
      ctx.beginPath(); ctx.moveTo(gx + 4 * (cell + 3) + 4, gy + 2 * (cell + 3)); ctx.lineTo(sx - bw / 2 - 6, h - top - bh / 2); ctx.stroke();
      // caption tokens with attention arcs
      const tx0 = sx + bw / 2 + 34, tx1 = w - 40;
      if (tx1 - tx0 > 150) {
        const ty = h / 2 + 18, step = (tx1 - tx0) / (words.length - 1);
        const shown = Math.floor((t * 1.2) % (words.length + 2));
        const q = Math.min(shown, words.length - 1);
        words.forEach((wd, i) => {
          const x = tx0 + i * step;
          if (i <= shown && i !== q) {
            const wgt = 0.25 + 0.75 * Math.abs(Math.sin(i * 1.7 + t));
            ctx.strokeStyle = warm(0.2 + 0.6 * wgt); ctx.lineWidth = 1 + 2.5 * wgt;
            const xq = tx0 + q * step;
            ctx.beginPath(); ctx.moveTo(x, ty - 12); ctx.quadraticCurveTo((x + xq) / 2, ty - 40 - Math.abs(xq - x) * 0.35, xq, ty - 12); ctx.stroke();
          }
          ctx.lineWidth = 1;
          label(ctx, wd, x, ty, 13, i <= shown ? 0.95 : 0.25, "center");
        });
        mono(ctx, "attention to earlier words", tx0, ty + 26, 10, 0.5);
      }
    };
  })();

  /* ---------- 70-445: an orchestrator agent and its tools ---------- */
  const agents = (() => {
    const tools = ["Research", "CRM", "Email", "Evaluate", "Code"];
    return function (ctx, w, h, t) {
      const cx = w / 2, cy = h / 2, rx = Math.min(w * 0.36, 260), ry = h * 0.34;
      const active = Math.floor(t / 1.6) % tools.length, ph = (t % 1.6) / 1.6;
      tools.forEach((name, i) => {
        const a = -Math.PI / 2 + (i / tools.length) * TAU;
        const x = cx + rx * Math.cos(a), y = cy + ry * Math.sin(a);
        ctx.strokeStyle = i === active ? warm(0.8) : ink(0.25);
        ctx.setLineDash(i === active ? [] : [3, 4]);
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x, y); ctx.stroke();
        ctx.setLineDash([]);
        if (i === active) {
          const go = ph < 0.5, k = go ? ease(ph * 2) : ease((ph - 0.5) * 2);
          const px = go ? lerp(cx, x, k) : lerp(x, cx, k), py = go ? lerp(cy, y, k) : lerp(y, cy, k);
          ctx.fillStyle = warm(1); ctx.beginPath(); ctx.arc(px, py, 4, 0, TAU); ctx.fill();
        }
        node(ctx, x, y, 78, 24, name, i === active ? 0.7 : 0, 11);
      });
      node(ctx, cx, cy, 112, 32, "Orchestrator", 0.25 + 0.2 * Math.sin(t * 3), 13);
      mono(ctx, `step ${Math.floor(t / 1.6) + 1}: call ${tools[active].toLowerCase()}`, 16, 16, 11, 0.6);
    };
  })();

  /* ---------- 45-885 Data Visualization: one dataset, three charts ---------- */
  const charts = (() => {
    const vals = [0.55, 0.8, 0.35, 0.65, 0.9, 0.45, 0.7];
    const after = [0.7, 0.62, 0.5, 0.85, 0.72, 0.3, 0.9];
    const names = ["bars", "scatter", "slope graph"];
    return function (ctx, w, h, t) {
      const pad = 22, n = vals.length, stage = Math.floor(t / 3) % 3, f = ease(clamp((t % 3) / 1.2, 0, 1));
      const from = (stage + 2) % 3, to = stage;
      const pos = (mode, i) => {
        if (mode === 0) { const bw = (w - 2 * pad) / n; return { x: pad + bw * (i + 0.5), y: h - pad - vals[i] * (h - 2 * pad), bar: 1, bw: bw * 0.6 }; }
        if (mode === 1) return { x: pad + after[i] * (w - 2 * pad), y: h - pad - vals[i] * (h - 2 * pad), bar: 0, bw: 0 };
        return { x: pad + (i % 2 ? 0.78 : 0.22) * (w - 2 * pad), y: h - pad - (i % 2 ? after[i] : vals[i]) * (h - 2 * pad), bar: 0, bw: 0 };
      };
      ctx.strokeStyle = ink(0.3);
      ctx.beginPath(); ctx.moveTo(pad, pad / 2); ctx.lineTo(pad, h - pad); ctx.lineTo(w - pad, h - pad); ctx.stroke();
      const slopeF = to === 2 ? f : from === 2 ? 1 - f : 0;
      if (slopeF > 0) {
        for (let i = 0; i < n; i++) {
          const a = pad + 0.22 * (w - 2 * pad), b = pad + 0.78 * (w - 2 * pad);
          const ya = h - pad - vals[i] * (h - 2 * pad), yb = h - pad - after[i] * (h - 2 * pad);
          ctx.strokeStyle = after[i] > vals[i] ? warm(0.8 * slopeF) : ink(0.35 * slopeF);
          ctx.lineWidth = after[i] > vals[i] ? 2 : 1;
          ctx.beginPath(); ctx.moveTo(a, ya); ctx.lineTo(b, yb); ctx.stroke();
          ctx.fillStyle = ctx.strokeStyle; ctx.beginPath(); ctx.arc(a, ya, 3, 0, TAU); ctx.arc(b, yb, 3, 0, TAU); ctx.fill();
        }
        ctx.lineWidth = 1;
      }
      for (let i = 0; i < n; i++) {
        const A = pos(from, i), B = pos(to, i);
        const x = lerp(A.x, B.x, f), y = lerp(A.y, B.y, f), bar = lerp(A.bar, B.bar, f), bw = lerp(A.bw, B.bw, f);
        const hl = i === 4;
        if (bar > 0.01) { ctx.fillStyle = hl ? warm(0.9 * bar) : ink(0.5 * bar); ctx.fillRect(x - bw / 2, y, bw, h - pad - y); }
        if (slopeF < 0.99) { ctx.fillStyle = hl ? warm(1) : ink(0.9); ctx.beginPath(); ctx.arc(x, y, 4 * (1 - bar * 0.6), 0, TAU); ctx.fill(); }
      }
      mono(ctx, `same data, as a ${names[to]}`, w - pad, pad / 2 + 4, 11, 0.6, "right");
    };
  })();

  /* ---------- 46-885: exploratory brushing ---------- */
  const brush = (() => {
    const r = rng(46885), pts = Array.from({ length: 90 }, () => { const x = r(); return [x, clamp(0.2 + 0.6 * x + gauss(r) * 0.12, 0.02, 0.98)]; });
    return function (ctx, w, h, t) {
      const pad = 18, split = w * 0.62, sw = split - pad * 2;
      const bx = (0.5 + 0.38 * Math.sin(t * 0.7)) * 0.8, bwid = 0.22;
      const X = (x) => pad + x * sw, Y = (y) => h - pad - y * (h - 2 * pad);
      ctx.strokeStyle = ink(0.3); ctx.strokeRect(pad, pad, sw, h - 2 * pad);
      ctx.fillStyle = warm(0.12); ctx.fillRect(X(bx), pad, bwid * sw, h - 2 * pad);
      ctx.strokeStyle = warm(0.7); ctx.strokeRect(X(bx), pad, bwid * sw, h - 2 * pad);
      const sel = pts.map((p) => p[0] >= bx && p[0] <= bx + bwid);
      pts.forEach((p, i) => { ctx.fillStyle = sel[i] ? warm(1) : ink(0.55); ctx.beginPath(); ctx.arc(X(p[0]), Y(p[1]), 2.4, 0, TAU); ctx.fill(); });
      const bins = 8, hx = split + 10, hw = w - pad - hx, bh = (h - 2 * pad) / bins;
      const all = Array(bins).fill(0), hit = Array(bins).fill(0);
      pts.forEach((p, i) => { const b = Math.min(bins - 1, Math.floor(p[1] * bins)); all[b]++; if (sel[i]) hit[b]++; });
      const mx = Math.max(...all);
      for (let b = 0; b < bins; b++) {
        const y = h - pad - (b + 1) * bh + 2;
        ctx.fillStyle = ink(0.25); ctx.fillRect(hx, y, (all[b] / mx) * hw, bh - 4);
        ctx.fillStyle = warm(0.9); ctx.fillRect(hx, y, (hit[b] / mx) * hw, bh - 4);
      }
      mono(ctx, "brush one view, see it in the other", pad, pad - 8 < 6 ? 8 : pad - 8, 10, 0.55);
    };
  })();

  /* ---------- 46-880: Galton board ---------- */
  const galton = (() => {
    const rows = 9, bins = rows + 1;
    return function (ctx, w, h, t) {
      const cx = w * 0.32, top = 14, rowH = (h * 0.52) / rows, spread = Math.min(18, w / 40);
      for (let r = 0; r < rows; r++) for (let k = 0; k <= r; k++) {
        ctx.fillStyle = ink(0.4); ctx.beginPath(); ctx.arc(cx + (k - r / 2) * spread * 2, top + r * rowH, 1.8, 0, TAU); ctx.fill();
      }
      const counts = Array(bins).fill(0), N = Math.floor((t * 14) % 520);
      const rr = rng(880);
      let lastPath = null;
      for (let b = 0; b < N; b++) {
        let k = 0; const path = [];
        for (let r = 0; r < rows; r++) { const right = rr() < 0.5 ? 1 : 0; k += right; path.push(k); }
        counts[k]++; if (b === N - 1) lastPath = path;
      }
      const base = h - 14, mx = Math.max(8, ...counts), bw = spread * 2 - 2;
      for (let i = 0; i < bins; i++) {
        const x = cx + (i - rows / 2) * spread * 2, hh = (counts[i] / mx) * (h * 0.36);
        ctx.fillStyle = ink(0.55); ctx.fillRect(x - bw / 2, base - hh, bw, hh);
      }
      if (lastPath) {
        const fr = (t * 14) % 1;
        const r = Math.min(rows - 1, Math.floor(fr * rows)), k = lastPath[r];
        ctx.fillStyle = warm(1); ctx.beginPath(); ctx.arc(cx + (k - (r + 1) / 2) * spread * 2, top + (r + 0.5) * rowH, 3.5, 0, TAU); ctx.fill();
      }
      // normal curve overlay scaled to the counts
      ctx.strokeStyle = warm(0.9); ctx.lineWidth = 2; ctx.beginPath();
      const sd = Math.sqrt(rows / 4), peak = N / (sd * Math.sqrt(TAU));
      for (let i = 0; i <= 80; i++) {
        const z = (i / 80) * bins - 0.5, x = cx + (z - rows / 2) * spread * 2;
        const y = base - ((peak * Math.exp(-((z - rows / 2) ** 2) / (2 * sd * sd))) / mx) * (h * 0.36);
        i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
      }
      ctx.stroke(); ctx.lineWidth = 1;
      const tx = cx + rows * spread + 30;
      if (tx < w - 120) {
        label(ctx, "Central limit theorem", tx, h * 0.38, 15, 0.9);
        mono(ctx, `n = ${N} draws`, tx, h * 0.38 + 22, 11, 0.6);
      }
    };
  })();

  /* ---------- 46-887: cloud ML pipeline ---------- */
  const pipeline = (() => {
    const stages = ["Data", "S3", "Train", "Model API", "Dashboard"];
    return function (ctx, w, h, t) {
      const pad = 44, y = h * 0.44, step = (w - 2 * pad) / (stages.length - 1);
      ctx.strokeStyle = ink(0.35); ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(w - pad, y); ctx.stroke();
      for (let p = 0; p < 6; p++) {
        const x = pad + (((t * 0.22 + p / 6) % 1) * (w - 2 * pad));
        ctx.fillStyle = warm(0.95); ctx.beginPath(); ctx.arc(x, y, 3.2, 0, TAU); ctx.fill();
      }
      stages.forEach((s, i) => {
        const x = pad + i * step, glow = Math.max(0, 1 - Math.abs(((t * 0.22) % 1) * (stages.length - 1) - i) * 1.5);
        node(ctx, x, y, w < 520 ? 58 : 78, 26, s, glow * 0.8, w < 520 ? 10 : 12);
      });
      // a loss curve under Train, a live bar chart under Dashboard
      const lx = pad + 2 * step - 30, ly = y + 30;
      ctx.strokeStyle = ink(0.7); ctx.beginPath();
      for (let i = 0; i <= 30; i++) { const x = lx + i * 2, v = Math.exp(-i / 8) + 0.05 * Math.sin(i + t * 2); i ? ctx.lineTo(x, ly + 26 - v * 24) : ctx.moveTo(x, ly + 26 - v * 24); }
      ctx.stroke();
      mono(ctx, "loss", lx, ly + 36, 9, 0.5);
      const dx = pad + 4 * step - 26;
      for (let i = 0; i < 5; i++) { const v = 0.4 + 0.5 * Math.abs(Math.sin(i * 1.3 + t * 0.8)); ctx.fillStyle = i === 2 ? warm(0.9) : ink(0.55); ctx.fillRect(dx + i * 11, ly + 26 - v * 26, 8, v * 26); }
    };
  })();

  /* ---------- 90-803: neural network forward pass ---------- */
  const network = (() => {
    const layers = [4, 6, 6, 3];
    return function (ctx, w, h, t) {
      const pad = 40, lx = (i) => pad + (i / (layers.length - 1)) * (w - 2 * pad);
      const ny = (n, j) => h / 2 + (j - (n - 1) / 2) * Math.min(26, (h - 30) / n);
      const wave = (t * 0.8) % (layers.length + 0.6);
      for (let i = 0; i < layers.length - 1; i++) for (let a = 0; a < layers[i]; a++) for (let b = 0; b < layers[i + 1]; b++) {
        const on = Math.max(0, 1 - Math.abs(wave - (i + 0.5)) * 2);
        const wt = Math.abs(Math.sin(a * 3.1 + b * 1.7 + i));
        ctx.strokeStyle = on > 0 ? warm(0.1 + 0.6 * on * wt) : ink(0.1);
        ctx.beginPath(); ctx.moveTo(lx(i), ny(layers[i], a)); ctx.lineTo(lx(i + 1), ny(layers[i + 1], b)); ctx.stroke();
      }
      layers.forEach((n, i) => {
        for (let j = 0; j < n; j++) {
          const on = Math.max(0, 1 - Math.abs(wave - i) * 2) * Math.abs(Math.sin(j * 2.3 + i));
          ctx.fillStyle = on > 0.05 ? warm(0.3 + 0.7 * on) : ink(0.2);
          ctx.strokeStyle = ink(0.6);
          ctx.beginPath(); ctx.arc(lx(i), ny(n, j), 7, 0, TAU); ctx.fill(); ctx.stroke();
        }
      });
      mono(ctx, "inputs", lx(0), 12, 10, 0.55, "center");
      mono(ctx, "prediction", lx(layers.length - 1), 12, 10, 0.55, "center");
    };
  })();

  /* ---------- MSBA Math Skills: gradient descent on a loss surface ---------- */
  const descent = (() => {
    const f = (x, y) => 0.6 * x * x + 2.2 * y * y + 0.5 * x * y;
    const g = (x, y) => [1.2 * x + 0.5 * y, 4.4 * y + 0.5 * x];
    const path = [[-2.6, 1.3]];
    for (let i = 0; i < 40; i++) { const [x, y] = path[path.length - 1], d = g(x, y); path.push([x - 0.18 * d[0], y - 0.18 * d[1]]); }
    return function (ctx, w, h, t) {
      const cx = w * 0.5, cy = h * 0.52, s = Math.min(w / 7, h / 3.6);
      for (let lv = 1; lv <= 7; lv++) {
        const c = lv * lv * 0.35;
        ctx.strokeStyle = ink(0.12 + lv * 0.03); ctx.beginPath();
        for (let i = 0; i <= 90; i++) {
          const a = (i / 90) * TAU; let rr = 0.1;
          for (let k = 0; k < 30; k++) { if (f(rr * Math.cos(a), rr * Math.sin(a)) < c) rr += 0.1; }
          const x = cx + rr * Math.cos(a) * s, y = cy + rr * Math.sin(a) * s;
          i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
        }
        ctx.stroke();
      }
      const k = Math.floor((t * 5) % (path.length + 12));
      ctx.strokeStyle = warm(0.9); ctx.lineWidth = 2; ctx.beginPath();
      path.slice(0, Math.min(k, path.length) + 1).forEach(([x, y], i) => { const px = cx + x * s, py = cy + y * s; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); });
      ctx.stroke(); ctx.lineWidth = 1;
      const [bx, by] = path[Math.min(k, path.length - 1)];
      ctx.fillStyle = warm(1); ctx.beginPath(); ctx.arc(cx + bx * s, cy + by * s, 5, 0, TAU); ctx.fill();
      mono(ctx, "x ← x − η ∇f(x)", 16, 18, 12, 0.7);
      mono(ctx, `step ${Math.min(k, path.length - 1)}   f = ${f(bx, by).toFixed(3)}`, w - 16, h - 14, 11, 0.6, "right");
    };
  })();

  /* ---------- 70-377: teams forming ---------- */
  const teams = (() => {
    const r = rng(377), people = Array.from({ length: 24 }, (_, i) => ({ team: i % 4, sx: r(), sy: r() }));
    const hubs = [[0.2, 0.35], [0.45, 0.7], [0.7, 0.3], [0.88, 0.68]];
    return function (ctx, w, h, t) {
      const f = ease(clamp(((t % 7) - 1) / 3, 0, 1)), pad = 20;
      const P = people.map((p, i) => {
        const hb = hubs[p.team], a = (i / 6) * TAU + p.team;
        const tx = hb[0] + 0.07 * Math.cos(a), ty = hb[1] + 0.16 * Math.sin(a);
        return [pad + lerp(p.sx, tx, f) * (w - 2 * pad), pad + lerp(p.sy, ty, f) * (h - 2 * pad)];
      });
      if (f > 0.3) {
        people.forEach((p, i) => people.forEach((q, j) => {
          if (j > i && p.team === q.team) { ctx.strokeStyle = (p.team === 0 ? warm : ink)(0.25 * (f - 0.3) / 0.7); ctx.beginPath(); ctx.moveTo(...P[i]); ctx.lineTo(...P[j]); ctx.stroke(); }
        }));
      }
      P.forEach((pt, i) => { ctx.fillStyle = people[i].team === 0 ? warm(0.95) : ink(0.85); ctx.beginPath(); ctx.arc(pt[0], pt[1], 4, 0, TAU); ctx.fill(); });
      mono(ctx, f < 0.5 ? "hiring" : "teams", w - pad, pad - 4, 11, 0.6, "right");
    };
  })();

  const SCENES = { kmeans, vit, agents, charts, brush, galton, pipeline, network, descent, teams };
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setup(canvas) {
    const scene = SCENES[canvas.dataset.hero];
    if (!scene) return;
    const ctx = canvas.getContext("2d");
    const still = reduced || canvas.hasAttribute("data-static");
    let visible = true, raf = 0, t0 = performance.now();
    function size() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2), rect = canvas.getBoundingClientRect();
      canvas.width = Math.max(1, Math.round(rect.width * dpr));
      canvas.height = Math.max(1, Math.round(rect.height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return rect;
    }
    let rect = size();
    const mini = canvas.hasAttribute("data-static");
    function frame(now) {
      const t = still ? 5.2 : (now - t0) / 1000;
      ctx.clearRect(0, 0, rect.width, rect.height);
      MINI = mini;
      if (mini) { ctx.save(); ctx.scale(0.5, 0.5); scene(ctx, rect.width * 2, rect.height * 2, t); ctx.restore(); }
      else scene(ctx, rect.width, rect.height, t);
      MINI = false;
      if (!still && visible) raf = requestAnimationFrame(frame);
    }
    frame(performance.now());
    window.addEventListener("resize", () => { rect = size(); if (still || !visible) frame(performance.now()); });
    if (!still && "IntersectionObserver" in window) {
      new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        cancelAnimationFrame(raf);
        if (visible) raf = requestAnimationFrame(frame);
      }).observe(canvas);
    }
  }

  function init() { document.querySelectorAll("canvas[data-hero]").forEach(setup); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
