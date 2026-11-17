// Chat-comedy renderer (Blueprint 03, lingo/blueprints/DISCORD_CHAT_COMEDY_BLUEPRINT.md).
//   node chat.mjs <episode>                 -> out/chat_<episode>.mp4 (default 1920x1080 long-form, 30 fps, with sound)
//   node chat.mjs <episode> --still 1,5,9   -> out/chat_<episode>_<t>s.png (check frames first)
//   node chat.mjs <episode> --timeline      -> prints the beat timeline only (no render)
// Episode script: chat/episodes/<episode>.json. A Discord-like dark chat look drawn by us (no logos, no real people).
// Like the reference: one message per shot, lines appear one by one, and the camera re-fits the message so it
// fills the frame (short messages are shown huge, long ones zoom out a little as lines arrive).
import fs from "node:fs";
import path from "node:path";
import { spawn, spawnSync, execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const key = args.find((a) => !a.startsWith("--") && !/^[\d.,]+$/.test(a));
const opt = (n, d) => { const i = args.indexOf("--" + n); return i < 0 ? d : args[i + 1]; };
if (!key) throw new Error("usage: node chat.mjs <episode> [--still 1,5] [--timeline]");
const spec = JSON.parse(fs.readFileSync(path.join(HERE, "chat", "episodes", key + ".json"), "utf8"));
const W = spec.width || 1920, H = spec.height || 1080, FPS = spec.fps || 30;
const T = { lineGap: 0.55, holdBase: 0.6, holdPerChar: 0.03, readPerChar: 0.045, minHold: 0.75, lead: 0.1, tail: 0.6, ...(spec.timing || {}) };
const OUT = path.join(HERE, "out");
const PAGES = path.join(HERE, "cache", "pages");
fs.mkdirSync(OUT, { recursive: true }); fs.mkdirSync(PAGES, { recursive: true });
const url = (p) => pathToFileURL(path.isAbsolute(p) ? p : path.join(HERE, p)).href;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const plain = (s) => String(s).replace(/\[\[([^|\]]+)\|[^\]]+\]\]/g, "@$1");

// --- timeline -------------------------------------------------------------------------------------
function buildTimeline() {
  let t = T.lead, mood = "default";
  const beats = [];
  spec.beats.forEach((b, i) => {
    if (b.mood) mood = b.mood; // a beat can switch the scene's music, like Beluga's mood changes
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
    if (!b.big && !b.panel) lineTimes.forEach((lt, k) => sfx.push({ at: lt, name: k === 0 && b.firstSfx ? b.firstSfx : (spec.popSound || "discord_pop") }));
    if (b.ping) sfx.push({ at: start, name: "ping" });
    if (typingFrom != null) sfx.push({ at: typingFrom, name: "typing" });
    (b.sfx ? [].concat(b.sfx) : []).forEach((s) => sfx.push(typeof s === "string" ? { at: start, name: s } : { at: start + (s.offset || 0), name: s.name }));
    beats.push({ i, who: b.who, lines, lineTimes, start: +start.toFixed(3), end: +end.toFixed(3), typingFrom,
      music: (() => { const m = b.music ?? cast.music ?? false; return m === true ? mood : m; })(), sfx, zoom: b.zoom ?? 1, ping: !!b.ping, big: !!b.big, shake: !!b.shake, panel: b.panel || null });
    t = end;
  });
  return { beats, dur: +(t + T.tail).toFixed(3) };
}

