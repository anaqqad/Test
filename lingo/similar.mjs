// "Languages That Are Basically the Same be like": a ranking of language pairs. Each pair: two Wojaks, the same
// test words spoken in both languages (real Lingua Libre recordings), a live "words alike" meter, then the facts.
// Data: similar_pairs.json; audio: python3 fetch_pairs.py -> cache/audio/similar/.   node similar.mjs [--still t] [--preview]
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, renderClip, logoSvg } from "./render.mjs";
import { scene } from "./art.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out"), A = path.join(HERE, "cache", "audio", "similar"), TMP = path.join(HERE, "cache", "clips", "similar");
fs.mkdirSync(TMP, { recursive: true });
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const PAIRS = JSON.parse(fs.readFileSync(path.join(HERE, "similar_pairs.json")));
const MAN = JSON.parse(fs.readFileSync(path.join(A, "manifest.json")));
const nm = (p) => path.join(HERE, "node_modules", p);
const fileUrl = (p) => pathToFileURL(p).href;
const flag = (c) => fileUrl(nm("flag-icons/flags/4x3/" + c + ".svg"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const wj = (k) => { const f = path.join(HERE, "wojaks", k + ".png"); return fs.existsSync(f) ? fileUrl(f) : null; };
const TITLE = "Languages That Are Basically the Same be like";

// ranking order: by measured share of alike words (ascending), the most similar pair last
const order = Object.keys(PAIRS).filter((k) => MAN[k] && MAN[k].words.length >= 5)
  .map((k) => ({ k, n: MAN[k].words.length, s: MAN[k].words.filter((w) => w.same).length }))
  .sort((x, y) => x.s / x.n - y.s / y.n || x.s - y.s);

const SCRIPT_CSS = ["noto-sans-thai/700.css", "noto-sans-lao/700.css", "noto-naskh-arabic/700.css", "noto-sans-devanagari/700.css"].map((f) => `<link rel="stylesheet" href="${fileUrl(nm("@fontsource/" + f))}">`).join("");
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,"Noto Sans Thai","Noto Sans Lao","Noto Naskh Arabic","Noto Sans Devanagari","DejaVu Sans",sans-serif;background:#101522;color:#fff}
.a{position:absolute}.f{opacity:0}
#bg{left:-40px;top:-40px;width:2000px;height:1160px}#bg svg{width:100%;height:100%}
#bar{left:0;top:0;width:1920px;height:124px;background:linear-gradient(#fff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;gap:28px;color:#18181d;font-weight:800;font-size:64px}
#bar img{height:60px;border-radius:7px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
#bar .vs{font-size:34px;color:#e8262b;letter-spacing:2px}
.brand{left:22px;top:26px}
.rank{right:40px;top:40px;font-weight:800;font-size:30px;color:#18181d}
.who{bottom:0;width:560px;height:760px;display:flex;align-items:flex-end;justify-content:center;transform-origin:50% 100%}
.who img{max-height:720px;max-width:560px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.4))}
#panel{left:600px;top:150px;width:720px}
#meter{background:rgba(15,18,28,.88);border-radius:22px;padding:18px 26px;box-shadow:0 12px 30px rgba(0,0,0,.35)}
#meter .t{font-weight:800;font-size:26px;letter-spacing:2px;color:#ffcf5c;text-transform:uppercase}
#meter .n{font-weight:800;font-size:54px;line-height:1.1}
#meter .bar{height:20px;border-radius:10px;background:rgba(255,255,255,.12);margin-top:10px;overflow:hidden}
#meter .bar i{display:block;height:100%;width:0;border-radius:10px;background:linear-gradient(90deg,#4fc3ff,#34c759)}
#rows{margin-top:16px;display:flex;flex-direction:column;gap:6px}
.row{display:grid;grid-template-columns:1fr 54px 1fr;align-items:center;background:rgba(255,255,255,.94);color:#1d1d24;border-radius:14px;padding:6px 18px;font-weight:700;font-size:30px;opacity:0;transform:translateY(16px)}
.row .wa{text-align:right}.row .wb{text-align:left}
.row .m{text-align:center;font-size:30px}
.row.on .wa,.row.on .wb{color:#1d1d24}.row .wa,.row .wb{color:#8a8f9c}
.row.on.sa .wa{color:#e8262b}.row.on.sb .wb{color:#1d6fa5}
.card{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:20px;padding:20px 28px;font-weight:600;font-size:31px;line-height:1.32;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:9px solid #e8262b}
.card b{color:#e8262b}
#verdict{background:#1f7a4d;border-radius:20px;padding:18px 26px;font-weight:800;font-size:40px;line-height:1.2;box-shadow:0 12px 30px rgba(0,0,0,.35)}
#big{left:600px;top:150px;width:720px;display:none}
`;
const page = (body, S) => `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}${SCRIPT_CSS}<style>${CSS}</style></head><body>${body}<script>window.__S=${JSON.stringify(S)}</script>${SCRIPT}</body></html>`;
const SCRIPT = `<script>
const S=window.__S, ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
window.setT=function(t){
  document.querySelectorAll('[data-in]').forEach(e=>{const i=+e.dataset.in,o=+(e.dataset.out||1e9);const v=ease((t-i)/0.4)*ease((o-t)/0.35);e.style.opacity=v;e.style.transform='translateY('+(1-v)*18+'px)';});
  const bar=document.getElementById('bar'); if(bar) bar.style.transform='translateY('+(-(1-ease(t/0.45))*140)+'px)';
  if(!S.caps) return;
  const cur=S.caps.find(c=>t>=c.t-0.05&&t<=c.t+c.d+0.25);
  ['a','b'].forEach(side=>{const w=document.getElementById('who_'+side);if(!w)return;const on=cur&&cur.side===side;const k=on?1+0.04*Math.abs(Math.sin(t*9)):1;w.style.transform=(side==='b'?'scaleX(-1) ':'')+'scale('+k.toFixed(3)+') translateY('+((1-ease(t/0.6))*120).toFixed(1)+'px)';w.style.filter=on?'brightness(1.08)':'brightness(.92)';});
  S.rows.forEach((r,i)=>{const el=document.getElementById('row'+i);if(!el)return;const v=ease((t-r.t+0.2)/0.35)*(S.hideAt?ease((S.hideAt-t)/0.4):1);el.style.opacity=v;el.style.transform='translateY('+(1-v)*16+'px)';
    el.classList.toggle('on',t>=r.t);el.classList.toggle('sa',!!(cur&&cur.side==='a'&&cur.i===i));el.classList.toggle('sb',!!(cur&&cur.side==='b'&&cur.i===i));
    const m=el.querySelector('.m'); m.textContent=t>=r.end+0.1?(r.same?'✅':'❌'):(t>=r.t?'…':'');});
  const done=S.rows.filter(r=>t>=r.end+0.1), alike=done.filter(r=>r.same).length;
  const n=document.getElementById('mn'); if(n){n.textContent=alike+' / '+S.rows.length; document.getElementById('mb').style.width=(100*alike/S.rows.length)+'%';}
  const me=document.getElementById('meter'); if(me&&S.hideAt){me.style.opacity=ease((S.hideAt-t)/0.4);}
};
</script>`;
const brand = (sub) => `<div class="a brand">${logoSvg(70, true)}</div>${sub ? `<div class="a rank">${esc(sub)}</div>` : ""}`;

const scenes = [];
const add = (name, dur, html, S = {}, audio = null) => scenes.push({ name, dur, html: page(html, S), audio });

// intro
add("intro", 4.5, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f">${logoSvg(110)}</div>
    <div data-in="0.4" class="f" style="margin-top:40px;font-weight:800;font-size:92px;line-height:1.1;text-shadow:0 8px 40px rgba(0,0,0,.6);width:1500px">${esc(TITLE)}</div>
    <div data-in="1.2" class="f" style="margin-top:34px;font-weight:800;font-size:40px;color:#ffcf5c;letter-spacing:4px">RANKED BY OUR 10-WORD TEST</div>
    <div data-in="1.8" class="f" style="margin-top:50px;display:flex;gap:18px">${order.map((o) => `<img src="${flag(PAIRS[o.k].fa)}" style="height:52px;border-radius:6px"><img src="${flag(PAIRS[o.k].fb)}" style="height:52px;border-radius:6px;margin-right:16px">`).join("")}</div></div>`);

for (const [idx, o] of order.entries()) {
  const p = PAIRS[o.k], m = MAN[o.k];
  const rows = []; let k = -1;
  for (const c of m.captions) { if (c.side === "a") { k++; rows.push({ t: c.t, same: m.words[k].same, a: m.words[k].a, b: m.words[k].b }); } rows[k].end = c.t + c.d; }
  const end = m.len, dur = +(end + 8.0).toFixed(2);
  const verdict = `${o.s} of ${o.n} words alike`;
  const html = `<div class="a" id="bg">${scene(p.scene, o.k)}</div>
    <div class="a who" id="who_a" style="left:20px">${wj("s_" + p.a) ? `<img src="${wj("s_" + p.a)}">` : ""}</div>
    <div class="a who" id="who_b" style="right:20px">${wj("s_" + p.b) ? `<img src="${wj("s_" + p.b)}">` : ""}</div>
    <div class="a" style="left:60px;top:150px;display:flex;align-items:center;gap:12px;background:rgba(15,18,28,.85);padding:8px 16px;border-radius:14px;font-weight:800;font-size:28px"><img src="${flag(p.fa)}" style="height:34px;border-radius:5px">${esc(p.na)}</div>
    <div class="a" style="right:60px;top:150px;display:flex;align-items:center;gap:12px;background:rgba(15,18,28,.85);padding:8px 16px;border-radius:14px;font-weight:800;font-size:28px">${esc(p.nb)}<img src="${flag(p.fb)}" style="height:34px;border-radius:5px"></div>
    <div id="panel" class="a">
      <div id="meter"><div class="t">Words that sound alike</div><div class="n"><span id="mn">0 / ${rows.length}</span></div><div class="bar"><i id="mb"></i></div></div>
      <div id="rows">${rows.map((r, i) => `<div class="row" id="row${i}"><span class="wa">${esc(r.a)}</span><span class="m"></span><span class="wb">${esc(r.b)}</span></div>`).join("")}</div></div>
    <div class="a" style="left:600px;top:170px;width:720px;display:flex;flex-direction:column;gap:22px">
      <div data-in="${(end + 0.4).toFixed(2)}" class="f" id="verdict">✅ ${esc(verdict)}</div>
      ${p.cards.map((c, i) => `<div data-in="${(end + 1.2 + i * 3.0).toFixed(2)}" class="f card">${esc(c)}</div>`).join("")}</div>
    <div id="bar" class="a"><img src="${flag(p.fa)}">${esc(p.na)}<span class="vs">VS</span>${esc(p.nb)}<img src="${flag(p.fb)}"></div>
    ${brand(`#${order.length - idx} of ${order.length}`)}`;
  add(o.k, dur, html, { caps: m.captions, rows, hideAt: end + 0.3 }, path.join(A, o.k + ".wav"));
}

// outro
add("outro", 6, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f" style="font-weight:800;font-size:72px;line-height:1.15;width:1500px">Which pair did we miss?</div>
    <div data-in="0.8" class="f" style="margin-top:30px;font-weight:800;font-size:44px;color:#ffcf5c;letter-spacing:4px">TELL US IN THE COMMENTS 👇</div>
    <div data-in="1.4" class="f" style="margin-top:50px;display:flex;flex-direction:column;gap:14px;font-weight:700;font-size:34px">${[...order].reverse().map((o, i) => `<div>#${i + 1} ${esc(PAIRS[o.k].na)} – ${esc(PAIRS[o.k].nb)} <span style="color:#34c759">${o.s}/${o.n}</span></div>`).join("")}</div></div>`);

// ---------- render ----------
const stills = opt("still", null);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--font-render-hinting=none"] });
const clips = [];
for (const [i, s] of scenes.entries()) {
  const f = path.join(TMP, `${String(i).padStart(2, "0")}_${s.name}.mp4`);
  if (stills) await renderClip(browser, s.html, s.dur, f, String(stills).split(",").map(Number));
  else { await renderClip(browser, s.html, s.dur, f); console.log(`  ${s.name} (${s.dur}s)`); }
  clips.push(f);
}
await browser.close();
if (stills) { console.log("stills -> " + TMP); process.exit(0); }
let t = 0; const ins = [], filt = [];
for (const s of scenes) {
  if (s.audio) { const n = ins.length / 2 + 1; ins.push("-i", s.audio); filt.push(`[${n}]adelay=${Math.round(t * 1000)}|${Math.round(t * 1000)}[a${n}]`); }
  t += s.dur;
}
const n = ins.length / 2, T = t.toFixed(2);
const list = path.join(TMP, "list.txt");
fs.writeFileSync(list, clips.map((c) => `file '${c}'`).join("\n"));
const outFile = path.join(OUT, "similar.mp4");
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, ...ins, "-filter_complex",
  filt.join(";") + `;anullsrc=r=48000:cl=stereo,atrim=0:${T}[base];[base]` + [...Array(n).keys()].map((i) => `[a${i + 1}]`).join("") + `amix=inputs=${n + 1}:normalize=0,apad,atrim=0:${T},aresample=48000[aout]`,
  "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outFile], { stdio: "inherit" });
if (r.status) throw new Error("ffmpeg failed");
let t0 = 0;
fs.writeFileSync(path.join(OUT, "similar_timeline.json"), JSON.stringify(scenes.map((s) => { const e = { name: s.name, start: +t0.toFixed(2), dur: s.dur }; t0 += s.dur; return e; }), null, 1));
console.log(`done: ${outFile} (${T}s)`);
