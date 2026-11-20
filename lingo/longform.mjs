// Long-form map explainer renderer (Blueprint 04, blueprints/long-form-thelanguagemap.md).
// node longform.mjs <key> [--still 3,40,120] [--workers 3] [--preview]
//   episode:   longform/<key>/episode.mjs  (one line = one narrated sentence)
//   narration: cache/longform/<key>/vo/<id>.wav (python3 longform_tts.py <key>); without it, timing is estimated at 165 wpm
//   output:    out/longform_<key>.mp4 (+ out/longform_<key>_credits.txt)
import fs from "node:fs";
import path from "node:path";
import { spawn, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const W = 1920, H = 1080, FPS = 30;
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const key = args.find((a) => !a.startsWith("--") && !/^[\d.,]+$/.test(a));
if (!key) throw new Error("usage: node longform.mjs <key> [--still t1,t2] [--workers n]");
const EP = (await import(pathToFileURL(path.join(HERE, "longform", key, "episode.mjs")).href)).default;
const CACHE = path.join(HERE, "cache", "longform", key);
fs.mkdirSync(path.join(CACHE, "hear"), { recursive: true });
const nm = (p) => path.join(HERE, "node_modules", p);
const furl = (p) => pathToFileURL(p).href;
const r1 = (n) => Math.round(n * 10) / 10;

// ───────── audio durations ─────────
function dur(file) {
  const r = spawnSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file], { encoding: "utf8" });
  return parseFloat(r.stdout);
}
function hearFile(word) { // trimmed Lingua Libre word -> cache/longform/<key>/hear/<slug>.wav
  const src = path.join(HERE, "incoming", key, `LL-Q9166 (mlt)-GħawdxiVeru-${word}.wav`);
  const out = path.join(CACHE, "hear", word.replace(/[^\p{L}\p{N}]+/gu, "_") + ".wav");
  if (!fs.existsSync(out)) {
    if (!fs.existsSync(src)) throw new Error("missing recording " + src);
    spawnSync("ffmpeg", ["-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "48000", "-af",
      "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,afade=t=in:d=0.02,loudnorm=I=-17:TP=-2", out]);
  }
  return out;
}
function keithFile(a, b) {
  const src = path.join(HERE, "incoming", key, "WIKITONGUES-_Keith_speaking_Maltese.webm");
  const out = path.join(CACHE, "hear", `keith_${a}_${b}.wav`);
  if (!fs.existsSync(out)) spawnSync("ffmpeg", ["-v", "error", "-y", "-ss", String(a), "-t", String(b - a), "-i", src, "-vn", "-ac", "1", "-ar", "48000",
    "-af", `afade=t=in:d=0.1,afade=t=out:st=${b - a - 0.4}:d=0.4,loudnorm=I=-18:TP=-2`, out]);
  return out;
}

// ───────── timeline ─────────
const VOICE = opt("voice", "am_michael"); // narration set: cache/longform/<key>/vo_<voice>/
const VO = path.join(CACHE, "vo_" + VOICE);
let t = 0.6; const T = [];
let estimated = 0;
for (const L of EP.lines) {
  const vo = path.join(VO, L.id + ".wav");
  let sayDur;
  if (fs.existsSync(vo)) sayDur = dur(vo); else { sayDur = L.say.split(/\s+/).length / 2.75 + 0.2; estimated++; }
  const row = { ...L, t0: t, say0: t, sayDur, vo: fs.existsSync(vo) ? vo : null, clips: [] };
  t += sayDur;
  const clips = (L.hear || []).map((w) => ({ word: w, file: hearFile(w) }));
  if (L.keith) clips.push({ word: "keith", file: keithFile(...L.keith) });
  if (clips.length) t += 0.35;
  for (const c of clips) { const d = dur(c.file); row.clips.push({ ...c, t: t, d }); t += d + 0.45; }
  if ((L.show || []).some((s) => s.type === "title")) { row.titleAt = t + 0.1; t += 3.2; }
  if (L.end) { row.endAt = t + 0.3; t += 6.0; }
  t += L.gap ?? 0.38;
  row.t1 = t;
  T.push(row);
}
const TOTAL = t + 0.4;
fs.writeFileSync(path.join(CACHE, `chapters_${VOICE}.json`), JSON.stringify([{ t: 0, title: "Intro" }, ...T.filter((r) => r.kicker).map((r) => ({ t: r.t0, title: r.kicker }))].concat([{ t: T.find((r) => r.id === "z1")?.t0 ?? TOTAL, title: "RECAP" }]), null, 1));
if (estimated) console.log(`  ${estimated}/${T.length} lines have no narration yet: timing estimated at 165 wpm`);
console.log(`  total ${TOTAL.toFixed(1)} s (${(TOTAL / 60).toFixed(2)} min)`);

