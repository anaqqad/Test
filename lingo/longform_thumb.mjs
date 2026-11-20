// Long-form thumbnails in the channel look (white name strip, flag, Wojak, red hook with white outline), one per
// title variant: node longform_thumb.mjs malta3 [A|B ...]  ->  out/brand/thumbL_<key>_<variant>.png
// Reads EP.thumbs = { A: { name, flag, wojak, tag, hook: [..], bubble, cam, fill, inset, marks: [[text, place, color]] } }.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";
import { spawnSync } from "node:child_process";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const key = process.argv[2];
const EP = (await import(pathToFileURL(path.join(HERE, "longform", key, "episode.mjs")).href)).default;
const nm = (p) => path.join(HERE, "node_modules", p), furl = (p) => pathToFileURL(p).href;
const S = 20000, proj = d3.geoMercator().scale(S).translate([0, 0]), pxPerDeg = S * Math.PI / 180;
const [bx0, by0] = proj([-30, 63]), [bx1, by1] = proj([55, 18]); proj.clipExtent([[bx0, by0], [bx1, by1]]);
const gp = d3.geoPath(proj).digits(1);
const w10 = JSON.parse(fs.readFileSync(nm("world-atlas/countries-10m.json"))), feats = topo.feature(w10, w10.objects.countries).features;
const w50 = JSON.parse(fs.readFileSync(nm("world-atlas/countries-50m.json"))), f50 = topo.feature(w50, w50.objects.countries).features;
const boxA = (bx1 - bx0) * (by1 - by0);
const inBox = (f) => { const [[a, b], [c, d]] = d3.geoBounds(f); return c > -32 && a < 57 && d > 16 && b < 65; };
const landD = f50.filter(inBox).filter((f) => gp.area(f) < boxA * 0.5).map((f) => gp(f) || "").join("");
const reg = (spec) => { const f = feats.find((x) => x.id === spec.id); if (!spec.near) return f; const polys = f.geometry.type === "MultiPolygon" ? f.geometry.coordinates : [f.geometry.coordinates];
  return { type: "MultiPolygon", coordinates: polys.filter((c) => d3.geoDistance(d3.geoCentroid({ type: "Polygon", coordinates: c }), spec.near) * 180 / Math.PI < spec.r) }; };
