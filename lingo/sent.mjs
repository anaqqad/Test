// "Languages That Are Basically the Same be like" (sentence version): two Wojaks, the first reads one sentence, the
// second reads the same sentence in its language (Piper AI voices, labelled), then the words with no twin turn red
// and the scorecard (words, sound, grammar -> similarity %) comes up. Data: sent_pairs.json, scores: sent_score.py,
// audio: python3 sent_audio.py -> cache/audio/sent/.   node sent.mjs [--still t]
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, renderClip, logoSvg } from "./render.mjs";
import { scene } from "./art.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out"), A = path.join(HERE, "cache", "audio", "sent"), TMP = path.join(HERE, "cache", "clips", "sent");
fs.mkdirSync(TMP, { recursive: true });
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const D = JSON.parse(fs.readFileSync(path.join(HERE, "sent_pairs.json")));
const PAIRS = D.pairs;
const MAN = JSON.parse(fs.readFileSync(path.join(A, "manifest.json")));
const nm = (p) => path.join(HERE, "node_modules", p);
const fileUrl = (p) => pathToFileURL(p).href;
const flag = (c) => fileUrl(nm("flag-icons/flags/4x3/" + c + ".svg"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const wj = (code) => { for (const k of [D.wojaks[code], "s_" + code]) { const f = path.join(HERE, "wojaks", k + ".png"); if (fs.existsSync(f)) return fileUrl(f); } return null; };
const TITLE = "Languages That Are Basically the Same be like";
const order = Object.keys(PAIRS).filter((k) => MAN[k]).map((k) => ({ k, sc: MAN[k].score })).sort((x, y) => x.sc.exact - y.sc.exact);

const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,"DejaVu Sans",sans-serif;background:#101522;color:#fff}
.a{position:absolute}.f{opacity:0}
#bg{left:-40px;top:-40px;width:2000px;height:1160px}#bg svg{width:100%;height:100%}
#bar{left:0;top:0;width:1920px;height:124px;background:linear-gradient(#fff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;gap:28px;color:#18181d;font-weight:800;font-size:64px}
#bar img{height:60px;border-radius:7px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
#bar .vs{font-size:34px;color:#e8262b;letter-spacing:2px}
.brand{left:22px;top:26px}
.rank{right:40px;top:40px;font-weight:800;font-size:30px;color:#18181d}
.who{bottom:0;width:560px;height:760px;display:flex;align-items:flex-end;justify-content:center;transform-origin:50% 100%}
.who img{max-height:720px;max-width:560px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.4))}
.lab{top:150px;display:flex;align-items:center;gap:12px;background:rgba(15,18,28,.85);padding:8px 16px;border-radius:14px;font-weight:800;font-size:28px}
.lab img{height:34px;border-radius:5px}
.ai{left:50%;transform:translateX(-50%);bottom:18px;background:rgba(15,18,28,.85);padding:6px 18px;border-radius:12px;font-weight:800;font-size:24px;letter-spacing:3px;color:#ffcf5c}
#panel{left:540px;top:145px;width:840px;display:flex;flex-direction:column;gap:12px}
.say{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:22px;padding:14px 24px 14px 28px;font-weight:700;font-size:28px;line-height:1.3;box-shadow:0 12px 30px rgba(0,0,0,.35);position:relative;opacity:0}
.say.sa{border-left:10px solid #e8262b}.say.sb{border-right:10px solid #1d6fa5;text-align:left}
.say .hd{font-size:19px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:#8a8f9c;margin-bottom:6px;display:flex;align-items:center;gap:10px}.say .hd img{height:24px;border-radius:4px}
.say .w{color:#b9bcc6;transition:none}.say .w.on{color:#1d1d24}.say.diff .w.no{color:#e8262b;text-decoration:underline;text-decoration-thickness:3px}
#score{background:rgba(15,18,28,.92);border-radius:22px;padding:14px 26px;box-shadow:0 12px 30px rgba(0,0,0,.35)}
#score .t{font-weight:800;font-size:24px;letter-spacing:2px;color:#ffcf5c;text-transform:uppercase}
#score .r{display:grid;grid-template-columns:170px 1fr 100px;align-items:center;gap:16px;margin-top:6px;font-weight:800;font-size:28px}
#score .r .bar{height:20px;border-radius:10px;background:rgba(255,255,255,.12);overflow:hidden}
#score .r .bar i{display:block;height:100%;width:0;border-radius:10px;background:linear-gradient(90deg,#4fc3ff,#34c759)}
#score .r .v{text-align:right}
#score .sub{font-size:17px;color:#aab;margin-top:-2px}
#score .tot{margin-top:8px;padding-top:6px;border-top:2px solid rgba(255,255,255,.15);display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:32px}
#score .tot b{font-size:50px;color:#34c759}
.card{background:rgba(255,255,255,.96);color:#1d1d24;border-radius:20px;padding:20px 28px;font-weight:600;font-size:33px;line-height:1.32;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:9px solid #e8262b}
`;
const SCRIPT = `<script>
const S=window.__S, ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
window.setT=function(t){
  document.querySelectorAll('[data-in]').forEach(e=>{const i=+e.dataset.in,o=+(e.dataset.out||1e9);const v=ease((t-i)/0.4)*ease((o-t)/0.35);e.style.opacity=v;e.style.transform='translateY('+(1-v)*18+'px)';});
  const bar=document.getElementById('bar'); if(bar) bar.style.transform='translateY('+(-(1-ease(t/0.45))*140)+'px)';
  if(!S.caps) return;
  const cur=S.caps.find(c=>t>=c.t-0.05&&t<=c.t+c.d+0.25);
  ['a','b'].forEach(side=>{const w=document.getElementById('who_'+side);if(!w)return;const on=cur&&cur.side===side;const k=on?1+0.04*Math.abs(Math.sin(t*9)):1;w.style.transform=(side==='b'?'scaleX(-1) ':'')+'scale('+k.toFixed(3)+') translateY('+((1-ease(t/0.6))*120).toFixed(1)+'px)';w.style.filter=on?'brightness(1.08)':'brightness(.92)';});
  S.caps.forEach(c=>{const el=document.getElementById('say_'+c.side);if(!el)return;const v=ease((t-c.t+0.5)/0.4)*(S.hideAt?ease((S.hideAt-t)/0.4):1);el.style.opacity=v;el.style.transform='translateY('+(1-v)*16+'px)';
    const ws=el.querySelectorAll('.w'),n=ws.length;const frac=Math.min(1,Math.max(0,(t-c.t)/(c.d*0.97)));let acc=0;const tot=c.chars;ws.forEach((w,i)=>{acc+=(+w.dataset.n);w.classList.toggle('on',frac*tot>=acc-0.5*(+w.dataset.n));});
    el.classList.toggle('diff',t>=S.diffAt);});
  const sc=document.getElementById('score'); if(sc){const k0=ease((t-S.diffAt-0.4)/1.0);['vocab','sound','grammar'].forEach(k=>{const i=sc.querySelector('#b_'+k);if(i)i.style.width=(S.score[k]*k0)+'%';});}
};
</script>`;
const page = (body, S) => `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${CSS}</style></head><body>${body}<script>window.__S=${JSON.stringify(S)}</script>${SCRIPT}</body></html>`;
const brand = (sub) => `<div class="a brand">${logoSvg(70, true)}</div>${sub ? `<div class="a rank">${esc(sub)}</div>` : ""}`;
const scenes = [];
const add = (name, dur, html, S = {}, audio = null) => scenes.push({ name, dur, html: page(html, S), audio });

// the sentence as word spans (non-cognate words get class "no"); punctuation stays attached to the previous word
const spans = (sentence, wordsInfo) => {
  const bad = new Set(wordsInfo.filter((w) => !w.same).map((w) => w.w));
  const toks = sentence.match(/[^\s]+/g);
  return toks.map((tok) => { const core = tok.match(/\p{L}+(?:['’-]\p{L}+)*/u)?.[0] || ""; return `<span class="w${bad.has(core) ? " no" : ""}" data-n="${tok.length}">${esc(tok)}</span>`; }).join(" ");
};

add("intro", 4.5, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f">${logoSvg(110)}</div>
    <div data-in="0.4" class="f" style="margin-top:40px;font-weight:800;font-size:92px;line-height:1.1;text-shadow:0 8px 40px rgba(0,0,0,.6);width:1500px">${esc(TITLE)}</div>
    <div data-in="1.8" class="f" style="margin-top:50px;display:flex;gap:18px">${order.map((o) => `<img src="${flag(PAIRS[o.k].fa)}" style="height:52px;border-radius:6px"><img src="${flag(PAIRS[o.k].fb)}" style="height:52px;border-radius:6px;margin-right:16px">`).join("")}</div></div>`);

for (const [idx, o] of order.entries()) {
  const p = PAIRS[o.k], m = MAN[o.k], sc = m.score;
  const caps = m.captions.map((c) => ({ ...c, chars: D.sentences[p[c.side]].length }));
  const end = m.len, diffAt = end + 0.3, cardsAt = end + 7.5, dur = +(end + 15.5).toFixed(2);
  const srow = (k, label, sub) => `<div class="r"><span>${label}</span><div class="bar"><i id="b_${k}"></i></div><span class="v">${sc[k]}%</span></div><div class="sub">${esc(sub)}</div>`;
  const html = `<div class="a" id="bg">${scene(p.scene, o.k)}</div>
    <div class="a who" id="who_a" style="left:0">${wj(p.a) ? `<img src="${wj(p.a)}">` : ""}</div>
    <div class="a who" id="who_b" style="right:0">${wj(p.b) ? `<img src="${wj(p.b)}">` : ""}</div>
    <div class="a lab" style="left:40px"><img src="${flag(p.fa)}">${esc(p.na)}</div>
    <div class="a lab" style="right:40px">${esc(p.nb)}<img src="${flag(p.fb)}"></div>
    <div class="a ai">AI VOICES</div>
    <div id="panel" class="a">
      <div class="say sa" id="say_a"><div class="hd"><img src="${flag(p.fa)}">${esc(p.na)}</div>${spans(D.sentences[p.a], sc.words_a)}</div>
      <div class="say sb" id="say_b"><div class="hd"><img src="${flag(p.fb)}">${esc(p.nb)}</div>${spans(D.sentences[p.b], sc.words_b)}</div>
      <div data-in="${diffAt.toFixed(2)}" data-out="${cardsAt.toFixed(2)}" class="f" id="score"><div class="t">Scorecard · red = no twin</div>
        ${srow("vocab", "Words", `${sc.cognates} of ${sc.n} words have a twin`)}${srow("sound", "Sound", "spelling distance of the twin words")}${srow("grammar", "Grammar", `${sc.grammar_ok} of 6: cases, genders, article, verb endings, word order, script`)}
        <div class="tot"><span>SIMILARITY</span><b>${sc.total}%</b></div></div></div>
    <div class="a" style="left:540px;top:150px;width:840px;display:flex;flex-direction:column;gap:22px">
      ${p.cards.map((c, i) => `<div data-in="${(cardsAt + 0.5 + i * 3.4).toFixed(2)}" class="f card">${esc(c)}</div>`).join("")}</div>
    <div id="bar" class="a"><img src="${flag(p.fa)}">${esc(p.na)}<span class="vs">VS</span>${esc(p.nb)}<img src="${flag(p.fb)}"></div>
    ${brand(`#${order.length - idx} of ${order.length}`)}`;
  add(o.k, dur, html, { caps, diffAt, hideAt: cardsAt, score: sc }, path.join(A, o.k + ".wav"));
}

add("outro", 6, `<div class="a" id="bg" style="opacity:.35">${scene("abstract", "title")}</div>
  <div class="a" style="left:0;top:0;width:1920px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div data-in="0.2" class="f" style="font-weight:800;font-size:72px;line-height:1.15;width:1500px">Which pair did we miss?</div>
    <div data-in="0.8" class="f" style="margin-top:30px;font-weight:800;font-size:44px;color:#ffcf5c;letter-spacing:4px">TELL US IN THE COMMENTS 👇</div>
    <div data-in="1.4" class="f" style="margin-top:50px;display:flex;flex-direction:column;gap:14px;font-weight:700;font-size:34px">${[...order].reverse().map((o, i) => `<div>#${i + 1} ${esc(PAIRS[o.k].na)} – ${esc(PAIRS[o.k].nb)} <span style="color:#34c759">${o.sc.total}%</span></div>`).join("")}</div></div>`);

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
const outFile = path.join(OUT, "sent.mp4");
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, ...ins, "-filter_complex",
  filt.join(";") + `;anullsrc=r=48000:cl=stereo,atrim=0:${T}[base];[base]` + [...Array(n).keys()].map((i) => `[a${i + 1}]`).join("") + `amix=inputs=${n + 1}:normalize=0,apad,atrim=0:${T},aresample=48000[aout]`,
  "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outFile], { stdio: "inherit" });
if (r.status) throw new Error("ffmpeg failed");
let t0 = 0;
fs.writeFileSync(path.join(OUT, "sent_timeline.json"), JSON.stringify(scenes.map((s) => { const e = { name: s.name, start: +t0.toFixed(2), dur: s.dur }; t0 += s.dur; return e; }), null, 1));
console.log(`done: ${outFile} (${T}s)`);
