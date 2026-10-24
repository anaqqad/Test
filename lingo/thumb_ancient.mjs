// Thumbnails for the "Extinct Languages Simulated by AI" series: node thumb_ancient.mjs [1|2] -> out/brand/thumb_ancient[2].png
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character, scene } from "./art.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const css = ["montserrat/800.css", "noto-serif/700.css", "noto-sans-old-persian/400.css", "noto-serif-tc/700.css"]
  .map((f) => `<link rel="stylesheet" href="${pathToFileURL(path.join(HERE, "node_modules/@fontsource", f)).href}">`).join("");
const PART = process.argv[2] || "1";
const P = {
  // Caesar, since the line is his
  1: { scene: "tuscany", say: "VENI · VIDI · VICI", sayFont: "'Noto Serif',serif", saySize: 44, out: "thumb_ancient.png", tag: "PART 1",
       who: { skin: "olive", hair: "short", hairColor: "#3b2a1a", hat: { type: "laurel", color: "#d9b13b", color2: "#b8901f" }, outfit: { type: "wrap", color: "#f4f1e8", color2: "#9b1d1d", trim: "#d9b13b" }, expression: "open" } },
  // Darius: "adam Dārayavauš", I am Darius, in Old Persian cuneiform
  2: { scene: "zagros", say: "𐎠𐎭𐎶𐏐𐎭𐎠𐎼𐎹𐎺𐎢𐏁", sayFont: "'Noto Sans Old Persian'", saySize: 52, out: "thumb_ancient2.png", tag: "PART 2",
       who: { skin: "olive", hair: "long", hairColor: "black", beard: true, hat: { type: "crown", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "coat", color: "#5b2a6b", inner: "#d9b13b" }, expression: "open" } },
  // Li Bai: "Before my bed, bright moonlight" in characters
  3: { scene: "hills", say: "床前明月光", sayFont: "'Noto Serif TC',serif", saySize: 56, out: "thumb_ancient3.png", tag: "PART 3",
       who: { skin: "light", hair: "bun", hairColor: "black", mustache: true, beardColor: "#1d1d1d", outfit: { type: "coat", color: "#f4f1e8", inner: "#1f4e8c" }, expression: "open" } },
}[PART];
const roman = P.who;
const outline = (w, c = "#000") => [-w, 0, w].flatMap((x) => [-w, 0, w].map((y) => `${x}px ${y}px 0 ${c}`)).join(",");
// a sound wave under the title
const bars = Array.from({ length: 34 }, (_, i) => 10 + Math.round(Math.abs(Math.sin(i * 0.9) * Math.sin(i * 0.31 + 1)) * 54));
const wave = `<svg width="560" height="70" viewBox="0 0 560 70">${bars.map((h, i) => `<rect x="${i * 16.5}" y="${35 - h / 2}" width="9" height="${h}" rx="4.5" fill="#f2d38a"/>`).join("")}</svg>`;
const html = `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat}.a{position:absolute}.a>svg{width:100%;height:100%}</style>
<div class="a" style="left:-30px;top:-30px;width:1340px;height:780px">${scene(P.scene, "thumb")}</div>
<div class="a" style="inset:0;background:linear-gradient(180deg,rgba(255,140,40,.38),rgba(170,70,20,.22) 55%,rgba(20,8,0,.45)),linear-gradient(90deg,rgba(10,6,4,0) 28%,rgba(10,6,4,.82) 58%)"></div>
<div class="a" style="left:10px;top:170px;width:500px;height:720px">${character(roman, "r")}</div>
<div class="a" style="left:150px;top:70px;background:#fffaf0;border:5px solid #1b1b1b;border-radius:26px;padding:10px 26px;font-family:${P.sayFont};font-weight:700;font-size:${P.saySize}px;letter-spacing:2px;color:#1b1b1b;box-shadow:0 8px 0 rgba(0,0,0,.45);white-space:nowrap">${P.say}<div class="a" style="left:87px;bottom:-37px;width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-top:34px solid #1b1b1b"></div></div>
<div class="a" style="left:640px;top:170px;width:600px;text-align:center">
  <div style="font-weight:800;font-size:112px;line-height:.95;color:#fff;text-shadow:${outline(5)},0 10px 0 #000">${P.top || "EXTINCT"}<br><span style="font-size:${P.mid ? 104 : 84}px">${P.mid || "LANGUAGES"}</span></div>
  <div style="display:inline-block;margin-top:30px;background:linear-gradient(#ffd75e,#e9a91c);color:#1b1b1b;font-weight:800;font-size:66px;padding:6px 34px 10px;border-radius:20px;border:5px solid #000;box-shadow:0 9px 0 rgba(0,0,0,.6);white-space:nowrap;${P.pillSize ? `font-size:${P.pillSize}px` : ""}">${P.pill || "REVIVED BY AI"}</div>
  <div style="margin-top:34px;opacity:.95">${wave}</div>
</div>
${P.tag ? `<div class="a" style="right:28px;top:26px;background:#c0392b;color:#fff;font-weight:800;font-size:46px;padding:4px 22px 8px;border-radius:14px;border:5px solid #000;box-shadow:0 7px 0 rgba(0,0,0,.6);transform:rotate(3deg)">${P.tag}</div>` : ""}
<div>
</div>`;
const f = path.join(HERE, "cache", "pages", `thumb_ancient${PART}.html`);
fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, "out", "brand", P.out) });
await b.close();
console.log("out/brand/" + P.out);
