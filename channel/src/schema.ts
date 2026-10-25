// One JSON file describes one whole video. Everything the renderer does is derived from it.
import { z } from "zod";

const LonLat = z.tuple([z.number(), z.number()]);
// ISO calendar date, "1950-06-25". Years 1..9999 (proleptic Gregorian).
const IsoDate = z.string().regex(/^\d{1,4}-\d{2}-\d{2}$/, "expected YYYY-MM-DD");
const Geometry = z.object({
  type: z.enum(["Polygon", "MultiPolygon"]),
  coordinates: z.array(z.any()),
});

export const FactionSchema = z.object({
  id: z.string(),
  name: z.string(),
  color: z.string(), // territory wash
  ink: z.string().optional(), // markers and text; defaults to a darkened color
  marker: z.enum(["square", "circle", "diamond", "triangle", "banner"]).default("square"),
  // Unit markers as national flags (sprites drawn in src/lib/flags.ts), mixed by weight and limited to the dates
  // each contingent was in the field. When set, these replace the plain marker shape.
  flags: z
    .array(
      z.object({
        flag: z.string(),
        weight: z.number().default(1),
        from: IsoDate.optional(),
        to: IsoDate.optional(),
        region: z.tuple([LonLat, LonLat]).optional(), // only units inside this [[west, south], [east, north]] box
      }),
    )
    .default([]),
});

