// Visual styles. "atlas": engraved parchment (Borderclock). "warroom": dark campaign map with terrain relief
// (the battle format). Components read the mutable `theme`; applyTheme() switches it before a video renders.
const atlas = {
  paper: "#efe3c4",
  paperDim: "#d9cfb6", // land outside the theatre
  sea: "#b8cbc3",
  ink: "#33281c",
  labelInk: "#33281c",
  labelHalo: "rgba(239,227,196,0.85)",
  river: "#7f9fa6",
  front: "#f3b43c", // the burning front line
  accent: "#b8322a",
  panel: "#1d1914",
  panelText: "#f1e6cc",
  muted: "#a99a7c",
  washMode: "multiply" as GlobalCompositeOperation,
  washAlpha: 0.78,
  ripples: true, // engraved coastline ripples on the sea
  grain: 10,
  coastAlpha: 0.85,
  display: "Cinzel", // titles, dates, labels
  number: "Barlow Condensed", // counters and captions
};

const warroom: typeof atlas = {
  ...atlas,
  paper: "#3a3f45",
  paperDim: "#2c3035",
  sea: "#1b2631",
  ink: "#0e1114",
  labelInk: "#eef1f3",
  labelHalo: "rgba(14,17,20,0.85)",
  river: "#4f7b9a",
  front: "#ffd27a",
  accent: "#e0533f",
  panel: "#12161a",
  panelText: "#eef1f3",
  muted: "#8d969e",
  washMode: "source-over",
  washAlpha: 0.86,
  ripples: false,
  grain: 6,
  coastAlpha: 0.9,
};

export const themes = { atlas, warroom };
export type ThemeName = keyof typeof themes;
export const theme = { ...atlas };

export function applyTheme(name: ThemeName) {
  Object.assign(theme, themes[name]);
}
