// Render a video from its JSON, plus thumbnail, YouTube description with chapters, and optional QC stills.
//   node scripts/render.mjs korean-war              -> out/<id>/<id>.mp4, thumbnail.jpg, description.txt
//   node scripts/render.mjs korean-war --qc         -> out/<id>/qc/ one still per event, for fact-checking
//   node scripts/render.mjs korean-war --short      -> out/<id>/<id>-short.mp4 (vertical 1080x1920) + short-description.txt
//   node scripts/render.mjs korean-war --keyframes  -> out/<id>/keys/ one still per territory keyframe
//   node scripts/render.mjs korean-war --frames=0,450,900
//   node scripts/render.mjs korean-war --range=0-299 -> render only these frames (timing / previews)
//   options: --concurrency=N, --scale=0.5 (fast preview), --browser=/path/to/chrome (or env REMOTION_BROWSER)
import fs from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";

const args = process.argv.slice(2);
const baseId = args.find((a) => !a.startsWith("--"));
const opt = (name) => args.find((a) => a.startsWith(`--${name}`))?.split("=")[1] ?? (args.includes(`--${name}`) ? true : undefined);
if (!baseId) throw new Error("usage: node scripts/render.mjs <video-id> [--short] [--qc] [--frames=a,b] [--scale=0.5]");
const isShort = Boolean(opt("short"));
const id = isShort ? `${baseId}-short` : baseId;

const outDir = path.resolve("out", baseId);
fs.mkdirSync(outDir, { recursive: true });
const browserExecutable = opt("browser") || process.env.REMOTION_BROWSER || null;
const scale = Number(opt("scale") ?? 1);
const concurrency = opt("concurrency") ? Number(opt("concurrency")) : null;

const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const common = { serveUrl, browserExecutable, chromiumOptions: { gl: "swangle" } };
const composition = await selectComposition({ ...common, id });
const { events, video } = composition.props;

// Remotion ships its own ffmpeg, so this works on Windows without installing one.
const ffmpeg = (ffArgs) => {
  const r = spawnSync(process.platform === "win32" ? "npx.cmd" : "npx", ["remotion", "ffmpeg", ...ffArgs], { encoding: "utf8", shell: process.platform === "win32" });
  if (r.status !== 0) throw new Error(r.stderr.slice(-2000));
  return r.stderr;
};
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
} else if (opt("keyframes")) {
  const dir = path.join(outDir, "keys");
  fs.mkdirSync(dir, { recursive: true });
  for (const [i, k] of composition.props.keyframes.entries()) {
    await still(Math.min(composition.durationInFrames - 1, k.frame), path.join(dir, `${String(i).padStart(2, "0")}-${k.date}.jpg`));
  }
} else if (opt("qc")) {
  const dir = path.join(outDir, "qc");
  fs.mkdirSync(dir, { recursive: true });
  for (const [i, e] of events.entries()) {
    await still(Math.min(composition.durationInFrames - 1, e.frame + composition.fps), path.join(dir, `${String(i).padStart(2, "0")}-${e.date}.jpg`));
  }
} else {
  const raw = path.join(outDir, `${id}.raw.mp4`);
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
    outputLocation: raw,
    frameRange: opt("range") ? String(opt("range")).split("-").map(Number) : null,
    onProgress: ({ progress }) => {
      const pct = Math.floor(progress * 20) * 5;
      if (pct !== last) process.stdout.write(`${(last = pct)}% `);
    },
  });
  const secs = (Date.now() - t0) / 1000;
  const frames = opt("range") ? String(opt("range")).split("-").map(Number).reduce((a, b) => b - a + 1) : composition.durationInFrames;
  console.log(`\nrendered in ${secs.toFixed(0)} s (${((secs * 1000) / frames).toFixed(0)} ms/frame)`);

  // Two-pass loudness normalisation to YouTube's -14 LUFS, true peak -1 dBTP; video stream copied untouched.
  const target = "I=-14:TP=-1:LRA=11";
  const m = ffmpeg(["-hide_banner", "-i", raw, "-vn", "-af", `loudnorm=${target}:print_format=json`, "-f", "null", "-"]);
  const j = JSON.parse(m.slice(m.lastIndexOf("{"), m.lastIndexOf("}") + 1));
  ffmpeg(["-hide_banner", "-y", "-i", raw, "-c:v", "copy", "-af",
    `loudnorm=${target}:measured_I=${j.input_i}:measured_TP=${j.input_tp}:measured_LRA=${j.input_lra}:measured_thresh=${j.input_thresh}:offset=${j.target_offset}:linear=true`,
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", mp4]);
  fs.rmSync(raw);
  console.log(`wrote ${path.relative(".", mp4)} (audio ${j.input_i} -> -14 LUFS)`);
  if (opt("range")) process.exit(0);

  if (isShort) {
    // Shorts: no chapters or thumbnail upload; title + one line + credits.
    const yt = video.youtube;
    fs.writeFileSync(path.join(outDir, "short-description.txt"),
      [`${video.header.title}, day by day`, "", yt.summary, "", "Full video on the channel.", "", ...(yt.credits.length ? ["Music / data:", ...yt.credits] : []), ""].join("\n"));
    console.log("wrote", path.relative(".", path.join(outDir, "short-description.txt")));
    process.exit(0);
  }
  const thumb = await selectComposition({ ...common, id: `${id}-thumb` });
  await still(0, path.join(outDir, "thumbnail.jpg"), thumb);

  // YouTube chapters: first at 0:00, at least 3, each at least 10 s long.
  const chapters = [{ frame: 0, title: "Intro" }];
  for (const e of events.filter((x) => x.chapter && x.frame > 0)) {
    if (e.frame - chapters[chapters.length - 1].frame >= 10 * composition.fps) chapters.push(e);
  }
  const lines = chapters.length >= 3 ? chapters.map((c) => `${stamp(c.frame)} ${c.title}`) : [];
  const yt = video.youtube;
  const desc = [
    yt.summary || "[One-line summary of the video]",
    "",
    ...lines,
    "",
    ...(video.header.footnote ? [video.header.footnote, ""] : []),
    "Sources:",
    ...(yt.sources.length ? yt.sources.map((s) => `- ${s}`) : ["[list sources here]"]),
    "",
    ...(yt.credits.length ? ["Music:", ...yt.credits, ""] : []),
    "Map data: Natural Earth (public domain).",
  ];
  fs.writeFileSync(path.join(outDir, "description.txt"), desc.join("\n") + "\n");
  fs.writeFileSync(path.join(outDir, "upload.txt"), [`Title: ${yt.title || video.header.title}`, `Tags: ${yt.tags.join(", ")}`, ""].join("\n"));
  console.log("wrote", path.relative(".", path.join(outDir, "description.txt")));
}
