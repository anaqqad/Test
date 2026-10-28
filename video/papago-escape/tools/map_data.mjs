// Projects US states around southern Arizona into a 1920x1080 frame for the route map card.
// Usage (from remotion/): node ../tools/map_data.mjs ../build/states-10m.json src/data/map.json
// states-10m.json: https://cdn.jsdelivr.net/npm/us-atlas@3.0.1/states-10m.json
// Output: {states: [{name, d}], highlight, places: {name: [x, y]}, labels: [{text, x, y}]}
import fs from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(process.cwd() + "/"); // run from remotion/
const topo = require("topojson-client");
const [src, out] = process.argv.slice(2);
const us = JSON.parse(fs.readFileSync(src, "utf8"));
const states = topo.feature(us, us.objects.states).features;
// Centered between Phoenix and the head of the Gulf of California so the whole planned route fits.
const cLon = -113.63, cLat = 32.75, spanLon = 6.02;
const k = Math.cos((cLat * Math.PI) / 180);
const W = 1920, H = 1080;
const s = W / (spanLon * k);
const P = ([lon, lat]) => [(W / 2 + (lon - cLon) * k * s).toFixed(1), (H / 2 + (cLat - lat) * s).toFixed(1)];
const ring = (r) => "M" + r.map((p) => P(p).join(",")).join("L") + "Z";
const keep = ["Arizona", "California", "Nevada", "Utah", "New Mexico"];
const res = { states: [], highlight: "Arizona", places: {}, labels: [] };
for (const f of states) {
  if (!keep.includes(f.properties.name)) continue;
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  res.states.push({ name: f.properties.name, d: polys.map((p) => p.map(ring).join("")).join("") });
}
const places = { "Papago Park": [-111.94, 33.46], "Gila Bend": [-112.72, 32.95], Yuma: [-114.62, 32.69], "Gulf of California": [-114.75, 31.75] };
for (const [n, c] of Object.entries(places)) res.places[n] = P(c).map(Number);
for (const [text, c] of [["ARIZONA", [-111.0, 32.4]], ["MEXICO", [-113.0, 31.75]], ["CALIFORNIA", [-115.8, 33.3]]]) {
  const [x, y] = P(c).map(Number);
  res.labels.push({ text, x, y });
}
fs.writeFileSync(out, JSON.stringify(res));
console.log(res.states.length, "states", res.places);
