import { z } from "zod";

/**
 * MathDoc: history-of-math documentary in the "diagram + archive" style.
 * One beat = one picture = one clause or sentence of narration. Timing is not written
 * in the spec: scripts/tts_mathdoc.py measures the voice-over and writes
 * public/generated/<id>/timeline.json, which calculateMathDocMetadata attaches here.
 */
export const mathDocVisualSchema = z.object({
  kind: z.enum(["diagram", "image"]),
  /** diagram name from src/mathdoc/diagrams.tsx */
  diagram: z.string().optional(),
  background: z.enum(["slate", "concrete", "parchment"]).optional(),
  /** asset key (public/pd/<id>/<key>.jpg) */
  image: z.string().optional(),
  /** image camera move: revealOut = start on the focus and pull back; pushIn = slow push to the focus */
  motion: z.enum(["revealOut", "pushIn", "panRight", "static"]).optional(),
  focus: z.tuple([z.number(), z.number()]).optional(),
  /** parchment name plaque, like the reference's portrait labels */
  plaque: z.string().optional(),
  /** red scribbled-out inset card, e.g. the number someone disputes */
  stamp: z.string().optional(),
  /** how this picture enters: hard cut (default) or dissolve over the previous one */
  entrance: z.enum(["cut", "matchDissolve"]).optional(),
  /** per-beat options for the diagram (labels, numbers, modes) */
  props: z.record(z.string(), z.any()).optional(),
});

export const mathDocBeatSchema = z.object({
  id: z.string(),
  text: z.string(),
  visual: mathDocVisualSchema,
  /** diagram step name -> spoken word that triggers it */
  cues: z.record(z.string(), z.string()).optional(),
  /** starts a new narration section (ElevenLabs synthesizes one section per request) */
  section: z.string().optional(),
});

export const timelineSchema = z.object({
  fps: z.number(),
  durationInFrames: z.number(),
  beats: z.array(
    z.object({
      id: z.string(),
      startFrame: z.number(),
      endFrame: z.number(),
      cues: z.record(z.string(), z.number()),
      words: z.array(z.object({ text: z.string(), start: z.number(), end: z.number() })),
    }),
  ),
});

export const mathDocSpecSchema = z.object({
  id: z.string(),
  title: z.string(),
  fps: z.number().default(30),
  width: z.number().default(1920),
  height: z.number().default(1080),
  // kokoro: { voice }, elevenlabs: { voiceId, model, stability, similarity, speed, ... }
  voice: z.object({ engine: z.string(), voice: z.string().optional(), voiceId: z.string().optional() }).passthrough(),
  music: z.object({ volume: z.number() }).optional(),
  assets: z.record(z.string(), z.object({ commons: z.string() })).default({}),
  beats: z.array(mathDocBeatSchema).min(1),
  /** attached by calculateMathDocMetadata */
  timeline: timelineSchema.optional(),
  hasMusic: z.boolean().optional(),
  hasMix: z.boolean().optional(),
});

export type MathDocSpec = z.infer<typeof mathDocSpecSchema>;
export type MathDocBeat = z.infer<typeof mathDocBeatSchema>;
export type MathDocTimeline = z.infer<typeof timelineSchema>;
