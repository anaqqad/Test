import { z } from "zod";
import { timelineSchema } from "../mathdoc/schema";

/**
 * Reel: vertical 1080x1920 short (Facebook / Instagram Reels, YouTube Shorts).
 * Same spec shape as MathDoc (id, voice, assets, beats[{id, text, section, visual}]), so
 * scripts/tts_mathdoc.py voices it unchanged and writes the same timeline.json.
 * Visuals are photo-led: Ken Burns on archival images, cards, an illustrative map, an end card.
 */

/** [x0, y0, x1, y1] in 0..1 image coordinates */
const box = z.tuple([z.number(), z.number(), z.number(), z.number()]);

export const reelVisualSchema = z.object({
  kind: z.enum(["photo", "card", "map", "title", "thennow", "endcard"]),
  /** asset key (public/pd/<id>/<key>.jpg) */
  image: z.string().optional(),
  /** photo: image point (0..1) the camera holds on, and where on screen (0..1) it sits */
  focus: z.tuple([z.number(), z.number()]).optional(),
  anchor: z.tuple([z.number(), z.number()]).optional(),
  /** photo: zoom over the beat, 1 = just covers the frame */
  zoom: z.tuple([z.number(), z.number()]).optional(),
  motion: z.enum(["zoom", "panLeft", "panRight"]).optional(),
  /** card: part of the image to show, and the line under it */
  crop: box.optional(),
  caption: z.string().optional(),
  /** card: style it as a newspaper clipping (paper, torn edge, slight tilt) */
  clipping: z.boolean().optional(),
  /** title: typographic card for beats with no fitting picture (a year, a date, a short line) */
  title: z.string().optional(),
  sub: z.string().optional(),
  /** thennow: old and current photo of the same place; a gold line wipes from then to now */
  then: z.string().optional(),
  now: z.string().optional(),
  thenFocus: z.tuple([z.number(), z.number()]).optional(),
  nowFocus: z.tuple([z.number(), z.number()]).optional(),
  thenLabel: z.string().optional(),
  nowLabel: z.string().optional(),
  /** map: which leg of the route this beat shows */
  step: z.enum(["wharf", "forts", "sumter", "fleet"]).optional(),
});

export const reelOverlaysSchema = z.object({
  /** big bold opening line (the hook); on screen from frame 0 */
  hook: z.string().optional(),
  lowerThird: z.object({ name: z.string(), sub: z.string().optional() }).optional(),
  /** year counter: counts from -> to over the beat */
  year: z.object({ from: z.number(), to: z.number() }).optional(),
  /** location chip with a map pin */
  pin: z.object({ label: z.string(), sub: z.string().optional() }).optional(),
  /** short gold label stamped mid-frame, e.g. a date or a number */
  stamp: z.string().optional(),
});

export const reelBeatSchema = z.object({
  id: z.string(),
  text: z.string(),
  section: z.string().optional(),
  visual: reelVisualSchema,
  overlays: reelOverlaysSchema.optional(),
  /** word-by-word captions for this beat (off for the hook and end card, which show their own text) */
  captions: z.boolean().optional(),
  cues: z.record(z.string(), z.string()).optional(),
});

export const imageMetaSchema = z.object({ width: z.number(), height: z.number() });

export const reelSpecSchema = z.object({
  id: z.string(),
  title: z.string(),
  format: z.literal("reel"),
  fps: z.number().default(30),
  width: z.number().default(1080),
  height: z.number().default(1920),
  voice: z.object({ engine: z.string() }).passthrough(),
  music: z.object({ volume: z.number() }).optional(),
  mix: z.record(z.string(), z.number()).optional(),
  brand: z.object({ page: z.string(), cta: z.string() }),
  assets: z.record(z.string(), z.object({ commons: z.string() })).default({}),
  /** face boxes per asset key, [x0,y0,x1,y1] in 0..1 image coordinates (safe-zone QC) */
  faces: z.record(z.string(), z.array(box)).default({}),
  beats: z.array(reelBeatSchema).min(1),
  facts: z.array(z.any()).optional(),
  /** attached by calculateReelMetadata */
  timeline: timelineSchema.optional(),
  images: z.record(z.string(), imageMetaSchema).optional(),
  hasMix: z.boolean().optional(),
  /** render the safe-zone QC mask instead of the picture (scripts/qc_reel.py) */
  qc: z.boolean().optional(),
});

export type ReelSpec = z.infer<typeof reelSpecSchema>;
export type ReelBeat = z.infer<typeof reelBeatSchema>;
export type ReelVisual = z.infer<typeof reelVisualSchema>;
