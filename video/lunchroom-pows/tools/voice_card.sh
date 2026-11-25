#!/bin/bash
# voice_card.sh <in.mp3> <start> <dur> <out.mp4> "<line1>" "<line2>": waveform card for an audio-only archive recording
in=$1; ss=$2; d=$3; out=$4; l1=$5; l2=$6
F=/c/Windows/Fonts
ffmpeg -v error -y -ss $ss -t $d -i "$in" -f lavfi -i "color=c=0x121110:s=1280x720:r=30:d=$d" -filter_complex \
"[0:a]aformat=channel_layouts=mono,showwaves=s=1000x220:mode=cline:draw=full:colors=0xE0442E:scale=sqrt:r=30[w];\
[1:v][w]overlay=140:250,drawtext=fontfile='C\:/Windows/Fonts/georgia.ttf':text='$l1':fontcolor=0xECE9E1:fontsize=42:x=(w-tw)/2:y=120,\
drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':text='$l2':fontcolor=0x9A958C:fontsize=20:x=(w-tw)/2:y=560[v]" \
-map "[v]" -map 0:a -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest "$out"
