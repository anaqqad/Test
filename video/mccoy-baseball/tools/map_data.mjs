// Projects US states around Illinois into a 1920x1080 frame for the route map card.
// Output: remotion/src/data/map.json {states: [{name, d}], places: {name: [x, y]}}
import fs from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(process.cwd() + "/"); // run from remotion/
const topo = require("topojson-client");
const [src, out] = process.argv.slice(2);
const us = JSON.parse(fs.readFileSync(src, "utf8"));
const states = topo.feature(us, us.objects.states).features;
// Centered on northern Illinois so Washington, Peoria and Chicago sit well apart.
const cLon = -88.3, cLat = 41.47, spanLon = 7.4;
const k = Math.cos((cLat * Math.PI) / 180);
const W = 1920, H = 1080;
const s = W / (spanLon * k);
const P = ([lon, lat]) => [(W / 2 + (lon - cLon) * k * s).toFixed(1), (H / 2 + (cLat - lat) * s).toFixed(1)];
const ring = (r) => "M" + r.map((p) => P(p).join(",")).join("L") + "Z";
const keep = ["Illinois", "Indiana", "Wisconsin", "Iowa", "Missouri", "Kentucky", "Michigan", "Ohio", "Tennessee", "Minnesota", "Arkansas", "Kansas", "Nebraska"];
const res = { states: [], places: {} };
for (const f of states) {
  if (!keep.includes(f.properties.name)) continue;
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  res.states.push({ name: f.properties.name, d: polys.map((p) => p.map(ring).join("")).join("") });
}
const places = { Chicago: [-87.63, 41.88], Peoria: [-89.59, 40.69], "Washington, Ill.": [-89.41, 40.70], "Camp Grant": [-89.09, 42.24], "Camp Ellis": [-90.32, 40.37], "Lake Michigan": [-87.25, 42.75] };
for (const [n, c] of Object.entries(places)) res.places[n] = P(c).map(Number);
fs.writeFileSync(out, JSON.stringify(res));
console.log(res.states.length, "states", res.places);
