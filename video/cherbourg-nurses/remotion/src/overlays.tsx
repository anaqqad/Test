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

/** SubscribeButton: the channel's own call to subscribe, lower right. A dark tab slides in with the channel name,
 *  a grease-pencil red SUBSCRIBE button, a pointer clicks it, it turns to SUBSCRIBED with a tick, the bell rings,
 *  and a hand-drawn circle goes round it. Our palette and fonts only; no platform logo. */
export const SubscribeButton: React.FC<{ channel: string; tagline: string }> = ({ channel, tagline }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const clamp = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
  const slide = interpolate(f, [0, 12, d - 10, d], [520, 0, 0, 520], clamp);
  const ease = 1 - Math.pow(1 - interpolate(f, [8, 34], [0, 1], clamp), 3);
  const px = 1520 + (1700 - 1520) * ease, py = 1060 + (958 - 1060) * ease; // pointer travels to the button
  const press = f >= 34 && f < 40;
  const done = f >= 38;
  const pointer = interpolate(f, [6, 10, 52, 60], [0, 1, 1, 0], clamp);
  const ring = done ? Math.sin((f - 38) * 0.9) * 14 * Math.max(0, 1 - (f - 38) / 30) : 0;
  const circle = interpolate(f, [44, 62], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ transform: `translateX(${slide}px)` }}>
      <div style={{ position: "absolute", right: 70, bottom: 92, display: "flex", alignItems: "center", gap: 22, background: "#0b0b0b", padding: "18px 22px 18px 26px", boxShadow: "0 6px 24px rgba(0,0,0,.55)" }}>
        <div>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 44, letterSpacing: 1, color: C.light, textTransform: "uppercase", lineHeight: 1 }}>{channel}</div>
          <div style={{ fontFamily: MONO, fontSize: 18, letterSpacing: 1.2, color: C.lightSoft, textTransform: "uppercase", marginTop: 6 }}>{tagline}</div>
        </div>
        <div style={{ position: "relative", transform: `scale(${press ? 0.93 : 1})` }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 40, letterSpacing: 2, padding: "12px 26px 10px", textTransform: "uppercase",
            background: done ? "#2a2a2a" : C.grease, color: done ? C.light : "#fff", border: done ? `2px solid ${C.lightSoft}` : "2px solid transparent" }}>
            {done ? "Subscribed ✓" : "Subscribe"}
          </div>
          <svg width="250" height="110" viewBox="0 0 250 110" style={{ position: "absolute", left: -20, top: -22, overflow: "visible" }}>
            <path d="M14,58 C10,18 90,4 150,8 C215,12 246,34 238,62 C228,98 120,104 60,96 C22,90 8,72 18,48"
              fill="none" stroke={C.grease} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - circle} />
          </svg>
        </div>
        <svg width="46" height="50" viewBox="0 0 24 26" style={{ transform: `rotate(${ring}deg)`, transformOrigin: "50% 10%" }}>
          <path d="M12 2a1.5 1.5 0 0 1 1.5 1.5v.7A7 7 0 0 1 19 11v5l2 3H3l2-3v-5a7 7 0 0 1 5.5-6.8v-.7A1.5 1.5 0 0 1 12 2zm-2.5 19h5a2.5 2.5 0 0 1-5 0z"
            fill={done ? C.light : C.lightSoft} />
        </svg>
      </div>
      <svg width="44" height="56" viewBox="0 0 22 28" style={{ position: "absolute", left: px - slide, top: py, opacity: pointer, transform: `scale(${press ? 0.88 : 1})` }}>
        <path d="M2 1 L2 22 L7.5 17 L11 26 L14.5 24.5 L11 16 L18 16 Z" fill="#fff" stroke="#111" strokeWidth={1.4} strokeLinejoin="round" />
      </svg>
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
