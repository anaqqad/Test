// "Field ledger": how the channel shows data, dates, documents and maps.
// Full-frame graph paper with a red margin rule. Figures and headlines in condensed caps, labels and
// sources typed in mono, emphasis in grease pencil (underlines, ticks, hatched bars, routes).
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C, HEAD, MONO, QUOTE } from "./theme";
import { Stroke, useEnv, useProg, wobble } from "./marks";
import map from "./data/map.json";

const MARGIN = 170;

export const Paper: React.FC<{ file: string; head: string; source: string; children: React.ReactNode }> = ({ file, head, source, children }) => {
  const o = useEnv();
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const drift = interpolate(f, [0, d], [0, -18]); // the sheet slides very slowly upward
  const headIn = useProg(4, 12);
  return (
    <AbsoluteFill style={{ opacity: o, background: C.paper, overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `translateY(${drift}px)` }}>
        <svg width={1920} height={1140} style={{ position: "absolute" }}>
          <defs>
            <pattern id="minor" width={24} height={24} patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke={C.gridMinor} strokeWidth={1} /></pattern>
            <pattern id="major" width={120} height={120} patternUnits="userSpaceOnUse"><rect width={120} height={120} fill="url(#minor)" /><path d="M120 0H0V120" fill="none" stroke={C.gridMajor} strokeWidth={1.4} /></pattern>
            <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2" /><feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0.10 0" /></filter>
          </defs>
          <rect width={1920} height={1140} fill="url(#major)" />
          <line x1={MARGIN} y1={0} x2={MARGIN} y2={1140} stroke={C.grease} strokeWidth={2.5} opacity={0.75} />
          <line x1={MARGIN + 7} y1={0} x2={MARGIN + 7} y2={1140} stroke={C.grease} strokeWidth={1.2} opacity={0.6} />
          <rect width={1920} height={1140} filter="url(#grain)" />
        </svg>
        {children}
        <div style={{ position: "absolute", left: MARGIN + 30, top: 58, padding: "20px 28px 18px 20px", background: C.paper, boxShadow: `0 0 0 1px ${C.gridMajor}`, opacity: headIn, transform: `translateX(${(1 - headIn) * -16}px)` }}>
          <div style={{ fontFamily: MONO, fontSize: 22, letterSpacing: 3, color: C.inkSoft }}>{file}</div>
          <div style={{ fontFamily: HEAD, fontWeight: 700, fontSize: 92, lineHeight: 1, textTransform: "uppercase", color: C.ink, marginTop: 6 }}>{head}</div>
        </div>
        <div style={{ position: "absolute", left: MARGIN + 50, bottom: 70, background: C.paper, padding: "4px 8px", fontFamily: MONO, fontSize: 19, letterSpacing: 1, color: C.inkSoft, textTransform: "uppercase" }}>Source: {source}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Dated entries, one per ruled row; each gets a grease tick in the margin as it is read. */
export const LedgerTimeline: React.FC<{ file: string; head: string; rows: { date: string; text: string }[]; source: string }> = ({ file, head, rows, source }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const step = Math.min(30, (d - 60) / rows.length);
  return (
    <Paper file={file} head={head} source={source}>
      {rows.map((r, i) => {
        const t0 = 16 + i * step;
        const a = interpolate(f, [t0, t0 + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const tick = interpolate(f, [t0 + 6, t0 + 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const y = 300 + i * 132;
        return (
          <React.Fragment key={i}>
            <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
              <Stroke d={wobble([[MARGIN - 70, y + 34], [MARGIN - 52, y + 54], [MARGIN - 20, y + 10]], 20 + i, 1.5)} p={tick} w={6} />
              <line x1={MARGIN + 50} y1={y + 92} x2={1760} y2={y + 92} stroke={C.ink} strokeWidth={1.2} opacity={0.25 * a} />
            </svg>
            <div style={{ position: "absolute", left: MARGIN + 50, top: y + 14, width: 360, opacity: a, fontFamily: MONO, fontWeight: 500, fontSize: 30, color: C.inkSoft }}>{r.date}</div>
            <div style={{ position: "absolute", left: MARGIN + 430, top: y, width: 1150, opacity: a, transform: `translateX(${(1 - a) * 18}px)`, fontFamily: HEAD, fontWeight: 500, fontSize: 56, color: C.ink, textTransform: "uppercase" }}>{r.text}</div>
          </React.Fragment>
        );
      })}
    </Paper>
  );
};

/** Comparison: hatched grease bars on the grid, figure in big caps at the bar end. */
export const LedgerBars: React.FC<{ file: string; head: string; bars: { label: string; value: number; figure: string; note: string }[]; max: number; source: string }> = ({ file, head, bars, max, source }) => {
  const f = useCurrentFrame();
  const x0 = MARGIN + 50, full = 1180;
  return (
    <Paper file={file} head={head} source={source}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <pattern id="hatch" width={14} height={14} patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width={14} height={14} fill={C.grease} opacity={0.18} /><line x1={0} y1={0} x2={0} y2={14} stroke={C.grease} strokeWidth={6} opacity={0.85} /></pattern>
        </defs>
        {bars.map((b, i) => {
          const t0 = 22 + i * 26;
          const p = interpolate(f, [t0, t0 + 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const w = Math.max(6, (full * b.value) / max) * p;
          const y = 380 + i * 230;
          return (
            <g key={i}>
              <rect x={x0} y={y} width={w} height={96} fill="url(#hatch)" />
              <path d={wobble([[x0, y], [x0 + w, y], [x0 + w, y + 96], [x0, y + 96], [x0, y]], 40 + i, 1.6)} fill="none" stroke={C.grease} strokeWidth={4} opacity={p > 0 ? 0.95 : 0} />
            </g>
          );
        })}
      </svg>
      {bars.map((b, i) => {
        const t0 = 22 + i * 26;
        const p = interpolate(f, [t0, t0 + 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const w = Math.max(6, (full * b.value) / max) * p;
        const y = 380 + i * 230;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x0, top: y - 52, fontFamily: MONO, fontWeight: 500, fontSize: 28, color: C.ink, textTransform: "uppercase", letterSpacing: 1 }}>{b.label}</div>
            <div style={{ position: "absolute", left: x0 + w + 30, top: y - 6, opacity: p, fontFamily: HEAD, fontWeight: 700, fontSize: 96, lineHeight: 1, color: C.ink }}>{b.figure}</div>
            <div style={{ position: "absolute", left: x0, top: y + 110, opacity: p, fontFamily: MONO, fontSize: 24, color: C.inkSoft }}>{b.note}</div>
          </React.Fragment>
        );
      })}
    </Paper>
  );
};

/** A quoted passage, typed large, with the key words underlined in grease pencil. */
export const LedgerQuote: React.FC<{ file: string; head: string; before: string; key_: string; after: string; who: string; source: string }> = ({ file, head, before, key_, after, who, source }) => {
  const a = useProg(10, 14);
  const u = useProg(34, 20);
  return (
    <Paper file={file} head={head} source={source}>
      <div style={{ position: "absolute", left: MARGIN + 50, top: 330, width: 1500, opacity: a, fontFamily: QUOTE, fontSize: 70, lineHeight: 1.42, color: C.ink }}>
        <span style={{ fontStyle: "italic", color: C.grease, fontSize: 90, lineHeight: 0, verticalAlign: "-18px", marginRight: 8 }}>“</span>
        {before}
        <span style={{ position: "relative", display: "inline-block" }}>
          {key_}
          <span style={{ position: "absolute", left: -4, bottom: -4, height: 7, width: `${u * 102}%`, background: C.grease, borderRadius: 4, transform: "rotate(-0.5deg)", opacity: 0.92 }} />
          <span style={{ position: "absolute", left: 10, bottom: -13, height: 4, width: `${Math.max(0, u - 0.25) * 90}%`, background: C.grease, borderRadius: 3, transform: "rotate(0.4deg)", opacity: 0.7 }} />
        </span>
        {after}”
      </div>
      <div style={{ position: "absolute", left: MARGIN + 50, top: 820, opacity: a, fontFamily: MONO, fontSize: 28, color: C.ink }}>— {who}</div>
    </Paper>
  );
};

/** A news clipping pinned to the ledger: torn newsprint, slightly rotated, bracketed in grease. */
export const LedgerClipping: React.FC<{ file: string; head: string; kicker: string; headline: string; dateline: string; body: string; source: string }> = ({ file, head, kicker, headline, dateline, body, source }) => {
  const f = useCurrentFrame();
  const drop = interpolate(f, [6, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const br = useProg(30, 16);
  const torn = "polygon(0% 2%, 6% 0%, 14% 1.5%, 23% 0%, 33% 1.2%, 45% 0.2%, 58% 1.4%, 70% 0%, 82% 1.3%, 92% 0.3%, 100% 1.6%, 99.4% 98%, 91% 100%, 80% 98.6%, 68% 100%, 55% 98.8%, 43% 100%, 30% 98.5%, 18% 100%, 8% 98.7%, 0.4% 100%)";
  return (
    <Paper file={file} head={head} source={source}>
      <div style={{ position: "absolute", left: 640, top: 250, width: 900, opacity: drop, transform: `rotate(-1.6deg) translateY(${(1 - drop) * 30}px)`, filter: "drop-shadow(0 6px 10px rgba(0,0,0,.18))" }}>
        <div style={{ clipPath: torn, background: "#e6e1d3", padding: "46px 56px 54px" }}>
          <div style={{ fontFamily: MONO, fontSize: 18, letterSpacing: 3, color: "#4a463f", borderBottom: "2px solid #2b2924", paddingBottom: 8 }}>{kicker}</div>
          <div style={{ fontFamily: "'Times New Roman', Times, serif", fontWeight: 700, fontSize: 70, lineHeight: 1.0, textTransform: "uppercase", color: "#1b1a17", margin: "18px 0 20px" }}>{headline}</div>
          <div style={{ fontFamily: "'Times New Roman', Times, serif", fontSize: 31, lineHeight: 1.45, color: "#1b1a17", textAlign: "justify" }}><b>{dateline}</b> {body}</div>
        </div>
      </div>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <Stroke d={wobble([[600, 300], [580, 300], [578, 760], [598, 762]], 61, 1.5)} p={br} w={7} />
      </svg>
    </Paper>
  );
};

/** Route on the ledger: state lines in ink, the journey in grease pencil, stops typed in mono. */
export const LedgerMap: React.FC<{ file: string; head: string; stops: string[]; legs: string[]; extra?: string[]; source: string }> = ({ file, head, stops, legs, extra = [], source }) => {
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const P = map.places as Record<string, number[]>;
  const pts = stops.map((s) => P[s]);
  const draw = interpolate(f, [24, Math.min(d - 40, 150)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
  const total = seg.reduce((a, b) => a + b, 0);
  let acc = 0;
  const reached = pts.map((_, i) => (i > 0 && (acc += seg[i - 1]), draw * total >= acc - 1));
  return (
    <Paper file={file} head={head} source={source}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <defs>
          <pattern id="ill" width={10} height={10} patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1={0} y1={0} x2={0} y2={10} stroke={C.ink} strokeWidth={1} opacity={0.18} /></pattern>
        </defs>
        {map.states.map((s) => (
          <path key={s.name} d={s.d} fill={s.name === "Illinois" ? "url(#ill)" : "none"} stroke={C.ink} strokeWidth={s.name === "Illinois" ? 2.2 : 1.2} opacity={s.name === "Illinois" ? 0.8 : 0.4} />
        ))}
        <text x={P["Lake Michigan"][0]} y={P["Lake Michigan"][1]} fontFamily={MONO} fontSize={24} fill={C.inkSoft} letterSpacing={3}>LAKE MICHIGAN</text>
        <Stroke d={wobble(pts as [number, number][], 77, 2.5)} p={draw} w={8} />
        {extra.map((n) => (
          <g key={n} opacity={0.7}>
            <rect x={P[n][0] - 7} y={P[n][1] - 7} width={14} height={14} fill="none" stroke={C.ink} strokeWidth={2} />
            <text x={P[n][0] + 18} y={P[n][1] + 8} fontFamily={MONO} fontSize={22} fill={C.ink}>{n.toUpperCase()}</text>
          </g>
        ))}
        {pts.map((p, i) => (
          <g key={stops[i]} opacity={reached[i] ? 1 : 0}>
            <circle cx={p[0]} cy={p[1]} r={11} fill={C.ink} />
            <text x={p[0] + (i === 1 ? -24 : 24)} y={p[1] + (i === 1 ? 44 : i === 0 ? -18 : 10)} textAnchor={i === 1 ? "end" : "start"} fontFamily={HEAD} fontWeight={700} fontSize={48} fill={C.ink}>{stops[i].toUpperCase()}</text>
          </g>
        ))}
        {legs.map((l, i) => {
          const a = pts[i], b = pts[i + 1];
          return <text key={l} opacity={reached[i + 1] ? 1 : 0} x={(a[0] + b[0]) / 2 + 30} y={(a[1] + b[1]) / 2 + (i === 0 ? 80 : 10)} fontFamily={MONO} fontSize={26} fill={C.grease}>{l.toUpperCase()}</text>;
        })}
      </svg>
    </Paper>
  );
};
