import React from "react";
import { Composition, Folder, Still } from "remotion";
import robertSmalls from "../data/reel-robert-smalls.json";
import docSmalls from "../data/doc-robert-smalls.json";
import { calculateReelMetadata, Reel } from "./reel/Reel";
import { type ReelSpec, reelSpecSchema } from "./reel/schema";
import { calculateDocMetadata, Doc } from "./doc/Doc";
import { type DocSpec, docSpecSchema } from "./doc/schema";
import { Thumb, thumbSchema } from "./doc/Thumb";

const smalls: ReelSpec = reelSpecSchema.parse(robertSmalls);
const doc: DocSpec = docSpecSchema.parse(docSmalls);

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
      <Folder name="Docs">
        {/* Long-form 1920x1080 documentaries (~8 min). Render others with --props=<data/doc-*.json> */}
        <Composition
          id="Doc"
          component={Doc}
          schema={docSpecSchema}
          defaultProps={doc}
          calculateMetadata={calculateDocMetadata}
          durationInFrames={15000}
          fps={doc.fps}
          width={doc.width}
          height={doc.height}
        />
        <Still
          id="DocThumb"
          component={Thumb}
          schema={thumbSchema}
          defaultProps={{ folder: "doc-robert-smalls", image: "portrait", position: "45% 18%", zoom: 1.0, kicker: "He stole a warship.", label: "Then he bought it", sub: "his master's house" }}
          width={1280}
          height={720}
        />
      </Folder>
    </>
  );
};
