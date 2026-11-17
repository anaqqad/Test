// Chat-comedy renderer (Blueprint 03, lingo/blueprints/CHAT_COMEDY_BLUEPRINT.md).
//   node chat.mjs <episode>                 -> out/chat_<episode>.mp4 (1080x1920, 30 fps, with sound)
//   node chat.mjs <episode> --still 1,5,9   -> out/chat_<episode>_<t>s.png (check frames first)
//   node chat.mjs <episode> --timeline      -> prints the beat timeline only (no render)
// Episode script: chat/episodes/<episode>.json. Our own chat look (no real app's logo or branding).
import fs from "node:fs";
import path from "node:path";
import { spawn, execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const key = args.find((a) => !a.startsWith("--") && !/^[\d.,]+$/.test(a));
const opt = (n, d) => { const i = args.indexOf("--" + n); return i < 0 ? d : args[i + 1]; };
if (!key) throw new Error("usage: node chat.mjs <episode> [--still 1,5] [--timeline]");
const spec = JSON.parse(fs.readFileSync(path.join(HERE, "chat", "episodes", key + ".json"), "utf8"));
const W = spec.width || 1080, H = spec.height || 1920, FPS = spec.fps || 30;
const T = { lineGap: 0.42, holdBase: 0.55, holdPerChar: 0.03, readPerChar: 0.045, minHold: 0.7, lead: 0.1, tail: 0.5, ...(spec.timing || {}) };
const OUT = path.join(HERE, "out");
const PAGES = path.join(HERE, "cache", "pages");
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(PAGES, { recursive: true });
const url = (p) => pathToFileURL(path.isAbsolute(p) ? p : path.join(HERE, p)).href;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const plain = (s) => String(s).replace(/\[\[([^|\]]+)\|[^\]]+\]\]/g, "$1");

// --- timeline -------------------------------------------------------------------------------------
function buildTimeline() {
  let t = T.lead;
  const beats = [];
  spec.beats.forEach((b, i) => {
    t += b.pause || 0;
    let typingFrom = null;
    if (b.typing) { typingFrom = t; t += b.typing; }
    const lines = b.lines || (b.big ? [b.big] : b.panel ? [""] : []);
    const start = t, lineTimes = [];
    let x = start;
    lines.forEach((_, k) => { lineTimes.push(+x.toFixed(3)); if (k < lines.length - 1) x += b.lineGap ?? T.lineGap; });
    const last = plain(lines[lines.length - 1] || ""), all = plain(lines.join(" "));
    const end = b.hold != null ? x + b.hold
      : Math.max(x + Math.max(T.minHold, T.holdBase + T.holdPerChar * last.length), start + 0.3 + T.readPerChar * all.length);
    const cast = spec.cast[b.who] || {};
    const sfx = [];
    if (!b.big && !b.panel) lineTimes.forEach((lt, k) => sfx.push({ at: lt, name: k === 0 && b.firstSfx ? b.firstSfx : "pop" }));
    if (b.ping) sfx.push({ at: start, name: "ping" });
    if (typingFrom != null) sfx.push({ at: typingFrom, name: "typing" });
    (b.sfx ? [].concat(b.sfx) : []).forEach((s) => sfx.push(typeof s === "string" ? { at: start, name: s } : { at: start + (s.offset || 0), name: s.name }));
    beats.push({ i, who: b.who, lines, lineTimes, start: +start.toFixed(3), end: +end.toFixed(3), typingFrom,
      music: b.music ?? cast.music ?? false, sfx, zoom: b.zoom ?? 1, ping: !!b.ping, big: !!b.big, shake: !!b.shake, panel: b.panel || null });
    t = end;
  });
  const dur = +(t + T.tail).toFixed(3);
  return { beats, dur };
}

