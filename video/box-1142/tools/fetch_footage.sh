#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~0.5 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOT'
ADC-3883|ADC-3883.mp4|interrogation_florence_1945.mp4
ADC-4011|ADC-4011.mp4|interrogation_fifth_army_1945.mp4
ADC-4012|ADC-4012.mp4|interrogation_fifth_army_1945_b.mp4
RadioatW1944|RadioatW1944_512kb.mp4|radio_at_war_1944.mp4
SoundRec1943|SoundRec1943_512kb.mp4|sound_recording_1943.mp4
NPC-1212|NPC-1212.mp4|gripsholm_red_cross_1943.mp4
NPC-15652|NPC-15652.mp4|u858_surrender_1945.mp4
EOT
