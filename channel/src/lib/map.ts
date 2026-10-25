// The map engine: projection, base map raster, territory keyframes as signed distance fields, and the
// per-day territory state (washes, front line, area held, unit markers). Pure canvas, no WebGL, so it renders
// the same in Studio, on a laptop and on a headless server.
import * as d3 from "d3-geo";
import * as topojson from "topojson-client";
import { staticFile } from "remotion";
import type { Video } from "../schema";
import { dayNumber, smoothstep } from "./time";
import { signedDistance } from "./sdf";
import { theme } from "./theme";

export const VIEWPORT = { w: 1440, h: 1080 }; // map area; the sidebar takes the remaining 480 px

type Geo = d3.GeoPermissibleObjects;
type Rgb = [number, number, number];

const rgb = (hex: string): Rgb => {
  const n = parseInt(hex.replace("#", ""), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};

function mulberry32(seed: number) {
  return () => {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// d3-geo treats a clockwise ring as "everything except this"; hand-drawn data gets either winding.
function normalize(geom: { type: string; coordinates: any }): Geo {
  const polys: number[][][][] = geom.type === "Polygon" ? [geom.coordinates] : geom.coordinates;
  const fixed = polys.map((rings) => {
    const p = { type: "Polygon", coordinates: rings } as GeoJSON.Polygon;
    return d3.geoArea(p) > 2 * Math.PI ? rings.map((r) => r.slice().reverse()) : rings;
  });
  return { type: "MultiPolygon", coordinates: fixed } as GeoJSON.MultiPolygon;
}

type Layer = Video["territories"][number]["layers"][number];

// The region on one side of a front line, closed around a box well outside the map.
function beyondPolygon(beyond: NonNullable<Layer["beyond"]>, bounds: Video["map"]["bounds"]): Geo {
  const [[west, south], [east, north]] = bounds;
  const m = 20;
  const box = { west: west - m, east: east + m, south: Math.max(-89, south - m), north: Math.min(89, north + m) };
  const line = beyond.line;
  const first = line[0], last = line[line.length - 1];
  let ring: [number, number][];
  if (beyond.side === "north" || beyond.side === "south") {
    const y = beyond.side === "north" ? box.north : box.south;
    ring = [[box.west, first[1]], ...line, [box.east, last[1]], [box.east, y], [box.west, y]];
  } else {
    const x = beyond.side === "east" ? box.east : box.west;
    ring = [[first[0], box.south], ...line, [last[0], box.north], [x, box.north], [x, box.south]];
  }
  // Densify so long edges follow parallels/meridians instead of great circles.
  const dense: [number, number][] = [];
  for (let i = 0; i < ring.length; i++) {
    const a = ring[i], b = ring[(i + 1) % ring.length];
    const n = Math.max(1, Math.ceil(Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])) / 0.5));
    for (let j = 0; j < n; j++) dense.push([a[0] + ((b[0] - a[0]) * j) / n, a[1] + ((b[1] - a[1]) * j) / n]);
  }
  dense.push(dense[0]);
  return normalize({ type: "Polygon", coordinates: [dense] });
}

function makeProjection(video: Video, w: number, h: number): d3.GeoProjection {
  const [[west, south], [east, north]] = video.map.bounds;
  const lon0 = (west + east) / 2;
  let p: d3.GeoProjection;
  if (video.map.projection === "mercator") p = d3.geoMercator();
  else if (video.map.projection === "equirectangular") p = d3.geoEquirectangular();
  else {
    const span = north - south;
    p = d3.geoConicEqualArea().parallels(video.map.parallels ?? [south + span / 6, north - span / 6]);
  }
  p.rotate([-lon0, 0]);
  // Fit the lon/lat box by its edge points: polygon edges would be great circles, not parallels.
  const pts: [number, number][] = [];
  for (let i = 0; i <= 20; i++) {
    const lon = west + ((east - west) * i) / 20, lat = south + ((north - south) * i) / 20;
    pts.push([lon, south], [lon, north], [west, lat], [east, lat]);
  }
  return p.fitExtent([[0, 0], [w, h]], { type: "MultiPoint", coordinates: pts });
}

