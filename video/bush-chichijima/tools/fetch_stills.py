"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    'George H.W. Bush seated in a Grumman TBM Avenger, circa 1944 (H069-13).jpg': 'bush_cockpit_tall.jpg',
    'George Bush in the cockpit of his TBM Avenger during World War II - NARA - 186383.tif': 'bush_cockpit_wide.jpg',
    'George Bush, Navy pilot during World War II - NARA - 186380.tif': 'bush_flight_gear.jpg',
    'George Bush being rescued by the submarine, the U.S.S. Finback, after being shot down while on a bombing run of the... - NARA - 186382.tif': 'bush_rescue_still.jpg',
    'General Motors TBM-1C Avenger of VT-51 takes off from USS San Jacinto (CVL-30) on 28 June 1944 (80-G-238783).jpg': 'vt51_takeoff_jun44.jpg',
    'TBM-1C of VT-51 launches from USS San Jacinto (CVL-30) in May 1944.jpg': 'vt51_launch_may44.jpg',
    'TBM-1C Avenger of VT-51 over Majuro Atoll in May 1944.jpg': 'vt51_majuro.jpg',
    'Torpedo is loaded on TBM aboard USS San Jacinto (CVL-30) in October 1944.jpg': 'sanjac_torpedo.jpg',
    'USS San Jacinto (CVL-30) off the Philadelphia Naval Shipyard on 17 January 1944 (NH 43506).jpg': 'sanjac_philly.jpg',
    'USS San Jacinto (CVL-30) underway at sea on 23 January 1944 (80-G-212798).jpg': 'sanjac_underway.jpg',
    'USS San Jacinto (CVL-30) and USS Lexington (CV-16) underway in June 1944.jpg': 'sanjac_lexington.jpg',
    'USS San Jacinto (CVL-30) underway on 31 May 1944.jpg': 'sanjac_may44.jpg',
    'Sailors in hangar of USS San Jacinto (CVL-30) in April 1944.jpg': 'sanjac_hangar.jpg',
    'General Motors TBM-1C Avenger of VT-2 enroute to Saipan, circa in June 1944 (80-G-428459).jpg': 'tbm_saipan.jpg',
    'TBM Avenger with Mark 13 torpedo aboard USS Wasp (CV-18), 13 October 1944 (80-G-298609).jpg': 'tbm_torpedo_wasp.jpg',
    'Grumman TBF Avenger landing aboard USS Charger (CVE-30) on 22 April 1944 (80-G-K-1518).jpg': 'tbf_charger_colour.jpg',
    'Damaged Grumman TBM-3 Avenger of VT-82 in flight, circa in February 1945 (NH 89380).jpg': 'tbm_flak_damage.jpg',
    'USS FINBACK (SS-230).tif': 'finback_launch.jpg',
    'Vought OS2U Kingfisher with rescued airmen off Truk on 1 May 1944 (80-G-227991).jpg': 'kingfisher_truk.jpg',
    'USS Harder (SS-257) rescueing pilot at Woleai 1944.jpg': 'harder_rescue.jpg',
    'Yoshio Tachibana surrender.jpg': 'tachibana_surrender.jpg',
    'Yoshio Tachibana.jpg': 'tachibana.jpg',
    'Chichijima Fortress Command.jpg': 'chichi_fortress_hq.jpg',
    'ChichijimaIncident.png': 'marines_search_1946.jpg',
    'Map by the US Army Map Service - Chichi-Jima - south japanese islands - txu-pclmaps-oclc-6614419-chichi-jima-sheet 2.jpg': 'ams_chichi_map.jpg',
    'Futami Harbor in 1920s.jpg': 'futami_1920s.jpg',
    'Chichi Jima Island Aerial photograph.2014.jpg': 'chichi_aerial_2014.jpg',
    'Aerial photo of Futami Port on Chichijima Island. February 24, 2014.jpg': 'futami_aerial_2014.jpg',
    'Port of Futami and Futami Bay from Ogamiyama Park.jpg': 'futami_pano.jpg',
    'Futami Port , Chichi-jima - panoramio.jpg': 'futami_port.jpg',
    'Wreck ``Hinkomaru``.jpg': 'hinko_maru_wreck.jpg',
    'Japanese soldier and war criminal is sentenced to death.jpg': 'guam_sentence.jpg',
    'Koso Abe.jpg': 'koso_abe_guam.jpg',
    'Former Japanese Admiral Chuichi Hare at the War Crimes Trial Building, 1948.jpg': 'guam_trial_building.jpg',
    'US Navy 020617-N-0252D-002 Former U.S. President George H. Bush greets Sailors.jpg': 'bush_2002_japan.jpg',
    'George H. W. Bush sits in the cockpit of a U.S. Navy TBM-1C Avenger aircraft in Fargo.jpg': 'bush_1994_tbm.jpg',
    'Aviation cadets check flight boards for last minute instructions at Naval Air Training Center Corpus Christi, Texas.... - NARA - 520975.tif': 'corpus_christi_cadets.jpg',
    'Deck Log of USS FINBACK (SS-230), September 2, 1944. - NARA - 305184.tif': 'doc_finback_deck_log.jpg',
    'U.S. Submarine War Patrol Report, USS FINBACK (SS-230), 10th War Patrol, September 2, 1945. - NARA - 305245.tif': 'doc_finback_patrol.jpg',
    'U.S. Submarine War Patrol Report, USS FINBACK (SS-230), 10th War Patrol, September 2, 1945. - NARA - 305245 page 2.tif': 'doc_finback_patrol_2.jpg',
    'Deck Log of USS SAN JACINTO (CVL-30), September 2, 1944. - NARA - 305182.tif': 'doc_sanjac_deck_log.jpg',
    'World War II Casualty List by Aircraft Type, TBM1C, September 2, 1944. - NARA - 305178.tif': 'doc_casualty_list.jpg',
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
