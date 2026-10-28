#!/bin/bash
# Renders overlay cards that are missing or unreadable, retrying while the drive is nearly full
# (on this PC free space swings by gigabytes as Windows grows the page file).
cd "$(dirname "$0")/../remotion"
for attempt in $(seq 1 30); do
  ids=$(python -c "
import json, subprocess, os
o = json.load(open('../build/storyboard.json', encoding='utf-8'))['overlays']
bad = []
for c in o:
    f = f'../build/overlays/{c[\"id\"]}.webm'
    ok = os.path.exists(f) and subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip() not in ('', 'N/A')
    if not ok:
        bad.append(c['id'])
        if os.path.exists(f): os.remove(f)
print(' '.join(bad))")
  [ -z "$ids" ] && { echo ALLDONE; exit 0; }
  free=$(df -m /c | awk 'NR==2{print $4}')
  if [ "$free" -lt 300 ]; then echo "attempt $attempt: only ${free} MB free, waiting"; sleep 60; continue; fi
  echo "attempt $attempt: $(echo $ids | wc -w) cards to render (${free} MB free)"
  node render.mjs $ids 2>&1 | grep -E "frames [0-9]+s$|No space" | tail -3
done
echo GAVEUP
