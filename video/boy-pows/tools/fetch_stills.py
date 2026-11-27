"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    'Hans-Georg Henke.jpg': 'boy_pow_crying.jpg',
    'Potato farms in Aroostook County, Me. LCCN2017877410.jpg': 'aroostook_farm1.jpg',
    'Potato farms in Aroostook County, Me. LCCN2017877405.jpg': 'aroostook_farm2.jpg',
    'Potato farm in Aroostook county, Me., after the potatoes have been harvested LCCN2017877407.jpg': 'aroostook_after.jpg',
    'Children gathering potatoes on a large farm, vicinity of Caribou, Aroostook County, Me. Schools do not open until the potatoes are harvested LCCN2017877412.jpg': 'aroostook_children.jpg',
    'Potato farms showing layout of land and buildings, vicinity of Caribou, Aroostook, Me. LCCN2017877416.jpg': 'aroostook_layout.jpg',
    'German prisoners of war camp on December 18, 1944, Dade City, Florida - NARA - 23936579 (cropped).jpg': 'pows_dadecity.jpg',
    'German Prisoners of War Debarking - DPLA - e5831ff877fb467d3c8f71337abf8335.jpg': 'pows_debarking.jpg',
    'Medic gives a shot to soldier near front line (SC 361229), National Museum of Health and Medicine (3300153020).jpg': 'korea_medic.jpg',
    'Wounded soldier arriving at the 8063rd MASH.jpg': 'korea_mash.jpg',
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
