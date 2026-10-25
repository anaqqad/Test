// Calendar days <-> video frames. The clock is piecewise linear: each stretch of days plays at its own pace,
// events can freeze the clock, and there is a still intro and outro.
import type { Video } from "../schema";

const MS_PER_DAY = 86_400_000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function dayNumber(iso: string): number {
  const [y, m, d] = iso.split("-").map(Number);
  const date = new Date(Date.UTC(2000, m - 1, d));
  date.setUTCFullYear(y); // Date.UTC maps years 0-99 to 1900+
  return Math.round(date.getTime() / MS_PER_DAY);
}

export function dateParts(day: number): { y: number; m: number; d: number } {
  const date = new Date(Math.floor(day) * MS_PER_DAY);
  return { y: date.getUTCFullYear(), m: date.getUTCMonth() + 1, d: date.getUTCDate() };
}

export function formatDate(day: number, style: "long" | "short" = "long"): string {
  const { y, m, d } = dateParts(day);
  return style === "long" ? `${d} ${MONTHS[m - 1]} ${y}` : `${String(d).padStart(2, "0")}.${String(m).padStart(2, "0")}.${y}`;
}

type Anchor = { frame: number; day: number };

export type Timeline = {
  durationInFrames: number;
  startDay: number;
  endDay: number;
  dayAt: (frame: number) => number;
  frameAt: (day: number) => number; // first frame on which `day` is reached
  eventFrames: number[]; // same order as video.events
};

export function buildTimeline(video: Video): Timeline {
  const { fps, timeline, events } = video;
  const startDay = dayNumber(timeline.start);
  const endDay = dayNumber(timeline.end);
  const pace = timeline.pace.map((p) => ({ from: dayNumber(p.from), to: dayNumber(p.to), dps: p.daysPerSecond }));
  const paceAt = (day: number) => pace.find((p) => day >= p.from && day < p.to)?.dps ?? timeline.daysPerSecond;

  // Breakpoints where the pace may change or the clock holds.
  const holds = new Map<number, number>();
  for (const e of events) {
    const d = dayNumber(e.date);
    if (e.holdSeconds > 0) holds.set(d, (holds.get(d) ?? 0) + e.holdSeconds);
  }
  const cuts = new Set<number>([startDay, endDay, ...holds.keys()]);
  for (const p of pace) cuts.add(p.from), cuts.add(p.to);
  const days = [...cuts].filter((d) => d >= startDay && d <= endDay).sort((a, b) => a - b);

  const anchors: Anchor[] = [{ frame: 0, day: startDay }];
  let frame = timeline.introSeconds * fps;
  anchors.push({ frame, day: startDay });
  for (let i = 0; i < days.length; i++) {
    const day = days[i];
    if (i > 0) {
      frame += ((day - days[i - 1]) / paceAt(days[i - 1])) * fps;
      anchors.push({ frame, day });
    }
    const hold = holds.get(day);
    if (hold) {
      frame += hold * fps;
      anchors.push({ frame, day });
    }
  }
  frame += timeline.outroSeconds * fps;
  anchors.push({ frame, day: endDay });

  const dayAt = (f: number) => {
    if (f <= anchors[0].frame) return startDay;
    for (let i = 1; i < anchors.length; i++) {
      const a = anchors[i - 1], b = anchors[i];
      if (f <= b.frame) return b.frame === a.frame ? b.day : a.day + ((f - a.frame) / (b.frame - a.frame)) * (b.day - a.day);
    }
    return endDay;
  };
  const frameAt = (day: number) => {
    for (let i = 1; i < anchors.length; i++) {
      const a = anchors[i - 1], b = anchors[i];
      if (b.day > a.day && day <= b.day) return Math.round(a.frame + ((day - a.day) / (b.day - a.day)) * (b.frame - a.frame));
    }
    return Math.round(anchors[anchors.length - 1].frame);
  };

  return {
    durationInFrames: Math.ceil(frame),
    startDay,
    endDay,
    dayAt,
    frameAt,
    eventFrames: staggered(events.map((e) => frameAt(dayNumber(e.date))), fps),
  };
}

// Events that land on (nearly) the same frame play one after another, so each caption gets read.
function staggered(frames: number[], fps: number): number[] {
  const order = frames.map((f, i) => ({ f, i })).sort((a, b) => a.f - b.f || a.i - b.i);
  const out = frames.slice();
  let last = -Infinity;
  for (const { f, i } of order) {
    out[i] = Math.max(f, last + Math.round(2.4 * fps));
    last = out[i];
  }
  return out;
}

export const smoothstep = (t: number) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));

// Linear interpolation over [day, value] points, clamped at both ends.
export function sampleSeries(points: [number, number][], day: number): number {
  if (day <= points[0][0]) return points[0][1];
  for (let i = 1; i < points.length; i++) {
    const [d0, v0] = points[i - 1], [d1, v1] = points[i];
    if (day <= d1) return v0 + ((day - d0) / (d1 - d0 || 1)) * (v1 - v0);
  }
  return points[points.length - 1][1];
}
