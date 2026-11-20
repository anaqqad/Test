"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Honma Masaharu.jpg": "homma_portrait.jpg",
    "Portrait of General Masaharu Homma, 1943.jpg": "homma_1943.jpg",
    "Masaharu Homma ashore at Lingayen Gulf.jpg": "homma_lingayen_1941.jpg",
    "General Masaharu Homma, the \"Poet General\", on inspection tour of his Philippine command.jpg": "homma_poet_general.jpg",
    "Masaharu Homma and Shigenori Kuroda.jpg": "homma_kuroda_1945.jpg",
    "Japanese War Crimes Trials. Manila - NARA - 292610.jpg": "homma_trial_opening_1946.jpg",
    "111-SCA-Album 2919 180.jpg": "homma_prosecution_1946.jpg",
    "111-SCA-Album 2919 182.jpg": "homma_bows_mp_1946.jpg",
    "111-SCA-Album 2919 184.jpg": "homma_sentence_1946.jpg",
    "111-SCA-Album 2919 192.jpg": "homma_commission_standing.jpg",
    "111-SCA-Album 2919 194.jpg": "homma_commission_listen.jpg",
    "111-SCA-Album 2919 196.jpg": "homma_commission_evidence.jpg",
    "111-SCA-Album 2919 204.jpg": "homma_stand_a.jpg",
    "111-SCA-Album 2919 206.jpg": "homma_stand_b.jpg",
    "111-SCA-Album 2919 208.jpg": "homma_stand_c.jpg",
    "111-SCA-Album 2919 210.jpg": "homma_stand_d.jpg",
    "Americans Surrender Bataan.jpg": "surrender_negotiation_1942.jpg",
    "Bataan prisoners.jpg": "death_march_tied.jpg",
    "Burial detail at Camp O'Donnell after Bataan Death March.jpg": "odonnell_litters.jpg",
    "Surrender of American troops at Corregidor, Philippine Islands, 05-1942 - NARA - 535553.jpg": "corregidor_surrender_1942.jpg",
    "MacArthur Manila.jpg": "macarthur_manila_1945.jpg",
    "DouglasMacArthur1945.jpg": "macarthur_1945.jpg",
    "Gen. Masaharu Homma Execution Site.jpg": "homma_execution_site.jpg",
    "SUPREME COURT, U.S. STONE COURT LCCN2016862734.jpg": "supreme_court_stone.jpg",
    "Wiley Rutledge.jpg": "rutledge.jpg",
    "King discusses surrender.gif": "king_nakayama_1942.jpg",
    "American generals in captivity, July 1942.jpg": "generals_captivity_1942.jpg",
    "2016 Bataan Memorial Death March 160320-A-VT089-094.jpg": "bmdm_2016_survivor.jpg",
    "Bataan Memorial Death March 120325-A-TC907-865.jpg": "bmdm_2012_finish.jpg",
    "Jonathan M. Wainwright - Official Portrait.jpg": "wainwright_portrait.jpg",
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
