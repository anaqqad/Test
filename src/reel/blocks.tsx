import React, { createContext, useContext } from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { coverCrop, coverLayout, fitCrop, mapBox, type Rect } from "./layout";
import type { ReelBeat, ReelSpec } from "./schema";
import { B, CENTER_COL, EASE_IN_OUT, EASE_OUT, QC_CYAN, QC_MAGENTA, reveal, SAFE, SAFE_CX, SAFE_W, SEPIA, sans, serif } from "./style";

/**
 * QC mode: instead of the picture, every element that must stay out of Facebook's overlays
 * (captions, titles, labels) is painted solid magenta on black, and every face box cyan, so scripts/qc_reel.py can
 * measure exactly where it lands.
 */
export const QCContext = createContext(false);

/** Text wrapper: in QC mode the element becomes a solid magenta box of the same size. */
export const Critical: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => {
  const qc = useContext(QCContext);
  if (!qc) return <div style={style}>{children}</div>;
  return (
    <div
      style={{
        ...style,
        background: QC_MAGENTA,
        color: QC_MAGENTA,
        borderColor: QC_MAGENTA,
        boxShadow: "none",
        textShadow: "none",
        backgroundImage: "none",
        WebkitTextStroke: "0px",
      }}
    >
      {children}
    </div>
  );
};

const FaceMasks: React.FC<{ boxes: [number, number, number, number][]; rect: Rect }> = ({ boxes, rect }) => (
  <>
    {boxes.map((b, i) => {
      const r = mapBox(b, rect);
      return <div key={i} style={{ position: "absolute", left: r.x, top: r.y, width: r.w, height: r.h, background: QC_CYAN }} />;
    })}
  </>
);

/** Darkens the lower half so cream captions read on any photo, plus a soft vignette. */
const Grade: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(14,12,10,0.35) 0%, rgba(14,12,10,0) 22%, rgba(14,12,10,0) 45%, rgba(14,12,10,0.78) 72%, rgba(14,12,10,0.9) 100%)" }} />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 45% 40%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)" }} />
    <AbsoluteFill style={{ background: "rgba(120,72,20,0.10)", mixBlendMode: "multiply" }} />
  </>
);

const imgSize = (spec: ReelSpec, key: string) => spec.images?.[key] ?? { width: 1920, height: 1920 };

/** Full-bleed archival photo with a slow Ken Burns move and the warm sepia grade. */
export const PhotoBeat: React.FC<{ beat: ReelBeat; spec: ReelSpec; duration: number }> = ({ beat, spec, duration }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const qc = useContext(QCContext);
  const v = beat.visual;
  const key = v.image ?? "";
  const { width: iw, height: ih } = imgSize(spec, key);
  const p = interpolate(frame, [0, duration], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT });
  const [z0, z1] = v.zoom ?? [1.02, 1.15];
  const focus = v.focus ?? [0.5, 0.5];
  const pan = v.motion === "panLeft" ? 0.08 : v.motion === "panRight" ? -0.08 : 0;
  const f: [number, number] = [focus[0] - pan / 2 + pan * p, focus[1]];
  const rect = v.crop
    ? coverCrop(iw, ih, W, H, v.crop, f, v.anchor ?? [0.5, 0.4], z0 + (z1 - z0) * p)
    : coverLayout(iw, ih, W, H, f, v.anchor ?? [0.5, 0.4], z0 + (z1 - z0) * p);
  if (qc) return <FaceMasks boxes={spec.faces[key] ?? []} rect={rect} />;
  return (
    <AbsoluteFill style={{ backgroundColor: B.black, overflow: "hidden" }}>
      <Img
        src={staticFile(`pd/${spec.id}/${key}.jpg`)}
        style={{ position: "absolute", left: rect.x, top: rect.y, width: rect.w, height: rect.h, filter: SEPIA }}
      />
      <Grade />
    </AbsoluteFill>
  );
};

