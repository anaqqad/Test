// Thumbnail for "Why Arabs Can't Understand Each Other" (owner's idea): a Moroccan and an Algerian greet each
// other with "Labas?", while Egyptian, Syrian and Iraqi Wojaks look confused. Channel look kept: white name strip,
// photo, Wojaks, flags, red hook with a white outline. node thumb_arabic.mjs -> out/brand/thumbP_arabic.png
import fs from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const css = ["montserrat/700.css", "montserrat/800.css"].map((f) => `<link rel="stylesheet" href="${url("node_modules/@fontsource/" + f)}">`).join("");
export const PHOTO_CREDIT = "Medina of Fes, Morocco: photo by Petar Milošević, CC BY-SA 4.0, via Wikimedia Commons";
const trim = (k) => { const t = path.join(HERE, "cache", "pages", `wj_${k}.png`); execFileSync("convert", [path.join(HERE, "wojaks", `${k}.png`), "-trim", "+repage", t]); return pathToFileURL(t).href; };
const flag = (c) => url(`node_modules/flag-icons/flags/4x3/${c}.svg`);
const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const bubble = (x, y, text, code, tail) => `<div class="a bub" style="left:${x}px;top:${y}px"><span class="fl" style="background-image:url('${flag(code)}')"></span>${text}<i class="tail ${tail}"></i></div>`;
const confused = (k, code, x) => `<div class="a" style="left:${x}px;top:0;width:190px;height:262px;overflow:hidden">
  <img src="${trim(k)}" style="position:absolute;left:5px;bottom:0;width:180px;height:205px;object-fit:contain;object-position:center bottom">
  <div class="a q">???</div><span class="a fl2" style="background-image:url('${flag(code)}')"></span></div>`;
const html = `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:#000}.a{position:absolute}
.bub{background:#fff;border:5px solid #111;border-radius:26px;padding:8px 22px 10px 14px;font-weight:800;font-size:50px;color:#111;display:flex;align-items:center;gap:12px;box-shadow:0 8px 18px rgba(0,0,0,.45)}
.fl{display:inline-block;width:66px;height:44px;background-size:cover;border:2px solid #111;border-radius:4px}
.tail{position:absolute;bottom:-26px;width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-top:26px solid #111}.tail.l{left:40px}.tail.r{right:40px}
.q{left:0;right:0;top:4px;text-align:center;font-weight:800;font-size:46px;color:#fff;text-shadow:${stroke(4, "#111")}}
.fl2{left:8px;bottom:8px;width:54px;height:36px;background-size:cover;border:3px solid #fff;border-radius:4px;box-shadow:0 3px 8px rgba(0,0,0,.5)}</style>
<div class="a" style="inset:0;background:url('${url("cache/photos/arabic.jpg")}') 50% 50%/cover"></div>
<div class="a" style="inset:0;background:linear-gradient(90deg,rgba(0,0,0,.05),rgba(0,0,0,.25))"></div>
<div class="a" style="left:0;top:0;width:1280px;height:78px;background:#fff;text-align:center;font-weight:700;font-size:50px;line-height:80px;color:#111">Arabic</div>
<img class="a" src="${trim("th_mar")}" style="left:-10px;bottom:0;height:440px;max-width:360px;object-fit:contain;object-position:left bottom">
<img class="a" src="${trim("th_alg")}" style="left:300px;bottom:0;height:440px;max-width:360px;object-fit:contain;object-position:right bottom">
${bubble(24, 120, "Labas?", "ma", "l")}${bubble(330, 205, "Labas!", "dz", "r")}
<div class="a" style="left:676px;top:100px;width:588px;height:262px;background:rgba(255,255,255,.92);border:5px solid #111;border-radius:22px;box-shadow:0 8px 18px rgba(0,0,0,.45);overflow:hidden">${confused("th_egy_conf", "eg", 0)}${confused("th_syr_conf", "sy", 196)}${confused("th_irq_conf", "iq", 392)}</div>
<div class="a" style="right:34px;bottom:50px;width:700px;text-align:right;font-weight:800;font-size:88px;line-height:1.02;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45)">Can’t<br>Understand?!</div>`;
const f = path.join(HERE, "cache", "pages", "thumbP_arabic.html");
fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
await p.screenshot({ path: path.join(HERE, "out", "brand", "thumbP_arabic.png") });
await b.close();
console.log("out/brand/thumbP_arabic.png");
