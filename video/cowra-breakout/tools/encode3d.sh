#!/usr/bin/env bash
# Encode finished Blender frame folders (build/r3d/<shot>/<shot>/f_####.jpg) to assets/footage/r3d_<shot>.mp4.
cd "$(dirname "$0")/.."
for s in "$@"; do
  d="build/r3d/$s/$s"; n=$(ls "$d"/f_*.jpg 2>/dev/null | wc -l)
  grep -q "Blender quit" "build/r3d/$s/log.txt" || { echo "$s not finished ($n frames)"; continue; }
  ffmpeg -y -loglevel error -framerate 30 -i "$d/f_%04d.jpg" -c:v libx264 -crf 16 -pix_fmt yuv420p "assets/footage/r3d_$s.mp4" && rm -rf "$d" && echo "$s encoded ($n frames)"
done
