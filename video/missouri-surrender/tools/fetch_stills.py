"""Download the episode's Commons photos (public domain) into assets/stills and record their metadata.
Usage: python tools/fetch_stills.py"""
import json, re, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "WWIIFrontlinesResearch/1.0 (documentary research)"
FILES = {
    'Generaal MacArthur praat met oorlogscorrespondenten na zijn aankomst op vliegveld Atsugi te Japan, Bestanddeelnr 32008 005.tif': 'atsugi_mac_press.jpg',
    'MacArthur arrives at Atsugi;ac01732.jpg': 'atsugi_mac_colour.jpg',
    'MacArthur and Sutherland.jpg': 'atsugi_mac_staff.jpg',
    'MacArthur C-2413.tif': 'mac_pipe_manila.jpg',
    'MacArthur and Wainright in Japan HD-SN-99-02411.JPEG': 'mac_wainwright_newgrand.jpg',
    'Allied battleships in Sagami Bay 28 Aug 1945.jpg': 'fleet_sagami_fuji.jpg',
    '80-G-490436 (23405890804).jpg': 'missouri_anchored.jpg',
    '80-G-331688 Surrender of Japan, 1945.jpg': 'halsey_toast.jpg',
    'Allied POWs at Aomori 1945-08-29.JPEG': 'pows_flags.jpg',
    '80-G-490443 (22553854449).jpg': 'boyington_rescued.jpg',
    'Cpl. Leopold Anthony Mulikowski, WSMC, of Muskegon, Mich., rests on board the USS Benevolence, AH-13, after rescue... - NARA - 520929.jpg': 'benevolence_pow_rest.jpg',
    'Navy nurse and released POW on USS benevolence, August 1945 highres.jpg': 'benevolence_nurse.jpg',
    'New Clothes for Released Allied Prisoners - NARA - 6200936.jpg': 'drop_supplies_gathered.jpg',
    'Grumman TBF Avenger of VT-9 drops supplies over a prisoner-of-war camp in Japan, circa in September 1945.jpg': 'drop_avenger.jpg',
    'Aerial view of a prisoner-of-war camp near Nagoya, Japan, in August 1945.jpg': 'camp_aerial_nagoya.jpg',
    'SC 364365 - U.S.S. Missouri taking its place for signing of the surrender. (52125036431).jpg': 'missouri_taking_place.jpg',
    '80-G-332655 (22698243498).jpg': 'officers_await.jpg',
    'Spectators and photographers pick vantage spots on the deck of the USS MISSOURI in Tokyo Bay, to witness the formal Japanese surrender proceedings HD-SN-99-03020.jpg': 'spectators_vantage.jpg',
    'Japanese surrender signatories arrive aboard the USS MISSOURI in Tokyo Bay to participate in surrender ceremonies. - NARA - 531311.tif': 'delegation_arrives.jpg',
    '80-G-332667 (23128091291).jpg': 'delegation_cane.jpg',
    'USA C-2719 (Color) (23925987372).jpg': 'delegation_colour.jpg',
    '80-G-332693 (22698225768).jpg': 'delegation_bw.jpg',
    'Japanese-surrender-mac-arthur-speaking-ac02716.jpg': 'mac_speaking_colour.jpg',
    '80-G-332694 (23128074971).jpg': 'mac_speaking_bw.jpg',
    'Mamoru Shigemitsu signs the Instrument of Surrender, officially ending the Second World War - Original.tif': 'shigemitsu_signs_kase.jpg',
    '80-G-332681 (22493900514).jpg': 'shigemitsu_signs_navy.jpg',
    '80-G-332701 (23116630195).jpg': 'umezu_signs.jpg',
    'LC-DIG-PPMSCA-19289 (SC 211872) (22963128646).jpg': 'mac_signs_wp.jpg',
    'USA C-4627 (Color) (23407419523).jpg': 'mac_signs_wp_colour.jpg',
    'SC 212246 Surrender of Japan, Tokyo Bay, 2 September 1945.tif': 'sutherland_corrects.jpg',
    'NH 58406 (23738480180).jpg': 'nimitz_signs.jpg',
    'Lawrence Moore Cosgrave signs formal surrender.jpg': 'cosgrave_signs.jpg',
    'USA C-1189 (Color) (23925977802).jpg': 'overall_colour.jpg',
    '80-G-332660 (23666197079).jpg': 'mac_nimitz_walk.jpg',
    'USS Missouri (BB-63) flyover, Tokyo Bay, 2 September 1945 (80-G-421130).jpg': 'flyover_fleet.jpg',
    "F4U's and F6F's fly in formation during surrender ceremonies, Tokyo, Japan. USS MISSOURI (in) left foreground. - NARA - 520775.tif": 'flyover_missouri.jpg',
    '80-G-K-15394 (Color) (23666283499).jpg': 'delegation_departs_colour.jpg',
    '80-G-472629 (23407323743).jpg': 'delegation_honours.jpg',
    'Japanese envoys leave the USS Missouri (BB-63) in Tokyo Bay, Japan, after signing surrender papers. - NARA - 520922.tif': 'envoys_leave.jpg',
    'Instrument of surrender Japan2.jpg': 'instrument_p2.jpg',
    'Instrument of surrender Japan.jpg': 'instrument_p1.jpg',
    'Emperor Hirohito and General MacArthur.jpg': 'hirohito_macarthur.jpg',
    '?Mamoru Shigemitsu portrait': 'shigemitsu_portrait.jpg',
    '?Yoshijiro Umezu': 'umezu_portrait.jpg',
    '?Jonathan Wainwright 1945 portrait': 'wainwright_portrait.jpg',
    '?Harold Stassen Navy': 'stassen_navy.jpg',
    '?Robert Eichelberger portrait': 'eichelberger_portrait.jpg',
    '?Chester Nimitz official portrait': 'nimitz_portrait.jpg',
    '?William Halsey Jr official portrait': 'halsey_portrait.jpg',
    '?Higashikuni Naruhiko': 'higashikuni_portrait.jpg',
    '?Toshikazu Kase': 'kase_portrait.jpg',
    '?USS Benevolence AH-13': 'benevolence_ship.jpg',
    '?Atsugi airfield 1945': 'atsugi_field.jpg',
    '?Tokyo 1945 aerial destruction': 'tokyo_ruins_aerial.jpg',
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