// --- page -----------------------------------------------------------------------------------------
const hexA = (h, a) => { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
function rich(s) {
  return esc(s)
    .replace(/\[\[([^|\]]+)\|([^\]]+)\]\]/g, (_, l, c) => `<span class="rmen" style="color:${c};background:${hexA(c, 0.16)}">@${l}</span>`)
    .replace(/(^|\s)@([\w.]+)/g, '$1<span class="men">@$2</span>')
    .replace(/(^|\s)#([\w-]+)/g, '$1<span class="men">#$2</span>');
}
function avatar(c, cls = "av") {
  const src = c.avatar ? url(c.avatar) : "";
  return `<div class="${cls}" style="background:${c.avatarBg || "#4e5058"}">${src ? `<img src="${src}">` : ""}</div>`;
}
function clock(i) {
  const [h, m] = (spec.clock || "1:27").split(":").map(Number);
  const mm = m + Math.floor(i / 4), hh = h + Math.floor(mm / 60);
  return `${spec.dayLabel ?? "Today at "}${((hh - 1) % 12) + 1}:${String(mm % 60).padStart(2, "0")} ${spec.ampm || "PM"}`;
}
function beatHTML(b) {
  let inner;
  if (b.panel) {
    const rows = b.panel.rows.map((r) => { const c = spec.cast[r.who] || {}; return `<div class="prow"><div class="pav">${avatar(c)}<span class="dot"></span></div><b style="color:${c.color || "#f2f3f5"}">${esc(c.name || r.who)}</b></div>`; }).join("");
    inner = `<div class="msg"><div class="row panel"><div class="phead">${esc(b.panel.header)}</div>${rows}</div><div class="tyrow"><span class="dots"><i></i><i></i><i></i></span><span class="tyt"><b></b> is typing...</span></div></div>`;
  } else if (b.big) {
    inner = `<div class="msg"><div class="row bigm"><div class="bigt">${rich(b.lines[0])}</div></div><div class="tyrow"><span class="dots"><i></i><i></i><i></i></span><span class="tyt"><b></b> is typing...</span></div></div>`;
  } else {
    const c = spec.cast[b.who] || { name: b.who };
    const tag = c.bot ? `<span class="bot">✓ BOT</span>` : "";
    const lines = b.lines.map((l, k) => `<div class="ln" data-k="${k}">${rich(l)}</div>`).join("");
    inner = `<div class="msg"><div class="row">${avatar(c)}<div class="body"><div class="hd"><b style="color:${c.color || "#f2f3f5"}">${esc(c.name || b.who)}</b>${tag}<span class="tm">${clock(b.i)}</span></div>${lines}</div></div><div class="tyrow"><span class="dots"><i></i><i></i><i></i></span><span class="tyt"><b></b> is typing...</span></div></div>`;
  }
  return `<div class="band${b.ping ? " ping" : ""}${b.big ? " big" : ""}" id="b${b.i}">${inner}</div>`;
}
function page(tl) {
  const names = tl.beats.map((b) => (spec.cast[b.who] || {}).name || b.who);
  return `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:${W}px;height:${H}px;overflow:hidden;background:#0b0b0c;font-family:Inter,"Noto Color Emoji",sans-serif;-webkit-font-smoothing:antialiased}
.band{position:absolute;left:0;width:${W}px;display:none;background:#36383e;overflow:visible}
.band.ping{background:#45423a}
.band.ping::before{content:"";position:absolute;left:0;top:0;bottom:0;width:${Math.round(W * 0.006)}px;background:#f0b232}
.msg{position:absolute;left:0;top:0;display:inline-block;transform-origin:0 0;white-space:nowrap}
.row{display:flex;align-items:flex-start;gap:18px;padding:14px 26px 16px 18px}
.tyrow{display:none;align-items:center;gap:10px;padding:4px 26px 9px 22px;font-size:21px;color:#b5bac1}
.tyrow b{color:#f2f3f5;font-weight:700}
.tyrow .dots{display:inline-flex;gap:5px;margin-right:4px}.tyrow .dots i{width:9px;height:9px;border-radius:50%;background:#7d828a}
.band::after{content:"";position:absolute;left:0;right:0;bottom:0;height:var(--tyh,0px);background:#303237}
.av{flex:0 0 72px;width:72px;height:72px;border-radius:50%;overflow:hidden;margin-top:2px}
.av img{width:100%;height:100%;object-fit:cover;object-position:50% 8%;transform:scale(1.35);transform-origin:50% 0}
.hd{display:flex;align-items:baseline;gap:12px;line-height:1.25}
.hd b{font-size:31px;font-weight:600}
.tm{font-size:20px;color:#949ba4;font-weight:500}
.bot{align-self:center;font-size:15px;font-weight:700;color:#fff;background:#5865f2;border-radius:5px;padding:1px 7px;letter-spacing:.3px}
.ln{font-size:31px;line-height:1.42;color:#dbdee1;font-weight:400;display:none}
.men{color:#c9cdfb;background:rgba(88,101,242,.3);border-radius:4px;padding:0 3px;font-weight:500}
.rmen{border-radius:4px;padding:0 3px;font-weight:600}
.row.bigm{padding:10px 30px}.bigt{font-size:34px;font-weight:500;color:#e6e7ea}
.row.panel{flex-direction:column;align-items:flex-start;gap:12px;padding:18px 28px}
.phead{font-size:24px;font-weight:700;color:#949ba4;letter-spacing:.6px}
.prow{display:flex;align-items:center;gap:16px}.prow b{font-size:30px;font-weight:600}
.pav{position:relative}.pav .av{flex:0 0 56px;width:56px;height:56px}
.dot{position:absolute;right:-4px;bottom:-2px;width:22px;height:22px;border-radius:50%;background:#23a55a;border:5px solid #36383e}
.msg{z-index:1}
#wm{position:absolute;right:${Math.round(W * 0.02)}px;bottom:${Math.round(H * 0.03)}px;font:700 ${Math.round(H * 0.022)}px Montserrat,Inter;color:rgba(255,255,255,.18)}
</style>
<link rel="stylesheet" href="${url("node_modules/@fontsource/montserrat/700.css")}">
${tl.beats.map(beatHTML).join("\n")}
<div id="wm">${esc(spec.watermark || "LingoDude")}</div>
<script>
const TL=${JSON.stringify(tl)}, NAMES=${JSON.stringify(names)}, W=${W}, H=${H};
function rnd(i){const x=Math.sin(i*99.13)*43758.5;return x-Math.floor(x)}
const ease=u=>u<0?0:u>1?1:1-Math.pow(1-u,3);
const fitCache={};
// natural size of the message with k lines visible -> scale that makes it fill the frame like the reference
function fit(i,k,ty){const id=i+'_'+k+'_'+(ty?1:0);if(fitCache[id])return fitCache[id];
  const b=TL.beats[i],el=document.getElementById('b'+i),m=el.querySelector('.msg');
  el.style.display='block';m.style.transform='none';
  el.querySelectorAll('.ln').forEach((ln,j)=>ln.style.display=j<=k?'block':'none');
  const tr=el.querySelector('.tyrow');tr.style.display=ty?'flex':'none';
  const w=m.offsetWidth,h=m.offsetHeight,th=ty?tr.offsetHeight:0;
  const maxS=b.big?4.2:b.panel?4.0:3.1;
  let s=Math.min(maxS,(W*0.96)/w,(H*0.7)/h)*b.zoom;
  return fitCache[id]={s,w,h,th};}
window.setT=function(t){
  let cur=-1;for(let i=0;i<TL.beats.length;i++){if(TL.beats[i].start<=t)cur=i}
  TL.beats.forEach((b,i)=>{if(i!==cur)document.getElementById('b'+i).style.display='none'});
  const nx=TL.beats[cur+1];
  const typing=!!(nx&&nx.typingFrom!=null&&t>=nx.typingFrom&&t<nx.start);
  if(cur<0)return;
  const b=TL.beats[cur],el=document.getElementById('b'+cur),m=el.querySelector('.msg');
  let k=0;b.lineTimes.forEach((lt,j)=>{if(t>=lt)k=j});
  const f=fit(cur,k,typing);
  // the camera eases to the new fit for 0.15 s when a line arrives (the reference re-frames on every line)
  let s=f.s, h=f.h;
  if(k>0&&!typing){const p=fit(cur,k-1,false),u=ease((t-b.lineTimes[k])/0.15);s=p.s+(f.s-p.s)*u;h=p.h+(f.h-p.h)*u}
  if(typing){const p=fit(cur,k,false),u=ease((t-nx.typingFrom)/0.15);s=p.s+(f.s-p.s)*u;h=p.h+(f.h-p.h)*u}
  s=Math.min(s,(W*0.96)/f.w); // never let a line run off the frame while the camera re-fits
  const u0=t-b.start, pop=u0<0.1?0.97+0.03*(u0/0.1):1;
  const push=1+0.02*Math.min(1,u0/Math.max(0.6,b.end-b.start));
  s*=pop*push;
  el.style.display='block';
  el.querySelectorAll('.ln').forEach((ln,j)=>ln.style.display=j<=k?'block':'none');
  const tr=el.querySelector('.tyrow');tr.style.display=typing?'flex':'none';
  if(typing){tr.querySelector('b').textContent=NAMES[cur+1];
    const ph=Math.floor(t*3.2)%3;tr.querySelectorAll('.dots i').forEach((d,j)=>{d.style.background=j===ph?'#f2f3f5':'#7d828a'})}
  el.style.setProperty('--tyh',(typing?f.th*s:0)+'px');
  const bandH=h*s, yc=H*(0.5+(rnd(cur+1)-0.5)*0.16);
  let sx=0,sy=0;if(b.shake&&u0<0.4){sx=(rnd(Math.floor(t*60))-0.5)*W*0.012;sy=(rnd(Math.floor(t*60)+5)-0.5)*H*0.02}
  el.style.top=(yc-bandH/2+sy)+'px';el.style.height=bandH+'px';
  const x0=b.big?(W-f.w*s)/2:Math.max(0,Math.min(W*0.03,W-f.w*s));
  m.style.transform='translate('+(x0+sx)+'px,0) scale('+s+')';
};
</script>`;
}

