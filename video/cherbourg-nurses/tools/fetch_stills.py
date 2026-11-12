"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "USS Pillsbury (DE-133) alongside the captured German submarine U-505 on 4 June 1944 (80-G-324310).jpg": "pillsbury_alongside.jpg",
    "Captured German submarine U-505 lies near USS Guadalcanal (CVE-60) on 4 June 1944 (80-G-49170).jpg": "u505_near_guadalcanal.jpg",
    "Captain Daniel V. Gallery, USN, on the bridge of the captured German submarine U-505 on 4 June 1944 (80-G-49176).jpg": "gallery_on_u505.jpg",
    "Captain Daniel V. Gallery and Lieutenant Albert L. David aboard USS Guadalcanal (CVE-60), 1944.jpg": "gallery_david.jpg",
    "Lieutenant David.jpg": "david_portrait.jpg",
    "German prisoners of war from the captured submarine U-505 exercise on USS Guadalcanal (CVE-60), in June 1944.jpg": "pows_exercise.jpg",
    "USS Abnaki (ATF-96) tows the captured German submarine U-505 in the Atlantic Ocean on 4 June 1944 (80-G-324351).jpg": "abnaki_tow.jpg",
    "A U.S. Navy boarding party working to secure a tow line to the bow of the captured German submarine U-505, 4 June 1944 (80-G-49172).jpg": "towline_party.jpg",
    "Damaged German submarine U-505 under fire in the Atlantic Ocean on 4 June 1944.jpg": "u505_under_fire.jpg",
    "Grumman TBM Avenger of VC-8 flies over the captured German submarine U-505, 4 June 1944 (80-G-49168).jpg": "avenger_over_u505.jpg",
    "Daniel V. Gallery Portrait.jpg": "gallery_portrait.jpg",
    "Binoculars 7x50, Leitz, U-505 - Museum of Science and Industry (Chicago) - DSC06761.JPG": "binoculars_msi.jpg",
    "U-505 submarine Museum of Science and Industry (Chicago) 01.jpg": "u505_msi_01.jpg",
    "U-505 submarine Museum of Science and Industry (Chicago) 02.jpg": "u505_msi_02.jpg",
    "Museum of Science and Industry (Chicago) U-505 Hall 02Dec08.JPG": "u505_hall_2008.jpg",
    "U.S. naval officers on the conning tower of the captured German submarine U-505, in June 1944 (NH 10585).jpg": "officers_conning_tower.jpg",
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
