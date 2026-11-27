// Beluga-style thumbnail for chat comedies (Blueprint 03): node thumb_chat.mjs <episode> -> out/brand/thumbC_<episode>.png
// Like the reference thumbnails: two chat messages filling the frame (the setup, then the punchline reply), big avatars,
// the key mention highlighted, no other text.
import fs from "node:fs"; import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url"; import { chromium } from "playwright-core";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const key = process.argv[2];
const SPECS = {
  class: {
    time: "8:05 AM",
    msgs: [
      { name: "diego", color: "#f2f3f5", avatar: "wojaks/s_spa.png", bg: "#a83b3b", text: "i am so embarazada 😳" },
      { name: "Ms. Parker", color: "#f0b232", avatar: "wojaks/sl2_gla.png", bg: "#6b4f2f", text: "<span class='men'>@diego</span> ..." },
    ],
  },
};
const T = SPECS[key];
if (!T) throw new Error("no thumbnail spec for " + key + " (add one to SPECS in thumb_chat.mjs)");
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const msg = (m) => `<div class="m"><div class="av" style="background:${m.bg}"><img src="${url(m.avatar)}"></div>
  <div><div class="hd"><b style="color:${m.color}">${m.name}</b><span>${T.time}</span></div><div class="tx">${m.text}</div></div></div>`;
const html = `<!doctype html><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1280px;height:720px;overflow:hidden;background:#36383e;font-family:Inter,"Noto Color Emoji",sans-serif;display:flex;align-items:center}
.band{width:1280px;height:720px;background:#36383e;padding:30px 36px;display:flex;flex-direction:column;justify-content:center;gap:70px}
.m{display:flex;gap:30px;align-items:flex-start}
.av{flex:0 0 196px;height:196px;border-radius:50%;overflow:hidden}
.av img{width:100%;height:100%;object-fit:cover;object-position:50% 8%;transform:scale(1.35);transform-origin:50% 0}
.hd{display:flex;align-items:baseline;gap:18px;margin-top:4px}.hd b{font-size:74px;font-weight:700}.hd span{font-size:46px;color:#949ba4;font-weight:500}
.tx{font-size:86px;color:#e6e7ea;line-height:1.2;white-space:nowrap}
.men{color:#f6d36b;background:rgba(240,178,50,.25);border-radius:8px;padding:0 8px;font-weight:600}
</style><div class="band">${T.msgs.map(msg).join("")}</div>`;
const f = path.join(HERE, "cache", "pages", `thumbC_${key}.html`); fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
const out = path.join(HERE, "out", "brand", `thumbC_${key}.png`); await p.screenshot({ path: out }); await b.close(); console.log(out);
