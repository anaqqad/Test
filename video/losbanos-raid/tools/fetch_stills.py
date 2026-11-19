"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "Former internees of Los Banos with 11th Airborne troopers, 1945.jpg": "bowie_family_1945.jpg",
    "Navy Nurses Rescued from Los Banos.jpg": "navy_nurses_kinkaid_1945.jpg",
    "Navy Nurses Rescued from Los Banos 2.jpg": "navy_nurses_b_1945.jpg",
    "The American Soldier 1945.jpg": "american_soldier_painting.jpg",
    "LTG Joseph M. Swing.jpg": "swing.jpg",
    "188th GIR at Nasugbu, 1945.jpg": "gir188_nasugbu_1945.jpg",
    "XIV Corps Operations in Southern Luzon.jpg": "xiv_corps_map_1945.jpg",
    "Pook ng Bilangguang Kampo sa Los Baños, UPLB.jpg": "camp_marker_uplb.jpg",
    "Baker Hall historical marker.jpg": "baker_hall_marker.jpg",
    "Marking's Guerrillas.jpg": "markings_marker.jpg",
    "Laguna de Bay (view from Biñan, Laguna).jpg": "laguna_de_bay.jpg",
    "Santo Tomas.jpg": "santo_tomas_aerial_1945.jpg",
    "Shanties, STIC.jpg": "santo_tomas_shanties.jpg",
    "Liberation-Men-- santo tomas.jpg": "santo_tomas_men_1945.jpg",
    "WomenPOWs2.jpg": "santo_tomas_women.jpg",
    "1943 Meal card issued to interned civilians at the Santo Tomas Internment Camp.jpg": "meal_card_1943.jpg",
    "Army nurses rescued from Santo Tomas 1945.jpg": "army_nurses_1945.jpg",
    "Raising the Flag on Iwo Jima, larger - edit1.jpg": "iwo_flag_rosenthal.jpg",
    "DouglasMacArthur1945.jpg": "macarthur_1945.jpg",
    "SC 364522 - General view of Forward CP of \"D\" Co., 1st Bn., 511th P.I., 11th Airborne Div. Mt. Malapuno area, Luzon, P.I. 24 April, 1945.jpg": "co511_cp_1945.jpg",
    "11th-airborne-paradrop-june-45-luzon-8x10.jpg": "paradrop_aparri_1945.jpg",
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
