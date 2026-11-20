// JSON-driven wrappers (storyboard cards) for three skill devices:
// QuoteCard (quote-card-reveal, Brew), DocDesk (doc-desk-3d, Hoog) and GlobeMap (war-room-globe-maps, Watchfront).
// All times in the storyboard are seconds from the card start (plan.py turns spoken phrases into seconds).
import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { QuoteCard } from "./QuoteCard";
import { DocDesk3D, SHOTS } from "./DocDesk3D";
import { Arc, C, Caption, Cards, CountryFill, MapStage, Pin, THEME, Timeline, YearStamp, Zone } from "./GlobeKit";

const FPS = 30;
const fr = (t?: number) => (t === undefined || t === null ? undefined : Math.round(t * FPS));
const col = (c?: string) => (c && (C as Record<string, string>)[c]) || c;

export const QuoteCardJ: React.FC<{ bg?: string; portrait?: string; lines: { text: string; at: number }[]; by: string; byAt: number; size?: number; portraitH?: number }> = (p) => {
  const { durationInFrames: d } = useVideoConfig();
  const lines = p.lines.map((l) => ({ text: l.text, at: fr(l.at)! }));
  const noPortrait = !p.portrait;
  return (
    <QuoteCard bg={p.bg} portrait={p.portrait} lines={lines} by={p.by} byAt={fr(p.byAt)!} dur={d} size={p.size ?? (noPortrait ? 46 : 38)}
      portraitH={p.portraitH ?? 900} textX={noPortrait ? 360 : 820} textW={noPortrait ? 1200 : 860} />
  );
};

type ShotSpec = { t: number; kind: "wide" | "glide" | "grazing" | "heading" | "strip"; args: number[] };
export const DocDesk: React.FC<{ page: string; aspect: number; desk: string; shots: ShotSpec[]; credit: string }> = ({ page, aspect, desk, shots, credit }) => {
  const { durationInFrames: d } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {shots.map((s, i) => {
        const a = fr(s.t)!, b = i + 1 < shots.length ? fr(shots[i + 1].t)! : d;
        const shot = (SHOTS as any)[s.kind](...s.args);
        return (
          <Sequence key={i} from={a} durationInFrames={Math.max(1, b - a)}>
            <DocDesk3D page={page} aspect={aspect} desk={desk} shot={shot} dur={Math.max(1, b - a)} credit={credit} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const R = 459;
type LL = [number, number];
export const GlobeMap: React.FC<{
  theme?: "history" | "today";
  cam: { t: number; center: LL; scale: number; dur?: number }[];
  fills?: { ids: string[]; color: string; stroke?: string; at: number; out?: number; label?: string; labelAt?: LL }[];
  pins?: { ll: LL; label?: string; at: number; out?: number; color?: string }[];
  arcs?: { from: LL; to: LL; at: number; out?: number; color?: string; style?: "solid" | "dashed" | "dotted"; toLabel?: string; fromLabel?: string; loft?: number; draw?: number }[];
  zones?: { ring: LL[]; at: number; out?: number; label?: string }[];
  cards?: { at: number; kicker: string; body: string; accent?: string }[]; cardsOut?: number; footer?: string;
  year?: { at: number; year: string; sub?: string; out?: number };
  timeline?: { show: number; out?: number; nodes: { at: number; date: string; event: string }[] };
  captions?: { at: number; text: string; color?: string; out?: number }[];
}> = (p) => (
  <AbsoluteFill style={{ background: "#000" }}>
    <MapStage theme={p.theme === "today" ? THEME.today : THEME.history}
      cam={p.cam.map((k) => ({ f: fr(k.t)!, center: k.center, scale: R * k.scale, dur: k.dur }))}>
      {(p.fills ?? []).map((x, i) => <CountryFill key={`f${i}`} ids={x.ids} color={col(x.color)!} stroke={col(x.stroke)} at={fr(x.at)!} out={fr(x.out)} label={x.label} labelAt={x.labelAt} />)}
      {(p.zones ?? []).map((x, i) => <Zone key={`z${i}`} ring={x.ring} at={fr(x.at)!} out={fr(x.out)} label={x.label} />)}
      {(p.arcs ?? []).map((x, i) => <Arc key={`a${i}`} from={x.from} to={x.to} at={fr(x.at)!} out={fr(x.out)} color={col(x.color) ?? C.red} style={x.style ?? "solid"}
        toLabel={x.toLabel} fromLabel={x.fromLabel} loft={x.loft ?? 0.15} draw={x.draw ?? 24} />)}
      {(p.pins ?? []).map((x, i) => <Pin key={`p${i}`} ll={x.ll} label={x.label} at={fr(x.at)!} out={fr(x.out)} color={col(x.color)} />)}
      {p.year ? <YearStamp at={fr(p.year.at)!} year={p.year.year} sub={p.year.sub} out={fr(p.year.out)} color="#e9d9b8" /> : null}
      {p.cards ? <Cards out={fr(p.cardsOut)} footer={p.footer} cards={p.cards.map((c) => ({ at: fr(c.at)!, kicker: c.kicker, body: c.body, accent: col(c.accent) ?? C.red }))} /> : null}
      {p.timeline ? <Timeline show={fr(p.timeline.show)!} out={fr(p.timeline.out)} nodes={p.timeline.nodes.map((n) => ({ at: fr(n.at)!, date: n.date, event: n.event }))} /> : null}
      {(p.captions ?? []).map((x, i) => <Caption key={`c${i}`} at={fr(x.at)!} text={x.text} color={col(x.color)} out={fr(x.out)} />)}
    </MapStage>
  </AbsoluteFill>
);
