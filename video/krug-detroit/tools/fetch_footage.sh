#!/bin/bash
# Archive films for "krug-detroit" (all public domain / CC0, via the Internet Archive). Run from the episode folder.
cd "$(dirname "$0")/../assets/footage"
while IFS="|" read id f out; do [ -s "$out" ] || curl -sL --retry 3 -o "$out" "https://archive.org/download/$id/$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$f")"; echo "$out $(stat -c %s "$out")"; done <<'LIST'
wwf_the_battle_of_britain|the_battle_of_britain_512kb.mp4|battle_of_britain_1943.mp4
MyDadsCo1946|MyDadsCo1946_512kb.mp4|detroit_edison_1946.mp4
Behindth1935|Behindth1935_512kb.mp4|bright_lights_1935.mp4
BusDrive1946|BusDrive1946_512kb.mp4|bus_driver_1946.mp4
BoyinCou1940|BoyinCou1940_512kb.mp4|boy_in_court_1940.mp4
gov.fdr.273|gov.fdr.273_512kb.mp4|presidents_tour_1942.mp4
gov.archives.arc.93713|gov.archives.arc.93713_512kb.mp4|rouge_plant_1939.mp4
TroopTra1943|TroopTra1943_512kb.mp4|troop_train_1943.mp4
FB-164|FB-164 Controlling German Prisoners Of War c1944.mp4|controlling_german_pows_1944.mp4
LIST