/**
 * Card: a cropped archival image (a newspaper page, an engraving, a small photo) set on a blurred,
 * darkened copy of itself. `clipping` styles it as a cut-out newspaper clipping.
 */
export const CardBeat: React.FC<{ beat: ReelBeat; spec: ReelSpec; duration: number }> = ({ beat, spec, duration }) => {
  const frame = useCurrentFrame();
  const qc = useContext(QCContext);
  const v = beat.visual;
  const key = v.image ?? "";
  const { width: iw, height: ih } = imgSize(spec, key);
  const crop = v.crop ?? [0, 0, 1, 1];
  const inn = reveal(frame, 0, 12);
  const drift = interpolate(frame, [0, duration], [1, 1.04], { extrapolateRight: "clamp" });
  const tilt = v.clipping ? -2.2 : 0;
  const pad = v.clipping ? 26 : 14;
  // the card sits in the safe column, above the caption band
  const area: Rect = { x: SAFE.left + 10, y: 250, w: SAFE_W - 20, h: 820 };
  const { image, crop: c } = fitCrop(iw, ih, crop, { x: area.x + pad, y: area.y + pad, w: area.w - 2 * pad, h: area.h - 2 * pad });
  const local = (r: Rect): Rect => ({ x: r.x - c.x, y: r.y - c.y, w: r.w, h: r.h });
  const transform = `translateY(${(1 - inn) * 40}px) rotate(${tilt}deg) scale(${drift})`;
  const captionTop = c.y + c.h + pad + 34;
  if (qc) {
    return (
      <AbsoluteFill>
        <div style={{ position: "absolute", left: c.x, top: c.y, width: c.w, height: c.h, overflow: "hidden", transform, transformOrigin: "50% 50%" }}>
          <FaceMasks boxes={spec.faces[key] ?? []} rect={local(image)} />
        </div>
        {v.caption ? <CardCaption top={captionTop} text={v.caption} /> : null}
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{ backgroundColor: B.black, overflow: "hidden" }}>
      <Img
        src={staticFile(`pd/${spec.id}/${key}.jpg`)}
        style={{ position: "absolute", inset: -80, width: "calc(100% + 160px)", height: "calc(100% + 160px)", objectFit: "cover", filter: `${SEPIA} blur(28px) brightness(0.45)` }}
      />
      <div
        style={{
          position: "absolute",
          left: c.x - pad,
          top: c.y - pad,
          width: c.w + 2 * pad,
          height: c.h + 2 * pad,
          background: v.clipping ? B.paper : B.cream,
          boxShadow: "0 30px 60px rgba(0,0,0,0.6)",
          transform,
          transformOrigin: "50% 50%",
          opacity: inn,
          clipPath: v.clipping
            ? "polygon(0% 1%, 6% 0%, 14% 1.2%, 25% 0.2%, 37% 1%, 50% 0%, 63% 1.1%, 76% 0.3%, 88% 1%, 100% 0%, 99.2% 50%, 100% 100%, 90% 99%, 78% 100%, 64% 99.2%, 50% 100%, 36% 99%, 22% 100%, 10% 99.1%, 0% 100%, 0.8% 50%)"
            : undefined,
        }}
      >
        <div style={{ position: "absolute", left: pad, top: pad, width: c.w, height: c.h, overflow: "hidden" }}>
          <Img src={staticFile(`pd/${spec.id}/${key}.jpg`)} style={{ position: "absolute", ...toCss(local(image)), filter: SEPIA }} />
        </div>
      </div>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(14,12,10,0) 60%, rgba(14,12,10,0.85) 100%)" }} />
      {v.caption ? <CardCaption top={captionTop} text={v.caption} /> : null}
    </AbsoluteFill>
  );
};

const toCss = (r: Rect) => ({ left: r.x, top: r.y, width: r.w, height: r.h });

