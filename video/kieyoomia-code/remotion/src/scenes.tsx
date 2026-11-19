// Reconstruction scenes: flat 2D drawings that act out a moment the archive never filmed.
// Learned from the scene types that carry Immersive Past's wreck videos (side cross-sections with a moving camera,
// top-down "tactical" plots with clock stamps, icon-grid counters, a slowly turning object under a spotlight),
// redrawn in our own "Darkroom & Ledger" look: graphite/slate tones, warm paper light, grease-pencil red as the only
// accent, Barlow caps + Plex Mono labels. No teal seas, navy panels or their fonts. All shapes are drawn in code:
// no AI images, and people are silhouettes, never realistic faces.
//
//   Section    side cross-section (sea or ground) with keyframed camera, moving figures, torch beams, tunnels,
//              depth/distance ruler, date stamp, keyword pills, countdown ring, name tags.
//   Chart      top-down plot: ships/subs/columns moving along tracks with wakes, sonar cones, contacts,
//              depth-charge bursts, time stamps, running clock.
//   IconCount  grid of hundreds of small icons counting up, then the few that matter turn red.
//   ObjectTurn one object (stamped tag or a real artifact photo cut-out) turning slowly under a spotlight.
//
// All times in props are seconds from the start of the card; world/screen coordinates are pixels (1920x1080 frame).
import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, MONO } from "./theme";
import { Stroke, roughEllipse, useEnv, wobble } from "./marks";

// scene palette: the darkroom's greys and the ledger's paper, nothing saturated except grease red
export const S = {
  sky0: "#dcd8cd", sky1: "#b9b5aa",
  sea0: "#5b6461", sea1: "#323936", sea2: "#151918",
  bed0: "#6e6552", bed1: "#4a4436",
  soil0: "#6d5e47", soil1: "#584b3a", soil2: "#43392d", soil3: "#2f2820",
  steel: "#6f7472", steelHi: "#a3a8a5", steelLo: "#3c403f", line: "#1b1e1d",
  hullLight: "#a7aaa6", cabin: "#c3c4be",
  figure: "#151818", wood: "#8a7152",
  lamp: "245,236,212", // warm torch light (rgb)
  chart: "#171b1a", chartGrid: "#2b3230", chartInk: "#cfccc2",
};

const ez = Easing.inOut(Easing.cubic);
const cl = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };
type Key = { t: number; [k: string]: number };

/** Interpolate keyframes {t, a, b, ...} at time t (eased per segment unless linear). */
export const track = (keys: Key[], t: number, linear = false): Record<string, number> => {
  if (!keys || !keys.length) return {};
  if (keys.length === 1 || t <= keys[0].t) return keys[0];
  let i = 0;
  while (i < keys.length - 2 && t > keys[i + 1].t) i++;
  const a = keys[i], b = keys[i + 1];
  const raw = Math.min(1, Math.max(0, (t - a.t) / Math.max(1e-6, b.t - a.t)));
  const p = linear ? raw : ez(raw);
  const out: Record<string, number> = {};
  for (const k of Object.keys(b)) if (k !== "t") out[k] = (a[k] ?? b[k]) + (b[k] - (a[k] ?? b[k])) * p;
  return out;
};

const rnd = (seed: number) => {
  let s = (seed * 7919) % 233280;
  return () => ((s = (s * 9301 + 49297) % 233280) / 233280);
};

/** Point and angle at distance d along a polyline. */
const along = (pts: number[][], d: number) => {
  let acc = 0;
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
    const L = Math.hypot(x1 - x0, y1 - y0);
    if (acc + L >= d || i === pts.length - 2) {
      const t = L ? Math.min(1, Math.max(0, (d - acc) / L)) : 0;
      return { x: x0 + (x1 - x0) * t, y: y0 + (y1 - y0) * t, a: Math.atan2(y1 - y0, x1 - x0) };
    }
    acc += L;
  }
  return { x: pts[0][0], y: pts[0][1], a: 0 };
};
const plen = (pts: number[][]) => pts.slice(1).reduce((s, p, i) => s + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
/** Polyline cut at fraction p of its length. */
const partial = (pts: number[][], p: number) => {
  const L = plen(pts) * Math.min(1, Math.max(0, p));
  const out = [pts[0]];
  let acc = 0;
  for (let i = 0; i < pts.length - 1; i++) {
    const seg = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]);
    if (acc + seg >= L) { const q = along(pts, L); out.push([q.x, q.y]); return out; }
    out.push(pts[i + 1]);
    acc += seg;
  }
  return out;
};
const poly = (pts: number[][]) => "M" + pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join("L");

// ───────────────────────────── shared screen-space furniture ─────────────────────────────

/** Date/place stamp, top left, on every reconstruction (black tab + red square, mono strip). */
export const Stamp: React.FC<{ title?: string; sub?: string; t?: number }> = ({ title, sub }) => {
  const f = useCurrentFrame();
  if (!title) return null;
  const w = interpolate(f, [4, 14], [0, 100], cl);
  const w2 = interpolate(f, [10, 20], [0, 100], cl);
  return (
    <>
      <div style={{ position: "absolute", left: 64, top: 52, clipPath: `inset(0 ${100 - w}% 0 0)`, background: "#0b0b0b", padding: "8px 24px 6px 18px", display: "flex", alignItems: "center", gap: 14 }}>
        <div style={{ width: 14, height: 14, background: C.grease }} />
        <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 44, letterSpacing: 1, textTransform: "uppercase", color: C.light, lineHeight: 1.05 }}>{title}</div>
      </div>
      {sub ? <div style={{ position: "absolute", left: 64, top: 112, clipPath: `inset(0 ${100 - w2}% 0 0)`, background: C.light, padding: "5px 16px 4px", fontFamily: MONO, fontWeight: 500, fontSize: 19, letterSpacing: 1, textTransform: "uppercase", color: C.ink }}>{sub}</div> : null}
    </>
  );
};

/** Keyword pill in the middle of the frame: one fact the narration just said ("230 FEET"). */
const Pills: React.FC<{ pills?: { t0: number; t1: number; text: string; y?: number }[]; t: number }> = ({ pills, t }) => (
  <>
    {(pills || []).map((p, i) => {
      const o = interpolate(t, [p.t0, p.t0 + 0.25, p.t1 - 0.25, p.t1], [0, 1, 1, 0], cl);
      if (o <= 0) return null;
      const u = interpolate(t, [p.t0 + 0.2, p.t0 + 0.6], [0, 1], cl);
      return (
        <div key={i} style={{ position: "absolute", left: 0, right: 0, top: p.y ?? 300, display: "flex", justifyContent: "center", opacity: o, transform: `scale(${0.94 + 0.06 * o})` }}>
          <div style={{ position: "relative", background: "#0b0b0b", padding: "10px 30px 6px", fontFamily: HEAD, fontWeight: 700, fontSize: 64, letterSpacing: 2, color: C.light, textTransform: "uppercase", boxShadow: "0 6px 22px rgba(0,0,0,.45)" }}>
            {p.text}
            <svg width="100%" height="16" viewBox="0 0 100 16" preserveAspectRatio="none" style={{ position: "absolute", left: 0, bottom: -12 }}>
              <Stroke d={wobble([[4, 8], [96, 6]], 7 + i, 1.2)} p={u} w={5} />
            </svg>
          </div>
        </div>
      );
    })}
  </>
);

