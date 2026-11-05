"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {  # Commons title (or search query prefixed "?") -> local name
    "?SC 171617 German prisoners arriving prison camps Tunisia 1943": "tunisia_prisoners_1943.jpg",
    "?SC 171624 Unloading German prisoners arriving P.O.W. Tunisia": "tunisia_unloading_1943.jpg",
    "?German POWs aboard HMS JERVIS off Tunisia May 1943": "pows_jervis_1943.jpg",
    "?SC 184879 German war prisoners Camp Wallace Texas": "camp_wallace_a.jpg",
    "?SC 184882 German war prisoners Camp Wallace Texas work": "camp_wallace_b.jpg",
    "?SC 184884 Two German prisoners Camp Wallace Texas": "camp_wallace_c.jpg",
    "?Ft sam houston nat'l cem005": "fort_sam_pow_headstone.jpg",
    "?German Memorial Day ceremony Volkstrauertag Fort Sam Houston National Cemetery": "fort_sam_volkstrauertag_2023.jpg",
    "Fort Sam Houston National Cemetery, San Antonio, Texas, USA.jpg": "fort_sam_cemetery.jpg",
    "?United States Penitentiary Leavenworth Kansas West Street": "leavenworth.jpg",
    "View of the Main Entrance at Camp Swift Texas, August 6, 1944.jpg": "camp_swift_1944.jpg",
    "?Texas and New Orleans Southern Pacific Passenger Station Hearne": "hearne_station.jpg",
    "?Cotton Compress Hearne Texas": "hearne_cotton_compress.jpg",
    "Hearne TX - downtown with water tower.jpg": "hearne_downtown.jpg",
    "Camp Hearne Museum.png": "camp_hearne_museum.png",
    "Yorkville view from 86th St.jpg": "yorkville_view.jpg",
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
             "iiprop": "url|size|extmetadata", "iiurlwidth": 1800})
    p = next(iter(d["query"]["pages"].values()))
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    clean = lambda k: re.sub("<[^>]+>", "", m.get(k, {}).get("value", "")).strip()
    src = ii.get("thumburl") or ii["url"]
    if not (out_dir / name).exists():
        fetch(src, out_dir / name); time.sleep(1)
    meta[name] = {"title": title, "page": ii["descriptionurl"], "license": clean("LicenseShortName"),
                  "artist": clean("Artist"), "credit": clean("Credit"), "date": clean("DateTimeOriginal"),
                  "description": clean("ImageDescription")[:400]}
    print(name, "|", meta[name]["license"], "|", title)
(ROOT / "research/stills_meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
