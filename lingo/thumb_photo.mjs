// Photo-style thumbnails (white name strip, real landscape photo, meme-style character, flag, red hook):
// node thumb_photo.mjs [key ...] -> out/brand/thumbP_<key>.png. Photos are free-licence Wikimedia Commons
// files in cache/photos; their credits are in PHOTO_CREDITS below and go into the video description.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import { wojak } from "./art.mjs";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const url = (p) => pathToFileURL(path.join(HERE, p)).href;
const css = ["montserrat/700.css", "montserrat/800.css"].map((f) => `<link rel="stylesheet" href="${url("node_modules/@fontsource/" + f)}">`).join("");

export const PHOTO_CREDITS = {
  giza: "Pyramids of Giza: photo by Kallerna, CC BY-SA 3.0, via Wikimedia Commons",
  persepolis: "Persepolis: photo by Carole Raddato, CC BY-SA 2.0, via Wikimedia Commons",
  skellig: "Skellig Michael: photo by Jerzy Strzelecki, CC BY-SA 3.0, via Wikimedia Commons",
  bamburgh: "Bamburgh Castle: photo by mattbuck, CC BY-SA 4.0, via Wikimedia Commons",
  sounds: "Transkei, South Africa: photo by Michael Wittwer, CC BY-SA 4.0, via Wikimedia Commons",
  niche: "Khandagayty, Tuva: photo by AntonovAlexandr, CC BY-SA 3.0, via Wikimedia Commons",
  conlangs: "Old Town Market Square, Warsaw: photo by Rhododendrites, CC BY-SA 4.0, via Wikimedia Commons",
  extinct: "Terraced hills of Dhading, Nepal: photo by Everhard van Eimeren, CC BY-SA 4.0, via Wikimedia Commons",
  soundlike: "Valletta from the Grand Harbour: photo by Martin Furtschegger, CC BY 3.0, via Wikimedia Commons",
  a2usa: "Times Square: photo by Jerry Steinfield, CC BY-SA 4.0, via Wikimedia Commons",
  revived: "Jerusalem Old City: photo by Nettadi, CC BY-SA 3.0, via Wikimedia Commons",
  ancient4: "Saona Island: photo by Danu Widjajanto, CC BY-SA 4.0, via Wikimedia Commons",
  ancient5: "Newfoundland landscape: photo by Chris Scott, CC BY 3.0, via Wikimedia Commons",
  whistled: "Valle Gran Rey, La Gomera: photo by Llez, CC BY-SA 3.0, via Wikimedia Commons",
  similar: "Guadiana International Bridge (Spain-Portugal): photo by Curimedia, CC BY 2.0, via Wikimedia Commons",
  ancient6: "Mongolian steppes: photo by Francisco Anzola, CC BY 2.0, via Wikimedia Commons",
};
// Esperanto has its own flag, not in flag-icons: green field, white canton with a green star
const EO = "data:image/svg+xml;utf8," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400"><rect width="600" height="400" fill="#009900"/><rect width="200" height="200" fill="#fff"/><path d="M100 30 L118 82 L173 82 L128 114 L145 166 L100 134 L55 166 L72 114 L27 82 L82 82Z" fill="#009900"/></svg>');

