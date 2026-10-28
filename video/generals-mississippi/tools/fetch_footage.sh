#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~0.65 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOF'
111-adc-2350|111-adc-2350.mp4|brest_surrender_1944.mp4
TunisianVictory1944|TunisianVictory1944.mp4|tunisian_victory_1944.mp4
gov.archives.arc.23655|gov.archives.arc.23655_512kb.mp4|tunisian_campaign_1943.mp4
ADC-2222|ADC-2222.mp4|paris_aug_1944.mp4
gov.fdr.352.2a.2|gov.fdr.352.2a.2_512kb.mp4|the_river_1938.mp4
passenger_train|passenger_train_512kb.mp4|passenger_train_1940.mp4
EOF
