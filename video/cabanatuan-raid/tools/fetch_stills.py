"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    'AlamoScoutsRaidCabanatuanFeb1945.jpg': 'alamo_scouts_feb1945.jpg',
    'Cabanatuan Operations - Actions at the Objectives, January 1945.jpg': 'map_actions_objectives.jpg',
    'Cabanatuan Operations - Routes to and from the Objectives, January 1945.jpg': 'map_routes_objectives.jpg',
    'Cabanatuan Prison Hut.jpg': 'prison_hut.jpg',
    'Capt. Fisher.jpg': 'capt_fisher.jpg',
    'Mucci.jpg': 'mucci.jpg',
    'Henry A. Mucci.jpg': 'mucci_b.jpg',
    'Henry mucci.jpg': 'mucci_c.jpg',
    "Pajota's Guerrillas.jpg": 'pajota_guerrillas.jpg',
    'PajotaGuerillasCabuRaidCabanatuan.jpg': 'pajota_guerrillas_cabu.jpg',
    'POW March.jpg': 'pow_march.jpg',
    'POWs celebrate.jpg': 'pows_celebrate.jpg',
    'POWs in Hospital.jpg': 'pows_hospital.jpg',
    'POWs on Carts.jpg': 'pows_carts.jpg',
    'RangersafterRaidCabanatuan1945.jpg': 'rangers_after_raid.jpg',
    'RangerstrektallgrassJan1945.jpg': 'rangers_tall_grass.jpg',
    'RangerstrektoRaidCabanatuanJan301945.jpg': 'rangers_trek.jpg',
    'RangerwithCabanatuanPOWFeb1945.jpg': 'ranger_with_pow.jpg',
    'Rescued from Japs - DPLA - 9e283b4ad7a6ff71316d291fcd340565.jpg': 'rescued_from_japs.jpg',
    'RobertPrinceHortonVWhiteSixthArmy1945.jpg': 'prince_white_1945.jpg',
    'Gen. Krueger with Alamo scouts.jpg': 'krueger_alamo_scouts.jpg',
    'SC 201653 - Major Paul W. Wing, bareheaded, stands beside two friends after his release from the Cabanatuan prison camp on Luzon, P.I. (53009847516).jpg': 'sc201653_wing.jpg',
    'SC 201654 - L to R Robert C. Lautman, Signal Corps photographer who accompanied the 6th Ranger Bn. to the prison camp at Cabanatuan to release prisoners of war talking to T Sgt. Frederick Gutto (53010344333).jpg': 'sc201654_lautman.jpg',
    'SC 201655 - Pfc. Vernon M. Abbott of the 6th Ranger Bn. is shown carrying T Sgt. Charles G. Mortimer of Rainsburg, Pa., an injured prisoner of war released from the prison camp at Cabanatuan in the evac hospital. (53009275217).jpg': 'sc201655_abbott.jpg',
    'SC 396864 - Rangers of the 6th Ranger Bn. head toward the Cabanatuan prison camp on Luzon, P.I., in a daring move to liberate over five hundred prisoners of war. January, 1945. (52610717265).jpg': 'sc396864_rangers.jpg',
    'Giving a sick man a drink as US POWs of Japanese, Philippine Islands, Cabanatuan prison camp.jpg': 'camp_sick_drink.jpg',
    'On the porch of an emergency hospital these released American prisoners of war, liberated by U.S. Rangers from Cabanatuan prison camp on Luzon, Philippine Islands, wait for transfer to a base hospital. - NARA - 531251.tif': 'porch_hospital_531251.jpg',
    'Cap. Juan Pajota.JPG': 'pajota.jpg',
    'Captain Juan Pajota Cropped.jpg': 'pajota_crop.jpg',
    'Cabanatuan American Memorial.jpg': 'memorial.jpg',
    'Cabanatuan American Memorial - Flickr.jpg': 'memorial_flickr.jpg',
    'Cabanatuan American Memorial - Flickr 01.jpg': 'memorial_flickr1.jpg',
    'The Camp Pangatian Shrine in Cabanatuan City, Nueva Eija.JPG': 'pangatian_shrine.jpg',
    'Grave of Henry A Mucci.jpg': 'mucci_grave.jpg',
    'Honoring the past, U.S. and Philippines hold wreath-laying ceremony to recognize POWs at Pangatian War Memorial 140510-M-SD123-560.jpg': 'wreath_2014.jpg',
    'Cabanatuan American Memorial restoration project is a HUGH success 140508-A-KH064-070.jpg': 'memorial_2014.jpg',
    'Raid at Cabanatuan Memorare English historical marker.jpg': 'memorare_marker.jpg',
    'Alamo Scout.jpg': 'alamo_scout.jpg',
    'Alamoscouts losnegros feb1944.jpg': 'alamo_scouts_1944.jpg',
    'Cabanatuanraid3334jf.JPG': 'raid_site_jf.jpg',
    'Parkraidjf.JPG': 'raid_park_jf.jpg',
}

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"})
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(4 * (i + 1))
    raise SystemExit("API failed: " + url)

def fetch(url, out):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
                out.write_bytes(r.read()); return
        except Exception:
            time.sleep(5 * (i + 1))
    raise SystemExit("download failed: " + url)

meta = {}
out_dir = ROOT / "assets/stills"; out_dir.mkdir(parents=True, exist_ok=True)
for title, name in FILES.items():
    if title.startswith("?"):
        d = api({"action": "query", "list": "search", "srsearch": title[1:], "srnamespace": 6, "srlimit": 1})
        title = d["query"]["search"][0]["title"][5:]
    d = api({"action": "query", "titles": "File:" + title, "prop": "imageinfo",
             "iiprop": "url|size|extmetadata", "iiurlwidth": 1920})
    p = next(iter(d["query"]["pages"].values()))
    if "imageinfo" not in p:
        print("MISSING", title); continue
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    clean = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
    src = ii.get("thumburl") or ii["url"]
    if not (out_dir / name).exists():
        cands = [src] if "thumbnail_unscaled" not in src else []
        for w in [x for x in (1920, 1280, 960, 500, 330, 250) if x < ii["width"]]:  # unscaled originals answer 429: standard widths only
            if True:
                d2 = api({"action": "query", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": w})
                cands.append(next(iter(d2["query"]["pages"].values()))["imageinfo"][0].get("thumburl"))
        for c in [c for c in cands if c]:
            try:
                fetch(c, out_dir / name); break
            except SystemExit as e:
                print("  retry smaller:", e)
        else:
            print("FAILED", name); continue
        time.sleep(1)
    meta[name] = {"title": title, "page": ii["descriptionurl"], "license": clean("LicenseShortName"),
                  "artist": clean("Artist"), "credit": clean("Credit"), "date": clean("DateTimeOriginal"),
                  "description": clean("ImageDescription")[:400]}
    print(name, "|", meta[name]["license"], "|", title)
(ROOT / "research/stills_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
