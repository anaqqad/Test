"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Dr. L.A. Fritsche LCCN2014716570.jpg": "fritsche.jpg",
    "THE TOWN OF NEW ULM, MINNESOTA, WAS FOUNDED IN 1854 BY A GROUP OF GERMAN IMMIGRANTS. SINGLE FAMILY HOUSING THERE RUNS... - NARA - 558157.jpg": "new_ulm_houses_1975.jpg",
    "AERIAL VIEW OF THE TOWN OF NEW ULM, MINNESOTA, FOUNDED BY A LAND SOCIETY, COMPOSED OF GERMAN IMMIGRANTS. THE SITE, ON... - NARA - 558112.jpg": "new_ulm_aerial_1975.jpg",
    "MONUMENT AND STATUE OF HERMANN-ARMINIUS, GERMAN PATRIOT WHICH WAS ERECTED IN NEW ULM, MINNESOTA, IN 1888. THE TOWN... - NARA - 558116.jpg": "hermann_1975.jpg",
    "CLOSEUP OF THE STATUE OF HERMANN-ARMINIUS, GERMAN PATRIOT WHICH WAS ERECTED IN NEW ULM, MINNESOTA, IN 1888. THE TOWN... - NARA - 558114.jpg": "hermann_close_1975.jpg",
    "New ulm minnesota a6a34530u.tif": "new_ulm_1906.jpg",
    "New Ulm MN 1918.jpg": "new_ulm_1918.jpg",
    "New Ulm, Minnesota street scene.jpg": "new_ulm_street.jpg",
    "1915postcardNewUlmRollerMills.jpg": "new_ulm_mills_1915.jpg",
    "Flandrau State Park Group Camp.jpg": "flandrau_group_camp.jpg",
    "FlandrauStateParkBeachHouse.jpg": "flandrau_beachhouse.jpg",
    "Cottonwood River Flandrau.jpg": "cottonwood_river.jpg",
    "TEENAGE WORKERS ARE BARELY VISIBLE AS THEY DETASSEL CORN DURING THE SUMMER IN FIELDS NEAR NEW ULM, MINNESOTA. THE... - NARA - 558243.jpg": "corn_new_ulm_1975.jpg",
    "SC 192054-S - Prisoners of war captured in Lajatico sector by the 351st Inf. Regt., 88th Div., Fifth Army, smiling at their interrogator, expressing pleasure to be out of the war. 12 July, 1944.jpg": "pows_smiling_1944.jpg",
    "SC 196558 - Youthful German prisoners of war, captured near Kinzweiler, Germany, by the 120th Infantry Regiment, 30th Division. 21 November, 1944. (49547441856).jpg": "young_pows_1944.jpg",
    "Be with him at every mail call. V mail is private, reliable, patriotic.jpg": "vmail_poster.jpg",
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
