// Story cards added 19 Nov 2026 (ideas from the owner's Jewish History Room channel, drawn in Darkroom & Ledger):
// CastCard (who's who: a real photo print + name + role), Headline (one statement, one accent phrase in grease italic
// that gets underlined when it is spoken) and CodeWord (dictionary rows: word -> literal meaning -> what it meant).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, MONO, QUOTE } from "./theme";
import { Stroke, useEnv, wobble } from "./marks";
import { Paper } from "./ledger";

const FPS = 30;
const ramp = (f: number, a: number, len = 10) =>
  interpolate(f, [a, a + len], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });

const Grain: React.FC = () => (
  <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
    <filter id="cgrain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" /><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0" /></filter>
    <rect width={1920} height={1080} filter="url(#cgrain)" />
  </svg>
);

/** Who's who: a tilted print of the person on the dark table, the name in caps with a grease underline, role and facts. */
export const CastCard: React.FC<{
  image: string; aspect: number; crop?: [number, number, number, number]; focus?: [number, number];
  name: string; role: string; lines?: string[]; source: string; kicker?: string; side?: "left" | "right";
}> = ({ image, aspect, crop = [0, 0, 1, 1], focus = [0.5, 0.35], name, role, lines = [], source, kicker = "WHO'S WHO", side = "left" }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const o = useEnv();
  const ph = Math.min(760, 680 / aspect), pw = ph * aspect;
  const px = side === "left" ? 190 : 1920 - 190 - pw - 32;
  const tx = side === "left" ? px + pw + 140 : 150;
  const tw = side === "left" ? 1920 - tx - 120 : px - 260;
  const drop = interpolate(f, [0, 16], [40, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(0.8)) });
  const push = interpolate(f, [0, d], [1, 1.06]);
  const [cx, cy, cw, chh] = crop;
  const under = ramp(f, 20, 14);
  return (
    <AbsoluteFill style={{ opacity: o, background: `radial-gradient(ellipse at ${side === "left" ? "35%" : "65%"} 50%, ${C.tableGlow} 0%, ${C.table} 70%)` }}>
      <div style={{ position: "absolute", left: px, top: (1080 - ph) / 2 - 16 + drop, width: pw + 32, height: ph + 32, background: "#f3f1ec",
        transform: `rotate(${side === "left" ? -2.2 : 2.2}deg)`, boxShadow: "0 26px 60px rgba(0,0,0,0.65)" }}>
        <div style={{ position: "absolute", left: 16, top: 16, width: pw, height: ph, overflow: "hidden", background: "#000" }}>
          <div style={{ position: "absolute", inset: 0, transform: `scale(${push})`, transformOrigin: `${focus[0] * 100}% ${focus[1] * 100}%` }}>
            <Img src={staticFile(`stills/${image}`)} style={{ position: "absolute", width: `${100 / cw}%`, height: `${100 / chh}%`, left: `${(-cx / cw) * 100}%`, top: `${(-cy / chh) * 100}%`, filter: "grayscale(1) contrast(1.05)" }} />
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: tx, width: tw, top: 0, height: 1080, display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <div style={{ opacity: ramp(f, 8), fontFamily: MONO, fontSize: 26, letterSpacing: 4, color: C.grease }}>{kicker}</div>
        <div style={{ opacity: ramp(f, 12), transform: `translateY(${(1 - ramp(f, 12)) * 16}px)`, fontFamily: HEAD, fontWeight: 700, fontSize: name.length > 16 ? 96 : 120, lineHeight: 0.95, textTransform: "uppercase", color: C.light, marginTop: 12 }}>{name}</div>
        <svg width={tw} height={30} style={{ overflow: "visible", marginTop: 6 }}>
          <Stroke d={wobble([[0, 14], [Math.min(tw - 20, name.length * 52), 10]], 31, 2)} p={under} w={8} />
        </svg>
        <div style={{ opacity: ramp(f, 26), fontFamily: MONO, fontSize: 32, lineHeight: 1.4, color: C.light, marginTop: 18 }}>{role}</div>
        {lines.map((l, i) => (
          <div key={i} style={{ opacity: ramp(f, 34 + i * 10), transform: `translateX(${(1 - ramp(f, 34 + i * 10)) * 14}px)`, fontFamily: MONO, fontSize: 26, lineHeight: 1.45, color: C.lightSoft, marginTop: 14 }}>
            <span style={{ color: C.grease }}>■ </span>{l}
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: side === "left" ? tx : 150, bottom: 54, fontFamily: MONO, fontSize: 18, letterSpacing: 1, color: C.lightSoft, textTransform: "uppercase", opacity: ramp(f, 30) }}>{source}</div>
      <Grain />
    </AbsoluteFill>
  );
};

