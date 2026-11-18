"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "General of the Army Douglas MacArthur and Lieutenant General Jonathan Wainwright greet each other at the New Grand... - NARA - 531310.tif": "reunion_1945.jpg",
    "MacArthur and Wainright in Japan HD-SN-99-02411.JPEG": "reunion_b_1945.jpg",
    "Jonathan Wainwright under Imperial Japanese army.jpg": "wainwright_captive_1942.jpg",
    "Douglas MacArthur signs formal surrender.jpg": "missouri_signing.jpg",
    "General Douglas MacArthur signs as Supreme Allied Commander during formal surrender ceremonies on the USS Missouri in Tokyo Bay.jpg": "missouri_signing_b.jpg",
    "Wainwright and MacArthur at Philippine.jpg": "wainwright_macarthur_1941.jpg",
    "80-G-354136 Lieutenant General Jonathan M. Wainwright, USA.jpg": "wainwright_portrait.jpg",
    "Jonathan M. Wainwright - Official Portrait.jpg": "wainwright_official.jpg",
    "Americans Surrender Bataan.jpg": "bataan_surrender_1942.jpg",
    "General Jonathan Wainwright and Mrs. Wainwright Unveiling Japanese Surrender Documents, September 12, 1945 (4068880051).jpg": "wainwright_documents_1945.jpg",
    "Jonathan M. Wainwright, Djawa Baroe, Vol. 1, Iss. 7 (1943-04-01), p9.jpg": "djawa_baroe_1943.jpg",
    "American generals in captivity, July 1942.jpg": "generals_captivity_1942.jpg",
    "Surrender of Japanese Forces in the Philippines 1945.jpg": "baguio_1945.jpg",
    "The sidewalks of lower Broadway are jammed as the Wainwright motorcade goes north toward City Hall (LOC) (54563114524).jpg": "broadway_1945.jpg",
    "?MacArthur Jean Marie Adelaide railway station 20 March 1942": "adelaide_1942.jpg",
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
