// Photo-style thumbnails (white name strip, real landscape photo, meme-style character, flag, red hook):
// node thumb_photo.mjs [key ...] -> out/brand/thumbP_<key>.png. Photos are free-licence Wikimedia Commons
// files in cache/photos; their credits are in PHOTO_CREDITS below and go into the video description.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { memeCharacter } from "./art.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const css = ["montserrat/700.css", "montserrat/800.css"].map((f) => `<link rel="stylesheet" href="${url("node_modules/@fontsource/" + f)}">`).join("");

export const PHOTO_CREDITS = {
  giza: "Pyramids of Giza: photo by Kallerna, CC BY-SA 3.0, via Wikimedia Commons",
  persepolis: "Persepolis: photo by Carole Raddato, CC BY-SA 2.0, via Wikimedia Commons",
  skellig: "Skellig Michael: photo by Jerzy Strzelecki, CC BY-SA 3.0, via Wikimedia Commons",
  bamburgh: "Bamburgh Castle: photo by mattbuck, CC BY-SA 4.0, via Wikimedia Commons",
};

const T = {
  ancient: { name: "Ancient Egyptian", photo: "giza", pos: "50% 60%", flag: "eg", hook: ["Unheard for", "4,000 Years"],
    who: { skin: "brown", hair: "long", hairColor: "black", fem: true, hat: { type: "headband", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#d9b13b", trim: "#1f4e8c" }, earrings: "#d9b13b", expression: "neutral" } },
  ancient2: { name: "Old Persian", photo: "persepolis", pos: "50% 45%", flag: "ir", hook: ["Lost for", "2,500 Years"],
    who: { skin: "olive", hair: "long", hairColor: "black", beard: true, hat: { type: "crown", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "coat", color: "#5b2a6b", inner: "#d9b13b" }, expression: "neutral" } },
  ancient3: { name: "Old Irish", photo: "skellig", pos: "50% 50%", flag: "ie", hook: ["1,200", "Years Old"],
    who: { skin: "pale", hair: "short", hairColor: "auburn", outfit: { type: "wrap", color: "#6b4a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "neutral" } },
  english: { name: "Old English", photo: "bamburgh", pos: "50% 50%", flag: "gb-eng", hook: ["This Is", "English?!"],
    who: { skin: "pale", hair: "short", hairColor: "auburn", beard: true, beardColor: "#7a3b1c", outfit: { type: "tunic", color: "#2f5d3a", trim: "#c8a165" }, expression: "neutral" } },
};

const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const page = (t) => `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:#000}.a{position:absolute}.a>svg{width:100%;height:100%}</style>
<div class="a" style="inset:0;background:url('${url("cache/photos/" + t.photo + ".jpg")}') ${t.pos}/cover"></div>
<div class="a" style="left:0;top:0;width:1280px;height:78px;background:#fff;text-align:center;font-weight:700;font-size:50px;line-height:80px;color:#111">${t.name}</div>
<div class="a" style="left:-40px;top:96px;width:560px;height:806px">${memeCharacter(t.who, "p")}</div>
<div class="a" style="right:40px;top:112px;width:300px;height:200px;background:url('${url("node_modules/flag-icons/flags/4x3/" + t.flag + ".svg")}') center/cover;box-shadow:0 6px 18px rgba(0,0,0,.45)"></div>
<div class="a" style="right:40px;bottom:56px;width:720px;text-align:right;font-weight:800;font-size:104px;line-height:1.02;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45)">${t.hook.join("<br>")}</div>`;

const keys = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(T);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const k of keys) {
  const f = path.join(HERE, "cache", "pages", `thumbP_${k}.html`);
  fs.writeFileSync(f, page(T[k]));
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(HERE, "out", "brand", `thumbP_${k}.png`) });
  await p.close();
  console.log(`out/brand/thumbP_${k}.png`);
}
await b.close();
