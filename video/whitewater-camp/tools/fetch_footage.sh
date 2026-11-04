#!/bin/bash
# Archive films for "whitewater-camp" (all public domain / CC0, via the Internet Archive). Run from the episode folder.
cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out $(stat -c %s "$out")"; done <<'LIST'
TroopTra1943|TroopTra1943_512kb.mp4|troop_train_1943.mp4
FB-164|FB-164 Controlling German Prisoners Of War c1944.mp4|controlling_german_pows_1944.mp4
WoodForW1942|WoodForW1942_512kb.mp4|wood_for_war_1942.mp4
gov.archives.arc.13585|gov.archives.arc.13585_512kb.mp4|stump_to_ship_1930.mp4
ADC-140|111-adc-140 British In Middle East WWII - German Prisoners Shipped To US North Africa - Chinese Air Corps Graduation USA.mp4|prisoners_shipped_adc140.mp4
fc-fc-1163|fc-fc-1163.mp4|scout_canoes_1937.mp4
0787_Little_Smokey_The_True_Story_of_Americas_Forest_Fire_Preventin_01_46_27_00|0787_Little_Smokey_The_True_Story_of_Americas_Forest_Fire_Preventin_01_46_27_00.mp4|little_smokey_bear.mp4
Children1940|Children1940_512kb.mp4|children_must_learn_1940.mp4
gov.archives.arc.38686|gov.archives.arc.38686_512kb.mp4|women_in_defense_1941.mp4
gov.fdr.352.2a.3|gov.fdr.352.2a.3_512kb.mp4|power_and_the_land_1940.mp4
0561_When_Work_Is_Done_12_51_43_00|0561_When_Work_Is_Done_12_51_43_00.mp4|when_work_is_done_1943.mp4
WinterSportsInWhiteMountains|33.528WinterSportsInTheWhiteMountainNationalForest.mp4|winter_white_mountains_1934.mp4
LIST
