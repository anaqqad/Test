import React from "react";
import { AbsoluteFill, Composition } from "remotion";
import { ContextTag, Slug } from "./overlays";
import { PhotoCard } from "./photo";
import { LedgerBars, LedgerClipping, LedgerMap, LedgerQuote, LedgerTimeline } from "./ledger";

// One overlay = one entry of build/storyboard.json, rendered alone (ProRes 4444 with alpha) and laid
// over the footage track by tools/assemble.py.
const Overlay: React.FC<{ card: Record<string, any>; frames: number }> = ({ card: c }) => {
  switch (c.type) {
    case "ContextTag": return <ContextTag text={c.text} />;
    case "Slug": return <Slug title={c.title} subtitle={c.subtitle} />;
    case "PhotoCard": return <PhotoCard {...(c as any)} />;
    case "LedgerTimeline": return <LedgerTimeline file={c.file} head={c.head} rows={c.rows} source={c.source} />;
    case "LedgerBars": return <LedgerBars file={c.file} head={c.head} bars={c.bars} max={c.max} source={c.source} />;
    case "LedgerQuote": return <LedgerQuote file={c.file} head={c.head} before={c.before} key_={c.key} after={c.after} who={c.who} source={c.source} />;
    case "LedgerClipping": return <LedgerClipping file={c.file} head={c.head} kicker={c.kicker} headline={c.headline} dateline={c.dateline} body={c.body} source={c.source} />;
    case "LedgerMap": return <LedgerMap file={c.file} head={c.head} stops={c.stops} legs={c.legs} extra={c.extra} source={c.source} />;
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
    defaultProps={{ card: { type: "Slug", title: "January 2, 1944", subtitle: "Norfolk, Virginia" }, frames: 150 }}
    calculateMetadata={({ props }) => ({ durationInFrames: props.frames })}
  />
);
