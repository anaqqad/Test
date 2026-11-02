// Small overlays that sit on footage.
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, MONO } from "./theme";

/** Slug: date / name / note. A black tab wipes in from the left; a red square marks it as ours. */
export const Slug: React.FC<{ title: string; subtitle?: string }> = ({ title, subtitle }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const wipe = interpolate(f, [0, 10, d - 8, d], [0, 100, 100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sub = interpolate(f, [6, 16, d - 8, d], [0, 100, 100, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 96, bottom: 150, clipPath: `inset(0 ${100 - wipe}% 0 0)`, background: "#0b0b0b", padding: "10px 30px 8px 22px", display: "flex", alignItems: "center", gap: 18 }}>
        <div style={{ width: 18, height: 18, background: C.grease }} />
        <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 58, letterSpacing: 1, textTransform: "uppercase", color: C.light, lineHeight: 1.05, maxWidth: 1500 }}>{title}</div>
      </div>
      {subtitle ? (
        <div style={{ position: "absolute", left: 96, bottom: 104, clipPath: `inset(0 ${100 - sub}% 0 0)`, background: C.light, padding: "7px 22px 6px", fontFamily: MONO, fontWeight: 500, fontSize: 24, letterSpacing: 1, textTransform: "uppercase", color: C.ink }}>{subtitle}</div>
      ) : null}
    </AbsoluteFill>
  );
};

/** Honesty tag for stand-in or dated footage: typed mono in brackets with a red dot. */
export const ContextTag: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const o = interpolate(f, [0, 8, d - 8, d], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const n = Math.round(interpolate(f, [0, 18], [0, text.length], { extrapolateRight: "clamp" }));
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <div style={{ position: "absolute", left: 96, bottom: 44, display: "flex", alignItems: "center", gap: 12, fontFamily: MONO, fontSize: 22, letterSpacing: 1.5, color: "rgba(255,255,255,.82)", textTransform: "uppercase", textShadow: "0 1px 3px rgba(0,0,0,.9)" }}>
        <div style={{ width: 10, height: 10, borderRadius: 5, background: C.grease }} />
        [ {text.slice(0, n)} ]
      </div>
    </AbsoluteFill>
  );
};

/** BigNumber: the episode's figure, huge, counting up over the footage, with a label and a source line. */
export const BigNumber: React.FC<{ value: number; label: string; source: string }> = ({ value, label, source }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const o = interpolate(f, [0, 6, d - 10, d], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const t = interpolate(f, [2, 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const n = Math.round(value * (1 - Math.pow(1 - t, 3)));
  const line = interpolate(f, [30, 46], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const lab = interpolate(f, [36, 50], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: o, background: "radial-gradient(ellipse at center, rgba(0,0,0,.55) 0%, rgba(0,0,0,.78) 70%)" }}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", fontFamily: HEAD, fontWeight: 700, fontSize: 330, lineHeight: 1, letterSpacing: 4, color: C.light, fontVariantNumeric: "tabular-nums", textShadow: "0 4px 18px rgba(0,0,0,.6)" }}>
        {n.toLocaleString("en-US")}
      </div>
      <div style={{ position: "absolute", left: "50%", top: 600, width: 1100, height: 10, marginLeft: -550, background: C.grease, borderRadius: 5, clipPath: `inset(0 ${100 - line}% 0 0)`, transform: "rotate(-0.6deg)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 650, textAlign: "center", opacity: lab, fontFamily: HEAD, fontWeight: 700, fontSize: 64, letterSpacing: 2, textTransform: "uppercase", color: C.light }}>{label}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 750, textAlign: "center", opacity: lab, fontFamily: MONO, fontSize: 22, letterSpacing: 1.5, textTransform: "uppercase", color: C.lightSoft }}>{source}</div>
    </AbsoluteFill>
  );
};