// --- render ---------------------------------------------------------------------------------------
async function main() {
  const tl = buildTimeline();
  if (args.includes("--timeline")) {
    for (const b of tl.beats) console.log(`${b.start.toFixed(2).padStart(6)}-${b.end.toFixed(2).padEnd(6)} ${String(b.who).padEnd(7)} ${b.music ? "♪" : " "} ${(b.big ? "[BIG] " : b.panel ? "[PANEL] " + b.panel.header : "") + plain(b.lines.join(" / "))}`);
    console.log("duration", tl.dur, "s,", tl.beats.length, "beats");
    return;
  }
  const pageFile = path.join(PAGES, `chat_${key}.html`);
  fs.writeFileSync(pageFile, page(tl));
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const pg = await browser.newPage({ viewport: { width: W, height: H } });
  await pg.goto(pathToFileURL(pageFile).href);
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(400);
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
  fs.writeFileSync(tlFile, JSON.stringify({ ...tl, music: spec.music || null, musicDb: spec.musicDb ?? -21 }, null, 1));
  const wav = path.join(OUT, `chat_${key}.wav`);
  execFileSync("python3", [path.join(HERE, "chat_audio.py"), tlFile, wav], { stdio: "inherit" });
  const final = path.join(OUT, `chat_${key}.mp4`);
  // two-pass loudness: measure the mix, then apply one fixed gain to reach the reference's -14.8 LUFS
  const r = spawnSync("ffmpeg", ["-hide_banner", "-i", wav, "-af", "ebur128", "-f", "null", "-"], { encoding: "utf8" });
  const I = +((r.stderr.match(/I:\s+(-?[\d.]+) LUFS/g) || []).pop() || "I: -14").match(/-?[\d.]+/)[0];
  const gain = Math.min(0, (spec.loudness ?? -14) - I).toFixed(1); // levels are set in chat_audio.py like the reference; only turn down, never up
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", `volume=${gain}dB,alimiter=limit=0.89`, "-shortest", final]);
  console.log(`  loudness ${I} LUFS -> gain ${gain} dB`);
  fs.unlinkSync(silent); fs.unlinkSync(wav);
  console.log(`done: ${final} (${tl.dur}s, ${tl.beats.length} beats)`);
}
main().catch((e) => { console.error(e); process.exit(1); });
