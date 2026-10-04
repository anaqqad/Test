import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { C, SANS, SERIF } from "./theme";
import { LowerThird, SourceLine, Title, useDraw, useEnvelope } from "./parts";
import map from "./data/map.json";

/* ---------- small overlays on footage ---------- */

export const ContextLabel: React.FC<{ text: string }> = ({ text }) => {
  const o = useEnvelope();
  return (
    <AbsoluteFill style={{ opacity: o * 0.72 }}>
      <div style={{ position: "absolute", left: 90, bottom: 40, fontFamily: SANS, fontSize: 21, letterSpacing: 2, color: "#fff", textTransform: "uppercase", textShadow: "0 1px 3px rgba(0,0,0,.8)" }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

export const LowerThirdCard: React.FC<{ title: string; subtitle?: string; source?: string; width?: number }> = ({ title, subtitle, source, width = 1240 }) => {
  const o = useEnvelope();
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <LowerThird title={title} subtitle={subtitle} width={width} />
      {source ? <SourceLine text={source} /> : null}
    </AbsoluteFill>
  );
};

/* ---------- timeline ---------- */

export const TimelineCard: React.FC<{ title: string; points: { label: string; sub: string }[]; source: string }> = ({ title, points, source }) => {
  const o = useEnvelope();
  const line = useDraw(12, 30);
  const n = points.length;
  const x0 = 60, x1 = n > 3 ? 1330 : 1250;
  return (
    <AbsoluteFill style={{ opacity: o }}>
      <div style={{ position: "absolute", left: 90, top: 120, width: 1740, height: 650, background: C.panel }}>
        <div style={{ position: "absolute", left: 40, top: 36 }}>
          <Title text={title} size={46} />
        </div>
        <div style={{ position: "absolute", left: x0, top: 340, height: 3, width: (x1 - x0) * line, background: "rgba(212,165,55,0.75)" }} />
        {points.map((p, i) => {
          const x = x0 + ((x1 - x0) * i) / (n - 1);
          const shown = line >= i / (n - 1) - 0.001 ? 1 : 0;
          const a = interpolate(shown, [0, 1], [0, 1]);
          const align = "left";
          const left = x - 12;
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: x - 11, top: 330, width: 22, height: 22, borderRadius: 11, background: C.gold, opacity: a }} />
              <div style={{ position: "absolute", left, width: 432, top: 232, textAlign: align, fontFamily: SANS, fontWeight: 500, fontSize: 34, color: C.title, opacity: a }}>{p.label}</div>
              <div style={{ position: "absolute", left, width: 370, top: 384, textAlign: align, fontFamily: SANS, fontSize: 26, lineHeight: 1.35, color: C.body, opacity: a }}>{p.sub}</div>
            </React.Fragment>
          );
        })}
        <div style={{ position: "absolute", left: 40, bottom: 30, fontFamily: SANS, fontSize: 20, color: C.source }}>{source}</div>
      </div>
    </AbsoluteFill>
  );
};

/* ---------- documents ---------- */

type Para = { text: string; hl?: boolean };

const Paper: React.FC<{ children: React.ReactNode; tone?: "book" | "news" }> = ({ children, tone = "book" }) => (
  <div style={{ position: "relative", width: 840, height: 1050, background: tone === "book" ? C.paper : "#e9e5da", color: C.ink, boxShadow: "0 0 0 1px rgba(0,0,0,.15)", overflow: "hidden" }}>
    <svg width="840" height="1050" style={{ position: "absolute", inset: 0, opacity: 0.22, mixBlendMode: "multiply" }}>
      <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="4" /><feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.9 0" /></filter>
      <rect width="840" height="1050" filter="url(#grain)" />
    </svg>
    {children}
  </div>
);

