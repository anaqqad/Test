import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { z } from "zod";
import { B, SEPIA, sans, serif } from "../reel/style";

/**
 * YouTube thumbnail, 1280x720 (Template A from docs/youtube/COMPETITIVE_ANALYSIS_2026-10-26.md):
 * archival portrait on the left 55 %, a 1-3 word gold label and a small line on the right, thin gold frame.
 */
export const thumbSchema = z.object({
  folder: z.string(),
  image: z.string(),
  /** object-position of the portrait, e.g. "50% 20%" */
  position: z.string().default("50% 20%"),
  /** zoom on the portrait */
  zoom: z.number().default(1.0),
  label: z.string(),
  sub: z.string().optional(),
  kicker: z.string().optional(),
});
export type ThumbProps = z.infer<typeof thumbSchema>;

export const Thumb: React.FC<ThumbProps> = ({ folder, image, position, zoom, label, sub, kicker }) => (
  <AbsoluteFill style={{ backgroundColor: B.black }}>
    <div style={{ position: "absolute", left: 0, top: 0, width: 760, height: 720, overflow: "hidden" }}>
      <Img
        src={staticFile(`pd/${folder}/${image}.jpg`)}
        style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: position, transform: `scale(${zoom})`, transformOrigin: position, filter: `${SEPIA} contrast(1.12)` }}
      />
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(14,12,10,0) 55%, rgba(14,12,10,1) 100%)" }} />
    </div>
    <div style={{ position: "absolute", left: 640, right: 50, top: 0, bottom: 0, display: "flex", flexDirection: "column", justifyContent: "center", gap: 18 }}>
      {kicker ? <div style={{ fontFamily: sans, fontWeight: 800, fontSize: 34, letterSpacing: 4, color: B.cream, textTransform: "uppercase" }}>{kicker}</div> : null}
      <div style={{ fontFamily: serif, fontWeight: 900, fontSize: label.length > 12 ? 104 : 132, lineHeight: 0.95, color: B.gold, textShadow: "0 6px 30px rgba(0,0,0,0.9)", textTransform: "uppercase" }}>{label}</div>
      {sub ? <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 44, color: B.cream }}>{sub}</div> : null}
    </div>
    <AbsoluteFill style={{ border: `8px solid ${B.gold}`, boxSizing: "border-box" }} />
  </AbsoluteFill>
);
