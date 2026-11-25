#!/usr/bin/env bash
# Render 3D shots to assets/footage/r3d_<shot>.mp4 (30 fps). Encodes only when Blender quits cleanly.
# bash tools/render3d.sh "s_zero s_camp_day ..."   (stills: STILLS=1,120,300 bash tools/render3d.sh "s_zero")
cd "$(dirname "$0")/.."
B="C:/Users/anass/AppData/Local/Programs/blender-4.2.23-windows-x64/blender.exe"
for s in $1; do
  out="$(pwd -W)/build/r3d/$s"; mkdir -p "$out"
  if [ -n "$STILLS" ]; then "$B" -b -P tools/blender/scene.py -- "$out" "$s" "stills:$STILLS" > "$out/log.txt" 2>&1; echo "$s stills"; continue; fi
  [ -f "assets/footage/r3d_$s.mp4" ] && { echo "$s exists"; continue; }
  rm -f "$out"/f_*.jpg
  "$B" -b -P tools/blender/scene.py -- "$out" "$s" anim > "$out/log.txt" 2>&1
  if grep -q "Blender quit" "$out/log.txt"; then
    ffmpeg -y -loglevel error -framerate 30 -i "$out/f_%04d.jpg" -c:v libx264 -crf 16 -pix_fmt yuv420p "assets/footage/r3d_$s.mp4" && rm -f "$out"/f_*.jpg
    echo "$s done"
  else echo "$s FAILED"; tail -5 "$out/log.txt"; fi
done