/** Countdown ring, top right ("20 MINUTES OF AIR"): the red arc empties between t0 and t1. */
const Ring: React.FC<{ ring?: { t0: number; t1: number; label: string }; t: number }> = ({ ring, t }) => {
  if (!ring) return null;
  const o = interpolate(t, [ring.t0 - 0.3, ring.t0], [0, 1], cl);
  const p = interpolate(t, [ring.t0, ring.t1], [1, 0], cl);
  const r = 26, L = 2 * Math.PI * r;
  return (
    <div style={{ position: "absolute", right: 64, top: 52, opacity: o, display: "flex", alignItems: "center", gap: 16, background: "#0b0b0b", padding: "10px 14px 10px 22px" }}>
      <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 20, letterSpacing: 1.5, color: C.light, textTransform: "uppercase" }}>{ring.label}</div>
      <svg width={64} height={64} viewBox="0 0 64 64">
        <circle cx={32} cy={32} r={r} fill="none" stroke="#333" strokeWidth={7} />
        <circle cx={32} cy={32} r={r} fill="none" stroke={C.grease} strokeWidth={7} strokeDasharray={L} strokeDashoffset={L * (1 - p)} transform="rotate(-90 32 32)" strokeLinecap="round" />
      </svg>
    </div>
  );
};

/** Name tag with a leader line, pinned to a screen point (a diver, a ship, a man in a tunnel). */
const NameTag: React.FC<{ x: number; y: number; text: string; o: number; up?: number }> = ({ x, y, text, o, up = 70 }) => (
  <div style={{ position: "absolute", left: 0, top: 0, opacity: o }}>
    <svg width={1920} height={1080} style={{ position: "absolute" }}>
      <line x1={x} y1={y - 8} x2={x} y2={y - up} stroke={C.light} strokeWidth={2} opacity={0.85} />
      <circle cx={x} cy={y - 6} r={4} fill={C.grease} />
    </svg>
    <div style={{ position: "absolute", left: x, top: y - up - 34, transform: "translateX(-50%)", whiteSpace: "nowrap", background: "#0b0b0b", padding: "5px 12px 4px 10px", display: "flex", alignItems: "center", gap: 8, fontFamily: MONO, fontWeight: 500, fontSize: 18, letterSpacing: 1.2, color: C.light, textTransform: "uppercase" }}>
      <div style={{ width: 8, height: 8, background: C.grease }} />{text}
    </div>
  </div>
);

const SourceLine: React.FC<{ text?: string; left?: boolean }> = ({ text, left }) =>
  text ? <div style={{ position: "absolute", [left ? "left" : "right"]: 64, bottom: 40, fontFamily: MONO, fontSize: 16, letterSpacing: 1, color: "rgba(236,233,225,.7)", textTransform: "uppercase", textShadow: "0 1px 3px rgba(0,0,0,.8)" }}>{text}</div> : null;

// ───────────────────────────── drawn elements (side view) ─────────────────────────────
// Each faces right at flip=false; origin: hull/body centre (vessels at the waterline), feet for standing men.

const UBoat: React.FC<{ hole?: number; wreck?: boolean }> = ({ hole, wreck }) => (
  <g>
    <path d="M-500,-26 L-470,-34 L-462,30 L-500,22 Z" fill={S.steelLo} stroke={S.line} strokeWidth={3} />
    <path d="M-460,4 C-430,-24 -320,-36 -200,-38 L300,-38 C380,-37 440,-22 472,-2 C440,20 380,36 300,38 L-200,38 C-320,36 -430,28 -460,4 Z" fill={S.steel} stroke={S.line} strokeWidth={3} />
    <path d="M-430,-12 C-380,-28 -300,-35 -200,-36 L300,-36 C370,-35 420,-26 452,-12 Z" fill={S.steelHi} opacity={0.35} />
    <path d="M-445,14 L462,8 C432,24 380,35 300,37 L-200,37 C-320,35 -420,27 -445,14 Z" fill={S.steelLo} opacity={0.55} />
    <path d="M-400,-38 L-388,-50 L422,-50 L442,-38 Z" fill={S.steel} stroke={S.line} strokeWidth={2.5} />
    {Array.from({ length: 30 }, (_, i) => <rect key={i} x={-350 + i * 24} y={-29} width={11} height={5} rx={1.5} fill={S.line} opacity={0.7} />)}
    <path d="M-60,-50 L-48,-118 L70,-124 L108,-104 L112,-50 Z" fill={S.steel} stroke={S.line} strokeWidth={3} />
    <path d="M-48,-118 L70,-124 L108,-104 L-45,-102 Z" fill={S.steelHi} opacity={0.3} />
    <line x1={12} y1={-124} x2={16} y2={-178} stroke={S.line} strokeWidth={5} />
    <line x1={42} y1={-122} x2={44} y2={-160} stroke={S.line} strokeWidth={4} />
    <path d="M188,-50 L194,-66 L216,-66 L222,-50 Z" fill={S.line} />
    <line x1={205} y1={-61} x2={292} y2={-69} stroke={S.line} strokeWidth={6} strokeLinecap="round" />
    <path d="M-420,22 L-474,38 L-412,32 Z" fill={S.steelLo} stroke={S.line} strokeWidth={2} />
    <path d="M400,16 L448,30 L392,28 Z" fill={S.steelLo} stroke={S.line} strokeWidth={2} />
    {hole !== undefined ? (
      <g transform={`translate(${hole},0)`}>
        <path d="M-70,-40 L-52,-8 L-78,10 L-48,24 L-60,40 L-10,30 L20,44 L38,22 L74,30 L58,2 L80,-20 L44,-24 L30,-46 L-4,-30 L-30,-48 Z" fill="#0a0c0c" stroke={S.steelHi} strokeWidth={2} strokeLinejoin="round" />
        <path d="M-40,-10 L-20,4 L0,-6 L22,8 L40,-2" fill="none" stroke={S.steelLo} strokeWidth={3} />
      </g>
    ) : null}
    {wreck ? Array.from({ length: 70 }, (_, i) => {
      const r = rnd(i + 3);
      return <circle key={i} cx={-440 + r() * 900} cy={-46 + r() * 80} r={1.5 + r() * 3} fill={r() > 0.5 ? "#4e5550" : "#8b8f86"} opacity={0.55} />;
    }) : null}
  </g>
);

