// Derives the vertical Short from a video: same data, a 9:16 frame, and the clock sped up so the story runs in
// about `short.seconds`. Holds, captions, intro and outro shrink to fit the faster pace; the globe is dropped.
import type { Video } from "./schema";
import { buildTimeline, dayNumber } from "./lib/time";

export function toShort(video: Video): Video {
  const fps = video.fps;
  const tl = buildTimeline(video);
  const holds = video.events.reduce((a, e) => a + e.holdSeconds, 0);
  const run = tl.durationInFrames / fps - video.timeline.introSeconds - video.timeline.outroSeconds - holds;
  const intro = 1.5, outro = 3, holdScale = 0.35;
  const target = video.short.seconds - intro - outro - holds * holdScale;
  const k = Math.max(1, run / Math.max(10, target)); // only ever speed up

  // Captions must not overlap at the faster pace: keep at most one event per ~2.2 s of video, preferring chapters.
  const sorted = video.events.map((e, i) => ({ e, i, d: dayNumber(e.date) })).sort((a, b) => a.d - b.d);
  const keep = new Set<number>();
  let lastFrame = -Infinity;
  for (const x of sorted) {
    const f = tl.frameAt(x.d) / k;
    if (f - lastFrame >= 2.2 * fps || x.e.chapter) {
      keep.add(x.i);
      lastFrame = f;
    }
  }

  return {
    ...video,
    id: `${video.id}-short`,
    layout: "short",
    width: 1080,
    height: 1920,
    header: { ...video.header, globe: undefined, introClip: undefined, title: video.short.title ?? video.header.title },
    timeline: {
      ...video.timeline,
      introSeconds: intro,
      outroSeconds: outro,
      daysPerSecond: video.timeline.daysPerSecond * k,
      pace: video.timeline.pace.map((p) => ({ ...p, daysPerSecond: p.daysPerSecond * k })),
    },
    camera: video.camera.map((c) => ({ ...c, zoom: Math.min(4, c.zoom * video.short.zoom) })),
    events: video.events
      .filter((_, i) => keep.has(i))
      .map((e) => ({ ...e, holdSeconds: e.holdSeconds * holdScale, captionSeconds: Math.max(2.2, e.captionSeconds * 0.6), chapter: false })),
  };
}
