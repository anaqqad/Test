// Channel-look thumbnail with two characters facing each other (white name strip, photo, flag, red hook):
//   node thumb_duo.mjs <key> -> out/brand/thumbD_<key>.png
import fs from "node:fs"; import path from "node:path"; import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url"; import { chromium } from "playwright-core";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const key = process.argv[2];
const SPECS = {
  class: { name: "English Class", photo: "class", pos: "50% 40%", flag: "es",
           left: { wojak: "wojaks/s_spa.png", say: "i am embarazada 😳" },
           right: { wojak: "wojaks/sl2_gla_shock.png", hook: "DIEGO?!", flip: true } },
};
export const PHOTO_CREDITS = { class: "Classroom in the U.S.: photo by Marie from Malang, East Java, CC BY-SA 2.0, via Wikimedia Commons" };
const T = SPECS[key]; if (!T) throw new Error("no spec for " + key);
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const trim = (p, n) => { const o = path.join(HERE, "cache", "pages", `duo_${key}_${n}.png`); execFileSync("convert", [path.join(HERE, p), "-trim", "+repage", o]); return pathToFileURL(o).href; };
const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const html = `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${url("node_modules/@fontsource/montserrat/700.css")}"><link rel="stylesheet" href="${url("node_modules/@fontsource/montserrat/800.css")}"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat,"Noto Color Emoji";background:#000}
.a{position:absolute}
.photo{inset:0;background:url('${url("cache/photos/" + T.photo + ".jpg")}') ${T.pos}/cover;filter:brightness(.9)}
.strip{left:0;top:0;width:1280px;height:78px;background:#fff;text-align:center;font-weight:700;font-size:50px;line-height:80px;color:#111}
.flag{left:50%;top:104px;transform:translateX(-50%);width:170px;height:113px;background:url('${url("node_modules/flag-icons/flags/4x3/" + T.flag + ".svg")}') center/cover;box-shadow:0 6px 18px rgba(0,0,0,.45)}
.wl{left:90px;bottom:0;height:500px}.wr{right:-30px;bottom:0;height:560px;transform:scaleX(${T.right.flip ? -1 : 1})}
.bubble{left:170px;top:112px;background:#fff;color:#111;font:700 46px Inter,"Noto Color Emoji";padding:18px 28px;border-radius:28px;box-shadow:0 8px 22px rgba(0,0,0,.45);white-space:nowrap}
.bubble::after{content:"";position:absolute;left:160px;bottom:-26px;border:16px solid transparent;border-top:26px solid #fff;border-left:22px solid #fff}
.hook{right:190px;top:520px;font-weight:800;font-size:104px;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45);white-space:nowrap}
</style>
<div class="a photo"></div><div class="a strip">${T.name}</div>
<img class="a wl" src="${trim(T.left.wojak, "l")}"><img class="a wr" src="${trim(T.right.wojak, "r")}">
<div class="a bubble">${T.left.say}</div><div class="a hook">${T.right.hook}</div>`;
const f = path.join(HERE, "cache", "pages", `thumbD_${key}.html`); fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
const out = path.join(HERE, "out", "brand", `thumbD_${key}.png`); await p.screenshot({ path: out }); await b.close(); console.log(out);
