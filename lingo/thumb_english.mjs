// Thumbnail for "How English Sounded Through Time" -> out/brand/thumb_english.png
// Four speakers on a timeline, each saying the start of the Lord's Prayer in their own English.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character } from "./art.mjs";
import { VIDEOS } from "./videos.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const css = ["montserrat/800.css", "noto-serif/700.css"]
  .map((f) => `<link rel="stylesheet" href="${pathToFileURL(path.join(HERE, "node_modules/@fontsource", f)).href}">`).join("");
const it = (n) => VIDEOS.english.items.find((x) => x.name === n).char;
const outline = (w, c = "#000") => [-w, 0, w].flatMap((x) => [-w, 0, w].map((y) => `${x}px ${y}px 0 ${c}`)).join(",");
const stops = [
  ["1000 AD", "Fæder ūre", it("Old English"), "#8a5a2b"],
  ["1390", "Oure fadir", it("Chaucer's English"), "#9b3a2a"],
  ["1611", "Our Father which art", it("King James English"), "#3a4a7a"],
  ["TODAY", "Our Father", it("Modern English"), "#2f6fb0"],
];
const W = 305;
const html = `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:linear-gradient(90deg,#3a2414,#5b3a1c 30%,#2a3f63 75%,#1f4f86)}.a{position:absolute}.a>svg{width:100%;height:100%}
.bub{position:absolute;background:#fffaf0;border:4px solid #111;border-radius:18px;padding:6px 14px;font-family:'Noto Serif',serif;font-weight:700;color:#111;white-space:nowrap;box-shadow:0 6px 0 rgba(0,0,0,.45);transform:translateX(-50%)}
.bub:after{content:"";position:absolute;left:50%;margin-left:-12px;bottom:-22px;border:12px solid transparent;border-top:16px solid #111}</style>
<div class="a" style="left:0;top:14px;width:1280px;text-align:center;font-weight:800;font-size:100px;line-height:1;color:#fff;text-shadow:${outline(5)},0 9px 0 #000">ENGLISH</div>
<div class="a" style="left:0;top:122px;width:1280px;text-align:center"><span style="display:inline-block;background:linear-gradient(#ffd75e,#e9a91c);color:#111;font-weight:800;font-size:50px;padding:2px 30px 6px;border-radius:16px;border:5px solid #000;box-shadow:0 7px 0 rgba(0,0,0,.6)">THROUGH 1,000 YEARS</span></div>
${stops.map(([yr, say, ch, col], i) => {
  const cx = 40 + W / 2 + i * W;
  const size = [42, 42, 27, 40][i];
  return `<div class="bub" style="left:${cx}px;top:232px;font-size:${size}px">${say}</div>
<div class="a" style="left:${cx - 150}px;top:296px;width:300px;height:432px">${character({ ...ch, expression: "open" }, "s" + i)}</div>
<div class="a" style="left:${cx - 95}px;top:640px;width:190px;text-align:center;background:${col};color:#fff;font-weight:800;font-size:34px;padding:4px 0 6px;border-radius:12px;border:4px solid #000;box-shadow:0 5px 0 rgba(0,0,0,.5)">${yr}</div>`;
}).join("")}
${[0, 1, 2].map((i) => `<div class="a" style="left:${40 + (i + 1) * W - 26}px;top:658px;font-weight:800;font-size:44px;color:#ffd75e;text-shadow:${outline(3)}">➜</div>`).join("")}`;
const f = path.join(HERE, "cache", "pages", "thumb_english.html");
fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, "out", "brand", "thumb_english.png") });
await b.close();
console.log("out/brand/thumb_english.png");