const CardCaption: React.FC<{ top: number; text: string }> = ({ top, text }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: SAFE.left, width: SAFE_W, top, display: "flex", justifyContent: "center", opacity: reveal(frame, 8, 12) }}>
      <Critical style={{ fontFamily: serif, fontStyle: "italic", fontSize: 34, color: B.creamDim, textAlign: "center" }}>{text}</Critical>
    </div>
  );
};

/* ------------------------------------------------------------------ map */

/**
 * Illustrative map of Charleston harbor (not to scale): the city, the forts the Planter passed
 * and the Union blockade outside the bar. `step` shows one leg of the route per beat; earlier
 * legs stay drawn so consecutive map beats read as one journey.
 */
const PLACES = {
  wharf: { x: 300, y: 430, label: "Charleston wharf", lx: 330, ly: 360, align: "left" },
  pinckney: { x: 430, y: 520, label: "Castle Pinckney", lx: 470, ly: 500, align: "left" },
  johnson: { x: 345, y: 790, label: "Fort Johnson", lx: 315, ly: 770, align: "right" },
  sumter: { x: 560, y: 930, label: "Fort Sumter", lx: 525, ly: 905, align: "right" },
  moultrie: { x: 780, y: 770, label: "Fort Moultrie", lx: 745, ly: 690, align: "right" },
  fleet: { x: 710, y: 1170, label: "Union blockade", lx: 675, ly: 1145, align: "right" },
} as const;
type Place = keyof typeof PLACES;

const ROUTE = [
  [300, 430],
  [400, 480],
  [470, 600],
  [560, 760],
  [650, 870],
  [680, 1000],
  [710, 1170],
] as const;
// how far along ROUTE (0..1) each step ends
const STEP_END = { wharf: 0.0, forts: 0.36, sumter: 0.68, fleet: 1.0 } as const;
const STEP_PINS: Record<keyof typeof STEP_END, Place[]> = {
  wharf: ["wharf"],
  forts: ["wharf", "pinckney", "johnson"],
  sumter: ["wharf", "pinckney", "johnson", "sumter", "moultrie"],
  fleet: ["wharf", "pinckney", "johnson", "sumter", "moultrie", "fleet"],
};
const ORDER = ["wharf", "forts", "sumter", "fleet"] as const;

const routePath = ROUTE.map(([x, y], i) => `${i ? "L" : "M"} ${x} ${y}`).join(" ");
const routeLength = ROUTE.slice(1).reduce((a, [x, y], i) => a + Math.hypot(x - ROUTE[i][0], y - ROUTE[i][1]), 0);

const pointAt = (t: number) => {
  let d = t * routeLength;
  for (let i = 1; i < ROUTE.length; i++) {
    const [x0, y0] = ROUTE[i - 1];
    const [x1, y1] = ROUTE[i];
    const seg = Math.hypot(x1 - x0, y1 - y0);
    if (d <= seg) return { x: x0 + ((x1 - x0) * d) / seg, y: y0 + ((y1 - y0) * d) / seg };
    d -= seg;
  }
  return { x: ROUTE[ROUTE.length - 1][0], y: ROUTE[ROUTE.length - 1][1] };
};

