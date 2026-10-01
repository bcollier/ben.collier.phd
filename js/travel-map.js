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
      .on("mouseenter", function (e, d) { const p = byId.get(String(+d.id)); if (p) show(p); })
      .on("mouseleave", softHide)
      .on("click", function (e, d) { const p = byId.get(String(+d.id)); if (p) pin(p); });
    dotNodes = svg.append("g").selectAll("g").data(places).join("g").attr("class", "g-dot m-dot")
      .attr("transform", function (p) { const xy = projection([p.lon, p.lat]); p._xy = xy; return "translate(" + xy[0] + "," + xy[1] + ")"; })
      .attr("tabindex", 0).attr("role", "button").attr("aria-label", function (p) { return p.name + ": photos"; })
      .on("mouseenter", function (e, p) { show(p); })
      .on("mouseleave", softHide)
      .on("focus", function (e, p) { show(p); })
      .on("click", function (e, p) { pin(p); })
      .on("keydown", function (e, p) { if (e.key === "Enter" || e.key === " ") { pin(p); e.preventDefault(); } });
    dotNodes.append("circle").attr("class", "hit").attr("r", 9);
    dotNodes.append("circle").attr("class", "pulse").attr("r", 7);
    dotNodes.append("circle").attr("class", "core").attr("r", function (p) { return 3 + Math.min(3, Math.log10(p.count)); });
  });

  function years(p) {
    return p.years.length ? (p.years[0] === p.years[1] ? p.years[0] : p.years[0] + " to " + p.years[1]) : "";
  }

  function show(p) {
    clearTimeout(hideTimer);
    if (pinned && pinned !== p) return;
    if (shown !== p) {
      shown = p;
      pop.innerHTML = '<div class="mp-head"><strong>' + p.name + '</strong><span>' + years(p) + '</span></div><div class="mp-thumbs">' +
        p.photos.slice(0, 8).map(function (ph, i) {
          return '<button type="button" data-i="' + i + '" aria-label="' + p.name + ', ' + ph.place + '"><img src="' + root + ph.src.replace(".webp", "-t.webp") + '" alt=""></button>';
        }).join("") + "</div>";
      pop.querySelectorAll("button").forEach(function (b) {
        b.addEventListener("click", function () { open(p, +b.dataset.i); });
      });
      place(p);
      if (dotNodes) dotNodes.classed("on", function (d) { return d === p; });
    }
    pop.hidden = false;
  }

  // Put the popup beside the dot, flipped to stay inside the map.
  function place(p) {
    const box = mount.getBoundingClientRect(), wbox = wrap.getBoundingClientRect();
    const k = box.width / W;
    const x = (box.left - wbox.left) + p._xy[0] * k, y = (box.top - wbox.top) + p._xy[1] * k;
    pop.style.left = "0px"; pop.style.top = "0px"; pop.hidden = false;
    const pw = pop.offsetWidth, ph = pop.offsetHeight;
    let left = x + 14, top = y - ph / 2;
    if (left + pw > wbox.width) left = x - pw - 14;
    left = Math.max(4, Math.min(wbox.width - pw - 4, left));
    top = Math.max(4, Math.min(wbox.height - ph - 4, top));
    pop.style.left = left + "px"; pop.style.top = top + "px";
  }

  function softHide() {
    if (pinned) return;
    hideTimer = setTimeout(function () { pop.hidden = true; shown = null; if (dotNodes) dotNodes.classed("on", false); }, 250);
  }
  pop.addEventListener("mouseenter", function () { clearTimeout(hideTimer); });
  pop.addEventListener("mouseleave", softHide);

  function pin(p) {
    pinned = null;
    show(p);
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
      pinned = null; pop.hidden = true; shown = null;
    });
  });
})();