export const BookExcerpt: React.FC<{ head: string; chapter: string; paras: Para[]; page?: string; hlP?: number }> = ({ head, chapter, paras, page, hlP = 1 }) => (
  <Paper>
    <div style={{ position: "absolute", left: 80, right: 80, top: 64, display: "flex", justifyContent: "space-between", fontFamily: SERIF, fontSize: 18, letterSpacing: 3, color: "#6b6254" }}>
      <span>{head}</span>
      <span>{page}</span>
    </div>
    <div style={{ position: "absolute", left: 80, right: 80, top: 140, fontFamily: SERIF, fontSize: 24, letterSpacing: 4, textAlign: "center", color: "#3d372e" }}>{chapter}</div>
    <div style={{ position: "absolute", left: 80, right: 80, top: 230 }}>
      {paras.map((p, i) => (
        <p key={i} style={{ position: "relative", margin: "0 0 30px", fontFamily: SERIF, fontSize: 29, lineHeight: 1.62, textAlign: "justify", hyphens: "auto" }}>
          {p.text}
          {p.hl ? (
            <svg style={{ position: "absolute", left: -18, top: -12, width: "calc(100% + 36px)", height: "calc(100% + 24px)", overflow: "visible" }} viewBox="0 0 100 100" preserveAspectRatio="none">
              <rect x="0" y="0" width="100" height="100" fill="none" stroke={C.gold} strokeWidth="3" vectorEffect="non-scaling-stroke" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - hlP} />
            </svg>
          ) : null}
        </p>
      ))}
    </div>
  </Paper>
);

export const Clipping: React.FC<{ kicker: string; headline: string; dateline: string; body: string; hlP?: number }> = ({ kicker, headline, dateline, body, hlP = 1 }) => (
  <Paper tone="news">
    <div style={{ position: "absolute", left: 70, right: 70, top: 70, borderTop: "4px double #2a2722", borderBottom: "1px solid #2a2722", padding: "10px 0", fontFamily: SERIF, fontSize: 20, letterSpacing: 3, textAlign: "center" }}>{kicker}</div>
    <div style={{ position: "absolute", left: 70, right: 70, top: 170, fontFamily: SERIF, fontWeight: 700, fontSize: 76, lineHeight: 1.05, textAlign: "center", textTransform: "uppercase", letterSpacing: -1 }}>{headline}</div>
    <div style={{ position: "absolute", left: 70, right: 70, top: 470, fontFamily: SERIF, fontSize: 30, lineHeight: 1.6, textAlign: "justify" }}>
      <span style={{ position: "relative" }}>
        <b>{dateline}</b> {body}
      </span>
      <svg style={{ position: "absolute", left: -18, top: -14, width: "calc(100% + 36px)", height: "calc(100% + 28px)", overflow: "visible" }} viewBox="0 0 100 100" preserveAspectRatio="none">
        <rect x="0" y="0" width="100" height="100" fill="none" stroke={C.gold} strokeWidth="3" vectorEffect="non-scaling-stroke" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - hlP} />
      </svg>
    </div>
    <div style={{ position: "absolute", left: 70, right: 70, bottom: 60, borderTop: "1px solid #2a2722", paddingTop: 10, fontFamily: SANS, fontSize: 18, color: "#5a554c" }}>Reconstructed from the report as quoted in the memoir</div>
  </Paper>
);

/** Full-frame document: scan centered over a blurred, darkened copy of itself + lower third + citation. */
export const DocumentCard: React.FC<{
  doc: { kind: "book"; head: string; chapter: string; page?: string; paras: Para[] } | { kind: "clip"; kicker: string; headline: string; dateline: string; body: string };
  title: string;
  subtitle: string;
  source: string;
}> = ({ doc, title, subtitle, source }) => {
  const o = useEnvelope();
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const hlP = useDraw(30, 22);
  const push = interpolate(f, [0, d], [1, 1.04]);
  const page = doc.kind === "book" ? <BookExcerpt {...doc} hlP={hlP} /> : <Clipping {...doc} hlP={hlP} />;
  return (
    <AbsoluteFill style={{ opacity: o, background: "#222" }}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", filter: "blur(30px) brightness(0.55)", transform: "scale(2.4)" }}>{page}</AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", transform: `scale(${push})` }}>{page}</AbsoluteFill>
      <LowerThird title={title} subtitle={subtitle} width={1180} bottom={120} />
      <SourceLine text={source} />
    </AbsoluteFill>
  );
};

