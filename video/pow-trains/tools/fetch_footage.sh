#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~0.45 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOT'
TroopTra1943|TroopTra1943_512kb.mp4|troop_train_1943.mp4
ThisIsMy1940|ThisIsMy1940_512kb.mp4|this_is_my_railroad_1940.mp4
0734_Passenger_Train_The_03_48_41_00|0734_Passenger_Train_The_03_48_41_00.mp4|passenger_train_1940.mp4
GreatRai1942|GreatRai1942_512kb.mp4|great_railroad_1942.mp4
FB-164|FB-164 Controlling German Prisoners Of War c1944.mp4|controlling_german_pows_1944.mp4
gov.archives.arc.23655|gov.archives.arc.23655_512kb.mp4|tunisian_campaign_1943.mp4
EOT
