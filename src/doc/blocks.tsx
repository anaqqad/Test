import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { fitCrop, type Rect } from "../reel/layout";
import { HarborMap } from "../reel/blocks";
import { B, EASE_OUT, reveal, SEPIA, sans, serif } from "../reel/style";
import type { DocBeat, DocSpec } from "./schema";

/** Layout of the 1920x1080 frame: text keeps a 96 px margin; subtitles own the bottom band. */
export const M = 96;

const imgSize = (spec: DocSpec, key: string) => spec.images?.[key] ?? { width: 1920, height: 1080 };
const toCss = (r: Rect) => ({ left: r.x, top: r.y, width: r.w, height: r.h });

/** Card: an image (or a crop of it) framed on a blurred, darkened copy of itself, with a caption under it. */
export const DocCard: React.FC<{ beat: DocBeat; spec: DocSpec; duration: number }> = ({ beat, spec, duration }) => {
  const frame = useCurrentFrame();
  const v = beat.visual;
  const key = v.image ?? "";
  const { width: iw, height: ih } = imgSize(spec, key);
  const crop = (v.crop ?? [0, 0, 1, 1]) as [number, number, number, number];
  const inn = reveal(frame, 0, 14);
  const drift = interpolate(frame, [0, duration], [1, 1.05], { extrapolateRight: "clamp" });
  const pad = 14;
  const area: Rect = { x: 260, y: 90, w: 1400, h: 760 };
  const { image, crop: c } = fitCrop(iw, ih, crop, { x: area.x + pad, y: area.y + pad, w: area.w - 2 * pad, h: area.h - 2 * pad });
  const local = (r: Rect): Rect => ({ x: r.x - c.x, y: r.y - c.y, w: r.w, h: r.h });
  return (
    <AbsoluteFill style={{ backgroundColor: B.black, overflow: "hidden" }}>
      <Img
        src={staticFile(`pd/${spec.id}/${key}.jpg`)}
        style={{ position: "absolute", inset: -80, width: "calc(100% + 160px)", height: "calc(100% + 160px)", objectFit: "cover", filter: `${SEPIA} blur(30px) brightness(0.4)` }}
      />
      <div
        style={{
          position: "absolute",
          left: c.x - pad,
          top: c.y - pad,
          width: c.w + 2 * pad,
          height: c.h + 2 * pad,
          background: B.cream,
          boxShadow: "0 30px 70px rgba(0,0,0,0.65)",
          transform: `translateY(${(1 - inn) * 30}px) scale(${drift})`,
          opacity: inn,
        }}
      >
        <div style={{ position: "absolute", left: pad, top: pad, width: c.w, height: c.h, overflow: "hidden" }}>
          <Img src={staticFile(`pd/${spec.id}/${key}.jpg`)} style={{ position: "absolute", ...toCss(local(image)), filter: SEPIA }} />
        </div>
      </div>
      {v.caption ? (
        <div style={{ position: "absolute", left: 0, right: 0, top: c.y + c.h + pad + 18, textAlign: "center", opacity: reveal(frame, 10, 12) }}>
          <span style={{ fontFamily: serif, fontStyle: "italic", fontSize: 30, color: B.creamDim }}>{v.caption}</span>
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

/** The reel's portrait harbor map, scaled to the full frame height and centred, on open water. */
export const DocMap: React.FC<{ step: "wharf" | "forts" | "sumter" | "fleet"; duration: number }> = ({ step, duration }) => {
  const s = 1080 / 1420;
  return (
    <AbsoluteFill style={{ backgroundColor: B.water, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: (1920 - 1080 * s) / 2, top: 0, width: 1080, height: 1920, transform: `scale(${s})`, transformOrigin: "0 0" }}>
        <HarborMap step={step} duration={duration} />
      </div>
      <AbsoluteFill style={{ background: "linear-gradient(90deg, rgba(14,12,10,0.55) 0%, rgba(14,12,10,0) 22%, rgba(14,12,10,0) 78%, rgba(14,12,10,0.55) 100%)" }} />
    </AbsoluteFill>
  );
};

export const ChapterCard: React.FC<{ num: number; title: string }> = ({ num, title }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 0, 14);
  const b = reveal(frame, 8, 14);
  return (
    <AbsoluteFill style={{ backgroundColor: B.black }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, rgba(226,178,74,0.14) 0%, rgba(14,12,10,0) 60%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 380, display: "flex", flexDirection: "column", alignItems: "center", gap: 26 }}>
        <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 32, letterSpacing: 12, color: B.gold, textTransform: "uppercase", opacity: a }}>Chapter {num}</div>
        <div style={{ height: 4, width: 120 * a, background: B.gold }} />
        <div style={{ fontFamily: serif, fontWeight: 900, fontSize: 104, color: B.cream, opacity: b, transform: `translateY(${(1 - b) * 20}px)`, textAlign: "center" }}>{title}</div>
      </div>
    </AbsoluteFill>
  );
};

