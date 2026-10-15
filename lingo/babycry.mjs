// "Babies Cry With an Accent": real cry clips (public videos, credited) with their pitch traced live on screen,
// checked against the published studies. Data: python3 baby_analyze.py -> cache/babies/analysis.json.
// node babycry.mjs [--still t1,t2] [--preview]   -> out/babycry.mp4
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { FONT_CSS, renderClip } from "./render.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out"), B = path.join(HERE, "cache", "babies"), TMP = path.join(B, "build");
fs.mkdirSync(TMP, { recursive: true });
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf("--" + k); return i < 0 ? d : args[i + 1] ?? true; };
const A = JSON.parse(fs.readFileSync(path.join(B, "analysis.json")));
const flag = (c) => pathToFileURL(path.join(HERE, "node_modules/flag-icons/flags/4x3", c + ".svg")).href;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");

// ---------- country segments: which stretches of each clip are played ----------
const C = {
  france: { name: "France", lang: "French", flag: "fr", pieces: [[2.6, 3.5], [8.4, 12.8]] },
  germany: { name: "Germany", lang: "German", flag: "de", pieces: [[0.4, 11.1]] },
  china: { name: "China", lang: "Mandarin", flag: "cn", pieces: [[0.0, 10.6]] },
  cameroon2: { name: "Cameroon", lang: "?", flag: "cm", pieces: [[11.2, 18.4]] },
  sweden: { name: "Sweden", lang: "Swedish", flag: "se", pieces: [[1.1, 21.2]] },
};
// cries inside the played pieces, on the segment's own clock
function track(k) {
  let off = 0; const cries = [];
  for (const [a, b] of C[k].pieces) {
    for (const c of A[k].cries) if (c.start >= a && c.end <= b) cries.push({ ...c, t0: off + c.start - a });
    off += b - a;
  }
  return { len: off, cries };
}
const stats = (k) => A[k].shapes;
// melody "turns" per second of crying (direction changes over 2 semitones), cries above 300 Hz only (skips adult voices)
const turns = (k) => { const cs = A[k].cries.filter((c) => c.median_hz > 300); return cs.reduce((a, c) => a + c.arcs, 0) / cs.reduce((a, c) => a + c.end - c.start, 0); };

