/* The two photo reels on /reels/. Each reel is a slideshow: about 1.2s a
   photo, a slow pan and zoom, a quick crossfade, the place on a taped label.
   Music is one shared track that starts only when a visitor presses play.
   With prefers-reduced-motion the photos simply fade, with no pan or zoom.
   Without this script the page shows each reel's poster frame. */
(function () {
  "use strict";
  var el = document.getElementById("reels-data");
  if (!el) return;
  var data = JSON.parse(el.textContent);
  var STEP = 1200, AHEAD = 4;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var audio = null, muted = false, players = [];

  function music() {
    if (!audio && data.music) {
      audio = new Audio(data.music);
      audio.loop = true;
      audio.preload = "none";
      audio.volume = 0.7;
    }
    return audio;
  }
  function syncMusic() {
    var a = music();
    if (!a) return;
    var any = players.some(function (p) { return p.playing; });
    a.muted = muted;
    if (any && a.paused) { var pr = a.play(); if (pr && pr.catch) pr.catch(function () {}); }
    if (!any && !a.paused) a.pause();
  }
  function setMuted(m) {
    muted = m;
    players.forEach(function (p) {
      p.mute.setAttribute("aria-pressed", m ? "true" : "false");
      p.mute.setAttribute("aria-label", m ? "Turn music on" : "Mute music");
      p.mute.textContent = m ? "muted" : "sound on";
    });
    if (audio) audio.muted = m;
  }

  // A gentle, repeatable pan for photo i: zoom in a little toward one corner.
  function pan(i) {
    var dx = [-3, 3, -2, 2, 0][i % 5], dy = [-2, 2, 3, -3, -2][(i * 3) % 5];
    return { from: "scale(1.02) translate(0,0)", to: "scale(1.1) translate(" + dx + "%," + dy + "%)" };
  }

  function Player(fig, reel) {
    var self = this;
    this.items = reel.items;
    this.fig = fig;
    this.stage = fig.querySelector(".reel-stage");
    this.imgs = fig.querySelectorAll(".reel-img");
    this.label = fig.querySelector(".reel-place");
    this.big = fig.querySelector(".reel-play");
    this.toggleBtn = fig.querySelector(".reel-toggle");
    this.mute = fig.querySelector(".reel-mute");
    this.fill = fig.querySelector(".reel-fill");
    this.counter = fig.querySelector(".reel-counter");
    this.i = -1; this.front = 0; this.playing = false; this.timer = 0; this.cache = {};
    this.toggleBtn.disabled = false;
    this.big.addEventListener("click", function () { self.play(); });
    this.toggleBtn.addEventListener("click", function () { self.playing ? self.pause() : self.play(); });
    this.mute.addEventListener("click", function () { setMuted(!muted); });
    this.stage.addEventListener("keydown", function (e) {
      if (e.target !== self.stage) return;
      if (e.key === " " || e.key === "Enter" || e.key === "k") { e.preventDefault(); self.playing ? self.pause() : self.play(); }
      else if (e.key === "ArrowRight") { e.preventDefault(); self.pause(); self.show(Math.min(self.i + 1, self.items.length - 1)); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); self.pause(); self.show(Math.max(self.i - 1, 0)); }
      else if (e.key === "m") { setMuted(!muted); }
    });
  }
  Player.prototype.src = function (i) { return "../" + this.items[i].src; };
  Player.prototype.preload = function (from) {
    for (var j = from; j < Math.min(from + AHEAD, this.items.length); j++) {
      if (!this.cache[j]) { var im = new Image(); im.decoding = "async"; im.src = this.src(j); this.cache[j] = im; }
    }
  };
  Player.prototype.show = function (i) {
    var it = this.items[i], next = this.imgs[1 - this.front], cur = this.imgs[this.front];
    this.i = i;
    this.preload(i + 1);
    next.src = this.src(i);
    next.width = it.w; next.height = it.h;
    next.alt = "Photo " + (i + 1) + " of " + this.items.length + (it.place ? ", " + it.place : "");
    if (!still) {
      var k = pan(i);
      next.style.transition = "none";
      next.style.transform = k.from;
      void next.offsetWidth;
      next.style.transition = "";
      next.style.transform = k.to;
    }
    next.classList.add("on");
    cur.classList.remove("on");
    cur.alt = "";
    this.front = 1 - this.front;
    if (it.place) { this.label.textContent = it.place; this.label.hidden = false; }
    else this.label.hidden = true;
    this.fill.style.width = ((i + 1) / this.items.length * 100) + "%";
    this.counter.textContent = (i + 1) + " / " + this.items.length;
  };
  Player.prototype.tick = function () {
    var self = this;
    if (!this.playing) return;
    if (this.i + 1 >= this.items.length) { this.finish(); return; }
    var n = this.i + 1, im = this.cache[n];
    var go = function () { if (self.playing) { self.show(n); self.timer = setTimeout(function () { self.tick(); }, STEP); } };
    // Wait for the next photo on a slow connection rather than fading to a blank.
    if (im && !im.complete) { im.onload = im.onerror = go; } else go();
  };
  Player.prototype.play = function () {
    var self = this, refocus = document.activeElement === this.big;
    if (this.i + 1 >= this.items.length) this.i = -1;
    this.playing = true;
    this.fig.classList.add("playing");
    this.big.hidden = true;
    this.toggleBtn.textContent = "pause";
    this.toggleBtn.setAttribute("aria-label", "Pause");
    this.preload(this.i + 1);
    syncMusic();
    this.tick();
    if (refocus) this.stage.focus();
  };
  Player.prototype.pause = function () {
    this.playing = false;
    clearTimeout(this.timer);
    this.fig.classList.remove("playing");
    this.toggleBtn.textContent = "resume";
    this.toggleBtn.setAttribute("aria-label", "Resume");
    syncMusic();
  };
  Player.prototype.finish = function () {
    this.pause();
    this.toggleBtn.textContent = "play again";
    this.toggleBtn.setAttribute("aria-label", "Play again");
  };

  data.reels.forEach(function (r) {
    var fig = document.querySelector('.reel[data-reel="' + r.id + '"]');
    if (fig) players.push(new Player(fig, r));
  });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden) players.forEach(function (p) { if (p.playing) p.pause(); });
  });
})();
