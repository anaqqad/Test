// QC stills for overlay cards: renders several frames of each card to PNG (no video encode).
// Usage: node stills.mjs <storyboard.json> <outDir> [cardId ...]   (env AT="0.1,0.4,0.7,0.95" = fractions of the card)
import fs from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";

const [sbPath, outDir, ...only] = process.argv.slice(2);
const sb = JSON.parse(fs.readFileSync(sbPath, "utf8"));
fs.mkdirSync(outDir, { recursive: true });
const at = (process.env.AT || "0.15,0.45,0.75,0.95").split(",").map(Number);
const serveUrl = await bundle({ entryPoint: path.join(import.meta.dirname, "src/index.ts") });
for (const card of sb.overlays) {
  if (only.length && !only.includes(card.id)) continue;
  const frames = Math.round((card.end - card.start) * sb.fps);
  const inputProps = { card, frames };
  const composition = await selectComposition({ serveUrl, id: "Overlay", inputProps });
  for (const a of at) {
    const frame = Math.min(frames - 1, Math.round(frames * a));
    const out = path.join(outDir, `${card.id}_${String(frame).padStart(4, "0")}.png`);
    await renderStill({ composition, serveUrl, output: out, frame, inputProps });
    console.log(out);
  }
}
