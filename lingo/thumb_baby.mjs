// Thumbnail for the "Babies Cry With an Accent" video: node thumb_baby.mjs -> out/brand/thumbP_babycry.png
// Same look as thumb_photo.mjs (white name strip, big Wojak, flags, red hook), on a soft nursery-coloured background.
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const css = ["montserrat/700.css", "montserrat/800.css"].map((f) => `<link rel="stylesheet" href="${url("node_modules/@fontsource/" + f)}">`).join("");
const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const flagBox = (c, arrow, col) => `<div style="display:flex;align-items:center;gap:14px"><div style="width:190px;height:127px;background:url('${url("node_modules/flag-icons/flags/4x3/" + c + ".svg")}') center/cover;border:5px solid #fff;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,.4)"></div><div style="font-weight:800;font-size:110px;line-height:1;color:${col};text-shadow:${stroke(6, "#fff")}">${arrow}</div></div>`;
const html = `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:radial-gradient(circle at 30% 60%,#ffe2ec,#f7b8cf 55%,#d98fb0)}.a{position:absolute}</style>
<div class="a" style="left:0;top:0;width:1280px;height:78px;background:#fff;text-align:center;font-weight:700;font-size:50px;line-height:80px;color:#111">Newborn Babies</div>
<img class="a" src="${url("wojaks/babycry.png")}" style="left:-10px;bottom:0;height:640px;max-width:640px;object-fit:contain;object-position:left bottom">
<div class="a" style="right:44px;top:112px;display:flex;flex-direction:column;gap:22px;align-items:flex-end">${flagBox("fr", "↗", "#1d8fe0")}${flagBox("de", "↘", "#e8262b")}</div>
<div class="a" style="right:40px;bottom:46px;width:760px;text-align:right;font-weight:800;font-size:96px;line-height:1.02;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.35)">Crying With<br>an Accent?!</div>`;
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
const f = path.join(HERE, "cache", "pages", "thumb_babycry.html");
(await import("node:fs")).writeFileSync(f, html);
await p.goto(pathToFileURL(f).href);
await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, "out", "brand", "thumbP_babycry.png") });
await b.close();
console.log("out/brand/thumbP_babycry.png");
