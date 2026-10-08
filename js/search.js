/* Site search: a small full-text engine and the notebook-style search box.

   The index (assets/search-index.json) is written by scripts/build.py from
   the pages themselves, one record per page and per section. It is fetched
   the first time someone reaches for search, never on a plain page view.

   How a query is ranked, in four steps:
   1. Every word is folded the same way on both sides: lower case, accents
      off, plural "s" dropped, and course numbers joined ("70-445" and
      "70 445" both become "70445").
   2. Each query word is matched against the vocabulary three ways: exactly
      (full weight), as a prefix ("clust" finds "clustering", weight up to
      0.8), and with a typo or two (edit distance 1 for words of 4 to 7
      letters, 2 for longer ones, weight 0.6 and 0.4). A few shorthands
      expand to the words the site uses: "ml" to "machine learning", "genai",
      "llm", "chatgpt" and "claude" to generative AI.
   3. A record scores, per query word, the best of those matches times how
      rare the word is (idf) times where it appears: title 6, headings 3,
      tags 2.5, body 1, the rest of a long section 0.6. Records that contain
      every query word are kept ahead of partial matches.
   4. Bonuses: the whole query as a phrase in the title (x2) or text (x1.4),
      an exact title or page name (x1.6), and a page over one of its
      sections (x1.15). A news item's title is its first sentence, so it
      weighs 2.5, not 6.

   Keys: "/" or Cmd/Ctrl+K opens, arrows move, Enter opens, Esc closes. */