export const VideoSchema = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/),
  fps: z.number().int().default(30),
  width: z.number().int().default(1920),
  height: z.number().int().default(1080),
  // Marks data that has not been fact-checked; rendered as a visible banner so it can never ship by accident.
  draft: z.boolean().default(false),
  style: z.enum(["atlas", "warroom"]).default("atlas"),
  // "sidebar": 1440 px map + 480 px dashboard (long-form). "full": full-frame map with a HUD (battle format).
  // "short": 1080x1920 vertical, generated automatically from any video by toShort() (src/short.ts).
  layout: z.enum(["sidebar", "full", "short"]).default("sidebar"),
  // Tuning for the generated Short.
  short: z
    .object({ seconds: z.number().default(45), zoom: z.number().default(1.25), title: z.string().optional() })
    .default({ seconds: 45, zoom: 1.25 }),

  header: z.object({
    title: z.string(),
    subtitle: z.string(),
    hook: z.string().optional(), // one line shown over the cold open
    introClip: z.string().optional(), // pre-rendered clip in public/ (e.g. a Blender globe shot) played over the intro
    // Cold open on a turning globe: spins from `from` to `to` (lon, lat), optionally showing the territory of
    // `showDate` (e.g. the empire at its peak, as a teaser), then dissolves into the flat map.
    globe: z.object({ from: LonLat, to: LonLat, showDate: IsoDate.optional() }).optional(),
    footnote: z.string().default(""), // small print in the sidebar, e.g. "Borders approximate"
    outro: z.string().default(""), // closing line on the end card (the last outroSeconds, under YouTube's end screen)
    watermark: z.string().default(""),
  }),

  map: z.object({
    projection: z.enum(["conicEqualArea", "mercator", "equirectangular"]).default("conicEqualArea"),
    parallels: z.tuple([z.number(), z.number()]).optional(),
    bounds: z.tuple([LonLat, LonLat]), // [[west, south], [east, north]] framed at zoom 1
    resolutionScale: z.number().min(0.5).max(3).default(1.25), // map raster size relative to the viewport
    landDetail: z.enum(["10m", "50m"]).default("10m"),
    // Countries (Natural Earth names) where territory is painted; other land is drawn as neutral. Empty = all.
    theatre: z.array(z.string()).default([]),
    markers: z.boolean().default(true), // unit markers
    // "line": units crowd every front (wars). "advancing": only where a border is moving (empires on campaign).
    markerFront: z.enum(["line", "advancing"]).default("line"),
    markerDensity: z.number().min(0).max(1).default(0.3), // share of interior positions that show a unit
    flagShape: z.enum(["rect", "round"]).default("rect"),
    markerSpacing: z.tuple([z.number(), z.number()]).default([24, 9]), // interior grid, front grid (px at zoom 1)
    relief: z.boolean().default(false), // hillshaded terrain; needs `node scripts/fetch-terrain.mjs <id>` first
    reliefStrength: z.number().default(1),
    rivers: z.boolean().default(false), // Natural Earth rivers and lakes
    // Which modern borders to draw: inside the theatre they are usually anachronistic.
    borders: z.enum(["outsideTheatre", "all", "none"]).default("outsideTheatre"),
    edgeGlow: z.boolean().default(true), // glow where a faction borders unclaimed land (an empire's frontier)
    labels: z
      .array(
        z.object({
          text: z.string(),
          at: LonLat,
          kind: z.enum(["country", "city", "sea", "region"]).default("country"),
          size: z.number().optional(),
          from: IsoDate.optional(), // shown only while the place/state existed under this name
          to: IsoDate.optional(),
        }),
      )
      .default([]),
  }),

  factions: z.array(FactionSchema).min(1),

  // Territory keyframes. Each keyframe paints layers in order; a later layer takes the pixels it covers away
  // from every other faction (so enclaves and pockets are just a small layer at the end). Shapes may spill over
  // the sea and outside the theatre: they are clipped at render time, so only the front lines need care.
  // Between keyframes the borders morph by signed-distance interpolation.
  territories: z
    .array(
      z.object({
        date: IsoDate,
        layers: z.array(
          z
            .object({
              faction: z.string(),
              everywhere: z.boolean().optional(),
              countries: z.array(z.string()).optional(), // Natural Earth names, e.g. "South Korea"
              geometry: Geometry.optional(),
              // Everything on one side of a front line. For north/south the line runs west -> east and must not
              // double back in longitude; for east/west it runs south -> north. Ends extend to the map edge.
              beyond: z.object({ side: z.enum(["north", "south", "east", "west"]), line: z.array(LonLat).min(2) }).optional(),
            })
            .refine((l) => [l.everywhere, l.countries, l.geometry, l.beyond].filter(Boolean).length === 1, {
              message: "a layer needs exactly one of everywhere / countries / geometry / beyond",
            }),
        ),
        note: z.string().optional(), // source / reasoning, for the fact-check pass
        cut: z.boolean().default(false), // switch to this keyframe instantly instead of morphing (e.g. a recolour)
      }),
    )
    .min(1),

  timeline: z.object({
    start: IsoDate,
    end: IsoDate,
    clock: z.enum(["day", "year"]).default("day"), // "year" for empires: shows the year only, counts years
    introSeconds: z.number().default(3),
    outroSeconds: z.number().default(8),
    daysPerSecond: z.number().positive(),
    // Override the pace for stretches of the story (slow down for the decisive days, fast-forward stalemates).
    pace: z.array(z.object({ from: IsoDate, to: IsoDate, daysPerSecond: z.number().positive() })).default([]),
  }),

  camera: z
    .array(z.object({ date: IsoDate, center: LonLat, zoom: z.number().min(1).max(4).default(1) }))
    .default([]),

  events: z
    .array(
      z.object({
        date: IsoDate,
        title: z.string(),
        text: z.string().default(""),
        at: LonLat.optional(),
        holdSeconds: z.number().default(0), // freeze the clock on this day while the caption reads
        captionSeconds: z.number().default(4),
        chapter: z.boolean().default(false), // becomes a YouTube chapter in the generated description
        sfx: z.string().optional(), // file in public/, e.g. "sfx/stamp.wav"
        source: z.string().optional(), // citation for the fact-check pass (not rendered)
      }),
    )
    .default([]),

  // Offensive arrows: grow along `path` from `from` to `to`, then fade out.
  arrows: z
    .array(
      z.object({
        faction: z.string(),
        from: IsoDate,
        to: IsoDate,
        path: z.array(LonLat).min(2),
        width: z.number().default(1),
        color: z.string().optional(), // defaults to the faction colour, lightened
      }),
    )
    .default([]),

  // Army strength shown on the map: a flag badge and a big number that changes over time.
  forces: z
    .array(
      z.object({
        factionId: z.string(),
        flag: z.string().optional(),
        at: LonLat,
        moves: z.array(z.tuple([IsoDate, LonLat])).default([]), // optional dated positions, so it follows the camera
        label: z.string(),
        points: z.array(z.tuple([IsoDate, z.number()])).min(1),
        from: IsoDate.optional(),
        to: IsoDate.optional(),
      }),
    )
    .default([]),

  counters: z
    .array(
      z.discriminatedUnion("kind", [
        // A losses table: one row per side, one column per measure (e.g. killed, wounded, captured).
        z.object({
          kind: z.literal("table"),
          label: z.string(),
          columns: z.array(z.string()),
          rows: z.array(
            z.object({
              factionId: z.string(),
              flag: z.string().optional(),
              series: z.array(z.array(z.tuple([IsoDate, z.number()])).min(1).nullable()), // null: no figure ("—")
            }),
          ),
          source: z.string().optional(),
        }),
        // Area held, measured from the rendered territory (equal-area projection recommended).
        // "share" compares the sides (wars); "total" shows the combined area and its share of the world's land
        // outside Antarctica (empires).
        z.object({ kind: z.literal("area"), label: z.string().default("Territory held"), mode: z.enum(["share", "total"]).default("share") }),
        // Any sourced number that changes over time, e.g. casualties; linearly interpolated between points.
        z.object({
          kind: z.literal("series"),
          label: z.string(),
          rows: z.array(
            z.object({ factionId: z.string(), points: z.array(z.tuple([IsoDate, z.number()])).min(1) }),
          ),
          source: z.string().optional(),
        }),
      ]),
    )
    .default([{ kind: "area", label: "Territory held", mode: "share" }]),

  leaders: z
    .array(
      z.object({
        factionId: z.string(),
        name: z.string(),
        role: z.string().default(""),
        image: z.string().optional(), // file in public/, public-domain portrait
        from: IsoDate.optional(),
        to: IsoDate.optional(),
      }),
    )
    .default([]),

  audio: z
    .object({
      music: z
        .array(z.object({ src: z.string(), volume: z.number().default(0.6), startFrom: z.number().default(0) }))
        .default([]),
      voiceover: z.string().optional(), // optional narration file; music ducks under it
      eventSfxVolume: z.number().default(0.5),
    })
    .default({ music: [], eventSfxVolume: 0.5 }),

  // Everything the upload needs; scripts/render.mjs writes description.txt from it plus the chapters.
  youtube: z
    .object({
      title: z.string().default(""),
      summary: z.string().default(""),
      sources: z.array(z.string()).default([]),
      credits: z.array(z.string()).default([]), // music credits exactly as the licence requires
      tags: z.array(z.string()).default([]),
    })
    .default({ title: "", summary: "", sources: [], credits: [], tags: [] }),

  thumbnail: z
    .object({
      date: IsoDate.optional(), // map state to show; defaults to the most dramatic keyframe you pick
      text: z.string().default(""), // 0-4 words
      textAt: z.enum(["top-left", "bottom-left", "top-right", "bottom-right"]).default("top-left"), // keep it off the subject
      highlight: LonLat.optional(), // ring around the one place the eye should land
      zoom: z.number().optional(),
      center: LonLat.optional(),
    })
    .default({ text: "", textAt: "top-left" }),
});

export type Video = z.infer<typeof VideoSchema>;
export type VideoInput = z.input<typeof VideoSchema>;
export type Faction = z.infer<typeof FactionSchema>;
