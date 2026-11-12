#!/usr/bin/env bash
# Resumable long render: renders the video muted in chunks to out/parts-<id>/ (skipping finished chunks), then joins them
# and muxes public/generated/<id>/mix.wav. Survives a container restart: run it again and it continues.
# Usage: bash scripts/render_chunks.sh <Comp> <spec-id> <out.mp4> <total-frames> [chunk] [extra remotion args]
set -u
comp=$1; id=$2; out=$3; total=$4; chunk=${5:-1500}; shift 5 2>/dev/null || shift $#
parts=out/parts-$id; mkdir -p "$parts" _parked
for d in public/generated/*/; do n=$(basename "$d"); [ "$n" != "$id" ] && mv "$d" _parked/; done
trap 'for d in _parked/*/; do [ -d "$d" ] && mv "$d" public/generated/; done; rmdir _parked 2>/dev/null' EXIT
rm -f "$parts/list.tmp"; i=0
for ((s=0; s<total; s+=chunk)); do
  e=$((s+chunk-1)); [ $e -ge $total ] && e=$((total-1))
  f=$(printf "%s/%03d.mp4" "$parts" $i)
  if [ ! -s "$f.done" ]; then
    echo "chunk $i: frames $s-$e"
    npx remotion render "$comp" "$f" --props="data/$id.json" --frames=$s-$e --muted "$@" 2>&1 | tr '\r' '\n' | grep -E "Error|error" | head -3
    [ -s "$f" ] && echo ok > "$f.done" || { echo "chunk $i failed"; exit 1; }
  fi
  echo "file '$(basename "$f")'" >> "$parts/list.tmp"; i=$((i+1))
done
mv "$parts/list.tmp" "$parts/list.txt"
ffmpeg -y -loglevel error -f concat -safe 0 -i "$parts/list.txt" -i "public/generated/$id/mix.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart "$out" && echo "DONE $out"