// --- page -----------------------------------------------------------------------------------------
function rich(s) {
  return esc(s)
    .replace(/\[\[([^|\]]+)\|([^\]]+)\]\]/g, (_, l, c) => `<span class="pill" style="--c:${c}"><i></i>${l}</span>`)
    .replace(/(^|\s)@([\w.]+)/g, '$1<span class="men">@$2</span>')
    .replace(/(^|\s)#([\w-]+)/g, '$1<span class="men">#$2</span>');
}
function avatar(c) {
  const src = c.avatar ? url(c.avatar) : "";
  return `<div class="av" style="background:${c.avatarBg || "#3a3d45"}">${src ? `<img src="${src}">` : ""}</div>`;
}
function clock(i) {
  const [h, m] = (spec.clock || "9:41").split(":").map(Number);
  const mm = m + Math.floor(i / 4), hh = h + Math.floor(mm / 60);
  return `${((hh - 1) % 12) + 1}:${String(mm % 60).padStart(2, "0")} ${spec.ampm || "PM"}`;
}
function beatHTML(b) {
  if (b.panel) {
    const rows = b.panel.rows.map((r) => { const c = spec.cast[r.who] || {}; return `<div class="prow">${avatar(c)}<b style="color:${c.color || "#f2f3f5"}">${esc(c.name || r.who)}</b><span class="dot"></span></div>`; }).join("");
    return `<div class="band panel" id="b${b.i}"><div class="phead">${esc(b.panel.header)}</div>${rows}</div>`;
  }
  if (b.big) return `<div class="band big" id="b${b.i}"><div class="bigt">${rich(b.lines[0])}</div></div>`;
  const c = spec.cast[b.who] || { name: b.who };
  const tag = c.bot ? `<span class="bot">BOT</span>` : c.role ? `<span class="pill" style="--c:${c.roleColor || "#99aab5"}"><i></i>${esc(c.role)}</span>` : "";
  const lines = b.lines.map((l, k) => `<div class="ln" data-k="${k}">${rich(l)}</div>`).join("");
  return `<div class="band${b.ping ? " ping" : ""}" id="b${b.i}">${avatar(c)}<div class="body"><div class="hd"><b style="color:${c.color || "#f2f3f5"}">${esc(c.name || b.who)}</b>${tag}<span class="tm">${clock(b.i)}</span></div>${lines}</div></div>`;
}
function page(tl) {
  const typingNames = tl.beats.map((b) => (spec.cast[b.who] || {}).name || b.who);
  return `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:${W}px;height:${H}px;overflow:hidden;background:#0d0d10;font-family:Inter,"Noto Color Emoji",sans-serif;-webkit-font-smoothing:antialiased}
.band{position:absolute;left:0;width:${W}px;top:50%;display:none;gap:30px;padding:44px 40px 50px;background:#2b2d33;transform-origin:50% 50%}
.band.ping{background:#3a3628;box-shadow:inset 10px 0 0 #f0b232}
.av{flex:0 0 164px;height:164px;border-radius:50%;overflow:hidden;display:flex;align-items:flex-end;justify-content:center}
.av img{width:135%;height:135%;object-fit:cover;object-position:50% 0%;transform:translateY(6%)}
.body{flex:1;min-width:0}
.hd{display:flex;align-items:center;gap:16px;margin-bottom:8px;flex-wrap:wrap}
.hd b{font-size:66px;font-weight:700}
.tm{font-size:40px;color:#949ba4;font-weight:500}
.pill{display:inline-flex;align-items:center;gap:10px;font-size:40px;font-weight:600;color:#e8e9eb;background:#1e1f24;border-radius:12px;padding:4px 16px;vertical-align:middle}
.pill i{width:20px;height:20px;border-radius:50%;background:var(--c)}
.ln .pill{font-size:68px;padding:4px 20px;border:3px solid var(--c)}
.ln .pill i{width:28px;height:28px}
.bot{font-size:34px;font-weight:700;color:#fff;background:#5b6ee1;border-radius:8px;padding:2px 10px}
.ln{font-size:76px;line-height:1.3;color:#dfe1e5;font-weight:500;word-wrap:break-word;visibility:hidden}
.men{color:#c9d4ff;background:rgba(91,110,225,.35);border-radius:8px;padding:0 6px}
.big{justify-content:center;padding:70px 70px}
.bigt{font-size:124px;font-weight:800;color:#fff;text-align:center;line-height:1.1}
.panel{flex-direction:column;gap:26px;padding:50px 60px;background:#24262b}
.phead{font-size:64px;font-weight:800;color:#b5bac1;letter-spacing:2px}
.prow{display:flex;align-items:center;gap:30px}.prow b{font-size:70px}
.dot{width:40px;height:40px;border-radius:50%;background:#3ba55d;border:7px solid #24262b}
#typing{position:absolute;left:60px;top:${Math.round(H * 0.5 + 420)}px;font-size:46px;color:#b5bac1;display:none}
#typing b{color:#fff}
#typing span{display:inline-block;width:14px;height:14px;border-radius:50%;background:#b5bac1;margin-left:8px}
#wm{position:absolute;bottom:90px;width:100%;text-align:center;font:700 38px Montserrat,Inter;color:rgba(255,255,255,.22)}
</style>
<link rel="stylesheet" href="${url("node_modules/@fontsource/montserrat/700.css")}">
${tl.beats.map(beatHTML).join("\n")}
<div id="typing"><b></b> is typing<span></span><span></span><span></span></div>
<div id="wm">${esc(spec.watermark || "LingoDude")}</div>
<script>
const TL=${JSON.stringify(tl)}, NAMES=${JSON.stringify(typingNames)};
function rnd(i){const x=Math.sin(i*99.13)*43758.5;return x-Math.floor(x)}
window.setT=function(t){
  let cur=-1;for(let i=0;i<TL.beats.length;i++){if(TL.beats[i].start<=t)cur=i}
  // while the next beat's typing indicator runs, keep showing the current card
  TL.beats.forEach((b,i)=>{const el=document.getElementById('b'+i);el.style.display=(i===cur)?'flex':'none'});
  const ty=document.getElementById('typing');ty.style.display='none';
  const nx=TL.beats[cur+1];
  if(nx&&nx.typingFrom!=null&&t>=nx.typingFrom&&t<nx.start){ty.style.display='block';ty.querySelector('b').textContent=NAMES[cur+1];
    ty.querySelectorAll('span').forEach((s,k)=>{s.style.transform='translateY('+(-10*Math.max(0,Math.sin((t*7)-k*0.9)))+'px)'})}
  if(cur<0)return;
  const b=TL.beats[cur],el=document.getElementById('b'+cur);
  el.querySelectorAll('.ln').forEach((ln,k)=>{ln.style.visibility=t>=b.lineTimes[k]?'visible':'hidden'});
  const u=t-b.start, pop=u<0.12?0.965+0.035*(u/0.12):1;
  // a small re-pop on every new line, like a cut to a tighter frame
  let lp=1;b.lineTimes.forEach((lt,k)=>{if(k>0&&t>=lt&&t-lt<0.1)lp=1+0.012*(1-(t-lt)/0.1)});
  const push=1+0.03*Math.min(1,u/Math.max(0.5,b.end-b.start));
  const s=b.zoom*pop*lp*push;
  const y=(rnd(cur+1)-0.5)*140;
  let sx=0,sy=0;if(b.shake&&u<0.4){sx=(rnd(Math.floor(t*60))-0.5)*22;sy=(rnd(Math.floor(t*60)+5)-0.5)*22}
  el.style.transform='translate('+sx+'px,calc(-50% + '+(y+sy)+'px)) scale('+s+')';
};
</script>`;
}

