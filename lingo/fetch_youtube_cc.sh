#!/bin/bash
# Run on the owner's PC (YouTube blocks the cloud session). Needs yt-dlp and ffmpeg.
# If YouTube says "confirm you're not a bot", run: bash lingo/fetch_youtube_cc.sh chrome
# (yt-dlp then uses your signed-in Chrome session on this PC; nothing leaves your machine).
# Downloads the audio of the Creative Commons (CC BY) videos listed in ideas/japanese_understand_sources.md.
cd "$(dirname "$0")" && mkdir -p incoming/japanese
EXTRA=(); [ -n "$1" ] && EXTRA=(--cookies-from-browser "$1")
for id in 4P-XZqNJ6-E _Q84WXzvb7M 840bjqOZfFc hK71csogWT0 yG4RSssIpPU 51eRKMkHWBA Roi-Csw7RPc mIEtnvlQXLE 0e5VM1fg7Do stnXsGsDAhY EhVFv_eW_f4 LYwF_BeUHBM; do
  yt-dlp "${EXTRA[@]}" -f bestaudio -x --audio-format opus --audio-quality 64K --write-info-json -o "incoming/japanese/%(id)s.%(ext)s" "https://www.youtube.com/watch?v=$id"
done
ls -la incoming/japanese