(function () {
  "use strict";
  var doc = document, html = doc.documentElement;
  var root = html.getAttribute("data-root") || "";
  var LABELS = { course: "Courses", project: "Coding with AI projects", app: "Apps coded with AI", talk: "Talks",
    news: "News", cv: "CV", page: "Pages" };
  var CHIPS = [["all", "All"], ["course", "Courses"], ["project", "Projects"], ["app", "Apps coded with AI"],
    ["talk", "Talks"], ["news", "News"], ["cv", "CV"]];
  var TRY = ["data mining", "70-445", "claude code", "machine learning", "capstone", "teaching award", "reels"];
  var FIELDS = [["t", 6], ["h", 3], ["g", 2.5], ["p", 0.8], ["b", 1], ["x", 0.6]];
  var PER_GROUP = 4, PER_FILTER = 40;
  var STOP = {};
  ("a an and are as at be by for from has have i in is it its me my of on or our so than that the their them " +
    "then there these they this to was we were what when where which who will with you your about how not")
    .split(" ").forEach(function (w) { STOP[w] = 1; });

  // Shorthand on the left, what the site says on the right.
  var GEN = ["generative ai", "large language model", "language model", "llm", "chatgpt"];
  var SYN = {
    ml: ["machine learning"], ai: ["artificial intelligence"], genai: GEN, llm: GEN, chatgpt: GEN,
    claude: GEN, gpt: GEN, gemini: GEN, openai: GEN, nlp: ["natural language processing", "text mining"],
    viz: ["visualization"], dataviz: ["data visualization"], datavis: ["data visualization"], stats: ["statistics"], stat: ["statistics"],
    prob: ["probability"], dl: ["deep learning", "neural network"], cv: ["curriculum vitae", "resume"],
    resume: ["cv"], msba: ["ms in business analytics"], ob: ["organizational behavior"],
    kmeans: ["clustering"], aws: ["amazon web services", "sagemaker"], agent: ["agentic"], agentic: ["agent"],
    vision: ["computer vision"], evals: ["evaluation"], fce: ["evaluation"], talk: ["presentation", "workshop"],
    speaking: ["talk"], vibe: ["coding with ai"], capstone: ["advising"], thesis: ["advising"],
    exec: ["executive education"], qatar: ["doha"], doha: ["qatar"], cmu: ["carnegie mellon"]
  };

  // Brand names only stand in for generative AI where the brand itself is missing.
  var LOOSE = { claude: 1, chatgpt: 1, gpt: 1, gemini: 1, openai: 1 };

  // ---- text folding, shared by the index and the query -------------------
  function fold(s) {
    s = String(s || "").toLowerCase();
    if (s.normalize) s = s.normalize("NFKD").replace(/[̀-ͯ]/g, "");
    return s.replace(/\b(\d{2})-(\d{3})\b/g, "$1$2").replace(/\bk-means\b/g, "kmeans");
  }
  function stem(w) {
    if (w.length > 4 && /ies$/.test(w)) return w.slice(0, -3) + "y";
    if (w.length > 4 && /s$/.test(w) && !/(ss|us|is)$/.test(w)) return w.slice(0, -1);
    return w;
  }
  function words(s) {
    var m = fold(s).match(/[a-z0-9]+/g) || [];
    for (var i = 0; i < m.length; i++) m[i] = stem(m[i]);
    return m;
  }
  function queryWords(q) {
    q = fold(q).replace(/\b(\d{2})\s+(\d{3})\b/g, "$1$2");
    var all = words(q), kept = all.filter(function (w) { return !STOP[w]; });
    var out = [], seen = {};
    (kept.length ? kept : all).forEach(function (w) { if (!seen[w]) { seen[w] = 1; out.push(w); } });
    return out;
  }

  // Damerau-Levenshtein distance, giving up once it passes max.
  function dist(a, b, max) {
    var la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    var prev2 = null, prev = [], cur, i, j;
    for (j = 0; j <= lb; j++) prev[j] = j;
    for (i = 1; i <= la; i++) {
      cur = [i];
      var low = i;
      for (j = 1; j <= lb; j++) {
        var cost = a.charCodeAt(i - 1) === b.charCodeAt(j - 1) ? 0 : 1;
        var v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
        if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
        cur[j] = v;
        if (v < low) low = v;
      }
      if (low > max) return max + 1;
      prev2 = prev; prev = cur;
    }
    return prev[lb];
  }

  // ---- the engine ---------------------------------------------------------
  function Engine(data) {
    var docs = this.docs = data.docs, post = this.post = Object.create(null);
    var lens = docs.map(function (d) { return words((d.b || "") + " " + (d.x || "")).length; });
    var avg = lens.reduce(function (a, b) { return a + b; }, 0) / Math.max(1, docs.length);
    docs.forEach(function (d, i) {
      var w = Object.create(null);
      FIELDS.forEach(function (f) {
        if (!d[f[0]]) return;
        var cnt = Object.create(null);
        words(d[f[0]]).forEach(function (t) { cnt[t] = (cnt[t] || 0) + 1; });
        var norm = (f[0] === "b" || f[0] === "x") ? 1 / Math.sqrt(0.5 + 0.5 * lens[i] / avg) : 1;
        // A news item's "title" is just its first sentence, so it counts for less.
        var boost = f[0] === "t" && d.k === "news" ? 2.5 : f[1];
        for (var t in cnt) w[t] = (w[t] || 0) + boost * (1 + Math.log(cnt[t])) * norm;
      });
      for (var t in w) (post[t] || (post[t] = [])).push(i, w[t]);
      d._t = " " + words(d.t).join(" ") + " ";
      d._n = d.u.indexOf("#") < 0 && d.g ? " " + words(d.g.split(" \u00b7 ")[0]).join(" ") + " " : "";
      d._b = " " + words((d.h || "") + " " + (d.b || "") + " " + (d.g || "")).join(" ") + " ";
    });
    this.vocab = Object.keys(post).sort();
    this.n = docs.length;
  }
  Engine.prototype.idf = function (t) {
    return Math.log(1 + this.n / (this.post[t].length / 2));
  };
  Engine.prototype.lower = function (t) {
    var v = this.vocab, lo = 0, hi = v.length;
    while (lo < hi) { var mid = (lo + hi) >> 1; if (v[mid] < t) lo = mid + 1; else hi = mid; }
    return lo;
  };
  // Every vocabulary word a query word may stand for, with a weight.
  Engine.prototype.expand = function (t, last) {
    var alts = [], seen = Object.create(null), v = this.vocab, post = this.post;
    function add(term, w) { if (!seen[term] || seen[term] < w) { seen[term] = w; alts.push([term, w]); } }
    if (post[t]) add(t, 1);
    if (t.length >= 3 || (last && t.length >= 2) || /^\d{2,}$/.test(t)) {
      for (var i = this.lower(t), n = 0; i < v.length && n < 80 && v[i].lastIndexOf(t, 0) === 0; i++, n++) {
        if (v[i] !== t) add(v[i], 0.8 * Math.sqrt(t.length / v[i].length));
      }
    }
    if (t.length >= 5 && !/^\d+$/.test(t)) {
      // Typos: one edit for words of 5 to 7 letters, two for longer ones. A
      // word the site already uses gets its near neighbours at half weight.
      var max = t.length >= 8 ? 2 : 1, damp = post[t] ? 0.5 : 1;
      for (var k = 0; k < v.length; k++) {
        var c = v[k];
        if (seen[c] || Math.abs(c.length - t.length) > max || /^\d+$/.test(c)) continue;
        var d = dist(t, c, max);
        if (d <= max) add(c, (d === 1 ? 0.6 : 0.4) * damp);
      }
    }
    return alts;
  };
  Engine.prototype.search = function (q) {
    var t0 = (window.performance || Date).now();
    var qw = queryWords(q), self = this, docs = this.docs;
    var hits = Object.create(null);   // doc -> {s, n, m: {term: 1}}
    qw.forEach(function (t, qi) {
      var best = Object.create(null), matched = Object.create(null);
      function credit(doc, val, terms) {
        if (!best[doc] || val > best[doc]) best[doc] = val;
        var m = matched[doc] || (matched[doc] = []);
        m.push.apply(m, terms);
      }
      self.expand(t, qi === qw.length - 1).forEach(function (a) {
        var list = self.post[a[0]], idf = self.idf(a[0]);
        for (var j = 0; j < list.length; j += 2) credit(list[j], a[1] * list[j + 1] * idf, [a[0]]);
      });
      var synOnly = Object.create(null);
      (SYN[t] || []).forEach(function (phrase) {
        var ts = words(phrase), lists = ts.map(function (w) { return self.post[w]; });
        if (lists.some(function (l) { return !l; })) return;
        var acc = Object.create(null), count = Object.create(null);
        lists.forEach(function (l, li) {
          var idf = self.idf(ts[li]);
          for (var j = 0; j < l.length; j += 2) { acc[l[j]] = (acc[l[j]] || 0) + l[j + 1] * idf; count[l[j]] = (count[l[j]] || 0) + 1; }
        });
        var w = ts.length > 1 ? 0.7 / Math.sqrt(ts.length) : 0.45;
        // A record that already has the word itself keeps its highlights to that word.
        for (var d in acc) {
          if (count[d] !== ts.length) continue;
          var direct = LOOSE[t] && matched[d] && !synOnly[d];
          if (!matched[d]) synOnly[d] = 1;
          credit(+d, w * acc[d], direct ? [] : ts);
        }
      });
      for (var d in best) {
        var h = hits[d] || (hits[d] = { s: 0, n: 0, m: Object.create(null) });
        h.s += best[d]; h.n++;
        matched[d].forEach(function (w) { h.m[w] = 1; });
      }
    });
    var ids = Object.keys(hits), need = qw.length;
    var full = ids.filter(function (d) { return hits[d].n === need; });
    if (!full.length && need > 2) full = ids.filter(function (d) { return hits[d].n >= need - 1; });
    var phrase = " " + qw.join(" ") + " ";
    var out = full.map(function (d) {
      var r = docs[d], h = hits[d], s = h.s;
      if (need > 1 && r._t.indexOf(phrase) >= 0) s *= 2;
      else if (need > 1 && r._b.indexOf(phrase) >= 0) s *= 1.4;
      if (r._t === phrase || r._n === phrase) s *= 1.6;
      if (r.u.indexOf("#") < 0) s *= 1.15;
      return { doc: r, score: s, terms: h.m };
    }).sort(function (a, b) { return b.score - a.score; });
    this.lastMs = (window.performance || Date).now() - t0;
    return out;
  };
  // A close word from the vocabulary, for "did you mean".
  Engine.prototype.suggest = function (q) {
    var qw = queryWords(q), self = this, changed = false;
    var fixed = qw.map(function (t) {
      if (self.post[t] || t.length < 4) return t;
      var best = null, bd = 4;
      self.vocab.forEach(function (c) {
        if (Math.abs(c.length - t.length) > 3) return;
        var d = dist(t, c, 3);
        if (d < bd || (d === bd && best && self.post[c].length > self.post[best].length)) { bd = d; best = c; }
      });
      if (best) { changed = true; return best; }
      return t;
    });
    return changed ? fixed.join(" ") : "";
  };

  // ---- snippets and highlighting -------------------------------------------
  var WORD = /[0-9A-Za-zÀ-ɏ]+(?:-[0-9]{3})?/g;
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function isHit(word, terms) {
    var w = words(word);
    return w.length === 1 && !STOP[w[0]] && terms[w[0]] === 1;
  }
  function mark(text, terms) {
    var out = "", last = 0, m;
    WORD.lastIndex = 0;
    while ((m = WORD.exec(text))) {
      if (isHit(m[0], terms)) {
        out += esc(text.slice(last, m.index)) + "<mark>" + esc(m[0]) + "</mark>";
        last = m.index + m[0].length;
      }
    }
    return out + esc(text.slice(last));
  }
  function snippet(text, terms, size) {
    if (!text) return "";
    size = size || 170;
    var pos = [], m;
    WORD.lastIndex = 0;
    while ((m = WORD.exec(text))) if (isHit(m[0], terms)) pos.push(m.index);
    var start = 0;
    if (pos.length) {
      var bestN = -1;
      pos.forEach(function (p) {
        var n = pos.filter(function (q) { return q >= p && q < p + size - 40; }).length;
        if (n > bestN) { bestN = n; start = p; }
      });
      start = Math.max(0, start - 40);
      if (start > 0) { var sp = text.indexOf(" ", start); start = sp >= 0 && sp < start + 20 ? sp + 1 : start; }
    }
    var end = Math.min(text.length, start + size);
    if (end < text.length) { var e = text.lastIndexOf(" ", end); if (e > start + size * 0.6) end = e; }
    return (start > 0 ? "…" : "") + mark(text.slice(start, end), terms) + (end < text.length && !/…$/.test(text.slice(start, end)) ? "…" : "");
  }

  // ---- index loading --------------------------------------------------------
  var engine = null, loading = null;
  function load() {
    if (!loading) {
      loading = fetch(root + "assets/search-index.json", { cache: "no-cache" })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (data) { engine = new Engine(data); return engine; });
      loading.catch(function () { loading = null; });
    }
    return loading;
  }

  // ---- recent searches (this browser only) --------------------------------
  var RECENT = "nb-search-recent";
  function recent() {
    try { var a = JSON.parse(localStorage.getItem(RECENT) || "[]"); return Array.isArray(a) ? a.slice(0, 6) : []; }
    catch (e) { return []; }
  }
  function remember(q) {
    q = String(q || "").trim();
    if (q.length < 2) return;
    try {
      var a = recent().filter(function (x) { return x.toLowerCase() !== q.toLowerCase(); });
      a.unshift(q);
      localStorage.setItem(RECENT, JSON.stringify(a.slice(0, 6)));
    } catch (e) { /* storage blocked: nothing to remember */ }
  }
  function forget() { try { localStorage.removeItem(RECENT); } catch (e) { /* ignore */ } }

  // ---- the search box (overlay and search page share it) ------------------
  var uid = 0;
  function UI(opts) {
    this.id = "srch" + (++uid);
    this.modal = !!opts.modal;
    this.input = opts.input;
    this.box = opts.box;
    this.filter = "all";
    this.results = [];
    this.active = -1;
    this.onOpen = opts.onOpen || function () {};
    var self = this, id = this.id;
    this.box.insertAdjacentHTML("beforeend",
      '<div class="srch-chips" role="group" aria-label="Show only"></div>' +
      '<p class="srch-status" id="' + id + '-status" role="status" aria-live="polite"></p>' +
      '<div class="srch-list" id="' + id + '-list" role="listbox" aria-label="Search results"></div>' +
      '<div class="srch-empty"></div>');
    this.chips = this.box.querySelector(".srch-chips");
    this.status = this.box.querySelector(".srch-status");
    this.list = this.box.querySelector(".srch-list");
    this.empty = this.box.querySelector(".srch-empty");
    var inp = this.input;
    inp.setAttribute("role", "combobox");
    inp.setAttribute("aria-autocomplete", "list");
    inp.setAttribute("aria-controls", id + "-list");
    inp.setAttribute("aria-expanded", "false");
    inp.setAttribute("aria-describedby", id + "-status");
    // A query takes a few milliseconds, so results follow every keystroke.
    inp.addEventListener("input", function () { self.run(); });
    inp.addEventListener("keydown", function (e) { self.key(e); });
    this.chips.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-k]");
      if (!b) return;
      self.filter = b.getAttribute("data-k");
      self.run();
    });
    this.list.addEventListener("click", function (e) {
      var o = e.target.closest("[role=option]");
      if (!o) return;
      if (o.hasAttribute("data-more")) { e.preventDefault(); self.filter = o.getAttribute("data-more"); self.run(); inp.focus(); return; }
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) { remember(inp.value); return; }
      e.preventDefault();
      self.go(o);
    });
    this.list.addEventListener("mousemove", function (e) {
      var o = e.target.closest("[role=option]");
      if (o) self.move(self.options().indexOf(o), true);
    });
    this.empty.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.hasAttribute("data-clear")) { forget(); self.run(); inp.focus(); return; }
      inp.value = b.getAttribute("data-q");
      self.run();
      inp.focus();
    });
  }
  UI.prototype.options = function () { return Array.prototype.slice.call(this.list.querySelectorAll("[role=option]")); };
  UI.prototype.move = function (i, quiet) {
    var opts = this.options();
    if (!opts.length) { this.active = -1; this.input.removeAttribute("aria-activedescendant"); return; }
    i = (i + opts.length) % opts.length;
    opts.forEach(function (o, k) { o.setAttribute("aria-selected", k === i ? "true" : "false"); });
    this.active = i;
    this.input.setAttribute("aria-activedescendant", opts[i].id);
    if (!quiet) opts[i].scrollIntoView({ block: "nearest" });
  };
  UI.prototype.key = function (e) {
    var opts = this.options();
    if (e.key === "ArrowDown") { e.preventDefault(); this.move(this.active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); this.move(this.active < 0 ? opts.length - 1 : this.active - 1); }
    else if (e.key === "Enter") {
      e.preventDefault();
      var o = opts[this.active >= 0 ? this.active : 0];
      if (!o) return;
      if (o.hasAttribute("data-more")) { this.filter = o.getAttribute("data-more"); this.run(); return; }
      this.go(o, e.metaKey || e.ctrlKey);
    }
  };
  UI.prototype.go = function (o, newTab) {
    var a = o.querySelector("a");
    remember(this.input.value);
    if (newTab) { window.open(a.href, "_blank", "noopener"); return; }
    this.onOpen();
    location.href = a.href;
  };
  UI.prototype.chipRow = function (counts) {
    var self = this;
    this.chips.innerHTML = CHIPS.map(function (c) {
      var n = c[0] === "all" ? counts.all : (counts[c[0]] || 0);
      var on = self.filter === c[0];
      return '<button type="button" class="srch-chip k-' + c[0] + '" data-k="' + c[0] + '" aria-pressed="' + on + '"' +
        (n || on ? "" : " disabled") + ">" + esc(c[1]) + (counts.q ? ' <span class="n">' + n + "</span>" : "") + "</button>";
    }).join("");
  };
  UI.prototype.run = function () {
    var self = this, q = this.input.value.trim();
    if (this.onQuery) this.onQuery(q);
    if (!engine) {
      this.status.textContent = "Opening the index…";
      load().then(function () { self.run(); }, function () {
        self.status.textContent = "The search index did not load. The list of every page still works.";
      });
      return;
    }
    if (!q || !queryWords(q).length) return this.idle();
    var res = engine.search(q), counts = { all: res.length, q: true }, groups = {}, order = [];
    res.forEach(function (r) {
      var k = r.doc.k;
      counts[k] = (counts[k] || 0) + 1;
      if (!groups[k]) { groups[k] = []; order.push(k); }
      groups[k].push(r);
    });
    if (this.filter !== "all" && !counts[this.filter]) this.filter = "all";
    this.chipRow(counts);
    this.empty.innerHTML = "";
    if (!res.length) return this.none(q);
    var shown = this.filter === "all" ? order : [this.filter], id = this.id, n = 0, out = "";
    shown.forEach(function (k) {
      var list = groups[k], cap = self.filter === "all" ? PER_GROUP : PER_FILTER, gid = id + "-g-" + k;
      out += '<div class="srch-group k-' + k + '" role="group" aria-labelledby="' + gid + '">' +
        '<p class="srch-gh" id="' + gid + '"><span class="srch-gl">' + esc(LABELS[k]) + '</span> <span class="srch-gc">' +
        list.length + '<span class="sr-only"> results</span></span></p>';
      list.slice(0, cap).forEach(function (r, i) {
        var d = r.doc, meta = [d.d, d.g && d.k === "course" ? d.g.split(" · ")[0] : ""].filter(Boolean).join(" · ");
        out += '<div class="srch-card" role="option" id="' + id + "-o" + (n++) + '" aria-selected="false" style="--r:' + ((i % 3) - 1) * 0.35 + 'deg">' +
          '<a href="' + esc(root + d.u || "./") + '" tabindex="-1">' +
          (d.p ? '<span class="srch-crumb">' + esc(d.p) + " ›</span>" : "") +
          '<span class="srch-t">' + mark(d.t, r.terms) + "</span>" +
          (meta ? '<span class="srch-meta">' + esc(meta) + "</span>" : "") +
          (d.b ? '<span class="srch-snip">' + snippet(d.b, r.terms) + "</span>" : "") +
          "</a></div>";
      });
      if (list.length > cap) {
        out += '<div class="srch-more" role="option" id="' + id + "-o" + (n++) + '" aria-selected="false" data-more="' + k + '">' +
          "<a tabindex=\"-1\">Show all " + list.length + " in " + esc(LABELS[k]) + " →</a></div>";
      }
      out += "</div>";
    });
    this.list.innerHTML = out;
    this.input.setAttribute("aria-expanded", "true");
    var inView = this.filter === "all" ? res.length : counts[this.filter];
    this.status.textContent = inView + (inView === 1 ? " result" : " results") + " for “" + q + "”" +
      (this.filter === "all" ? "" : " in " + LABELS[this.filter]) + " · " + Math.max(1, Math.round(engine.lastMs)) + " ms";
    this.move(0, true);
    this.list.scrollTop = 0;
  };
  UI.prototype.idle = function () {
    this.chips.innerHTML = "";
    this.list.innerHTML = "";
    this.input.setAttribute("aria-expanded", "false");
    this.input.removeAttribute("aria-activedescendant");
    this.active = -1;
    this.status.textContent = "";
    var r = recent(), out = "";
    if (r.length) {
      out += '<div class="srch-try"><p class="srch-gh"><span class="srch-gl">Recent searches</span></p><div class="srch-pills">' +
        r.map(function (q) { return '<button type="button" class="srch-pill recent" data-q="' + esc(q) + '" data-ga-label="recent search">' + esc(q) + "</button>"; }).join("") +
        '<button type="button" class="srch-clear" data-clear data-ga-label="clear recent searches">clear</button></div></div>';
    }
    out += '<div class="srch-try"><p class="srch-gh"><span class="srch-gl">Try</span></p><div class="srch-pills">' +
      TRY.map(function (q) { return '<button type="button" class="srch-pill" data-q="' + esc(q) + '">' + esc(q) + "</button>"; }).join("") +
      "</div></div>";
    this.empty.innerHTML = out;
  };
  UI.prototype.none = function (q) {
    this.list.innerHTML = "";
    this.chips.innerHTML = "";
    this.input.setAttribute("aria-expanded", "false");
    this.input.removeAttribute("aria-activedescendant");
    this.active = -1;
    this.status.textContent = "No results for “" + q + "”";
    var fix = engine.suggest(q), out = '<p class="srch-none">Nothing in the notebook for “' + esc(q) + '”.</p>';
    if (fix) out += '<p class="srch-none-sub">Did you mean <button type="button" class="srch-pill" data-q="' + esc(fix) + '">' + esc(fix) + "</button>?</p>";
    out += '<p class="srch-none-sub">Fewer words usually help, or try one of these:</p><div class="srch-pills">' +
      TRY.map(function (t) { return '<button type="button" class="srch-pill" data-q="' + esc(t) + '">' + esc(t) + "</button>"; }).join("") + "</div>";
    this.empty.innerHTML = out;
  };

  // ---- the overlay ------------------------------------------------------------
  var overlay = null, ui = null, opener = null;
  var GLASS = '<svg class="srch-glass" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M10.6 4.2c3.7-.3 6.6 2.5 6.5 6.1-.1 3.5-3 6.3-6.6 6.2-3.5-.1-6.2-3-6.1-6.4.1-3.2 2.8-5.7 6.2-5.9Z"/><path d="M15.4 15.6c1.6 1.5 3.3 3.1 4.9 4.8"/></svg>';
  function build() {
    overlay = doc.createElement("div");
    overlay.className = "srch";
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="srch-backdrop" data-close></div>' +
      '<div class="srch-dialog" role="dialog" aria-modal="true" aria-labelledby="srch-title">' +
      '<div class="srch-top"><div class="srch-pad">' +
      '<label class="srch-label" id="srch-title" for="srch-q">Search the notebook</label>' +
      '<div class="srch-row">' + GLASS +
      '<input id="srch-q" type="search" placeholder="search courses, projects, talks..." autocomplete="off" spellcheck="false" enterkeyhint="go">' +
      '<button type="button" class="srch-x" data-close aria-label="Close search">esc</button></div></div></div>' +
      '<div class="srch-body"></div>' +
      '<p class="srch-keys" aria-hidden="true"><kbd>↑</kbd><kbd>↓</kbd> move <kbd>Enter</kbd> open <kbd>Esc</kbd> close <a href="' + root + 'search/">search page →</a></p>' +
      "</div>";
    doc.body.appendChild(overlay);
    ui = new UI({ modal: true, input: overlay.querySelector("#srch-q"), box: overlay.querySelector(".srch-body"), onOpen: close });
    overlay.addEventListener("click", function (e) { if (e.target.closest("[data-close]")) close(); });
    overlay.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); close(); return; }
      if (e.key !== "Tab") return;
      var f = Array.prototype.filter.call(overlay.querySelectorAll("input, button:not([disabled]), a[href]:not([tabindex='-1'])"),
        function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  function open(q) {
    var page = pageUI();
    if (page) { page.input.focus(); page.input.select(); return; }
    if (!overlay) build();
    if (!overlay.hidden) { ui.input.focus(); return; }
    opener = doc.activeElement;
    overlay.hidden = false;
    html.classList.add("srch-open");
    if (typeof q === "string") ui.input.value = q;
    ui.run();
    ui.input.focus();
    ui.input.select();
  }
  function close() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    html.classList.remove("srch-open");
    if (opener && opener.focus && doc.contains(opener)) opener.focus();
    opener = null;
  }

  // ---- the search page --------------------------------------------------------
  var pageCtl;
  function pageUI() {
    if (pageCtl !== undefined) return pageCtl;
    var mount = doc.querySelector("[data-search-page]");
    if (!mount) return (pageCtl = null);
    var input = doc.getElementById("srch-page-q"), all = doc.getElementById("every-page");
    var form = input.form;
    pageCtl = new UI({ modal: false, input: input, box: mount });
    pageCtl.onQuery = function (q) {
      if (all) all.hidden = !!q;
      try { history.replaceState(null, "", q ? "?q=" + encodeURIComponent(q) : location.pathname); } catch (e) { /* file:// */ }
    };
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    var q = new URLSearchParams(location.search).get("q");
    if (q) input.value = q;
    pageCtl.run();
    return pageCtl;
  }

  // ---- wiring -------------------------------------------------------------------
  function typing(el) {
    return el && (el.isContentEditable || /^(input|textarea|select)$/i.test(el.tagName));
  }
  doc.addEventListener("keydown", function (e) {
    if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey) && !e.altKey) {
      e.preventDefault();
      if (overlay && !overlay.hidden) close(); else open();
    } else if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey && !typing(e.target)) {
      e.preventDefault();
      open();
    }
  });
  doc.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-search-open]");
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault();
    open();
  });
  // Fetch the index as soon as someone heads for the search tab.
  ["pointerenter", "focusin", "touchstart"].forEach(function (ev) {
    doc.addEventListener(ev, function (e) {
      if (e.target.closest && e.target.closest("[data-search-open]")) load();
    }, { passive: true, capture: true });
  });
  if (doc.querySelector("[data-search-page]")) pageUI();

  // For tests and the curious: siteSearch.query("data mining").
  window.siteSearch = {
    open: open, close: close, ready: function () { return load(); },
    query: function (q) { return engine ? engine.search(q) : null; },
    lastMs: function () { return engine ? engine.lastMs : null; }
  };
})();
