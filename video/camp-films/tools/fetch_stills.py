"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Halloran General Hospital, Staten Island, N.Y (NYPL b15279351-104782).tiff": "halloran_a.jpg",
    "17112-Halloran General Hospital, Staten Island, N.Y (NYPL b15279351-104744).tiff": "halloran_b.jpg",
    "Halloran General Hospital, Stapleton, Staten Island, N.Y (NYPL b15279351-104756).tiff": "halloran_c.jpg",
    "Aerial, Camp Butner 001 (21955780899).jpg": "butner_aerial.jpg",
    "From PhC.184 Massengill Postcard Collection, August 2015 addition, State Archives of North Carolina, Raleigh, NC. (21950899520).jpg": "butner_postcard.jpg",
    "Italian POWs at Camp Butner during World War II.jpg": "butner_italian_pows.jpg",
    "SC 184883 - This German prisoner of war, a former watchmaker, now repairs typewriters at Camp Wallace, Texas, as a part of his assigned work. 1943. (52278313082).jpg": "wallace_watchmaker.jpg",
    "SC 184881 - German war prisoners at Camp Wallace, Texas, assigned to work in the warehouse are shown as they make up an order of fruits and vegetables. 1943. (52277277152).jpg": "wallace_warehouse.jpg",
    "SC 184880 - German war prisoners at Camp Wallace, Texas, assigned to work in the Ordnance Command Shop -5 take a great interest in the American automobile and truck. (52278394112).jpg": "wallace_truck.jpg",
    "German Prisoners of War Farming in Normandy - DPLA - 0395dab7c721104fa1692964daf640aa.jpg": "pows_normandy_farm.jpg",
    "Crossville-Main-Street-tn1.jpg": "crossville_main.jpg",
    "Crossville-old-courthouse-tn1.jpg": "crossville_courthouse.jpg",
    "Prisoners liberation dachau.jpg": "dachau_liberation.jpg",
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
