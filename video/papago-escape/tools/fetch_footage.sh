#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~0.9 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOF'
TF1-3346|TF 1-3346 Land and Live in the Desert 1945.mp4|land_and_live_desert_1944.mp4
70-328|70-328.mp4|arizona_1940.mp4
NPC-15652|NPC-15652.mp4|u858_surrender_1945.mp4
NPC-9052|428-npc-9052 Now it can be told (MN-5883) ca 06-1944.mp4|u505_capture_1944.mp4
NPC-1209|NPC-1209.mp4|uboat_survivors_1943.mp4
1945-12-10_Christmas_Brings_Joy_To_Everyone|1945-12-10_Christmas_Brings_Joy_To_Everyone_512kb.mp4|christmas_1945.mp4
EOF
