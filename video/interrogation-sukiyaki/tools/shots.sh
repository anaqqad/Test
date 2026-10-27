#!/bin/bash
# Shot boundaries per film (scene score > 0.3 on a 6 fps, 160 px proxy) -> build/shots/<film>.txt
for f in assets/footage/*.mp4; do b=$(basename "$f" .mp4); [ -s build/shots/$b.txt ] && continue
nice -n 10 ffmpeg -v info -i "$f" -an -vf "fps=6,scale=160:-2,select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 > build/shots/$b.txt; done
echo SHOTSDONE
