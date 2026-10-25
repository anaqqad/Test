import React from "react";
import { Composition, Still } from "remotion";
import { videos } from "./videos";
import { buildTimeline, dayNumber } from "./lib/time";
import { Timelapse } from "./Timelapse";
import { Thumbnail } from "./Thumbnail";

export const Root: React.FC = () => (
  <>
    {videos.map((video) => {
      const tl = buildTimeline(video);
      // Event frames travel with the props so scripts/render.mjs can write chapters and QC stills.
      const events = video.events.map((e, i) => ({ frame: tl.eventFrames[i], title: e.title, chapter: e.chapter, date: e.date }));
      const keyframes = video.territories.map((k) => ({ date: k.date, frame: tl.frameAt(dayNumber(k.date)) }));
      return (
      <React.Fragment key={video.id}>
        <Composition
          id={video.id}
          component={Timelapse}
          durationInFrames={tl.durationInFrames}
          fps={video.fps}
          width={video.width}
          height={video.height}
          defaultProps={{ video, events, keyframes }}
        />
        <Still id={`${video.id}-thumb`} component={Thumbnail} width={1920} height={1080} defaultProps={{ video }} />
      </React.Fragment>
      );
    })}
  </>
);
