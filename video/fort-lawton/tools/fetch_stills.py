"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Staff_Sergeant_Charles_M_Robinson_where_Guglielmo_Olivotto_was_hung,_1944,_U.S._ARMY_Signal_Corps.jpg": "obstacle_course_1944.jpg",
    "Members_of_the_Fort_Lawton_Court_Martial_Panel_(top)_with_Judge_Advocate_General_Corps_defense_(bottom_left)_and_prosecution_lawyers_(bottom_right)_and_stenographer_(bottom_center).jpg": "court_panel_1944.jpg",
    "Fort_Lawton_-_Guglielmo_Olivotto_grave_01.jpg": "olivotto_grave.jpg",
    "Fort_Lawton_headstone_of_Gugliemo_Olivotto.jpg": "olivotto_headstone.jpg",
    "Fort_Lawton_Cemetery_01.jpg": "fort_lawton_cemetery.jpg",
    "Fort_Lawton_01.jpg": "fort_lawton_buildings.jpg",
    "Seattle_-_Discovery_Park_04.jpg": "discovery_park_meadow.jpg",
    "Discovery_Park,_Seattle_pano_01.jpg": "discovery_park_pano.jpg",
    "Seattle_-_Second_Avenue,_1944.gif": "seattle_1944.gif",
    "Jaworski_Newcombe_(cropped).jpg": "jaworski_1977.jpg",
    "SC_180068_-_Italian_prisoners_of_war_in_America._(52613822973).jpg": "italian_pows_a.jpg",
    "SC_180070_-_Italian_prisoners_of_war_in_America._(52613328861).jpg": "italian_pows_b.jpg",
    "SC_180072_-_Italian_prisoners_of_war_in_America._(52613582244).jpg": "italian_pows_c.jpg",
    "Fort_Lawton_Freedom_Grove_plaque.jpg": "freedom_grove_plaque.jpg",
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
    for i in range(6):
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
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    clean = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
    src = ii.get("thumburl") or ii["url"]
    if not (out_dir / name).exists():
        if "thumbnail_unscaled" in src:  # small originals: ask for a standard thumbnail width (unscaled originals get 429)
            w = max(x for x in (250, 330, 500, 960, 1280) if x < ii["width"]) if ii["width"] > 250 else None
            if w:
                d2 = api({"action": "query", "titles": "File:" + title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": w})
                src = next(iter(d2["query"]["pages"].values()))["imageinfo"][0]["thumburl"]
        fetch(src, out_dir / name); time.sleep(1)
    meta[name] = {"title": title, "page": ii["descriptionurl"], "license": clean("LicenseShortName"),
                  "artist": clean("Artist"), "credit": clean("Credit"), "date": clean("DateTimeOriginal"),
                  "description": clean("ImageDescription")[:400]}
    print(name, "|", meta[name]["license"], "|", title)
(ROOT / "research/stills_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
