import React from "react";
import { AbsoluteFill, Composition } from "remotion";
import { ContextLabel, DocumentCard, LowerThirdCard, RouteMapCard, TimelineCard } from "./cards";

// One overlay = one card from storyboard.json, rendered on its own with alpha and laid over the
// footage track by tools/assemble.py. `frames` is the card's length.
type Props = { card: Record<string, any>; frames: number };

const Overlay: React.FC<Props> = ({ card }) => {
  const c = card as any;
  switch (c.type) {
    case "ContextLabel": return <ContextLabel text={c.text} />;
    case "LowerThird": return <LowerThirdCard title={c.title} subtitle={c.subtitle} source={c.source} width={c.width} />;
    case "TimelineCard": return <TimelineCard title={c.title} points={c.points} source={c.source} />;
    case "DocumentCard": return <DocumentCard doc={c.doc} title={c.title} subtitle={c.subtitle} source={c.source} />;
    case "RouteMapCard": return <RouteMapCard title={c.title} subtitle={c.subtitle} stops={c.stops} legs={c.legs} source={c.source} extra={c.extra} />;
    default: return <AbsoluteFill />;
  }
};

export const Root: React.FC = () => (
  <Composition
    id="Overlay"
    component={Overlay}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={150}
    defaultProps={{ card: { type: "LowerThird", title: "May 12, 1943", subtitle: "Surrender on Cap Bon, Tunisia" }, frames: 150 }}
    calculateMetadata={({ props }) => ({ durationInFrames: props.frames })}
  />
);