function canvas2d(w: number, h: number) {
  const c = new OffscreenCanvas(w, h);
  const ctx = c.getContext("2d", { willReadFrequently: true })!;
  return { c, ctx };
}

function rasterize(geo: Geo, projection: d3.GeoProjection, w: number, h: number): Uint8Array {
  const { ctx } = canvas2d(w, h);
  ctx.fillStyle = "#fff";
  ctx.beginPath();
  d3.geoPath(projection, ctx as unknown as CanvasRenderingContext2D)(geo);
  ctx.fill();
  const px = ctx.getImageData(0, 0, w, h).data;
  const mask = new Uint8Array(w * h);
  for (let i = 0; i < mask.length; i++) mask[i] = px[i * 4 + 3] > 127 ? 1 : 0;
  return mask;
}

export type DayState = {
  day: number;
  wash: OffscreenCanvas; // territory colours, composited with "multiply" over the paper
  front: OffscreenCanvas; // glowing front line, composited normally
  areaKm2: number[]; // per faction, same order as video.factions
  markers: { x: number; y: number; faction: number; front: boolean }[];
};

export class MapEngine {
  readonly w: number;
  readonly h: number;
  readonly projection: d3.GeoProjection;
  readonly base: OffscreenCanvas;
  private landIdx: Int32Array; // land pixels inside the theatre: the only pixels territory is painted on
  private pixelKm2: Float32Array; // area of one map pixel, per row
  private keyDays: number[];
  private sdfCache = new Map<number, Float32Array[]>();
  private candidates: { x: number; y: number; i: number; r: number }[] = [];
  private last: DayState | null = null;
  private colors: Rgb[];
  private frontRgb = rgb(theme.front);

  constructor(private video: Video, private world: any) {
    const s = video.map.resolutionScale;
    this.w = Math.round(VIEWPORT.w * s);
    this.h = Math.round(VIEWPORT.h * s);
    this.projection = makeProjection(video, this.w, this.h);
    const countries = world.objects.countries;
    const land = topojson.merge(world, countries.geometries) as Geo;
    // Modern borders inside the theatre are anachronistic (they are what the war decided), so skip them.
    const inTheatre = (g: any) => video.map.theatre.includes(g.properties.name);
    const borders = topojson.mesh(world, countries, (a: any, b: any) => a !== b && !(inTheatre(a) && inTheatre(b))) as Geo;

    const landMask = rasterize(land, this.projection, this.w, this.h);
    const theatre = video.map.theatre.length ? rasterize(this.countries(video.map.theatre), this.projection, this.w, this.h) : landMask;
    const idx: number[] = [];
    for (let i = 0; i < landMask.length; i++) if (landMask[i] && theatre[i]) idx.push(i);
    this.landIdx = Int32Array.from(idx);
    this.pixelKm2 = this.measurePixels();
    this.base = this.paintBase(land, borders, landMask, theatre);
    this.keyDays = video.territories.map((k) => dayNumber(k.date));
    this.colors = video.factions.map((f) => rgb(f.color));

    // Marker candidates: a jittered grid on land; each has a fixed random draw so markers don't flicker.
    const rand = mulberry32(7);
    const step = 22 * s;
    for (let y = step / 2; y < this.h; y += step)
      for (let x = step / 2; x < this.w; x += step) {
        const px = Math.round(x + (rand() - 0.5) * step * 0.8), py = Math.round(y + (rand() - 0.5) * step * 0.8);
        const i = py * this.w + px;
        if (px >= 0 && py >= 0 && px < this.w && py < this.h && landMask[i] && theatre[i]) this.candidates.push({ x: px, y: py, i, r: rand() });
      }
  }

  private countries(names: string[]): Geo {
    const geoms = this.world.objects.countries.geometries;
    const known = new Set(geoms.map((g: any) => g.properties.name));
    const unknown = names.filter((n) => !known.has(n));
    if (unknown.length) throw new Error(`Unknown country names (use Natural Earth names): ${unknown.join(", ")}`);
    return topojson.merge(this.world, geoms.filter((g: any) => names.includes(g.properties.name))) as Geo;
  }

