// Beluga-style thumbnail for chat comedies (Blueprint 03): node thumb_chat.mjs <episode> -> out/brand/thumbC_<episode>.png
// One huge chat message + "X is typing..." cliffhanger + a big reaction Wojak + the channel's red hook (white outline).
import fs from "node:fs"; import path from "node:path"; import { execFileSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url"; import { chromium } from "playwright-core";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const key = process.argv[2];
const T = {
  class: { who: { name: "diego", color: "#f2f3f5", avatar: "wojaks/s_spa.png", bg: "#a83b3b" }, text: "i am so <span class='hl'>embarazada</span> 😳",
           typing: "Ms. Parker", react: "wojaks/sl2_gla.png", hook: ["PREGNANT?!"] },
}[key];
if (!T) throw new Error("no thumbnail spec for " + key);
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const trimmed = path.join(HERE, "cache", "pages", `wjc_${key}.png`);
execFileSync("convert", [path.join(HERE, T.react), "-trim", "+repage", trimmed]);
const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const html = `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${url("node_modules/@fontsource/montserrat/800.css")}"><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1280px;height:720px;overflow:hidden;background:#0b0b0c;font-family:Inter,"Noto Color Emoji",sans-serif}
.band{position:absolute;left:0;top:175px;width:1280px;background:#36383e}
.row{display:flex;gap:26px;padding:26px 34px 22px}
.av{flex:0 0 150px;height:150px;border-radius:50%;overflow:hidden;background:${T.who.bg}}.av img{width:100%;height:100%;object-fit:cover;object-position:50% 8%;transform:scale(1.35);transform-origin:50% 0}
.hd{font-size:52px;font-weight:600;color:${T.who.color}}.hd span{font-size:32px;color:#949ba4;font-weight:500;margin-left:14px}
.tx{font-size:90px;color:#e6e7ea;line-height:1.15;white-space:nowrap}.hl{color:#fff;font-weight:700}
.ty{background:#303237;padding:10px 34px 14px 40px;font-size:36px;color:#b5bac1;display:flex;align-items:center;gap:14px}
.ty b{color:#fff}.ty i{display:inline-block;width:14px;height:14px;border-radius:50%;background:#7d828a;margin-right:6px}.ty i:last-of-type{background:#f2f3f5}
.react{position:absolute;right:10px;bottom:0;height:300px}
.hook{position:absolute;left:40px;top:28px;font:800 118px Montserrat;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.5)}
</style>
<div class="band"><div class="row"><div class="av"><img src="${url(T.who.avatar)}"></div><div><div class="hd">${T.who.name}<span>Today at 8:05 AM</span></div><div class="tx">${T.text}</div></div></div>
<div class="ty"><span><i></i><i></i><i></i></span><span><b>${T.typing}</b> is typing...</span></div></div>
<img class="react" src="${pathToFileURL(trimmed).href}">
<div class="hook">${T.hook.join("<br>")}</div>`;
const f = path.join(HERE, "cache", "pages", `thumbC_${key}.html`); fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
const out = path.join(HERE, "out", "brand", `thumbC_${key}.png`); await p.screenshot({ path: out }); await b.close(); console.log(out);
