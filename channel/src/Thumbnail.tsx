import React from "react";
import { AbsoluteFill } from "remotion";
import type { Video } from "./schema";
import { buildTimeline, dayNumber, formatDate } from "./lib/time";
import { cameraAt, viewTransform } from "./lib/camera";
import { useEngine } from "./lib/useEngine";
import { MapView } from "./components/MapView";
import { applyTheme, theme } from "./lib/theme";

// 1920x1080 still from the same data: the map at its most telling date, cropped 16:9, plus 0-4 words.
export const Thumbnail: React.FC<{ video: Video }> = ({ video }) => {
  applyTheme(video.style);
  const engine = useEngine(video);
  const tl = buildTimeline(video);
  const day = video.thumbnail.date ? dayNumber(video.thumbnail.date) : tl.endDay;
  if (!engine) return <AbsoluteFill style={{ background: theme.panel }} />;
  const base = cameraAt(video, day);
  const camera = { center: video.thumbnail.center ?? base.center, zoom: video.thumbnail.zoom ?? base.zoom };
  // The map viewport is 4:3; scale it to 1920 wide and crop top and bottom.
  const scale = 1920 / engine.vw;
  const top = (1080 - 1080 * scale) / 2;
  const [tv, th] = video.thumbnail.textAt.split("-");
  const ring = video.thumbnail.highlight && (() => {
    const { k, tx, ty } = viewTransform(engine, camera, video.map.resolutionScale);
    const [x, y] = engine.project(video.thumbnail.highlight!);
    return { x: (x * k + tx) * scale, y: (y * k + ty) * scale + top };
  })();
  return (
    <AbsoluteFill style={{ background: theme.panel, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 0, top, width: engine.vw, height: 1080, transform: `scale(${scale})`, transformOrigin: "top left" }}>
        <MapView video={video} engine={engine} day={day} frame={-1000} eventFrames={tl.eventFrames} camera={camera} />
      </div>
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(90deg, rgba(29,25,20,0.0) 50%, rgba(29,25,20,0.35))" }} />
      {video.thumbnail.text && (
        <div style={{ position: "absolute", [th]: 70, [tv]: 60, textAlign: th === "right" ? "right" : "left", fontFamily: theme.display, fontWeight: 700, fontSize: 150, lineHeight: 0.95, color: "#fff", WebkitTextStroke: `10px ${theme.panel}`, paintOrder: "stroke fill", maxWidth: 1300, textTransform: "uppercase" }}>
          {video.thumbnail.text}
        </div>
      )}
      {ring && (
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
          <circle cx={ring.x} cy={ring.y} r={120} fill="none" stroke={theme.panel} strokeWidth={22} />
          <circle cx={ring.x} cy={ring.y} r={120} fill="none" stroke={theme.front} strokeWidth={12} />
        </svg>
      )}
      <div style={{ position: "absolute", [th === "left" ? "right" : "left"]: 60, [tv === "top" ? "bottom" : "top"]: 50, padding: "10px 22px", background: theme.panel, color: theme.front, fontFamily: theme.display, fontWeight: 700, fontSize: 64, borderBottom: `6px solid ${theme.front}` }}>
        {formatDate(day)}
      </div>
    </AbsoluteFill>
  );
};
