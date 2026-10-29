#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/ (~1 GB).
# No symlinks to other episodes: Git Bash on Windows copies instead of linking, so every film is fetched once here.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOT'
ThisIsMy1940|ThisIsMy1940_512kb.mp4|this_is_my_railroad_1940.mp4
ThisIsMy1940_2|ThisIsMy1940_2_512kb.mp4|this_is_my_railroad_1940_b.mp4
gov.dod.dimoc.29754|gov.dod.dimoc.29754_512kb.mp4|ski_safety_1942.mp4
gov.archives.arc.39099|gov.archives.arc.39099_512kb.mp4|ski_newsreel_1946.mp4
Summersc1941_2|Summersc1941_2_512kb.mp4|san_francisco_1941.mp4
70-328|70-328.mp4|arizona_1940.mp4
TF1-3346|TF 1-3346 Land and Live in the Desert 1945.mp4|land_and_live_desert_1944.mp4
gov.archives.arc.23655|gov.archives.arc.23655_512kb.mp4|tunisian_campaign_1943.mp4
EOT