export const HarborMap: React.FC<{ step: keyof typeof STEP_END; duration: number }> = ({ step, duration }) => {
  const frame = useCurrentFrame();
  const qc = useContext(QCContext);
  const idx = ORDER.indexOf(step);
  const from = idx > 0 ? STEP_END[ORDER[idx - 1]] : 0;
  const to = STEP_END[step];
  const t = from + (to - from) * interpolate(frame, [4, Math.max(5, duration - 6)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT });
  const boat = pointAt(t);
  const prevPins = idx > 0 ? STEP_PINS[ORDER[idx - 1]] : [];
  const pins = STEP_PINS[step];
  const highlight: Place | null = step === "sumter" ? "sumter" : step === "fleet" ? "fleet" : step === "wharf" ? "wharf" : null;

  const labels = pins.map((k, i) => {
    const pl = PLACES[k];
    const isNew = !prevPins.includes(k);
    const a = isNew ? reveal(frame, 6 + i * 4, 10) : 1;
    const hot = k === highlight;
    const style: React.CSSProperties = {
      position: "absolute",
      top: pl.ly - (hot ? 30 : 22),
      ...(pl.align === "left" ? { left: pl.lx } : { right: 1080 - pl.lx }),
      padding: hot ? "6px 20px 10px" : "6px 14px",
      background: hot ? B.gold : "rgba(14,12,10,0.88)",
      borderRadius: 6,
      fontFamily: hot ? serif : sans,
      fontWeight: hot ? 900 : 700,
      fontSize: hot ? 46 : 26,
      letterSpacing: hot ? 0 : 2,
      textTransform: hot ? "none" : "uppercase",
      color: hot ? B.black : B.cream,
      whiteSpace: "nowrap",
      opacity: a,
    };
    return (
      <Critical key={k} style={style}>
        {pl.label}
      </Critical>
    );
  });

  if (qc) return <AbsoluteFill>{labels}</AbsoluteFill>;
  const pulse = 1 + 0.25 * Math.sin(frame / 4);
  return (
    <AbsoluteFill style={{ backgroundColor: B.water }}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute", inset: 0 }}>
        <defs>
          <pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
            <line x1="0" y1="0" x2="0" y2="14" stroke="rgba(244,234,213,0.05)" strokeWidth="2" />
          </pattern>
        </defs>
        <rect width="1080" height="1920" fill="url(#hatch)" />
        {/* Charleston peninsula between the Ashley and Cooper rivers */}
        <path d="M 0 0 L 360 0 L 380 180 L 360 330 L 330 420 L 285 465 L 200 440 L 110 360 L 0 330 Z" fill={B.land} />
        {/* Mount Pleasant and Sullivan's Island */}
        <path d="M 640 0 L 1080 0 L 1080 690 L 940 740 L 840 770 L 790 790 L 760 760 L 740 700 L 690 580 L 600 470 L 560 320 Z" fill={B.land} />
        {/* James Island and Morris Island */}
        <path d="M 0 560 L 200 560 L 290 650 L 345 790 L 400 890 L 460 980 L 480 1080 L 450 1260 L 400 1420 L 0 1420 Z" fill={B.land} />
        {/* Castle Pinckney shoal */}
        <ellipse cx={430} cy={520} rx={28} ry={16} fill={B.land} />
        {/* Fort Sumter on its shoal */}
        <polygon points="540,915 580,915 590,945 550,960 530,940" fill={B.land} stroke={B.ink} strokeWidth={3} />
        <text x={150} y={250} fill="rgba(42,33,25,0.55)" fontFamily={serif} fontStyle="italic" fontSize={46}>
          Charleston
        </text>
        <text x={600} y={1195} fill="rgba(244,234,213,0.35)" fontFamily={serif} fontStyle="italic" fontSize={40}>
          Atlantic Ocean
        </text>
        {/* route so far */}
        <path
          d={routePath}
          fill="none"
          stroke={B.gold}
          strokeWidth={8}
          strokeDasharray={`${t * routeLength} ${routeLength}`}
          strokeLinecap="round"
        />
        {pins.map((k) => {
          const pl = PLACES[k];
          const hot = k === highlight;
          const a = prevPins.includes(k) ? 1 : reveal(frame, 4, 10);
          return (
            <g key={k} transform={`translate(${pl.x} ${pl.y}) scale(${a * (hot ? pulse : 1)})`}>
              <circle r={hot ? 20 : 13} fill={hot ? B.gold : B.cream} stroke={B.ink} strokeWidth={4} />
            </g>
          );
        })}
        {/* the Planter */}
        <g transform={`translate(${boat.x} ${boat.y})`}>
          <circle r={24} fill={B.black} stroke={B.gold} strokeWidth={5} />
          <path d="M -12 4 L 12 4 L 8 11 L -8 11 Z M -2 -12 L -2 4 M -2 -12 L 9 -2 L -2 -2" fill={B.gold} stroke={B.gold} strokeWidth={3} />
        </g>
      </svg>
      {labels}
      <div style={{ position: "absolute", left: SAFE.left, top: 1236, fontFamily: sans, fontSize: 24, letterSpacing: 2, color: "rgba(244,234,213,0.45)", textTransform: "uppercase" }}>
        Illustrative map, not to scale
      </div>
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------- overlays */

/** Bold hook line, *starred* words in gold. Fully visible on frame 0 so the first frame works as the cover. */
export const HookText: React.FC<{ text: string; animate?: boolean }> = ({ text, animate = true }) => {
  const frame = useCurrentFrame();
  const words = text.split(" ");
  return (
    <div style={{ position: "absolute", left: SAFE.left, width: SAFE_W, top: 900, display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 18 }}>
      <Critical style={{ height: 10, width: 140, background: B.gold }}>{""}</Critical>
      <Critical
        style={{
          fontFamily: serif,
          fontWeight: 900,
          fontSize: 92,
          lineHeight: 1.04,
          color: B.cream,
          textShadow: "0 4px 24px rgba(0,0,0,0.85)",
        }}
      >
        {words.map((raw, i) => {
          // *a phrase* = gold: a word is gold from the one that opens with * to the one that closes with *
          const opens = words.slice(0, i + 1).filter((x) => x.startsWith("*")).length;
          const closes = words.slice(0, i).filter((x) => /\*[.,!?]?$/.test(x)).length;
          const gold = opens > closes;
          const w = raw.replace(/\*/g, "");
          // no fade on frame 0: the words settle in place, they never start invisible
          const y = animate ? interpolate(frame, [i * 1.5, i * 1.5 + 8], [14, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_OUT }) : 0;
          return (
            <span key={i} style={{ display: "inline-block", marginRight: 22, color: gold ? B.gold : undefined, transform: `translateY(${y}px)` }}>
              {w}
            </span>
          );
        })}
      </Critical>
    </div>
  );
};

export const LowerThird: React.FC<{ name: string; sub?: string }> = ({ name, sub }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 4, 14);
  return (
    <div style={{ position: "absolute", left: SAFE.left, top: 930, opacity: a, transform: `translateX(${(1 - a) * -40}px)` }}>
      <Critical style={{ display: "inline-block", padding: "16px 30px 18px 26px", background: "rgba(14,12,10,0.86)", borderLeft: `10px solid ${B.gold}` }}>
        <div style={{ fontFamily: serif, fontWeight: 800, fontSize: 64, color: B.cream, lineHeight: 1.05 }}>{name}</div>
        {sub ? <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 30, letterSpacing: 2, color: B.gold, marginTop: 6, textTransform: "uppercase" }}>{sub}</div> : null}
      </Critical>
    </div>
  );
};

