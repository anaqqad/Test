#!/usr/bin/env bash
# Keep the original video up to 27.667 s, put the new ending clip after it, and keep the ORIGINAL audio
# for the whole 30 s (same voices, same "No kid of mine sleeps in a car" line).
# Usage: bash splice.sh ltx_ending.mp4   (or a MiniMax/Hailuo clip made from start_frame.png)
set -e
NEW="${1:-ltx_ending.mp4}"
ffmpeg -y -i the_car_original.mp4 -i "$NEW" -filter_complex \
 "[0:v]trim=0:27.667,setpts=PTS-STARTPTS[a];\
  [1:v]scale=480:-2,crop=480:854,setsar=1,fps=24,trim=0:2.413,setpts=PTS-STARTPTS[b];\
  [a][b]concat=n=2:v=1:a=0[v]" \
 -map "[v]" -map 0:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t 30.08 the_car_fixed.mp4
echo "wrote the_car_fixed.mp4"
