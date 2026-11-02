#!/bin/bash
# Renders overlay cards that are missing or unreadable, retrying while the drive is nearly full
# (on this PC free space swings by gigabytes as Windows grows the page file).
cd "$(dirname "$0")/../remotion"
for attempt in $(seq 1 200); do
  ids=$(python -c "
import json, subprocess, os
o = json.load(open('../build/storyboard.json', encoding='utf-8'))['overlays']
bad = []
for c in o:
    f = f'../build/overlays/{c[\"id\"]}.webm'
    ok = os.path.exists(f) and subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout.strip() not in ('', 'N/A')
    if not ok:
        bad.append(c['id'])
        try:
            os.remove(f)
        except OSError:
            pass
print(' '.join(bad) or 'NONE')")
  [ "$ids" = NONE ] && { echo ALLDONE; exit 0; }
  [ -z "$ids" ] && { echo "check failed, retrying"; sleep 20; continue; }
  free=$(df -m /c | awk 'NR==2{print $4}')
  if [ "$free" -lt 300 ]; then echo "attempt $attempt: only ${free} MB free, waiting"; sleep 60; continue; fi
  echo "attempt $attempt: $(echo $ids | wc -w) cards to render (${free} MB free)"
  HEIGHT=${HEIGHT:-720} node render.mjs $ids 2>&1 | grep -E "frames [0-9]+s$|No space" | tail -3
done
echo GAVEUP