export const YearCounter: React.FC<{ from: number; to: number; duration: number }> = ({ from, to, duration }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [4, Math.max(5, duration * 0.7)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT });
  const year = Math.round(from + (to - from) * p);
  return (
    <div style={{ position: "absolute", left: SAFE.left, top: 190, opacity: reveal(frame, 0, 8) }}>
      <Critical style={{ fontFamily: serif, fontWeight: 900, fontSize: 150, lineHeight: 1, color: B.gold, textShadow: "0 6px 30px rgba(0,0,0,0.8)", fontVariantNumeric: "tabular-nums" }}>
        {year}
      </Critical>
    </div>
  );
};

export const PinChip: React.FC<{ label: string; sub?: string; top: number }> = ({ label, sub, top }) => {
  const frame = useCurrentFrame();
  const a = reveal(frame, 6, 12);
  return (
    <div style={{ position: "absolute", left: SAFE.left, top, opacity: a, transform: `translateY(${(1 - a) * 20}px)` }}>
      <Critical style={{ display: "flex", alignItems: "center", gap: 18, padding: "14px 28px 14px 20px", background: "rgba(14,12,10,0.82)", borderRadius: 60, border: `3px solid ${B.gold}` }}>
        <svg width={40} height={52} viewBox="0 0 40 52">
          <path d="M 20 50 C 20 50 2 28 2 18 A 18 18 0 0 1 38 18 C 38 28 20 50 20 50 Z" fill={B.gold} />
          <circle cx={20} cy={18} r={7} fill={B.black} />
        </svg>
        <div>
          <div style={{ fontFamily: serif, fontWeight: 800, fontSize: 46, color: B.cream, lineHeight: 1.05 }}>{label}</div>
          {sub ? <div style={{ fontFamily: sans, fontWeight: 600, fontSize: 24, letterSpacing: 2, color: B.gold, textTransform: "uppercase" }}>{sub}</div> : null}
        </div>
      </Critical>
    </div>
  );
};