export const BigTitle: React.FC<{ title: string; sub?: string }> = ({ title, sub }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 0, 12);
  const b = reveal(frame, 8, 12);
  return (
    <AbsoluteFill style={{ backgroundColor: B.black }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 42%, rgba(226,178,74,0.14) 0%, rgba(14,12,10,0) 62%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, display: "flex", flexDirection: "column", alignItems: "center", gap: 24, textAlign: "center" }}>
        <div style={{ fontFamily: serif, fontWeight: 900, fontSize: title.length > 8 ? 150 : 210, lineHeight: 1, color: B.gold, opacity: a, transform: `translateY(${(1 - a) * 24}px)` }}>{title}</div>
        <div style={{ height: 5, width: 160, background: B.gold, opacity: b }} />
        {sub ? <div style={{ fontFamily: serif, fontStyle: "italic", fontSize: 58, color: B.cream, opacity: b, maxWidth: 1500 }}>{sub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

export const QuoteCard: React.FC<{ quote: string; by?: string }> = ({ quote, by }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 0, 16);
  const b = reveal(frame, 14, 14);
  return (
    <AbsoluteFill style={{ backgroundColor: B.black }}>
      <div style={{ position: "absolute", left: 220, right: 220, top: 250, display: "flex", flexDirection: "column", gap: 36 }}>
        <div style={{ fontFamily: serif, fontSize: 200, lineHeight: 0.6, color: B.gold, opacity: a }}>“</div>
        <div style={{ fontFamily: serif, fontStyle: "italic", fontWeight: 600, fontSize: 76, lineHeight: 1.2, color: B.cream, opacity: a }}>{quote}</div>
        {by ? <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 30, letterSpacing: 6, color: B.gold, textTransform: "uppercase", opacity: b }}>— {by}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

export const DocEndCard: React.FC<{ page: string; line: string }> = ({ page, line }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 0, 12);
  const b = reveal(frame, 10, 14);
  return (
    <AbsoluteFill style={{ backgroundColor: B.black }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(226,178,74,0.16) 0%, rgba(14,12,10,0) 60%)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 330, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, textAlign: "center" }}>
        <div style={{ fontFamily: sans, fontWeight: 700, fontSize: 34, letterSpacing: 10, color: B.creamDim, textTransform: "uppercase", opacity: a }}>Subscribe to</div>
        <div style={{ fontFamily: serif, fontWeight: 900, fontSize: 118, color: B.gold, opacity: a, transform: `scale(${0.95 + 0.05 * a})` }}>{page}</div>
        <div style={{ height: 5, width: 160, background: B.gold, opacity: b }} />
        <div style={{ fontFamily: serif, fontStyle: "italic", fontSize: 54, color: B.cream, opacity: b }}>{line}</div>
        <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 30, letterSpacing: 4, color: B.creamDim, opacity: b, marginTop: 20 }}>Sources: theblackhistoryroom.com</div>
      </div>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------- overlays */

