// Projects the US states east of the Rockies into a 1920x1080 frame for the route map card (Krug's run, 1942).
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
// Centered so Detroit, New York and San Antonio all fit below the card header.
const cLon = -86.3, cLat = 36.4, spanLon = 43.9;
const k = Math.cos((cLat * Math.PI) / 180);
const W = 1920, H = 1080;
const s = W / (spanLon * k);
const P = ([lon, lat]) => [(W / 2 + (lon - cLon) * k * s).toFixed(1), (H / 2 + (cLat - lat) * s).toFixed(1)];
const ring = (r) => "M" + r.map((p) => P(p).join(",")).join("L") + "Z";
const skip = ["Alaska", "Hawaii", "Puerto Rico", "Guam", "American Samoa", "Commonwealth of the Northern Mariana Islands", "United States Virgin Islands"];
const res = { states: [], highlight: "Michigan", places: {}, labels: [] };
for (const f of states) {
  if (skip.includes(f.properties.name)) continue;
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  res.states.push({ name: f.properties.name, d: polys.map((p) => p.map(ring).join("")).join("") });
}
const places = { Detroit: [-83.05, 42.33], Chicago: [-87.63, 41.88], "New York": [-74.0, 40.71], Pittsburgh: [-80.0, 40.44],
  Nashville: [-86.78, 36.16], Dallas: [-96.8, 32.78], "San Antonio": [-98.49, 29.42], Laredo: [-99.51, 27.53], Philadelphia: [-75.17, 39.95], Cincinnati: [-84.51, 39.1] };
for (const [n, c] of Object.entries(places)) res.places[n] = P(c).map(Number);
for (const [text, c] of [["MEXICO", [-103.8, 29.2]], ["CANADA", [-80.5, 44.6]], ["TEXAS", [-100.5, 32.0]]]) {
  const [x, y] = P(c).map(Number);
  res.labels.push({ text, x, y });
}
fs.writeFileSync(out, JSON.stringify(res));
console.log(res.states.length, "states", res.places);
