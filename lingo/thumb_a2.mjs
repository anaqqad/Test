// Thumbnail for the A2 skit -> out/brand/thumb_a2usa.png
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { character } from "./art.mjs";
import { setting } from "./skit_art.mjs";
import { SKIT } from "./skit_a2.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const font = [800].map((w) => `<link rel="stylesheet" href="${pathToFileURL(path.join(HERE, `node_modules/@fontsource/montserrat/${w}.css`)).href}">`).join("");
const html = `<!doctype html><meta charset="utf-8">${font}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat}.a{position:absolute}.a>svg{width:100%;height:100%}</style>
<div class="a" style="left:-20px;top:-20px;width:1320px;height:760px">${setting("barber")}</div>
<div class="a" style="inset:0;background:linear-gradient(90deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.6) 62%)"></div>
<div class="a" style="left:20px;top:110px;width:520px;height:740px">${character({ ...SKIT.sami, hair: "bald", expression: "sad" }, "t")}</div>
<div class="a" style="left:370px;top:150px;font-size:110px">💦</div>
<div class="a" style="left:560px;top:110px;width:690px;text-align:center">
<div style="font-weight:800;font-size:96px;line-height:1;color:#fff;text-shadow:${[-4, 0, 4].flatMap((x) => [-4, 0, 4].map((y) => `${x}px ${y}px 0 #000`)).join(",")},0 9px 0 #000">A2 ENGLISH<br>IN THE USA</div>
<div style="display:inline-block;margin-top:28px;background:#e74c3c;color:#fff;font-weight:800;font-size:58px;padding:8px 30px;border-radius:18px;box-shadow:0 8px 0 rgba(0,0,0,.5)">"YES. THANK YOU."</div></div>`;
const f = path.join(HERE, "cache", "pages", "thumb_a2.html");
fs.writeFileSync(f, html);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready);
await p.screenshot({ path: path.join(HERE, "out", "brand", "thumb_a2usa.png") });
await b.close();