const T = {
  ancient: { part: "PART 1", name: "Ancient Egyptian", photo: "giza", pos: "50% 60%", flag: "eg", hook: ["Unheard for", "4,000 Years"],
    who: { skin: "brown", hair: "long", hairColor: "black", fem: true, hat: { type: "headband", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "dress", color: "#f4f1e8", color2: "#d9b13b", trim: "#1f4e8c" }, earrings: "#d9b13b", expression: "neutral" } },
  ancient2: { part: "PART 2", name: "Old Persian", photo: "persepolis", pos: "50% 45%", flag: "ir", hook: ["Lost for", "2,500 Years"],
    who: { skin: "olive", hair: "long", hairColor: "black", beard: true, hat: { type: "crown", color: "#d9b13b", color2: "#1f4e8c" }, outfit: { type: "coat", color: "#5b2a6b", inner: "#d9b13b" }, expression: "neutral" } },
  ancient3: { part: "PART 3", name: "Old Irish", photo: "skellig", pos: "50% 50%", flag: "ie", hook: ["1,200", "Years Old"],
    who: { skin: "pale", hair: "short", hairColor: "auburn", outfit: { type: "wrap", color: "#6b4a2b", color2: "#3b2a16", trim: "#c8a165" }, expression: "neutral" } },
  english: { name: "Old English", photo: "bamburgh", pos: "50% 50%", flag: "gb-eng", hook: ["This Is", "English?!"],
    who: { skin: "pale", hair: "short", hairColor: "auburn", beard: true, beardColor: "#7a3b1c", outfit: { type: "tunic", color: "#2f5d3a", trim: "#c8a165" }, expression: "neutral" } },
  ancient4: { part: "PART 4", name: "Taíno", photo: "ancient4", pos: "50% 60%", flag: "do", hook: ["You Speak It", "Every Day"] },
  similar: { name: "Spanish vs Portuguese", photo: "similar", pos: "50% 50%", flag: "es", flag2: "pt", img: "wojaks/similar.png", hook: ["Same", "Language?!"] },
  whistled: { part: "PART 1", name: "Silbo Gomero", photo: "whistled", pos: "50% 50%", flag: "es", hook: ["NO", "WORDS"] },
  ancient5: { part: "PART 5", name: "Beothuk", photo: "ancient5", pos: "50% 50%", flag: "ca", hook: ["Not One", "Sentence Left"], hookSize: 86 },
  ancient6: { part: "PART 6", name: "Middle Mongolian", photo: "ancient6", pos: "50% 50%", flag: "mn", hook: ["Genghis Khan", "Spoke This"], hookSize: 86 },
  sounds: { name: "Xhosa", photo: "sounds", pos: "50% 50%", flag: "za", hook: ["Weirdest", "Sounds Ever"] },
  niche: { name: "Tuvan", photo: "niche", pos: "50% 50%", flag: "ru", hook: ["Who Speaks", "This?"] },
  conlangs: { name: "Esperanto", photo: "conlangs", pos: "50% 50%", flagUrl: EO, hook: ["Someone", "Invented It"] },
  extinct: { name: "Kusunda", photo: "extinct", pos: "50% 50%", flag: "np", hook: ["Almost", "Gone"] },
  soundlike: { name: "Maltese", photo: "soundlike", pos: "50% 50%", flag: "mt", hook: ["This Isn't", "Arabic?!"] },
  a2usa: { name: "A2 English", photo: "a2usa", pos: "50% 40%", flag: "us", hook: ["Yes.", "Thank You."] },
  revived: { name: "Hebrew", photo: "revived", pos: "50% 50%", flag: "il", hook: ["Back From", "the Dead"] },
};

const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const page = (t) => `<!doctype html><meta charset="utf-8">${css}<style>*{margin:0;padding:0}body{width:1280px;height:720px;overflow:hidden;font-family:Montserrat;background:#000}.a{position:absolute}.a>svg{width:100%;height:100%}</style>
<div class="a" style="inset:0;background:url('${url("cache/photos/" + t.photo + ".jpg")}') ${t.pos}/cover"></div>
<div class="a" style="left:0;top:0;width:1280px;height:78px;background:#fff;text-align:center;font-weight:700;font-size:50px;line-height:80px;color:#111">${t.name}</div>
${t.img ? `<img class="a" src="${url(t.img)}" style="left:0;bottom:0;height:560px;max-width:760px;object-fit:contain;object-position:left bottom">` : `<div class="a" style="left:-110px;top:40px;width:660px;height:950px">${wojak(t.who, "p")}</div>`}
${t.part ? `<div class="a" style="right:40px;top:328px;width:300px;text-align:center;background:#e8262b;color:#fff;font-weight:800;font-size:54px;padding:2px 0 6px;border:5px solid #fff;border-radius:12px;box-shadow:0 6px 18px rgba(0,0,0,.45)">${t.part}</div>` : ""}
${t.flag2 ? `<div class="a" style="right:360px;top:112px;width:300px;height:200px;background:url('${url("node_modules/flag-icons/flags/4x3/" + t.flag2 + ".svg")}') center/cover;box-shadow:0 6px 18px rgba(0,0,0,.45);border:5px solid #fff;border-radius:10px"></div>` : ""}
<div class="a" style="right:40px;top:112px;width:300px;height:200px;background:url('${t.flagUrl || url("node_modules/flag-icons/flags/4x3/" + t.flag + ".svg")}') center/${t.flag === "np" ? "contain no-repeat" : "cover"};${t.flag === "np" ? "box-shadow:none;" : ""}box-shadow:0 6px 18px rgba(0,0,0,.45)"></div>
<div class="a" style="right:40px;bottom:56px;width:720px;text-align:right;font-weight:800;font-size:${t.hookSize || 104}px;line-height:1.02;color:${t.hookColor || "#e8262b"};text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45)">${t.hook.join("<br>")}</div>`;

const keys = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(T);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
for (const k of keys) {
  // a character drawn elsewhere (e.g. made in ChatGPT, transparent PNG) wins over the built-in drawing
  const own = path.join(HERE, "wojaks", `${k}.png`);
  if (fs.existsSync(own)) T[k].img = pathToFileURL(own).href;
  const f = path.join(HERE, "cache", "pages", `thumbP_${k}.html`);
  fs.writeFileSync(f, page(T[k]));
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto(pathToFileURL(f).href); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
  await p.screenshot({ path: path.join(HERE, "out", "brand", `thumbP_${k}.png`) });
  await p.close();
  console.log(`out/brand/thumbP_${k}.png`);
}
await b.close();