export const Stamp: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [4, 10, 14], [1.12, 0.97, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: SAFE.left, width: SAFE_W, top: 190, display: "flex", justifyContent: "flex-start", opacity: frame >= 4 ? 1 : 0 }}>
      <Critical
        style={{
          fontFamily: serif,
          fontWeight: 900,
          fontSize: 96,
          color: B.black,
          background: B.gold,
          padding: "8px 34px 14px",
          transform: `rotate(-3deg) scale(${s})`,
          transformOrigin: "0% 50%",
          boxShadow: "0 18px 40px rgba(0,0,0,0.55)",
          textTransform: "uppercase",
        }}
      >
        {text}
      </Critical>
    </div>
  );
};

/* ------------------------------------------------------------- then / now */

/**
 * Then and now: the old photo (sepia) fills the frame, then a gold line sweeps left to right and
 * reveals today's photo (in colour) of the same place. The year chip switches when the line passes
 * the middle. Both photos hold still apart from a very slow push, so the wipe is the only motion.
 */
export const ThenNowBeat: React.FC<{ beat: ReelBeat; spec: ReelSpec; duration: number }> = ({ beat, spec, duration }) => {
  const frame = useCurrentFrame();
  const { width: W, height: H } = useVideoConfig();
  const qc = useContext(QCContext);
  const v = beat.visual;
  const thenKey = v.then ?? "";
  const nowKey = v.now ?? "";
  const push = interpolate(frame, [0, duration], [1.0, 1.03], { extrapolateRight: "clamp" });
  const tSize = imgSize(spec, thenKey);
  const nSize = imgSize(spec, nowKey);
  const anchor: [number, number] = v.anchor ?? [0.5, 0.42];
  const tRect = coverCrop(tSize.width, tSize.height, W, H, v.thenCrop ?? [0, 0, 1, 1], v.thenFocus ?? v.focus ?? [0.5, 0.45], anchor, push);
  const nRect = coverCrop(nSize.width, nSize.height, W, H, v.nowCrop ?? [0, 0, 1, 1], v.nowFocus ?? v.focus ?? [0.5, 0.45], anchor, push);
  // the wipe runs through the middle of the beat, so each picture is seen on its own first
  const p = interpolate(frame, [duration * 0.32, duration * 0.68], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: EASE_IN_OUT });
  const x = p * W;
  const label = p < 0.5 ? v.thenLabel ?? "THEN" : v.nowLabel ?? "TODAY";
  const chip = (
    <div style={{ position: "absolute", left: SAFE.left, top: 190 }}>
      <Critical
        style={{
          fontFamily: serif,
          fontWeight: 900,
          fontSize: 96,
          lineHeight: 1,
          color: p < 0.5 ? B.gold : B.cream,
          textShadow: "0 6px 30px rgba(0,0,0,0.85)",
        }}
      >
        {label}
      </Critical>
    </div>
  );
  if (qc) return <AbsoluteFill>{chip}</AbsoluteFill>;
  return (
    <AbsoluteFill style={{ backgroundColor: B.black, overflow: "hidden" }}>
      <Img src={staticFile(`pd/${spec.id}/${thenKey}.jpg`)} style={{ position: "absolute", ...toCss(tRect), filter: SEPIA }} />
      <AbsoluteFill style={{ clipPath: `inset(0 ${W - x}px 0 0)` }}>
        <Img src={staticFile(`pd/${spec.id}/${nowKey}.jpg`)} style={{ position: "absolute", ...toCss(nRect), filter: "saturate(0.9) contrast(1.04)" }} />
      </AbsoluteFill>
      {p > 0 && p < 1 ? (
        <div style={{ position: "absolute", left: x - 4, top: 0, width: 8, height: H, background: B.gold, boxShadow: "0 0 24px rgba(226,178,74,0.8)" }} />
      ) : null}
      <Grade />
      {chip}
    </AbsoluteFill>
  );
};

