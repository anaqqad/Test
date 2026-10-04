// Renders a narrated comedy skit (skit_a2.mjs): moving avatars, talking mouths, speech bubbles, settings.
//   python3 tts_skit.py skit_a2.mjs && node skit_render.mjs skit_a2.mjs [--still 2,8] [--scenes 0-2]
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character } from "./art.mjs";
import { setting, foreground, kiosk, phoneUI } from "./skit_art.mjs";
import { FONT_CSS, BASE_CSS, renderClip, logoSvg } from "./render.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1]; };
const file = args.find((a) => a.endsWith(".mjs")) || "skit_a2.mjs";
const { SKIT } = await import(pathToFileURL(path.join(HERE, file)).href);
const DIR = path.join(HERE, "cache", "skit", SKIT.key);
const TL = JSON.parse(fs.readFileSync(path.join(DIR, "timeline.json")));
const OUT = path.join(HERE, "out");
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const EXPR = { "?": "neutral", sweat: "sad", "!": "open" };
const FX = { "?": "❓", "!": "❗", sweat: "💦" };

function scenePage(si, sc, tl, baldBefore) {
  const lines = tl.lines;
  const sami = SKIT.sami;
  // Sami's look over time: expression from his latest line, bald from the barber onwards
  const variants = new Map();
  const vkey = (expr, bald) => `${expr}_${bald ? 1 : 0}`;
  const addV = (expr, bald) => { const k = vkey(expr, bald); if (!variants.has(k)) variants.set(k, character({ ...sami, expression: expr, ...(bald ? { hair: "bald" } : {}) }, "s" + k)); return k; };
  let bald = baldBefore, expr = "smile";
  const samiTrack = [{ t: 0, k: addV(expr, bald), open: addV("open", bald) }];
  for (const l of lines) {
    if (l.opts && l.opts.bald) bald = true;
    if (l.who === "S") expr = EXPR[l.fx] || "smile";
    samiTrack.push({ t: l.start, k: addV(expr, bald), open: addV("open", bald) });
  }
  const o = sc.other;
  let otherHtml = "";
  if (o && o.char) otherHtml = `<div class="v" data-k="base">${character(o.char, "o" + si)}</div><div class="v" data-k="open">${character({ ...o.char, expression: "open" }, "oo" + si)}</div>`;
  else if (o && o.machine) otherHtml = `<div class="v" data-k="base">${kiosk()}</div>`;
  else if (o && o.phone) otherHtml = `<div class="v" data-k="base">${phoneUI()}</div><div id="rings"></div>`;
  const D = tl.dur;
  const data = lines.map((l) => ({ who: l.who, s: l.start, d: l.dur, m: l.mouth, fx: l.fx || null }));
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${BASE_CSS}
  #stage{left:0;top:0;width:1920px;height:1080px;transform-origin:50% 60%}
  .layer{left:0;top:0;width:1920px;height:1080px}.layer svg{width:100%;height:100%}
  .who{width:640px;height:885px;bottom:-95px}
  .who .v{position:absolute;inset:0;opacity:0}.who svg{width:100%;height:100%;filter:drop-shadow(0 16px 26px rgba(0,0,0,.35))}
  #sami{left:200px}#other{left:1090px}#other .v svg{transform:scaleX(-1)}
  #other.machine{left:1150px;width:600px;height:900px;bottom:-40px}#other.machine .v svg{transform:none}
  .bub{top:60px;max-width:820px;background:#fff;color:#16182b;font-weight:800;font-size:40px;line-height:1.25;padding:26px 34px;border-radius:30px;box-shadow:0 12px 30px rgba(0,0,0,.35);opacity:0}
  .bub:after{content:"";position:absolute;bottom:-30px;border:22px solid transparent;border-top:34px solid #fff}
  #bS{left:110px}#bS:after{left:150px}#bO{right:110px}#bO:after{right:170px}
  #nar{left:160px;right:160px;bottom:36px;background:rgba(14,16,30,.88);color:#fff;font-weight:700;font-size:38px;line-height:1.3;padding:22px 34px 24px;border-radius:24px;border-left:10px solid #ffcf5c;opacity:0;box-shadow:0 10px 30px rgba(0,0,0,.4)}
  #nar small{display:block;color:#ffcf5c;font-size:20px;letter-spacing:4px;font-weight:800;margin-bottom:6px}
  #lab{left:36px;top:30px;background:rgba(14,16,30,.82);color:#fff;font-weight:800;font-size:28px;padding:10px 22px;border-radius:18px}
  #brand{right:36px;top:34px;color:#fff;font-weight:800;font-size:26px;text-shadow:0 2px 8px rgba(0,0,0,.6)}
  #fx{left:520px;top:300px;font-size:120px;opacity:0}
  #rings{position:absolute;left:150px;top:120px;width:300px;height:300px;border-radius:50%;border:10px solid #4fd1ff;opacity:0}
  #fade{left:0;top:0;width:1920px;height:1080px;background:#000}
  </style></head><body>
  <div id="stage" class="abs">
    <div class="layer abs">${setting(sc.setting)}</div>
    <div id="other" class="abs who ${o && !o.char ? "machine" : ""}">${otherHtml}</div>
    <div class="layer abs">${foreground(sc.setting)}</div>
    <div id="sami" class="abs who">${[...variants].map(([k, svg]) => `<div class="v" data-k="${k}">${svg}</div>`).join("")}</div>
  </div>
  <div id="fx" class="abs"></div>
  <div id="bS" class="abs bub"></div><div id="bO" class="abs bub"></div>
  <div id="nar" class="abs"><small>🎙 NARRATOR</small><span></span></div>
  <div id="lab" class="abs">📍 ${esc(sc.label)}</div><div id="brand" class="abs">LingoDude</div>
  <div id="fade" class="abs"></div>
  <script>
  const D=${D}, L=${JSON.stringify(data)}, TX=${JSON.stringify(lines.map((l) => l.text))}, ST=${JSON.stringify(samiTrack)}, ENTER=${si === 0 || !sc.keepSami ? 1 : 0};
  const $=(s)=>document.querySelector(s);
  const ease=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3), back=(x)=>{x=Math.min(1,Math.max(0,x));const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const samiV=[...document.querySelectorAll('#sami .v')], othV=[...document.querySelectorAll('#other .v')];
  const show=(els,k)=>els.forEach(e=>e.style.opacity=e.dataset.k===k?1:0);
  const mouthAt=(l,t)=>{const i=Math.floor((t-l.s)*30);return i>=0&&i<l.m.length&&l.m[i]==='1'};
  window.setT=(t)=>{
    const cur=L.find(l=>t>=l.s&&t<l.s+l.d);
    const last=[...L].reverse().find(l=>t>=l.s);
    // Sami walks in, bobbing, then breathes
    const w=ENTER?ease(t/1.1):1; const walking=t<1.1&&ENTER;
    const talkS=cur&&cur.who==='S';
    $('#sami').style.transform='translateX('+(-760*(1-w))+'px) translateY('+((walking?-Math.abs(Math.sin(t*11))*22:0)+Math.sin(t*1.7)*5+(talkS?Math.sin(t*15)*4:0))+'px) rotate('+(walking?Math.sin(t*11)*2.5:Math.sin(t*1.2)*0.8)+'deg)';
    const st=[...ST].reverse().find(s=>t>=s.t)||ST[0];
    show(samiV, talkS&&mouthAt(cur,t)?st.open:st.k);
    // the other person / machine
    const talkO=cur&&cur.who!=='S'&&cur.who!=='N';
    if(othV.length){show(othV, talkO&&othV.length>1&&mouthAt(cur,t)?'open':'base');
      $('#other').style.transform='translateY('+(Math.sin(t*1.5+1)*5+(talkO?Math.sin(t*15)*4:0))+'px)';
      const scr=document.querySelector('#scr'); if(scr) scr.setAttribute('fill', talkO&&Math.floor(t*4)%2?'#e74c3c':'#f39c12');
      const r=$('#rings'); if(r){const p=(t*1.2)%1; r.style.opacity=talkO?(1-p):0; r.style.transform='scale('+(0.6+p*0.8)+')';}}
    // camera leans toward whoever talks
    const lean=cur?(cur.who==='S'?-1:cur.who==='N'?0:1):0;
    $('#stage').style.transform='scale('+(1.03+0.01*Math.sin(t*0.5))+') translateX('+(-lean*14)+'px)';
    // bubbles and narrator caption
    const bub=(el,on,txt,l)=>{el.style.opacity=on?1:0; if(on){el.textContent=txt; const k=back((t-l.s)/0.35); el.style.transform='scale('+(0.6+0.4*k)+')';}};
    const lineOn=(who)=>L.findIndex(l=>who(l.who)&&t>=l.s-0.05&&t<l.s+l.d+0.45);
    let i=lineOn(w=>w==='S'); bub($('#bS'),i>=0,TX[i],L[i]);
    i=lineOn(w=>w!=='S'&&w!=='N'); bub($('#bO'),i>=0,TX[i],L[i]);
    i=lineOn(w=>w==='N'); const n=$('#nar'); n.style.opacity=i>=0?1:0; if(i>=0){n.querySelector('span').textContent=TX[i]; n.style.transform='translateY('+(1-ease((t-L[i].s)/0.3))*30+'px)';}
    // reaction emoji above Sami
    const f=[...L].reverse().find(l=>l.who==='S'&&l.fx&&t>=l.s&&t<l.s+l.d+1.2); const fe=$('#fx');
    if(f){fe.textContent=${JSON.stringify(FX)}[f.fx]; fe.style.opacity=1; fe.style.transform='translateY('+(-Math.sin((t-f.s)*3)*10)+'px) scale('+back((t-f.s)/0.4)+')';} else fe.style.opacity=0;
    $('#fade').style.opacity=Math.max(0,1-t/0.3,(t-(D-0.3))/0.3);
  };
  </script></body></html>`;
}

function cardPage(title, sub, dur) {
  return `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${BASE_CSS}
  body{background:radial-gradient(1200px 800px at 50% 45%,#2f6fb0 0%,#14234a 60%,#070b18 100%)}
  #logo{left:0;width:1920px;top:250px;text-align:center}
  #t{left:160px;width:1600px;top:400px;text-align:center;color:#fff;font-weight:800;font-size:100px;line-height:1.08;text-shadow:0 8px 40px rgba(0,0,0,.6)}
  #p{left:0;width:1920px;top:700px;text-align:center;color:#ffcf5c;font-weight:800;font-size:50px;letter-spacing:4px}
  #fade{left:0;top:0;width:1920px;height:1080px;background:#000}</style></head><body>
  <div id="logo" class="abs">${logoSvg(110)}</div><div id="t" class="abs">${esc(title)}</div><div id="p" class="abs">${esc(sub)}</div><div id="fade" class="abs"></div>
  <script>const D=${dur};const $=(s)=>document.querySelector(s);const e=(x)=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
  window.setT=(t)=>{$('#t').style.transform='scale('+(0.9+0.1*e(t/0.7))+')';$('#t').style.opacity=e(t/0.5);$('#p').style.opacity=e((t-0.6)/0.5);$('#fade').style.opacity=Math.max(0,1-t/0.4,(t-(D-0.4))/0.4);};</script></body></html>`;
}

async function main() {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--font-render-hinting=none"] });
  const clipDir = path.join(HERE, "cache", "clips", SKIT.key);
  fs.mkdirSync(clipDir, { recursive: true });
  const jobs = [{ name: "intro", dur: 3.5, html: cardPage(SKIT.title, "😅 a survival story", 3.5) }];
  let bald = false;
  SKIT.scenes.forEach((sc, si) => {
    const tl = TL.scenes[si];
    if (sc.label === "One year later") bald = false; // hair grew back
    jobs.push({ name: String(si).padStart(2, "0"), dur: tl.dur, html: scenePage(si, sc, tl, bald), si });
    if (tl.lines.some((l) => l.opts && l.opts.bald)) bald = true;
  });
  jobs.push({ name: "outro", dur: 4.0, html: cardPage("What was YOUR A2 moment?", "Tell us in the comments 👇", 4.0) });
  const stills = opt("still", null);
  const range = opt("scenes", null);
  let sel = jobs;
  if (range) { const [a, b] = range.split("-").map(Number); sel = jobs.filter((j) => j.si !== undefined && j.si >= a && j.si <= (b ?? a)); }
  if (stills) {
    for (const j of sel) await renderClip(browser, j.html, j.dur, path.join(OUT, `${SKIT.key}_${j.name}.mp4`), stills.split(",").map(Number));
    await browser.close();
    return console.log("stills ->", OUT);
  }
  const t0 = Date.now();
  let next = 0;
  await Promise.all(Array.from({ length: 3 }, async () => {
    while (next < sel.length) {
      const j = sel[next++];
      j.file = path.join(clipDir, `${j.name}.mp4`);
      const sig = j.file + ".sig", h = String(j.html.length) + [...j.html].reduce((a, c) => (a * 33 + c.charCodeAt(0)) >>> 0, 5381);
      if (fs.existsSync(j.file) && fs.existsSync(sig) && fs.readFileSync(sig, "utf8") === h) continue;
      await renderClip(browser, j.html, j.dur, j.file);
      fs.writeFileSync(sig, h);
      console.log(`  ${j.name} done (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
    }
  }));
  await browser.close();
  if (range) return;
  // video
  const list = path.join(clipDir, "list.txt");
  fs.writeFileSync(list, jobs.map((j) => `file '${j.file}'`).join("\n"));
  const silent = path.join(clipDir, "video.mp4");
  execFileSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", silent]);
  // voice track: every line at its place
  let off = 0; const inputs = [], filt = [], mix = [];
  let total = jobs.reduce((a, j) => a + j.dur, 0);
  inputs.push("-f", "lavfi", "-t", total.toFixed(3), "-i", "anullsrc=r=48000:cl=stereo"); mix.push("[0]");
  let n = 1;
  for (const j of jobs) {
    if (j.si !== undefined) for (const l of TL.scenes[j.si].lines) {
      inputs.push("-i", l.wav);
      const ms = Math.round((off + l.start) * 1000);
      filt.push(`[${n}]aresample=48000,pan=stereo|c0=c0|c1=c0,adelay=${ms}|${ms}[a${n}]`); mix.push(`[a${n}]`); n++;
    }
    off += j.dur;
  }
  filt.push(`${mix.join("")}amix=inputs=${mix.length}:normalize=0,loudnorm=I=-16:TP=-1.5[out]`);
  const audio = path.join(clipDir, "audio.wav");
  execFileSync("ffmpeg", ["-v", "error", "-y", ...inputs, "-filter_complex", filt.join(";"), "-map", "[out]", "-ar", "48000", "-t", total.toFixed(3), audio]);
  const final = path.join(OUT, `${SKIT.key}.mp4`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", silent, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final]);
  console.log("done:", final, total.toFixed(1) + "s");
}
main().catch((e) => { console.error(e); process.exit(1); });