const DiveBoat: React.FC = () => (
  <g>
    <path d="M-180,-34 L196,-34 C190,-10 172,8 150,20 L-160,20 C-170,6 -178,-12 -180,-34 Z" fill={S.hullLight} stroke={S.line} strokeWidth={3} />
    <rect x={-180} y={-4} width={360} height={7} fill={S.line} opacity={0.6} />
    <path d="M-110,-34 L-110,-92 L20,-92 L34,-34 Z" fill={S.cabin} stroke={S.line} strokeWidth={3} />
    {[-96, -60, -24].map((x) => <rect key={x} x={x} y={-80} width={26} height={16} fill={S.line} opacity={0.8} />)}
    <line x1={-60} y1={-92} x2={-60} y2={-150} stroke={S.line} strokeWidth={4} />
    <line x1={-60} y1={-130} x2={-20} y2={-124} stroke={S.line} strokeWidth={2} />
    {[70, 104, 136].map((x, i) => (
      <g key={x} transform={`translate(${x},-34)`}>
        <rect x={-6} y={-38} width={12} height={38} rx={4} fill={S.figure} />
        <circle cx={0} cy={-46} r={7} fill={S.figure} />
      </g>
    ))}
  </g>
);

const Escort: React.FC = () => (
  <g>
    <path d="M-380,-26 L396,-34 C380,-8 360,8 340,14 L-356,14 C-370,0 -378,-14 -380,-26 Z" fill={S.hullLight} stroke={S.line} strokeWidth={3} />
    <rect x={-376} y={0} width={740} height={6} fill={S.line} opacity={0.55} />
    <path d="M-160,-30 L-160,-76 L60,-76 L60,-32 Z" fill={S.cabin} stroke={S.line} strokeWidth={3} />
    <path d="M0,-76 L0,-118 L44,-118 L50,-76 Z" fill={S.cabin} stroke={S.line} strokeWidth={3} />
    <path d="M-90,-76 L-84,-120 L-50,-120 L-46,-76 Z" fill={S.steel} stroke={S.line} strokeWidth={3} />
    <line x1={20} y1={-118} x2={20} y2={-190} stroke={S.line} strokeWidth={4} />
    <line x1={-10} y1={-170} x2={50} y2={-170} stroke={S.line} strokeWidth={3} />
    <path d="M220,-32 L226,-48 L252,-48 L258,-32 Z" fill={S.steel} stroke={S.line} strokeWidth={2} />
    <line x1={240} y1={-42} x2={300} y2={-48} stroke={S.line} strokeWidth={5} />
    <path d="M-300,-26 L-294,-42 L-266,-42 L-260,-26 Z" fill={S.steel} stroke={S.line} strokeWidth={2} />
  </g>
);

const Diver: React.FC<{ t: number; seed: number }> = ({ t, seed }) => {
  const kick = Math.sin(t * 5 + seed) * 6;
  return (
    <g>
      <path d={`M-56,-2 L-88,${-12 + kick} L-90,${4 + kick} Z`} fill={S.figure} />
      <path d={`M-56,4 L-84,${14 - kick} L-82,${24 - kick} Z`} fill={S.figure} />
      <path d="M-60,-3 L-20,-7 L-18,7 L-58,7 Z" fill={S.figure} />
      <ellipse cx={6} cy={0} rx={31} ry={11} fill={S.figure} />
      <rect x={-22} y={-21} width={46} height={12} rx={6} fill={S.steelHi} stroke={S.figure} strokeWidth={2} />
      <circle cx={43} cy={-3} r={10} fill={S.figure} />
      <rect x={45} y={-8} width={9} height={6} rx={1.5} fill="#bfc8c4" />
      <path d="M22,4 L58,10" stroke={S.figure} strokeWidth={7} strokeLinecap="round" />
      <rect x={54} y={6} width={12} height={8} rx={2} fill={S.steelLo} />
    </g>
  );
};

const Man: React.FC<{ pose?: string; t: number; seed: number }> = ({ pose, t, seed }) => {
  if (pose === "crawl") {
    const a = Math.sin(t * 4 + seed) * 5;
    return (
      <g>
        <ellipse cx={0} cy={-14} rx={36} ry={11} fill={S.figure} />
        <circle cx={44} cy={-20} r={10} fill={S.figure} />
        <path d={`M28,-8 L${52 + a},2`} stroke={S.figure} strokeWidth={7} strokeLinecap="round" />
        <path d={`M-30,-10 L-66,${-4 - a}`} stroke={S.figure} strokeWidth={8} strokeLinecap="round" />
        <path d={`M-30,-16 L-64,${-18 + a}`} stroke={S.figure} strokeWidth={8} strokeLinecap="round" />
      </g>
    );
  }
  const step = pose === "walk" ? Math.sin(t * 6 + seed) * 8 : 0;
  return (
    <g>
      <path d={`M-4,-40 L${-8 - step},0`} stroke={S.figure} strokeWidth={9} strokeLinecap="round" />
      <path d={`M4,-40 L${8 + step},0`} stroke={S.figure} strokeWidth={9} strokeLinecap="round" />
      <rect x={-11} y={-84} width={22} height={48} rx={8} fill={S.figure} />
      <path d={`M-8,-78 L${-14 + step / 2},-46 M8,-78 L${14 - step / 2},-46`} stroke={S.figure} strokeWidth={7} strokeLinecap="round" />
      <circle cx={0} cy={-96} r={10} fill={S.figure} />
    </g>
  );
};

const Hut: React.FC<{ w?: number }> = ({ w = 420 }) => (
  <g>
    <rect x={-w / 2} y={-110} width={w} height={110} fill="#8d8572" stroke={S.line} strokeWidth={3} />
    <path d={`M${-w / 2 - 20},-110 L0,-170 L${w / 2 + 20},-110 Z`} fill="#4f4a3f" stroke={S.line} strokeWidth={3} />
    {Array.from({ length: Math.floor(w / 70) }, (_, i) => <rect key={i} x={-w / 2 + 30 + i * 70} y={-80} width={30} height={26} fill={S.line} opacity={0.75} />)}
    <rect x={-w / 2 - 6} y={-6} width={w + 12} height={8} fill={S.line} opacity={0.5} />
  </g>
);

const Fence: React.FC<{ w?: number }> = ({ w = 600 }) => (
  <g>
    {Array.from({ length: Math.floor(w / 60) + 1 }, (_, i) => <line key={i} x1={-w / 2 + i * 60} y1={0} x2={-w / 2 + i * 60} y2={-140} stroke={S.line} strokeWidth={5} />)}
    {[-30, -62, -94, -126].map((y) => <path key={y} d={wobble([[-w / 2, y], [w / 2, y]], y, 1.5)} fill="none" stroke={S.line} strokeWidth={1.6} />)}
  </g>
);

