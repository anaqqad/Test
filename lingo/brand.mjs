// Channel art + thumbnails: node brand.mjs -> out/brand/*.png
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character, scene } from "./art.mjs";
import { VIDEOS } from "./videos.mjs";
import { logoSvg } from "./render.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out", "brand");
fs.mkdirSync(OUT, { recursive: true });
const font = [700, 800].map((w) => `<link rel="stylesheet" href="${pathToFileURL(path.join(HERE, `node_modules/@fontsource/montserrat/${w}.css`)).href}">`).join("");
const flag = (c, h) => c && fs.existsSync(path.join(HERE, `node_modules/flag-icons/flags/4x3/${c}.svg`)) ? `<img style="height:${h}px;border-radius:8px;box-shadow:0 4px 14px rgba(0,0,0,.4)" src="${pathToFileURL(path.join(HERE, `node_modules/flag-icons/flags/4x3/${c}.svg`)).href}">` : "";
const css = `*{margin:0;padding:0;box-sizing:border-box}body{font-family:Montserrat,sans-serif;overflow:hidden}.abs{position:absolute}`;

const pages = {
  avatar: [800, 800, `<body style="background:radial-gradient(circle at 40% 35%,#3a3f78,#0d1024)"><div class="abs" style="left:110px;top:150px">
    <svg width="580" height="500" viewBox="0 0 160 140"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffcf5c"/><stop offset="1" stop-color="#ff6b5c"/></linearGradient></defs>
    <path d="M20 10 h120 a16 16 0 0 1 16 16 v66 a16 16 0 0 1 -16 16 h-70 l-30 26 v-26 h-20 a16 16 0 0 1 -16 -16 v-66 a16 16 0 0 1 16 -16z" fill="url(#g)"/>
    <text x="80" y="82" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="58" fill="#16182b">LD</text></svg></div></body>`],
  banner: [2560, 1440, `<body><div class="abs" style="inset:0">${scene("faroe", "banner")}</div><div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(10,12,30,.15),rgba(10,12,30,.75) 30%,rgba(10,12,30,.75) 70%,rgba(10,12,30,.15))"></div>
    <div class="abs" style="left:0;width:2560px;top:560px;text-align:center">${logoSvg(150)}<div style="color:#fff;font-weight:700;font-size:44px;margin-top:18px;letter-spacing:1px">Rare, endangered &amp; weird languages of the world</div></div></body>`],
};
const thumbs = {
  extinct: ["NEARLY EXTINCT", "HEAR THEM NOW", 1, "#d1495b"],
  niche: ["INSANELY NICHE", "WHO SPEAKS THIS?", 5, "#2a9d8f"],
  hardest: ["HARDEST LANGUAGES", "RANKED", 17, "#ff9500"],
  sounds: ["WEIRDEST SOUNDS", "😳", 0, "#8e44ad"],
  conlangs: ["MADE-UP LANGUAGES", "REAL SPEAKERS", 2, "#6c5ce7"],
  revived: ["BACK FROM THE DEAD", "REVIVED", 0, "#2a9d8f"],
  soundlike: ["THIS ISN'T ARABIC?!", "🤔", 0, "#ff9500"],
};
for (const [k, [t1, t2, i, col]] of Object.entries(thumbs)) {
  const it = VIDEOS[k].items[i];
  const bg = it.scene ? scene(it.scene, it.name) : `<div style="width:100%;height:100%;background:radial-gradient(circle at 30% 50%,#5a2a10,#0b0f1a 70%)"></div>`;
  pages["thumb_" + k] = [1280, 720, `<body><div class="abs" style="left:-20px;top:-20px;width:1320px;height:760px">${bg}</div>
    <div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(0,0,0,0) 30%,rgba(0,0,0,.65) 60%)"></div>
    <div class="abs" style="left:-10px;top:80px;width:560px;height:806px">${character(it.char, "t")}</div>
    <div class="abs" style="left:560px;top:120px;width:690px;text-align:center">
      <div style="margin-bottom:22px">${flag(it.flag, 80)}</div>
      <div style="font-weight:800;font-size:92px;line-height:.98;color:#fff;text-shadow:-4px -4px 0 #000,-4px 0px 0 #000,-4px 4px 0 #000,0px -4px 0 #000,0px 4px 0 #000,4px -4px 0 #000,4px 0px 0 #000,4px 4px 0 #000,0 9px 0 #000,0 0 40px rgba(0,0,0,.6)">${t1}</div>
      <div style="display:inline-block;margin-top:26px;background:${col};color:#fff;font-weight:800;font-size:64px;padding:8px 34px;border-radius:18px;box-shadow:0 8px 0 rgba(0,0,0,.5)">${t2}</div></div>
    </body>`];
}
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const [name, [w, h, body]] of Object.entries(pages)) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const f = path.join(HERE, "cache", "pages", `brand_${name}.html`);
  fs.writeFileSync(f, `<!doctype html><meta charset="utf-8">${font}<style>${css} svg{display:block}.abs>svg{width:100%;height:100%}</style>${body}`);
  await page.goto(pathToFileURL(f).href);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  await page.close();
}
await browser.close();
console.log("brand ->", OUT);
