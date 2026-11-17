"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "William Edwin Dyess.jpg": "dyess_portrait.jpg",
    "Bataan prisoners.jpg": "bataan_prisoners.jpg",
    "Burial detail at Camp O'Donnell after Bataan Death March.jpg": "odonnell_burial.jpg",
    "March of Death - Resting 03.jpg": "march_resting.jpg",
    "?Photograph of American Prisoners Using Improvised Litters to Carry Comrades": "litters_1942.jpg",
    "Austin C. Shofner as 1st LT in January 1941.jpg": "shofner_1941.jpg",
    "Stephen Michael Mellnik - Cadet Photo.jpg": "mellnik_cadet.jpg",
    "USS Trout (SS-202) (51075706306).jpg": "uss_trout.jpg",
    "Davao Penal Colony train.jpg": "dapecol_train.jpg",
    "?Map by the US Army Map Service - Davao and Santa Ana": "davao_map_1944.jpg",
    "Lockheed P-38G-1-LO Lightning LOC fsa.8d22581.jpg": "p38g_1942.jpg",
    "Administration Building, Grand Central Airport, Glendale, Calif (post 00219).jpg": "grand_central_postcard.jpg",
    "Davao Penal Colony Historical Marker.jpg": "dapecol_marker.jpg",
    "?List of American Prisoners of the Japs in the Davao Concentration Camp, 17 February 1945": "davao_list_1945.jpg",
    "LCDR Arthur H Clark.jpg": "clark_trout.jpg",
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
