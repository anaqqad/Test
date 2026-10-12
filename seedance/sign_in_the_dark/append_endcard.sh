#!/usr/bin/env bash
# Usage: bash append_endcard.sh out.mp4 final.mp4   (adds the 3-second Kindle end card)
set -e
IN="${1:-out.mp4}"; OUT="${2:-final.mp4}"; DIR="$(cd "$(dirname "$0")" && pwd)"
ffmpeg -y -i "$IN" -i "$DIR/kindle_endcard.mp4" -filter_complex "[0:v]scale=480:854,setsar=1,fps=24[a];[1:v]scale=480:854,setsar=1,fps=24[b];[0:a]aresample=44100,aformat=channel_layouts=stereo[aa];[1:a]aresample=44100,aformat=channel_layouts=stereo[ba];[a][aa][b][ba]concat=n=2:v=1:a=1[v][au]" -map "[v]" -map "[au]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac "$OUT"
echo "wrote $OUT"
