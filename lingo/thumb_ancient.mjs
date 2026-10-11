// Thumbnail for the simulated dead-languages video -> out/brand/thumb_ancient.png
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character } from "./art.mjs";
import { VIDEOS } from "./videos.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const css = ["montserrat/800.css", "noto-sans-egyptian-hieroglyphs/400.css", "noto-sans-cuneiform/400.css", "noto-serif/700.css"]
  .map((f) => `<link rel="stylesheet" href="${pathToFileURL(path.join(HERE, "node_modules/@fontsource", f)).href}">`).join("");
const it = (n) => VIDEOS.ancient.items.find((x) => x.name === n);
const outline = (w, c = "#000") => [-w, 0, w].flatMap((x) => [-w, 0, w].map((y) => `${x}px ${y}px 0 ${c}`)).join(",");
// faint ancient writing in the background
const glyphs = "𓋹𓍑𓋴𓂀𓆣𓇳𓊽𓅓𓃭 𒈗𒂊𒂍𒈬𒈾𒆕𒀭𒌓 VENI VIDI VICI μῆνιν ἄειδε θεὰ ".repeat(14);
const people = [
  ["Ancient Egyptian", "𓋹𓍑𓋴", "Noto Sans Egyptian Hieroglyphs", 70],
  ["Classical Latin", "VENI VIDI VICI", "Noto Serif", 30],
  ["Sumerian", "𒈗𒂊 𒂍", "Noto Sans Cuneiform", 52],
];
const html = `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:radial-gradient(circle at 50% 70%,#5a3a14,#1a1208 55%,#07060a)}.a{position:absolute}.a>svg{width:100%;height:100%}
.bub{position:absolute;background:#fff;border:5px solid #000;border-radius:22px;padding:6px 18px;color:#1b1b1b;white-space:nowrap;box-shadow:0 6px 0 rgba(0,0,0,.5)}
.bub:after{content:"";position:absolute;left:34px;bottom:-26px;border:14px solid transparent;border-top:18px solid #000}</style>
<div class="a" style="inset:-20px;font-size:46px;line-height:1.5;color:#c8a165;opacity:.13;word-break:break-all;font-family:'Noto Sans Egyptian Hieroglyphs','Noto Sans Cuneiform','Noto Serif'">${glyphs}</div>
<div class="a" style="left:0;top:18px;width:1280px;text-align:center;font-weight:800;font-size:118px;line-height:1;color:#fff;text-shadow:${outline(5)},0 10px 0 #000">DEAD LANGUAGES</div>
<div class="a" style="left:0;top:150px;width:1280px;text-align:center"><span style="display:inline-block;background:#ffcc00;color:#111;font-weight:800;font-size:56px;padding:6px 30px;border-radius:16px;border:5px solid #000;box-shadow:0 8px 0 rgba(0,0,0,.6)">🤖 SIMULATED BY AI 🔊</span></div>
${people.map(([n, txt, font, size], i) => `
<div class="a" style="left:${40 + i * 410}px;top:300px;width:380px;height:547px">${character({ ...it(n).char, expression: "open" }, "p" + i)}</div>
<div class="bub" style="left:${[190, 610, 900][i]}px;top:${262}px;font-family:'${font}';font-size:${size}px;line-height:1.15">${txt}</div>
<div class="a" style="left:${40 + i * 410}px;top:672px;width:380px;text-align:center;font-weight:800;font-size:28px;color:#f2d38a;text-shadow:${outline(3)}">${n.replace("Classical ", "").toUpperCase()}</div>`).join("")}`;
const f = path.join(HERE, "cache", "pages", "thumb_ancient.html");
fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, "out", "brand", "thumb_ancient.png") });
await b.close();
console.log("out/brand/thumb_ancient.png");
