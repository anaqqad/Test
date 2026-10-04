import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig, Easing } from "remotion";
import { C, FADE, SANS, SERIF } from "./theme";

/** Opacity envelope: fade in over FADE frames, out over the last FADE frames. */
export const useEnvelope = () => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  return interpolate(f, [0, FADE, d - FADE, d], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

/** 0..1 progress of a draw-on animation starting at `start` frames and lasting `len` frames. */
export const useDraw = (start: number, len: number) => {
  const f = useCurrentFrame();
  return interpolate(f, [start, start + len], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
};

/** Serif title with a gold underline that draws left to right under the text only. */
export const Title: React.FC<{ text: string; size?: number; delay?: number }> = ({ text, size = 44, delay = 4 }) => {
  const p = useDraw(delay, 16);
  return (
    <div style={{ display: "inline-block", fontFamily: SERIF, fontSize: size, color: C.title, lineHeight: 1.25 }}>
      {text}
      <div style={{ height: 3, marginTop: 6, background: C.gold, width: `${p * 100}%` }} />
    </div>
  );
};

/** Navy lower third: serif title + sans subtitle. Bottom-left, ~4.7 % from the edge (as measured). */
export const LowerThird: React.FC<{ title: string; subtitle?: string; width?: number; bottom?: number }> = ({ title, subtitle, width = 1240, bottom = 118 }) => (
  <div style={{ position: "absolute", left: 90, bottom, width, background: C.panel, padding: "20px 34px 22px" }}>
    <Title text={title} size={42} />
    {subtitle ? <div style={{ fontFamily: SANS, fontSize: 28, color: C.body, marginTop: 10 }}>{subtitle}</div> : null}
  </div>
);

/** Tiny citation line, bottom-right. */
export const SourceLine: React.FC<{ text: string }> = ({ text }) => (
  <div style={{ position: "absolute", right: 72, bottom: 34, maxWidth: 1500, textAlign: "right", fontFamily: SANS, fontSize: 21, color: C.source, background: "rgba(10,14,24,0.55)", padding: "4px 10px" }}>
    {text}
  </div>
);
