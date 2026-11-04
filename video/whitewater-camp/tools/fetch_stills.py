"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {  # Commons title (or search query prefixed "?") -> local name
    "Camp Merged.jpg": "whitewater_camp_1944.jpg",
    "German Prisoners of War Debarking - DPLA - e5831ff877fb467d3c8f71337abf8335.jpg": "pows_debarking_1942.jpg",
    "German prisoners wait for transport to the rear at El Alamein, 25 October 1942. E18523.jpg": "alamein_prisoners_1942.jpg",
    "A British soldier gives a V-for-Victory sign to German prisoners captured at El Alamein, 26 October 1942. E18522.jpg": "alamein_prisoners_b.jpg",
    "Prison team Camp 132 Medicine Hat.jpg": "medicine_hat_hockey.jpg",
    "Eaton's Spring and Summer Catalogue 1942.jpg": "eatons_1942.jpg",
    "MunitionsWorkersToronto.jpg": "munitions_workers_1944.jpg",
    "Workers from GECO munitions factory dancing (I0058227).jpg": "geco_dance_1943.jpg",
    "Winnipeg 1944 a068055-v8.jpg": "winnipeg_1944.jpg",
    "Moon Lake shoreline - Riding Mountain National Park.JPG": "rmnp_moon_lake.jpg",
    "Riding mountain national park 3 - reflection.jpg": "rmnp_reflection.jpg",
    "Bison herd - Lake Audy - Riding Mountain National Park.JPG": "rmnp_lake_audy.jpg",
    "Riding Mountain National Park Manitoba Canada (5).JPG": "rmnp_forest.jpg",
    "Shoal Lake grain elevator.jpg": "shoal_lake_elevator.jpg",
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
