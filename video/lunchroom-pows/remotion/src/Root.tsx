import React from "react";
import { AbsoluteFill, Composition } from "remotion";
import { BigNumber, ContextTag, Slug, SubscribeButton } from "./overlays";
import { ArchivePrint, PhotoCard } from "./photo";
import { Chart, IconCount, ObjectTurn, Section } from "./scenes";
import { CastCard, CodeWord, Headline, Verdict } from "./cards";
import { DocDesk, GlobeMap, QuoteCardJ } from "./devices";
import { LedgerDocument } from "./document";
import { LedgerBars, LedgerClipping, LedgerMap, LedgerQuote, LedgerTimeline } from "./ledger";

// One overlay = one entry of build/storyboard.json, rendered alone (ProRes 4444 with alpha) and laid
// over the footage track by tools/assemble.py.
const Overlay: React.FC<{ card: Record<string, any>; frames: number }> = ({ card: c }) => {
  switch (c.type) {
    case "ContextTag": return <ContextTag text={c.text} />;
    case "Slug": return <Slug title={c.title} subtitle={c.subtitle} />;
    case "SubscribeButton": return <SubscribeButton channel={c.channel} tagline={c.tagline} />;
    case "BigNumber": return <BigNumber value={c.value} label={c.label} source={c.source} />;
    case "PhotoCard": return <PhotoCard {...(c as any)} />;
    case "ArchivePrint": return <ArchivePrint {...(c as any)} />;
    case "LedgerDocument": return <LedgerDocument {...(c as any)} />;
    case "LedgerTimeline": return <LedgerTimeline file={c.file} head={c.head} rows={c.rows} source={c.source} />;
    case "LedgerBars": return <LedgerBars file={c.file} head={c.head} bars={c.bars} max={c.max} source={c.source} />;
    case "LedgerQuote": return <LedgerQuote file={c.file} head={c.head} before={c.before} key_={c.key} after={c.after} who={c.who} source={c.source} />;
    case "LedgerClipping": return <LedgerClipping file={c.file} head={c.head} kicker={c.kicker} headline={c.headline} dateline={c.dateline} body={c.body} source={c.source} />;
    case "LedgerMap": return <LedgerMap file={c.file} head={c.head} stops={c.stops} legs={c.legs} extra={c.extra} source={c.source} />;
    case "Section": return <Section {...(c as any)} />;
    case "Chart": return <Chart {...(c as any)} />;
    case "IconCount": return <IconCount {...(c as any)} />;
    case "ObjectTurn": return <ObjectTurn {...(c as any)} />;
    case "CastCard": return <CastCard {...(c as any)} />;
    case "Headline": return <Headline {...(c as any)} />;
    case "CodeWord": return <CodeWord {...(c as any)} />;
    case "Verdict": return <Verdict {...(c as any)} />;
    case "QuoteCard": return <QuoteCardJ {...(c as any)} />;
    case "DocDesk": return <DocDesk {...(c as any)} />;
    case "GlobeMap": return <GlobeMap {...(c as any)} />;
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
