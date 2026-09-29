// Equirectangular textures for the Blender globe: base map + empire mask (4096x2048).
import fs from "node:fs";
import * as d3 from "d3-geo";
import * as topo from "topojson-client";
const W = 4096, H = 2048;
const world = JSON.parse(fs.readFileSync("countries-50m.json"));
const land = topo.merge(world, world.objects.countries.geometries);
const proj = d3.geoEquirectangular().scale(W / (2 * Math.PI)).translate([W / 2, H / 2]);
const path = d3.geoPath(proj);
let ring = [[27, 46.5], [28, 50], [30, 53], [33, 57], [38, 59], [48, 60], [58, 61], [65, 60], [75, 58], [85, 57], [95, 56],
  [105, 55], [115, 54], [125, 53], [132, 50], [135, 47], [131, 43], [129.5, 41], [129.5, 35], [126, 34], [122, 30], [121, 25],
  [117, 23], [111, 20.5], [108, 21.5], [104, 22.5], [100, 21.5], [98, 24], [97, 28], [93, 28], [88, 28], [82, 30], [78, 32],
  [74, 34], [71, 33], [69, 30], [66, 26], [61, 25], [57, 26], [54, 27], [50, 30], [48, 30], [45, 33], [42, 34], [40, 36.5],
  [36, 36.8], [32, 37.5], [29, 40.5], [33, 42], [37, 44], [40, 43], [38, 46], [33, 45], [30, 46], [27, 46.5]];
let empire = { type: "Polygon", coordinates: [ring] };
if (d3.geoArea(empire) > 2 * Math.PI) empire = { type: "Polygon", coordinates: [ring.slice().reverse()] };
const grat = d3.geoGraticule().step([15, 15])();
const page = (svg) => `<!doctype html><style>html,body{margin:0}</style><svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${svg}</svg>`;
fs.writeFileSync("globe_base.html", page(`
  <defs><clipPath id="l"><path d="${path(land)}"/></clipPath></defs>
  <rect width="${W}" height="${H}" fill="#1f4152"/>
  <path d="${path(grat)}" fill="none" stroke="#9cc3cf" stroke-opacity=".18" stroke-width="3"/>
  <path d="${path(land)}" fill="#e9dcbd" stroke="#7d6c4c" stroke-width="3"/>
  <g clip-path="url(#l)"><path d="${path(empire)}" fill="#b3261e"/></g>
  <path d="${path(empire)}" fill="none" stroke="#5e0f0b" stroke-width="6" clip-path="url(#l)"/>`));
fs.writeFileSync("globe_mask.html", page(`
  <defs><clipPath id="l"><path d="${path(land)}"/></clipPath></defs>
  <rect width="${W}" height="${H}" fill="#000"/>
  <g clip-path="url(#l)"><path d="${path(empire)}" fill="#fff" stroke="#fff" stroke-width="6"/></g>`));
fs.writeFileSync("globe_plain.html", page(`
  <rect width="${W}" height="${H}" fill="#1f4152"/>
  <path d="${path(grat)}" fill="none" stroke="#9cc3cf" stroke-opacity=".18" stroke-width="3"/>
  <path d="${path(land)}" fill="#e9dcbd" stroke="#7d6c4c" stroke-width="3"/>`));
console.log("ok");
