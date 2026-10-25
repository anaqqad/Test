import React, { useLayoutEffect, useRef } from "react";
import type { Video } from "../schema";
import { cameraAt, viewTransform, type Camera } from "../lib/camera";
import { VIEWPORT, type MapEngine } from "../lib/map";
import { theme } from "../lib/theme";
import { dayNumber } from "../lib/time";

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

export const MapView: React.FC<Props> = ({ video, engine, day, frame, eventFrames, camera }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  const s = video.map.resolutionScale;

  useLayoutEffect(() => {
    const ctx = ref.current!.getContext("2d")!;
    const state = engine.state(day);
    const { k, tx, ty } = viewTransform(engine, camera ?? cameraAt(video, day), s);

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, VIEWPORT.w, VIEWPORT.h);
    ctx.setTransform(k, 0, 0, k, tx, ty);
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(engine.base, 0, 0);
    ctx.globalCompositeOperation = "multiply";
    ctx.globalAlpha = 0.78;
    ctx.drawImage(state.wash, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    ctx.globalAlpha = 1;

    // Front line (core and halo are baked into the layer: a canvas blur filter is very slow without a GPU).
    ctx.drawImage(state.front, 0, 0);

    // Unit markers, sized in screen pixels so zooming in doesn't inflate them.
    const r = 4.2 / k;
    ctx.lineWidth = 1.1 / k;
    ctx.strokeStyle = theme.paper;
    for (const m of state.markers) {
      const f = video.factions[m.faction];
      ctx.fillStyle = f.ink ?? f.color;
      drawMarker(ctx, f.marker, m.x, m.y, m.front ? r * 1.15 : r * 0.85);
    }

    // Labels.
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    for (const l of video.map.labels) {
      if ((l.from && day < dayNumber(l.from)) || (l.to && day >= dayNumber(l.to))) continue;
      const [x, y] = engine.project(l.at);
      const px = (l.size ?? (l.kind === "city" ? 17 : l.kind === "sea" ? 20 : 26)) / Math.sqrt(k);
      ctx.fillStyle = theme.ink;
      if (l.kind === "city") {
        ctx.globalAlpha = 0.95;
        ctx.beginPath();
        ctx.arc(x, y, 3.2 / k, 0, Math.PI * 2);
        ctx.fill();
        ctx.font = `700 ${px}px "${theme.number}"`;
        ctx.textAlign = "left";
        ctx.lineWidth = 3.5 / k;
        ctx.strokeStyle = "rgba(239,227,196,0.85)";
        ctx.strokeText(l.text, x + 6 / k, y);
        ctx.fillText(l.text, x + 6 / k, y);
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

    // Event pulses: an expanding ink ring and a gold dot at the place where it happened.
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
  }, [engine, video, day, frame, eventFrames, camera, s]);

  return <canvas ref={ref} width={VIEWPORT.w} height={VIEWPORT.h} style={{ position: "absolute", left: 0, top: 0 }} />;
};

