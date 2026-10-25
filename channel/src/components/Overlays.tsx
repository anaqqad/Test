import React from "react";
import { interpolate } from "remotion";
import type { Video } from "../schema";
import { theme } from "../lib/theme";
import { VIEWPORT } from "../lib/map";

// Cold open: the title and one hook line over the starting map, gone before the clock starts.
export const TitleCard: React.FC<{ video: Video; frame: number; fps: number }> = ({ video, frame, fps }) => {
  const end = video.timeline.introSeconds * fps;
  const opacity = interpolate(frame, [0, 6, end - 12, end], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (opacity <= 0) return null;
  const rise = interpolate(frame, [0, 18], [24, 0], { extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: VIEWPORT.w, height: VIEWPORT.h, opacity, background: "radial-gradient(ellipse at center, rgba(29,25,20,0.55), rgba(29,25,20,0.85))", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", color: theme.panelText }}>
      <div style={{ transform: `translateY(${rise}px)`, fontFamily: theme.display, fontWeight: 700, fontSize: 84, lineHeight: 1.05, maxWidth: 1200, textShadow: "0 4px 24px rgba(0,0,0,0.6)" }}>{video.header.title}</div>
      <div style={{ fontFamily: theme.number, fontWeight: 700, fontSize: 34, color: theme.front, letterSpacing: 6, marginTop: 18 }}>{video.header.subtitle.toUpperCase()}</div>
      {video.header.hook && <div style={{ fontFamily: theme.number, fontWeight: 500, fontSize: 38, marginTop: 34, maxWidth: 1000 }}>{video.header.hook}</div>}
    </div>
  );
};

// Lower-third caption for the most recent event, sliding in from the left.
export const EventCaption: React.FC<{ video: Video; frame: number; fps: number; eventFrames: number[] }> = ({ video, frame, fps, eventFrames }) => {
  let idx = -1;
  video.events.forEach((e, i) => {
    if (eventFrames[i] <= frame && frame < eventFrames[i] + (e.captionSeconds + e.holdSeconds) * fps) idx = i;
  });
  if (idx < 0) return null;
  const e = video.events[idx];
  const age = frame - eventFrames[idx];
  const life = (e.captionSeconds + e.holdSeconds) * fps;
  const x = interpolate(age, [0, 10], [-40, 0], { extrapolateRight: "clamp" });
  const opacity = interpolate(age, [0, 8, life - 10, life], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 48, bottom: 92, maxWidth: 820, opacity, transform: `translateX(${x}px)`, background: "rgba(29,25,20,0.88)", borderLeft: `6px solid ${theme.front}`, padding: "18px 26px", color: theme.panelText, boxShadow: "0 8px 30px rgba(0,0,0,0.35)" }}>
      <div style={{ fontFamily: theme.display, fontWeight: 700, fontSize: 38, lineHeight: 1.1 }}>{e.title}</div>
      {e.text && <div style={{ fontFamily: theme.number, fontWeight: 500, fontSize: 30, marginTop: 8, lineHeight: 1.25 }}>{e.text}</div>}
    </div>
  );
};

// Progress through the war with a tick per event: shows how much story is left.
export const ProgressBar: React.FC<{ video: Video; day: number; startDay: number; endDay: number; eventDays: number[] }> = ({ day, startDay, endDay, eventDays }) => {
  const p = (d: number) => `${(100 * (d - startDay)) / Math.max(1, endDay - startDay)}%`;
  return (
    <div style={{ position: "absolute", left: 48, right: 48, bottom: 40, height: 6, background: "rgba(51,40,28,0.35)", borderRadius: 3 }}>
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: p(day), background: theme.accent, borderRadius: 3 }} />
      {eventDays.map((d, i) => (
        <div key={i} style={{ position: "absolute", left: p(d), top: -5, width: 3, height: 16, marginLeft: -1.5, background: d <= day ? theme.front : theme.ink, opacity: d <= day ? 1 : 0.5 }} />
      ))}
    </div>
  );
};

export const DraftBanner: React.FC = () => (
  <div style={{ position: "absolute", left: 0, top: 0, padding: "8px 18px", background: "#c0392b", color: "#fff", fontFamily: theme.number, fontWeight: 700, fontSize: 22, letterSpacing: 3 }}>
    DRAFT DATA - NOT FACT-CHECKED - DO NOT PUBLISH
  </div>
);

// End card: the final map dims and one closing line sits at the top, leaving room for YouTube's end-screen
// elements (video + subscribe) in the middle and bottom.
export const EndCard: React.FC<{ video: Video; frame: number; fps: number; durationInFrames: number }> = ({ video, frame, fps, durationInFrames }) => {
  const start = durationInFrames - video.timeline.outroSeconds * fps;
  const t = interpolate(frame, [start + fps, start + 2 * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (t <= 0) return null;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: VIEWPORT.w, height: VIEWPORT.h, background: `rgba(29,25,20,${0.5 * t})` }}>
      {video.header.outro && (
        <div style={{ position: "absolute", left: 80, right: 80, top: 90, opacity: t, textAlign: "center", fontFamily: theme.display, fontWeight: 700, fontSize: 52, lineHeight: 1.2, color: theme.panelText, textShadow: "0 4px 24px rgba(0,0,0,0.6)" }}>
          {video.header.outro}
        </div>
      )}
    </div>
  );
};
