import { loadFont } from "@remotion/fonts";
import { Easing, interpolate, staticFile } from "remotion";

/** The Black History Room: black, cream and gold. */
const BHR = {
  black: "#0E0C0A",
  ink: "#1A1612",
  cream: "#F4EAD5",
  creamDim: "rgba(244,234,213,0.78)",
  gold: "#E2B24A",
  goldDeep: "#A97C22",
  paper: "#E9DCC0",
  paperInk: "#2A2119",
  water: "#231E17",
  land: "#C9B58E",
};

/** Boston Before Us: night navy, lamplight gold, cream (matches the page's banner and avatar). */
const BBU: typeof BHR = {
  black: "#0D1522",
  ink: "#16223A",
  cream: "#F2EBDD",
  creamDim: "rgba(242,235,221,0.78)",
  gold: "#D9A84E",
  goldDeep: "#A57A2B",
  paper: "#E6DCC6",
  paperInk: "#1E2533",
  water: "#18233A",
  land: "#BFB08F",
};

export const THEMES = { bhr: BHR, bbu: BBU } as const;
export type ThemeName = keyof typeof THEMES;

/**
 * Current palette. A render shows one page's reel, so Reel sets it once from spec.brand.theme
 * (applyTheme) before any block reads it.
 */
export const B: typeof BHR = { ...BHR };
export const applyTheme = (name: ThemeName = "bhr") => Object.assign(B, THEMES[name]);

/** Colour of the safe-zone QC mask (scripts/qc_reel.py looks for it). */
export const QC_MAGENTA = "#FF00FF";
/** Faces are masked in cyan: they must avoid the overlays too, but may be cropped by the frame edge. */
export const QC_CYAN = "#00FFFF";

loadFont({ family: "Playfair Display", url: staticFile("fonts/PlayfairDisplay-Variable.woff2"), weight: "400 900" });
loadFont({ family: "Playfair Display", url: staticFile("fonts/PlayfairDisplay-Italic-Variable.woff2"), weight: "400 900", style: "italic" });
loadFont({ family: "Inter", url: staticFile("fonts/Inter-Variable.woff2"), weight: "100 900" });

export const serif = "'Playfair Display', Georgia, serif";
export const sans = "'Inter', 'Helvetica Neue', Arial, sans-serif";

/** Archival photos: warm sepia so every source sits in the same palette. */
export const SEPIA = "sepia(0.62) saturate(0.95) contrast(1.06) brightness(0.93)";

/**
 * Facebook Reels covers the bottom 20 % (caption, music line) and the right 15 % (like, comment,
 * share buttons). Captions, text and faces stay inside SAFE; scripts/qc_reel.py measures it.
 */
export const SAFE = { left: 60, top: 150, right: 1080 * 0.85, bottom: 1920 * 0.8 } as const;
/** horizontal centre of the safe column */
export const SAFE_CX = (SAFE.left + SAFE.right) / 2;
export const SAFE_W = SAFE.right - SAFE.left;
/** Column centred on the frame that still stays inside SAFE (mirror of the right margin): for centred cards. */
export const CENTER_COL = { left: 1080 - SAFE.right, width: 1080 - 2 * (1080 - SAFE.right) } as const;

export const EASE_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const EASE_IN_OUT = Easing.bezier(0.65, 0, 0.35, 1);
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** 0 -> 1 over `dur` frames starting at `at`, eased. */
export const reveal = (frame: number, at: number, dur = 10) => interpolate(frame, [at, at + dur], [0, 1], { ...clamp, easing: EASE_OUT });
