import { z } from "zod";
import { timelineSchema } from "../mathdoc/schema";
import { imageMetaSchema, reelOverlaysSchema, reelVisualSchema } from "../reel/schema";

/**
 * Doc: horizontal 1920x1080 long-form documentary (about 8 minutes) for YouTube.
 * Same spec shape as the Reel (and MathDoc), so scripts/tts_mathdoc.py voices it unchanged.
 * Adds chapter cards and quote cards; captions are phrase subtitles at the bottom.
 */
export const docVisualSchema = reelVisualSchema.extend({
  kind: z.enum(["photo", "card", "map", "title", "thennow", "endcard", "chapter", "quote"]),
  /** chapter: number and title */
  num: z.number().optional(),
  /** quote: the words and who said them */
  quote: z.string().optional(),
  by: z.string().optional(),
});

export const docBeatSchema = z.object({
  id: z.string(),
  text: z.string(),
  section: z.string().optional(),
  visual: docVisualSchema,
  overlays: reelOverlaysSchema.optional(),
  captions: z.boolean().optional(),
  cues: z.record(z.string(), z.string()).optional(),
});

export const docSpecSchema = z.object({
  id: z.string(),
  title: z.string(),
  format: z.literal("doc"),
  fps: z.number().default(30),
  width: z.number().default(1920),
  height: z.number().default(1080),
  voice: z.object({ engine: z.string() }).passthrough(),
  music: z.object({ volume: z.number() }).optional(),
  mix: z.record(z.string(), z.number()).optional(),
  brand: z.object({
    page: z.string(),
    cta: z.string(),
    ctaLine: z.string().default(""),
    theme: z.enum(["bhr", "bbu"]).default("bhr"),
  }),
  assets: z.record(z.string(), z.object({ commons: z.string() })).default({}),
  faces: z.record(z.string(), z.array(z.tuple([z.number(), z.number(), z.number(), z.number()]))).default({}),
  beats: z.array(docBeatSchema).min(1),
  facts: z.array(z.any()).optional(),
  timeline: timelineSchema.optional(),
  images: z.record(z.string(), imageMetaSchema).optional(),
  hasMix: z.boolean().optional(),
});

export type DocSpec = z.infer<typeof docSpecSchema>;
export type DocBeat = z.infer<typeof docBeatSchema>;