const Tower: React.FC = () => (
  <g>
    <path d="M-40,0 L-26,-200 M40,0 L26,-200 M-36,-60 L34,-120 M36,-60 L-34,-120" stroke={S.line} strokeWidth={6} />
    <rect x={-50} y={-250} width={100} height={52} fill="#7a7262" stroke={S.line} strokeWidth={3} />
    <rect x={-38} y={-240} width={76} height={20} fill={S.line} opacity={0.8} />
    <path d="M-62,-250 L0,-284 L62,-250 Z" fill="#4f4a3f" stroke={S.line} strokeWidth={3} />
  </g>
);

const Mound: React.FC<{ w?: number }> = ({ w = 300 }) => (
  <path d={`M${-w / 2},6 C${-w / 4},-34 ${w / 4},-30 ${w / 2},6 Z`} fill={S.bed0} />
);

// ───────────────────────────── Section ─────────────────────────────

type SItem = {
  kind: "uboat" | "boat" | "escort" | "diver" | "man" | "hut" | "fence" | "tower" | "mound" | "tunnel" | "rope";
  x?: number; y?: number; s?: number; flip?: boolean; rot?: number;
  move?: Key[]; linear?: boolean; pose?: string;
  label?: string; labelAt?: number; labelTo?: number; labelUp?: number;
  beam?: number; beamLen?: number; beamAt?: number;
  hole?: number; wreck?: boolean; w?: number;
  pts?: number[][]; dig?: [number, number]; // tunnel / rope polyline and when it is dug (s)
  follow?: number; lag?: number; // ride the dig front of items[follow] (a tunnel), lag px behind it
  t0?: number; t1?: number; // visibility window (s)
};

export type SectionProps = {
  world?: "sea" | "ground";
  W?: number; H?: number; surface?: number; floor?: number;
  date?: string; place?: string;
  items: SItem[];
  cam: Key[]; // {t, x, y, z}: world point at screen centre and zoom
  ruler?: { unit: string; per: number; step: number; max: number };
  pills?: { t0: number; t1: number; text: string; y?: number }[];
  ring?: { t0: number; t1: number; label: string };
  source?: string;
};

