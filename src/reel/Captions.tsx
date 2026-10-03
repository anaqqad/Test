import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import type { MathDocTimeline } from "../mathdoc/schema";
import { Critical } from "./blocks";
import { B, SAFE, SAFE_W, serif } from "./style";

type Word = { text: string; start: number; end: number };
export type Chunk = { words: Word[]; start: number; end: number };

const MAX_WORDS = 4;
const MAX_CHARS = 28; // a chunk longer than this is split further (at most two lines at 88 px)
const PAUSE = 0.35;

/** Split n words into k groups as evenly as possible, larger groups first. */
const balanced = <T,>(items: T[], k: number): T[][] => {
  const out: T[][] = [];
  let i = 0;
  for (let g = 0; g < k; g++) {
    const size = Math.ceil((items.length - i) / (k - g));
    out.push(items.slice(i, i + size));
    i += size;
  }
  return out;
};

const chars = (ws: Word[]) => ws.map((w) => w.text).join(" ").length;

/**
 * Caption chunks of 2-4 words. The narration is cut into phrases at punctuation and at pauses
 * longer than PAUSE; a one-word phrase joins its neighbour; each phrase is then split into the
 * fewest even groups of at most 4 words (and MAX_CHARS characters), never leaving a word alone.
 * scripts/qc_reel.py mirrors this function; keep them in step.
 */
export const chunkWords = (words: Word[]): Chunk[] => {
  const phrases: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w, i) => {
    cur.push(w);
    const next = words[i + 1];
    if (!next || /[.,!?;:]$/.test(w.text) || next.start - w.end > PAUSE) {
      phrases.push(cur);
      cur = [];
    }
  });
  const merged: Word[][] = [];
  for (let i = 0; i < phrases.length; i++) {
    const p = phrases[i];
    const prev = merged[merged.length - 1];
    if (p.length === 1 && prev && prev.length < MAX_WORDS) prev.push(...p);
    else if (p.length === 1 && phrases[i + 1]) phrases[i + 1] = [...p, ...phrases[i + 1]];
    else merged.push(p);
  }
  const out: Word[][] = [];
  for (const p of merged) {
    let k = Math.ceil(p.length / MAX_WORDS);
    while (k < Math.floor(p.length / 2) && balanced(p, k).some((g) => chars(g) > MAX_CHARS)) k++;
    out.push(...balanced(p, k));
  }
  return out.map((ws) => ({ words: ws, start: ws[0].start, end: ws[ws.length - 1].end }));
};

/**
 * Word-by-word captions, driven by timeline.json: 2-4 words at a time in large serif type, cream,
 * with the word being spoken in gold. Most viewers watch with the sound off, so these carry the story.
 */
export const Captions: React.FC<{ timeline: MathDocTimeline; hidden: Set<string> }> = ({ timeline, hidden }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const chunks = React.useMemo(() => {
    const out: Chunk[] = [];
    for (const b of timeline.beats) if (!hidden.has(b.id) && b.words.length) out.push(...chunkWords(b.words));
    return out;
  }, [timeline, hidden]);
  const i = chunks.findIndex((c, k) => t >= c.start - 0.08 && t < (chunks[k + 1] ? Math.min(chunks[k + 1].start - 0.08, c.end + 0.6) : c.end + 0.6));
  if (i < 0) return null;
  const chunk = chunks[i];
  const active = chunk.words.findIndex((w, k) => t >= w.start - 0.03 && (k === chunk.words.length - 1 || t < chunk.words[k + 1].start - 0.03));
  return (
    <div style={{ position: "absolute", left: SAFE.left, width: SAFE_W, bottom: 1920 - SAFE.bottom + 40, display: "flex", justifyContent: "center" }}>
      <Critical
        style={{
          fontFamily: serif,
          fontWeight: 800,
          fontSize: 88,
          lineHeight: 1.08,
          textAlign: "center",
          color: B.cream,
          textShadow: "0 3px 0 rgba(0,0,0,0.55), 0 6px 28px rgba(0,0,0,0.9)",
          maxWidth: SAFE_W,
        }}
      >
        {chunk.words.map((w, k) => (
          <span key={k} style={{ color: k === active ? B.gold : undefined }}>
            {w.text}
            {k < chunk.words.length - 1 ? " " : ""}
          </span>
        ))}
      </Critical>
    </div>
  );
};
