#!/bin/bash
# Downloads the public-domain footage listed in research/footage_credits.md into assets/footage/.
set -e; cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out"; done <<'EOF'
FB-164|FB-164 Controlling German Prisoners Of War c1944.mp4|pow_control_1944.mp4
0994_Chicago_01_45_18_18|0994_Chicago_01_45_18_18_3mb.mp4|chicago_1936.mp4
Behindth1935|Behindth1935.mp4|bright_lights_1935.mp4
FreedomH1956|FreedomH1956.mp4|freedom_highway_1956.mp4
TroopTra1943|TroopTra1943.mp4|troop_train_1943.mp4
NPC-4386|NPC-4386.mp4|newport_news_1943.mp4
gov.archives.arc.38972|gov.archives.arc.38972_512kb.mp4|hamburg_bombed_1943.mp4
NPC-1533a|NPC-1533a.mp4|pows_naples_1943.mp4
1945-05-08_Germany_Gives_Up|1945-05-08_Germany_Gives_Up.mp4|germany_gives_up_1945.mp4
x_marks_the_spot|x_marks_the_spot.mp4|x_marks_the_spot_1942.mp4
gov.archives.arc.44362|gov.archives.arc.44362_512kb.mp4|wochenschau_1943.mp4
American1955|American1955.mp4|american_harvest_1955.mp4
AndSoTheyLive|And_So_They_Live.mp4|and_so_they_live_1940.mp4
news_parade_of_1945|news_parade_of_1945.mp4|news_parade_1945.mp4
gov.archives.arc.38967|gov.archives.arc.38967_512kb.mp4|sicily_invasion_1943.mp4
battle_of_san_pietro|battle_of_san_pietro_512kb.mp4|san_pietro_1945.mp4
LondonCanTakeIt|london_can_take_it_512kb.mp4|london_can_take_it_1940.mp4
wwf_the_battle_of_russia_pt1|the_battle_of_russia_pt1_512kb.mp4|battle_of_russia_1943.mp4
NPC-16081|NPC-16081.mp4|atlantic_convoy_1942.mp4
CityTheP1939|CityTheP1939.mp4|the_city_1939.mp4
GoldenHa1950|GoldenHa1950.mp4|cannery_calpak_1950.mp4
Arteries1941|Arteries1941.mp4|arteries_nyc_1941.mp4
Tuesdayi1945|Tuesdayi1945.mp4|tuesday_in_november_1945.mp4
NewsOfTheDay1943|NewsOfTheDay1943.mp4|news_of_the_day_1943.mp4
EOF
