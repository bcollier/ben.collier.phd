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

  fetch(root + "assets/vendor/countries-110m.json").then(function (r) { return r.json(); }).then(function (world) {
    const countries = topojson.feature(world, world.objects.countries).features.filter(function (f) { return f.id !== "010"; });
    const projection = d3.geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: "FeatureCollection", features: countries });
    const path = d3.geoPath(projection);
    svg.append("path").attr("class", "m-sphere").attr("d", path({ type: "Sphere" }));
    landPaths = svg.append("g").selectAll("path").data(countries).join("path")
      .attr("class", function (d) { return byId.has(String(+d.id)) ? "g-land visited" : "g-land"; })
      .attr("d", path)
      .on("click", function (e, d) { const p = byId.get(String(+d.id)); if (p) pin(p); });
    dotNodes = svg.append("g").selectAll("g").data(places).join("g").attr("class", "g-dot m-dot")
      .attr("transform", function (p) { const xy = projection([p.lon, p.lat]); p._xy = xy; return "translate(" + xy[0] + "," + xy[1] + ")"; })
      .attr("tabindex", 0).attr("role", "button").attr("aria-label", function (p) { return p.name + ": photos"; })
      .on("focus", function (e, p) { show(p); })
      .on("click", function (e, p) { pin(p); })
      .on("keydown", function (e, p) { if (e.key === "Enter" || e.key === " ") { pin(p); e.preventDefault(); } });
    // One pointer tracker instead of per-shape enter/leave events: the nearest
    // dot within reach wins, otherwise the visited country under the pointer.
    let target = null;
    svg.on("pointermove", function (e) {
      const m = d3.pointer(e);
      let best = null, dist = 16;
      places.forEach(function (p) { const d = Math.hypot(p._xy[0] - m[0], p._xy[1] - m[1]); if (d < dist) { dist = d; best = p; } });
      if (!best && e.target.__data__ && e.target.classList.contains("visited")) best = byId.get(String(+e.target.__data__.id));
      if (best === target) return;
      target = best;
      if (best) show(best); else softHide();
    });
    svg.on("pointerleave", function () { target = null; softHide(); });
    dotNodes.append("circle").attr("class", "hit").attr("r", 9);
    dotNodes.append("circle").attr("class", "pulse").attr("r", 7);
    dotNodes.append("circle").attr("class", "core").attr("r", function (p) { return 3 + Math.min(3, Math.log10(p.count)); });
  });

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

  // A curved line from the dot to the card's nearest corner, drawn on.
  function drawLeader(p) {
    if (!leader) leader = svg.append("path").attr("class", "m-leader");
    const box = mount.getBoundingClientRect(), cb = pop.getBoundingClientRect();
    if (!box.width || getComputedStyle(pop).position !== "absolute") { leader.attr("d", null); return; }
    const k = W / box.width;
    const cx = (cb.right - box.left) * k, cy = (cb.top - box.top) * k + 18;
    const [x, y] = p._xy;
    const mx = (x + cx) / 2, my = Math.min(y, cy) - 40;
    leader.attr("d", "M" + x + "," + y + " Q" + mx + "," + my + " " + cx + "," + cy);
    const len = leader.node().getTotalLength();
    leader.interrupt().attr("stroke-dasharray", len).attr("stroke-dashoffset", len).style("opacity", 1)
      .transition().duration(520).ease(d3.easeCubicOut).attr("stroke-dashoffset", 0);
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
