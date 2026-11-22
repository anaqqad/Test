// War-room globe map kit (learned from Watchfront, "Are We Already Living Through the Start of WW3?"; spec:
// styles/STYLE-WATCHFRONT-MAPS/MAPS.md). One orthographic globe for everything; shots change by a rotate+zoom camera
// move (75-90 f, fast start / long settle), never by cuts. Flat semantic fills, cyan borders, rim glow, Exo 2 caps,
// IBM Plex Mono kickers. Every element lands on its keyword (0 to +0.3 s); camera moves start on sentence starts.
import React, { createContext, useContext, useMemo } from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { geoOrthographic, geoPath, geoInterpolate, geoDistance, geoGraticule10 } from "d3-geo";
import { feature, mesh } from "topojson-client";
// @ts-ignore json
import countries50 from "world-atlas/countries-50m.json";
import { loadFont as loadExo } from "@remotion/google-fonts/Exo2";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";

export const EXO = loadExo("normal", { weights: ["600", "700"], subsets: ["latin"] }).fontFamily;
export const MONO = loadMono("normal", { weights: ["400", "500"], subsets: ["latin"] }).fontFamily;

export const THEME = {
  today: { space0: "#06141f", space1: "#000910", sea: "#072236", land: "#245570", border: "rgba(79,166,200,0.7)", rim: "#3fa9d6", text: "#e8eef2", accent: "#7fd3ef" },
  history: { space0: "#14110c", space1: "#060504", sea: "#10191c", land: "#685b49", border: "rgba(201,179,143,0.7)", rim: "#c9b38f", text: "#efe6d6", accent: "#c9b38f" },
};
export const C = { ally: "#3973a9", allyStroke: "#7fb3e6", focus: "#21a1bd", rival: "#4f4d59", hot: "#c25a55", hotStroke: "#ef7a70", third: "#7a774c", partner: "#3fb7b0", red: "#ef6158", amber: "#f2b630", zone: "rgba(179,154,58,0.45)", west: "#8fc6ef" };
export type Theme = typeof THEME.today;

const W = 1920, H = 1080;
const topo: any = countries50;
const COUNTRIES: any[] = (feature(topo, topo.objects.countries) as any).features;
const BORDERS = mesh(topo, topo.objects.countries);
const GRAT = geoGraticule10();
const byId = new Map(COUNTRIES.map((f) => [String(f.id).padStart(3, "0"), f]));
export const country = (id: string) => byId.get(id.padStart(3, "0"));

// ---------- camera ----------
export type CamKey = { f: number; center: [number, number]; scale: number; dur?: number }; // scale = globe radius in px
const EASE = Easing.bezier(0.3, 0, 0.15, 1);
export function cameraAt(keys: CamKey[], frame: number) {
  let i = 0;
  while (i + 1 < keys.length && keys[i + 1].f <= frame) i++;
  const k = keys[i], prev = keys[i - 1];
  if (!prev) return { center: k.center, scale: k.scale };
  const t = EASE(Math.min(1, Math.max(0, (frame - k.f) / (k.dur ?? 84))));
  const center = geoInterpolate(prev.center, k.center)(t) as [number, number];
  const scale = prev.scale * Math.pow(k.scale / prev.scale, t);
  return { center, scale };
}

type Ctx = { proj: any; path: any; center: [number, number]; scale: number; theme: Theme };
const MapCtx = createContext<Ctx | null>(null);
export const useMap = () => useContext(MapCtx)!;
const visible = (p: [number, number], c: [number, number]) => geoDistance(p, c) < Math.PI / 2 - 0.02;

