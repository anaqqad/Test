import React, { useLayoutEffect, useRef } from "react";
import type { Video } from "../schema";
import { cameraAt, viewTransform, type Camera } from "../lib/camera";
import type { MapEngine } from "../lib/map";
import { theme } from "../lib/theme";
import { dayNumber, sampleSeries, smoothstep } from "../lib/time";
import { flagSprite } from "../lib/flags";

type Props = {
  video: Video;
  engine: MapEngine;
  day: number;
  frame: number;
  eventFrames: number[];
  camera?: Camera; // overrides the timeline camera (thumbnails)
};

const PULSE_FRAMES = 50;

function drawMarker(ctx: CanvasRenderingContext2D, shape: string, x: number, y: number, r: number) {
  ctx.beginPath();
  if (shape === "circle") ctx.arc(x, y, r, 0, Math.PI * 2);
  else if (shape === "diamond") ctx.moveTo(x, y - r * 1.25), ctx.lineTo(x + r * 1.25, y), ctx.lineTo(x, y + r * 1.25), ctx.lineTo(x - r * 1.25, y);
  else if (shape === "triangle") ctx.moveTo(x, y - r * 1.3), ctx.lineTo(x + r * 1.2, y + r * 0.9), ctx.lineTo(x - r * 1.2, y + r * 0.9);
  else ctx.rect(x - r, y - r * 0.75, r * 2, r * 1.5);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}

function lighten(hex: string, amount: number): string {
  const n = parseInt(hex.replace("#", ""), 16);
  const c = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => Math.round(v + (255 - v) * amount));
  return `rgb(${c.join(",")})`;
}

// Catmull-Rom through the projected points, sampled densely, for smooth arrow shafts.
function smoothPath(pts: [number, number][], steps = 12): [number, number][] {
  if (pts.length < 3) return pts;
  const out: [number, number][] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let j = 0; j < steps; j++) {
      const t = j / steps, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map((d) =>
        0.5 * (2 * p1[d] + (-p0[d] + p2[d]) * t + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * t2 + (-p0[d] + 3 * p1[d] - 3 * p2[d] + p3[d]) * t3),
      ) as [number, number]);
    }
  }
  out.push(pts[pts.length - 1]);
  return out;
}

