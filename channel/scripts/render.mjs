// Render a video from its JSON, plus thumbnail, YouTube description with chapters, and optional QC stills.
//   node scripts/render.mjs korean-war-demo              -> out/<id>/<id>.mp4, thumbnail.jpg, description.txt
//   node scripts/render.mjs korean-war-demo --qc         -> out/<id>/qc/ one still per event, for fact-checking
//   node scripts/render.mjs korean-war-demo --frames=0,450,900
//   node scripts/render.mjs korean-war-demo --range=0-299 -> render only these frames (timing / previews)
//   options: --concurrency=N, --scale=0.5 (fast preview), --browser=/path/to/chrome (or env REMOTION_BROWSER)
import fs from "node:fs";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";

const args = process.argv.slice(2);
const id = args.find((a) => !a.startsWith("--"));
const opt = (name) => args.find((a) => a.startsWith(`--${name}`))?.split("=")[1] ?? (args.includes(`--${name}`) ? true : undefined);
if (!id) throw new Error("usage: node scripts/render.mjs <video-id> [--qc] [--frames=a,b] [--scale=0.5]");

const outDir = path.resolve("out", id);
fs.mkdirSync(outDir, { recursive: true });
const browserExecutable = opt("browser") || process.env.REMOTION_BROWSER || null;
const scale = Number(opt("scale") ?? 1);
const concurrency = opt("concurrency") ? Number(opt("concurrency")) : null;

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const common = { serveUrl, browserExecutable, chromiumOptions: { gl: "swangle" } };
const composition = await selectComposition({ ...common, id });
const { events } = composition.props;
const stamp = (frame) => {
  const s = Math.floor(frame / composition.fps);
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
};
const still = async (frame, file, comp = composition) => {
  await renderStill({ ...common, composition: comp, frame, output: file, imageFormat: "jpeg", jpegQuality: 90, scale });
  console.log("wrote", path.relative(".", file));
};

if (opt("frames")) {
  for (const f of String(opt("frames")).split(",").map(Number)) await still(f, path.join(outDir, `frame-${String(f).padStart(5, "0")}.jpg`));
} else if (opt("qc")) {
  const dir = path.join(outDir, "qc");
  fs.mkdirSync(dir, { recursive: true });
  for (const [i, e] of events.entries()) {
    await still(Math.min(composition.durationInFrames - 1, e.frame + composition.fps), path.join(dir, `${String(i).padStart(2, "0")}-${e.date}.jpg`));
  }
} else {
  const mp4 = path.join(outDir, `${id}.mp4`);
  const t0 = Date.now();
  let last = -1;
  await renderMedia({
    ...common,
    composition,
    codec: "h264",
    crf: 16,
    scale,
    concurrency,
    outputLocation: mp4,
    frameRange: opt("range") ? String(opt("range")).split("-").map(Number) : null,
    onProgress: ({ progress }) => {
      const pct = Math.floor(progress * 20) * 5;
      if (pct !== last) process.stdout.write(`${(last = pct)}% `);
    },
  });
  const secs = (Date.now() - t0) / 1000;
  const frames = opt("range") ? String(opt("range")).split("-").map(Number).reduce((a, b) => b - a + 1) : composition.durationInFrames;
  console.log(`\nwrote ${path.relative(".", mp4)} in ${secs.toFixed(0)} s (${((secs * 1000) / frames).toFixed(0)} ms/frame)`);
  if (opt("range")) process.exit(0);

  const thumb = await selectComposition({ ...common, id: `${id}-thumb` });
  await still(0, path.join(outDir, "thumbnail.jpg"), thumb);

  // YouTube chapters: first at 0:00, at least 3, each at least 10 s long.
  const chapters = [{ frame: 0, title: "Intro" }];
  for (const e of events.filter((x) => x.chapter && x.frame > 0)) {
    if (e.frame - chapters[chapters.length - 1].frame >= 10 * composition.fps) chapters.push(e);
  }
  const lines = chapters.length >= 3 ? chapters.map((c) => `${stamp(c.frame)} ${c.title}`) : [];
  fs.writeFileSync(path.join(outDir, "description.txt"), ["[One-line summary of the video]", "", ...lines, "", "Sources:", "[list sources here]", ""].join("\n"));
  console.log("wrote", path.relative(".", path.join(outDir, "description.txt")));
}