// ───────── map geometry ─────────
const world = JSON.parse(fs.readFileSync(nm("world-atlas/countries-10m.json")));
const feats = topo.feature(world, world.objects.countries).features;
const S = 20000; // Mercator px per radian (≈349 px per degree)
const proj = d3.geoMercator().scale(S).translate([0, 0]);
const [bx0, by0] = proj([-30, 63]), [bx1, by1] = proj([55, 18]);
proj.clipExtent([[bx0, by0], [bx1, by1]]);
const gp = d3.geoPath(proj).digits(1);
const pxPerDeg = S * Math.PI / 180;
const P = (k) => { const ll = Array.isArray(k) ? k : EP.places[k]; if (!ll) throw new Error("no place " + k); return proj(ll); };
const inBox = (f) => { const [[a, b], [c, d]] = d3.geoBounds(f); return c > -32 && a < 57 && d > 16 && b < 65; };
const boxA = (bx1 - bx0) * (by1 - by0);
const sane = (f) => gp.area(f) < boxA * 0.5; // a mis-wound tiny polygon (e.g. Maldives) would otherwise fill the whole box
const world50 = JSON.parse(fs.readFileSync(nm("world-atlas/countries-50m.json")));
const feats50 = topo.feature(world50, world50.objects.countries).features;
const gp50 = d3.geoPath(proj).digits(0); // the base land layer is drawn every frame: 50m detail keeps frames fast; highlights stay 10m
const detail = new Set(EP.landDetail || []); // small countries drawn from 10m in the base layer too (no 50m edge peeking out at close zoom)
const landD = feats50.filter(inBox).filter(sane).filter((f) => !detail.has(f.id)).map((f) => gp50(f) || "").join("") + feats.filter((f) => detail.has(f.id)).map((f) => gp(f) || "").join("");
function regionD(spec) {
  const f = feats.find((x) => x.id === spec.id);
  if (!f) throw new Error("no country " + spec.id);
  if (!spec.near) return gp(f);
  const polys = f.geometry.type === "MultiPolygon" ? f.geometry.coordinates : [f.geometry.coordinates];
  const pick = polys.filter((c) => d3.geoDistance(d3.geoCentroid({ type: "Polygon", coordinates: c }), spec.near) * 180 / Math.PI < spec.r);
  return gp({ type: "MultiPolygon", coordinates: pick });
}
const REG = Object.fromEntries(Object.entries(EP.regions).sort((x, y) => !!x[1].near - !!y[1].near).map(([k, v]) => [k, regionD(v)])); // parts (near) drawn above whole countries

// camera keyframes (world px + zoom)
const camK = []; let lastCam = null;
for (const r of T) if (r.cam) { const [x, y] = proj(r.cam.c); const z = W / (r.cam.span * pxPerDeg); camK.push({ t: r.t0 - 0.2, x, y, z }); lastCam = r.cam; }
// fills: per region keyframes
const fillK = {}; for (const k of Object.keys(REG)) fillK[k] = [];
const setFill = (tt, obj) => { for (const [k, v] of Object.entries(obj)) { if (!fillK[k]) throw new Error("no region " + k); fillK[k].push({ t: tt, c: v }); } };
for (const r of T) { if (r.fill) setFill(r.t0, r.fill); if (r.then) setFill(r.t0 + r.sayDur * r.then.at, r.then.fill); }
// labels, routes, year, kicker
const labelK = []; // a label set lasts until the next camera move after the line that set it
T.forEach((r, i) => {
  if (r.labels) labelK.push({ t: r.t0, items: r.labels.map(([txt, at]) => ({ txt, p: P(at) })) });
  else if (r.cam && labelK.length && labelK[labelK.length - 1].items.length) labelK.push({ t: r.t0, items: [] });
});
const routes = T.filter((r) => r.route).map((r, i) => {
  const idx = T.indexOf(r), a = P(r.route.from), b = P(r.route.to), mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
  const dx = b[0] - a[0], dy = b[1] - a[1], k = 0.18;
  return { t: r.t0 + 0.2, tOut: (T[idx + 2] || T[T.length - 1]).t1, color: r.route.color, a, b, d: `M${r1(a[0])},${r1(a[1])} Q${r1(mx - dy * k)},${r1(my + dx * k)} ${r1(b[0])},${r1(b[1])}` };
});
const yearK = T.filter((r) => "year" in r).map((r) => ({ t: r.t0, v: r.year }));
const kickK = T.filter((r) => r.kicker).map((r) => ({ t: r.t0, v: r.kicker }));
// overlays
const OV = [];
T.forEach((r, i) => {
  const until = (T[i + (r.hold || 0)] || r).t1 - 0.15;
  for (const s of r.show || []) {
    const o = { ...s, tIn: r.t0 + 0.12, tOut: until };
    if (s.type === "title") { o.tIn = r.titleAt; o.tOut = r.titleAt + 3.0; }
    if (s.from && typeof s.from === "string") { o.a = P(s.from); o.b = P(s.to); }
    if (s.at) o.p = P(s.at);
    OV.push(o);
  }
  for (const c of r.clips) OV.push({ type: "hear", word: c.word, tIn: c.t - 0.15, tOut: c.t + c.d + 0.25, d: c.d });
  if (r.endAt) OV.push({ type: "end", tIn: r.endAt, tOut: TOTAL + 1 });
});
const DATA = { W, H, TOTAL, camK, fillK, labelK, routes, yearK, kickK, OV, title: EP.cardTitle, next: EP.next, colors: EP.colors };

// ───────── paper texture (generated once) ─────────
const TEX = path.join(HERE, "cache", "longform", "paper.png");
if (!fs.existsSync(TEX)) spawnSync("python3", ["-c", `
import numpy as np, zlib, struct
rng=np.random.default_rng(7); n=1024
def blur(a,k):
    for _ in range(k): a=(a+np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1))/5
    return a
g=blur(rng.random((n,n)),2)*0.5+blur(rng.random((n,n)),12)*0.5
fib=blur(rng.random((n,n))**8,1)
v=np.clip(200+ (g-g.mean())/g.std()*14 - fib*40,0,255).astype(np.uint8)
raw=b''.join(b'\\x00'+v[i].tobytes() for i in range(n))
def ch(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
open(${JSON.stringify(TEX)},'wb').write(b'\\x89PNG\\r\\n\\x1a\\n'+ch(b'IHDR',struct.pack('>IIBBBBB',n,n,8,0,0,0,0))+ch(b'IDAT',zlib.compress(raw,9))+ch(b'IEND',b''))
`]);

