// Download elevation tiles (AWS Terrain Tiles, "terrarium" PNG encoding) covering a video's map bounds into
// public/terrain/<id>/, for the hillshaded relief. Run once per video: node scripts/fetch-terrain.mjs <video-id>
// Attribution (put it in the description): Terrain Tiles by Mapzen/Tilezen on AWS Open Data, from SRTM, GMTED2010,
// ETOPO1 and EU-DEM (Copernicus).
import fs from "node:fs";
import path from "node:path";

const id = process.argv[2];
const video = JSON.parse(fs.readFileSync(`data/videos/${id}.json`, "utf8"));
const [[w0, s0], [e0, n0]] = video.map.bounds;
// The camera can show beyond the bounds; the vertical Short shows ~1.8x the width in height.
const latMid = ((s0 + n0) / 2) * (Math.PI / 180);
const padX = (e0 - w0) * 0.35;
const padY = Math.max((n0 - s0) * 0.35, ((e0 - w0) * Math.cos(latMid) * 1.8 - (n0 - s0)) / 2 + 0.3);
const w = w0 - padX, e = e0 + padX, s = Math.max(-80, s0 - padY), n = Math.min(80, n0 + padY);

// One tile pixel per ~1.5 output pixels at zoom 1 is plenty for a hillshade.
const pxPerDeg = 2400 / (e0 - w0) / 1.5;
let z = Math.max(3, Math.min(10, Math.round(Math.log2((pxPerDeg * 360) / 256))));
const tx = (lon) => Math.floor(((lon + 180) / 360) * 2 ** z);
const ty = (lat) => Math.floor(((1 - Math.log(Math.tan((lat * Math.PI) / 180) + 1 / Math.cos((lat * Math.PI) / 180)) / Math.PI) / 2) * 2 ** z);
while ((tx(e) - tx(w) + 1) * (ty(s) - ty(n) + 1) > 400) z--;
const x0 = tx(w), x1 = tx(e), y0 = ty(n), y1 = ty(s);

const dir = path.join("public", "terrain", id);
fs.mkdirSync(dir, { recursive: true });
let n_ = 0;
for (let y = y0; y <= y1; y++)
  for (let x = x0; x <= x1; x++) {
    const file = path.join(dir, `${z}-${x}-${y}.png`);
    if (fs.existsSync(file)) continue;
    const res = await fetch(`https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${z}/${x}/${y}.png`);
    if (!res.ok) throw new Error(`tile ${z}/${x}/${y}: ${res.status}`);
    fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
    n_++;
  }
fs.writeFileSync(path.join(dir, "manifest.json"), JSON.stringify({ z, x0, x1, y0, y1 }));
console.log(`zoom ${z}, ${(x1 - x0 + 1) * (y1 - y0 + 1)} tiles (${n_} downloaded) -> ${dir}`);
