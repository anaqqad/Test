// Builds theme/bhr/assets/map/world-110m.json: [[iso2, name, svgPath], ...] for the Global African History map.
// Data: Natural Earth 1:110m admin-0 countries (public domain), packaged as world-atlas@2.0.2 TopoJSON.
// Usage: node build_map.mjs <dir with node_modules: world-atlas@2.0.2 topojson-client@3 d3-geo@3 i18n-iso-countries@7> <out.json>
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import path from 'node:path';

const [modDir, out] = process.argv.slice(2);
const require = createRequire(path.join(path.resolve(modDir), 'index.js'));
const topo = require('world-atlas/countries-110m.json');
const { feature, merge } = require('topojson-client');
const d3 = require('d3-geo');
const iso = require('i18n-iso-countries');

const W = 960, H = 500;
// Owner decision (2026-10-15): Western Sahara (ISO 732) is drawn as part of Morocco (504), one shape, no inner border.
const MERGE = { '504': ['504', '732'] };
const geoms = topo.objects.countries.geometries;
const merged = new Set(Object.values(MERGE).flat());
let all = feature(topo, topo.objects.countries).features.filter((f) => f.properties.name !== 'Antarctica' && !merged.has(f.id));
for (const [id, parts] of Object.entries(MERGE)) {
  const shape = merge(topo, geoms.filter((g) => parts.includes(g.id)));
  const base = geoms.find((g) => g.id === id);
  all.push({ type: 'Feature', id, properties: base.properties, geometry: shape });
}
const projection = d3.geoNaturalEarth1().fitExtent([[4, 4], [W - 4, H - 4]], { type: 'FeatureCollection', features: all });
const pathGen = d3.geoPath(projection).digits(1);

const rows = [];
let missing = 0;
for (const f of all) {
  const code = f.id ? iso.numericToAlpha2(f.id) : undefined;
  // Kosovo and Northern Cyprus have no ISO numeric code in Natural Earth; they are drawn but not clickable.
  const iso2 = code ? code.toLowerCase() : '';
  if (!iso2) missing++;
  rows.push([iso2, f.properties.name, pathGen(f)]);
}
rows.sort((a, b) => a[1].localeCompare(b[1]));
writeFileSync(out, JSON.stringify({ viewBox: `0 0 ${W} ${H}`, source: 'Natural Earth 1:110m (public domain) via world-atlas 2.0.2', countries: rows }));
// Static SVG for the map page (loaded by fetch, cached by the browser). Countries carry data-iso; colours/links are
// added on the page from the live story counts.
const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}">` +
  rows.map(([iso, name, d]) => `<path${iso ? ` data-iso="${iso}"` : ""} d="${d}"><title>${esc(name)}</title></path>`).join("") + "</svg>";
writeFileSync(out.replace(/.json$/, ".svg"), svg);
console.log(`${rows.length} shapes, ${missing} without ISO code; wrote ${out.replace(/.json$/, ".svg")} (${svg.length} bytes)`);
