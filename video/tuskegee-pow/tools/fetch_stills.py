"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Lt. Col. (retired) Alexander Jefferson, Veterans Day 2013 131111-Z-GK080-023.jpg": "jefferson_2013.jpg",
    "Tuskegee Airmen 332nd Fighter Group pilots ppmsca13245u.jpg": "pilots_frissell.jpg",
    "Tuskegee airman.jpg": "airman_frissell_a.jpg",
    "Tuskegee airman2.jpg": "airman_frissell_b.jpg",
    "Tuskegee airmen 2.jpg": "airmen_frissell_c.jpg",
    "Tuskegee airmen attending a briefing in Ramitelli, Italy.jpg": "briefing_ramitelli.jpg",
    "Tuskegee airmen exiting the parachute room.jpg": "parachute_room.jpg",
    "Tuskegee airmen playing cards in the officers' club.jpg": "officers_club.jpg",
    "P-51Cs 332nd FG with goats Ramitelli 1945.jpg": "p51s_ramitelli.jpg",
    "Pilots of the 332nd Fighter Group.jpg": "pilots_332nd.jpg",
    "Tuskegee Airman Edward Gleed with his P-51.jpg": "gleed_p51.jpg",
    "First Tuskeegee Class.jpg": "first_class.jpg",
    "Stalag Luft III.jpg": "stalag_luft3.jpg",
    "Stalag Luft III drawing.jpg": "stalag_luft3_drawing.jpg",
    "2015 Zagan Stalag 2.JPG": "zagan_2015.jpg",
    "Liberation of Stalag 7a, Moosburg, Germany BU7099.jpg": "moosburg_a.jpg",
    "Liberation of Stalag 7a, Moosburg, Germany BU7103.jpg": "moosburg_b.jpg",
    "Liberation of Stalag 7a, Moosburg, Germany BU7104.jpg": "moosburg_c.jpg",
    "Liberation of Stalag 7a, Moosburg, Germany BU7116.jpg": "moosburg_d.jpg",
    "Stalag VII A.jpg": "stalag_7a.jpg",
    "RMS Queen Mary 20Jun1945 NewYork.jpeg": "queen_mary_1945.jpg",
    "Alexander Jefferson Tuskegee Airman.JPG": "jefferson_cc.jpg",
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
