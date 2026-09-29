# Blender shots

Blender is used for the few "wow" shots per video that SVG/Remotion can't do well (3D globes, camera flights,
physics). Each shot is a Python script: no clicking, it renders headless on the VPS, and the MP4 is dropped
into a video timeline like any other clip.

## Install on the VPS (5-15 min)
    sudo bash blender/install_vps.sh

Needs ~1.5 GB disk, 4 GB+ RAM. No graphics card needed (EEVEE runs on the CPU through Mesa; `libegl1` is
required, without it EEVEE/Workbench abort).

## globe_mongols.py: the Mongol Empire spreading across a 3D globe (8 s, 1080p, 24 fps)
    blender -b --factory-startup -P blender/globe_mongols.py -- --preview --still 1,60,120,190   # 4 check frames
    blender -b --factory-startup -P blender/globe_mongols.py                                     # full shot -> blender/out/

- Globe turns from Europe to Asia while the camera zooms in; the empire spreads outward from Karakorum
  with a gold front line; the year counts 1206 -> 1279; title and year fade in.
- Map: real coastlines (Natural Earth via world-atlas) drawn into an equirectangular texture;
  the globe shader maps it with atan2/asin, so no UV unwrapping is needed.
- Measured on a 4-core cloud VM without GPU (Cycles, 8 samples): ~20 s per 1080p frame; a 3090-class GPU renders it in well under a second per frame.

## Another empire / country
Edit the `ring` (lon, lat outline) in `globe_tex.mjs`, regenerate the textures
(`npm i d3-geo topojson-client`, world-atlas `countries-50m.json`, headless Chrome screenshot of the two
HTML files at 4096x2048), then change `KARAKORUM` (the starting point), the years and the camera keys in
`globe_mongols.py`.

## Fonts
`assets/Cinzel.ttf` is Cinzel Bold (SIL Open Font License) with overlapping contours removed: Blender's
text fill drops letters on fonts with overlaps (variable-font exports), so always run
`fontTools.ttLib.removeOverlaps` on a new font first.
