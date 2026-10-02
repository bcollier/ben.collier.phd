/* Reels, version 2: a music video cut to the beat, drawn live in the browser.
   data/reels_v2.json (from scripts/make_reels_v2.py) is the edit: every shot
   with its start time, length, photos and effects. This file only renders it.

   Two layers: a WebGL canvas for the photos (crop toward the face, push and
   punch zooms, colour split, glitch, duotone grades, kaleidoscope, grids and
   panels) and a 2D canvas on top for type, the seal, stage lights, sparkles
   and the closing mosaic. Every frame is a pure function of the song time,
   so seeking works and ?capture can render it frame by frame.

   With prefers-reduced-motion the same edit plays with no flashes, colour
   split, glitch, shake, zoom punches or kaleidoscope spin. */
(function () {
  "use strict";
  var dataEl = document.getElementById("reels-v2-data");
  var root = document.querySelector(".v2");
  if (!dataEl || !root) return;
  var D = JSON.parse(dataEl.textContent);
  var BASE = "../";
  var BEAT = 60 / D.bpm;
  var CAPTURE = /[?&]capture\b/.test(location.search);
  var CALM = !CAPTURE && window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DISPLAY = '"Black Han Sans", "Arial Black", Impact, sans-serif';
  var MONO = '"IBM Plex Mono", ui-monospace, monospace';
  var shots = D.shots, imgs = D.img;
  var BEN = imgs.map(function (_, i) { return i; }).filter(function (i) { return imgs[i].r !== "b"; });

  var stage = root.querySelector(".v2-stage");
  var glc = stage.querySelector(".v2-gl");
  var ov = stage.querySelector(".v2-fx");
  var poster = stage.querySelector(".v2-poster");
  var bigPlay = stage.querySelector(".v2-play");
  var toggle = root.querySelector(".v2-toggle");
  var muteBtn = root.querySelector(".v2-mute");
  var seek = root.querySelector(".v2-seek");
  var clock = root.querySelector(".v2-time");
  var fullBtn = root.querySelector(".v2-full");
  if (CAPTURE) document.documentElement.classList.add("v2-capture");

  // ---------------------------------------------------------------- utils
  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function lerp(a, b, k) { return a + (b - a) * k; }
  function ease(k) { k = clamp(k, 0, 1); return k * k * (3 - 2 * k); }
  function outBack(k) { k = clamp(k, 0, 1); var c = 1.7; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); }
  function hash(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
  function has(s, tok) { return !!(s.fx && (" " + s.fx + " ").indexOf(" " + tok + " ") >= 0); }
  function rgb(hex) { var n = parseInt(hex.slice(1), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; }
  function css(c, a) { return "rgba(" + Math.round(c[0] * 255) + "," + Math.round(c[1] * 255) + "," + Math.round(c[2] * 255) + "," + a + ")"; }
  function fmt(t) { t = Math.max(0, Math.floor(t)); return Math.floor(t / 60) + ":" + ("0" + t % 60).slice(-2); }
  function shotAt(t) {
    var lo = 0, hi = shots.length - 1;
    if (t < shots[0].t) return 0;
    while (lo < hi) { var m = (lo + hi + 1) >> 1; if (shots[m].t <= t) lo = m; else hi = m - 1; }
    return lo;
  }
  function beatInfo(t) {
    var b = (t - D.t0) / BEAT;
    if (b < 0) return { n: -1, since: 9, pulse: 0, bar: 0 };
    var n = Math.floor(b), since = (b - n) * BEAT;
    return { n: n, since: since, pulse: Math.exp(-since * 9), bar: ((n - 2) % 4 + 4) % 4 };
  }
  function energy(t) {
    var d = D.drops, calm = D.calm;
    for (var i = 0; i < calm.length; i++) if (t >= calm[i][0] && t < calm[i][1]) return 0.25;
    if ((t >= d[0] && t < calm[1][0]) || (t >= d[1] && t < D.dur - 30)) return 1;
    return 0.55;
  }

  // ---------------------------------------------------------------- WebGL
  var gl = glc.getContext("webgl", { premultipliedAlpha: false, antialias: false, preserveDrawingBuffer: CAPTURE });
  if (!gl) { root.classList.add("v2-nogl"); return; }
  var VS = "attribute vec2 P;varying vec2 U;void main(){U=vec2(P.x*.5+.5,.5-P.y*.5);gl_Position=vec4(P,0.,1.);}";
  var FS = [
    "precision highp float;",
    "uniform sampler2D T0,T1,T2,T3;uniform vec4 X0,X1,X2,X3,IA;uniform vec2 R;",
    "uniform float SA,MODE,TIME,ALPHA,RGB,GLITCH,WAVE,DUO,FLASH,ZB,SOFT,REVEAL,NEON,DARK,SEED,FZ,PAN,SPIN;",
    "uniform vec3 C1,C2,FC;varying vec2 U;",
    "float h1(float n){return fract(sin(n*127.1)*43758.5453);}",
    "float h2(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}",
    "vec2 mir(vec2 p){return 1.-abs(1.-mod(p,2.));}",
    "vec3 tx(int i,vec2 p){p=clamp(p,.001,.999);if(i==0)return texture2D(T0,p).rgb;if(i==1)return texture2D(T1,p).rgb;if(i==2)return texture2D(T2,p).rgb;return texture2D(T3,p).rgb;}",
    "vec4 xf(int i){if(i==0)return X0;if(i==1)return X1;if(i==2)return X2;return X3;}",
    "vec2 cv(int i,vec2 u){vec4 x=xf(i);return x.zw+(u-.5)*x.xy;}",
    "vec3 sp(int i,vec2 u,float a){vec2 d=(u-.5)*a;return vec3(tx(i,cv(i,u+d)).r,tx(i,cv(i,u)).g,tx(i,cv(i,u-d)).b);}",
    "vec3 zb(int i,vec2 u){vec3 c=vec3(0.);for(int k=0;k<8;k++){float s=1.-ZB*float(k)*.035;c+=sp(i,.5+(u-.5)*s,RGB);}return c/8.;}",
    "void main(){",
    " vec2 u=U;",
    " u.x+=sin(u.y*18.+TIME*6.)*WAVE;",
    " if(GLITCH>0.){float b=floor(u.y*26.);float f=floor(TIME*15.);if(h1(b+f*7.3+SEED)<GLITCH*.45){u.x+=(h1(b*3.1+f)-.5)*.22*GLITCH;}}",
    " vec3 c;",
    " if(MODE<.5){c=ZB>0.?zb(0,u):sp(0,u,RGB);}",
    " else if(MODE<1.5){",
    "  float ia=IA.x;vec2 sz=ia>SA?vec2(1.,SA/ia):vec2(ia/SA,1.);sz*=FZ;vec2 q=(u-(.5-sz*.5))/sz;",
    "  vec3 bg=vec3(0.);for(int k=0;k<9;k++){vec2 o=vec2(mod(float(k),3.)-1.,floor(float(k)/3.)-1.)*.035;bg+=tx(0,cv(0,u*.8+.1+o));}bg/=9.;",
    "  float bl=dot(bg,vec3(.3,.59,.11));bg=mix(bg,mix(C1,C2,bl),.65)*.5;",
    "  if(q.x>=0.&&q.x<=1.&&q.y>=0.&&q.y<=1.){vec2 d=(q-.5)*RGB;c=vec3(tx(0,q+d).r,tx(0,q).g,tx(0,q-d).b);}else c=bg;",
    "  vec2 e=abs(u-.5)-sz*.5;float dist=length(max(e,0.))+min(max(e.x,e.y),0.);",
    "  c+=mix(C1,C2,u.y)*exp(-abs(dist)*R.y*.25)*NEON;",
    " }",
    " else if(MODE<2.5){",
    "  vec2 g=floor(u*2.);int q=int(g.x+g.y*2.);vec2 l=fract(u*2.);",
    "  if(g.x+g.y*2.<REVEAL){c=sp(q,l,RGB);}else{c=mix(C1,C2,l.y)*.12;}",
    "  vec2 gd=abs(u-.5);float ln=exp(-min(gd.x,gd.y)*R.y*.6);c=mix(c,mix(C1,C2,u.x),ln*.9);",
    " }",
    " else if(MODE<3.5){",
    "  float s=floor(u.x*3.);vec2 l=vec2(fract(u.x*3.),u.y+(s-1.)*PAN);",
    "  vec2 d=(l-.5)*RGB;vec2 p0=X1.zw+(l-.5)*X1.xy;vec2 pd=d*X1.xy;",
    "  vec3 t=vec3(tx(0,p0+pd).r,tx(0,p0).g,tx(0,p0-pd).b);",
    "  float L=dot(t,vec3(.3,.59,.11));",
    "  c=s<.5?mix(t,C1*L*1.8,.55):(s<1.5?t:mix(t,C2*L*1.8,.55));",
    "  float ed=min(fract(u.x*3.),1.-fract(u.x*3.));c=mix(c,vec3(1.),exp(-ed*R.x*.6)*.8);",
    " }",
    " else if(MODE<4.5){",
    "  vec2 p=(u-.5)*vec2(SA,1.);float r=length(p);float a=atan(p.y,p.x)+SPIN;",
    "  float sg=6.2831853/6.;a=mod(a,sg);a=abs(a-sg*.5);",
    "  vec2 k=vec2(cos(a),sin(a))*r*(1.25+.2*sin(TIME*.7));",
    "  vec3 t=tx(0,mir(X0.zw+k*.8+vec2(sin(SPIN*.3),cos(SPIN*.23))*.08));",
    "  c=mix(t,t.brg,.5+.5*sin(TIME*1.7));c*=1.+.25*exp(-r*3.);",
    " }",
    " else{float r=length((u-.5)*vec2(SA,1.));c=mix(vec3(.09,.02,.14),vec3(.01,0.,.03),clamp(r*1.3,0.,1.))+C1*.06*(1.-r);}",
    " float L=dot(c,vec3(.299,.587,.114));",
    " c=mix(c,mix(C1*.85,C2*1.1+.08,smoothstep(.04,.96,L)),DUO);",
    " c=mix(vec3(L),c,1.18);c=(c-.5)*1.08+.5;",
    " c=mix(c,sqrt(max(c,0.))*.92+.04,SOFT*.6);",
    " c*=1.-DARK;",
    " c=mix(c,FC,FLASH);",
    " vec2 vv=u-.5;c*=1.-dot(vv,vv)*.85;",
    " c*=.96+.04*sin(gl_FragCoord.y*3.14159);",
    " c+=(h2(gl_FragCoord.xy+TIME*61.)-.5)*.045;",
    " gl_FragColor=vec4(clamp(c,0.,1.),ALPHA);",
    "}"].join("\n");
  function compile(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  var prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  gl.useProgram(prog);
  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var aP = gl.getAttribLocation(prog, "P");
  gl.enableVertexAttribArray(aP);
  gl.vertexAttribPointer(aP, 2, gl.FLOAT, false, 0, 0);
  var U = {};
  "T0 T1 T2 T3 X0 X1 X2 X3 IA R SA MODE TIME ALPHA RGB GLITCH WAVE DUO FLASH ZB SOFT REVEAL NEON DARK SEED FZ PAN SPIN C1 C2 FC"
    .split(" ").forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
  for (var u = 0; u < 4; u++) gl.uniform1i(U["T" + u], u);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  var blank = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, blank);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([0, 0, 0, 255]));

  // ---------------------------------------------------------------- loading
  var tex = {}, loading = {}, thumbs = {};
  function loadTex(id) {
    if (tex[id] || loading[id]) return loading[id] || Promise.resolve();
    loading[id] = new Promise(function (res) {
      var im = new Image();
      im.decoding = "async";
      im.onload = function () {
        var go = function () {
          var t = gl.createTexture();
          gl.bindTexture(gl.TEXTURE_2D, t);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
          gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, im);
          tex[id] = t; delete loading[id]; res();
        };
        if (im.decode) im.decode().then(go, go); else go();
      };
      im.onerror = function () { delete loading[id]; res(); };
      im.src = BASE + imgs[id].src;
    });
    return loading[id];
  }
  function loadThumb(id) {
    if (thumbs[id]) return thumbs[id].p;
    var im = new Image();
    var p = new Promise(function (res) { im.onload = im.onerror = function () { res(); }; });
    im.src = BASE + imgs[id].t;
    thumbs[id] = { im: im, p: p };
    return p;
  }
  function needs(t0, t1) {
    var out = [], i = shotAt(t0);
    for (; i < shots.length && shots[i].t <= t1; i++) {
      var s = shots[i];
      if (s.k === "mosaic" || s.k === "end") { BEN.forEach(function (id) { out.push(["t", id]); }); continue; }
      (s.i || []).forEach(function (id) { out.push(["g", id]); });
    }
    return out;
  }
  function ensure(t0, t1) {
    return Promise.all(needs(t0, t1).map(function (n) { return n[0] === "g" ? loadTex(n[1]) : loadThumb(n[1]); }));
  }
  function evict(t) {
    var keep = {};
    needs(Math.max(0, t - 2), t + 10).forEach(function (n) { if (n[0] === "g") keep[n[1]] = 1; });
    Object.keys(tex).forEach(function (id) { if (!keep[id]) { gl.deleteTexture(tex[id]); delete tex[id]; } });
  }
  function ready(s) { return (s.i && s.k !== "mosaic" && s.k !== "end") ? s.i.every(function (id) { return tex[id]; }) : true; }

  // ---------------------------------------------------------------- sizing
  var W = 0, H = 0, SA = 16 / 9, ctx = ov.getContext("2d");
  function resize() {
    var r = stage.getBoundingClientRect();
    var dpr = CAPTURE ? 1 : Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.round(r.width * dpr), h = Math.round(r.height * dpr);
    var cap = 1920 / Math.max(w, h);
    if (cap < 1) { w = Math.round(w * cap); h = Math.round(h * cap); }
    if (w === W && h === H) return;
    W = glc.width = ov.width = w; H = glc.height = ov.height = h; SA = w / h;
    gl.viewport(0, 0, w, h);
  }

  // Where to sample an image so it covers a box of aspect `box`, zoomed by z,
  // centred toward (fx, fy) without running off the edge.
  function cover(id, box, z, fx, fy) {
    var m = imgs[id], ia = m.w / m.h, sx, sy;
    if (ia > box) { sx = box / ia; sy = 1; } else { sx = 1; sy = ia / box; }
    sx /= z; sy /= z;
    return [sx, sy, clamp(fx, sx / 2, 1 - sx / 2), clamp(fy, sy / 2, 1 - sy / 2)];
  }

  // ---------------------------------------------------------------- one shot
  function uniforms(s, t, alpha) {
    var lt = t - s.t, p = clamp(lt / s.d, 0, 1), bi = beatInfo(t);
    var g = s.g || ["#ff2d95", "#22e6ff"], c1 = rgb(g[0]), c2 = rgb(g[1]);
    var start = Math.exp(-lt * 9);
    var o = { MODE: 0, RGB: 0, GLITCH: 0, WAVE: 0, DUO: 0.14, FLASH: 0, ZB: 0, SOFT: 0, REVEAL: 4, NEON: 0, DARK: 0, FZ: 0.86, PAN: 0, SPIN: 0, FC: [1, 1, 1] };
    var z = 1, punch = 0, id = s.i ? s.i[0] : -1, f = id >= 0 ? imgs[id].f : [0.5, 0.45, 0];
    var fx = f[0], fy = f[1];
    if (has(s, "push")) { z = 1 + 0.16 * ease(p); fx = lerp(0.5, fx, ease(p)); fy = lerp(0.48, fy, ease(p)); }
    if (has(s, "punch")) punch = start;
    if (has(s, "beat")) punch = Math.max(punch, bi.pulse);
    z *= 1 + 0.12 * punch;
    if (has(s, "rgb")) o.RGB = 0.004 + 0.022 * Math.max(punch, bi.pulse * 0.6);
    if (has(s, "neon")) { o.DUO = 0.42; o.RGB = Math.max(o.RGB, 0.003); }
    if (has(s, "duo")) o.DUO = Math.max(o.DUO, 0.34);
    if (has(s, "glitch")) { o.GLITCH = 0.3 + 0.7 * bi.pulse; o.WAVE = 0.004 * bi.pulse; o.RGB = Math.max(o.RGB, 0.01 + 0.02 * bi.pulse); }
    if (has(s, "soft")) { o.SOFT = 0.8; o.DUO = 0.28; }
    if (has(s, "riser")) { o.ZB = 0.4 + 0.6 * p; o.RGB = Math.max(o.RGB, 0.01 + 0.03 * p); }
    if (has(s, "whiteout")) { o.ZB = 1; o.FLASH = Math.pow(p, 2.2); }
    if (has(s, "drop")) { o.FLASH = Math.max(o.FLASH, 0.85 * Math.exp(-lt * 7)); o.FC = c1.map(function (v) { return 0.6 + 0.4 * v; }); }
    if (has(s, "fadein")) alpha *= ease(lt / 0.6);
    // shake on drops and big punches
    var sh = has(s, "drop") ? 0.03 * Math.exp(-lt * 5) : 0.004 * punch;
    var shx = (hash(Math.floor(t * 30)) - 0.5) * sh, shy = (hash(Math.floor(t * 30) + 9) - 0.5) * sh;
    if (CALM) { o.RGB = 0; o.GLITCH = 0; o.WAVE = 0; o.ZB = 0; o.FLASH *= 0.25; z = has(s, "push") ? 1 + 0.06 * ease(p) : 1; shx = shy = 0; }
    var X = [[1, 1, 0.5, 0.5], [1, 1, 0.5, 0.5], [1, 1, 0.5, 0.5], [1, 1, 0.5, 0.5]], IA = [1, 1, 1, 1];
    var ids = s.i || [];
    if ((s.k === "photo" || s.k === "title") && id >= 0) {
      o.MODE = (has(s, "frame") || s.k === "title") ? 1 : 0;
      if (o.MODE === 1) { o.FZ = 0.84 * z; o.NEON = 0.9; X[0] = cover(id, SA, 1.05, 0.5, 0.5); }
      else X[0] = cover(id, SA, z, fx + shx, fy + shy);
      if (s.k === "title") { o.DARK = 0.45; o.DUO = 0.5; }
      IA[0] = imgs[id].w / imgs[id].h;
    } else if (s.k === "grid") {
      o.MODE = 2;
      o.REVEAL = CALM ? 4 : Math.min(4, Math.floor(lt / BEAT + 0.001) + 1);
      for (var q = 0; q < 4; q++) {
        var m = imgs[ids[q]], pop = (q === o.REVEAL - 1 && !CALM) ? 1 + 0.15 * Math.exp(-(lt - q * BEAT) * 10) : 1;
        X[q] = cover(ids[q], SA, pop * (1 + 0.05 * p), m.f[0], m.f[1]);
      }
      o.RGB = CALM ? 0 : 0.008 * bi.pulse;
    } else if (s.k === "panels") {
      o.MODE = 3;
      X[1] = cover(id, SA / 3, 1.05 + 0.1 * p, fx, fy);
      o.PAN = CALM ? 0 : 0.06 * Math.sin(p * Math.PI) * (1 - p);
      o.RGB = CALM ? 0 : 0.01 * bi.pulse;
      o.DUO = 0.1;
    } else if (s.k === "kaleido") {
      o.MODE = CALM ? 0 : 4;
      o.SPIN = CALM ? 0 : t * 0.5 + bi.pulse * 0.08;
      X[0] = CALM ? cover(id, SA, 1, 0.5, 0.5) : [1, 1, f[0], f[1]];
      o.DUO = 0.2;
    } else {
      o.MODE = 5; o.DUO = 0;
    }
    for (var k = 0; k < 4; k++) {
      gl.activeTexture(gl.TEXTURE0 + k);
      gl.bindTexture(gl.TEXTURE_2D, (ids[k] != null && tex[ids[k]]) || (k > 0 && ids[0] != null && tex[ids[0]]) || blank);
      gl.uniform4fv(U["X" + k], X[k]);
    }
    gl.uniform4fv(U.IA, IA);
    gl.uniform2f(U.R, W, H);
    gl.uniform1f(U.SA, SA);
    gl.uniform1f(U.TIME, t);
    gl.uniform1f(U.ALPHA, alpha);
    gl.uniform1f(U.SEED, shots.indexOf(s) * 1.7);
    ["MODE", "RGB", "GLITCH", "WAVE", "DUO", "FLASH", "ZB", "SOFT", "REVEAL", "NEON", "DARK", "FZ", "PAN", "SPIN"]
      .forEach(function (n) { gl.uniform1f(U[n], o[n]); });
    gl.uniform3fv(U.C1, c1); gl.uniform3fv(U.C2, c2); gl.uniform3fv(U.FC, o.FC);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }

  // ---------------------------------------------------------------- overlay
  function text(str, x, y, size, opt) {
    opt = opt || {};
    ctx.save();
    ctx.translate(x, y);
    if (opt.rot) ctx.rotate(opt.rot);
    if (opt.scale) ctx.scale(opt.scale, opt.scale);
    ctx.font = size + "px " + DISPLAY;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    var w = ctx.measureText(str).width, max = W * 0.88;
    if (w > max) { var k = max / w; ctx.scale(k, k); }
    var split = CALM ? 0 : (opt.split || 0);
    if (split) {
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = "rgba(34,230,255,.75)"; ctx.fillText(str, -split, 0);
      ctx.fillStyle = "rgba(255,45,149,.75)"; ctx.fillText(str, split, 0);
      ctx.globalCompositeOperation = "source-over";
    }
    var gr = ctx.createLinearGradient(0, -size / 2, 0, size / 2);
    gr.addColorStop(0, opt.c1 || "#fff4fb"); gr.addColorStop(0.55, opt.c2 || "#ff7ac8"); gr.addColorStop(1, opt.c3 || "#ffd23f");
    ctx.shadowColor = opt.glow || "rgba(255,45,149,.9)";
    ctx.shadowBlur = size * 0.35;
    ctx.lineWidth = Math.max(2, size * 0.05);
    ctx.strokeStyle = "rgba(20,0,30,.85)";
    ctx.strokeText(str, 0, 0);
    ctx.fillStyle = gr;
    ctx.fillText(str, 0, 0);
    ctx.restore();
  }

  var GLYPHS = "BENCOLIR#*+=벤콜리어";
  function glitchText(str, lt, seed) {
    if (CALM) return str;
    var out = "";
    for (var i = 0; i < str.length; i++) {
      var at = 0.15 + hash(i * 7.1 + seed) * 1.1;
      if (str[i] === " " || lt > at) out += str[i];
      else if (lt > at - 0.45) out += GLYPHS[Math.floor(hash(i + Math.floor(lt * 20)) * GLYPHS.length)];
      else out += " ";
    }
    return out;
  }

  // The seal: rings, ticks, a six-point star and Ben's name in hangul,
  // drawn as if by a brush of light.
  function seal(cx, cy, R, k, alpha, rot) {
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(rot);
    ctx.globalAlpha = alpha;
    ctx.globalCompositeOperation = "lighter";
    ctx.lineCap = "round";
    ctx.shadowBlur = R * 0.08;
    var gold = "rgba(255,210,63,.95)", pink = "rgba(255,70,170,.95)";
    function arc(r, a, b, col, w) {
      if (b <= a) return;
      ctx.strokeStyle = col; ctx.shadowColor = col; ctx.lineWidth = w;
      ctx.beginPath(); ctx.arc(0, 0, r, a, b); ctx.stroke();
    }
    function seg(k0, k1) { return clamp((k - k0) / (k1 - k0), 0, 1); }
    var a = seg(0, 0.3), b = seg(0.1, 0.4);
    arc(R, -Math.PI / 2, -Math.PI / 2 + a * Math.PI * 2, gold, R * 0.018);
    arc(R * 0.86, Math.PI / 2, Math.PI / 2 + b * Math.PI * 2, pink, R * 0.01);
    arc(R * 0.5, 0, seg(0.45, 0.7) * Math.PI * 2, gold, R * 0.008);
    var tk = seg(0.2, 0.5);
    ctx.strokeStyle = gold; ctx.shadowColor = gold; ctx.lineWidth = R * 0.008;
    for (var i = 0; i < 24; i++) {
      if (i / 24 > tk) break;
      var an = i / 24 * Math.PI * 2, r1 = R * (i % 2 ? 0.9 : 0.88), r2 = R * 0.97;
      ctx.beginPath(); ctx.moveTo(Math.cos(an) * r1, Math.sin(an) * r1); ctx.lineTo(Math.cos(an) * r2, Math.sin(an) * r2); ctx.stroke();
    }
    var st = seg(0.35, 0.75);
    [0, Math.PI].forEach(function (off, j) {
      ctx.strokeStyle = j ? pink : gold; ctx.shadowColor = ctx.strokeStyle; ctx.lineWidth = R * 0.012;
      ctx.beginPath();
      for (var e = 0; e <= 3; e++) {
        var kk = clamp(st * 3 - e + 1, 0, 1);
        var a0 = off - Math.PI / 2 + (e - 1) * Math.PI * 2 / 3, a1 = a0 + Math.PI * 2 / 3;
        var x0 = Math.cos(a0) * R * 0.8, y0 = Math.sin(a0) * R * 0.8, x1 = Math.cos(a1) * R * 0.8, y1 = Math.sin(a1) * R * 0.8;
        if (e === 0) continue;
        ctx.moveTo(x0, y0); ctx.lineTo(lerp(x0, x1, kk), lerp(y0, y1, kk));
      }
      ctx.stroke();
    });
    var ring = "벤 · 콜리어 · BEN COLLIER · ";
    var lk = seg(0.55, 0.95);
    ctx.font = Math.round(R * 0.075) + "px " + DISPLAY;
    ctx.fillStyle = "rgba(255,240,200,.95)"; ctx.shadowColor = gold;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    var n = ring.length * 2;
    for (var c = 0; c < n * lk; c++) {
      var ch = ring[c % ring.length], an2 = c / n * Math.PI * 2 - Math.PI / 2;
      ctx.save(); ctx.rotate(an2 + Math.PI / 2); ctx.fillText(ch, 0, -R * 0.68); ctx.restore();
    }
    ctx.restore();
  }

  function stars(t, e, W, H) {
    if (e <= 0) return;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    var n = Math.round(14 + 34 * e);
    for (var i = 0; i < n; i++) {
      var P = 1.1 + hash(i * 1.3) * 1.2, ph = hash(i * 5.7) * P, cyc = Math.floor((t + ph) / P), k = ((t + ph) % P) / P;
      var x = hash(i * 3.1 + cyc * 1.7) * W, y = hash(i * 9.2 + cyc * 2.3) * H, s = Math.sin(k * Math.PI) * H * (0.008 + 0.018 * hash(i + cyc));
      if (CALM) s *= 0.6;
      ctx.fillStyle = i % 3 ? "rgba(255,235,255,.9)" : "rgba(255,210,63,.9)";
      ctx.beginPath();
      ctx.moveTo(x, y - s * 2); ctx.lineTo(x + s * 0.3, y - s * 0.3); ctx.lineTo(x + s * 2, y); ctx.lineTo(x + s * 0.3, y + s * 0.3);
      ctx.lineTo(x, y + s * 2); ctx.lineTo(x - s * 0.3, y + s * 0.3); ctx.lineTo(x - s * 2, y); ctx.lineTo(x - s * 0.3, y - s * 0.3);
      ctx.fill();
    }
    ctx.restore();
  }

  function beams(t, e, g, pulse) {
    if (e < 0.5) return;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    var cols = [rgb(g[0]), rgb(g[1])];
    for (var i = 0; i < 4; i++) {
      var x = W * (0.12 + i * 0.25), sw = CALM ? 0 : Math.sin(t * (0.9 + i * 0.17) + i * 2) * 0.45;
      ctx.save(); ctx.translate(x, -H * 0.05); ctx.rotate(sw);
      var L = H * 1.4, half = W * 0.07;
      var gr = ctx.createLinearGradient(0, 0, 0, L);
      var a = (0.1 + 0.12 * pulse) * e;
      gr.addColorStop(0, css(cols[i % 2], a * 1.6)); gr.addColorStop(1, css(cols[i % 2], 0));
      ctx.fillStyle = gr;
      ctx.beginPath(); ctx.moveTo(-half * 0.08, 0); ctx.lineTo(half * 0.08, 0); ctx.lineTo(half, L); ctx.lineTo(-half, L); ctx.fill();
      ctx.restore();
    }
    ctx.restore();
  }

  function rings(t) {
    D.drops.forEach(function (td) {
      var k = t - td;
      if (k < 0 || k > 1.4 || CALM) return;
      ctx.save();
      ctx.globalCompositeOperation = "lighter";
      for (var j = 0; j < 3; j++) {
        var kk = k - j * 0.12; if (kk < 0) continue;
        var r = Math.hypot(W, H) * 0.6 * (1 - Math.exp(-kk * 3.2));
        ctx.strokeStyle = j % 2 ? "rgba(34,230,255," + (0.8 * (1 - kk / 1.4)) + ")" : "rgba(255,45,149," + (0.9 * (1 - kk / 1.4)) + ")";
        ctx.lineWidth = H * 0.02 * (1 - kk / 1.4);
        ctx.beginPath(); ctx.arc(W / 2, H / 2, r, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.restore();
    });
  }

  function chip(place, lt, g) {
    var k = ease(lt / 0.22), s = Math.round(H * 0.045);
    ctx.save();
    ctx.font = s + "px " + DISPLAY;
    var label = place.toUpperCase(), w = ctx.measureText(label).width + s * 1.6, h = s * 1.55;
    var x = W * 0.04 - (1 - k) * (w + W * 0.05), y = H * 0.86;
    ctx.translate(x, y); ctx.rotate(-0.035);
    ctx.fillStyle = "rgba(14,4,24,.72)";
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(0, -h / 2, w, h, h / 2); else ctx.rect(0, -h / 2, w, h);
    ctx.fill();
    var gr = ctx.createLinearGradient(0, 0, w, 0); gr.addColorStop(0, g[0]); gr.addColorStop(1, g[1]);
    ctx.strokeStyle = gr; ctx.lineWidth = Math.max(2, s * 0.09); ctx.stroke();
    ctx.fillStyle = g[0]; ctx.beginPath(); ctx.arc(s * 0.62, 0, s * 0.18, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#fff"; ctx.textBaseline = "middle"; ctx.fillText(label, s * 1.0, s * 0.04);
    ctx.restore();
  }

  function hud(t, bi) {
    var s = Math.max(10, Math.round(H * 0.026));
    ctx.save();
    ctx.font = "600 " + s + "px " + MONO;
    ctx.fillStyle = "rgba(255,255,255,.75)";
    ctx.textBaseline = "top";
    ctx.fillText("BEN · REELS VOL.2", W * 0.03, H * 0.04);
    for (var i = 0; i < 4; i++) {
      ctx.fillStyle = (bi.n >= 0 && bi.bar === i) ? "#ff2d95" : "rgba(255,255,255,.3)";
      ctx.beginPath(); ctx.arc(W * 0.97 - (3 - i) * s * 1.3, H * 0.04 + s * 0.5, s * 0.32, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }

  // The closing mosaic: every photo, oldest first, landing on the beat.
  function mosaic(s, t, dim) {
    var n = BEN.length, cols = Math.ceil(Math.sqrt(n * SA)), rows = Math.ceil(n / cols);
    var cell = Math.min(W / cols, H / rows), gx = (W - cell * cols) / 2, gy = (H - cell * rows) / 2;
    var ms = shots.filter(function (x) { return x.k === "mosaic"; })[0];
    var lt = t - ms.t, span = ms.d * 0.72;
    // The camera starts close on the newest tile and pulls back to the whole wall.
    var k0 = ease(lt / ms.d), zoom = CALM ? 1 : lerp(2.6, 1, k0);
    var last = clamp(Math.floor(lt / span * n), 0, n - 1);
    var lx = gx + (last % cols + 0.5) * cell, ly = gy + (Math.floor(last / cols) + 0.5) * cell;
    var cx = lerp(lx, W / 2, k0), cy = lerp(ly, H / 2, k0);
    if (s.k === "end") { zoom = 1; cx = W / 2; cy = H / 2; }
    ctx.save();
    ctx.translate(W / 2, H / 2); ctx.scale(zoom, zoom); ctx.translate(-cx, -cy);
    for (var i = 0; i < n; i++) {
      var at = Math.floor((i / n) * span / (BEAT / 2)) * (BEAT / 2), k = (lt - at) / 0.25;
      if (k <= 0) continue;
      var th = thumbs[BEN[i]]; if (!th || !th.im.complete || !th.im.naturalWidth) continue;
      var im = th.im, m = imgs[BEN[i]], side = Math.min(im.naturalWidth, im.naturalHeight);
      var sx = clamp(m.f[0] * im.naturalWidth - side / 2, 0, im.naturalWidth - side), sy = clamp(m.f[1] * im.naturalHeight - side / 2, 0, im.naturalHeight - side);
      var c = i % cols, r = Math.floor(i / cols), sc = CALM ? 1 : outBack(k);
      var x = gx + c * cell + cell / 2, y = gy + r * cell + cell / 2, w = cell * 0.94 * sc;
      ctx.globalAlpha = dim * clamp(k, 0, 1);
      ctx.drawImage(im, sx, sy, side, side, x - w / 2, y - w / 2, w, w);
      if (k < 1.6 && !CALM) { ctx.strokeStyle = "rgba(255,45,149," + (1 - k / 1.6) + ")"; ctx.lineWidth = cell * 0.06; ctx.strokeRect(x - w / 2, y - w / 2, w, w); }
    }
    ctx.restore();
  }

  function overlay(s, t) {
    var lt = t - s.t, p = clamp(lt / s.d, 0, 1), bi = beatInfo(t), e = energy(t), g = s.g || ["#ff2d95", "#22e6ff"];
    ctx.clearRect(0, 0, W, H);
    if (s.k === "mosaic") mosaic(s, t, 1);
    if (s.k === "end") {
      var fade = clamp((s.t + s.d - t) / 3, 0, 1);
      mosaic(s, t, 0.3 * fade);
      seal(W / 2, H / 2, H * 0.42, clamp(lt / 4, 0, 1), 0.55 * fade, t * 0.05);
      text(s.text, W / 2, H * 0.47, Math.round(H * 0.13), { split: 4 * bi.pulse });
      ctx.globalAlpha = fade;
      ctx.font = Math.round(H * 0.035) + "px " + MONO; ctx.fillStyle = "#ffe9f6"; ctx.textAlign = "center";
      ctx.fillText(s.sub, W / 2, H * 0.6);
      ctx.globalAlpha = 1;
      if (fade < 1) { ctx.fillStyle = "rgba(0,0,0," + (1 - fade) + ")"; ctx.fillRect(0, 0, W, H); }
      return;
    }
    beams(t, e, g, bi.pulse);
    if (s.k === "sigil") {
      seal(W / 2, H / 2, H * 0.36 * (1 + 0.015 * bi.pulse), clamp(lt / (s.d * 0.9), 0, 1), 1, t * 0.06);
      if (lt > s.d * 0.55) text("벤", W / 2, H / 2, Math.round(H * 0.16 * (1 + 0.04 * bi.pulse)), { split: 3 });
    }
    if (s.k === "title") {
      var size = Math.round(H * 0.17);
      if (has(s, "glitchin")) {
        seal(W / 2, H / 2, H * 0.36, 1, 0.45, t * 0.06);
        text(glitchText(s.text, lt, 3), W / 2, H * 0.47, size, { split: 6 * Math.exp(-lt * 1.5) + 4 * bi.pulse });
        if (s.sub && lt > 1.6) {
          ctx.save(); ctx.globalAlpha = ease((lt - 1.6) / 0.5);
          ctx.font = "600 " + Math.round(H * 0.04) + "px " + MONO; ctx.fillStyle = "#ffe9f6"; ctx.textAlign = "center";
          ctx.fillText(s.sub.toUpperCase(), W / 2, H * 0.62); ctx.restore();
        }
      } else {
        var sc = CALM ? 1 : 1 + 0.7 * Math.exp(-lt * 11);
        text(s.text, W / 2, H * 0.5, size, { scale: sc, rot: -0.06, split: 10 * Math.exp(-lt * 4) + 5 * bi.pulse });
      }
    }
    if (s.k === "photo" && s.d >= 0.8 && s.i) {
      var pl = imgs[s.i[0]].p;
      if (pl && !has(s, "whiteout")) chip(pl, lt, g);
    }
    rings(t);
    stars(t, s.k === "sigil" ? 0.6 : e, W, H);
    hud(t, bi);
    void p;
  }

  // ---------------------------------------------------------------- frame
  var lastGood = 0;
  function render(t) {
    resize();
    var i = shotAt(t), s = shots[i];
    if (!ready(s) && !CAPTURE) {
      // A photo is still on its way: hold the last shot that is ready.
      i = lastGood; s = shots[i];
      t = Math.min(t, s.t + s.d - 0.001);
    } else lastGood = i;
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);
    if (has(s, "fadein") && i > 0 && ready(shots[i - 1])) uniforms(shots[i - 1], Math.min(t, s.t - 0.001), 1);
    uniforms(s, t, 1);
    overlay(s, t);
  }

  // ---------------------------------------------------------------- playback
  var audio = null, playing = false, muted = false, tStart = 0, wallStart = 0, tNow = 0, raf = 0, poll = 0;
  function now() {
    if (!playing) return tNow;
    var wall = tStart + (performance.now() - wallStart) / 1000;
    if (audio && !audio.paused && !audio.seeking && audio.readyState >= 2) {
      var a = audio.currentTime;
      if (Math.abs(a - wall) > 0.08) { tStart = a; wallStart = performance.now(); wall = a; }
    }
    return wall;
  }
  function frame() {
    if (!playing) return;
    tNow = now();
    if (tNow >= D.dur) { stop(true); return; }
    render(tNow);
    if (seek && !seeking) seek.value = tNow;
    if (clock) clock.textContent = fmt(tNow) + " / " + fmt(D.dur);
    raf = requestAnimationFrame(frame);
  }
  function getAudio() {
    if (!audio && D.music && D.music.src) {
      audio = new Audio(BASE + D.music.src);
      audio.preload = "auto";
      audio.muted = muted;
    }
    return audio;
  }
  function play() {
    if (playing) return;
    if (tNow >= D.dur - 0.05) tNow = 0;
    poster.hidden = true;
    bigPlay.hidden = true;
    root.classList.add("playing");
    toggle.textContent = "pause"; toggle.setAttribute("aria-label", "Pause");
    ensure(tNow, tNow + 4).then(function () {
      playing = true;
      tStart = tNow; wallStart = performance.now();
      var a = getAudio();
      if (a) { a.currentTime = tNow; var pr = a.play(); if (pr && pr.catch) pr.catch(function () {}); }
      clearInterval(poll);
      poll = setInterval(function () { var t = now(); ensure(t, t + 7); evict(t); }, 400);
      frame();
    });
  }
  function stop(ended) {
    playing = false;
    cancelAnimationFrame(raf);
    clearInterval(poll);
    if (audio) audio.pause();
    root.classList.remove("playing");
    toggle.textContent = ended ? "play again" : "resume";
    toggle.setAttribute("aria-label", ended ? "Play again" : "Resume");
    if (ended) { tNow = D.dur; bigPlay.hidden = false; }
  }
  var seeking = false;
  function jump(t) {
    tNow = clamp(t, 0, D.dur - 0.05);
    poster.hidden = true;
    if (playing) { tStart = tNow; wallStart = performance.now(); if (audio) audio.currentTime = tNow; }
    ensure(tNow, tNow + 3).then(function () { if (!playing) render(tNow); });
    if (clock) clock.textContent = fmt(tNow) + " / " + fmt(D.dur);
  }

  bigPlay.addEventListener("click", function () { play(); stage.focus(); });
  toggle.disabled = false;
  toggle.addEventListener("click", function () { playing ? stop(false) : play(); });
  muteBtn.addEventListener("click", function () {
    muted = !muted;
    if (audio) audio.muted = muted;
    muteBtn.setAttribute("aria-pressed", muted ? "true" : "false");
    muteBtn.textContent = muted ? "muted" : "sound on";
  });
  if (seek) {
    seek.max = D.dur;
    seek.addEventListener("input", function () { seeking = true; jump(+seek.value); });
    seek.addEventListener("change", function () { seeking = false; });
  }
  if (fullBtn) {
    if (!stage.requestFullscreen) fullBtn.hidden = true;
    fullBtn.addEventListener("click", function () {
      if (document.fullscreenElement) document.exitFullscreen(); else stage.requestFullscreen().catch(function () {});
    });
  }
  stage.addEventListener("keydown", function (e) {
    if (e.target !== stage) return;
    if (e.key === " " || e.key === "k" || e.key === "Enter") { e.preventDefault(); playing ? stop(false) : play(); }
    else if (e.key === "ArrowRight") { e.preventDefault(); jump(tNow + 5); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); jump(tNow - 5); }
    else if (e.key === "m") muteBtn.click();
    else if (e.key === "f" && fullBtn) fullBtn.click();
  });
  document.addEventListener("visibilitychange", function () { if (document.hidden && playing) stop(false); });
  window.addEventListener("resize", function () { if (!playing && poster.hidden) render(tNow); });
  if (clock) clock.textContent = "0:00 / " + fmt(D.dur);

  // For scripts/render_reels_v2.py: draw any moment, once its photos are in.
  window.__reelsV2 = {
    dur: D.dur,
    fonts: function () { return document.fonts ? Promise.all([document.fonts.load("40px \"Black Han Sans\""), document.fonts.load("600 20px \"IBM Plex Mono\"")]) : Promise.resolve(); },
    frame: function (t) { return ensure(Math.max(0, t - 0.6), t + 0.2).then(function () { poster.hidden = true; render(t); }); }
  };
})();
