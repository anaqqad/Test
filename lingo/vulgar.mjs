// "Ranking the World's Most Vulgar Languages": 10 -> 1 by the number of words tagged vulgar on Wiktionary (vulgar.json).
// Each language: Wojak, rank, the count filling a meter, one signature swear word with its literal meaning (spoken by a
// real Lingua Libre recording, python3 fetch_vulgar.py), then two fact cards.   node vulgar.mjs [--still t]
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, renderClip, logoSvg } from "./render.mjs";
import { scene } from "./art.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const SET = opt("set", "vulgar"); // vulgar (default) or polite
const OUT = path.join(HERE, "out"), A = path.join(HERE, "cache", "audio", SET), TMP = path.join(HERE, "cache", "clips", SET);
fs.mkdirSync(TMP, { recursive: true });
const D = JSON.parse(fs.readFileSync(path.join(HERE, SET + ".json")));
const ACC = D.accent || "#e8262b"; // flash and highlight colour
const MAN = JSON.parse(fs.readFileSync(path.join(A, "manifest.json")));
const nm = (p) => path.join(HERE, "node_modules", p);
const fileUrl = (p) => pathToFileURL(p).href;
const flag = (c) => fileUrl(nm("flag-icons/flags/4x3/" + c + ".svg"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const wj = (it) => { const v = MAN[it.key]?.voice === "female" ? [it.wojak + "_f", it.wojak] : [it.wojak]; for (const k of v) { const f = path.join(HERE, "wojaks", k + ".png"); if (fs.existsSync(f)) return fileUrl(f); } return null; };
const items = [...D.items].sort((a, b) => a.count - b.count); // 10 -> 1
const MAX = Math.max(...items.map((i) => i.count));
const SCRIPT_CSS = ["noto-sans-sc/700.css", "noto-sans-jp/700.css", "noto-sans-kr/700.css", "noto-sans-thai/700.css", "noto-sans-myanmar/700.css", "noto-sans-tamil/700.css"].map((f) => fs.existsSync(nm("@fontsource/" + f)) ? `<link rel="stylesheet" href="${fileUrl(nm("@fontsource/" + f))}">` : "").join("");

const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,"Noto Sans SC","Noto Sans JP","Noto Sans KR","Noto Sans Thai","Noto Sans Myanmar","Noto Sans Tamil","DejaVu Sans",sans-serif;background:#101522;color:#fff}
.a{position:absolute}.f{opacity:0}
#bg{left:-40px;top:-40px;width:2000px;height:1160px}#bg svg{width:100%;height:100%}
#bar{left:0;top:0;width:1920px;height:124px;background:linear-gradient(#fff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;gap:28px;color:#18181d;font-weight:800;font-size:64px}
#bar img{height:60px;border-radius:7px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.brand{left:22px;top:26px}
.rank{right:40px;top:28px;font-weight:800;font-size:54px;color:#e8262b}
.who{left:40px;bottom:0;width:720px;height:820px;display:flex;align-items:flex-end;justify-content:center;transform-origin:50% 100%}
.who img{max-height:800px;max-width:720px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.4))}
#panel{left:800px;top:160px;width:1060px;display:flex;flex-direction:column;gap:20px}
#meter{background:rgba(15,18,28,.9);border-radius:22px;padding:20px 30px;box-shadow:0 12px 30px rgba(0,0,0,.35)}
#meter .t{font-weight:800;font-size:26px;letter-spacing:2px;color:#ffcf5c;text-transform:uppercase}
#meter .n{font-weight:800;font-size:92px;line-height:1.05}
#meter .n small{font-size:30px;color:#aab;font-weight:700;margin-left:14px;letter-spacing:1px}
#meter .bar{height:26px;border-radius:13px;background:rgba(255,255,255,.12);margin-top:12px;overflow:hidden}
#meter .bar i{display:block;height:100%;width:0;border-radius:13px;background:linear-gradient(90deg,#ffcf5c,#e8262b)}
#word{transform-origin:50% 50%;background:rgba(255,255,255,.96);color:#1d1d24;border-radius:22px;padding:22px 32px;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:12px solid #e8262b}
#word .hd{font-size:22px;font-weight:800;letter-spacing:2px;color:#8a8f9c;text-transform:uppercase}
#word .w{font-weight:800;font-size:84px;line-height:1.1;color:#e8262b}
#word .w.tall{line-height:1.45;padding-top:8px}
#word .rom{font-weight:700;font-size:30px;color:#8a8f9c;margin-top:2px}
#word .lit{font-weight:700;font-size:34px;color:#1d1d24;margin-top:4px}#word .lit b{color:#8a8f9c;font-weight:800;font-size:22px;letter-spacing:2px;margin-right:10px}
.card{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:20px;padding:20px 28px;font-weight:600;font-size:33px;line-height:1.32;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:9px solid #e8262b}
.norec{font-size:22px;color:#8a8f9c;font-weight:700;margin-top:6px}
`;
const SCRIPT = `<script>
const S=window.__S, ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
window.setT=function(t){
  document.querySelectorAll('[data-in]').forEach(e=>{const i=+e.dataset.in,o=+(e.dataset.out||1e9);const v=ease((t-i)/0.4)*ease((o-t)/0.35);e.style.opacity=v;e.style.transform='translateY('+(1-v)*18+'px)';});
  const bar=document.getElementById('bar'); if(bar) bar.style.transform='translateY('+(-(1-ease(t/0.45))*140)+'px)';
  const on=(S.say||[]).some(s=>t>=s.t-0.05&&t<=s.t+s.d+0.2);
  const wd=document.getElementById('word'); if(wd){const k=on?1.06:1;wd.style.transform='scale('+k+')';wd.style.boxShadow=on?'0 0 0 8px '+S.acc+'73, 0 12px 30px rgba(0,0,0,.35)':'';}
  const fl=document.getElementById('flash'); if(fl) fl.style.opacity=on?0.22:0;
  const w=document.getElementById('who'); if(w){const k=on?1+0.05*Math.abs(Math.sin(t*10)):1;w.style.transform='scale('+k.toFixed(3)+') translateY('+((1-ease(t/0.6))*140).toFixed(1)+'px)';w.style.filter=on?'brightness(1.1)':'brightness(.95)';}
  if(S.count!==undefined){const k=ease((t-0.8)/1.6);const n=document.getElementById('mn');if(n)n.firstChild.textContent=Math.round(S.count*k).toLocaleString('en-US');const b=document.getElementById('mb');if(b)b.style.width=(100*S.count*k/S.max)+'%';}
};
</script>`;
const page = (body, S) => `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}${SCRIPT_CSS}<style>${CSS}</style></head><body>${body}<script>window.__S=${JSON.stringify(S)}</script>${SCRIPT}</body></html>`;
const brand = (sub) => `<div class="a brand">${logoSvg(70, true)}</div>${sub ? `<div class="a rank">${esc(sub)}</div>` : ""}`;
const scenes = [];
const add = (name, dur, html, S = {}, audio = []) => scenes.push({ name, dur, html: page(html, S), audio });

add("intro", 5, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f">${logoSvg(110)}</div>
    <div data-in="0.4" class="f" style="margin-top:40px;font-weight:800;font-size:92px;line-height:1.1;text-shadow:0 8px 40px rgba(0,0,0,.6);width:1500px">${esc(D.title)}</div>
    <div data-in="1.2" class="f" style="margin-top:34px;font-weight:800;font-size:36px;color:#ffcf5c;letter-spacing:4px">${esc(D.subtitle || "BY THE NUMBER OF VULGAR WORDS IN THE DICTIONARY")}</div>
    <div data-in="1.8" class="f" style="margin-top:50px;display:flex;gap:18px">${items.map((i) => `<img src="${flag(i.flag)}" style="height:52px;border-radius:6px">`).join("")}</div></div>`);

for (const [idx, it] of items.entries()) {
  const m = MAN[it.key], rank = items.length - idx;
  const say = m ? [{ t: 4.2, d: m.d }, { t: 4.2 + m.d + 0.9, d: m.d }] : [];
  const wordAt = 3.6, cardsAt = m ? say[1].t + m.d + 1.2 : 6.5, dur = +(cardsAt + 8.5).toFixed(2);
  const html = `<div class="a" id="bg">${scene(it.scene, it.key)}</div>
    <div class="a" id="flash" style="left:0;top:0;width:1920px;height:1080px;background:${ACC};opacity:0;pointer-events:none"></div>
    <div class="a who" id="who">${wj(it) ? `<img src="${wj(it)}">` : ""}</div>
    <div id="panel" class="a">
      <div data-in="0.3" class="f" id="meter"><div class="t">${esc(D.meter || "Vulgar words in the dictionary")}</div><div class="n" id="mn">0<small>${esc(D.meter_unit || "WORDS TAGGED VULGAR")}</small></div><div class="bar"><i id="mb"></i></div></div>
      <div data-in="${wordAt}" class="f" id="word"><div class="hd">${esc(D.word_label || "Signature swear word")}</div><div class="w${/[\u1000-\u109F\u0B80-\u0BFF\u0E00-\u0E7F]/.test(it.word) ? " tall" : ""}">${esc(it.word)}</div>${it.roman ? `<div class="rom">${esc(it.roman)}</div>` : ""}<div class="lit"><b>${esc(D.lit_label || "LITERALLY")}</b>${esc(it.lit)}</div>${m?.ai ? `<div class="norec">AI VOICE (no native recording exists yet)</div>` : ""}</div>
      ${it.cards.map((c, i) => `<div data-in="${(cardsAt + i * 3.6).toFixed(2)}" class="f card">${esc(c)}</div>`).join("")}</div>
    <div id="bar" class="a"><img src="${flag(it.flag)}">${esc(it.name)}</div>
    ${brand(`#${rank}`)}`;
  add(it.key, dur, html, { say, count: it.count, max: MAX, acc: ACC }, m ? say.map((s) => ({ file: path.join(A, it.key + ".wav"), at: s.t })) : []);
}

add("outro", 7, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f" style="font-weight:800;font-size:72px;line-height:1.15;width:1500px">${esc(D.outro || "Which language swears best?")}</div>
    <div data-in="0.8" class="f" style="margin-top:24px;font-weight:800;font-size:44px;color:#ffcf5c;letter-spacing:4px">TELL US IN THE COMMENTS 👇</div>
    <div data-in="1.4" class="f" style="margin-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:10px 80px;font-weight:700;font-size:32px;text-align:left">${[...items].reverse().map((it, i) => `<div>#${i + 1} ${esc(it.name)} <span style="color:#ffcf5c">${it.count.toLocaleString("en-US")}</span></div>`).join("")}</div></div>`);

const stills = opt("still", null);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--font-render-hinting=none"] });
const clips = [];
for (const [i, s] of scenes.entries()) {
  const f = path.join(TMP, `${String(i).padStart(2, "0")}_${s.name}.mp4`);
  if (opt("mix", false) && fs.existsSync(f)) { /* --mix: audio only, the clips are reused */ }
  else if (stills) await renderClip(browser, s.html, s.dur, f, String(stills).split(",").map(Number));
  else { await renderClip(browser, s.html, s.dur, f); console.log(`  ${s.name} (${s.dur}s)`); }
  clips.push(f);
}
await browser.close();
if (stills) { console.log("stills -> " + TMP); process.exit(0); }
let t = 0; const ins = [], filt = [];
for (const s of scenes) {
  for (const a of s.audio) { const n = ins.length / 2 + 1; ins.push("-i", a.file); const ms = Math.round((t + a.at) * 1000); filt.push(`[${n}]adelay=${ms}|${ms}[a${n}]`); }
  t += s.dur;
}
const n = ins.length / 2, T = t.toFixed(2);
const list = path.join(TMP, "list.txt");
fs.writeFileSync(list, clips.map((c) => `file '${c}'`).join("\n"));
const outFile = path.join(OUT, SET + ".mp4");
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, ...ins, "-filter_complex",
  filt.join(";") + `;anullsrc=r=48000:cl=stereo,atrim=0:${T}[base];[base]` + [...Array(n).keys()].map((i) => `[a${i + 1}]`).join("") + `amix=inputs=${n + 1}:normalize=0,apad,atrim=0:${T},aresample=48000[aout]`,
  "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outFile], { stdio: "inherit" });
if (r.status) throw new Error("ffmpeg failed");
let t0 = 0;
fs.writeFileSync(path.join(OUT, SET + "_timeline.json"), JSON.stringify(scenes.map((s) => { const e = { name: s.name, start: +t0.toFixed(2), dur: s.dur }; t0 += s.dur; return e; }), null, 1));
console.log(`done: ${outFile} (${T}s)`);