  private layerGeo(layer: Layer): Geo {
    if (layer.geometry) return normalize(layer.geometry);
    if (layer.countries) return this.countries(layer.countries);
    if (layer.beyond) return beyondPolygon(layer.beyond, this.video.map.bounds);
    return { type: "Sphere" } as Geo;
  }

  // km² covered by one pixel in each row (exact for equal-area and cylindrical projections).
  private measurePixels(): Float32Array {
    const out = new Float32Array(this.h);
    const R = 6371.0088;
    const x = this.w / 2;
    for (let y = 0; y < this.h; y++) {
      const ring = [[x, y], [x, y + 1], [x + 1, y + 1], [x + 1, y], [x, y]].map((p) => this.projection.invert!(p as [number, number])!);
      const a = d3.geoArea({ type: "Polygon", coordinates: [ring] });
      out[y] = Math.min(a, 4 * Math.PI - a) * R * R;
    }
    return out;
  }

  private paintBase(land: Geo, borders: Geo, landMask: Uint8Array, theatre: Uint8Array): OffscreenCanvas {
    const { w, h } = this;
    const s = this.video.map.resolutionScale;
    const { c, ctx } = canvas2d(w, h);
    const path = d3.geoPath(this.projection, ctx as unknown as CanvasRenderingContext2D);

    // Sea with engraved coastline ripples, from the distance to land.
    const img = ctx.createImageData(w, h);
    const sea = rgb(theme.sea), paper = rgb(theme.paper), paperDim = rgb(theme.paperDim), ink = rgb(theme.ink);
    const dist = signedDistance(landMask, w, h, 400);
    const spacing = 6 * s;
    const rand = mulberry32(11);
    for (let i = 0; i < w * h; i++) {
      const grain = (rand() - 0.5) * 10;
      let r: number, g: number, b: number;
      if (landMask[i]) [r, g, b] = theatre[i] ? paper : paperDim;
      else {
        [r, g, b] = sea;
        const d = -dist[i];
        const k = Math.round(d / spacing);
        if (k >= 1 && k <= 5) {
          const a = Math.max(0, 1 - Math.abs(d - k * spacing) / (0.9 * s)) * 0.32 * (1 - (k - 1) / 5);
          r += (ink[0] - r) * a, g += (ink[1] - g) * a, b += (ink[2] - b) * a;
        }
      }
      img.data[i * 4] = r + grain;
      img.data[i * 4 + 1] = g + grain;
      img.data[i * 4 + 2] = b + grain;
      img.data[i * 4 + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);

    const [[west, south], [east, north]] = this.video.map.bounds;
    const span = Math.max(east - west, north - south);
    const stepDeg = [1, 2, 5, 10, 15, 30].find((st) => span / st <= 8) ?? 30;
    ctx.strokeStyle = theme.ink;
    ctx.globalAlpha = 0.1;
    ctx.lineWidth = 1 * s;
    ctx.beginPath();
    path(d3.geoGraticule().step([stepDeg, stepDeg])());
    ctx.stroke();

    ctx.globalAlpha = 0.45;
    ctx.setLineDash([4 * s, 3 * s]);
    ctx.beginPath();
    path(borders);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.globalAlpha = 0.85;
    ctx.lineWidth = 1.3 * s;
    ctx.beginPath();
    path(land);
    ctx.stroke();
    ctx.globalAlpha = 1;
    return c;
  }

  private keyframeSdf(k: number): Float32Array[] {
    let sdf = this.sdfCache.get(k);
    if (!sdf) {
      const { w, h } = this;
      const ids = this.video.factions.map((f) => f.id);
      const masks = ids.map(() => new Uint8Array(w * h));
      for (const layer of this.video.territories[k].layers) {
        const f = ids.indexOf(layer.faction);
        if (f < 0) throw new Error(`Unknown faction "${layer.faction}" in territories[${k}]`);
        const m = rasterize(this.layerGeo(layer), this.projection, w, h);
        for (let i = 0; i < m.length; i++) if (m[i]) for (let g = 0; g < masks.length; g++) masks[g][i] = g === f ? 1 : 0;
      }
      sdf = masks.map((m) => signedDistance(m, w, h));
      if (this.sdfCache.size >= 4) this.sdfCache.delete(this.sdfCache.keys().next().value!);
      this.sdfCache.set(k, sdf);
    }
    return sdf;
  }

  project(lonLat: [number, number]): [number, number] {
    return this.projection(lonLat) ?? [0, 0];
  }

  state(day: number): DayState {
    if (this.last && this.last.day === day) return this.last;
    const { w, h, keyDays } = this;
    const s = this.video.map.resolutionScale;
    let b = keyDays.findIndex((d) => d > day);
    if (b === -1) b = keyDays.length - 1;
    const a = Math.max(0, day >= keyDays[b] ? b : b - 1);
    const t = a === b ? 0 : smoothstep((day - keyDays[a]) / (keyDays[b] - keyDays[a]));
    const A = this.keyframeSdf(a), B = this.keyframeSdf(b);
    const F = this.video.factions.length;

    const wash = canvas2d(w, h), front = canvas2d(w, h);
    const washImg = wash.ctx.createImageData(w, h), frontImg = front.ctx.createImageData(w, h);
    const owner = new Int8Array(w * h).fill(-1);
    const gap = new Float32Array(w * h).fill(1e9);
    const areaKm2 = new Array(F).fill(0);
    const frontWidth = 2.2 * s;
    const frontZone = 40 * s; // markers crowd within this band of the front
    const [fr, fg, fb] = this.frontRgb;

    for (const i of this.landIdx) {
      let best = -1, d1 = -Infinity, d2 = -Infinity;
      for (let f = 0; f < F; f++) {
        const d = A[f][i] + (B[f][i] - A[f][i]) * t;
        if (d > d1) (d2 = d1), (d1 = d), (best = f);
        else if (d > d2) d2 = d;
      }
      if (d1 <= -0.5) continue;
      owner[i] = best;
      areaKm2[best] += this.pixelKm2[(i / w) | 0];
      const [r, g, bl] = this.colors[best];
      const o = i * 4;
      washImg.data[o] = r, washImg.data[o + 1] = g, washImg.data[o + 2] = bl;
      washImg.data[o + 3] = 255 * Math.min(1, d1 + 0.5);
      if (F > 1 && d2 > -frontZone) {
        gap[i] = d1 - d2;
        const glow = Math.max(0, 1 - (d1 - d2) / (2 * frontWidth));
        if (glow > 0) {
          frontImg.data[o] = fr, frontImg.data[o + 1] = fg, frontImg.data[o + 2] = fb;
          frontImg.data[o + 3] = 255 * glow;
        }
      }
    }
    wash.ctx.putImageData(washImg, 0, 0);
    front.ctx.putImageData(frontImg, 0, 0);

    const markers: DayState["markers"] = [];
    for (const c of this.candidates) {
      const f = owner[c.i];
      if (f < 0) continue;
      const nearFront = gap[c.i] < frontZone;
      if (nearFront ? c.r < 0.85 : c.r < 0.12) markers.push({ x: c.x, y: c.y, faction: f, front: nearFront });
    }

    this.last = { day, wash: wash.c, front: front.c, areaKm2, markers };
    return this.last;
  }
}

const engines = new Map<string, Promise<MapEngine>>();
const worlds = new Map<string, Promise<any>>();

export function loadEngine(video: Video): Promise<MapEngine> {
  const key = JSON.stringify([video.id, video.map, video.factions, video.territories]);
  let p = engines.get(key);
  if (!p) {
    const file = `geo/countries-${video.map.landDetail}.json`;
    if (!worlds.has(file)) worlds.set(file, fetch(staticFile(file)).then((r) => r.json()));
    p = worlds.get(file)!.then((world) => new MapEngine(video, world));
    engines.set(key, p);
  }
  return p;
}
