#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~1.1 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOF'
NPC-744|NPC-744.mp4|pows_noumea_1943.mp4
NPC-740|NPC-740.mp4|pows_noumea_b_1943.mp4
NPC-8680|NPC-8680.mp4|iwo_nisei_prisoners_1945.mp4
NPC-4511|NPC-4511.mp4|saipan_prisoners_1944.mp4
KnowYourEnemyJapan|KnowYourEnemyJapan.mp4|know_your_enemy_japan.mp4
December7th|December7th_512kb.mp4|december_7th.mp4
September21945Newsreel-JapaneseSurrenderSigningOnMissouri|September21945Newsreel-JapaneseSurrenderSigningOnMissouri.mp4|surrender_1945.mp4
passenger_train|passenger_train_512kb.mp4|passenger_train_1940.mp4
428-npc-22250|428-npc-22250.mp4|golden_gate_aerials_1945.mp4
EOF