// --- render ---------------------------------------------------------------------------------------
async function main() {
  const tl = buildTimeline();
  if (args.includes("--timeline")) {
    for (const b of tl.beats) console.log(`${b.start.toFixed(2).padStart(6)}-${b.end.toFixed(2).padEnd(6)} ${String(b.who).padEnd(7)} ${b.music ? "♪" : " "} ${(b.big ? "[BIG] " : b.panel ? "[PANEL] " : "") + plain(b.lines.join(" / "))}`);
    console.log("duration", tl.dur, "s,", tl.beats.length, "beats");
    return;
  }
  const pageFile = path.join(PAGES, `chat_${key}.html`);
  fs.writeFileSync(pageFile, page(tl));
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const pg = await browser.newPage({ viewport: { width: W, height: H } });
  await pg.goto(pathToFileURL(pageFile).href);
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
  const stills = opt("still", null);
  if (stills) {
    for (const t of stills.split(",").map(Number)) { await pg.evaluate((t) => window.setT(t), t); await pg.screenshot({ path: path.join(OUT, `chat_${key}_${t}s.png`) }); }
    console.log("stills ->", OUT); await browser.close(); return;
  }
  const silent = path.join(OUT, `chat_${key}_silent.mp4`);
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", silent], { stdio: ["pipe", "inherit", "inherit"] });
  const n = Math.round(tl.dur * FPS);
  for (let f = 0; f < n; f++) {
    await pg.evaluate((t) => window.setT(t), f / FPS);
    const buf = await pg.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end(); await new Promise((r, j) => ff.on("close", (c) => (c ? j(new Error("ffmpeg " + c)) : r())));
  await browser.close();
  const tlFile = path.join(OUT, `chat_${key}_timeline.json`);
  fs.writeFileSync(tlFile, JSON.stringify({ ...tl, music: spec.music || null }, null, 1));
  const wav = path.join(OUT, `chat_${key}.wav`);
  execFileSync("python3", [path.join(HERE, "chat_audio.py"), tlFile, wav], { stdio: "inherit" });
  const final = path.join(OUT, `chat_${key}.mp4`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5", "-shortest", final]);
  fs.unlinkSync(silent);
  console.log(`done: ${final} (${tl.dur}s, ${tl.beats.length} beats)`);
}
main().catch((e) => { console.error(e); process.exit(1); });
