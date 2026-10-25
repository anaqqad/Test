import { continueRender, delayRender, staticFile } from "remotion";

const faces: [string, string, string][] = [
  ["Cinzel", "fonts/Cinzel.ttf", "700"],
  ["Barlow Condensed", "fonts/barlow-condensed-latin-500-normal.woff2", "500"],
  ["Barlow Condensed", "fonts/barlow-condensed-latin-700-normal.woff2", "700"],
];

let loaded: Promise<void> | null = null;

export function loadFonts(): Promise<void> {
  if (!loaded) {
    const handle = delayRender("fonts");
    loaded = Promise.all(
      faces.map(async ([family, file, weight]) => {
        const face = new FontFace(family, `url(${staticFile(file)})`, { weight });
        await face.load();
        document.fonts.add(face);
      }),
    ).then(() => continueRender(handle));
  }
  return loaded;
}
