import React from "react";
import { Composition, Folder } from "remotion";
import robertSmalls from "../data/reel-robert-smalls.json";
import { calculateReelMetadata, Reel } from "./reel/Reel";
import { type ReelSpec, reelSpecSchema } from "./reel/schema";

const smalls: ReelSpec = reelSpecSchema.parse(robertSmalls);

export const RemotionRoot: React.FC = () => {
  return (
    <Folder name="Reels">
      {/* The Black History Room: vertical 1080x1920 reels. Render other stories with --props=<data/reel-*.json> */}
      <Composition
        id="Reel"
        component={Reel}
        schema={reelSpecSchema}
        defaultProps={smalls}
        calculateMetadata={calculateReelMetadata}
        durationInFrames={1800}
        fps={smalls.fps}
        width={smalls.width}
        height={smalls.height}
      />
    </Folder>
  );
};
