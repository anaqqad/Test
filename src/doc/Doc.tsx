import React from "react";
import { Audio } from "@remotion/media";
import { AbsoluteFill, type CalculateMetadataFunction, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { type MathDocTimeline, timelineSchema } from "../mathdoc/schema";
import { PhotoBeat, QCContext, ThenNowBeat } from "../reel/blocks";
import type { ReelBeat, ReelSpec } from "../reel/schema";
import { applyTheme, B, serif } from "../reel/style";
import { BigTitle, ChapterCard, DocCard, DocEndCard, DocHook, DocLowerThird, DocMap, DocPin, DocStamp, DocYear, QuoteCard } from "./blocks";
import { type DocBeat, type DocSpec, docSpecSchema } from "./schema";

/** Without narration: ~2.7 words per second, so a layout preview has roughly the right length. */
const estimateTimeline = (spec: DocSpec): MathDocTimeline => {
  let t = 0.4;
  const fps = spec.fps;
  const beats = spec.beats.map((b, i) => {
    if (i > 0 && b.section) t += 1.0;
    const start = t;
    const words = b.text.split(/\s+/).map((w) => {
      const d = 0.17 + 0.045 * w.length;
      const word = { text: w, start: t, end: t + d * 0.9 };
      t += d;
      return word;
    });
    t += /[.!?]$/.test(b.text.trim()) ? 0.45 : 0.2;
    return { id: b.id, startFrame: i === 0 ? 0 : Math.round((start - 0.1) * fps), endFrame: 0, cues: {}, words };
  });
  const total = Math.round((t + 2.5) * fps);
  beats.forEach((b, i) => (b.endFrame = beats[i + 1]?.startFrame ?? total));
  return { fps, durationInFrames: total, beats };
};

export const calculateDocMetadata: CalculateMetadataFunction<DocSpec> = async ({ props, abortSignal }) => {
  const spec = docSpecSchema.parse(props);
  const load = async <T,>(file: string, parse: (x: unknown) => T): Promise<T | null> => {
    try {
      const res = await fetch(staticFile(file), { signal: abortSignal });
      return res.ok ? parse(await res.json()) : null;
    } catch {
      return null;
    }
  };
  const timeline = await load(`generated/${spec.id}/timeline.json`, (x) => timelineSchema.parse(x));
  const credits = await load(`pd/${spec.id}/credits.json`, (x) => x as Record<string, { width: number; height: number }>);
  let hasMix = false;
  try {
    hasMix = (await fetch(staticFile(`generated/${spec.id}/mix.wav`), { method: "HEAD", signal: abortSignal })).ok;
  } catch {
    hasMix = false;
  }
  const tl = timeline ?? estimateTimeline(spec);
  const images = Object.fromEntries(Object.entries(credits ?? {}).map(([k, v]) => [k, { width: v.width, height: v.height }]));
  return {
    durationInFrames: tl.durationInFrames,
    fps: spec.fps,
    width: spec.width,
    height: spec.height,
    defaultOutName: spec.id,
    props: { ...spec, timeline: tl, images, hasMix: hasMix && Boolean(timeline) },
  };
};

const Visual: React.FC<{ beat: DocBeat; spec: DocSpec; duration: number }> = ({ beat, spec, duration }) => {
  const v = beat.visual;
  // the reel's photo and then/now blocks size themselves from the composition, so they work at 16:9
  const asReel = { beat: beat as unknown as ReelBeat, spec: spec as unknown as ReelSpec, duration };
  if (v.kind === "photo") return <PhotoBeat {...asReel} />;
  if (v.kind === "thennow") return <ThenNowBeat {...asReel} />;
  if (v.kind === "card") return <DocCard beat={beat} spec={spec} duration={duration} />;
  if (v.kind === "map") return <DocMap step={v.step ?? "wharf"} duration={duration} />;
  if (v.kind === "chapter") return <ChapterCard num={v.num ?? 1} title={v.title ?? ""} />;
  if (v.kind === "title") return <BigTitle title={v.title ?? ""} sub={v.sub} />;
  if (v.kind === "quote") return <QuoteCard quote={v.quote ?? ""} by={v.by} />;
  return <DocEndCard page={spec.brand.page} line={spec.brand.ctaLine} />;
};

const Overlays: React.FC<{ beat: DocBeat; duration: number }> = ({ beat, duration }) => {
  const o = beat.overlays ?? {};
  return (
    <>
      {o.year ? <DocYear from={o.year.from} to={o.year.to} duration={duration} /> : null}
      {o.stamp ? <DocStamp text={o.stamp} /> : null}
      {o.pin ? <DocPin label={o.pin.label} sub={o.pin.sub} top={o.year || o.stamp ? 200 : 70} /> : null}
      {o.lowerThird ? <DocLowerThird name={o.lowerThird.name} sub={o.lowerThird.sub} /> : null}
      {o.hook ? <DocHook text={o.hook} /> : null}
    </>
  );
};

type Word = { text: string; start: number; end: number };
const MAX_WORDS = 8;
const MAX_CHARS = 48;

/** Subtitle lines: cut at punctuation and pauses, at most MAX_WORDS words / MAX_CHARS characters. */
const lines = (words: Word[]) => {
  const out: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w, i) => {
    const next = words[i + 1];
    const len = [...cur, w].map((x) => x.text).join(" ").length;
    if (cur.length && (cur.length >= MAX_WORDS || len > MAX_CHARS)) {
      out.push(cur);
      cur = [];
    }
    cur.push(w);
    if (!next || /[.!?;:]$/.test(w.text) || (/,$/.test(w.text) && cur.length >= 4) || next.start - w.end > 0.4) {
      out.push(cur);
      cur = [];
    }
  });
  return out.filter((l) => l.length).map((ws) => ({ ws, start: ws[0].start, end: ws[ws.length - 1].end }));
};

