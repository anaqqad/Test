// "Words That Don't Exist in English be like": two Wojaks per word. The native speaker says the word (real Commons
// recording), the English Wojak translates it with as many words as it takes (Piper AI voice, labelled), the counter
// shows how many English words were needed; ranked 10 -> 1 by that count. Data: untrans.json; audio: python3
// fetch_untrans.py -> cache/audio/untrans/.   node untrans.mjs [--still t] [--mix]
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, renderClip, logoSvg } from "./render.mjs";
import { scene } from "./art.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out"), A = path.join(HERE, "cache", "audio", "untrans"), TMP = path.join(HERE, "cache", "clips", "untrans");
fs.mkdirSync(TMP, { recursive: true });
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const D = JSON.parse(fs.readFileSync(path.join(HERE, "untrans.json")));
const MAN = JSON.parse(fs.readFileSync(path.join(A, "manifest.json")));
const nm = (p) => path.join(HERE, "node_modules", p);
const fileUrl = (p) => pathToFileURL(p).href;
const flag = (c) => fileUrl(nm("flag-icons/flags/4x3/" + c + ".svg"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const wj = (keys) => { for (const k of keys) { const f = path.join(HERE, "wojaks", k + ".png"); if (fs.existsSync(f)) return fileUrl(f); } return null; };
const items = D.items.filter((i) => MAN[i.key]).map((i) => ({ ...i, m: MAN[i.key] })).sort((a, b) => a.m.words - b.m.words || a.m.de - b.m.de); // 10 -> 1
const SCRIPT_CSS = ["noto-sans-jp/700.css", "noto-sans-kr/700.css", "noto-sans-devanagari/700.css"].map((f) => fs.existsSync(nm("@fontsource/" + f)) ? `<link rel="stylesheet" href="${fileUrl(nm("@fontsource/" + f))}">` : "").join("");

const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,"Noto Sans JP","Noto Sans KR","Noto Sans Devanagari","DejaVu Sans",sans-serif;background:#101522;color:#fff}
.a{position:absolute}.f{opacity:0}
#bg{left:-40px;top:-40px;width:2000px;height:1160px}#bg svg{width:100%;height:100%}
#bar{left:0;top:0;width:1920px;height:124px;background:linear-gradient(#fff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;gap:28px;color:#18181d;font-weight:800;font-size:64px}
#bar img{height:60px;border-radius:7px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
#bar .vs{font-size:34px;color:#e8262b;letter-spacing:2px}
.brand{left:22px;top:26px}
.rank{right:40px;top:28px;font-weight:800;font-size:54px;color:#e8262b}
.who{bottom:0;width:540px;height:760px;display:flex;align-items:flex-end;justify-content:center;transform-origin:50% 100%}
.who img{max-height:720px;max-width:540px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.4))}
.lab{top:150px;display:flex;align-items:center;gap:12px;background:rgba(15,18,28,.85);padding:8px 16px;border-radius:14px;font-weight:800;font-size:28px}
.lab img{height:34px;border-radius:5px}
.ai{left:50%;transform:translateX(-50%);bottom:18px;background:rgba(15,18,28,.85);padding:6px 18px;border-radius:12px;font-weight:800;font-size:22px;letter-spacing:3px;color:#ffcf5c}
#panel{left:540px;top:150px;width:840px;display:flex;flex-direction:column;gap:16px}
.say{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:22px;padding:18px 26px;box-shadow:0 12px 30px rgba(0,0,0,.35);opacity:0}
.say.sa{border-left:12px solid #e8262b}.say.sb{border-right:12px solid #1d6fa5}
.say .hd{font-size:20px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#8a8f9c;display:flex;align-items:center;gap:10px;margin-bottom:4px}.say .hd img{height:24px;border-radius:4px}
.say .w{font-weight:800;font-size:78px;line-height:1.1;color:#e8262b}
.say .rom{font-weight:700;font-size:28px;color:#8a8f9c;margin-top:2px}
.say .lit{font-weight:700;font-size:28px;color:#1d1d24;margin-top:8px}.say .lit b{color:#8a8f9c;font-size:20px;letter-spacing:2px;margin-right:10px}
.say .tr{font-weight:700;font-size:36px;line-height:1.3}.say .tr .c{color:#b9bcc6}.say .tr .c.on{color:#1d1d24}
#count{background:rgba(15,18,28,.92);border-radius:22px;padding:16px 28px;box-shadow:0 12px 30px rgba(0,0,0,.35);display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:30px;letter-spacing:2px;color:#ffcf5c}
#count b{font-size:72px;color:#fff;line-height:1}
.card{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:20px;padding:18px 26px;font-weight:600;font-size:31px;line-height:1.3;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:9px solid #e8262b}
`;
const SCRIPT = `<script>
const S=window.__S, ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
window.setT=function(t){
  document.querySelectorAll('[data-in]').forEach(e=>{const i=+e.dataset.in,o=+(e.dataset.out||1e9);const v=ease((t-i)/0.4)*ease((o-t)/0.35);e.style.opacity=v;e.style.transform='translateY('+(1-v)*18+'px)';});
  const bar=document.getElementById('bar'); if(bar) bar.style.transform='translateY('+(-(1-ease(t/0.45))*140)+'px)';
  const cur=(S.caps||[]).find(c=>t>=c.t-0.05&&t<=c.t+c.d+0.2);
  ['a','b'].forEach(side=>{const w=document.getElementById('who_'+side);if(!w)return;const on=cur&&cur.side===side;const k=on?1+0.04*Math.abs(Math.sin(t*9)):1;w.style.transform=(side==='b'?'scaleX(-1) ':'')+'scale('+k.toFixed(3)+') translateY('+((1-ease(t/0.6))*120).toFixed(1)+'px)';w.style.filter=on?'brightness(1.08)':'brightness(.92)';});
  const sa=document.getElementById('say_a'); if(sa){const v=ease((t-S.wordAt)/0.4);sa.style.opacity=v;sa.style.transform='translateY('+(1-v)*16+'px) scale('+(cur&&cur.side==='a'?1.03:1)+')';}
  const sb=document.getElementById('say_b'); if(sb){const v=ease((t-S.enAt+0.3)/0.4);sb.style.opacity=v;sb.style.transform='translateY('+(1-v)*16+'px)';
    const ws=sb.querySelectorAll('.c'),frac=Math.min(1,Math.max(0,(t-S.enAt)/(S.enD*0.95)));ws.forEach((w,i)=>w.classList.toggle('on',frac*ws.length>=i+0.5));}
  const c=document.getElementById('cn'); if(c){const k=ease((t-S.countAt)/0.8);c.textContent=Math.round(S.words*k);}
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
    <div data-in="1.2" class="f" style="margin-top:34px;font-weight:800;font-size:36px;color:#ffcf5c;letter-spacing:4px">RANKED BY HOW MANY ENGLISH WORDS IT TAKES</div>
    <div data-in="1.8" class="f" style="margin-top:50px;display:flex;gap:18px">${items.map((i) => `<img src="${flag(i.flag)}" style="height:52px;border-radius:6px">`).join("")}</div></div>`);

for (const [idx, it] of items.entries()) {
  const m = it.m, rank = items.length - idx;
  const wordAt = 1.0, say = [{ side: "a", t: 1.6, d: m.dw }, { side: "a", t: 1.6 + m.dw + 0.8, d: m.dw }];
  const enAt = say[1].t + m.dw + 1.4; say.push({ side: "b", t: enAt, d: m.de });
  const countAt = enAt + m.de + 0.6, factAt = countAt + 2.2, dur = +(factAt + 6.5).toFixed(2);
  const tr = it.translation.split(/\s+/).map((w) => `<span class="c">${esc(w)}</span>`).join(" ");
  const html = `<div class="a" id="bg">${scene(it.scene, it.key)}</div>
    <div class="a who" id="who_a" style="left:10px">${wj([(it.voice || m.voice) === "female" ? it.wojak + "_f" : "", it.wojak]) ? `<img src="${wj([(it.voice || m.voice) === "female" ? it.wojak + "_f" : "", it.wojak])}">` : ""}</div>
    <div class="a who" id="who_b" style="right:10px">${wj([D.english_wojak]) ? `<img src="${wj([D.english_wojak])}">` : ""}</div>
    <div class="a lab" style="left:40px"><img src="${flag(it.flag)}">${esc(it.name)}</div>
    <div class="a lab" style="right:40px">English<img src="${flag("gb")}"></div>
    <div class="a ai">ENGLISH: AI VOICE</div>
    <div id="panel" class="a">
      <div class="say sa" id="say_a"><div class="hd"><img src="${flag(it.flag)}">${esc(it.name)}</div><div class="w">${esc(it.word)}</div>${it.roman ? `<div class="rom">${esc(it.roman)}</div>` : ""}</div>
      <div class="say sb" id="say_b"><div class="hd"><img src="${flag("gb")}">English, as many words as it takes</div><div class="tr">${tr}</div></div>
      <div data-in="${countAt.toFixed(2)}" class="f" id="count"><span>ENGLISH WORDS NEEDED</span><b id="cn">0</b></div>
      <div data-in="${factAt.toFixed(2)}" class="f card">${esc(it.fact)}</div></div>
    <div id="bar" class="a"><img src="${flag(it.flag)}">${esc(it.word)}</div>
    ${brand(`#${rank}`)}`;
  add(it.key, dur, html, { caps: say, wordAt, enAt, enD: m.de, countAt, words: m.words },
    [{ file: path.join(A, it.key + "_w.wav"), at: say[0].t }, { file: path.join(A, it.key + "_w.wav"), at: say[1].t }, { file: path.join(A, it.key + "_en.wav"), at: enAt }]);
}

add("outro", 7, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f" style="font-weight:800;font-size:72px;line-height:1.15;width:1500px">Which word did we miss?</div>
    <div data-in="0.8" class="f" style="margin-top:24px;font-weight:800;font-size:44px;color:#ffcf5c;letter-spacing:4px">TELL US IN THE COMMENTS 👇</div>
    <div data-in="1.4" class="f" style="margin-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:10px 80px;font-weight:700;font-size:32px;text-align:left">${[...items].reverse().map((it, i) => `<div>#${i + 1} ${esc(it.word)} (${esc(it.name)}) <span style="color:#ffcf5c">${it.m.words} words</span></div>`).join("")}</div></div>`);

const stills = opt("still", null);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--font-render-hinting=none"] });
const clips = [];
for (const [i, s] of scenes.entries()) {
  const f = path.join(TMP, `${String(i).padStart(2, "0")}_${s.name}.mp4`);
  if (opt("mix", false) && fs.existsSync(f)) { }
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
const outFile = path.join(OUT, "untrans.mp4");
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, ...ins, "-filter_complex",
  filt.join(";") + `;anullsrc=r=48000:cl=stereo,atrim=0:${T}[base];[base]` + [...Array(n).keys()].map((i) => `[a${i + 1}]`).join("") + `amix=inputs=${n + 1}:normalize=0,apad,atrim=0:${T},aresample=48000[aout]`,
  "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outFile], { stdio: "inherit" });
if (r.status) throw new Error("ffmpeg failed");
let t0 = 0;
fs.writeFileSync(path.join(OUT, "untrans_timeline.json"), JSON.stringify(scenes.map((s) => { const e = { name: s.name, start: +t0.toFixed(2), dur: s.dur }; t0 += s.dur; return e; }), null, 1));
console.log(`done: ${outFile} (${T}s)`);
