# Test repo: Blender shots for history documentaries

Handover from a cloud Claude Code session (no GPU) to a local session on the owner's PC (RTX 3090 Ti, 24 GB).

## What this is
- `blender/globe_mongols.py`: 8-second 1080p/24 fps shot, fully scripted (no clicking): a 3D globe turns from
  Europe to Asia, the camera zooms in, the Mongol Empire spreads in red from Karakorum with a gold front line,
  the year counts 1206 -> 1279, titles in Cinzel.
- `blender/assets/`: map texture (real coastlines, Natural Earth via world-atlas), empire mask, Cinzel Bold
  with overlapping contours removed (Blender's text fill drops letters on fonts with overlaps).
- `blender/globe_tex.mjs`: regenerates the textures for another empire (edit `ring`).
- `blender/install_vps.sh`: Ubuntu/Debian install of Blender 4.2 LTS + Rhubarb Lip Sync.

## Running on this PC (Windows)
1. Install Blender 4.2 LTS from blender.org and make sure `blender` is on PATH (or use the full path to
   `blender.exe`). Update the NVIDIA driver; `nvidia-smi` must show the card.
2. Check frames first, then the full shot:
       blender -b --factory-startup -P blender/globe_mongols.py -- --gpu --preview --still 1,60,120,190
       blender -b --factory-startup -P blender/globe_mongols.py -- --gpu
   Output: `blender/out/` (PNG stills, MP4). The script prints "GPU devices: [...]"; if the list is empty,
   OptiX isn't available (driver) and it renders on the CPU.
3. Options: `--engine CYCLES|EEVEE` (default CYCLES), `--samples N` (default 8; the scene is unlit, so
   samples only anti-alias edges), `--frames 1-192`, `--out file.mp4`.

## Measured
- Cloud VM, 4 CPU cores, no GPU: EEVEE ~42 s/frame (software OpenGL), Cycles ~1.1 s per sample per 1080p
  frame (8 samples ~20 s/frame). EEVEE/Workbench on Linux without a GPU need `libegl1` or Blender aborts.
- A 3090 Ti should be far faster; measure and note it here.

## Next ideas (not started)
- Photoreal Earth from space (NASA Blue Marble + clouds + night lights), real-terrain flyovers from
  elevation data, museum-style artefact close-ups, smoke/fire, collapsing walls.

## Rules from the owner
- Commit Blender work to this repo (anaqqad/Test), not to the-ink-effect.
- Never print, log or commit API keys; secrets come from environment variables.
- Ask before any paid API usage.
- Don't touch unrelated projects or folders on this machine.

## Reels for The Black History Room (added 2026-10-03)
- Vertical 1080x1920 Remotion format at the repo root; see README.md. Pilot: `data/reel-robert-smalls.json`.
- Pipeline copied from anaqqad/Youtube-Automation (MathDoc), same file names. The owner chose to keep it here.
- ElevenLabs "Andrew" is paid: ask before every `tts_mathdoc.py` run on an elevenlabs spec, and give the
  character count (pilot: ~910 characters). Kokoro scratch takes are free.
- Never commit `voices/`. Images: public domain / CC0 only, credits in `public/pd/<id>/credits.json`.
- Measured on the cloud VM (4 CPU, no GPU): Reel render 212 s for 62.6 s of video; safe-zone QC ~70 s.