// ---------- stage: space, rim glow, sea, land, borders, vignette ----------
export const MapStage: React.FC<{ cam: CamKey[]; theme?: Theme; grat?: boolean; children?: React.ReactNode }> = ({ cam, theme = THEME.today, grat = false, children }) => {
  const f = useCurrentFrame();
  const { center, scale } = cameraAt(cam, f);
  const proj = geoOrthographic().rotate([-center[0], -center[1]]).scale(scale).translate([W / 2, H / 2]).clipAngle(90);
  const path = geoPath(proj);
  const land = useMemo(() => COUNTRIES, []);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 50%, ${theme.space0} 0%, ${theme.space1} 75%)` }}>
      <svg width={W} height={H} style={{ position: "absolute" }}>
        <defs>
          <radialGradient id="seaG" cx="0.5" cy="0.5" r="0.5"><stop offset="0.82" stopColor={theme.sea} /><stop offset="1" stopColor="#020a12" /></radialGradient>
          <filter id="rimBlur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation={Math.max(6, scale * 0.04)} /></filter>
        </defs>
        <circle cx={W / 2} cy={H / 2} r={scale * 1.015} fill="none" stroke={theme.rim} strokeWidth={scale * 0.05} opacity={0.45} filter="url(#rimBlur)" />
        <path d={path({ type: "Sphere" }) || ""} fill="url(#seaG)" />
        {grat && <path d={path(GRAT) || ""} fill="none" stroke={theme.border} strokeWidth={1} opacity={0.12} />}
        <path d={path({ type: "FeatureCollection", features: land } as any) || ""} fill={theme.land} />
        <MapCtx.Provider value={{ proj, path, center, scale, theme }}>
          <g id="fills">{React.Children.toArray(children).filter((c: any) => c?.type?.layer === "fill")}</g>
          <path d={path(BORDERS) || ""} fill="none" stroke={theme.border} strokeWidth={1.5} strokeLinejoin="round" />
          <circle cx={W / 2} cy={H / 2} r={scale} fill="none" stroke={theme.rim} strokeWidth={1.5} opacity={0.6} />
          {React.Children.toArray(children).filter((c: any) => c?.type?.layer !== "fill" && c?.type?.layer !== "hud")}
        </MapCtx.Provider>
      </svg>
      <MapCtx.Provider value={{ proj, path, center, scale, theme }}>
        {React.Children.toArray(children).filter((c: any) => c?.type?.layer === "hud")}
      </MapCtx.Provider>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse 85% 85% at 50% 50%, transparent 60%, rgba(0,4,10,0.65) 100%)", pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};

const fade = (f: number, at: number, len = 9, out?: number) =>
  Math.min(interpolate(f, [at, at + len], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    out == null ? 1 : interpolate(f, [out, out + 8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));

const Label: React.FC<{ x: number; y: number; text: string; size?: number; color?: string; o: number; anchor?: "middle" | "start" }> = ({ x, y, text, size = 0.04 * H, color = "#e8eef2", o, anchor = "middle" }) =>
  <text x={x} y={y} textAnchor={anchor} fontFamily={EXO} fontWeight={700} fontSize={size} letterSpacing="0.04em" fill={color} opacity={o}
    style={{ paintOrder: "stroke", stroke: "rgba(0,8,16,0.85)", strokeWidth: 4 }}>{text.toUpperCase()}</text>;

// ---------- D3 country / bloc fill ----------
export const CountryFill: React.FC<{ ids: string[]; color: string; stroke?: string; at: number; out?: number; label?: string; labelAt?: [number, number]; labelColor?: string; labelMinScale?: number }> & { layer?: string } =
  ({ ids, color, stroke, at, out, label, labelAt, labelColor, labelMinScale = 900 }) => {
    const f = useCurrentFrame(); const { path, proj, center, scale } = useMap();
    const o = fade(f, at, 9, out);
    if (o <= 0) return null;
    const p = labelAt && visible(labelAt, center) ? proj(labelAt) : null;
    return <g opacity={o}>
      {ids.map((id) => { const c = country(id); return c ? <path key={id} d={path(c) || ""} fill={color} stroke={stroke ?? color} strokeWidth={2} /> : null; })}
      {p && label && <Label x={p[0]} y={p[1]} text={label} o={fade(f, at + 4, 8, out) * interpolate(scale, [labelMinScale * 0.8, labelMinScale], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} color={labelColor} />}
    </g>;
  };
CountryFill.layer = "fill";

// ---------- D1 pins and focus rings ----------
export const Pin: React.FC<{ at: number; ll: [number, number]; label?: string; out?: number; color?: string; ring?: boolean }> = ({ at, ll, label, out, color = C.red, ring = true }) => {
  const f = useCurrentFrame(); const { proj, center } = useMap();
  if (!visible(ll, center)) return null;
  const o = fade(f, at, 6, out); if (o <= 0) return null;
  const s = interpolate(f, [at, at + 6], [0.6, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  const [x, y] = proj(ll);
  return <g opacity={o} transform={`translate(${x},${y}) scale(${s})`}>
    {ring && <circle r={0.0225 * H} fill="none" stroke={color} strokeWidth={1.5} opacity={0.7} />}
    <circle r={0.006 * H} fill={color} stroke="#071420" strokeWidth={2} />
    {label && <Label x={0} y={-0.035 * H} text={label} size={0.026 * H} o={1} />}
  </g>;
};

// ---------- D4 lofted great-circle arc ----------
export const Arc: React.FC<{ at: number; from: [number, number]; to: [number, number]; color?: string; style?: "solid" | "dashed" | "dotted"; out?: number; draw?: number; loft?: number; toLabel?: string; fromLabel?: string }> =
  ({ at, from, to, color = C.amber, style = "solid", out, draw = 14, loft = 0.2, toLabel, fromLabel }) => {
    const f = useCurrentFrame(); const { proj, center } = useMap();
    const o = fade(f, at, 2, out); if (o <= 0) return null;
    const p = interpolate(f, [at, at + draw], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
    const gi = geoInterpolate(from, to); const N = 64;
    const a = proj(from), b = proj(to);
    const chord = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const pts: [number, number][] = [];
    for (let i = 0; i <= N * p; i++) {
      const t = i / N, ll = gi(t) as [number, number];
      if (!visible(ll, center)) continue;
      const q = proj(ll); const h = loft * chord * Math.sin(Math.PI * t);
      pts.push([q[0], q[1] - h]);
    }
    if (pts.length < 2) return null;
    const d = "M" + pts.map((q) => q.join(",")).join("L");
    const dash = style === "dashed" ? "10 7" : style === "dotted" ? "2 6" : undefined;
    const endO = fade(f, at + draw, 6, out);
    return <g opacity={o}>
      <path d={d} fill="none" stroke={color} strokeWidth={3.5} strokeDasharray={dash} strokeLinecap="round" />
      {visible(from, center) && <circle cx={a[0]} cy={a[1]} r={0.007 * H} fill={color} stroke="#fff" strokeWidth={1} />}
      {fromLabel && visible(from, center) && <Label x={a[0] + 14} y={a[1] - 10} text={fromLabel} size={0.026 * H} o={1} anchor="start" />}
      {visible(to, center) && <g opacity={endO}><circle cx={b[0]} cy={b[1]} r={0.007 * H} fill={color} stroke="#071420" strokeWidth={2} />
        {toLabel && <Label x={b[0]} y={b[1] - 18} text={toLabel} size={0.026 * H} o={1} color={color} />}</g>}
    </g>;
  };

// ---------- D6 zone (hatched polygon, marching dashed outline) + D7 ships ----------
export const Zone: React.FC<{ at: number; ring: [number, number][]; label?: string; out?: number; color?: string; fill?: string }> = ({ at, ring, label, out, color = C.amber, fill = C.zone }) => {
  const f = useCurrentFrame(); const { path, proj } = useMap();
  const o = fade(f, at, 10, out); if (o <= 0) return null;
  const s = interpolate(f, [at, at + 10], [0.92, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const poly = { type: "Polygon", coordinates: [[...ring, ring[0]].reverse()] } as any;
  const c = proj(ring.reduce((m, p) => [m[0] + p[0] / ring.length, m[1] + p[1] / ring.length], [0, 0]) as [number, number]);
  const low = ring.reduce((m, p) => (p[1] < m[1] ? p : m), ring[0]);   // southernmost point: label goes under the zone
  const lab = proj(low);
  return <g opacity={o} transform={`translate(${c[0]},${c[1]}) scale(${s}) translate(${-c[0]},${-c[1]})`}>
    <defs><pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" stroke={color} strokeWidth={1.2} opacity={0.6} /></pattern></defs>
    <path d={path(poly) || ""} fill={fill} />
    <path d={path(poly) || ""} fill="url(#hatch)" />
    <path d={path(poly) || ""} fill="none" stroke={color} strokeWidth={2} strokeDasharray="8 6" strokeDashoffset={-f * 0.35} />
    {label && <text x={lab[0]} y={lab[1] + 0.035 * H} textAnchor="middle" fontFamily={MONO} fontWeight={500} fontSize={0.022 * H} fill={color} letterSpacing="0.15em">{label.toUpperCase()}</text>}
  </g>;
};
export const Ship: React.FC<{ at: number; ll: [number, number]; heading?: number; color?: string; out?: number }> = ({ at, ll, heading = 0, color = "#669edb", out }) => {
  const f = useCurrentFrame(); const { proj, center } = useMap();
  if (!visible(ll, center)) return null;
  const o = fade(f, at, 6, out); if (o <= 0) return null;
  const [x, y] = proj(ll); const drift = (f - at) * 0.03;
  return <rect x={-0.013 * H} y={-0.004 * H} width={0.026 * H} height={0.008 * H} rx={0.004 * H} fill={color} stroke="#071420" strokeWidth={1.5} opacity={o}
    transform={`translate(${x + drift},${y}) rotate(${heading})`} />;
};

// ---------- HUD (slots in % of the frame) ----------
const Hud: React.FC<{ children: React.ReactNode }> & { layer?: string } = ({ children }) => <AbsoluteFill style={{ pointerEvents: "none" }}>{children}</AbsoluteFill>;
Hud.layer = "hud";
export { Hud };

export type Card = { at: number; kicker: string; body: string; accent: string; flag?: string };
export const Cards: React.FC<{ cards: Card[]; out?: number; footer?: string }> & { layer?: string } = ({ cards, out, footer }) => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", left: "66%", top: "14%", width: "30%" }}>
    {cards.map((c, i) => {
      const o = fade(f, c.at, 8, out); const dx = interpolate(f, [c.at, c.at + 8], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
      return <div key={i} style={{ opacity: o, transform: `translateX(${dx}px)`, display: "flex", gap: 14, alignItems: "center", background: "rgba(6,20,31,0.85)", borderLeft: `3px solid ${c.accent}`, padding: "12px 16px", marginBottom: 10 }}>
        {c.flag && <Img src={staticFile(c.flag)} style={{ width: 52, height: 34, objectFit: "cover" }} />}
        <div>
          <div style={{ fontFamily: MONO, fontSize: 0.017 * H, letterSpacing: "0.18em", color: c.accent, textTransform: "uppercase" }}>{c.kicker}</div>
          <div style={{ fontFamily: EXO, fontWeight: 600, fontSize: 0.029 * H, color: "#e8eef2", lineHeight: 1.2 }}>{c.body}</div>
        </div>
      </div>;
    })}
    {footer && <div style={{ fontFamily: MONO, fontSize: 0.015 * H, letterSpacing: "0.15em", color: "rgba(232,238,242,0.4)", opacity: fade(f, cards[0]?.at ?? 0, 8, out) }}>{footer.toUpperCase()}</div>}
  </div>;
};
Cards.layer = "hud";

export const YearStamp: React.FC<{ at: number; year: string; sub?: string; color?: string; out?: number }> & { layer?: string } = ({ at, year, sub, color = "#7fd3ef", out }) => {
  const f = useCurrentFrame(); const o = fade(f, at, 9, out); const dy = interpolate(f, [at, at + 9], [6, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <div style={{ position: "absolute", left: "6%", top: "9%", opacity: o, transform: `translateY(${dy}px)` }}>
    <div style={{ width: "3vw", height: 1, background: color, marginBottom: 10 }} />
    <div style={{ fontFamily: EXO, fontWeight: 700, fontSize: 0.046 * H, letterSpacing: "0.12em", color }}>{year}</div>
    {sub && <div style={{ fontFamily: MONO, fontSize: 0.017 * H, letterSpacing: "0.2em", color: "rgba(232,238,242,0.55)", textTransform: "uppercase" }}>{sub}</div>}
  </div>;
};
YearStamp.layer = "hud";

export type Node = { at: number; date: string; event: string };
export const Timeline: React.FC<{ nodes: Node[]; show: number; out?: number }> & { layer?: string } = ({ nodes, show, out }) => {
  const f = useCurrentFrame(); const o = fade(f, show, 10, out);
  const active = nodes.reduce((k, n, i) => (f >= n.at ? i : k), -1);
  return <div style={{ position: "absolute", left: "8%", width: "84%", top: "84%", opacity: o }}>
    <div style={{ position: "absolute", top: 30, left: 0, right: 0, height: 1, background: "rgba(127,169,192,0.5)" }} />
    {nodes.map((n, i) => {
      const x = (i / (nodes.length - 1)) * 100, lit = i <= active, cur = i === active;
      return <div key={i} style={{ position: "absolute", left: `${x}%`, transform: "translateX(-50%)", textAlign: "center", width: 260 }}>
        <div style={{ fontFamily: EXO, fontWeight: 700, fontSize: 0.024 * H, color: lit ? "#e8eef2" : "rgba(232,238,242,0.35)" }}>{n.date}</div>
        <div style={{ margin: "4px auto", width: 0.012 * H, height: 0.012 * H, borderRadius: "50%", background: cur ? C.red : lit ? "#e8eef2" : "rgba(232,238,242,0.3)" }} />
        <div style={{ fontFamily: EXO, fontWeight: 600, fontSize: 0.021 * H, color: cur ? C.red : lit ? "#c9d6de" : "rgba(232,238,242,0.35)" }}>{n.event}</div>
      </div>;
    })}
  </div>;
};
Timeline.layer = "hud";

export const Caption: React.FC<{ at: number; text: string; color?: string; out?: number }> & { layer?: string } = ({ at, text, color = "#e8eef2", out }) => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", top: "6%", width: "100%", textAlign: "center", fontFamily: EXO, fontWeight: 700, fontSize: 0.028 * H, letterSpacing: "0.06em", color, opacity: fade(f, at, 10, out) }}>{text.toUpperCase()}</div>;
};
Caption.layer = "hud";
