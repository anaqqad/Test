"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    '"... WAAC cooks prepare dinner for the first time in new kitchen at Fort Huachuca, Arizona.", 12-05-1942 - NARA - 531152.jpg': 'huachuca_kitchen.jpg',
    'Private William Major and Private Andrew Paxson patrol the southern border from a peak of the Huachuca Mountains.jpg': 'huachuca_patrol.jpg',
    'The 93rd Infantry Division reactivated May 15, 1942, was the first all-Negro division to be formed during World War... - NARA - 531142.tif': 'huachuca_93rd.jpg',
    '"WAAC officers go shopping...soon after their arrival at Fort Huachuca, Arizona, these two officers (3d Officers Vera Ha - NARA - 531154.jpg': 'huachuca_waac.jpg',
    'German Prisoners of War Debarking - DPLA - e5831ff877fb467d3c8f71337abf8335.jpg': 'pows_debarking.jpg',
    'German prisoners of war camp on December 18, 1944, Dade City, Florida - NARA - 23936579 (cropped).jpg': 'pows_dadecity.jpg',
    'Funeral of Richard Jasker, German prisoner of war, who died of natural causes, at Camp Robinson prisoner of war camp. 24 April, 1944. (49622305606).jpg': 'robinson_funeral.jpg',
    '"Lena Horne conserves fuel (gas).", ca. 1941 - ca. 1945 - NARA - 535820.jpg': 'horne_fuel.jpg',
    '(Portrait of Lena Horne, New York, N.Y., between 1946 and 1948) (LOC) (4843132965).jpg': 'horne_gottlieb.jpg',
    'Lena Horne with Tuskegee airmen.png': 'horne_tuskegee.png',
    'Camp Robinson Arkansas Company D 68th Training Battalion - Feb 1943.jpg': 'robinson_pano.jpg',
    '1943 Colored Waiting Room Sign.jpg': 'colored_waiting.jpg',
    'JimCrowInDurhamNC.jpg': 'durham_bus.jpg',
    '“COLORED WAITING ROOM” and “HITLER’S LOVE LIFE REVEALED” - Jim Crow in Durham, North Carolina (cropped).jpg': 'durham_hitler.jpg',
    "Executive Order 9981 dated July 26, 1948, Establishing the President's Committee on Equality of Treatment and Opportunity in the Armed Services - DPLA - cfebd9153dfafb906c36564baed37b99 (page 1).jpg": 'eo9981_p1.jpg',
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
