"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    "First 29 Navajo U.S. Marine Corps code-talker recruits being sworn in at Fort Wingate, NM. - NARA - 295175.jpg": "first29_1942.jpg",
    "Cpl. Henry Blake Jr., (left) and PFC George H. Kirk, Navajo Indians serving with a Marine Signal Unit.jpg": "blake_kirk_1943.jpg",
    "Navajo Indian communication men with the Marines on Saipan landed with the first assault waves to his the beach. - NARA - 532526.tif": "saipan_navajo_1944.jpg",
    "Navajo Code Talkers.jpg": "saipan_codetalkers_small.jpg",
    "Navajo code talkers (4373317805).jpg": "codetalkers_usmc_a.jpg",
    "Navajo code talkers (4374070382).jpg": "codetalkers_usmc_b.jpg",
    "Navajo Code Talkers talk.jpg": "codetalkers_talk.jpg",
    "Chester Nez.JPG": "chester_nez.jpg",
    "Honoring a Legend (13870772273).jpg": "nez_funeral_2014.jpg",
    "Liberated Allied prisoners of war at Nagasaki, in September 1945.jpg": "nagasaki_pows_1945.jpg",
    "Nagasaki 1945 - Before and after (adjusted).jpg": "nagasaki_before_after.jpg",
    "Nagasaki temple destroyed.jpg": "nagasaki_temple_1945.jpg",
    "A-bomb effects in Hamaguchi-machi district, Nagasaki.jpg": "nagasaki_hamaguchi_1945.jpg",
    "Burial detail at Camp O'Donnell after Bataan Death March.jpg": "odonnell_burial.jpg",
    "Photograph of American Prisoners Using Improvised Litters to Carry Comrades, 05-1942 - NARA - 535564.jpg": "litters_1942.jpg",
    "USMC first wave on Saipan HD-SN-99-02834.JPEG": "saipan_first_wave.jpg",
    "First Iwo Jima Flag Raising.jpg": "iwo_first_flag.jpg",
    "Shiprock rising above the high desert plain, San Juan County, New Mexico.jpg": "shiprock.jpg",
    "Postcard from the Fort Defiance Indian Agency - DPLA - 453ae941be4a0bdab25c456b186adda7 (page 1).jpg": "fort_defiance_postcard.jpg",
    "Navaho-enlistment-letter-page01.jpg": "vogel_letter_p1.jpg",
    "Navaho-enlistment-letter-page02.jpg": "vogel_letter_p2.jpg",
    "127-N-89670.jpg": "usmc_127n89670.jpg",
    "Members of the Navajo Code-Talkers, a World War II communications company which used Navajo language to convey military tactics while evading enemy detection, pledge allegiance to t - DPLA - 299e5b5e47c1be01cd78a2ce6824c7c9.jpeg": "codetalkers_pledge.jpg",
    "200th Coast Artillery NM Guard Philippines 1942.jpg": "200th_ca_1942.jpg",
    "NA 127-N-114541.jpg": "death_march_hands_tied.jpg",
    "Nagasakibomb.jpg": "nagasaki_cloud.jpg",
    "Medal presentation Smithsonian Code Talkers Bush (16925866277).jpg": "medal_2001.jpg",
    "Navajo code talker Thomas Begay.jpg": "thomas_begay.jpg",
    "Chester Nez (cropped).JPG": "chester_nez_cropped.jpg",
    "Postcard from the Fort Defiance Indian Agency - DPLA - 453ae941be4a0bdab25c456b186adda7 (page 2).jpg": "fort_defiance_postcard_b.jpg",
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