const Subtitles: React.FC<{ timeline: MathDocTimeline; hidden: Set<string> }> = ({ timeline, hidden }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const all = React.useMemo(() => timeline.beats.filter((b) => !hidden.has(b.id)).flatMap((b) => lines(b.words)), [timeline, hidden]);
  const i = all.findIndex((l, k) => t >= l.start - 0.05 && t < (all[k + 1] ? Math.min(all[k + 1].start - 0.05, l.end + 0.7) : l.end + 0.7));
  if (i < 0) return null;
  return (
    <div style={{ position: "absolute", left: 160, right: 160, bottom: 64, display: "flex", justifyContent: "center" }}>
      <div style={{ fontFamily: serif, fontWeight: 700, fontSize: 50, lineHeight: 1.15, textAlign: "center", color: B.cream, textShadow: "0 3px 0 rgba(0,0,0,0.6), 0 6px 26px rgba(0,0,0,0.95)" }}>
        {all[i].ws.map((w) => w.text).join(" ")}
      </div>
    </div>
  );
};

/** Long-form documentary: one Sequence per beat at the narration's beat boundaries, short dissolves, subtitles on top. */
export const Doc: React.FC<DocSpec> = (spec) => {
  applyTheme(spec.brand.theme);
  const tl = spec.timeline ?? estimateTimeline(spec);
  const hidden = React.useMemo(() => new Set(spec.beats.filter((b) => b.captions === false).map((b) => b.id)), [spec.beats]);
  const FADE = 8;
  return (
    <QCContext.Provider value={false}>
      <AbsoluteFill style={{ backgroundColor: B.black }}>
        {spec.beats.map((beat, i) => {
          const t = tl.beats.find((b) => b.id === beat.id) ?? tl.beats[i];
          const from = Math.max(0, t.startFrame - (i ? FADE : 0));
          const duration = t.endFrame - from;
          return (
            <Sequence key={beat.id} from={from} durationInFrames={duration} name={`${i + 1}. ${beat.id}`}>
              <FadeIn frames={i ? FADE : 0}>
                <Visual beat={beat} spec={spec} duration={duration} />
                <Overlays beat={beat} duration={duration} />
              </FadeIn>
            </Sequence>
          );
        })}
        <Subtitles timeline={tl} hidden={hidden} />
        {spec.hasMix ? <Audio src={staticFile(`generated/${spec.id}/mix.wav`)} /> : null}
      </AbsoluteFill>
    </QCContext.Provider>
  );
};

const FadeIn: React.FC<{ frames: number; children: React.ReactNode }> = ({ frames, children }) => {
  const frame = useCurrentFrame();
  const o = frames ? interpolate(frame, [0, frames], [0, 1], { extrapolateRight: "clamp" }) : 1;
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