// ---------- page template ----------
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;font-family:Montserrat;background:#101522;color:#fff}
.a{position:absolute}.f{opacity:0;transition:none}
#bar{left:0;top:0;width:1920px;height:120px;background:linear-gradient(#fff,#f1eee8);color:#18181d;display:flex;align-items:center;justify-content:center;gap:24px;box-shadow:0 6px 24px rgba(0,0,0,.3)}
#bar h1{font-weight:800;font-size:68px}#bar img{height:62px;border-radius:6px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
.brand{left:26px;top:44px;font-weight:800;font-size:24px;color:#18181d}
.card{background:#fff;color:#1d1d24;border-radius:20px;padding:22px 30px;font-weight:600;font-size:34px;line-height:1.3;box-shadow:0 12px 30px rgba(0,0,0,.35);border-left:10px solid #ff4d5a}
.card b{color:#e8262b}
.tag{font-weight:800;font-size:22px;letter-spacing:3px;color:#ffcf5c;text-transform:uppercase}
.badge{font-weight:800;font-size:30px;padding:8px 18px;border-radius:12px;color:#fff}
.src{left:40px;bottom:22px;font-size:20px;font-weight:600;color:#9aa3b8}
#plot{left:90px;top:190px;width:1100px;height:600px;background:#18203a;border-radius:24px;border:3px solid #2d3a63}`;

const SCRIPT = `<script>
const S=window.__S;
window.setT=function(t){
  document.querySelectorAll('[data-in]').forEach(e=>{const i=+e.dataset.in,o=+(e.dataset.out||1e9);
    const v=Math.min(1,Math.max(0,(t-i)/0.35))*Math.min(1,Math.max(0,(o-t)/0.35));e.style.opacity=v;
    e.style.transform=e.dataset.pop?'scale('+(0.85+0.15*v)+')':'translateY('+(1-v)*24+'px)';});
  (S.traces||[]).forEach((tr,i)=>{const el=document.getElementById('tr'+i);if(!el)return;
    const pts=tr.p.filter(p=>p[0]<=t).map(p=>p[1]+','+p[2]).join(' ');el.setAttribute('points',pts);});
  const ph=document.getElementById('ph');if(ph&&S.play){const x=S.play.x0+(S.play.x1-S.play.x0)*Math.min(1,Math.max(0,(t-S.play.t0)/S.play.len));ph.setAttribute('x1',x);ph.setAttribute('x2',x);ph.style.opacity=(t>=S.play.t0&&t<=S.play.t0+S.play.len)?1:0;}
  document.querySelectorAll('[data-count]').forEach(e=>{const ts=JSON.parse(e.dataset.count);e.textContent=ts.filter(x=>x<=t).length;});
};
</script>`;
const page = (body, S = {}) => `<!doctype html><html><head><meta charset="utf-8">${FONT_CSS}<style>${CSS}</style></head><body>${body}<script>window.__S=${JSON.stringify(S)}</script>${SCRIPT}</body></html>`;
const bar = (title, fl) => `<div id="bar" class="a"><h1>${esc(title)}</h1>${fl ? `<img src="${flag(fl)}">` : ""}</div><div class="a brand">LingoDude</div>`;

// pitch plot: x = seconds on the segment clock, y = log pitch 150..1100 Hz
function plot(k, t0, opts = {}) {
  const { len, cries } = track(k);
  const X0 = 80, X1 = 1060, Y0 = 540, Y1 = 40;
  const y = (hz) => Y0 - (Math.log(Math.min(Math.max(hz, 150), 1100) / 150) / Math.log(1100 / 150)) * (Y0 - Y1);
  const x = (s) => X0 + (s / len) * (X1 - X0);
  const col = { rising: "#4fc3ff", falling: "#ff5c6c", "rise-fall": "#c9c9d6" };
  // median-of-7 smoothing removes pitch-tracker octave jumps (single-frame spikes) before drawing
  const med = (q) => q.map((p, i) => { const w = q.slice(Math.max(0, i - 3), i + 4).map((v) => v[1]).sort((m, n) => m - n); return [p[0], w[w.length >> 1]]; });
  const traces = cries.map((c) => ({ c: col[c.shape], p: med(c.contour).filter((_, i) => i % 2 === 0).filter((q) => q[1] > 200).map(([s, hz]) => [+(t0 + c.t0 + s).toFixed(3), +x(c.t0 + s).toFixed(1), +y(hz).toFixed(1)]) }));
  const grid = [200, 300, 500, 800].map((hz) => `<line x1="${X0}" x2="${X1}" y1="${y(hz)}" y2="${y(hz)}" stroke="#2d3a63" stroke-width="2"/><text x="${X0 - 12}" y="${y(hz) + 8}" fill="#7d89a8" font-size="22" text-anchor="end" font-weight="700">${hz}</text>`).join("");
  const labels = opts.labels === false ? "" : cries.map((c) => {
    const mid = c.t0 + (c.end - c.start) / 2, top = Math.min(...med(c.contour).map((q) => y(q[1]))) - 16;
    const sym = c.shape === "rising" ? "↗" : c.shape === "falling" ? "↘" : "↗↘";
    return `<text data-in="${(t0 + c.t0 + c.end - c.start).toFixed(2)}" class="f" x="${x(mid)}" y="${Math.max(top, 70)}" text-anchor="middle" font-size="44" font-weight="800" fill="${col[c.shape]}">${sym}</text>`;
  }).join("");
  const svg = `<svg class="a" style="left:0;top:0" width="1100" height="600" viewBox="0 0 1100 600">${grid}
    <text x="${X0}" y="${Y0 + 46}" fill="#7d89a8" font-size="22" font-weight="700">PITCH OF EACH CRY (Hz) · TRACED FROM THE RECORDING</text>
    ${traces.map((tr, i) => `<polyline id="tr${i}" fill="none" stroke="${tr.c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`).join("")}
    <line id="ph" x1="${X0}" x2="${X0}" y1="${Y1 - 10}" y2="${Y0}" stroke="#ffcf5c" stroke-width="3" stroke-dasharray="8 8"/>${labels}</svg>`;
  return { html: `<div id="plot" class="a">${svg}</div>`, S: { traces, play: { x0: X0, x1: X1, t0, len } }, len, cries };
}

// ---------- scenes ----------
const scenes = [];
const SRC = "Clip: public video, used for illustration only. Not a recording from the studies.";
const add = (name, dur, html, S, audio = []) => scenes.push({ name, dur, html: page(html, S), audio });

// 0 disclaimer
add("disclaimer", 7, `<div class="a" style="left:260px;top:250px;width:1400px;text-align:center">
  <div class="tag" data-in="0.1" class="f" style="font-size:30px">⚠️ Before we start</div>
  <div data-in="0.4" class="f" style="margin-top:34px;font-size:44px;font-weight:700;line-height:1.4">The baby cries in this video come from <b style="color:#ffcf5c">public videos</b>, not from the scientific studies.</div>
  <div data-in="1.6" class="f" style="margin-top:30px;font-size:38px;font-weight:600;line-height:1.4;color:#c9d1e6">One baby proves nothing. The real research measured <b style="color:#fff">hundreds of cries</b>. Studies and video sources are in the description.</div></div>`);

// 1 hook: French then German, short
{
  const fr = track("france"), de = track("germany");
  add("hook", 9.5, `${bar("Babies Cry With an Accent?")}
    <div class="a" style="left:0;top:330px;width:1920px;text-align:center">
      <div data-in="0.2" class="f" style="font-size:64px;font-weight:800">Can a baby only a few days old…</div>
      <div data-in="3.6" class="f" style="margin-top:40px;font-size:64px;font-weight:800;color:#ffcf5c">…already cry with an <u>accent</u>?</div>
      <div data-in="0.6" class="f" style="margin-top:80px;display:flex;justify-content:center;gap:160px">
        <div style="text-align:center"><img src="${flag("fr")}" style="height:150px;border-radius:12px"><div style="font-size:40px;font-weight:800;margin-top:12px">🔊 French baby</div></div>
        <div data-in="3.4" class="f" style="text-align:center"><img src="${flag("de")}" style="height:150px;border-radius:12px"><div style="font-size:40px;font-weight:800;margin-top:12px">🔊 German baby</div></div></div></div>`,
    {}, [{ k: "france", from: 8.4, to: 11.4, at: 0.3 }, { k: "germany", from: 5.2, to: 7.6, at: 3.6 }, { k: "germany", from: 8.3, to: 10.2, at: 6.3 }]);
}

// 2 the study
add("study", 12, `${bar("The Study")}
  <div class="a" style="left:120px;top:200px;width:1680px">
    <div data-in="0.2" class="f card">In 2009, scientists in Germany and France recorded <b>60 newborns</b>, only 2 to 5 days old, and analysed <b>1,254 cries</b>.</div>
    <div data-in="3.2" class="f" style="display:flex;gap:60px;margin-top:50px">
      <div style="flex:1;background:#18203a;border-radius:24px;padding:26px;text-align:center"><img src="${flag("fr")}" style="height:80px;border-radius:8px">
        <svg width="600" height="220" viewBox="0 0 600 220"><path d="M40 180 C200 175 380 140 560 40" fill="none" stroke="#4fc3ff" stroke-width="12" stroke-linecap="round"/></svg>
        <div style="font-size:40px;font-weight:800;color:#4fc3ff">French babies: mostly RISING ↗</div></div>
      <div style="flex:1;background:#18203a;border-radius:24px;padding:26px;text-align:center"><img src="${flag("de")}" style="height:80px;border-radius:8px">
        <svg width="600" height="220" viewBox="0 0 600 220"><path d="M40 40 C220 140 400 175 560 180" fill="none" stroke="#ff5c6c" stroke-width="12" stroke-linecap="round"/></svg>
        <div style="font-size:40px;font-weight:800;color:#ff5c6c">German babies: mostly FALLING ↘</div></div></div>
    <div data-in="7.2" class="f card" style="margin-top:44px">Just like their mothers' languages: French phrases tend to <b>rise</b> at the end, German words tend to start <b>strong and fall</b>.</div></div>
  <div class="a src">Mampe, Friederici, Christophe &amp; Wermke (2009), Current Biology 19: 1994-1997</div>`);

// country test scene
function countryScene(k, claim, verdict, verdictColor, note) {
  const lead = 2.2, pl = plot(k, lead), dur = +(lead + pl.len + 4.2).toFixed(2);
  const rising = pl.cries.filter((c) => c.shape === "rising").map((c) => +(lead + c.t0 + c.end - c.start).toFixed(2));
  const falling = pl.cries.filter((c) => c.shape === "falling").map((c) => +(lead + c.t0 + c.end - c.start).toFixed(2));
  const end = lead + pl.len;
  const html = `${bar(`${C[k].name}`, C[k].flag)}${pl.html}
    <div class="a" style="left:1240px;top:190px;width:600px">
      <div data-in="0.2" class="f card" style="font-size:30px">${claim}</div>
      <div data-in="${lead}" class="f" style="margin-top:30px;display:flex;gap:20px">
        <div class="badge" style="background:#1d6fa5">↗ rising <span data-count='${JSON.stringify(rising)}'>0</span></div>
        <div class="badge" style="background:#a5323d">↘ falling <span data-count='${JSON.stringify(falling)}'>0</span></div></div>
      <div data-in="${(end + 0.3).toFixed(2)}" data-pop="1" class="f" style="margin-top:34px;background:${verdictColor};border-radius:20px;padding:20px 26px;font-size:36px;font-weight:800;line-height:1.25">${verdict}</div>
      ${note ? `<div data-in="${(end + 1.2).toFixed(2)}" class="f" style="margin-top:22px;font-size:26px;font-weight:600;color:#c9d1e6;line-height:1.35">${note}</div>` : ""}</div>
    <div class="a src">${SRC}</div>`;
  let at = lead; const audio = [];
  for (const [a, b] of C[k].pieces) { audio.push({ k, from: a, to: b, at }); at += b - a; }
  add(k, dur, html, pl.S, audio);
}

countryScene("france", "Study: French newborns mostly cry with a <b>rising</b> melody.",
  `✅ Our French baby: ${stats("france").rising} of ${A.france.cries.length} cries rising`, "#1f7a4d");
countryScene("germany", "Study: German newborns mostly cry with a <b>falling</b> melody.",
  `✅ Our German baby: ${stats("germany").falling} of ${A.germany.cries.length} cries falling`, "#1f7a4d");

// 3 why: the womb
add("womb", 11, `${bar("But How?")}
  <svg class="a" style="left:160px;top:230px" width="620" height="620" viewBox="0 0 620 620">
    <circle cx="310" cy="310" r="270" fill="#5a2a3a" stroke="#ff8fa3" stroke-width="10"/>
    <circle cx="300" cy="330" r="120" fill="#f2c4a8"/><circle cx="270" cy="310" r="10" fill="#3a2a2a"/><circle cx="330" cy="310" r="10" fill="#3a2a2a"/>
    <path d="M285 360 q15 10 30 0" stroke="#3a2a2a" stroke-width="6" fill="none"/>
    ${[0, 1, 2].map((i) => `<path data-in="${1 + i * 0.5}" class="f" d="M${560 - i * 40} ${180 + i * 10} q30 130 0 260" stroke="#ffcf5c" stroke-width="10" fill="none" stroke-linecap="round"/>`).join("")}</svg>
  <div class="a" style="left:880px;top:250px;width:900px">
    <div data-in="0.3" class="f card">In the last months of pregnancy, babies can hear their mother's voice through the womb.</div>
    <div data-in="3.6" class="f card" style="margin-top:30px">The words are muffled, but the <b>melody</b> of the language gets through: its rises and falls.</div>
    <div data-in="7" class="f card" style="margin-top:30px">So when they are born, they cry with that melody. Their first language lesson happened <b>before birth</b>.</div></div>`);

// 4 tonal languages
add("tonal", 9, `${bar("What About Tonal Languages?")}
  <div class="a" style="left:160px;top:230px;width:1600px">
    <div data-in="0.2" class="f card">In tonal languages like Mandarin, the pitch of a word changes its meaning. <b>mā</b> is mother, <b>mǎ</b> is horse.</div>
    <div data-in="3.4" class="f card" style="margin-top:34px">The same research team recorded <b>55 Chinese</b> newborns and <b>21 Nso</b> newborns from Cameroon, whose language Lamnso is also tonal. Their cries had <b>more ups and downs</b> than German babies' cries.</div></div>
  <div class="a src">Wermke et al., Journal of Voice (Mandarin) and Speech, Language and Hearing (Lamnso)</div>`);

const ups = (k) => turns(k).toFixed(1);
countryScene("china", "Study: Chinese newborns cry with <b>more ups and downs</b> than German newborns.",
  `✅ Our Chinese baby: ${ups("china")} pitch turns per second, vs ${ups("germany")} for our German baby`, "#1f7a4d",
  "A turn = the melody changes direction by more than 2 semitones.");
countryScene("cameroon2", "Study: Nso babies' cries swing even more, almost <b>like chanting</b>.",
  `✅ Our Cameroonian baby: ${ups("cameroon2")} pitch turns per second, vs ${ups("germany")} for our German baby`, "#1f7a4d",
  "But Cameroon has 250+ languages, and we do not know which one this family speaks.");

add("sweden_intro", 6.5, `${bar("Bonus: Sweden", "se")}
  <div class="a" style="left:160px;top:260px;width:1600px">
    <div data-in="0.2" class="f card">Swedish is famous for its sing-song melody: some words differ only by their pitch, like <b>anden</b> (the duck) and <b>anden</b> (the spirit).</div>
    <div data-in="2.8" class="f card" style="margin-top:34px">News reports say Swedish newborns cry in a more sing-song way. We could not find the published study yet, so let's just listen.</div></div>`);
countryScene("sweden", "Is our Swedish baby sing-song?",
  `🤔 Not sing-song: ${ups("sweden")} pitch turns per second, vs ${ups("germany")} for our German baby`, "#6b5a1f",
  `A second Swedish baby we checked: ${ups("sweden2")} turns per second. Also calmer.`);

// 5 outro
add("outro", 10, `${bar("So… Do Babies Cry With an Accent?")}
  <div class="a" style="left:200px;top:230px;width:1520px">
    <div data-in="0.2" class="f card">One baby proves nothing. Four of our babies matched the studies. Our two Swedish babies did not.</div>
    <div data-in="3" class="f card" style="margin-top:30px">That is exactly why scientists record <b>hundreds</b> of babies. And in the big studies, the pattern is real.</div>
    <div data-in="5.8" class="f" style="margin-top:56px;text-align:center;font-size:56px;font-weight:800;color:#ffcf5c">Which language should we test next? 👇</div></div>`);

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

// audio: every scene's cry pieces (filtered, same filters as the cleaned files but without trimming) on one timeline
let t = 0; const ins = [], filt = [];
for (const s of scenes) {
  for (const a of s.audio) {
    const n = ins.length / 2 + 1; // input 0 is the video
    ins.push("-i", path.join(B, "raw", a.k + ".wav"));
    const delay = Math.round((t + a.at) * 1000);
    filt.push(`[${n}]atrim=${a.from}:${a.to},asetpts=PTS-STARTPTS,highpass=f=150,lowpass=f=8000,afftdn=nf=-30,loudnorm=I=-20:TP=-3,afade=t=in:d=0.05,afade=t=out:st=${(a.to - a.from - 0.08).toFixed(2)}:d=0.08,adelay=${delay}|${delay}[a${n}]`);
  }
  t += s.dur;
}
const n = ins.length / 2;
const list = path.join(TMP, "list.txt");
fs.writeFileSync(list, clips.map((c) => `file '${c}'`).join("\n"));
const outFile = path.join(OUT, "babycry.mp4");
const r = spawnSync("ffmpeg", ["-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list, ...ins, "-filter_complex",
  filt.join(";") + ";" + [...Array(n).keys()].map((i) => `[a${i + 1}]`).join("") + `amix=inputs=${n}:normalize=0,apad,atrim=0:${t.toFixed(2)},aresample=48000,pan=stereo|c0=c0|c1=c0[aout]`,
  "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", outFile], { stdio: "inherit" });
if (r.status) throw new Error("ffmpeg failed");
fs.writeFileSync(path.join(OUT, "babycry_timeline.json"), JSON.stringify(scenes.reduce((acc, s) => { acc.list.push({ name: s.name, start: +acc.t.toFixed(2), dur: s.dur }); acc.t += s.dur; return acc; }, { t: 0, list: [] }).list, null, 1));
console.log(`done: ${outFile} (${t.toFixed(1)}s)`);