export const Section: React.FC<SectionProps> = (p) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const o = useEnv(8, 8);
  const W = p.W ?? 4000, H = p.H ?? 1600, sf = p.surface ?? 420, fl = p.floor ?? 1250;
  const sea = (p.world ?? "sea") === "sea";
  const cam = track(p.cam, t) as { x: number; y: number; z: number };
  const toScreen = (x: number, y: number) => [(x - cam.x) * cam.z + 960, (y - cam.y) * cam.z + 540];
  const front = (tn: SItem, lag = 0) => {
    const prog = interpolate(t, tn.dig ?? [0, 0.001], [0, 1], cl);
    const L = plen(tn.pts!) * prog;
    const q = along(tn.pts!, Math.max(0, L - lag));
    return { x: q.x, y: q.y, a: (q.a * 180) / Math.PI };
  };
  const pos = (it: SItem): { x: number; y: number; rot?: number } => {
    if (it.follow !== undefined) {
      const q = front(p.items[it.follow], it.lag ?? 60);
      const up = Math.abs(Math.cos((q.a * Math.PI) / 180)) < 0.5; // in a shaft the body turns head-first along it
      return { x: q.x, y: q.y + (up ? 0 : 14 * (it.s ?? 1)), rot: q.a };
    }
    return (it.move ? track(it.move, t, it.linear) : { x: it.x ?? 0, y: it.y ?? 0, rot: it.rot ?? 0 }) as { x: number; y: number; rot?: number };
  };
  const vis = (it: SItem) => (it.t0 === undefined || t >= it.t0) && (it.t1 === undefined || t <= it.t1);
  const wave = (y: number, amp: number, ph: number) => {
    const pts: string[] = [];
    for (let x = -200; x <= W + 200; x += 40) pts.push(`${x},${(y + Math.sin(x / 90 + ph) * amp + Math.sin(x / 37 + ph * 1.7) * amp * 0.4).toFixed(1)}`);
    return pts.join(" L");
  };
  const r0 = rnd(11);
  const snow = Array.from({ length: 140 }, () => [r0() * W, sf + r0() * (fl - sf), 0.6 + r0() * 1.8, r0()]);
  const r1 = rnd(5);
  const pebbles = Array.from({ length: 160 }, () => [r1() * W, sf + 40 + r1() * (H - sf), 2 + r1() * 6]);

  const body = (it: SItem, i: number) => {
    if (!vis(it)) return null;
    if (it.kind === "tunnel" && it.pts) {
      const [d0, d1] = it.dig ?? [0, 0.001];
      const prog = interpolate(t, [d0, d1], [0, 1], cl);
      const cut = partial(it.pts, prog);
      const L = plen(cut);
      const frames = Array.from({ length: Math.floor(L / 80) }, (_, k) => along(cut, 40 + k * 80));
      const w = it.w ?? 54;
      return (
        <g key={i}>
          <path d={poly(cut)} fill="none" stroke="#120f0b" strokeWidth={w} strokeLinejoin="round" strokeLinecap="round" />
          <path d={poly(cut)} fill="none" stroke="#7a6a52" strokeWidth={w - 14} strokeLinejoin="round" strokeLinecap="round" />
          <path d={poly(cut)} fill="none" stroke="#9a8a6e" strokeWidth={6} strokeLinejoin="round" strokeLinecap="round" opacity={0.5} transform="translate(0,-12)" />
          {frames.map((q, k) => {
            const nx = -Math.sin(q.a) * (w / 2), ny = Math.cos(q.a) * (w / 2);
            return <line key={k} x1={q.x - nx} y1={q.y - ny} x2={q.x + nx} y2={q.y + ny} stroke="#3e3123" strokeWidth={7} />;
          })}
        </g>
      );
    }
    if (it.kind === "rope" && it.pts) {
      return <path key={i} d={poly(it.pts)} fill="none" stroke="#d8d2c2" strokeWidth={2.5} opacity={0.8} />;
    }
    const q = pos(it);
    const s = it.s ?? 1;
    const tr = `translate(${q.x},${q.y}) rotate(${q.rot ?? it.rot ?? 0}) scale(${it.flip ? -s : s},${s})`;
    const bob = it.kind === "boat" || it.kind === "escort" ? Math.sin(t * 1.4 + i) * 3 : 0;
    let el: React.ReactNode = null;
    if (it.kind === "uboat") el = <UBoat hole={it.hole} wreck={it.wreck} />;
    if (it.kind === "boat") el = <DiveBoat />;
    if (it.kind === "escort") el = <Escort />;
    if (it.kind === "diver") el = <Diver t={t} seed={i} />;
    if (it.kind === "man") el = <Man pose={it.pose} t={t} seed={i} />;
    if (it.kind === "hut") el = <Hut w={it.w} />;
    if (it.kind === "fence") el = <Fence w={it.w} />;
    if (it.kind === "tower") el = <Tower />;
    if (it.kind === "mound") el = <Mound w={it.w} />;
    return <g key={i} transform={`translate(0,${bob}) ${tr}`}>{el}</g>;
  };

  // torch beams, drawn with screen blending above everything
  const beams = p.items.map((it, i) => {
    if (it.beam === undefined || !vis(it)) return null;
    const on = interpolate(t, [it.beamAt ?? 0, (it.beamAt ?? 0) + 0.4], [0, 1], cl);
    const q = pos(it);
    const s = it.s ?? 1, dir = it.flip ? -1 : 1;
    const rr = (((q.rot ?? it.rot ?? 0) as number) * Math.PI) / 180;
    const lx = 62 * s * dir, ly = 10 * s;
    const hx = q.x + lx * Math.cos(rr) - ly * Math.sin(rr), hy = q.y + lx * Math.sin(rr) + ly * Math.cos(rr);
    const ang = ((((q.rot ?? it.rot ?? 0) as number) + (it.flip ? 180 - it.beam : it.beam)) * Math.PI) / 180; // beam is relative to the body
    const L = (it.beamLen ?? 520) * s, spread = 0.2 + Math.sin(t * 2 + i) * 0.015;
    const a1 = ang - spread, a2 = ang + spread;
    return (
      <g key={`b${i}`} opacity={on * (0.92 + Math.sin(t * 9 + i) * 0.04)}>
        <defs>
          <radialGradient id={`bg${i}`} cx={hx} cy={hy} r={L} gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor={`rgb(${S.lamp})`} stopOpacity={0.85} />
            <stop offset="0.55" stopColor={`rgb(${S.lamp})`} stopOpacity={0.25} />
            <stop offset="1" stopColor={`rgb(${S.lamp})`} stopOpacity={0} />
          </radialGradient>
        </defs>
        <path d={`M${hx},${hy} L${hx + Math.cos(a1) * L},${hy + Math.sin(a1) * L} A${L},${L} 0 0 1 ${hx + Math.cos(a2) * L},${hy + Math.sin(a2) * L} Z`} fill={`url(#bg${i})`} style={{ mixBlendMode: "screen" }} />
      </g>
    );
  });

  const bubbles = p.items.flatMap((it, i) => {
    if (it.kind !== "diver" || !vis(it)) return [];
    const q = pos(it);
    const s = it.s ?? 1, dir = it.flip ? -1 : 1;
    return Array.from({ length: 6 }, (_, k) => {
      const age = ((t * 0.9 + k / 6 + i * 0.13) % 1);
      return <circle key={`bb${i}-${k}`} cx={q.x + (40 * dir + Math.sin(age * 12 + k) * 6) * s} cy={q.y - 14 * s - age * 160 * s} r={(2 + age * 4) * s} fill="none" stroke="#d9e0dc" strokeWidth={1.5} opacity={0.7 * (1 - age)} />;
    });
  });

  // ruler: depth (sea) or depth below ground, right edge, follows the camera
  const ruler = p.ruler ? (() => {
    const ticks = [];
    for (let v = 0; v <= p.ruler!.max; v += p.ruler!.step) {
      const [, y] = toScreen(0, sf + v * p.ruler!.per);
      if (y < 30 || y > 1050) continue;
      ticks.push(
        <g key={v}>
          <line x1={1836} y1={y} x2={1860} y2={y} stroke={C.light} strokeWidth={2} />
          <text x={1828} y={y + 6} textAnchor="end" fontFamily={MONO} fontSize={17} fill={C.light} letterSpacing={1}>{v === 0 ? "0" : `${v} ${p.ruler!.unit}`}</text>
        </g>
      );
    }
    return <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}><line x1={1860} y1={0} x2={1860} y2={1080} stroke={C.light} strokeWidth={1.5} opacity={0.6} />{ticks}</svg>;
  })() : null;

  const tags = p.items.map((it, i) => {
    if (!it.label || !vis(it)) return null;
    const a = it.labelAt ?? 0.5, b = it.labelTo ?? 999;
    const lo = interpolate(t, [a, a + 0.3, b - 0.3, b], [0, 1, 1, 0], cl);
    if (lo <= 0) return null;
    const q = it.kind === "tunnel" && it.pts ? (() => { const c = partial(it.pts!, interpolate(t, it.dig ?? [0, 0.001], [0, 1], cl)); const e = c[c.length - 1]; return { x: e[0], y: e[1] }; })() : pos(it);
    const [x, y] = toScreen(q.x, q.y - (it.kind === "man" ? 100 * (it.s ?? 1) : it.kind === "uboat" ? 120 * (it.s ?? 1) : it.kind === "boat" || it.kind === "escort" ? 90 * (it.s ?? 1) : 20 * (it.s ?? 1)));
    return <NameTag key={`t${i}`} x={x} y={y} text={it.label} o={lo} up={it.labelUp} />;
  });

  return (
    <AbsoluteFill style={{ opacity: o, background: S.sea2, overflow: "hidden" }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={S.sky1} /><stop offset="1" stopColor={S.sky0} /></linearGradient>
          <linearGradient id="sea" gradientUnits="userSpaceOnUse" x1="0" y1={sf} x2="0" y2={fl}><stop offset="0" stopColor={S.sea0} /><stop offset="0.45" stopColor={S.sea1} /><stop offset="1" stopColor={S.sea2} /></linearGradient>
          <linearGradient id="bed" gradientUnits="userSpaceOnUse" x1="0" y1={fl} x2="0" y2={H}><stop offset="0" stopColor={S.bed0} /><stop offset="1" stopColor={S.bed1} /></linearGradient>
          <filter id="sgrain"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="4" /><feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0.07 0" /></filter>
        </defs>
        <g transform={`translate(960,540) scale(${cam.z}) translate(${-cam.x},${-cam.y})`}>
          <rect x={-400} y={-1000} width={W + 800} height={sf + 1000} fill="url(#sky)" />
          {sea ? (
            <>
              <path d={`M-200,${sf} L${wave(sf, 4, t * 1.3)} L${W + 200},${H + 400} L-200,${H + 400} Z`} fill="url(#sea)" />
              {[0, 1, 2, 3, 4].map((k) => {
                const x = (k * 900 + t * 12) % (W + 400) - 200;
                return <path key={k} d={`M${x},${sf} L${x + 160},${sf} L${x + 520},${fl} L${x + 280},${fl} Z`} fill="#e9e6da" opacity={0.045} />;
              })}
              {snow.map(([x, y, r, ph], k) => <circle key={k} cx={x + Math.sin(t * 0.5 + ph * 6) * 10} cy={y + ((t * 6 * (0.5 + ph)) % 60)} r={r} fill="#cfd3cc" opacity={0.25} />)}
              <path d={`M-200,${fl} L${wave(fl, 10, 0.4)} L${W + 200},${H + 400} L-200,${H + 400} Z`} fill="url(#bed)" />
              <path d={`M-200,${fl + 30} L${wave(fl + 30, 8, 2.1)}`} fill="none" stroke={S.bed1} strokeWidth={3} opacity={0.6} />
              <path d={`M-200,${sf} L${wave(sf, 4, t * 1.3)}`} fill="none" stroke="#eeebe1" strokeWidth={3} opacity={0.8} />
            </>
          ) : (
            <>
              {[[sf, S.soil0], [sf + 140, S.soil1], [sf + 360, S.soil2], [sf + 640, S.soil3]].map(([y, c], k) => (
                <path key={k} d={`M-200,${y} L${wave(y as number, k ? 9 : 2, k * 1.9)} L${W + 200},${H + 600} L-200,${H + 600} Z`} fill={c as string} />
              ))}
              {pebbles.map(([x, y, r], k) => <ellipse key={k} cx={x} cy={y} rx={r} ry={r * 0.7} fill="#2a241c" opacity={0.35} />)}
              <path d={`M-200,${sf} L${wave(sf, 2, 0)}`} fill="none" stroke="#3d3a2c" strokeWidth={6} />
            </>
          )}
          {p.items.map(body)}
          {bubbles}
          {beams}
        </g>
        <rect width={1920} height={1080} filter="url(#sgrain)" />
        <rect width={1920} height={1080} fill="url(#vig)" />
        <defs><radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="0.6" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.45} /></radialGradient></defs>
      </svg>
      {ruler}
      {tags}
      <Stamp title={p.date} sub={p.place} />
      <Ring ring={p.ring} t={t} />
      <Pills pills={p.pills} t={t} />
      <SourceLine text={p.source} left />
    </AbsoluteFill>
  );
};