const fontCss = [
  ...["700", "800", "900", "700-italic", "800-italic"].map((w) => nm(`@fontsource/fraunces/${w}.css`)),
  ...["500", "700", "800"].map((w) => nm(`@fontsource/inter/${w}.css`)),
  nm("@fontsource/noto-naskh-arabic/700.css"),
].map((f) => `<link rel="stylesheet" href="${furl(f)}">`).join("");
const imgUrl = (p) => furl(path.join(HERE, p));
for (const o of OV) if (o.img) o.img = fs.existsSync(path.join(HERE, o.img)) ? imgUrl(o.img) : null;

const html = `<!doctype html><html><head><meta charset="utf-8">${fontCss}<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:${W}px;height:${H}px;overflow:hidden;background:#174a63;font-family:Inter,sans-serif}
#sea{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#2a6d8c 0%,#21607e 45%,#163f55 100%)}
svg{position:absolute;inset:0}
#map{filter:drop-shadow(0 3px 0 rgba(70,50,20,.28)) drop-shadow(0 10px 16px rgba(0,0,0,.28))}
#hi{filter:drop-shadow(2px 6px 0 rgba(40,20,10,.42)) drop-shadow(4px 14px 16px rgba(0,0,0,.4))}
#tex{position:absolute;inset:0;background:url(${furl(TEX)});background-size:1024px;mix-blend-mode:multiply;opacity:.38;pointer-events:none}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0) 55%,rgba(5,20,30,.45) 100%)}
.lab{position:absolute;transform:translate(-50%,-50%);font:800 21px Inter;letter-spacing:.18em;color:#3a2c1e;text-shadow:0 0 6px rgba(240,230,205,.9),0 0 2px rgba(240,230,205,1);white-space:nowrap}
#year{position:absolute;right:56px;top:46px;background:#fbf7ee;border-radius:8px;padding:6px 18px 8px;font:900 46px Fraunces;color:#1c1712;box-shadow:0 6px 16px rgba(0,0,0,.35)}
#kick{position:absolute;left:56px;top:52px;background:#fbf7ee;border-radius:8px;padding:9px 18px;font:800 21px Inter;letter-spacing:.16em;color:#1c1712;box-shadow:0 6px 16px rgba(0,0,0,.3)}
#kick b{display:inline-block;width:10px;height:10px;border-radius:50%;background:#d9533f;margin-right:12px;vertical-align:2px}
.card{position:absolute;background:#fbf7ee;border-radius:10px;box-shadow:0 10px 26px rgba(0,0,0,.38);color:#1c1712}
.k{font:800 17px Inter;letter-spacing:.16em;color:#a2463a;text-transform:uppercase}
.big{font:900 104px/1 Fraunces;color:#d9533f}
.serif{font-family:Fraunces}
.pill{display:inline-block;font:800 14px Inter;letter-spacing:.14em;color:#fff;background:#d9533f;border-radius:5px;padding:3px 8px}
.word{font:italic 800 54px/1.1 Fraunces}
.gloss{font:500 22px Inter;color:#6d6358}
.ar{font:700 42px "Noto Naskh Arabic";direction:rtl}
.cap{position:absolute;left:50%;bottom:64px;transform:translateX(-50%);background:#fbf7ee;border-radius:10px;padding:14px 26px;font:800 30px Inter;color:#1c1712;box-shadow:0 8px 20px rgba(0,0,0,.35);white-space:nowrap}
.stamp{position:absolute;left:50%;top:44%;font:900 92px Inter;letter-spacing:.06em;color:#d9533f;border:9px solid #d9533f;border-radius:14px;padding:6px 30px;background:rgba(251,247,238,.85)}
.dot{display:inline-block;width:13px;height:13px;border-radius:50%;margin:0 4px 4px 0}
.on{outline:5px solid #d9533f;outline-offset:4px}
#ov>div{will-change:transform,opacity}
</style></head><body>
<div id="sea"></div>
<svg id="map" viewBox="0 0 ${W} ${H}"><g id="cam"><path id="land" d="${landD}" fill="#e9dcbf" stroke="#c9b48e" stroke-width="1.2" vector-effect="non-scaling-stroke" stroke-linejoin="round"/></g></svg>
<svg id="hi" viewBox="0 0 ${W} ${H}"><g id="cam2">${Object.entries(REG).map(([k, d]) => `<path id="r_${k}" d="${d}" fill="transparent" stroke="rgba(60,30,20,.35)" stroke-width="1" vector-effect="non-scaling-stroke"/>`).join("")}</g></svg>
<svg id="rt" viewBox="0 0 ${W} ${H}"><g id="cam3"></g></svg>
<div id="tex"></div><div id="vig"></div>
<div id="labs"></div><div id="ov"></div>
<div id="kick" style="opacity:0"></div><div id="year" style="opacity:0"></div>
<script>
const D=${JSON.stringify(DATA)};
const $=(s)=>document.querySelector(s);
const ease=(x)=>x<0?0:x>1?1:x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
const eo=(x)=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const back=(x)=>{x=Math.max(0,Math.min(1,x));const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const hex=(c)=>c?[parseInt(c.slice(1,3),16),parseInt(c.slice(3,5),16),parseInt(c.slice(5,7),16),1]:[233,220,191,0];
const mix=(a,b,k)=>a.map((v,i)=>v+(b[i]-v)*k);
function cam(t){const K=D.camK;let i=K.findIndex(k=>k.t>t);if(i<0)i=K.length;const b=K[Math.max(0,i-1)],a=K[Math.max(0,i-2)]||b;
  const drift=1+0.05*Math.min(1,Math.max(0,(t-b.t-1.7)/14));if(i<=1)return {...K[0],z:K[0].z*drift};const k=ease((t-b.t)/1.7);return {x:a.x+(b.x-a.x)*k,y:a.y+(b.y-a.y)*k,z:Math.exp(Math.log(a.z*(1+0.05*Math.min(1,Math.max(0,(b.t-a.t-1.7)/14))))+(Math.log(b.z*drift)-Math.log(a.z*(1+0.05*Math.min(1,Math.max(0,(b.t-a.t-1.7)/14)))))*k)}}
// build static route + overlay nodes once
const R=$("#cam3");D.routes.forEach((r,i)=>{R.insertAdjacentHTML("beforeend",'<path id="rt'+i+'" d="'+r.d+'" fill="none" stroke="'+r.color+'" stroke-width="5" stroke-linecap="round" vector-effect="non-scaling-stroke" stroke-dasharray="1 14" /><circle id="rh'+i+'" r="9" fill="'+r.color+'" stroke="#fbf7ee" stroke-width="3" vector-effect="non-scaling-stroke"/>');const el=document.getElementById("rt"+i),len=el.getTotalLength();r.pts=Array.from({length:61},(_,j)=>{const q=el.getPointAtLength(len*j/60);return [q.x,q.y]})});
const ov=$("#ov");
function chipHTML(it,lang,col){const [w,g,src]=it;return '<div class="card chip" data-w="'+w+'" style="position:relative;display:inline-block;padding:14px 22px 14px;margin:0 9px;text-align:center">'+(lang?'<div class="pill" style="background:'+(col||"#d9533f")+'">'+lang+'</div>':'')+'<div class="word" style="font-size:'+(g?44:40)+'px;margin-top:4px">'+w+'</div>'+(g?'<div class="gloss">“'+g+'”</div>':'')+(src?'<div class="gloss" style="font-size:19px;color:#a2463a;margin-top:2px">← '+src+'</div>':'')+'</div>'}
const BUILD={
 number:o=>'<div class="card" style="left:50%;top:70px;padding:14px 34px 16px;text-align:center"><div class="big"><span class="n"></span></div><div class="k" style="margin-top:6px;color:#3a2c1e">'+o.caption+'</div></div>',
 chip:o=>'<div style="position:absolute;'+(o.pos==="right"?"right:130px;top:380px":"left:130px;top:380px")+'">'+chipHTML([o.word,o.gloss],o.lang).replace('margin:0 9px','margin:0')+'</div>',
 pair:o=>'<div style="position:absolute;left:50%;bottom:90px;transform:translateX(-50%);display:flex;align-items:center;gap:26px">'+chipHTML([o.a.word,o.a.gloss],o.a.lang).replace('margin:0 9px','margin:0')+'<div style="font:900 60px Fraunces;color:#fbf7ee;text-shadow:0 3px 8px rgba(0,0,0,.5)">≈</div><div class="card" style="position:relative;padding:14px 26px;text-align:center"><div class="pill" style="background:#b98a2c">'+o.b.lang+'</div><div class="ar" style="margin-top:2px">'+o.b.script+'</div><div class="word" style="font-size:34px">'+o.b.word+'</div><div class="gloss">“'+o.b.gloss+'”</div></div></div>',
 chips:o=>'<div style="position:absolute;left:50%;bottom:70px;transform:translateX(-50%);text-align:center;white-space:nowrap">'+(o.title?'<div class="card k" style="position:relative;display:inline-block;padding:7px 16px;margin-bottom:14px;color:#1c1712">'+o.title+'</div><br>':'')+o.items.map(it=>chipHTML(o.plain?[it[0]]:it,o.plain?null:(o.src||"MALTESE"),o.src==="ITALIAN"?"#3f9a6a":o.src==="ENGLISH"?"#3d6fd6":null)).join("")+'</div>',
 caption:o=>'<div class="cap">'+o.text+'</div>',
 card:o=>'<div class="card serif" style="left:50%;top:50%;transform:translate(-50%,-50%);padding:28px 44px;font:900 50px/1.15 Fraunces;text-align:center;max-width:1100px">'+o.text+'</div>',
 stamp:o=>'<div class="stamp">'+o.text+'</div>',
 title:o=>'<div style="position:absolute;inset:0;background:rgba(10,30,42,.35)"></div><div class="card" style="left:50%;top:50%;transform:translate(-50%,-50%);padding:34px 64px 40px;text-align:center;width:1180px"><div class="k" style="color:#d9533f">LingoDude</div><div style="font:900 74px/1.08 Fraunces;margin-top:12px">'+D.title+'</div></div>',
 portrait:o=>'<div class="card" style="right:70px;top:150px;width:300px;padding:22px 20px 18px;text-align:center"><div style="width:210px;height:250px;margin:0 auto;border-radius:50%;border:4px solid #1c1712;overflow:hidden;background:#efe6d3;display:flex;align-items:flex-end;justify-content:center">'+(o.mystery&&!o.reveal?'<div style="font:900 140px Fraunces;color:#1c1712;line-height:250px">?</div>':o.img?'<img src="'+o.img+'" style="width:118%;margin-bottom:-6px">':'<div style="font:900 120px Fraunces;color:#1c1712;line-height:250px">'+(o.reveal?"✓":"?")+'</div>')+'</div><div style="font:900 34px/1.1 Fraunces;margin-top:16px">'+o.name+'</div><div class="k" style="margin-top:8px;font-size:14px;color:#6d6358">'+o.role+'</div></div>',
 doc:o=>'<div class="card" style="left:90px;top:220px;width:560px;padding:26px 30px"><div class="k">'+o.kicker+'</div><div style="font:italic 900 52px/1.1 Fraunces;margin:10px 0 12px">'+o.title+'</div>'+o.lines.map(l=>'<div style="font:500 25px/1.35 Inter;color:#4b4238">'+l+'</div>').join("")+'</div>',
 quote:o=>'<div class="card" style="left:90px;top:240px;width:560px;padding:24px 30px"><div class="k">'+o.kicker+'</div><div style="font:italic 900 56px/1.1 Fraunces;margin-top:10px">“'+o.text+'”</div></div>',
 def:o=>'<div class="card" style="left:90px;top:200px;width:560px;padding:24px 30px"><div class="k">'+o.q+'</div><div style="font:800 30px/1.3 Inter;margin-top:10px">'+o.a+'</div><div style="font:500 25px/1.35 Inter;color:#6d6358;margin-top:8px">'+o.note+'</div></div>',
 dots:o=>{const per=10;return '<div class="card" style="left:90px;top:170px;width:700px;padding:24px 30px"><div class="k">'+o.title+'</div>'+o.rows.map((r,i)=>'<div style="margin-top:16px"><span style="font:900 46px Fraunces;color:'+r[2]+'" class="n'+i+'"></span> <span class="k" style="color:#3a2c1e">'+r[0]+'</span><div style="margin-top:8px;line-height:0">'+Array.from({length:Math.round(r[1]/per)},(_,j)=>'<span class="dot d'+i+'" style="background:'+r[2]+'"></span>').join("")+'</div></div>').join("")+'<div style="font:500 18px Inter;color:#6d6358;margin-top:12px">'+o.unit+'</div></div>'},
 bar:o=>'<div class="card" style="left:50%;bottom:80px;transform:translateX(-50%);width:1300px;padding:24px 30px"><div class="k">'+o.title+'</div><div style="display:flex;height:64px;margin-top:16px;border-radius:8px;overflow:hidden">'+o.parts.map((p,i)=>'<div class="seg" style="width:'+p[1]+'%;background:'+p[2]+';display:flex;align-items:center;justify-content:center;font:800 22px Inter;color:#fff;white-space:nowrap;overflow:hidden">'+p[0]+'</div>').join("")+'</div></div>',
 gauge:o=>'<div class="card" style="left:50%;top:80px;transform:translateX(-50%);width:820px;padding:20px 30px 24px"><div style="display:flex;justify-content:space-between;align-items:baseline"><div class="k" style="color:#3a2c1e;max-width:560px;line-height:1.35">'+o.label+'</div><div style="font:900 70px Fraunces;color:#d9533f"><span class="n"></span>%</div></div><div style="height:12px;background:#e4dccb;border-radius:6px;margin-top:10px"><div class="g" style="height:12px;background:#d9533f;border-radius:6px;width:0"></div></div></div>',
 split:o=>'<div style="position:absolute;left:50%;bottom:80px;transform:translateX(-50%);display:flex;gap:30px">'+[o.left,o.right].map(s=>'<div class="card" style="position:relative;width:440px;padding:20px 26px"><div class="pill" style="background:'+s.color+'">'+s.lang+'</div>'+s.items.map(x=>'<div style="font:italic 800 38px/1.3 Fraunces;margin-top:6px">'+x+'</div>').join("")+'</div>').join("")+'</div>',
 versus:o=>'<div style="position:absolute;left:50%;bottom:90px;transform:translateX(-50%);display:flex;align-items:center;gap:30px">'+[o.a,o.b].map(s=>'<div class="card" style="position:relative;padding:18px 34px;text-align:center"><div class="pill" style="background:'+s.color+'">'+s.lang+'</div><div class="word" style="margin-top:4px">'+s.word+'</div></div>').join('<div style="font:900 50px Fraunces;color:#fbf7ee;text-shadow:0 3px 8px rgba(0,0,0,.5)">vs</div>')+'</div>',
 root:o=>'<div class="card" style="left:50%;bottom:70px;transform:translateX(-50%);padding:22px 34px;display:flex;gap:40px;align-items:center"><div style="text-align:center"><div class="k">ROOT</div><div style="font:900 60px Fraunces;color:#d9533f">'+o.root+'</div></div>'+o.items.map((it,i)=>'<div class="chip" data-w="'+it[0]+'" style="text-align:center;padding:6px 12px;border-radius:8px"><div class="pill">MALTESE</div><div class="word" style="font-size:46px">'+it[0]+'</div><div class="gloss">“'+it[1]+'”</div><div class="ar" style="font-size:32px;margin-top:4px">'+o.arabic[i][1]+'</div><div class="gloss" style="font-style:italic">'+o.arabic[i][0]+'</div></div>').join("")+'</div>',
 speaker:o=>'<div class="card" style="left:50%;top:50%;transform:translate(-50%,-50%);width:640px;padding:28px 34px;text-align:center"><div class="pill">REAL RECORDING · MALTESE</div><div style="font:900 64px Fraunces;margin-top:10px">'+o.name+'</div><div class="k" style="color:#6d6358">'+o.place+' · '+o.src+'</div><div class="wave" style="height:90px;margin-top:16px;display:flex;gap:6px;align-items:center;justify-content:center">'+Array.from({length:30},()=>'<i style="display:block;width:9px;border-radius:5px;background:#d9533f;height:10px"></i>').join("")+'</div></div>',
 hear:o=>o.word==="keith"?'':'<div class="card" style="left:50%;top:76px;transform:translateX(-50%);padding:10px 22px;display:flex;gap:14px;align-items:center;white-space:nowrap"><span class="pill">▶ HEAR IT</span><span style="font:italic 800 34px Fraunces">'+o.word+'</span></div>',
 end:o=>'<div style="position:absolute;inset:0;background:rgba(8,24,34,.62)"></div><div style="position:absolute;left:0;right:0;top:40%;text-align:center"><div style="font:900 110px Fraunces;color:#fbf7ee">LingoDude</div><div style="display:inline-block;margin-top:18px;background:#fbf7ee;border-radius:8px;padding:10px 22px;font:800 24px Inter;letter-spacing:.08em;color:#1c1712">NEXT: '+D.next.toUpperCase()+'</div></div>',
 dist:o=>'', bubble:o=>'<div class="card bub" style="padding:10px 18px;font:italic 800 32px Fraunces;white-space:nowrap">'+o.text+'</div>',
};
D.OV.forEach((o,i)=>{const el=document.createElement("div");el.style.cssText="position:absolute;inset:0;opacity:0";el.innerHTML=BUILD[o.type](o);ov.appendChild(el);o.el=el;
  if(o.type==="dist"){R.insertAdjacentHTML("beforeend",'<path id="ds'+i+'" d="M'+o.a[0]+','+o.a[1]+' L'+o.b[0]+','+o.b[1]+'" stroke="#fbf7ee" stroke-width="3" stroke-dasharray="8 8" vector-effect="non-scaling-stroke" opacity="0"/>');el.innerHTML='<div class="card dl" style="padding:6px 14px;font:800 24px Inter;white-space:nowrap">'+o.text+'</div>'}});
const labs=$("#labs");
function setT(t){
  const c=cam(t),z=c.z,tr='translate('+(${W}/2)+' '+(${H}/2)+') scale('+z+') translate('+(-c.x)+' '+(-c.y)+')';
  ["cam","cam2","cam3"].forEach(id=>document.getElementById(id).setAttribute("transform",tr));
  const sp=(p)=>[(p[0]-c.x)*z+${W}/2,(p[1]-c.y)*z+${H}/2];
  for(const k in D.fillK){const K=D.fillK[k];let col=[233,220,191,0];let prev=col;
    for(const f of K){if(f.t>t)break;const target=hex(f.c);const kk=eo((t-f.t)/0.8);col=mix(prev,target,kk);prev=kk>=1?target:col}
    document.getElementById("r_"+k).setAttribute("fill",'rgba('+col[0]+','+col[1]+','+col[2]+','+col[3]+')');
    document.getElementById("r_"+k).setAttribute("stroke-opacity",col[3])}
  // labels
  let L=null,Lt=0;for(const l of D.labelK){if(l.t<=t){L=l;Lt=l.t}}
  labs.innerHTML="";if(L){const a=Math.min(1,(t-Lt)/0.5);L.items.forEach(it=>{const p=sp(it.p);if(p[0]<-200||p[0]>${W}+200||p[1]<-100||p[1]>${H}+100)return;labs.insertAdjacentHTML("beforeend",'<div class="lab" style="left:'+p[0]+'px;top:'+(p[1]-34)+'px;opacity:'+a+'">'+it.txt+'</div>')})}
  // routes
  D.routes.forEach((r,i)=>{const p=document.getElementById("rt"+i),h=document.getElementById("rh"+i);const k=eo((t-r.t)/1.6),out=1-Math.min(1,Math.max(0,(t-r.tOut)/0.5));
    const vis=(t>=r.t&&out>0)?out:0;p.style.opacity=vis;h.style.opacity=vis;if(!vis)return;
    const m=Math.max(1,Math.round(k*(r.pts.length-1)));p.setAttribute("d","M"+r.pts.slice(0,m+1).map(q=>q[0]+","+q[1]).join(" L"));
    const q=r.pts[m];h.setAttribute("cx",q[0]);h.setAttribute("cy",q[1]);h.setAttribute("r",9/z);});
  // year + kicker
  let y=null;for(const k of D.yearK)if(k.t<=t)y=k;const ye=$("#year");if(y&&y.v){ye.textContent=y.v;ye.style.opacity=Math.min(1,(t-y.t)/0.3)}else ye.style.opacity=0;
  let kk=null;for(const k of D.kickK)if(k.t<=t)kk=k;const ke=$("#kick");if(kk&&t-kk.t<6){ke.innerHTML="<b></b>"+kk.v;const a=Math.min(1,(t-kk.t)/0.35)*Math.min(1,(kk.t+6-t)/0.5);ke.style.opacity=a;ke.style.transform="translateX("+(-30*(1-eo((t-kk.t)/0.4)))+"px)"}else ke.style.opacity=0;
  // overlays
  let hearWord=null;for(const o of D.OV)if(o.type==="hear"&&t>=o.tIn&&t<=o.tOut)hearWord=o.word;
  D.OV.forEach((o,i)=>{const el=o.el;const a=Math.min(eo((t-o.tIn)/0.3),1-eo((t-o.tOut)/0.3)); if(t<o.tIn-0.01||t>o.tOut+0.3){el.style.opacity=0;if(o.type==="dist"){document.getElementById("ds"+i).setAttribute("opacity",0)}return}
    el.style.opacity=Math.max(0,a);const p=eo((t-o.tIn)/0.35);
    if(!["title","end","stamp","dist","bubble"].includes(o.type))el.style.transform="scale("+(0.94+0.06*back((t-o.tIn)/0.35))+")",el.style.transformOrigin="50% 60%";
    if(o.type==="stamp"){const s=el.firstChild;const q=Math.min(1,(t-o.tIn)/0.14);s.style.transform="translate(-50%,-50%) rotate(-8deg) scale("+(1.5-0.5*q)+")"}
    if(o.type==="number"){const q=eo((t-o.tIn)/1.1);const v=o.from+(o.to-o.from)*q;el.querySelector(".n").textContent=(o.prefix||"")+(o.decimals?v.toFixed(o.decimals):Math.round(v).toLocaleString("en-US"))+(o.suffix||"")}
    if(o.type==="gauge"){const q=eo((t-o.tIn-0.2)/1.1);el.querySelector(".n").textContent=(o.prefix||"")+Math.round(o.value*q);el.querySelector(".g").style.width=(o.value*q)+"%"}
    if(o.type==="dots"){o.rows.forEach((r,ri)=>{const st=o.tIn+0.3+ri*1.6;const q=eo((t-st)/1.2);el.querySelector(".n"+ri).textContent=Math.round(r[1]*q);el.querySelectorAll(".d"+ri).forEach((d,j,all)=>d.style.opacity=j<q*all.length?1:0)})}
    if(o.type==="bar"){el.querySelectorAll(".seg").forEach((s,j)=>{const q=eo((t-o.tIn-0.2-j*0.35)/0.6);s.style.width=(o.parts[j][1]*q)+"%"})}
    if(o.type==="speaker"){const on=D.OV.find(h=>h.type==="hear"&&h.word==="keith"&&t>=h.tIn&&t<=h.tOut);el.querySelectorAll(".wave i").forEach((b,j)=>{b.style.height=(on?10+70*Math.abs(Math.sin(t*9+j*1.7)*Math.sin(t*3.1+j*.6)):10)+"px"})}
    if(o.type==="dist"){const a2=sp(o.a),b2=sp(o.b);document.getElementById("ds"+i).setAttribute("opacity",Math.max(0,a));const d=el.firstChild;d.style.position="absolute";d.style.left=((a2[0]+b2[0])/2)+"px";d.style.top=((a2[1]+b2[1])/2)+"px";d.style.transform="translate(-50%,-50%)"}
    if(o.type==="bubble"){const p2=sp(o.p);const d=el.firstChild;d.style.position="absolute";d.style.left=p2[0]+"px";d.style.top=(p2[1]-70)+"px";d.style.transform="translate(-50%,-50%) scale("+(0.8+0.2*back((t-o.tIn)/0.35))+")"}
    el.querySelectorAll(".chip").forEach(ch=>ch.classList.toggle("on",ch.dataset.w===hearWord));
  });
}
window.setT=setT;
</script></body></html>`;

