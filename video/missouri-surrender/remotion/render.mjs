// Renders every overlay card in ../storyboard.json to ../build/overlays/<id>.webm (VP9 with alpha: a few MB each,
// where ProRes 4444 needed hundreds; tools/assemble.py decodes it with libvpx-vp9 to keep the alpha).
// Usage: node render.mjs [cardId ...]   (no ids = all cards that are missing or older than the storyboard)
import fs from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";

const root = path.resolve(import.meta.dirname, "..");
const sb = JSON.parse(fs.readFileSync(process.env.SB || path.join(root, "build/storyboard.json"), "utf8"));
const outDir = process.env.OUT || path.join(root, "build/overlays");
fs.mkdirSync(outDir, { recursive: true });
const only = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const stills = process.argv.includes("--stills");
// stills are served from public/stills (gitignored); copy them from assets/stills
fs.mkdirSync(path.join(import.meta.dirname, "public/stills"), { recursive: true });
for (const f of fs.readdirSync(path.join(root, "assets/stills"))) fs.copyFileSync(path.join(root, "assets/stills", f), path.join(import.meta.dirname, "public/stills", f));
// null = Remotion downloads its own headless Chrome on first run; set BROWSER to use a local one
const browserExecutable = process.env.BROWSER || null;
const serveUrl = await bundle({ entryPoint: path.join(import.meta.dirname, "src/index.ts") });
for (const card of sb.overlays) {
  if (only.length && !only.includes(card.id)) continue;
  const frames = Math.round((card.end - card.start) * sb.fps);
  const inputProps = { card, frames };
  let composition;
  try { composition = await selectComposition({ serveUrl, id: "Overlay", inputProps, browserExecutable, timeoutInMilliseconds: 180000 }); }
  catch (e) { console.log(card.id, "Error:", String(e).slice(0, 160)); continue; }
  if (stills) {
    const out = path.join(outDir, `${card.id}.png`);
    await renderStill({ composition, serveUrl, output: out, frame: Math.max(0, frames - 22), inputProps, browserExecutable });
    console.log("still", out);
    continue;
  }
  // full-screen cards need no alpha: JPEG frames take ~1/6 of the temp space of PNG
  const OPAQUE = new Set(["QuoteCard", "DocDesk", "GlobeMap"]);  // these never fade to transparent
  const out = path.join(outDir, `${card.id}.webm`);
  const t = Date.now();
  try { await renderMedia({
    composition, serveUrl, codec: "vp9", ...(OPAQUE.has(card.type) ? { pixelFormat: "yuv420p", imageFormat: "jpeg", jpegQuality: 92 } : { pixelFormat: "yuva420p", imageFormat: "png" }), crf: 18,
    outputLocation: out, inputProps, browserExecutable, concurrency: 3, muted: true,
    // HEIGHT=720 renders 1280x720 (the published size): frames are written to temp as PNGs first, ~2 MB each at 1080p
    scale: Number(process.env.HEIGHT || 1080) / 1080, timeoutInMilliseconds: 180000,
  }); } catch (e) { console.log(card.id, "Error:", String(e).slice(0, 160)); try { fs.unlinkSync(out); } catch {} continue; }
  console.log(card.id, frames, "frames", ((Date.now() - t) / 1000).toFixed(0) + "s");
}