// ───────────────────────────── Chart (top-down plot) ─────────────────────────────

type Track = { label?: string; kind?: "escort" | "sub" | "cargo" | "column"; pts: number[][]; t0: number; t1: number; sonar?: [number, number]; labelAt?: number };
export type ChartProps = {
  head: string; date?: string;
  clock?: { t0: number; t1: number; from: string; to: string };
  tracks: Track[];
  contacts?: { t: number; x: number; y: number; label: string }[];
  booms?: { t: number; x: number; y: number; n?: number }[];
  stamps?: { t: number; x: number; y: number; text: string }[];
  coast?: number[][];
  zoom?: [number, number];
  source?: string;
};

const TopHull: React.FC<{ kind?: string }> = ({ kind }) => {
  if (kind === "sub") return <path d="M-46,-6 L30,-6 Q48,0 30,6 L-46,6 Q-52,0 -46,-6 Z M-6,-4 L10,-4 L10,4 L-6,4 Z" fill="#8c908c" stroke={S.line} strokeWidth={1.5} fillRule="evenodd" />;
  if (kind === "cargo") return <g><path d="M-60,-11 L40,-11 Q66,0 40,11 L-60,11 Z" fill="#bdbab0" stroke={S.line} strokeWidth={1.5} />{[-40, -18, 4, 26].map((x) => <rect key={x} x={x} y={-7} width={16} height={14} fill="#8a877e" />)}</g>;
  if (kind === "column") return <g>{[0, 1, 2, 3, 4].map((k) => <circle key={k} cx={-k * 16} cy={0} r={5} fill={C.light} />)}</g>;
  return <g><path d="M-56,-9 L34,-9 Q62,0 34,9 L-56,9 Z" fill={S.hullLight} stroke={S.line} strokeWidth={1.5} /><rect x={-20} y={-5} width={30} height={10} fill="#7d817d" /><circle cx={22} cy={0} r={3.5} fill={S.line} /></g>;
};

