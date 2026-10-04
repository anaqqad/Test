// House style "Darkroom & Ledger" — see HOUSE_STYLE.md at the repo root.
// Photos live on a light table as frames of a black 35 mm strip, marked up in grease pencil.
// Data and documents live on field-ledger graph paper, marked up in the same grease pencil.
import "@fontsource/barlow-condensed/500.css";
import "@fontsource/barlow-condensed/700.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import "@fontsource/ibm-plex-serif/400.css";
import "@fontsource/ibm-plex-serif/400-italic.css";

export const C = {
  table: "#121212", // light table, switched off
  tableGlow: "#202020",
  rebate: "#050505", // film border
  edge: "#8a7a58", // edge print on film
  paper: "#f1eee6", // ledger paper
  gridMinor: "#d5dcd7",
  gridMajor: "#b4c3bc",
  ink: "#171717",
  inkSoft: "#5f5b54",
  grease: "#e0442e", // grease pencil: the only accent colour
  light: "#ece9e1", // text on dark
  lightSoft: "#9a968e",
};

export const HEAD = "'Barlow Condensed', 'Arial Narrow', sans-serif"; // headlines, figures: uppercase
export const MONO = "'IBM Plex Mono', 'DejaVu Sans Mono', monospace"; // dates, sources, labels
export const QUOTE = "'IBM Plex Serif', Georgia, serif"; // quoted words only

export const FADE = 9;
