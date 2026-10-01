// Travel globe. An orthographic globe drawn with d3 in SVG: visited countries
// are filled, and each has a dot on the city where most of its photos were
// taken. Hovering (or tapping) a dot or a visited country opens a card with
// that country's photos. The globe turns slowly until someone touches it.
(function () {
  const mount = document.getElementById("globe");
  const dataEl = document.getElementById("travel-data");
  if (!mount || !dataEl || !window.d3 || !window.topojson) return;
  const root = document.documentElement.getAttribute("data-root") || "";
  const places = JSON.parse(dataEl.textContent).countries;
  const byId = new Map(places.map(function (p) { return [String(+p.id), p]; }));
  const card = document.getElementById("globe-card");
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const css = getComputedStyle(document.documentElement);
  const color = function (v, fb) { return (css.getPropertyValue(v) || fb).trim(); };

  const size = 640;
  const svg = d3.select(mount).append("svg")
    .attr("viewBox", "0 0 " + size + " " + size)
    .attr("role", "img")
    .attr("aria-label", "A globe marking the " + places.length + " countries I have visited");
  const projection = d3.geoOrthographic().scale(size / 2 - 8).translate([size / 2, size / 2]).clipAngle(90).rotate([-20, -25]);
  const path = d3.geoPath(projection);
  const graticule = d3.geoGraticule10();

  svg.append("circle").attr("class", "g-ocean").attr("cx", size / 2).attr("cy", size / 2).attr("r", size / 2 - 8);
  const grat = svg.append("path").attr("class", "g-grat");
  const land = svg.append("g");
  const dots = svg.append("g");
  let landPaths, dotNodes;

  fetch(root + "assets/vendor/countries-110m.json").then(function (r) { return r.json(); }).then(function (world) {
    const countries = topojson.feature(world, world.objects.countries).features;
    landPaths = land.selectAll("path").data(countries).join("path")
      .attr("class", function (d) { return byId.has(String(+d.id)) ? "g-land visited" : "g-land"; })
      .on("mouseenter", function (e, d) { const p = byId.get(String(+d.id)); if (p) open(p, e); })
      .on("click", function (e, d) { const p = byId.get(String(+d.id)); if (p) open(p, e, true); });
    dotNodes = dots.selectAll("g").data(places).join("g").attr("class", "g-dot")
      .attr("tabindex", 0).attr("role", "button")
      .attr("aria-label", function (p) { return p.name + ": photos"; })
      .on("mouseenter", function (e, p) { open(p, e); })
      .on("focus", function (e, p) { open(p, e, true); })
      .on("click", function (e, p) { open(p, e, true); })
      .on("keydown", function (e, p) { if (e.key === "Enter" || e.key === " ") { open(p, e, true); e.preventDefault(); } });
    dotNodes.append("circle").attr("class", "pulse").attr("r", 9);
    dotNodes.append("circle").attr("class", "core").attr("r", function (p) { return 4 + Math.min(4, Math.log10(p.count)); });
    draw();
    spin();
  });

  function draw() {
    grat.attr("d", path(graticule));
    if (landPaths) landPaths.attr("d", path);
    if (dotNodes) {
      const center = projection.invert([size / 2, size / 2]);
      dotNodes.each(function (p) {
        const visible = d3.geoDistance([p.lon, p.lat], center) < Math.PI / 2 - 0.05;
        const xy = projection([p.lon, p.lat]);
        this.setAttribute("transform", "translate(" + xy[0] + "," + xy[1] + ")");
        this.style.display = visible ? "" : "none";
      });
    }
  }

  // Slow turn until the visitor drags, hovers, or picks a country.
  let spinning = !still, last = null;
  function spin(t) {
    if (!spinning) { last = null; return; }
    if (last != null) {
      const r = projection.rotate();
      projection.rotate([r[0] + (t - last) * 0.006, r[1], r[2]]);
      draw();
    }
    last = t;
    requestAnimationFrame(spin);
  }
  function stopSpin() { spinning = false; }

  svg.call(d3.drag().on("start", stopSpin).on("drag", function (e) {
    const r = projection.rotate(), k = 75 / projection.scale();
    projection.rotate([r[0] + e.dx * k, Math.max(-70, Math.min(70, r[1] - e.dy * k)), r[2]]);
    draw();
  }));

  function turnTo(p) {
    const from = projection.rotate(), to = [-p.lon, -p.lat * 0.8, 0];
    const interp = d3.interpolate(from, to);
    d3.transition().duration(still ? 0 : 900).tween("rotate", function () {
      return function (t) { projection.rotate(interp(t)); draw(); };
    });
  }

  // The card: one large photo that crossfades through the set, plus thumbnails.
  let current = null, timer = null, slide = 0;
  function open(p, evt, pinned) {
    stopSpin();
    if (current !== p) {
      current = p;
      slide = 0;
      const years = p.years.length ? (p.years[0] === p.years[1] ? p.years[0] : p.years[0] + " to " + p.years[1]) : "";
      card.innerHTML =
        '<div class="gc-head"><strong>' + p.name + '</strong><span>' + [p.city, years].filter(Boolean).join(" · ") + '</span></div>' +
        '<div class="gc-stage">' + p.photos.map(function (ph, i) {
          return '<img src="' + root + ph.src + '" alt="' + p.name + ', ' + ph.place + ', ' + ph.date + '"' + (i === 0 ? ' class="on"' : ' loading="lazy"') + '>';
        }).join("") + '<span class="gc-cap"></span></div>' +
        '<div class="gc-thumbs">' + p.photos.map(function (ph, i) {
          return '<button type="button" aria-label="Photo ' + (i + 1) + ' of ' + p.photos.length + '"><img src="' + root + ph.src.replace(".webp", "-t.webp") + '" alt=""></button>';
        }).join("") + '</div>';
      card.querySelectorAll(".gc-thumbs button").forEach(function (b, i) {
        b.addEventListener("click", function () { show(i); restart(); });
      });
      show(0);
      restart();
      document.querySelectorAll(".country-list button").forEach(function (b) { b.classList.toggle("on", b.dataset.cc === p.cc); });
      if (dotNodes) dotNodes.classed("on", function (d) { return d === p; });
    }
    card.hidden = false;
    card.classList.toggle("pinned", !!pinned);
  }
  function show(i) {
    const imgs = card.querySelectorAll(".gc-stage img");
    slide = (i + imgs.length) % imgs.length;
    imgs.forEach(function (im, k) { im.classList.toggle("on", k === slide); });
    card.querySelectorAll(".gc-thumbs button").forEach(function (b, k) { b.classList.toggle("on", k === slide); });
    const ph = current.photos[slide];
    const m = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    card.querySelector(".gc-cap").textContent = ph.place + " · " + m[+ph.date.slice(5, 7) - 1] + " " + ph.date.slice(0, 4);
  }
  function restart() {
    clearInterval(timer);
    if (!still && current && current.photos.length > 1) timer = setInterval(function () { show(slide + 1); }, 2600);
  }

  // Every country is also a button below the globe, for touch and keyboards.
  document.querySelectorAll(".country-list button").forEach(function (b) {
    b.addEventListener("click", function () {
      const p = places.find(function (x) { return x.cc === b.dataset.cc; });
      turnTo(p);
      open(p, null, true);
      if (window.matchMedia("(max-width: 52rem)").matches) card.scrollIntoView({ behavior: still ? "auto" : "smooth", block: "nearest" });
    });
  });

  open(places[0], null, false);
  if (!still) spinning = true;
})();
