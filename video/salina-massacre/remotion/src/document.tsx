// "Marked document": how the channel shows one sentence on a real scanned page.
// The scan lies on the field ledger, the view closes in on the passage, and a grease-pencil highlighter
// runs along the printed lines in step with the narration, with a bracket drawn in the margin beside it.
// Rects come from tools/doc_spans.py (scan pixels); timing comes from tools/plan.py (seconds into the card).
import React from "react";
import { Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C } from "./theme";
import { Stroke, wobble } from "./marks";
import { Paper } from "./ledger";

type Span = { rects: number[][]; at: number; dur: number };
export type DocumentProps = { file: string; head: string; image: string; pw: number; ph: number; spans: Span[]; source: string };

// the part of the ledger the scan may fill: right of the margin rule, between the headline and the source line
const VIEW = { x: 220, y: 250, w: 1580, h: 720 };
const FILL = 0.92; // the highlighted passage ends up this wide in the view

const bandPath = (x: number, y: number, w: number, h: number, seed: number) => {
  // a marker stroke, not a box: uneven top and bottom edges
  const top = wobble([[x, y + 2], [x + w, y]], seed, 2.4).slice(1);
  const bottom = wobble([[x + w, y + h], [x, y + h - 2]], seed + 1, 2.4).slice(1);
  return `M${top}L${bottom}Z`;
};

export const LedgerDocument: React.FC<DocumentProps> = ({ file, head, image, pw, ph, spans, source }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const all = spans.flatMap((s) => s.rects);
  const x0 = Math.min(...all.map((r) => r[0])), x1 = Math.max(...all.map((r) => r[0] + r[2]));
  const y0 = Math.min(...all.map((r) => r[1])), y1 = Math.max(...all.map((r) => r[1] + r[3]));

  // the view: first the whole scan, then the passage
  const kWide = Math.min(VIEW.w / pw, VIEW.h / ph);
  const kNear = Math.max(kWide, Math.min((VIEW.w * FILL) / (x1 - x0), (VIEW.h * 0.7) / (y1 - y0)));
  const firstAt = spans[0].at * fps;
  const move1 = Math.max(38, firstAt - 3), move0 = Math.max(14, move1 - 75); // closes in just before the sentence is read
  const m = interpolate(f, [move0, move1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  const k = kWide * Math.pow(kNear / kWide, m);
  const cx = interpolate(m, [0, 1], [pw / 2, (x0 + x1) / 2]);
  const cy = interpolate(m, [0, 1], [ph / 2, (y0 + y1) / 2]);
  const left = VIEW.w / 2 - cx * k, top = VIEW.h / 2 - cy * k;
  const seen = interpolate(f, [2, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <Paper file={file} head={head} source={source}>
      <div style={{ position: "absolute", left: VIEW.x, top: VIEW.y, width: VIEW.w, height: VIEW.h, overflow: "hidden", opacity: seen }}>
        <div style={{ position: "absolute", left, top, width: pw, height: ph, transform: `scale(${k})`, transformOrigin: "0 0", background: C.paper, boxShadow: `0 0 0 ${1.5 / k}px ${C.gridMajor}` }}>
          <Img src={staticFile(`stills/${image}`)} style={{ position: "absolute", left: 0, top: 0, width: pw, height: ph, filter: "grayscale(1) contrast(1.08)", mixBlendMode: "multiply" }} />
          <svg width={pw} height={ph} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", mixBlendMode: "multiply" }}>
            {spans.map((s, j) => {
              const total = s.rects.reduce((t, r) => t + r[2], 0);
              const run = interpolate(f, [s.at * fps, (s.at + s.dur) * fps], [0, total], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              let before = 0;
              return s.rects.map((r, i) => {
                const shown = Math.max(0, Math.min(r[2], run - before));
                before += r[2];
                return (
                  <React.Fragment key={`${j}-${i}`}>
                    <clipPath id={`run-${j}-${i}`}><rect x={r[0] - 6} y={r[1] - 8} width={shown + 6} height={r[3] + 16} /></clipPath>
                    <path d={bandPath(r[0], r[1], r[2], r[3], 31 + j * 7 + i * 3)} fill={C.grease} fillOpacity={0.5} clipPath={`url(#run-${j}-${i})`} />
                  </React.Fragment>
                );
              });
            })}
          </svg>
          <svg width={pw} height={ph} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
            {spans.map((s, j) => {
              const a = Math.min(...s.rects.map((r) => r[0])) - 20;
              const t = s.rects[0][1] - 4, b = s.rects[s.rects.length - 1][1] + s.rects[s.rects.length - 1][3] + 4;
              const p = interpolate(f, [s.at * fps - 4, s.at * fps + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
              return <Stroke key={j} d={wobble([[a + 12, t], [a, t], [a, b], [a + 12, b]], 40 + j, 1)} p={p} w={7 / k} />;
            })}
          </svg>
        </div>
      </div>
    </Paper>
  );
};
