#!/usr/bin/env bash
# Render one Remotion composition with every other generated/<id> folder parked outside public/,
# so the bundle copy stays small on a nearly full disk. Usage: scripts/render_parked.sh <Comp> <spec-id> <out.mp4> [extra args]
set -u
comp=$1; id=$2; out=$3; shift 3
mkdir -p _parked
for d in public/generated/*/; do n=$(basename "$d"); [ "$n" != "$id" ] && mv "$d" _parked/; done
npx remotion render "$comp" "$out" --props="data/$id.json" "$@" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' | grep -v "^    at" | grep -v "404\|Failed to load" | tail -3
for d in _parked/*/; do mv "$d" public/generated/; done
rmdir _parked 2>/dev/null
ls -la "$out" 2>&1 | tail -1
