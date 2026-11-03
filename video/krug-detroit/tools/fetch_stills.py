"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {  # Commons title (or search query prefixed "?") -> local name
    "Hans Peter Krug (1942).jpg": "krug_1942.jpg",
    "Max Stephan (1943).png": "stephan_1943.png",
    "Max Stephan jury.jpg": "jury_1942.jpg",
    "Arthur J. Tuttle portrait.jpg": "tuttle.jpg",
    "Bowmanville boys school to house Nazi officer prisoners.jpg": "bowmanville_1941.jpg",
    "Administration & school building at Camp 30.jpg": "camp30_admin_1941.jpg",
    "Detroit Skyline 1942.jpg": "detroit_skyline_1942.jpg",
    "Woodward Ave Detroit 1942.jpg": "woodward_1942.jpg",
    "Belle Island Bathing Beach, Detroit, Mich (62392).jpg": "belle_isle.jpg",
    "?Rockwell Canvas waiting room Greyhound bus terminal Pittsburgh Bubley": "pittsburgh_greyhound_1943.jpg",
    "Union Bus Terminal Nashville Tenn c1940.jpg": "nashville_bus_1940.jpg",
    "U. S. Penitentiary, Atlanta, Ga. (8343901588).jpg": "atlanta_pen.jpg",
    "Franklin D. Roosevelt - NARA - 196080.jpg": "fdr_1942.jpg",
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
