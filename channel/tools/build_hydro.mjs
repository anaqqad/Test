// Natural Earth 10m rivers and lakes (public domain) -> public/geo/hydro.json, merged global + Europe detail,
// coordinates rounded to 0.01 degree. Run once: node tools/build_hydro.mjs <dir with the unzipped shapefiles>
import fs from "node:fs";
import path from "node:path";
import * as shapefile from "shapefile";

const dir = process.argv[2];
const read = async (name) => (await shapefile.read(path.join(dir, name, `${name}.shp`), path.join(dir, name, `${name}.dbf`), { encoding: "utf-8" })).features;
const round = (c) => (typeof c[0] === "number" ? [Math.round(c[0] * 100) / 100, Math.round(c[1] * 100) / 100] : c.map(round));
const slim = (f, keep) => ({ type: "Feature", properties: Object.fromEntries(keep.map((k) => [k, f.properties[k]])), geometry: { type: f.geometry.type, coordinates: round(f.geometry.coordinates) } });

const rivers = [...(await read("ne_10m_rivers_lake_centerlines")), ...(await read("ne_10m_rivers_europe"))]
  .filter((f) => f.geometry && f.properties.featurecla !== "Lake Centerline")
  .map((f) => slim(f, ["name", "scalerank"]));
const lakes = [...(await read("ne_10m_lakes")), ...(await read("ne_10m_lakes_europe"))].filter((f) => f.geometry).map((f) => slim(f, ["name", "scalerank"]));
fs.writeFileSync("public/geo/hydro.json", JSON.stringify({ rivers: { type: "FeatureCollection", features: rivers }, lakes: { type: "FeatureCollection", features: lakes } }));
console.log("rivers", rivers.length, "lakes", lakes.length, (fs.statSync("public/geo/hydro.json").size / 1e6).toFixed(1), "MB");