/* ---------- route map ---------- */

export const RouteMapCard: React.FC<{ title: string; subtitle: string; stops: string[]; legs: string[]; source: string; extra?: string[] }> = ({ title, subtitle, stops, legs, source, extra = [] }) => {
  const o = useEnvelope();
  const f = useCurrentFrame();
  const { durationInFrames: d } = useVideoConfig();
  const pts = stops.map((s) => (map.places as Record<string, number[]>)[s]);
  const draw = useDraw(20, Math.min(110, d - 60));
  const zoom = interpolate(f, [0, d], [1.0, 1.06]);
  // total path length for progressive draw
  const seg = pts.slice(1).map((p, i) => Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]));
  const total = seg.reduce((a, b) => a + b, 0);
  const pathD = "M" + pts.map((p) => p.join(",")).join("L");
  let acc = 0;
  const reached = pts.map((_, i) => {
    if (i > 0) acc += seg[i - 1];
    return draw * total >= acc - 1;
  });
  return (
    <AbsoluteFill style={{ opacity: o, background: "#0e1626" }}>
      <AbsoluteFill style={{ transform: `scale(${zoom})`, transformOrigin: "1050px 480px" }}>
        <svg width={1920} height={1080}>
          {map.states.map((s) => (
            <path key={s.name} d={s.d} fill={s.name === "Illinois" ? "#3b4a63" : "#28344a"} stroke="#56667f" strokeWidth={1.5} />
          ))}
          <path d={pathD} fill="none" stroke={C.gold} strokeWidth={6} strokeDasharray="14 10" pathLength={total} style={{ clipPath: "none" }} strokeDashoffset={0} opacity={0.25} />
          <path d={pathD} fill="none" stroke={C.gold} strokeWidth={6} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
          {extra.map((n) => {
            const p = (map.places as Record<string, number[]>)[n];
            return (
              <g key={n} opacity={0.75}>
                <circle cx={p[0]} cy={p[1]} r={8} fill="none" stroke={C.body} strokeWidth={2} />
                <text x={p[0] + 16} y={p[1] + 8} fontFamily={SANS} fontSize={24} fill={C.body}>{n}</text>
              </g>
            );
          })}
          {pts.map((p, i) => (
            <g key={stops[i]} opacity={reached[i] ? 1 : 0}>
              <circle cx={p[0]} cy={p[1]} r={11} fill={C.gold} />
              <text x={p[0] + (i === 0 ? 22 : i === 1 ? -22 : 22)} y={p[1] + (i === 0 ? 12 : i === 1 ? 12 : -18)} textAnchor={i === 1 ? "end" : "start"} fontFamily={SERIF} fontSize={36} fill={C.title}>{stops[i]}</text>
            </g>
          ))}
          {legs.map((l, i) => {
            const a = pts[i], b = pts[i + 1];
            return (
              <text key={l} opacity={reached[i + 1] ? 1 : 0} x={(a[0] + b[0]) / 2 + 14} y={(a[1] + b[1]) / 2 + (i === 0 ? 70 : -30)} fontFamily={SANS} fontSize={26} fill={C.gold} textAnchor="middle">{l}</text>
            );
          })}
          <text x={(map.places as Record<string, number[]>)["Lake Michigan"][0]} y={(map.places as Record<string, number[]>)["Lake Michigan"][1]} fontFamily={SERIF} fontStyle="italic" fontSize={30} fill="#7d8aa0">Lake Michigan</text>
        </svg>
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 90, top: 90, background: C.panel, padding: "24px 34px" }}>
        <Title text={title} size={44} />
        <div style={{ fontFamily: SANS, fontSize: 27, color: C.body, marginTop: 10 }}>{subtitle}</div>
      </div>
      <SourceLine text={source} />
    </AbsoluteFill>
  );
};