/* ----------------------------------------------------------- title card */

/**
 * Typographic card for beats with no fitting picture: a big gold line (a year, a date) and a cream
 * sub-line, on black with a faint gold glow. Used instead of re-using a photo.
 */
export const TitleCard: React.FC<{ title: string; sub?: string }> = ({ title, sub }) => {
  const frame = useCurrentFrame();
  const qc = useContext(QCContext);
  const a = reveal(frame, 0, 12);
  const b = reveal(frame, 8, 12);
  return (
    <AbsoluteFill style={{ backgroundColor: qc ? "transparent" : B.black }}>
      {qc ? null : <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 38%, rgba(226,178,74,0.14) 0%, rgba(14,12,10,0) 62%)" }} />}
      <div style={{ position: "absolute", left: CENTER_COL.left, width: CENTER_COL.width, top: 470, display: "flex", flexDirection: "column", alignItems: "center", gap: 28, textAlign: "center" }}>
        <Critical style={{ fontFamily: serif, fontWeight: 900, fontSize: title.length > 6 ? 150 : 230, lineHeight: 1, color: B.gold, opacity: a, transform: `translateY(${(1 - a) * 24}px)` }}>
          {title}
        </Critical>
        <Critical style={{ height: 6, width: 160, background: B.gold, opacity: b }}>{""}</Critical>
        {sub ? (
          <Critical style={{ fontFamily: serif, fontStyle: "italic", fontSize: 58, lineHeight: 1.15, color: B.cream, opacity: b, maxWidth: CENTER_COL.width }}>
            {sub}
          </Critical>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/* -------------------------------------------------------------- end card */

export const EndCard: React.FC<{ page: string; line: string }> = ({ page, line }) => {
  const frame = useCurrentFrame();
  const qc = useContext(QCContext);
  const a = reveal(frame, 0, 10);
  const b = reveal(frame, 8, 12);
  return (
    <AbsoluteFill style={{ backgroundColor: qc ? "transparent" : B.black }}>
      {qc ? null : <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, rgba(226,178,74,0.16) 0%, rgba(14,12,10,0) 60%)" }} />}
      <div style={{ position: "absolute", left: CENTER_COL.left, width: CENTER_COL.width, top: 640, display: "flex", flexDirection: "column", alignItems: "center", gap: 26, textAlign: "center" }}>
        <Critical style={{ fontFamily: sans, fontWeight: 700, fontSize: 40, letterSpacing: 8, color: B.creamDim, textTransform: "uppercase", opacity: a }}>Follow</Critical>
        <Critical style={{ fontFamily: serif, fontWeight: 900, fontSize: 104, lineHeight: 1.02, color: B.gold, opacity: a, transform: `scale(${0.94 + 0.06 * a})` }}>
          {page}
        </Critical>
        <Critical style={{ height: 6, width: 160, background: B.gold, opacity: b }}>{""}</Critical>
        <Critical style={{ fontFamily: serif, fontStyle: "italic", fontSize: 60, color: B.cream, opacity: b }}>{line}</Critical>
      </div>
    </AbsoluteFill>
  );
};

export { SAFE_CX };