export const Chart: React.FC<ChartProps> = (p) => {
  const f = useCurrentFrame();
  const { fps, durationInFrames: d } = useVideoConfig();
  const t = f / fps;
  const o = useEnv(8, 8);
  const z = interpolate(f, [0, d], p.zoom ?? [1.0, 1.08]);
  const clock = p.clock ? (() => {
    const m = (s: string) => { const [h, mm] = s.split(":").map(Number); return h * 60 + mm; };
    const v = Math.round(interpolate(t, [p.clock.t0, p.clock.t1], [m(p.clock.from), m(p.clock.to)], cl));
    return `${String(Math.floor(v / 60) % 24).padStart(2, "0")}:${String(v % 60).padStart(2, "0")}`;
  })() : null;
  const r = rnd(21);
  const flecks = Array.from({ length: 220 }, () => [r() * 1920, r() * 1080, r() * 6.28]);
  return (
    <AbsoluteFill style={{ opacity: o, background: S.chart, overflow: "hidden" }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <defs>
          <filter id="cgrain"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.03" numOctaves="3" seed={8} /><feColorMatrix values="0 0 0 0 0.6  0 0 0 0 0.65  0 0 0 0 0.62  0 0 0 0.10 0" /></filter>
          <radialGradient id="cvig" cx="50%" cy="50%" r="75%"><stop offset="0.55" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.55} /></radialGradient>
        </defs>
        <g transform={`translate(960,540) scale(${z}) translate(-960,-540)`}>
          <rect x={-200} y={-200} width={2320} height={1480} filter="url(#cgrain)" />
          {Array.from({ length: 13 }, (_, k) => <line key={`v${k}`} x1={k * 160} y1={-200} x2={k * 160} y2={1280} stroke={S.chartGrid} strokeWidth={1.2} />)}
          {Array.from({ length: 8 }, (_, k) => <line key={`h${k}`} x1={-200} y1={k * 160} x2={2120} y2={k * 160} stroke={S.chartGrid} strokeWidth={1.2} />)}
          {flecks.map(([x, y, ph], k) => <path key={k} d={`M${x},${y} l${8 + Math.sin(t + ph) * 3},0`} stroke="#9aa39f" strokeWidth={1.2} opacity={0.18} />)}
          {p.coast ? <path d={poly(p.coast) + "L2200,-300L-300,-300Z"} fill="#2a2f2c" stroke={C.light} strokeWidth={2} opacity={0.9} /> : null}
          {p.tracks.map((tr, i) => {
            const prog = interpolate(t, [tr.t0, tr.t1], [0, 1], cl);
            if (t < tr.t0 - 0.2) return null;
            const past = partial(tr.pts, prog);
            const L = plen(tr.pts);
            const q = along(tr.pts, L * prog);
            const deg = (q.a * 180) / Math.PI;
            const so = tr.sonar ? interpolate(t, [tr.sonar[0], tr.sonar[0] + 0.3, tr.sonar[1] - 0.3, tr.sonar[1]], [0, 1, 1, 0], cl) : 0;
            return (
              <g key={i}>
                <path d={poly(tr.pts)} fill="none" stroke={C.light} strokeWidth={1.5} strokeDasharray="6 10" opacity={0.18} />
                <path d={poly(past)} fill="none" stroke="#e8e5da" strokeWidth={14} opacity={0.12} strokeLinecap="round" strokeLinejoin="round" />
                <path d={poly(past)} fill="none" stroke="#f1eee6" strokeWidth={4} opacity={0.55} strokeLinecap="round" strokeLinejoin="round" />
                <g transform={`translate(${q.x},${q.y}) rotate(${deg})`}>
                  {so > 0 ? <path d="M60,0 L330,-95 Q350,0 330,95 Z" fill={C.grease} opacity={0.13 * so} stroke={C.grease} strokeWidth={2} strokeDasharray="8 8" strokeOpacity={0.8 * so} /> : null}
                  <path d="M-60,-10 L-120,-26 M-60,10 L-120,26" stroke="#f1eee6" strokeWidth={2} opacity={0.4} />
                  <TopHull kind={tr.kind} />
                </g>
                {tr.label ? (() => {
                  const lo = interpolate(t, [tr.labelAt ?? tr.t0, (tr.labelAt ?? tr.t0) + 0.4], [0, 1], cl);
                  return <g opacity={lo}><rect x={q.x - 4} y={q.y + 26} width={tr.label.length * 11.5 + 30} height={28} fill="#0b0b0b" /><rect x={q.x + 6} y={q.y + 36} width={8} height={8} fill={C.grease} /><text x={q.x + 22} y={q.y + 46} fontFamily={MONO} fontWeight={500} fontSize={17} letterSpacing={1} fill={C.light}>{tr.label.toUpperCase()}</text></g>;
                })() : null}
              </g>
            );
          })}
          {(p.booms || []).map((b, i) => {
            const n = b.n ?? 5;
            return Array.from({ length: n }, (_, k) => {
              const t0 = b.t + k * 0.35;
              const a = (t - t0) / 1.6;
              if (a < 0) return null;
              const ang = (k / n) * 6.28 + i;
              const cx = b.x + (k ? Math.cos(ang) * 46 : 0), cy = b.y + (k ? Math.sin(ang) * 46 : 0);
              const rr = 10 + Math.min(1, a) * 46;
              return (
                <g key={`${i}-${k}`}>
                  <circle cx={cx} cy={cy} r={rr} fill="#f1eee6" opacity={Math.max(0, 0.9 - a * 0.55) * 0.75} />
                  <circle cx={cx} cy={cy} r={rr * 1.4} fill="none" stroke="#f1eee6" strokeWidth={2} opacity={Math.max(0, 0.6 - a * 0.5)} />
                  <circle cx={cx} cy={cy} r={6} fill={C.grease} opacity={a < 3 ? 0.9 : 0.5} />
                </g>
              );
            });
          })}
          {(p.contacts || []).map((c, i) => {
            const a = interpolate(t, [c.t, c.t + 0.7], [0, 1], cl);
            if (a <= 0) return null;
            return (
              <g key={i}>
                <Stroke d={roughEllipse(c.x, c.y, 34, 34, 30 + i)} p={a} w={4} />
                <line x1={c.x - 52} y1={c.y} x2={c.x + 52} y2={c.y} stroke={C.grease} strokeWidth={2} opacity={a} />
                <line x1={c.x} y1={c.y - 52} x2={c.x} y2={c.y + 52} stroke={C.grease} strokeWidth={2} opacity={a} />
                <g opacity={a}><rect x={c.x + 46} y={c.y - 58} width={c.label.length * 11.5 + 24} height={28} fill="#0b0b0b" /><text x={c.x + 58} y={c.y - 38} fontFamily={MONO} fontWeight={500} fontSize={17} letterSpacing={1} fill={C.light}>{c.label.toUpperCase()}</text></g>
              </g>
            );
          })}
          {(p.stamps || []).map((s, i) => {
            const a = interpolate(t, [s.t, s.t + 0.3], [0, 1], cl);
            return <g key={i} opacity={a}><circle cx={s.x} cy={s.y} r={5} fill={C.light} /><text x={s.x + 12} y={s.y + 6} fontFamily={MONO} fontWeight={500} fontSize={20} fill={C.light}>{s.text}</text></g>;
          })}
        </g>
        <rect width={1920} height={1080} fill="url(#cvig)" />
      </svg>
      <Stamp title={p.head} sub={[clock, p.date].filter(Boolean).join(" · ")} />
      <SourceLine text={p.source} />
    </AbsoluteFill>
  );
};

// ───────────────────────────── IconCount ─────────────────────────────

const Icon: React.FC<{ kind: string }> = ({ kind }) => {
  if (kind === "sub") return <path d="M1,11 Q2,9 6,9 L8,9 L9,6 L12,6 L13,9 L18,9 Q21,10 19,12 L4,12 Q1,12 1,11 Z" />;
  if (kind === "plane") return <path d="M10,2 L11,8 L19,11 L19,12.5 L11,11 L10.6,16 L13,17.5 L13,18.5 L10,17.8 L7,18.5 L7,17.5 L9.4,16 L9,11 L1,12.5 L1,11 L9,8 Z" />;
  if (kind === "ship") return <path d="M1,12 L19,12 L17,16 L3,16 Z M6,8 L13,8 L13,12 L6,12 Z M9,4 L11,4 L11,8 L9,8 Z" />;
  return <path d="M10,2.2 a2.6,2.6 0 1 1 -0.01,0 Z M6.6,7.4 Q10,6.4 13.4,7.4 L14.2,13 L12.6,13 L12.4,18 L10.6,18 L10,13.6 L9.4,18 L7.6,18 L7.4,13 L5.8,13 Z" />;
};

export type IconCountProps = { icon?: "man" | "sub" | "plane" | "ship"; total: number; label: string; accent?: string; highlight?: { n: number; label: string; accent?: string; at: number }; source?: string; file?: string };

