#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/.
set -e; cd "$(dirname "$0")/../assets/footage"
# Shared films live in ../chicago-lights; fetch them there first (its tools/fetch_footage.sh), then link:
for f in troop_train_1943 and_so_they_live_1940 pow_control_1944 the_city_1939 american_harvest_1955 x_marks_the_spot_1942 tuesday_in_november_1945; do ln -sf ../../../chicago-lights/assets/footage/$f.mp4 $f.mp4; done
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOF'
NPC-744|NPC-744.mp4|pows_noumea_1943.mp4
NPC-740|NPC-740.mp4|pows_noumea_b_1943.mp4
NPC-8680|NPC-8680.mp4|iwo_nisei_prisoners_1945.mp4
NPC-4511|NPC-4511.mp4|saipan_prisoners_1944.mp4
KnowYourEnemyJapan|KnowYourEnemyJapan.mp4|know_your_enemy_japan.mp4
December7th|December7th_512kb.mp4|december_7th.mp4
NPC-15563|NPC-15563.mp4|midget_sub_1945.mp4
PlayInTheSno|PlayInTheSno.mp4|snow_1945.mp4
September21945Newsreel-JapaneseSurrenderSigningOnMissouri|September21945Newsreel-JapaneseSurrenderSigningOnMissouri.mp4|surrender_1945.mp4
passenger_train|passenger_train.mp4|passenger_train_1940.mp4
1944-06-30_Saipan_Is_Ours|1944-06-30_Saipan_Is_Ours.mp4|saipan_is_ours_1944.mp4
Challeng1944|Challeng1944.mp4|challenge_democracy_1944.mp4
EOF
