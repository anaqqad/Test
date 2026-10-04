// Renders the videos: HTML/SVG frames in headless Chromium -> x264, then audio mix -> out/<video>.mp4
//   node render.mjs <video> [--preview] [--still i,j] [--items 0-3] [--fps 30] [--workers 3]
import fs from "node:fs";
import path from "node:path";
import { spawn, execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";
import { chromium } from "playwright-core";
import { character, scene, shade } from "./art.mjs";
import { VIDEOS, CHANNEL } from "./videos.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CACHE = path.join(HERE, "cache"), OUT = path.join(HERE, "out");
fs.mkdirSync(path.join(CACHE, "pages"), { recursive: true });
fs.mkdirSync(OUT, { recursive: true });
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const FPS = +opt("fps", 30), PREVIEW = args.includes("--preview");
const fileUrl = (p) => pathToFileURL(p).href;
const nm = (p) => path.join(HERE, "node_modules", p);

// ---------------- shared bits ----------------
const FONT_CSS = [600, 700, 800].map((w) => `<link rel="stylesheet" href="${fileUrl(nm(`@fontsource/montserrat/${w}.css`))}">`).join("");
const world = JSON.parse(fs.readFileSync(nm("world-atlas/land-110m.json")));
const land = topo.feature(world, world.objects.land);

function globe([lat, lon], size = 250) {
  const p = d3.geoOrthographic().rotate([-lon, -lat * 0.8]).scale(size / 2 - 4).translate([size / 2, size / 2]).clipAngle(90);
  const g = d3.geoPath(p);
  const [x, y] = p([lon, lat]);
  const grat = d3.geoGraticule().step([20, 20])();
  return `<svg viewBox="0 0 ${size} ${size}" width="${size}" height="${size}">
    <defs><radialGradient id="oc" cx=".38" cy=".32"><stop offset="0" stop-color="#4f9bd0"/><stop offset="1" stop-color="#173f66"/></radialGradient>
    <radialGradient id="gl" cx=".35" cy=".3"><stop offset="0" stop-color="#fff" stop-opacity=".35"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
    <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 4}" fill="url(#oc)"/>
    <path d="${g(grat)}" fill="none" stroke="#bfe0ff" stroke-opacity=".18" stroke-width="1"/>
    <path d="${g(land)}" fill="#efe3c2" stroke="#9c8a62" stroke-width="1"/>
    <circle class="pulse" cx="${x}" cy="${y}" r="10" fill="none" stroke="#ff3b30" stroke-width="4"/>
    <circle cx="${x}" cy="${y}" r="8" fill="#ff3b30" stroke="#fff" stroke-width="3"/>
    <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 4}" fill="url(#gl)" stroke="#fff" stroke-width="5"/></svg>`;
}

const FLAGS = {
  eo: `<svg viewBox="0 0 3 2"><rect width="3" height="2" fill="#009933"/><rect width="1" height="1" fill="#fff"/><path transform="translate(.5 .5) scale(.4)" d="M0 -1 L.29 -.4 L.95 -.31 L.48 .15 L.59 .81 L0 .5 L-.59 .81 L-.48 .15 L-.95 -.31 L-.29 -.4Z" fill="#009933"/></svg>`,
  kernow: `<svg viewBox="0 0 5 3"><rect width="5" height="3" fill="#111"/><rect x="2.1" width=".8" height="3" fill="#fff"/><rect y="1.1" width="5" height=".8" fill="#fff"/></svg>`,
  liv: `<svg viewBox="0 0 5 3"><rect width="5" height="3" fill="#2f7d3a"/><rect y="1.2" width="5" height=".6" fill="#fff"/><rect y="1.8" width="5" height="1.2" fill="#2f5fa8"/></svg>`,
  nfris: `<svg viewBox="0 0 5 3"><rect width="5" height="1" fill="#f2c200"/><rect y="1" width="5" height="1" fill="#c8102e"/><rect y="2" width="5" height="1" fill="#1f4fa0"/></svg>`,
  gag: `<svg viewBox="0 0 5 3"><rect width="5" height="1.8" fill="#1f5fbf"/><rect y="1.8" width="5" height=".6" fill="#fff"/><rect y="2.4" width="5" height=".6" fill="#d52b1e"/>${[1.4, 2.5, 3.6].map((x) => `<path transform="translate(${x} ${x === 2.5 ? 0.7 : 0.95}) scale(.28)" d="M0 -1 L.29 -.4 L.95 -.31 L.48 .15 L.59 .81 L0 .5 L-.59 .81 L-.48 .15 L-.95 -.31 L-.29 -.4Z" fill="#f2c200"/>`).join("")}</svg>`,
};
function flagHtml(code, h) {
  if (!code) return "";
  const w = Math.round(h * 4 / 3);
  if (FLAGS[code]) return `<span class="flag" style="width:${Math.round(h * 5 / 3)}px;height:${h}px">${FLAGS[code]}</span>`;
  const f = nm(`flag-icons/flags/4x3/${code}.svg`);
  return fs.existsSync(f) ? `<span class="flag" style="width:${w}px;height:${h}px"><img src="${fileUrl(f)}"></span>` : "";
}

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
// bold numbers and quoted words so cards scan quickly
const rich = (s) => esc(s).replace(/('[^']{2,60}'|\b\d[\d,.]*\b(?:\s?(?:million|years|consonants|vowels|letters|sounds|tones|speakers|cases|words))?)/g, "<b>$1</b>");

const BASE_CSS = `
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;overflow:hidden;background:#000;font-family:Montserrat,"DejaVu Sans",sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}
.flag{display:inline-block;border-radius:8px;overflow:hidden;box-shadow:0 3px 10px rgba(0,0,0,.25),0 0 0 2px rgba(0,0,0,.08);vertical-align:middle;flex:none}
.flag img,.flag svg{width:100%;height:100%;display:block;object-fit:cover}
b{font-weight:800;color:var(--accent)}
`;

// ---------------- page templates ----------------
function storyPage(video, item, idx, dur, audio) {
  const accent = video.accent || "#d1495b";
  const times = item.cards.map((_, i) => 1.1 + i * 5.0);
  const caps = audio?.captions || [];
  const listen = caps.length ? "" : `<div id="listen" class="abs pill"><span class="eq"><i></i><i></i><i></i><i></i></span>Listen</div>`;
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${BASE_CSS}
  :root{--accent:${accent}}
  #bg{left:-40px;top:-40px;width:2000px;height:1160px;transform-origin:60% 40%}
  #bg svg{width:100%;height:100%}
  #bar{left:0;top:0;width:1920px;height:132px;background:linear-gradient(#ffffff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;gap:26px}
  #bar h1{font-weight:800;font-size:80px;letter-spacing:-1px;color:#18181d}
  #count{right:46px;top:16px;text-align:right}
  #count .n{font-weight:800;font-size:54px;color:#18181d;line-height:1}
  #count .l{font-weight:700;font-size:19px;letter-spacing:3px;text-transform:uppercase;color:${accent};margin-top:6px}
  #brand{left:40px;top:38px;font-weight:800;font-size:26px;color:#18181d;opacity:.85;display:flex;align-items:center;gap:12px}
  #brand small{display:block;font-weight:600;font-size:16px;color:#888;letter-spacing:1px}
  #char{left:10px;bottom:-60px;width:660px;height:951px;transform-origin:50% 100%}
  #char svg{width:100%;height:100%;filter:drop-shadow(0 18px 30px rgba(0,0,0,.35))}
  #cards{left:690px;top:178px;width:890px;display:flex;flex-direction:column;gap:26px}
  .card{background:rgba(255,255,255,.96);border-radius:22px;padding:24px 32px 26px 40px;font-weight:600;font-size:32px;line-height:1.36;color:#1d1d22;box-shadow:0 14px 34px rgba(0,0,0,.30);position:relative;opacity:0}
  .card:before{content:"";position:absolute;left:0;top:18px;bottom:18px;width:9px;border-radius:0 6px 6px 0;background:var(--accent)}
  #globe{right:44px;top:172px;width:260px;text-align:center}
  #globe svg{filter:drop-shadow(0 12px 22px rgba(0,0,0,.4))}
  #globe .lab{margin-top:10px;display:inline-block;background:rgba(15,18,28,.82);color:#fff;font-weight:700;font-size:21px;padding:8px 16px;border-radius:14px;line-height:1.25}
  .pill{left:50%;bottom:44px;transform:translateX(-50%);background:rgba(15,18,28,.85);color:#fff;font-weight:700;font-size:28px;padding:12px 26px;border-radius:40px;display:flex;align-items:center;gap:14px;box-shadow:0 8px 24px rgba(0,0,0,.3);white-space:nowrap}
  .pill.muted{color:#cfd3dc;font-size:24px}
  #listen{left:1135px}
  .eq{display:flex;gap:4px;align-items:flex-end;height:26px}.eq i{display:block;width:6px;background:${accent};border-radius:3px;height:10px}
  #cap{left:1135px;font-size:40px;padding:14px 34px;opacity:0}
  #cap .w{font-weight:800}
  #fade{left:0;top:0;width:1920px;height:1080px;background:#000;pointer-events:none}
  </style></head><body>
  <div id="bg" class="abs">${scene(item.scene, item.name)}</div>
  <div id="char" class="abs">${character(item.char, "c" + idx)}</div>
  <div id="cards" class="abs">${item.cards.map((c) => `<div class="card">${rich(c)}</div>`).join("")}</div>
  ${item.loc ? `<div id="globe" class="abs">${globe(item.loc)}<br><span class="lab">📍 ${esc(item.loc[2])}</span></div>` : ""}
  ${listen}
  <div id="cap" class="abs pill"><span>🔊</span><span class="w"></span></div>
  <div id="bar" class="abs">${flagHtml(item.flag, 66)}<h1>${esc(item.name)}</h1></div>
  <div id="brand" class="abs"><div>${CHANNEL}<small>${esc(video.part || "")}</small></div></div>
  <div id="count" class="abs"><div class="n">${esc(item.speakers)}</div><div class="l">${video.counterLabel}</div></div>
  <div id="fade" class="abs"></div>
  <script>
  const D=${dur}, T=${JSON.stringify(times)}, CAPS=${JSON.stringify(caps)};
  const $=(s)=>document.querySelector(s), cards=[...document.querySelectorAll('.card')], eq=[...document.querySelectorAll('.eq i')];
  const ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3), back=(x)=>{x=Math.min(1,Math.max(0,x));const c=1.5;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  window.setT=(t)=>{
    $('#bg').style.transform='scale('+(1.0+0.05*t/D)+') translateX('+(-12*t/D)+'px)';
    const ci=ease(t/0.7); $('#char').style.transform='translateY('+((1-ci)*140+Math.sin(t*1.6)*5)+'px) rotate('+(Math.sin(t*1.1)*0.7)+'deg)';
    cards.forEach((c,i)=>{const k=(t-T[i])/0.5; c.style.opacity=Math.min(1,Math.max(0,k*1.6)); c.style.transform='translateY('+(1-back(k))*36+'px) scale('+(0.96+0.04*back(k))+')';});
    const g=$('#globe'); if(g){const k=ease((t-0.4)/0.6); g.style.opacity=k; g.style.transform='scale('+(0.8+0.2*back((t-0.4)/0.6))+')'; const p=g.querySelector('.pulse'); const ph=(t*0.9)%1; p.setAttribute('r',8+ph*26); p.style.opacity=1-ph;}
    const l=$('#listen'); if(l){l.style.opacity=ease((t-0.8)/0.4);}
    eq.forEach((e,i)=>e.style.height=(8+Math.abs(Math.sin(t*(5+i*1.7)+i))*18)+'px');
    const cap=CAPS.find(c=>t>=c.t-0.15&&t<=c.t+Math.max(c.d,0.9)+0.35); const ce=$('#cap');
    if(cap){ce.style.opacity=1; ce.querySelector('.w').textContent=cap.text;} else ce.style.opacity=0;
    $('#bar').style.transform='translateY('+(-(1-ease(t/0.45))*140)+'px)';
    $('#fade').style.opacity=Math.max(0,1-t/0.35, (t-(D-0.3))/0.3);
  };
  </script></body></html>`;
}

function rankingPage(video, items, idx, dur, audio) {
  const item = items[idx];
  const col = (s) => (s <= 3 ? "#34c759" : s <= 5 ? "#ffcc00" : s <= 7.5 ? "#ff9500" : "#ff3b30");
  const accent = col(item.score);
  const prev = items.slice(0, idx);
  const axisX = (s) => 140 + (s / 10) * 1640;
  const stack = {};
  const placed = prev.map((p) => { const k = p.score; stack[k] = (stack[k] || 0) + 1; return { p, lvl: stack[k] - 1 }; });
  const curLvl = stack[item.score] || 0;
  const caps = audio?.captions || [];
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${BASE_CSS}
  :root{--accent:${accent}}
  body{background:radial-gradient(1400px 900px at 28% 55%, ${shade(accent, -0.55)} 0%, #0b0f1a 55%, #05070c 100%)}
  #grid{left:0;top:0;width:1920px;height:1080px;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:60px 60px}
  #glow{left:60px;top:150px;width:760px;height:760px;border-radius:50%;background:radial-gradient(${accent}55,transparent 65%)}
  #char{left:90px;bottom:110px;width:620px;height:893px;transform-origin:50% 100%;-webkit-mask-image:linear-gradient(#000 82%,transparent 99%)}
  #char svg{width:100%;height:100%;filter:drop-shadow(0 22px 40px rgba(0,0,0,.6))}
  #head{left:820px;top:150px;display:flex;align-items:center;gap:30px}
  #head h1{font-weight:800;font-size:96px;color:#fff;letter-spacing:-1px}
  #score{left:820px;top:290px;display:flex;align-items:baseline;gap:22px}
  #score .n{font-weight:800;font-size:150px;color:${accent};line-height:1;text-shadow:0 0 40px ${accent}66}
  #score .l{font-weight:700;font-size:26px;color:#9aa3b5;letter-spacing:4px;text-transform:uppercase}
  #meter{left:824px;top:465px;width:960px;height:26px;border-radius:13px;background:rgba(255,255,255,.1);overflow:hidden}
  #meter i{display:block;height:100%;width:0;border-radius:13px;background:linear-gradient(90deg,#34c759,#ffcc00 45%,#ff9500 70%,#ff3b30)}
  #meter i{background-size:960px 100%}
  #chip{left:824px;top:520px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.14);color:#dfe4ee;font-weight:700;font-size:24px;padding:10px 20px;border-radius:14px}
  #text{left:824px;top:600px;width:960px;color:#eef1f7;font-weight:600;font-size:34px;line-height:1.42}
  #text b{color:${accent}}
  #axis{left:0;top:930px;width:1920px;height:150px}
  #axis .line{position:absolute;left:140px;width:1640px;top:96px;height:4px;background:rgba(255,255,255,.25);border-radius:2px}
  #axis .tk{position:absolute;top:108px;font-weight:700;font-size:18px;color:#7c869a;transform:translateX(-50%)}
  #axis .end{position:absolute;top:104px;font-weight:800;font-size:18px;letter-spacing:2px}
  .mini{position:absolute;transform:translate(-50%,0)}
  #top{left:40px;top:40px;color:#c7cdd9;font-weight:700;font-size:24px}
  #top small{display:block;color:#7c869a;font-size:18px;font-weight:600}
  #brand{right:40px;top:40px;color:#fff;font-weight:800;font-size:26px;opacity:.85}
  #rank{right:40px;top:80px;color:#7c869a;font-weight:700;font-size:20px}
  #cap{left:1300px;top:862px;transform:translateX(-50%);background:rgba(255,255,255,.1);color:#fff;font-weight:800;font-size:34px;padding:10px 28px;border-radius:30px;opacity:0;white-space:nowrap}
  #fade{left:0;top:0;width:1920px;height:1080px;background:#000}
  </style></head><body>
  <div id="grid" class="abs"></div><div id="glow" class="abs"></div>
  <div id="top" class="abs">${esc(video.title)}<small>${esc(video.part)}</small></div>
  <div id="brand" class="abs">${CHANNEL}</div><div id="rank" class="abs">#${idx + 1} of ${items.length}</div>
  <div id="char" class="abs">${character(item.char, "r" + idx)}</div>
  <div id="head" class="abs">${flagHtml(item.flag, 90)}<h1>${esc(item.name)}</h1></div>
  <div id="score" class="abs"><span class="n">0/10</span><span class="l">${video.scoreLabel}</span></div>
  <div id="meter" class="abs"><i></i></div>
  <div id="chip" class="abs">⏱ ~${item.weeks} weeks of full-time classes (US Foreign Service Institute)</div>
  <div id="text" class="abs">${item.cards.map(rich).join("<br>")}</div>
  <div id="cap" class="abs">🔊 <span class="w"></span></div>
  <div id="axis" class="abs"><div class="line"></div>
    <span class="end" style="left:60px;color:#34c759">EASY</span><span class="end" style="left:1800px;color:#ff3b30">HARD</span>
    ${[0, 2, 4, 6, 8, 10].map((s) => `<span class="tk" style="left:${axisX(s)}px">${s}</span>`).join("")}
    ${placed.map(({ p, lvl }) => `<span class="mini" style="left:${axisX(p.score)}px;top:${50 - lvl * 40}px">${flagHtml(p.flag, 36)}</span>`).join("")}
    <span class="mini" id="cur" style="left:${axisX(item.score)}px;top:${50 - curLvl * 40}px">${flagHtml(item.flag, 36)}</span>
  </div>
  <div id="fade" class="abs"></div>
  <script>
  const D=${dur}, S=${item.score}, CAPS=${JSON.stringify(caps)};
  const $=(s)=>document.querySelector(s);
  const ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3), back=(x)=>{x=Math.min(1,Math.max(0,x));const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const fmt=(v)=>(Math.round(v*2)/2).toString().replace(/\\.0$/,'');
  window.setT=(t)=>{
    const ci=ease(t/0.7); $('#char').style.transform='translateY('+((1-ci)*120+Math.sin(t*1.6)*5)+'px) rotate('+(Math.sin(t*1.1)*0.7)+'deg)';
    $('#head').style.opacity=ease((t-0.2)/0.4); $('#head').style.transform='translateX('+(1-ease((t-0.2)/0.5))*60+'px)';
    const k=ease((t-0.9)/1.4); $('#score .n').textContent=fmt(S*k)+'/10'; $('#score').style.opacity=ease((t-0.7)/0.3);
    $('#meter i').style.width=(S/10*100*k)+'%';
    $('#chip').style.opacity=ease((t-1.8)/0.4);
    $('#text').style.opacity=ease((t-2.2)/0.5); $('#text').style.transform='translateY('+(1-ease((t-2.2)/0.5))*24+'px)';
    const c=$('#cur'); const dk=(t-2.6)/0.6; c.style.opacity=dk>0?1:0; c.style.transform='translate(-50%,'+(-(1-back(dk))*120)+'px)';
    const cap=CAPS.find(x=>t>=x.t-0.15&&t<=x.t+Math.max(x.d,0.9)+0.35); const ce=$('#cap');
    if(cap){ce.style.opacity=1; ce.querySelector('.w').textContent=cap.text;} else ce.style.opacity=0;
    $('#fade').style.opacity=Math.max(0,1-t/0.3,(t-(D-0.25))/0.25);
  };
  </script></body></html>`;
}

function titlePage(video, dur, outro = false) {
  const items = video.items;
  const flags = items.filter((i) => i.flag).slice(0, 12).map((i) => flagHtml(i.flag, 54)).join("");
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${BASE_CSS}
  body{background:radial-gradient(1200px 800px at 50% 45%, #2a2f5a 0%, #0d1024 60%, #05060f 100%)}
  #bg{left:0;top:0;width:1920px;height:1080px;opacity:.35}#bg svg{width:100%;height:100%}
  #logo{left:0;width:1920px;top:250px;text-align:center}
  #t{left:160px;width:1600px;top:${outro ? 380 : 400}px;text-align:center;color:#fff;font-weight:800;font-size:${outro ? 78 : 104}px;line-height:1.1;letter-spacing:-1px;text-shadow:0 8px 40px rgba(0,0,0,.6)}
  #p{left:0;width:1920px;top:${outro ? 600 : 650}px;text-align:center;color:#ffcf5c;font-weight:800;font-size:52px;letter-spacing:6px;text-transform:uppercase}
  #flags{left:0;width:1920px;top:800px;display:flex;justify-content:center;gap:22px}
  #fade{left:0;top:0;width:1920px;height:1080px;background:#000}
  </style></head><body>
  <div id="bg" class="abs">${scene("abstract", "title")}</div>
  <div id="logo" class="abs">${logoSvg(110)}</div>
  <div id="t" class="abs">${outro ? "Which language should we cover next?" : esc(video.title)}</div>
  <div id="p" class="abs">${outro ? "Tell us in the comments 👇" : esc(video.part || "")}</div>
  <div id="flags" class="abs">${outro ? "" : flags}</div>
  <div id="fade" class="abs"></div>
  <script>const D=${dur}; const $=(s)=>document.querySelector(s); const e=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
  const fl=[...document.querySelectorAll('#flags .flag')];
  window.setT=(t)=>{ $('#t').style.transform='scale('+(0.9+0.1*e(t/0.8))+')'; $('#t').style.opacity=e(t/0.5);
    $('#p').style.opacity=e((t-0.5)/0.5); $('#logo').style.opacity=e((t-0.2)/0.5);
    fl.forEach((f,i)=>{const k=e((t-0.7-i*0.07)/0.4); f.style.opacity=k; f.style.transform='translateY('+(1-k)*40+'px)';});
    $('#fade').style.opacity=Math.max(0,1-t/0.4,(t-(D-0.4))/0.4); };</script></body></html>`;
}

export function logoSvg(h = 120, dark = false) {
  // speech bubble + wordmark
  const txt = dark ? "#16182b" : "#ffffff";
  return `<svg height="${h}" viewBox="0 0 640 140" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffcf5c"/><stop offset="1" stop-color="#ff6b5c"/></linearGradient></defs>
  <path d="M20 20 h110 a20 20 0 0 1 20 20 v56 a20 20 0 0 1 -20 20 h-58 l-30 24 v-24 h-22 a20 20 0 0 1 -20 -20 v-56 a20 20 0 0 1 20 -20z" fill="url(#lg)"/>
  <text x="75" y="88" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="50" fill="#16182b">LD</text>
  <text x="175" y="98" font-family="Montserrat" font-weight="800" font-size="78" fill="${txt}" letter-spacing="-1">Lingo<tspan fill="#ffcf5c">Dude</tspan></text></svg>`;
}

// ---------------- rendering ----------------
function segDuration(video, item) {
  return video.layout === "ranking" ? 11.0 : +(1.4 + 5.0 * item.cards.length + 1.2).toFixed(2);
}

async function renderClip(browser, html, dur, outFile, stills) {
  const pageFile = path.join(CACHE, "pages", path.basename(outFile).replace(/\.\w+$/, ".html"));
  fs.writeFileSync(pageFile, html);
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(fileUrl(pageFile));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  if (stills) {
    for (const t of stills) {
      await page.evaluate((t) => window.setT(t), t);
      await page.screenshot({ path: outFile.replace(/\.mp4$/, `_${t}s.png`) });
    }
    await page.close();
    return;
  }
  const n = Math.round(dur * FPS);
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", PREVIEW ? "veryfast" : "medium", "-crf", PREVIEW ? "26" : "17", "-pix_fmt", "yuv420p", "-r", String(FPS), outFile], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = 0; f < n; f++) {
    await page.evaluate((t) => window.setT(t), f / FPS);
    const buf = await page.screenshot({ type: "jpeg", quality: PREVIEW ? 80 : 95 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end();
  await new Promise((r, j) => ff.on("close", (c) => (c ? j(new Error("ffmpeg " + c)) : r())));
  await page.close();
}

function loadAudio(vkey) {
  const p = path.join(CACHE, "audio", vkey, "manifest.json");
  return fs.existsSync(p) ? JSON.parse(fs.readFileSync(p)) : {};
}

async function main() {
  const vkey = args.find((a) => !a.startsWith("--") && VIDEOS[a]);
  if (!vkey) throw new Error("usage: node render.mjs <" + Object.keys(VIDEOS).join("|") + ">");
  const video = VIDEOS[vkey];
  const manifest = loadAudio(vkey);
  const stills = opt("still", null);
  const itemsArg = opt("items", null);
  let sel = video.items.map((_, i) => i);
  if (itemsArg) { const [a, b] = String(itemsArg).split("-").map(Number); sel = sel.filter((i) => i >= a && i <= (b ?? a)); }
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--font-render-hinting=none", "--disable-lcd-text"] });
  const dir = path.join(CACHE, "clips", vkey);
  fs.mkdirSync(dir, { recursive: true });
  const jobs = [];
  const INTRO = 3.2, OUTRO = 4.0;
  if (!itemsArg) {
    jobs.push({ name: "intro", dur: INTRO, html: titlePage(video, INTRO) });
  }
  for (const i of sel) {
    const item = video.items[i], dur = segDuration(video, item), audio = manifest[item.name];
    if (!audio && !stills) { console.log(`  skipping ${item.name}: no recording`); continue; }
    const html = video.layout === "ranking" ? rankingPage(video, video.items, i, dur, audio) : storyPage(video, item, i, dur, audio);
    jobs.push({ name: String(i).padStart(2, "0"), dur, html, i });
  }
  if (!itemsArg) jobs.push({ name: "outro", dur: OUTRO, html: titlePage(video, OUTRO, true) });

  if (stills) {
    const ts = String(stills).split(",").map(Number);
    for (const j of jobs) await renderClip(browser, j.html, j.dur, path.join(OUT, `${vkey}_${j.name}.mp4`), ts);
    await browser.close();
    console.log("stills ->", OUT);
    return;
  }
  const workers = +opt("workers", 3);
  let next = 0;
  const t0 = Date.now();
  await Promise.all(Array.from({ length: workers }, async () => {
    while (next < jobs.length) {
      const j = jobs[next++];
      j.file = path.join(dir, `${j.name}.mp4`);
      const sig = path.join(dir, `${j.name}.sig`);
      const hash = String(j.html.length) + ":" + [...j.html].reduce((a, c) => (a * 33 + c.charCodeAt(0)) >>> 0, 5381) + ":" + FPS + PREVIEW;
      if (fs.existsSync(j.file) && fs.existsSync(sig) && fs.readFileSync(sig, "utf8") === hash) continue;
      await renderClip(browser, j.html, j.dur, j.file);
      fs.writeFileSync(sig, hash);
      console.log(`  clip ${j.name} (${j.dur}s) done, ${((Date.now() - t0) / 1000).toFixed(0)}s elapsed`);
    }
  }));
  await browser.close();

  // ---- assemble video
  const list = path.join(dir, "list.txt");
  fs.writeFileSync(list, jobs.map((j) => `file '${j.file}'`).join("\n"));
  const silent = path.join(dir, "video.mp4");
  execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", silent]);

  // ---- audio: language clips at their segment offsets
  let t = 0;
  const inputs = [], filters = [], mixes = [];
  const offsets = [];
  for (const j of jobs) { offsets.push(t); t += j.dur; }
  const total = t;
  // only real recordings found on Wikimedia Commons; no generated music. Silence under intro/outro.
  inputs.push("-f", "lavfi", "-t", total.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo");
  mixes.push("[0]");
  let nIn = 1;
  jobs.forEach((j, k) => {
    if (j.i === undefined || !manifest[video.items[j.i].name]) return;
    const wav = path.join(CACHE, "audio", vkey, video.items[j.i].name.replace(/[^\p{L}\p{N}_]+/gu, "_").replace(/^_+|_+$/g, "").toLowerCase() + ".wav");
    if (!fs.existsSync(wav)) return;
    inputs.push("-i", wav);
    const n = nIn++, ms = Math.round((offsets[k] + 0.25) * 1000);
    filters.push(`[${n}]atrim=0:${(j.dur - 0.4).toFixed(3)},afade=t=out:st=${(j.dur - 1.0).toFixed(3)}:d=0.6,adelay=${ms}|${ms}[a${n}]`);
    mixes.push(`[a${n}]`);
  });
  filters.push(`${mixes.join("")}amix=inputs=${mixes.length}:normalize=0,alimiter=limit=0.95[out]`);
  const mixed = path.join(dir, "audio.wav");
  execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs, "-filter_complex", filters.join(";"), "-map", "[out]", "-t", total.toFixed(3), mixed]);
  const final = path.join(OUT, `${vkey}${itemsArg ? "_part" : ""}.mp4`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", silent, "-i", mixed, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final]);
  console.log(`done: ${final} (${total.toFixed(1)}s) in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main().catch((e) => { console.error(e); process.exit(1); });
