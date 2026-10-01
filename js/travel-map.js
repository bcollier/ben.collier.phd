// Travel map: every visited country at once on a flat Natural Earth map.
// Hovering a dot or a shaded country shows a small popup of photos next to
// it; clicking pins the popup, and clicking a photo opens it full size. The
// tabs switch to the globe, which starts drawing only when first shown.
(function () {
  const mount = document.getElementById("worldmap");
  const dataEl = document.getElementById("travel-data");
  if (!mount || !dataEl || !window.d3 || !window.topojson) return;
  const root = document.documentElement.getAttribute("data-root") || "";
  const places = JSON.parse(dataEl.textContent).countries;
  const byId = new Map(places.map(function (p) { return [String(+p.id), p]; }));
  const pop = document.getElementById("map-pop");
  const wrap = document.getElementById("view-map");
  const viewer = document.getElementById("photo-view");
  const W = 960, H = 500;

  const svg = d3.select(mount).append("svg").attr("viewBox", "0 0 " + W + " " + H)
    .attr("role", "img").attr("aria-label", "A world map marking the " + places.length + " countries I have visited");
  let dotNodes, landPaths, pinned = null, shown = null, hideTimer = null;

  fetch(root + "assets/vendor/countries-110m.json").then(function (r) { return r.json(); }).then(function (atlas) {
    const countries = topojson.feature(atlas, atlas.objects.countries).features.filter(function (f) { return f.id !== "010"; });
    const projection = d3.geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: "FeatureCollection", features: countries });
    const path = d3.geoPath(projection);
    const world = svg.append("g").attr("class", "m-world");
    world.append("path").attr("class", "m-sphere").attr("d", path({ type: "Sphere" }));
    landPaths = world.append("g").selectAll("path").data(countries).join("path")
      .attr("class", function (d) { return byId.has(String(+d.id)) ? "g-land visited" : "g-land"; })
      .attr("d", path)
      .on("click", function (e, d) { const p = byId.get(String(+d.id)); if (p) pin(p); });
    places.forEach(function (p) { p._xy = projection([p.lon, p.lat]); });

    // Some countries' photos sit almost on top of a neighbour's (Rome and the
    // Vatican, Copenhagen and Malmo, Singapore and Johor Bahru). Those twins
    // are nudged apart along their real bearing by a fixed number of screen
    // pixels at every zoom, so both dots stay visible and clickable.
    const TWIN = 4, SEP = 16;
    places.forEach(function (p) {
      p._nudge = [0, 0];
      places.forEach(function (q) {
        if (q === p) return;
        const dx = p._xy[0] - q._xy[0], dy = p._xy[1] - q._xy[1], d = Math.hypot(dx, dy);
        if (d >= TWIN) return;
        const ux = d ? dx / d : (p.name < q.name ? -1 : 1), uy = d ? dy / d : 0;
        p._nudge[0] += ux * SEP / 2; p._nudge[1] += uy * SEP / 2;
      });
    });
    pos = function (p, k) { return [p._xy[0] + p._nudge[0] / k, p._xy[1] + p._nudge[1] / k]; };

    // Labels go on the side away from a close neighbour, and at full view a
    // label only shows when the dot has room around it.
    places.forEach(function (p) {
      const near = places.filter(function (q) { return q !== p && Math.hypot(q._xy[0] - p._xy[0], q._xy[1] - p._xy[1]) < 45; });
      // At full view, a dot with at most two neighbours gets a label when the
      // greedy placement below finds room (Australia beside New Zealand,
      // Iceland near the British Isles); crowded Europe waits for the zoom.
      p._roomy = near.length <= 2;
      const right = near.filter(function (q) { return q._xy[0] >= p._xy[0] && Math.abs(q._xy[1] - p._xy[1]) < 12; }).length;
      const left = near.filter(function (q) { return q._xy[0] < p._xy[0] && Math.abs(q._xy[1] - p._xy[1]) < 12; }).length;
      p._left = right > left || (right > 0 && right === left && p.count < 100);
    });

    dotNodes = world.append("g").selectAll("g").data(places).join("g").attr("class", "g-dot m-dot")
      .attr("tabindex", 0).attr("role", "button").attr("aria-label", function (p) { return p.name + ": photos"; })
      .on("focus", function (e, p) { zoomFor(p); show(p); })
      .on("click", function (e, p) { pin(p); })
      .on("keydown", function (e, p) { if (e.key === "Enter" || e.key === " ") { pin(p); e.preventDefault(); } });
    dotNodes.append("circle").attr("class", "hit").attr("r", 9);
    dotNodes.append("circle").attr("class", "pulse").attr("r", 7);
    dotNodes.append("circle").attr("class", "core").attr("r", function (p) { return 3 + Math.min(3, Math.log10(p.count)); });
    dotNodes.append("text").attr("class", "m-label")
      .attr("x", 8).attr("dy", "0.35em")
      .attr("text-anchor", function (p) { return p._left ? "end" : "start"; })
      .text(function (p) { return p.name; });

    // Zoom: hovering a crowded region (Europe, the Gulf, Southeast Asia)
    // eases the map in so each country is easy to pick out. Dots and labels
    // keep their size; leaving the region eases back out.
    let view = { k: 1, x: W / 2, y: H / 2 }, zone = null;
    function crowd(p) {
      const near = places.filter(function (q) { return Math.hypot(q._xy[0] - p._xy[0], q._xy[1] - p._xy[1]) < 70; });
      if (near.length < 3) return null;
      const xs = near.map(function (q) { return q._xy[0]; }), ys = near.map(function (q) { return q._xy[1]; });
      const x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
      const k = Math.max(1.8, Math.min(7, 0.55 * W / (x1 - x0 + 40), 0.55 * H / (y1 - y0 + 40)));
      return { x: (x0 + x1) / 2, y: (y0 + y1) / 2, k: k, r: Math.max(x1 - x0, y1 - y0) / 2 + 40, members: near };
    }
    // Greedy label placement at a given zoom: try right, left, above, below,
    // and skip a spot that would collide with a label or dot already placed.
    function placeLabels(v, show) {
      const boxes = [], at = function (p) { const q = pos(p, v.k); return [(q[0] - v.x) * v.k, (q[1] - v.y) * v.k]; };
      places.forEach(function (p) { const s = at(p); boxes.push([s[0] - 5, s[1] - 5, s[0] + 5, s[1] + 5]); });
      const hit = function (b) { return boxes.some(function (o) { return b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1]; }); };
      const order = places.filter(show).sort(function (a, b) { return b.count - a.count; });
      dotNodes.select(".m-label").style("display", "none");
      order.forEach(function (p) {
        const s = at(p), w = p.name.length * 5.9 + 4, h = 12;
        const spots = [["start", 8, 0, [s[0] + 7, s[1] - h / 2, s[0] + 7 + w, s[1] + h / 2]],
                       ["end", -8, 0, [s[0] - 7 - w, s[1] - h / 2, s[0] - 7, s[1] + h / 2]],
                       ["middle", 0, -12, [s[0] - w / 2, s[1] - 18, s[0] + w / 2, s[1] - 6]],
                       ["middle", 0, 14, [s[0] - w / 2, s[1] + 7, s[0] + w / 2, s[1] + 19]]];
        if (p._left) spots.unshift(spots.splice(1, 1)[0]);
        const spot = spots.find(function (c) { return !hit(c[3]); });
        if (!spot) return;
        boxes.push(spot[3]);
        dotNodes.filter(function (d) { return d === p; }).select(".m-label")
          .style("display", null).attr("text-anchor", spot[0]).attr("x", spot[1]).attr("y", spot[2]);
      });
    }
    function apply(v) {
      const tx = W / 2 - v.x * v.k, ty = H / 2 - v.y * v.k;
      world.attr("transform", "translate(" + tx + "," + ty + ") scale(" + v.k + ")");
      dotNodes.attr("transform", function (p) { const q = pos(p, v.k); return "translate(" + q[0] + "," + q[1] + ") scale(" + (1 / v.k) + ")"; });
      landPaths.style("stroke-width", 0.4 / v.k);
      view = v;
      if (shown) placeLeader(shown);
    }
    function labelsFor(v) {
      const z = zone;
      placeLabels(v, function (p) { return v.k > 1.2 ? (z && z.members.indexOf(p) >= 0) : p._roomy; });
      dotNodes.classed("labelled", true);
    }
    function zoomTo(v) {
      const from = view, i = d3.interpolate(from, v);
      labelsFor(v);
      svg.interrupt().transition().duration(still ? 0 : 650).ease(d3.easeCubicInOut).tween("zoom", function () { return function (t) { apply(i(t)); }; });
    }
    zoomFor = function (p) {
      const c = crowd(p);
      if (c && (!zone || Math.hypot(c.x - zone.x, c.y - zone.y) > 20)) { zone = c; zoomTo({ k: c.k, x: c.x, y: c.y }); }
      else if (!c && zone) { zone = null; zoomTo({ k: 1, x: W / 2, y: H / 2 }); }
    };
    toScreen = function (p) { const q = pos(p, view.k); return [W / 2 + (q[0] - view.x) * view.k, H / 2 + (q[1] - view.y) * view.k]; };
    apply(view);
    labelsFor(view);

    // One pointer tracker: the nearest dot within reach wins, otherwise the
    // visited country under the pointer.
    let target = null;
    svg.on("pointermove", function (e) {
      const m = d3.pointer(e, world.node());
      let best = null, dist = 16 / view.k;
      places.forEach(function (p) { const q = pos(p, view.k), d = Math.hypot(q[0] - m[0], q[1] - m[1]); if (d < dist) { dist = d; best = p; } });
      if (!best && e.target.__data__ && e.target.classList.contains("visited")) best = byId.get(String(+e.target.__data__.id));
      if (zone && !pinned && Math.hypot(m[0] - zone.x, m[1] - zone.y) > zone.r && (!best || zone.members.indexOf(best) < 0)) {
        zone = null; zoomTo({ k: 1, x: W / 2, y: H / 2 });
      }
      if (best === target) return;
      target = best;
      if (best) { zoomFor(best); show(best); } else softHide();
    });
    svg.on("pointerleave", function () {
      target = null; softHide();
      if (zone && !pinned) { zone = null; zoomTo({ k: 1, x: W / 2, y: H / 2 }); }
    });
  });

  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let zoomFor = function () {}, toScreen = function (p) { return p._xy; }, pos = function (p) { return p._xy; };

  function years(p) {
    return p.years.length ? (p.years[0] === p.years[1] ? p.years[0] : p.years[0] + " to " + p.years[1]) : "";
  }

  // The card docks in the empty South Pacific corner instead of covering the
  // map. A leader line draws from the dot to the card, the card rises in, and
  // its thumbnails follow one after another. Hover has a short intent delay so
  // sweeping the pointer across Europe does not flicker.
  let leader = null, intent = null;
  function show(p) {
    clearTimeout(hideTimer);
    if (pinned && pinned !== p) return;
    clearTimeout(intent);
    intent = setTimeout(function () { render(p); }, shown ? 60 : 110);
  }
  function render(p) {
    if (shown === p) { reveal(); return; }
    const swap = !!shown;
    shown = p;
    const fill = function () {
      pop.innerHTML = '<div class="mp-head"><strong>' + p.name + '</strong><span>' + [years(p), p.photos.length + (p.photos.length === 1 ? " photo" : " photos")].filter(Boolean).join(" · ") + '</span></div><div class="mp-thumbs">' +
        p.photos.slice(0, 8).map(function (ph, i) {
          return '<button type="button" data-i="' + i + '" style="--i:' + i + '" aria-label="' + p.name + ', ' + ph.place + '"><img src="' + root + ph.src.replace(".webp", "-t.webp") + '" alt=""></button>';
        }).join("") + "</div>";
      pop.querySelectorAll("button").forEach(function (b) {
        b.addEventListener("click", function () { open(p, +b.dataset.i); });
      });
      pop.classList.remove("swap"); void pop.offsetWidth; pop.classList.add("swap");
      reveal();
      drawLeader(p);
    };
    if (swap && pop.classList.contains("show")) { pop.classList.add("out"); setTimeout(function () { pop.classList.remove("out"); fill(); }, 140); }
    else fill();
    if (dotNodes) dotNodes.classed("on", function (d) { return d === p; });
  }
  function reveal() { pop.hidden = false; void pop.offsetWidth; pop.classList.add("show"); }

  // A curved line from the dot to the card's nearest corner, drawn on. It
  // follows the dot while the map zooms.
  function leaderPath(p) {
    const box = mount.getBoundingClientRect(), cb = pop.getBoundingClientRect();
    if (!box.width || getComputedStyle(pop).position !== "absolute") return null;
    const k = W / box.width;
    const cx = (cb.right - box.left) * k, cy = (cb.top - box.top) * k + 18;
    const xy = toScreen(p);
    const mx = (xy[0] + cx) / 2, my = Math.min(xy[1], cy) - 40;
    return "M" + xy[0] + "," + xy[1] + " Q" + mx + "," + my + " " + cx + "," + cy;
  }
  function placeLeader(p) {
    if (!leader) return;
    const d = leaderPath(p);
    if (d) leader.attr("d", d).attr("stroke-dasharray", null).attr("stroke-dashoffset", null);
  }
  function drawLeader(p) {
    if (!leader) leader = svg.append("path").attr("class", "m-leader");
    const d = leaderPath(p);
    if (!d) { leader.attr("d", null); return; }
    leader.attr("d", d);
    const len = leader.node().getTotalLength();
    leader.interrupt().attr("stroke-dasharray", len).attr("stroke-dashoffset", len).style("opacity", 1)
      .transition().duration(520).ease(d3.easeCubicOut).attr("stroke-dashoffset", 0)
      .on("end", function () { leader.attr("stroke-dasharray", null).attr("stroke-dashoffset", null); });
  }

  function softHide() {
    clearTimeout(intent);
    if (pinned) return;
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function () {
      pop.classList.remove("show"); shown = null;
      if (leader) leader.transition().duration(200).style("opacity", 0);
      if (dotNodes) dotNodes.classed("on", false);
      setTimeout(function () { if (!shown) pop.hidden = true; }, 260);
    }, 700);
  }
  pop.addEventListener("mouseenter", function () { clearTimeout(hideTimer); });
  pop.addEventListener("mouseleave", softHide);

  function pin(p) {
    pinned = null;
    clearTimeout(intent); clearTimeout(hideTimer);
    zoomFor(p);
    render(p);
    pinned = p;
    pop.classList.add("pinned");
    document.querySelectorAll(".country-list button").forEach(function (b) { b.classList.toggle("on", b.dataset.cc === p.cc); });
  }
  document.addEventListener("click", function (e) {
    if (!pinned || pop.contains(e.target) || e.target.closest(".m-dot, .g-land.visited, .country-list")) return;
    pinned = null; pop.classList.remove("pinned"); softHide();
  });

  function open(p, i) {
    const ph = p.photos[i];
    viewer.querySelector("img").src = root + ph.src;
    viewer.querySelector("img").alt = p.name + ", " + ph.place;
    viewer.querySelector("p").textContent = p.name + " · " + ph.place + " · " + ph.date.slice(0, 4);
    if (viewer.showModal) viewer.showModal();
  }
  viewer.querySelector("button").addEventListener("click", function () { viewer.close(); });
  viewer.addEventListener("click", function (e) { if (e.target === viewer) viewer.close(); });

  document.querySelectorAll(".country-list button").forEach(function (b) {
    b.addEventListener("click", function () {
      if (wrap.hidden) return;
      const p = places.find(function (x) { return x.cc === b.dataset.cc; });
      pin(p);
      wrap.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });

  // Map and globe tabs. The globe is only built the first time it is shown.
  let globeStarted = false;
  document.querySelectorAll(".view-tabs button").forEach(function (t) {
    t.addEventListener("click", function () {
      const globe = t.dataset.view === "globe";
      document.querySelectorAll(".view-tabs button").forEach(function (b) { b.setAttribute("aria-selected", String(b === t)); });
      wrap.hidden = globe;
      document.getElementById("view-globe").hidden = !globe;
      if (globe && !globeStarted && window.startGlobe) { globeStarted = true; window.startGlobe(); }
      pinned = null; pop.classList.remove("show"); pop.hidden = true; shown = null; if (leader) leader.style("opacity", 0);
    });
  });
})();