// ───────── thumbnail (--thumb): map + inset, channel look (white name strip, flag, Wojak, red hook with white outline) ─────────
if (opt("thumb")) {
  const th = EP.thumb, tw = 1280, thh = 720;
  const camT = (c, w, h) => { const [x, y] = proj(c.c); const z = w / (c.span * pxPerDeg); return `translate(${w / 2} ${h / 2}) scale(${z}) translate(${-x} ${-y})`; };
  const fills = (f) => Object.entries(f).map(([k, c]) => `<path d="${REG[k]}" fill="${c}" stroke="rgba(60,30,20,.35)" stroke-width="1" vector-effect="non-scaling-stroke"/>`).join("");
  const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
  const wj = path.join(CACHE, "thumb_wj.png"); spawnSync("convert", [path.join(HERE, th.wojak), "-trim", "+repage", wj]);
  const IS = th.inset;
  const page = `<!doctype html><meta charset="utf-8">${fontCss}<link rel="stylesheet" href="${furl(nm("@fontsource/montserrat/800.css"))}"><style>*{margin:0;padding:0}body{width:${tw}px;height:${thh}px;overflow:hidden;background:#174a63}
.a{position:absolute}#sea{position:absolute;inset:0;background:radial-gradient(ellipse at 60% 50%,#2a6d8c 0%,#21607e 45%,#163f55 100%)}
.m{filter:drop-shadow(0 3px 0 rgba(70,50,20,.28)) drop-shadow(0 8px 12px rgba(0,0,0,.28))}.h{filter:drop-shadow(2px 6px 0 rgba(40,20,10,.45)) drop-shadow(4px 12px 14px rgba(0,0,0,.4))}
#tex{position:absolute;inset:0;background:url(${furl(TEX)});background-size:800px;mix-blend-mode:multiply;opacity:.36}</style>
<div id="sea"></div>
<svg class="a m" style="inset:0" viewBox="0 0 ${tw} ${thh}"><g transform="${camT(th.cam, tw, thh)}"><path d="${landD}" fill="#e9dcbf" stroke="#c9b48e" stroke-width="1" vector-effect="non-scaling-stroke"/></g></svg>
<svg class="a h" style="inset:0" viewBox="0 0 ${tw} ${thh}"><g transform="${camT(th.cam, tw, thh)}">${fills(th.fill)}</g></svg>
<div id="tex"></div>
<div class="a" style="left:${IS.x - IS.r}px;top:${IS.y - IS.r}px;width:${IS.r * 2}px;height:${IS.r * 2}px;border-radius:50%;overflow:hidden;border:8px solid #fbf7ee;box-shadow:0 12px 30px rgba(0,0,0,.5);background:radial-gradient(#2a6d8c,#1c5672)">
 <svg class="a h" style="inset:0" viewBox="0 0 ${IS.r * 2} ${IS.r * 2}"><g transform="${camT(IS.cam, IS.r * 2, IS.r * 2)}">${fills({ malta: th.fill.malta })}</g></svg></div>
<div class="a" style="left:${IS.x + IS.bx}px;top:${IS.y + IS.by}px;background:#fbf7ee;border-radius:12px;padding:8px 18px;font:italic 800 42px Fraunces;color:#1c1712;box-shadow:0 8px 18px rgba(0,0,0,.45);white-space:nowrap">${th.bubble}</div>
<div class="a" style="left:0;top:0;width:${tw}px;height:78px;background:#fff;text-align:center;font:800 50px/80px Montserrat;color:#111">${th.name}</div>
<div class="a" style="right:40px;top:112px;width:240px;height:160px;background:url('${furl(nm("flag-icons/flags/4x3/" + th.flag + ".svg"))}') center/cover;box-shadow:0 6px 18px rgba(0,0,0,.45)"></div>
<img class="a" src="${furl(wj)}" style="left:-30px;bottom:0;height:470px">
<div class="a" style="right:40px;bottom:268px;background:#d9533f;border-radius:8px;padding:6px 16px;font:800 30px Inter;letter-spacing:.08em;color:#fff;box-shadow:0 6px 14px rgba(0,0,0,.4)">${th.tag}</div>
<div class="a" style="right:40px;bottom:46px;text-align:right;font:800 ${th.hookSize || 104}px/1.02 Montserrat;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45)">${th.hook.join("<br>")}</div>`;
  const f = path.join(CACHE, "thumb.html"); fs.writeFileSync(f, page);
  const b2 = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium" });
  const p = await b2.newPage({ viewport: { width: tw, height: thh } });
  await p.goto(furl(f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const out = path.join(HERE, "out", "brand", `thumbL_${key}.png`); await p.screenshot({ path: out }); await b2.close(); console.log(out);
  process.exit(0);
}

// ───────── render ─────────
const pageFile = path.join(CACHE, `page_${VOICE}.html`);
fs.writeFileSync(pageFile, html);
console.log(`  page ${(html.length / 1e6).toFixed(1)} MB`);
const browserArgs = ["--font-render-hinting=none", "--disable-lcd-text"];
const stills = opt("still", null);
const OUT = path.join(HERE, "out");
async function openPage(b) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto(furl(pageFile)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  return p;
}
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium", args: browserArgs });
if (stills) {
  const p = await openPage(b);
  const list = String(stills).split(",").map((s) => (/^[a-z]/.test(s) ? T.find((r) => r.id === s).t0 + 1.2 : +s));
  for (const s of list) { await p.evaluate((x) => window.setT(x), s); const f = path.join(OUT, `longform_${key}_${s.toFixed(1)}s.png`); await p.screenshot({ path: f }); console.log(f); }
  await b.close();
  process.exit(0);
}
// narration + Hear-It mix (numpy), then frames in parallel chunks
const mixFile = path.join(CACHE, `mix_${VOICE}.wav`);
fs.writeFileSync(path.join(CACHE, `mix_${VOICE}.json`), JSON.stringify({ total: TOTAL, items: T.flatMap((r) => [...(r.vo ? [{ f: r.vo, t: r.say0, kind: "vo" }] : []), ...r.clips.map((c) => ({ f: c.file, t: c.t, kind: "hear" }))]) }));
const mix = spawnSync("python3", [path.join(HERE, "longform_mix.py"), path.join(CACHE, `mix_${VOICE}.json`), mixFile], { stdio: "inherit" });
if (mix.status) throw new Error("mix failed");
const workers = +opt("workers", 3), nF = Math.ceil(TOTAL * FPS), per = Math.ceil(nF / workers);
const parts = [];
await Promise.all(Array.from({ length: workers }, async (_, w) => {
  const p = await openPage(b), f0 = w * per, f1 = Math.min(nF, f0 + per), out = path.join(CACHE, `part${w}_${VOICE}.mp4`); parts[w] = out;
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", opt("preview") ? "veryfast" : "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = f0; f < f1; f++) {
    await p.evaluate((x) => window.setT(x), f / FPS);
    const buf = await p.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (w === 0 && f % 300 === 0) console.log(`  frame ${f}/${f1} (worker 0)`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r)); await p.close();
}));
await b.close();
fs.writeFileSync(path.join(CACHE, `parts_${VOICE}.txt`), parts.map((p) => `file '${p}'`).join("\n"));
const final = path.join(OUT, `longform_${key}_${VOICE}.mp4`);
spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", path.join(CACHE, `parts_${VOICE}.txt`), "-i", mixFile, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final], { stdio: "inherit" });
console.log(final);