export const DocHook: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  return (
    <div style={{ position: "absolute", left: M, top: 330, width: 1100, display: "flex", flexDirection: "column", gap: 20 }}>
      <div style={{ height: 8, width: 130, background: B.gold }} />
      <div style={{ fontFamily: serif, fontWeight: 900, fontSize: 104, lineHeight: 1.04, color: B.cream, textShadow: "0 4px 24px rgba(0,0,0,0.85)" }}>
        {words.map((raw, i) => {
          const opens = words.slice(0, i + 1).filter((x) => x.startsWith("*")).length;
          const closes = words.slice(0, i).filter((x) => /\*[.,!?]?$/.test(x)).length;
          const y = interpolate(frame, [i * 1.5, i * 1.5 + 8], [14, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_OUT });
          return (
            <span key={i} style={{ display: "inline-block", marginRight: 24, color: opens > closes ? B.gold : undefined, transform: `translateY(${y}px)` }}>
              {raw.replace(/\*/g, "")}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export const DocLowerThird: React.FC<{ name: string; sub?: string }> = ({ name, sub }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 6, 14);
  return (
    <div style={{ position: "absolute", left: M, top: 690, opacity: a, transform: `translateX(${(1 - a) * -40}px)` }}>
      <div style={{ display: "inline-block", padding: "14px 30px 16px 24px", background: "rgba(14,12,10,0.86)", borderLeft: `8px solid ${B.gold}` }}>
        <div style={{ fontFamily: serif, fontWeight: 800, fontSize: 54, color: B.cream, lineHeight: 1.05 }}>{name}</div>
        {sub ? <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 24, letterSpacing: 3, color: B.gold, marginTop: 6, textTransform: "uppercase" }}>{sub}</div> : null}
      </div>
    </div>
  );
};

export const DocYear: React.FC<{ from: number; to: number; duration: number }> = ({ from, to, duration }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [4, Math.max(5, duration * 0.7)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: M, top: 60, opacity: reveal(frame, 0, 8), fontFamily: serif, fontWeight: 900, fontSize: 120, lineHeight: 1, color: B.gold, textShadow: "0 6px 30px rgba(0,0,0,0.8)", fontVariantNumeric: "tabular-nums" }}>
      {Math.round(from + (to - from) * p)}
    </div>
  );
};

export const DocPin: React.FC<{ label: string; sub?: string; top: number }> = ({ label, sub, top }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 6, 12);
  return (
    <div style={{ position: "absolute", left: M, top, opacity: a, transform: `translateY(${(1 - a) * 16}px)` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16, padding: "10px 24px 10px 16px", background: "rgba(14,12,10,0.82)", borderRadius: 50, border: `3px solid ${B.gold}` }}>
        <svg width={30} height={40} viewBox="0 0 40 52">
          <path d="M 20 50 C 20 50 2 28 2 18 A 18 18 0 0 1 38 18 C 38 28 20 50 20 50 Z" fill={B.gold} />
          <circle cx={20} cy={18} r={7} fill={B.black} />
        </svg>
        <div>
          <div style={{ fontFamily: serif, fontWeight: 800, fontSize: 36, color: B.cream, lineHeight: 1.05 }}>{label}</div>
          {sub ? <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 18, letterSpacing: 2, color: B.gold, textTransform: "uppercase" }}>{sub}</div> : null}
        </div>
      </div>
    </div>
  );
};

export const DocStamp: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [4, 10, 14], [1.12, 0.97, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: M, top: 70, opacity: frame >= 4 ? 1 : 0 }}>
      <div style={{ fontFamily: serif, fontWeight: 900, fontSize: 76, color: B.black, background: B.gold, padding: "6px 30px 12px", transform: `rotate(-3deg) scale(${s})`, transformOrigin: "0% 50%", boxShadow: "0 18px 40px rgba(0,0,0,0.55)", textTransform: "uppercase" }}>
        {text}
      </div>
    </div>
  );
};