// A tapered offensive arrow along `pts` (map pixels), drawn up to `progress` of its length. Widths in map pixels.
function drawArrow(ctx: CanvasRenderingContext2D, pts: [number, number][], progress: number, width: number, fill: string, outline: string, lw: number) {
  const len: number[] = [0];
  for (let i = 1; i < pts.length; i++) len.push(len[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const total = len[len.length - 1] * progress;
  if (total < width) return;
  const head = Math.min(width * 2.6, total * 0.5);
  const shaft: [number, number][] = [];
  for (let i = 0; i < pts.length && len[i] <= total - head; i++) shaft.push(pts[i]);
  const at = (d: number): [number, number] => {
    let i = 1;
    while (i < len.length - 1 && len[i] < d) i++;
    const f = (d - len[i - 1]) / (len[i] - len[i - 1] || 1);
    return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f];
  };
  const neck = at(total - head), tip = at(total);
  shaft.push(neck);
  const left: [number, number][] = [], right: [number, number][] = [];
  shaft.forEach((p, i) => {
    const q = shaft[Math.min(shaft.length - 1, i + 1)], o = shaft[Math.max(0, i - 1)];
    const dx = q[0] - o[0], dy = q[1] - o[1], n = Math.hypot(dx, dy) || 1;
    const w = (width / 2) * (0.35 + 0.65 * (i / Math.max(1, shaft.length - 1))); // taper from tail to neck
    left.push([p[0] - (dy / n) * w, p[1] + (dx / n) * w]);
    right.push([p[0] + (dy / n) * w, p[1] - (dx / n) * w]);
  });
  const dx = tip[0] - neck[0], dy = tip[1] - neck[1], n = Math.hypot(dx, dy) || 1;
  const hw = width * 1.15;
  ctx.beginPath();
  left.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.lineTo(neck[0] - (dy / n) * hw, neck[1] + (dx / n) * hw);
  ctx.lineTo(tip[0], tip[1]);
  ctx.lineTo(neck[0] + (dy / n) * hw, neck[1] - (dx / n) * hw);
  for (let i = right.length - 1; i >= 0; i--) ctx.lineTo(right[i][0], right[i][1]);
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.lineWidth = lw;
  ctx.strokeStyle = outline;
  ctx.stroke();
}

// Flags (or banners) in the field for a faction on a given day, with cumulative weights for picking.
type Region = [[number, number], [number, number]] | undefined;
const inRegion = (r: Region, lon: number, lat: number) => !r || (lon >= r[0][0] && lon <= r[1][0] && lat >= r[0][1] && lat <= r[1][1]);

// Flags in the field for a faction on a given day (optionally at a place), with cumulative weights for picking.
function flagSet(f: Video["factions"][number], day: number, lon?: number, lat?: number) {
  const active = f.flags.filter(
    (x) => (!x.from || day >= dayNumber(x.from)) && (!x.to || day < dayNumber(x.to)) && (lon === undefined || inRegion(x.region, lon, lat!)),
  );
  if (!active.length && f.marker === "banner") return [{ id: `banner:${f.ink ?? f.color}`, cum: 1 }];
  const total = active.reduce((a, x) => a + x.weight, 0);
  let acc = 0;
  return active.map((x) => ({ id: x.flag, cum: (acc += x.weight) / total }));
}

export const MapView: React.FC<Props> = ({ video, engine, day, frame, eventFrames, camera }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  const s = video.map.resolutionScale;
  const round = video.map.flagShape === "round";

  useLayoutEffect(() => {
    const ctx = ref.current!.getContext("2d")!;
    const state = engine.state(day);
    const { k, tx, ty } = viewTransform(engine, camera ?? cameraAt(video, day), s);

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, engine.vw, engine.vh);
    ctx.setTransform(k, 0, 0, k, tx, ty);
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(engine.base, 0, 0);
    ctx.globalCompositeOperation = theme.washMode;
    ctx.globalAlpha = theme.washAlpha;
    ctx.drawImage(state.wash, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.globalAlpha = 1;
    if (engine.relief) {
      ctx.globalCompositeOperation = "overlay";
      ctx.drawImage(engine.relief, 0, 0, engine.w, engine.h);
      ctx.globalCompositeOperation = "source-over";
    }
    if (engine.hydro) {
      ctx.globalAlpha = 0.9;
      ctx.drawImage(engine.hydro, 0, 0);
      ctx.globalAlpha = 1;
    }

    // Front line (core and halo are baked into the layer: a canvas blur filter is very slow without a GPU).
    ctx.drawImage(state.front, 0, 0);

    // Offensive arrows grow along their path between their dates, then fade over a few days.
    for (const a of video.arrows) {
      const d0 = dayNumber(a.from), d1 = dayNumber(a.to);
      const fade = Math.max(2, (d1 - d0) * 0.25);
      if (day < d0 || day > d1 + fade) continue;
      const progress = smoothstep(Math.min(1, (day - d0) / Math.max(0.5, d1 - d0)));
      const f = video.factions.find((x) => x.id === a.faction);
      ctx.globalAlpha = 0.88 * (day > d1 ? 1 - (day - d1) / fade : 1);
      const pts = smoothPath(a.path.map((p) => engine.project(p)));
      drawArrow(ctx, pts, progress, (16 * a.width) / k, a.color ?? lighten(f?.color ?? theme.accent, 0.35), theme.ink, 2 / k);
      ctx.globalAlpha = 1;
    }

    // Unit markers, sized in screen pixels so zooming in doesn't inflate them. Flags (or banners) when the
    // faction has them, mixed by weight among the contingents in the field on this day.
    const r = 4.2 / k;
    ctx.lineWidth = 1.1 / k;
    ctx.strokeStyle = theme.paper;
    const flagSets = video.factions.map((f) => flagSet(f, day));
    const regional = video.factions.map((f) => f.flags.some((x) => x.region));
    for (const m of state.markers) {
      const set = regional[m.faction] ? flagSet(video.factions[m.faction], day, m.lon, m.lat) : flagSets[m.faction];
      if (set.length) {
        const id = (set.find((x) => m.pick <= x.cum) ?? set[set.length - 1]).id;
        const sprite = flagSprite(id, round);
        const scale = ((m.front ? 0.56 : 0.5) * (round ? 0.95 : 1)) / k;
        const sw = sprite.width * scale, sh = sprite.height * scale;
        ctx.drawImage(sprite, m.x - sw / 2, m.y - sh / 2, sw, sh);
        continue;
      }
      const f = video.factions[m.faction];
      ctx.fillStyle = f.ink ?? f.color;
      drawMarker(ctx, f.marker, m.x, m.y, m.front ? r * 1.15 : r * 0.85);
    }

    // Labels. Cities go largest first; one that would overlap a placed label flips to the left of its dot,
    // or is left out, so district names never sit on top of a capital at city zoom.
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const placed: [number, number, number, number][] = [];
    const free = (b: [number, number, number, number]) => placed.every((p) => b[2] < p[0] || b[0] > p[2] || b[3] < p[1] || b[1] > p[3]);
    const labels = video.map.labels
      .filter((l) => !(l.from && day < dayNumber(l.from)) && !(l.to && day >= dayNumber(l.to)))
      .map((l, i) => ({ l, i }))
      .sort((a, b) => (a.l.kind === "city" ? 0 : 1) - (b.l.kind === "city" ? 0 : 1) || (b.l.size ?? 17) - (a.l.size ?? 17) || a.i - b.i);
    for (const { l } of labels) {
      const [x, y] = engine.project(l.at);
      const big = video.layout === "full" ? 1.3 : 1; // full-frame battle maps are read at a glance
      const px = ((l.size ?? (l.kind === "city" ? 17 : l.kind === "sea" ? 20 : 26)) * big) / Math.sqrt(k);
      ctx.fillStyle = theme.labelInk;
      if (l.kind === "city") {
        ctx.font = `700 ${px}px "${theme.number}"`;
        const w = ctx.measureText(l.text).width, pad = 6 / k, h = px * 0.6;
        const right: [number, number, number, number] = [x + pad, y - h, x + pad + w, y + h];
        const left: [number, number, number, number] = [x - pad - w, y - h, x - pad, y + h];
        const box = free(right) ? right : free(left) ? left : null;
        if (!box) continue;
        placed.push(box);
        ctx.globalAlpha = 0.95;
        ctx.beginPath();
        ctx.arc(x, y, 3.2 / k, 0, Math.PI * 2);
        ctx.fill();
        ctx.textAlign = box === right ? "left" : "right";
        ctx.lineWidth = 3.5 / k;
        ctx.strokeStyle = theme.labelHalo;
        ctx.strokeText(l.text, box === right ? x + pad : x - pad, y);
        ctx.fillText(l.text, box === right ? x + pad : x - pad, y);
        ctx.textAlign = "center";
      } else {
        ctx.globalAlpha = l.kind === "sea" ? 0.45 : 0.5;
        ctx.font = `700 ${px}px "${theme.display}"`;
        ctx.letterSpacing = `${px * 0.3}px`;
        ctx.fillText(l.text.toUpperCase(), x, y);
        ctx.letterSpacing = "0px";
      }
    }
    ctx.globalAlpha = 1;

    // Army strength on the map: badge + big number + label, in screen-space sizes.
    for (const fc of video.forces) {
      if ((fc.from && day < dayNumber(fc.from)) || (fc.to && day >= dayNumber(fc.to))) continue;
      let at = fc.at;
      if (fc.moves.length) {
        const ks = fc.moves.map(([d, p]) => ({ d: dayNumber(d), p }));
        at = ks[0].p;
        for (let i = 0; i < ks.length; i++) {
          if (day >= ks[i].d) at = ks[i].p;
          if (i + 1 < ks.length && day >= ks[i].d && day < ks[i + 1].d) {
            const t = smoothstep((day - ks[i].d) / (ks[i + 1].d - ks[i].d));
            at = [ks[i].p[0] + (ks[i + 1].p[0] - ks[i].p[0]) * t, ks[i].p[1] + (ks[i + 1].p[1] - ks[i].p[1]) * t];
          }
        }
      }
      // Keep the counter on screen (the vertical Short shows much less width), then back to map coordinates.
      const [px0, py0] = engine.project(at);
      const sx = Math.min(engine.vw - 300, Math.max(40, px0 * k + tx));
      const sy = Math.min(engine.vh - 160, Math.max(engine.vh > engine.vw ? 800 : 300, py0 * k + ty));
      const x = (sx - tx) / k, y = (sy - ty) / k;
      const value = sampleSeries(fc.points.map(([d, v]) => [dayNumber(d), v]), day);
      const f = video.factions.find((q) => q.id === fc.factionId);
      const id = fc.flag ?? f?.flags[0]?.flag;
      const b = 34 / k;
      if (id) ctx.drawImage(flagSprite(id, true), x - b / 2, y - b / 2, b, b);
      ctx.textAlign = "left";
      ctx.font = `700 ${40 / k}px "${theme.number}"`;
      ctx.lineWidth = 6 / k;
      ctx.strokeStyle = "rgba(10,12,14,0.85)";
      const txt = Math.round(value).toLocaleString("en-US");
      ctx.strokeText(txt, x + 24 / k, y - 2 / k);
      ctx.fillStyle = "#fff";
      ctx.fillText(txt, x + 24 / k, y - 2 / k);
      ctx.font = `700 ${14 / k}px "${theme.number}"`;
      ctx.letterSpacing = `${2 / k}px`;
      ctx.lineWidth = 4 / k;
      ctx.strokeText(fc.label.toUpperCase(), x + 26 / k, y + 22 / k);
      ctx.fillStyle = theme.front;
      ctx.fillText(fc.label.toUpperCase(), x + 26 / k, y + 22 / k);
      ctx.letterSpacing = "0px";
      ctx.textAlign = "center";
    }

    // Event pulses: an expanding ring and a gold dot at the place where it happened.
    video.events.forEach((e, i) => {
      if (!e.at) return;
      const age = frame - eventFrames[i];
      if (age < 0 || age > PULSE_FRAMES) return;
      const [x, y] = engine.project(e.at);
      const t = age / PULSE_FRAMES;
      ctx.globalAlpha = 1 - t;
      ctx.strokeStyle = theme.accent;
      ctx.lineWidth = 3 / k;
      for (const lag of [0, 0.25]) {
        const tt = Math.max(0, t - lag);
        ctx.beginPath();
        ctx.arc(x, y, (8 + 70 * tt) / k, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.fillStyle = theme.front;
      ctx.beginPath();
      ctx.arc(x, y, 6 / k, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    });
  }, [engine, video, day, frame, eventFrames, camera, s, round]);

  return <canvas ref={ref} width={engine.vw} height={engine.vh} style={{ position: "absolute", left: 0, top: 0 }} />;
};

export { flagSet };
