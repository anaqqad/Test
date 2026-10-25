import React from "react";
import { Composition, Still } from "remotion";
import { videos } from "./videos";
import type { Video } from "./schema";
import { buildTimeline, dayNumber } from "./lib/time";
import { Timelapse } from "./Timelapse";
import { Thumbnail } from "./Thumbnail";
import { toShort } from "./short";

// Event and keyframe frames travel with the props so scripts/render.mjs can write chapters and QC stills.
function meta(video: Video) {
  const tl = buildTimeline(video);
  return {
    tl,
    events: video.events.map((e, i) => ({ frame: tl.eventFrames[i], title: e.title, chapter: e.chapter, date: e.date })),
    keyframes: video.territories.map((k) => ({ date: k.date, frame: tl.frameAt(dayNumber(k.date)) })),
  };
}

// Each video registers three compositions: the video, its thumbnail still, and its vertical Short.
export const Root: React.FC = () => (
  <>
    {videos.map((video) => {
      const main = meta(video);
      const short = toShort(video);
      const sm = meta(short);
      return (
        <React.Fragment key={video.id}>
          <Composition
            id={video.id}
            component={Timelapse}
            durationInFrames={main.tl.durationInFrames}
            fps={video.fps}
            width={video.width}
            height={video.height}
            defaultProps={{ video, events: main.events, keyframes: main.keyframes }}
          />
          <Still id={`${video.id}-thumb`} component={Thumbnail} width={1920} height={1080} defaultProps={{ video }} />
          <Composition
            id={short.id}
            component={Timelapse}
            durationInFrames={sm.tl.durationInFrames}
            fps={short.fps}
            width={1080}
            height={1920}
            defaultProps={{ video: short, events: sm.events, keyframes: sm.keyframes }}
          />
        </React.Fragment>
      );
    })}
  </>
);
