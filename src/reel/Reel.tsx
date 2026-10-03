import React from "react";
import { Audio } from "@remotion/media";
import { AbsoluteFill, type CalculateMetadataFunction, Freeze, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { type MathDocTimeline, timelineSchema } from "../mathdoc/schema";
import { CardBeat, EndCard, HarborMap, ThenNowBeat, TitleCard, HookText, LowerThird, PhotoBeat, PinChip, QCContext, Stamp, YearCounter } from "./blocks";
import { Captions } from "./Captions";
import { type ReelBeat, type ReelSpec, reelSpecSchema } from "./schema";
import { applyTheme, B } from "./style";

const LOOP_FRAMES = 12;

/**
 * Without narration (layout previews before the voice is paid for): ~2.8 words per second,
 * words spread evenly so the captions still run.
 */
const estimateTimeline = (spec: ReelSpec): MathDocTimeline => {
  let t = 0.3;
  const fps = spec.fps;
  const beats = spec.beats.map((b, i) => {
    const words = b.text.split(/\s+/);
    const start = t;
    const out = words.map((w) => {
      const d = 0.16 + 0.045 * w.length;
      const word = { text: w, start: t, end: t + d * 0.9 };
      t += d;
      return word;
    });
    t += b.text.trim().match(/[.!?]$/) ? 0.4 : 0.2;
    if (spec.beats[i + 1]?.section) t += 0.3;
    return { id: b.id, startFrame: i === 0 ? 0 : Math.round((start - 0.1) * fps), endFrame: 0, cues: {}, words: out };
  });
  const total = Math.round((t + 1.2) * fps);
  beats.forEach((b, i) => (b.endFrame = beats[i + 1]?.startFrame ?? total));
  return { fps, durationInFrames: total, beats };
};

export const calculateReelMetadata: CalculateMetadataFunction<ReelSpec> = async ({ props, abortSignal }) => {
  const spec = reelSpecSchema.parse(props);
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

const Visual: React.FC<{ beat: ReelBeat; spec: ReelSpec; duration: number }> = ({ beat, spec, duration }) => {
  const v = beat.visual;
  if (v.kind === "photo") return <PhotoBeat beat={beat} spec={spec} duration={duration} />;
  if (v.kind === "card") return <CardBeat beat={beat} spec={spec} duration={duration} />;
  if (v.kind === "map") return <HarborMap step={v.step ?? "wharf"} duration={duration} />;
  if (v.kind === "title") return <TitleCard title={v.title ?? ""} sub={v.sub} />;
  if (v.kind === "thennow") return <ThenNowBeat beat={beat} spec={spec} duration={duration} />;
  return <EndCard page={spec.brand.page} line={spec.brand.ctaLine} />;
};

const Overlays: React.FC<{ beat: ReelBeat; duration: number }> = ({ beat, duration }) => {
  const o = beat.overlays ?? {};
  return (
    <>
      {o.year ? <YearCounter from={o.year.from} to={o.year.to} duration={duration} /> : null}
      {o.stamp ? <Stamp text={o.stamp} /> : null}
      {o.pin ? <PinChip label={o.pin.label} sub={o.pin.sub} top={o.year || o.stamp || beat.visual.kind === "thennow" ? 330 : 190} /> : null}
      {o.lowerThird ? <LowerThird name={o.lowerThird.name} sub={o.lowerThird.sub} /> : null}
      {o.hook ? <HookText text={o.hook} /> : null}
    </>
  );
};

/** The hook beat as it looks on frame 0: the cover still, and the target of the loop dissolve. */
const CoverFrame: React.FC<{ spec: ReelSpec }> = ({ spec }) => {
  const beat = spec.beats[0];
  const tl = spec.timeline;
  const duration = tl ? tl.beats[0].endFrame - tl.beats[0].startFrame : 60;
  return (
    <Freeze frame={0}>
      <Visual beat={beat} spec={spec} duration={duration} />
      {beat.overlays?.hook ? <HookText text={beat.overlays.hook} animate={false} /> : null}
    </Freeze>
  );
};

/**
 * Vertical reel: one Sequence per beat, cut where tts_mathdoc.py put the boundary, captions on
 * top, and a dissolve at the end back into the opening frame so the reel loops cleanly.
 */
export const Reel: React.FC<ReelSpec> = (spec) => {
  applyTheme(spec.brand.theme);
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const tl = spec.timeline ?? estimateTimeline(spec);
  const hidden = React.useMemo(() => new Set(spec.beats.filter((b) => b.captions === false).map((b) => b.id)), [spec.beats]);
  const loop = interpolate(frame, [durationInFrames - LOOP_FRAMES, durationInFrames - 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const qc = Boolean(spec.qc);

  return (
    <QCContext.Provider value={qc}>
      <AbsoluteFill style={{ backgroundColor: qc ? "#000" : B.black }}>
        {spec.beats.map((beat, i) => {
          const t = tl.beats.find((b) => b.id === beat.id) ?? tl.beats[i];
          const duration = t.endFrame - t.startFrame;
          return (
            <Sequence key={beat.id} from={t.startFrame} durationInFrames={duration} name={`${i + 1}. ${beat.id}`}>
              <Visual beat={beat} spec={spec} duration={duration} />
              <Overlays beat={beat} duration={duration} />
            </Sequence>
          );
        })}
        <Captions timeline={tl} hidden={hidden} />
        {loop > 0 && !qc ? (
          <AbsoluteFill style={{ opacity: loop }}>
            <CoverFrame spec={spec} />
          </AbsoluteFill>
        ) : null}
        {spec.hasMix && !qc ? <Audio src={staticFile(`generated/${spec.id}/mix.wav`)} /> : null}
      </AbsoluteFill>
    </QCContext.Provider>
  );
};
