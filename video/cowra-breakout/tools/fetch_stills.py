"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    'Darwin 42.jpg': 'darwin_neptuna_big.jpg',
    'USS Houston (CA-30) and USS Peary (DD-226) at Darwin 1942.jpg': 'houston_peary_darwin.jpg',
    '80-G-22163 (29528433590).jpg': 'zero_hiryu_crash.jpg',
    'StateLibQld 1 83231 Japanese prisoners of war arriving at Brisbane, ca. 1944.jpg': 'jpows_brisbane.jpg',
    'Japanese POW New Guinea.jpg': 'jpow_newguinea.jpg',
    'Japanese POWs Nov 1944.jpg': 'jpows_nov44.jpg',
    'Japanese prisoners and PIB at Singorkai.JPG': 'jpows_singorkai.jpg',
    'Cowra War Cemetery Hardy.JPG': 'grave_hardy.jpg',
    'Cowra War Cemetery Jones.JPG': 'grave_jones.jpg',
    'Cowra War Cemetery Doncaster.JPG': 'grave_doncaster.jpg',
    'Cowra Japanese War Cemetery Entry.JPG': 'jcem_entry.jpg',
    'Cowra Japanese War Cemetery 003.JPG': 'jcem_rows.jpg',
    'Cowra Japanese War Cemetery 001.JPG': 'jcem_wide.jpg',
    'Cowra Japanese War Cemetery 004.JPG': 'jcem_004.jpg',
    'Graves at the Japanese War Cemetery, Cowra August 2020.jpg': 'jcem_graves2020.jpg',
    'Cowra Japanese Gardens 2011 001.JPG': 'garden_001.jpg',
    'Cowra Japanese Gardens 2011 003.JPG': 'garden_lake.jpg',
    '07. Japanese Garden Pano, Cowra, NSW, 22.09.2006.jpg': 'garden_pano.jpg',
    '02. Japanese Garden, Cowra, NSW, 22.09.2006.jpg': 'garden_02.jpg',
    '06. Japanese Garden, Cowra, NSW, 22.09.2006.jpg': 'garden_cherry.jpg',
    'Cowra POW Camp Lookout Tower.JPG': 'site_tower.jpg',
    'Cowra POW Camp Ruins 001.JPG': 'site_ruins.jpg',
    'Cowra POW camp pan.jpg': 'site_pan.jpg',
    'Cowra POW Camp Breakout Monument.JPG': 'site_monument.jpg',
    'Cowra POW Camp Sign.JPG': 'site_sign.jpg',
    '619 - Cowra Prisoner of War Camp Site - PCO Plan Number 619 (5045173p1).jpg': 'pco_plan.jpg',
    'The monument to Lieutenant Harry Doncaster, killed in the Cowra Breakout of Japanese prisoners-of-war during World War Two. - panoramio.jpg': 'doncaster_monument.jpg',
    '?John Curtin prime minister portrait': 'curtin.jpg',
    '?Australian prisoners of war Changi 1945 released': 'aus_pows_changi.jpg',
    'Keiji Takezawa and Mr Albert J Oliver at Cowra High School 1970.jpg': 'takezawa_oliver.jpg',
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
