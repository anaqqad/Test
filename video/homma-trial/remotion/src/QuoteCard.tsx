// Quote card (learned from Brew's Newton quote): dark topical backdrop (blurred, darkened), cut-out portrait of the
// speaker bottom-left, the quote in a classic serif, centred block on the right, each LINE fading in from grey to white
// as the narrator reaches its first word, attribution "- Name" right-aligned after the last word. Camera opens on the
// portrait, eases out to show the text, then drifts slowly.
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/OldStandardTT";

const { fontFamily: SERIF } = loadFont("normal", { weights: ["400"], subsets: ["latin"] });

export type QuoteLine = { text: string; at: number }; // at = frame (local) when the narrator starts this line

export const QuoteCard: React.FC<{
  bg?: string; portrait?: string; lines: QuoteLine[]; by: string; byAt: number; dur: number;
  portraitH?: number; textX?: number; textW?: number; size?: number;
}> = ({ bg, portrait, lines, by, byAt, dur, portraitH = 900, textX = 900, textW = 960, size = 42 }) => {
  const f = useCurrentFrame();
  const intro = Math.max(12, Math.min(lines[0]?.at ?? 30, 40));
  const open = interpolate(f, [0, intro], [1, 0], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const scale = 1 + 0.32 * open + interpolate(f, [intro, dur], [0, 0.035], { extrapolateLeft: "clamp" });
  const tx = 560 * open; // centre the portrait first, then reveal the text side
  // the reference never stops moving: a steady push toward the text while it builds (portrait slides out left),
  // then a pull back to the full card as the attribution lands
  const push = interpolate(f, [intro, byAt - 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) });
  const back = interpolate(f, [byAt - 4, byAt + 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const toText = 1 + 0.26 * push * (1 - back);
  return (
    <AbsoluteFill style={{ background: "#05070c", overflow: "hidden" }}>
     <AbsoluteFill style={{ transform: `scale(${toText})`, transformOrigin: "70% 40%" }}>
      <AbsoluteFill style={{ transform: `translateX(${tx}px) scale(${scale})`, transformOrigin: "22% 60%" }}>
        {bg ? <Img src={staticFile(bg)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", filter: "blur(3px) brightness(0.32) saturate(0.7)" }} />
          : <AbsoluteFill style={{ background: "radial-gradient(ellipse at 70% 40%, #1b2440 0%, #070a14 70%)" }} />}
        <AbsoluteFill style={{ background: "radial-gradient(ellipse 80% 80% at 60% 45%, transparent 30%, rgba(0,0,0,0.65) 100%)" }} />
        {portrait ? <Img src={staticFile(portrait)} style={{ position: "absolute", left: 40, bottom: 0, height: portraitH, filter: "drop-shadow(0 0 40px rgba(0,0,0,0.6))" }} /> : null}
        <div style={{ position: "absolute", left: textX, top: 250, width: textW, fontFamily: SERIF, fontSize: size, lineHeight: 1.42, color: "#f3f1ea", textAlign: "center",
          textShadow: "0 0 18px rgba(0,0,0,0.9), 0 0 4px rgba(255,255,255,0.25)" }}>
          {lines.map((l, i) => {
            const o = interpolate(f, [l.at - 2, l.at + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            const grey = interpolate(f, [l.at, l.at + 16], [0.45, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return <div key={i} style={{ opacity: o, filter: `brightness(${grey})` }}>{(i === 0 ? "“" : "") + l.text + (i === lines.length - 1 ? "”" : "")}</div>;
          })}
          <div style={{ textAlign: "right", fontSize: size * 0.72, marginTop: 22, opacity: interpolate(f, [byAt, byAt + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) }}>- {by}</div>
        </div>
      </AbsoluteFill>
     </AbsoluteFill>
    </AbsoluteFill>
  );
};
