import React, { useMemo } from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Video } from "./schema";
import { buildTimeline, dayNumber } from "./lib/time";
import { useEngine } from "./lib/useEngine";
import { MapView } from "./components/MapView";
import { Sidebar } from "./components/Sidebar";
import { DraftBanner, EventCaption, ProgressBar, TitleCard } from "./components/Overlays";
import { theme } from "./lib/theme";

export type EventMeta = { frame: number; title: string; chapter: boolean; date: string };

export const Timelapse: React.FC<{ video: Video; events?: EventMeta[] }> = ({ video }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const tl = useMemo(() => buildTimeline(video), [video]);
  const eventDays = useMemo(() => video.events.map((e) => dayNumber(e.date)), [video]);
  const engine = useEngine(video);
  const day = tl.dayAt(frame);
  if (!engine) return <AbsoluteFill style={{ background: theme.panel }} />;
  const state = engine.state(day);

  return (
    <AbsoluteFill style={{ background: theme.panel }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1440, height: 1080, overflow: "hidden" }}>
        <MapView video={video} engine={engine} day={day} frame={frame} eventFrames={tl.eventFrames} />
        <div style={{ position: "absolute", inset: 0, pointerEvents: "none", background: "radial-gradient(ellipse at center, transparent 60%, rgba(51,40,28,0.28))" }} />
        <EventCaption video={video} frame={frame} fps={fps} eventFrames={tl.eventFrames} />
        <ProgressBar video={video} day={day} startDay={tl.startDay} endDay={tl.endDay} eventDays={eventDays} />
        {video.header.introClip && (
          <Sequence durationInFrames={video.timeline.introSeconds * fps}>
            <OffthreadVideo src={staticFile(video.header.introClip)} muted style={{ width: 1440, height: 1080, objectFit: "cover" }} />
          </Sequence>
        )}
        <TitleCard video={video} frame={frame} fps={fps} />
      </div>
      <Sidebar video={video} day={day} startDay={tl.startDay} frame={frame} eventFrames={tl.eventFrames} areaKm2={state.areaKm2} />
      {video.draft && <DraftBanner />}

      {video.audio.music.map((m, i) => (
        <Audio
          key={i}
          src={staticFile(m.src)}
          loop
          volume={(f) => m.volume * (video.audio.voiceover ? 0.35 : 1) * interpolate(f, [0, fps, durationInFrames - 3 * fps, durationInFrames], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
        />
      ))}
      {video.audio.voiceover && <Audio src={staticFile(video.audio.voiceover)} />}
      {video.events.map((e, i) =>
        e.sfx ? (
          <Sequence key={i} from={tl.eventFrames[i]} durationInFrames={4 * fps}>
            <Audio src={staticFile(e.sfx)} volume={video.audio.eventSfxVolume} />
          </Sequence>
        ) : null,
      )}
    </AbsoluteFill>
  );
};