const REG = Object.fromEntries(Object.entries(EP.regions).map(([k, v]) => [k, gp(reg(v))]));
const fontCss = [nm("@fontsource/fraunces/800-italic.css"), nm("@fontsource/inter/800.css"), nm("@fontsource/montserrat/800.css")].map((f) => `<link rel="stylesheet" href="${furl(f)}">`).join("");
const TEX = path.join(HERE, "cache", "longform", "paper.png");
const tw = 1280, thh = 720;
const camT = (c, w, h) => { const [x, y] = proj(c.c); const z = w / (c.span * pxPerDeg); return { tr: `translate(${w / 2} ${h / 2}) scale(${z}) translate(${-x} ${-y})`, sp: (ll) => { const [px, py] = proj(ll); return [(px - x) * z + w / 2, (py - y) * z + h / 2]; } }; };
const fills = (f) => Object.entries(f).map(([k, c]) => `<path d="${REG[k]}" fill="${c}" stroke="rgba(60,30,20,.35)" stroke-width="1" vector-effect="non-scaling-stroke"/>`).join("");
const stroke = (w, c) => [...Array(16)].map((_, i) => { const a = (i / 16) * 2 * Math.PI; return `${(Math.cos(a) * w).toFixed(1)}px ${(Math.sin(a) * w).toFixed(1)}px 0 ${c}`; }).join(",");
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || "/opt/pw-browsers/chromium" });
for (const v of process.argv.slice(3).length ? process.argv.slice(3) : Object.keys(EP.thumbs)) {
  const th = EP.thumbs[v], IS = th.inset, M = camT(th.cam, tw, thh);
  const wj = path.join(HERE, "cache", "longform", key, `thumb_wj_${v}.png`); spawnSync("convert", [path.join(HERE, th.wojak), "-trim", "+repage", wj]);
  const marks = (th.marks || []).map(([txt, at, col, off = [0, 0]]) => { const [x0, y0] = M.sp(EP.places[at]), x = x0 + off[0], y = y0 + off[1]; return `<div class="a" style="left:${x}px;top:${y}px;transform:translate(-50%,-50%) rotate(-4deg);background:${col};border:4px solid #fff;border-radius:10px;padding:4px 14px;font:800 34px Inter;letter-spacing:.06em;color:#fff;box-shadow:0 6px 14px rgba(0,0,0,.45);white-space:nowrap">${txt}</div>`; }).join("");
  const page = `<!doctype html><meta charset="utf-8">${fontCss}<style>*{margin:0;padding:0}body{width:${tw}px;height:${thh}px;overflow:hidden;background:#174a63}
.a{position:absolute}#sea{position:absolute;inset:0;background:radial-gradient(ellipse at 60% 50%,#2a6d8c 0%,#21607e 45%,#163f55 100%)}
.m{filter:drop-shadow(0 3px 0 rgba(70,50,20,.28)) drop-shadow(0 8px 12px rgba(0,0,0,.28))}.h{filter:drop-shadow(2px 6px 0 rgba(40,20,10,.45)) drop-shadow(4px 12px 14px rgba(0,0,0,.4))}
#tex{position:absolute;inset:0;background:url(${furl(TEX)});background-size:800px;mix-blend-mode:multiply;opacity:.36}</style>
<div id="sea"></div>
<svg class="a m" style="inset:0" viewBox="0 0 ${tw} ${thh}"><g transform="${M.tr}"><path d="${landD}" fill="#e9dcbf" stroke="#c9b48e" stroke-width="1" vector-effect="non-scaling-stroke"/></g></svg>
<svg class="a h" style="inset:0" viewBox="0 0 ${tw} ${thh}"><g transform="${M.tr}">${fills(th.fill)}</g></svg>
<div id="tex"></div>${marks}
${IS ? `<div class="a" style="left:${IS.x - IS.r}px;top:${IS.y - IS.r}px;width:${IS.r * 2}px;height:${IS.r * 2}px;border-radius:50%;overflow:hidden;border:8px solid #fbf7ee;box-shadow:0 12px 30px rgba(0,0,0,.5);background:radial-gradient(#2a6d8c,#1c5672)">
 <svg class="a h" style="inset:0" viewBox="0 0 ${IS.r * 2} ${IS.r * 2}"><g transform="${camT(IS.cam, IS.r * 2, IS.r * 2).tr}">${fills({ malta: th.fill.malta })}</g></svg></div>` : ""}
${th.bubble ? `<div class="a" style="left:${IS.x + IS.bx}px;top:${IS.y + IS.by}px;background:#fbf7ee;border-radius:12px;padding:8px 18px;font:italic 800 46px Fraunces;color:#1c1712;box-shadow:0 8px 18px rgba(0,0,0,.45);white-space:nowrap">${th.bubble}</div>` : ""}
<div class="a" style="left:0;top:0;width:${tw}px;height:78px;background:#fff;text-align:center;font:800 50px/80px Montserrat;color:#111">${th.name}</div>
<div class="a" style="right:40px;top:112px;width:240px;height:160px;background:url('${furl(nm("flag-icons/flags/4x3/" + th.flag + ".svg"))}') center/cover;box-shadow:0 6px 18px rgba(0,0,0,.45)"></div>
<img class="a" src="${furl(wj)}" style="left:-30px;bottom:0;height:470px">
${th.tag ? `<div class="a" style="right:40px;bottom:268px;background:#d9533f;border-radius:8px;padding:6px 16px;font:800 30px Inter;letter-spacing:.08em;color:#fff;box-shadow:0 6px 14px rgba(0,0,0,.4)">${th.tag}</div>` : ""}
<div class="a" style="right:40px;bottom:46px;text-align:right;font:800 ${th.hookSize || 104}px/1.02 Montserrat;color:#e8262b;text-shadow:${stroke(7, "#fff")},0 10px 20px rgba(0,0,0,.45)">${th.hook.join("<br>")}</div>`;
  const f = path.join(HERE, "cache", "longform", key, `thumb_${v}.html`); fs.writeFileSync(f, page);
  const p = await b.newPage({ viewport: { width: tw, height: thh } });
  await p.goto(furl(f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  const out = path.join(HERE, "out", "brand", `thumbL_${key}_${v}.png`); await p.screenshot({ path: out }); await p.close(); console.log(out);
}
await b.close();
