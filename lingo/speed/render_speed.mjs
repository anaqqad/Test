// "Ranking Languages by How Fast They're Spoken": live syllable counter on one read paragraph per language.
// node speed/render_speed.mjs [--still 3,10] -> out/speed.mp4   (data: speed/out/result.json from speed/measure.py)
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, logoSvg, renderClip } from "../render.mjs";
import { scene } from "../art.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const L = path.join(HERE, "..");
const R = JSON.parse(fs.readFileSync(path.join(HERE, "out", "result.json")));
const W = JSON.parse(fs.readFileSync(path.join(HERE, "words.json"))); // per language: words with times + display info
const args = process.argv.slice(2);
const stills = args.includes("--still") ? args[args.indexOf("--still") + 1].split(",").map(Number) : null;
const url = (p) => pathToFileURL(p).href;
const flag = (c) => url(path.join(L, "node_modules", "flag-icons", "flags", "4x3", c + ".svg"));
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const order = Object.keys(R).sort((a, b) => R[a].rate - R[b].rate); // slowest first, fastest last
const LEAD = 0.9, TAIL = 3.6, MAXR = 8;
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat,"Noto Sans JP","Noto Sans SC",sans-serif;background:#0b0f1a}
.a{position:absolute}#bg{left:-40px;top:-40px;width:2000px;height:1160px}#bg svg{width:100%;height:100%}
#bar{left:0;top:0;width:1920px;height:124px;background:linear-gradient(#fff,#f1eee8);box-shadow:0 6px 24px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;gap:28px;color:#18181d}
#bar img{height:60px;border-radius:7px;box-shadow:0 2px 6px rgba(0,0,0,.3)}#bar h1{font-weight:800;font-size:66px}
#rank{right:44px;top:26px;font-weight:800;font-size:64px;color:#e8262b}#brand{left:30px;top:30px}
#wj{left:20px;bottom:0;height:820px}#wj img{height:100%;filter:drop-shadow(0 18px 30px rgba(0,0,0,.5))}
#panel{left:760px;top:160px;width:1110px;background:rgba(12,14,24,.92);border-radius:26px;padding:26px 34px;color:#fff;box-shadow:0 12px 30px rgba(0,0,0,.4)}
.row{display:flex;gap:40px;align-items:flex-end}.k{font-weight:800;font-size:22px;letter-spacing:2px;color:#ffcf5c}
.big{font-weight:800;font-size:120px;line-height:1}.mid{font-weight:800;font-size:64px;line-height:1.1}.u{font-size:26px;color:#aab;font-weight:700;margin-left:8px}
#gauge{height:30px;border-radius:15px;background:rgba(255,255,255,.12);margin-top:18px;overflow:hidden}#gauge i{display:block;height:100%;width:0;background:linear-gradient(90deg,#34c759,#ffcc00 55%,#e8262b)}
#txt{left:760px;top:540px;width:1110px;height:auto;max-height:380px;background:rgba(255,255,255,.95);border-radius:22px;padding:24px 30px;font-weight:600;font-size:32px;line-height:1.45;color:#18181d;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.35)}
#txt .s{color:#c9cdd6}#txt .n{color:#e8262b}
#stamp{left:760px;top:360px;width:1110px;text-align:center;opacity:0}#stamp div{display:inline-block;background:#e8262b;color:#fff;font-weight:800;font-size:76px;padding:14px 36px;border-radius:18px;border:6px solid #fff;box-shadow:0 12px 30px rgba(0,0,0,.5);transform:rotate(-3deg)}
#fade{inset:0;background:#000;pointer-events:none}`;

function langPage(k, idx) {
  const r = R[k], w = W[k];
  const words = w.words; // [t (s from first word), text]
  const dur = LEAD + (r.end - r.start) + TAIL;
  const pauses = w.pauses; // [[a,b]] relative to first word: excluded from the stopwatch
  return [dur, `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${CSS}</style></head><body>
<div id="bg" class="a">${scene(w.scene, k)}</div>
<div id="wj" class="a"><img src="${url(path.join(L, "wojaks", w.wojak + ".png"))}"></div>
<div id="bar" class="a"><img src="${flag(w.flag)}"><h1>${esc(w.name)}</h1></div><div id="brand" class="a">${logoSvg(58, true)}</div><div id="rank" class="a">#${order.length - idx}</div>
<div id="panel" class="a"><div class="row"><div><div class="k">SYLLABLES</div><div class="big" id="cnt">0</div></div>
<div><div class="k">SPEAKING TIME</div><div class="mid" id="clk">0.0<span class="u">s</span></div></div>
<div><div class="k">SPEED</div><div class="mid" id="spd">–<span class="u">syl/s</span></div></div></div><div id="gauge"><i id="g"></i></div></div>
<div id="txt" class="a">${words.map((x, i) => `<span class="s" id="w${i}">${esc(x[1])}</span>`).join(w.sep)}</div>
<div id="stamp" class="a"><div>${r.rate.toFixed(2)} syllables / second</div></div>
<div id="fade" class="a"></div>
<script>
const TK=${JSON.stringify(r.ticks)}, WD=${JSON.stringify(words.map((x) => x[0]))}, PS=${JSON.stringify(pauses)}, LEAD=${LEAD}, SPAN=${(r.end - r.start).toFixed(3)}, D=${dur.toFixed(3)}, RATE=${r.rate}, N=${r.syllables}, ST=${r.speaking_time};
const $=(i)=>document.getElementById(i);
function speak(t){ if(t<=0) return 0; let s=Math.min(t,SPAN); for(const [a,b] of PS){ if(t>a) s-=Math.min(t,b)-a; } return Math.max(0,s); }
let shown=-1;
window.setT=(t)=>{
  const u=t-LEAD; let n=0; while(n<TK.length&&TK[n]<=u) n++;
  if(u>SPAN) n=N;
  $('cnt').textContent=n;
  const sp=u>SPAN?ST:speak(u); $('clk').firstChild.textContent=sp.toFixed(1);
  const rate=sp>1.5?n/sp:0; $('spd').firstChild.textContent=u>SPAN?RATE.toFixed(2):(rate?rate.toFixed(1):'–');
  $('g').style.width=(100*Math.min(1,(u>SPAN?RATE:rate)/${MAXR}))+'%';
  let last=-1; WD.forEach((wt,i)=>{ if(u>=wt) last=i; });
  if(last!==shown){ for(let i=0;i<WD.length;i++){ const e=$('w'+i); e.className=i<last?'':(i===last?'n':'s'); } shown=last;
    const e=$('w'+Math.max(0,last)); const box=$('txt'); if(e.offsetTop>box.scrollTop+280) box.scrollTop=e.offsetTop-140; }
  const k=(u-SPAN-0.3)/0.35; const st=$('stamp'); st.style.opacity=Math.max(0,Math.min(1,k*2)); st.style.transform='scale('+(k<0?1.6:Math.max(1,1.6-0.6*Math.min(1,k)))+')';
  $('wj').style.transform='translateY('+(Math.sin(t*1.5)*5)+'px)';
  $('fade').style.opacity=Math.max(0,1-t/0.3,(t-(D-0.3))/0.3);
};
</script></body></html>`];
}

function titlePage() {
  const dur = 5.5;
  return [dur, `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${CSS}
#t{left:0;right:0;top:300px;text-align:center;color:#fff}#t h1{font-weight:800;font-size:92px;line-height:1.1}#t p{font-weight:700;font-size:38px;color:#ffcf5c;margin-top:26px;letter-spacing:1px}
#fl{left:0;right:0;top:700px;text-align:center}#fl img{height:56px;margin:0 10px;border-radius:6px}</style></head><body>
<div id="bg" class="a">${scene("abstract", "speed")}</div><div class="a" style="left:0;right:0;top:170px;text-align:center">${logoSvg(110)}</div>
<div id="t" class="a"><h1>Ranking Languages by<br>How Fast They're Spoken</h1><p>WE COUNTED EVERY SYLLABLE OF A REAL SPEAKER</p></div>
<div id="fl" class="a">${order.map((k) => `<img src="${flag(W[k].flag)}">`).join("")}</div><div id="fade" class="a"></div>
<script>window.setT=(t)=>{document.getElementById('fade').style.opacity=Math.max(0,1-t/0.4,(t-${dur - 0.3})/0.3);};</script></body></html>`];
}

function boardPage() {
  const dur = 9;
  const top = [...order].reverse();
  return [dur, `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${CSS}
#h{left:0;right:0;top:40px;text-align:center;color:#fff;font-weight:800;font-size:60px}
.r{position:absolute;left:180px;width:1560px;height:96px;display:flex;align-items:center;gap:22px;color:#fff;font-weight:800;font-size:40px;opacity:0}
.r img{height:52px;border-radius:6px}.r .b{flex:1;height:44px;background:rgba(255,255,255,.1);border-radius:22px;overflow:hidden}.r .b i{display:block;height:100%;background:linear-gradient(90deg,#34c759,#ffcc00 55%,#e8262b)}
.r .v{width:120px;text-align:right}.r .nm{width:300px}.r .no{width:70px;color:#ffcf5c}
#note{left:0;right:0;bottom:30px;text-align:center;color:#aab;font-weight:700;font-size:26px}</style></head><body>
<div id="bg" class="a">${scene("abstract", "board")}</div><div id="h" class="a">Syllables per second</div>
${top.map((k, i) => `<div class="r" id="r${i}" style="top:${150 + i * 104}px"><span class="no">#${i + 1}</span><img src="${flag(W[k].flag)}"><span class="nm">${esc(W[k].name)}</span><span class="b"><i style="width:${(100 * R[k].rate) / MAXR}%"></i></span><span class="v">${R[k].rate.toFixed(2)}</span></div>`).join("")}
<div id="note" class="a">One read paragraph per language, one speaker each, pauses not counted. Which language should we time next?</div><div id="fade" class="a"></div>
<script>window.setT=(t)=>{for(let i=0;i<${top.length};i++){const e=document.getElementById('r'+i);const k=(t-0.4-(${top.length}-1-i)*0.35)/0.4;e.style.opacity=Math.max(0,Math.min(1,k));e.style.transform='translateX('+(1-Math.min(1,Math.max(0,k)))*-60+'px)';}
document.getElementById('fade').style.opacity=Math.max(0,1-t/0.4,(t-${dur - 0.4})/0.4);};</script></body></html>`];
}

const pages = [["00_intro", ...titlePage()], ...order.map((k, i) => [`${String(i + 1).padStart(2, "0")}_${k}`, ...langPage(k, i)]), ["99_board", ...boardPage()]];
const TMP = path.join(L, "cache", "clips", "speed"); fs.mkdirSync(TMP, { recursive: true });
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
for (const [name, dur, html] of pages) {
  const f = path.join(TMP, name + ".mp4");
  await renderClip(b, html, dur, f, stills);
  if (!stills) console.log("  ", name, dur.toFixed(1) + "s");
}
await b.close();
if (stills) { console.log("stills -> " + TMP); process.exit(0); }
// audio: each paragraph from the original recording, placed under its clip
let t = 0; const inputs = [], filt = [], mix = [];
pages.forEach(([name, dur], i) => {
  const k = name.split("_")[1];
  if (R[k]) {
    const r = R[k], src = W[k].src, a = Math.max(0, r.start - 0.3), len = r.end - r.start + 0.6;
    inputs.push("-ss", a.toFixed(3), "-t", len.toFixed(3), "-i", src);
    const n = inputs.filter((x) => x === "-i").length - 1, ms = Math.round((t + LEAD - (r.start - a)) * 1000);
    filt.push(`[${n}]aresample=48000,pan=stereo|c0=c0|c1=c0,loudnorm=I=-16:TP=-1.5,afade=t=in:d=0.15,afade=t=out:st=${(len - 0.3).toFixed(2)}:d=0.3,adelay=${ms}|${ms}[a${n}]`);
    mix.push(`[a${n}]`);
  }
  t += dur;
});
const list = path.join(TMP, "list.txt");
fs.writeFileSync(list, pages.map(([n]) => `file '${path.join(TMP, n + ".mp4")}'`).join("\n"));
execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", path.join(TMP, "silent.mp4")]);
execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs, "-filter_complex", filt.join(";") + `;${mix.join("")}amix=inputs=${mix.length}:normalize=0,apad[o]`, "-map", "[o]", "-t", t.toFixed(3), path.join(TMP, "audio.wav")]);
execFileSync("ffmpeg", ["-v", "error", "-y", "-i", path.join(TMP, "silent.mp4"), "-i", path.join(TMP, "audio.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", path.join(L, "out", "speed.mp4")]);
console.log("done: out/speed.mp4", t.toFixed(1) + "s");
