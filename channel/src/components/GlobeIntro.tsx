import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import * as d3 from "d3-geo";
import * as topojson from "topojson-client";
import { cancelRender, continueRender, delayRender, interpolate, staticFile } from "remotion";
import type { Video } from "../schema";
import type { MapEngine } from "../lib/map";
import { dayNumber, smoothstep } from "../lib/time";
import { theme } from "../lib/theme";

let land50: Promise<d3.GeoPermissibleObjects> | null = null;
const loadLand = () =>
  (land50 ??= fetch(staticFile("geo/countries-50m.json"))
    .then((r) => r.json())
    .then((w) => topojson.merge(w, w.objects.countries.geometries) as d3.GeoPermissibleObjects));

// Cold open: the globe turns to the region and zooms in, with the title on the left, then dissolves into the map.
export const GlobeIntro: React.FC<{ video: Video; engine: MapEngine; frame: number; fps: number }> = ({ video, engine, frame, fps }) => {
  const ref = useRef<HTMLCanvasElement>(null);
  const [land, setLand] = useState<d3.GeoPermissibleObjects | null>(null);
  const [handle] = useState(() => delayRender("globe land"));
  useEffect(() => {
    loadLand().then((l) => (setLand(l), continueRender(handle))).catch(cancelRender);
  }, [handle]);

  const globe = video.header.globe!;
  const total = video.timeline.introSeconds * fps;
  const p = frame / total;
  const { clip, shapes } = React.useMemo(
    () => engine.shapesAt(dayNumber(globe.showDate ?? video.timeline.start)),
    [engine, globe.showDate, video.timeline.start],
  );

  useLayoutEffect(() => {
    if (!land) return;
    const ctx = ref.current!.getContext("2d")!;
    const W = 1920, H = 1080;
    const turn = smoothstep(interpolate(p, [0, 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
    const zoom = smoothstep(interpolate(p, [0.45, 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
    const lon = globe.from[0] + (globe.to[0] - globe.from[0]) * turn;
    const lat = globe.from[1] + (globe.to[1] - globe.from[1]) * turn;
    const r = 400 * Math.pow(4, zoom);
    const cx = 1320 - 300 * zoom, cy = H / 2;
    const proj = d3.geoOrthographic().rotate([-lon, -lat]).scale(r).translate([cx, cy]).clipAngle(90);
    const path = d3.geoPath(proj, ctx);

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    const bg = ctx.createRadialGradient(cx, cy, r * 0.5, cx, cy, Math.max(W, H));
    bg.addColorStop(0, "#2b2620");
    bg.addColorStop(1, theme.panel);
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, W, H);

    const halo = ctx.createRadialGradient(cx, cy, r * 0.98, cx, cy, r * 1.12);
    halo.addColorStop(0, "rgba(243,180,60,0.35)");
    halo.addColorStop(1, "rgba(243,180,60,0)");
    ctx.fillStyle = halo;
    ctx.beginPath();
    ctx.arc(cx, cy, r * 1.12, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = theme.sea;
    ctx.beginPath();
    path({ type: "Sphere" });
    ctx.fill();
    ctx.strokeStyle = theme.ink;
    ctx.globalAlpha = 0.12;
    ctx.lineWidth = 1;
    ctx.beginPath();
    path(d3.geoGraticule().step([15, 15])());
    ctx.stroke();
    ctx.globalAlpha = 1;

    ctx.fillStyle = theme.paper;
    ctx.beginPath();
    path(land);
    ctx.fill();

    // Territory, clipped to the theatre (or all land); later layers paint over earlier ones, as on the flat map.
    ctx.save();
    ctx.beginPath();
    path(land);
    ctx.clip();
    if (clip) {
      ctx.beginPath();
      path(clip);
      ctx.clip();
    }
    ctx.globalAlpha = 0.85;
    for (const s of shapes) {
      ctx.fillStyle = s.color;
      ctx.beginPath();
      path(s.geo);
      ctx.fill();
    }
    ctx.restore();

    ctx.strokeStyle = theme.ink;
    ctx.lineWidth = 1.2;
    ctx.globalAlpha = 0.8;
    ctx.beginPath();
    path(land);
    ctx.stroke();
    ctx.globalAlpha = 1;

    // Shading for a sense of roundness.
    const shade = ctx.createRadialGradient(cx - r * 0.35, cy - r * 0.35, r * 0.1, cx, cy, r);
    shade.addColorStop(0, "rgba(255,255,255,0.10)");
    shade.addColorStop(1, "rgba(29,25,20,0.35)");
    ctx.fillStyle = shade;
    ctx.beginPath();
    path({ type: "Sphere" });
    ctx.fill();

    const [px, py] = proj(globe.to) ?? [cx, cy];
    const pulse = (frame % fps) / fps;
    ctx.strokeStyle = theme.front;
    ctx.globalAlpha = 1 - pulse;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(px, py, 8 + 30 * pulse, 0, Math.PI * 2);
    ctx.stroke();
    ctx.globalAlpha = 1;
  }, [land, p, frame, fps, clip, shapes, globe]);

  const opacity = interpolate(p, [0.86, 1], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const textIn = interpolate(frame, [4, 20], [0, 1], { extrapolateRight: "clamp" });
  const textOut = interpolate(p, [0.6, 0.8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", inset: 0, opacity }}>
      <canvas ref={ref} width={1920} height={1080} style={{ position: "absolute", inset: 0 }} />
      <div style={{ position: "absolute", left: 100, top: 0, bottom: 0, width: 700, display: "flex", flexDirection: "column", justifyContent: "center", opacity: textIn * textOut, transform: `translateY(${(1 - textIn) * 20}px)`, color: theme.panelText }}>
        <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 92, lineHeight: 1.02, textShadow: "0 4px 30px rgba(0,0,0,0.7)" }}>{video.header.title}</div>
        <div style={{ fontFamily: theme.number, fontWeight: 700, fontSize: 34, color: theme.front, letterSpacing: 6, marginTop: 20 }}>{video.header.subtitle.toUpperCase()}</div>
        {video.header.hook && <div style={{ fontFamily: theme.number, fontWeight: 500, fontSize: 40, marginTop: 34, lineHeight: 1.25 }}>{video.header.hook}</div>}
      </div>
    </div>
  );
};
