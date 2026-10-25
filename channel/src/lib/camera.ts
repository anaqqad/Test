import type { Video } from "../schema";
import type { MapEngine } from "./map";
import { dayNumber, smoothstep } from "./time";

export type Camera = { center: [number, number]; zoom: number };

// Camera keys are pinned to dates, so moves stay in sync with the story when the pace changes.
export function cameraAt(video: Video, day: number): Camera {
  const [[w, s], [e, n]] = video.map.bounds;
  const keys = video.camera.map((k) => ({ day: dayNumber(k.date), center: k.center, zoom: k.zoom }));
  if (!keys.length) return { center: [(w + e) / 2, (s + n) / 2], zoom: 1 };
  if (day <= keys[0].day) return keys[0];
  for (let i = 1; i < keys.length; i++) {
    const a = keys[i - 1], b = keys[i];
    if (day <= b.day) {
      const t = smoothstep((day - a.day) / (b.day - a.day));
      return {
        center: [a.center[0] + (b.center[0] - a.center[0]) * t, a.center[1] + (b.center[1] - a.center[1]) * t],
        zoom: a.zoom + (b.zoom - a.zoom) * t,
      };
    }
  }
  return keys[keys.length - 1];
}

// Affine transform from map raster pixels to viewport pixels, clamped so the view never leaves the map.
export function viewTransform(engine: MapEngine, cam: Camera, scale: number) {
  const k = cam.zoom / scale;
  const [cx, cy] = engine.project(cam.center);
  const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
  const tx = clamp(engine.vw / 2 - cx * k, engine.vw - engine.w * k, 0);
  // In the vertical Short the HUD fills the top third, so the camera's focus sits lower in the frame.
  const focusY = engine.vh > engine.vw ? 0.62 : 0.5;
  const ty = clamp(engine.vh * focusY - cy * k, engine.vh - engine.h * k, 0);
  return { k, tx, ty };
}
