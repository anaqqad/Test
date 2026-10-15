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

// GeoJSON (longitude/latitude) for the interactive Leaflet map: same countries and Morocco merge, coordinates
// rounded to 0.01° (~1 km, plenty for 1:110m data). Properties: iso2, name.
// Shapes that cross the 180° line (Russia, Fiji): move their western points east (+360°) so Leaflet does not
// draw lines across the whole map.
const flat = (c) => (typeof c[0] === "number" ? [c] : c.flatMap(flat));
const unwrap = (c) => (typeof c[0] === "number" ? [c[0] < 0 ? c[0] + 360 : c[0], c[1]] : c.map(unwrap));
const crosses = (g) => { const xs = flat(g.coordinates).map((c) => c[0]); return Math.min(...xs) < -150 && Math.max(...xs) > 150; };
const round = (c) => (typeof c[0] === 'number' ? [Math.round(c[0] * 100) / 100, Math.round(c[1] * 100) / 100] : c.map(round));
const geo = {
  type: 'FeatureCollection',
  features: all.map((f) => {
    const code = f.id ? iso.numericToAlpha2(f.id) : undefined;
    return { type: 'Feature', properties: { iso2: code ? code.toLowerCase() : '', name: f.properties.name }, geometry: { type: f.geometry.type, coordinates: round(crosses(f.geometry) ? unwrap(f.geometry.coordinates) : f.geometry.coordinates) } };
  }),
};
const geoOut = out.replace(/\.json$/, '.geojson');
writeFileSync(geoOut, JSON.stringify(geo));
console.log(`wrote ${geoOut} (${JSON.stringify(geo).length} bytes)`);
