// Grease-pencil marks: deterministic hand-drawn strokes that draw on over time.
import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "./theme";

const rnd = (seed: number) => {
  let s = seed * 9301 + 49297;
  return () => ((s = (s * 9301 + 49297) % 233280) / 233280) - 0.5;
};

/** Wobbly polyline through points, as an SVG path. */
export const wobble = (pts: [number, number][], seed: number, amp = 2.2) => {
  const r = rnd(seed);
  const out: string[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
    const n = Math.max(2, Math.round(Math.hypot(x1 - x0, y1 - y0) / 40));
    for (let k = i === 0 ? 0 : 1; k <= n; k++) {
      const t = k / n;
      out.push(`${(x0 + (x1 - x0) * t + r() * amp).toFixed(1)},${(y0 + (y1 - y0) * t + r() * amp).toFixed(1)}`);
    }
  }
  return "M" + out.join("L");
};

/** Hand-drawn ellipse that overshoots its start, like a quick grease-pencil circle. */
export const roughEllipse = (cx: number, cy: number, rx: number, ry: number, seed: number) => {
  const r = rnd(seed);
  const pts: string[] = [];
  const turns = 1.12;
  for (let i = 0; i <= 64; i++) {
    const a = -Math.PI * 0.6 + (i / 64) * Math.PI * 2 * turns;
    const k = 1 + r() * 0.05 + (i / 64) * 0.04;
    pts.push(`${(cx + Math.cos(a) * rx * k).toFixed(1)},${(cy + Math.sin(a) * ry * k).toFixed(1)}`);
  }
  return "M" + pts.join("L");
};

/** Progress 0..1 between frames a and a+len. */
export const useProg = (a: number, len: number) => {
  const f = useCurrentFrame();
  return interpolate(f, [a, a + len], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
};

/** Overall card envelope (fade in/out). */
export const useEnv = (inLen = 9, outLen = 9) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  return interpolate(f, [0, inLen, d - outLen, d], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

export const Stroke: React.FC<{ d: string; p: number; w?: number; color?: string; opacity?: number }> = ({ d, p, w = 6, color = C.grease, opacity = 0.92 }) => (
  <path d={d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} opacity={opacity} />
);