export const IconCount: React.FC<IconCountProps> = (p) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const o = useEnv(8, 8);
  const area = { x: 120, y: 110, w: 1680, h: 640 };
  const cell = Math.sqrt((area.w * area.h) / p.total) * 0.98;
  const cols = Math.max(1, Math.floor(area.w / cell)), rows = Math.ceil(p.total / cols);
  const size = Math.min(cell, area.h / rows);
  const ox = area.x + (area.w - cols * size) / 2, oy = area.y + (area.h - rows * size) / 2;
  const fill = interpolate(t, [0.4, 2.6], [0, p.total], { ...cl, easing: Easing.out(Easing.cubic) });
  const h = p.highlight;
  const hp = h ? interpolate(t, [h.at, h.at + 0.8], [0, 1], cl) : 0;
  const picks = new Set<number>();
  if (h) { const r = rnd(4); while (picks.size < Math.min(h.n, p.total)) picks.add(Math.floor(r() * p.total)); }
  const num = h && hp > 0 ? Math.round(interpolate(hp, [0, 1], [p.total, h.n])) : Math.round(fill);
  const lab = h && hp > 0.5 ? h.label : p.label, acc = h && hp > 0.5 ? h.accent : p.accent;
  const words = lab.toUpperCase().split(" ");
  return (
    <AbsoluteFill style={{ opacity: o, background: `radial-gradient(ellipse at 50% 40%, ${C.tableGlow} 0%, ${C.table} 70%)` }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {Array.from({ length: p.total }, (_, i) => {
          const on = Math.min(1, Math.max(0, fill - i + 1));
          if (on <= 0) return null;
          const pick = picks.has(i);
          const col = pick ? (hp > 0 ? C.grease : C.light) : C.light;
          const op = on * (pick ? 0.92 : 0.92 - hp * 0.75);
          const sc = pick ? 1 + hp * 0.25 : 1;
          return (
            <g key={i} transform={`translate(${ox + (i % cols) * size + size / 2},${oy + Math.floor(i / cols) * size + size / 2}) scale(${(size / 22) * 0.86 * sc}) translate(-10,-10)`} fill={col} opacity={op}>
              <Icon kind={p.icon ?? "man"} />
            </g>
          );
        })}
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 790, display: "flex", justifyContent: "center", alignItems: "baseline", gap: 30 }}>
        <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 170, lineHeight: 1, color: h && hp > 0.5 ? C.grease : C.light, fontVariantNumeric: "tabular-nums" }}>{num.toLocaleString("en-US")}</div>
        <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 76, lineHeight: 1, letterSpacing: 1 }}>
          {words.map((w, k) => <span key={k} style={{ color: acc && w === acc.toUpperCase() ? C.grease : C.light }}>{w}{k < words.length - 1 ? " " : ""}</span>)}
        </div>
      </div>
      {p.file ? <div style={{ position: "absolute", left: 120, top: 56, fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: C.lightSoft }}>{p.file}</div> : null}
      <SourceLine text={p.source} />
    </AbsoluteFill>
  );
};

// ───────────────────────────── ObjectTurn ─────────────────────────────

export type ObjectTurnProps = { shape?: "tag" | "image"; lines?: string[]; src?: string; w?: number; h?: number; title?: string; caption?: string; source?: string };

export const ObjectTurn: React.FC<ObjectTurnProps> = (p) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const o = useEnv(10, 10);
  const ry = interpolate(f, [0, d], [-32, 14], { easing: Easing.inOut(Easing.sin) });
  const rx = 12 + Math.sin(f / 40) * 2;
  const push = interpolate(f, [0, d], [0.92, 1.06]);
  const w = p.w ?? 640, h = p.h ?? 380;
  const cap = interpolate(f, [18, 30], [0, 1], cl);
  const face = p.shape === "image" && p.src ? (
    <Img src={staticFile(`stills/${p.src}`)} style={{ width: w, height: h, objectFit: "contain", filter: "grayscale(1) contrast(1.1)" }} />
  ) : (
    <div style={{ width: w, height: h, borderRadius: 26, background: "linear-gradient(160deg,#d9dbd6 0%,#a9ada8 45%,#8a8e89 100%)", boxShadow: "inset 0 0 0 3px rgba(255,255,255,.35), inset 0 -10px 30px rgba(0,0,0,.25)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", position: "relative" }}>
      {[[34, 34], [w - 34, 34]].map(([x, y], k) => <div key={k} style={{ position: "absolute", left: x - 14, top: y - 14, width: 28, height: 28, borderRadius: 14, background: "#1a1a1a", boxShadow: "inset 0 3px 4px rgba(0,0,0,.9)" }} />)}
      {(p.lines || []).map((l, k) => (
        <div key={k} style={{ fontFamily: k === 0 ? HEAD : MONO, fontWeight: k === 0 ? 700 : 500, fontSize: k === 0 ? 190 : 34, lineHeight: 1, letterSpacing: k === 0 ? 4 : 3, color: "#2b2d2b", textShadow: "0 2px 0 rgba(255,255,255,.55), 0 -1px 0 rgba(0,0,0,.35)", textTransform: "uppercase" }}>{l}</div>
      ))}
    </div>
  );
  return (
    <AbsoluteFill style={{ opacity: o, background: "#070707", overflow: "hidden" }}>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 46% 50% at 50% 47%, #3a3832 0%, #1c1b18 45%, #070707 80%)" }} />
      <div style={{ position: "absolute", left: "50%", top: 540 + h / 2 + 10, width: w * 1.1, height: 70, marginLeft: -w * 0.55, borderRadius: "50%", background: "radial-gradient(ellipse, rgba(0,0,0,.75) 0%, rgba(0,0,0,0) 70%)", transform: `scaleX(${Math.cos((ry * Math.PI) / 180)})` }} />
      <AbsoluteFill style={{ perspective: 1600, alignItems: "center", justifyContent: "center" }}>
        <div style={{ transformStyle: "preserve-3d", transform: `translateY(-40px) scale(${push}) rotateX(${rx}deg) rotateY(${ry}deg)` }}>
          {p.shape !== "image" ? [10, 8, 6, 4, 2].map((z) => <div key={z} style={{ position: "absolute", width: w, height: h, borderRadius: 26, background: "#4e514d", transform: `translateZ(${-z}px)` }} />) : null}
          <div style={{ transform: "translateZ(0px)", position: "relative" }}>
            {face}
            <div style={{ position: "absolute", inset: 0, borderRadius: p.shape === "image" ? 0 : 26, background: `linear-gradient(${100 + ry * 2}deg, rgba(255,250,235,0) 30%, rgba(255,250,235,.28) 48%, rgba(255,250,235,0) 62%)`, mixBlendMode: "screen" }} />
          </div>
        </div>
      </AbsoluteFill>
      {p.title ? (
        <div style={{ position: "absolute", left: 96, bottom: 84, opacity: cap }}>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 46, color: C.light, textTransform: "uppercase" }}>{p.title}</div>
          {p.caption ? <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 1, color: C.lightSoft, textTransform: "uppercase", marginTop: 4, maxWidth: 1100 }}>{p.caption}</div> : null}
        </div>
      ) : null}
      <SourceLine text={p.source} />
    </AbsoluteFill>
  );
};
