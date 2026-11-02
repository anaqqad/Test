#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~0.75 GB).
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOT'
TroopTra1943|TroopTra1943_512kb.mp4|troop_train_1943.mp4
FB-164|FB-164 Controlling German Prisoners Of War c1944.mp4|controlling_german_pows_1944.mp4
gov.archives.arc.23655|gov.archives.arc.23655_512kb.mp4|tunisian_campaign_1943.mp4
ThePlowThatBrokeThePlains_201503|96.2 The Plow That Broke the Plains.mp4|plow_plains_1936.mp4
FoodforF1943|FoodforF1943.mp4|food_for_fighters_1943.mp4
EOT