/** One statement on the dark table; the accent phrase is grease italic serif and gets underlined at `at` seconds. */
export const Headline: React.FC<{ kicker?: string; before?: string; accent: string; after?: string; at?: number; source?: string }> = ({ kicker, before = "", accent, after = "", at = 1.2, source }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const o = useEnv();
  const a = Math.round(at * FPS);
  const zoom = interpolate(f, [0, d], [1, 1.04]);
  const under = ramp(f, a, 14);
  const glow = interpolate(f, [a, a + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: o, background: `radial-gradient(ellipse at 50% 45%, ${C.tableGlow} 0%, ${C.table} 72%)`, alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: 1500, textAlign: "center", transform: `scale(${zoom})` }}>
        {kicker ? <div style={{ fontFamily: MONO, fontSize: 26, letterSpacing: 5, color: C.grease, opacity: ramp(f, 4), marginBottom: 34 }}>{kicker}</div> : null}
        <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 104, lineHeight: 1.04, textTransform: "uppercase", color: C.light, opacity: ramp(f, 6), transform: `translateY(${(1 - ramp(f, 6)) * 18}px)` }}>
          {before}{before ? " " : ""}
          <span style={{ position: "relative", display: "inline-block", fontFamily: QUOTE, fontStyle: "italic", fontWeight: 400, textTransform: "none", color: C.grease, fontSize: 112, opacity: 0.55 + 0.45 * glow }}>
            {accent}
            <svg width="100%" height={34} viewBox="0 0 100 34" preserveAspectRatio="none" style={{ position: "absolute", left: 0, bottom: -24, overflow: "visible" }}>
              <path d="M2 18 C 30 12, 60 24, 98 14" fill="none" stroke={C.grease} strokeWidth={5} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - under} />
            </svg>
          </span>
          {after ? " " : ""}{after}
        </div>
      </div>
      {source ? <div style={{ position: "absolute", left: 150, bottom: 54, fontFamily: MONO, fontSize: 18, letterSpacing: 1, color: C.lightSoft, textTransform: "uppercase", opacity: ramp(f, 20) }}>{source}</div> : null}
      <Grain />
    </AbsoluteFill>
  );
};

/** Dictionary rows on the ledger: the word, its literal meaning, and what it meant in the code. Rows appear at `at` (s). */
export const CodeWord: React.FC<{ file: string; head: string; rows: { word: string; lit: string; mil: string; at?: number }[]; source: string; colHeads?: [string, string, string] }> = ({ file, head, rows, source, colHeads = ["Word", "Literally", "In the code"] }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const n = rows.length;
  const rowH = Math.min(150, 620 / n);
  const x0 = 230, x1 = 800, x2 = 1310;
  return (
    <Paper file={file} head={head} source={source}>
      <div style={{ position: "absolute", top: 300, left: 0, width: 1920 }}>
        {[colHeads[0], colHeads[1], colHeads[2]].map((h, i) => (
          <div key={i} style={{ position: "absolute", left: [x0, x1, x2][i], top: 0, fontFamily: MONO, fontSize: 22, letterSpacing: 3, color: C.inkSoft, textTransform: "uppercase", opacity: ramp(f, 10) }}>{h}</div>
        ))}
        {rows.map((r, i) => {
          const t = Math.round((r.at ?? 0.8 + i * Math.max(1.2, (d / FPS - 2.5) / n)) * FPS);
          const a = ramp(f, t, 10), b = ramp(f, t + 10, 10), c = ramp(f, t + 20, 10);
          const y = 50 + i * rowH;
          return (
            <React.Fragment key={i}>
              <svg width={1920} height={rowH} style={{ position: "absolute", left: 0, top: y }}>
                <line x1={x0} y1={rowH - 14} x2={1760} y2={rowH - 14} stroke={C.ink} strokeWidth={1.2} opacity={0.22 * a} />
                <Stroke d={wobble([[x1 - 90, rowH / 2 - 6], [x1 - 30, rowH / 2 - 6]], 40 + i, 1.2)} p={b} w={5} color={C.inkSoft} />
                <Stroke d={wobble([[x2 - 90, rowH / 2 - 6], [x2 - 30, rowH / 2 - 6]], 60 + i, 1.2)} p={c} w={5} />
              </svg>
              <div style={{ position: "absolute", left: x0, top: y + rowH / 2 - 44, width: x1 - x0 - 110, opacity: a, fontFamily: QUOTE, fontSize: Math.min(64, rowH * 0.5), color: C.ink }}>{r.word}</div>
              <div style={{ position: "absolute", left: x1, top: y + rowH / 2 - 40, width: x2 - x1 - 110, opacity: b, fontFamily: QUOTE, fontStyle: "italic", fontSize: Math.min(54, rowH * 0.42), color: C.inkSoft }}>“{r.lit}”</div>
              <div style={{ position: "absolute", left: x2, top: y + rowH / 2 - 46, width: 1760 - x2, opacity: c, transform: `translateX(${(1 - c) * 14}px)`, fontFamily: HEAD, fontWeight: 700, fontSize: Math.min(70, rowH * 0.56), color: C.grease, textTransform: "uppercase" }}>{r.mil}</div>
            </React.Fragment>
          );
        })}
      </div>
    </Paper>
  );
};
