"""Builds two ~1-minute WWII Frontlines Shorts from the Bush / Chichi Jima episode (23 Nov 2026):

    data/reel-wwf-bush-fire.json       "Navy File Shows What George Bush Did When His Plane Caught Fire"
    data/reel-wwf-chichi-airmen.json   "8 Airmen Were Captured on Chichi Jima. None Came Home"

Long episode: https://youtu.be/8oOy8vqR4Lg. Research: WWII Frontlines repo, video/bush-chichijima/research/sources.md
(numbered sources there) and script.md. Film: U.S. Navy / Army film in that episode's assets/footage (public domain).
Photos and document strips: shorts/prep_bush_shorts.py in the WWII Frontlines repo writes public/pd/<id>/.
"""
import json
from pathlib import Path

DATA = Path(__file__).parent
EPISODE = "https://youtu.be/8oOy8vqR4Lg"

FIN = "USS Finback film of the rescue of Lt.(jg) George Bush, 2 Sept 1944 (George Bush Presidential Library / NARA)"
B24 = "7th AAF combat film CS-2599, B-24s over the Bonin Islands, 1944 (NARA)"
B24B = "11th Bomb Group combat film CS-3618, Chichi Jima, 1945 (NARA)"
BOMB = "Signal Corps film 111-ADC-1817, Chichi Jima bombed, Sept 1944 (NARA)"
SURA = "U.S. Navy film 428-NPC-17059, surrender of Chichi Jima aboard USS Dunlap, 3 Sept 1945 (NARA)"
SURB = "U.S. Navy film 428-NPC-17060, USS Dunlap off Chichi Jima, Sept 1945 (NARA)"

# Kokoro respellings, from the episode's tools/tts_kokoro.py PRON table (checked there with whisper)
PRON = {"Chichi Jima": "Chee-chee Jee-mah", "Iwo Jima": "Ee-woh Jee-mah", "Tachibana": "Tah-chee-bah-nah",
        "Matoba": "Mah-toh-bah", "Delaney": "Deh-lay-nee", "Yoshio": "Yo-shee-oh"}


def V(clip, focus=(0.5, 0.45), zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap):
    return {"kind": "card", "image": img, "caption": cap}


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


def spec(id, title, beats, clips, assets, sources, facts):
    return {
        "id": id, "title": title, "format": "reel", "fps": 30, "width": 1080, "height": 1920,
        "music": {"volume": 0.06},
        "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
        "brand": {"page": "WWII Frontlines", "cta": "Follow WWII Frontlines for more.", "theme": "wwf"},
        "voice": {"engine": "kokoro", "voice": "bm_george", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 0.6},
        "pronounce": PRON,
        "assets": {k: {"commons": v} for k, v in assets.items()},
        "clips": clips, "beats": beats, "sources": sources, "facts": facts,
    }


def beat(B, id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


S = lambda u: {"url": u}
SOURCES = {
    "AAR": S("https://catalog.archives.gov/id/305238"),
    "FINBACK": S("https://catalog.archives.gov/id/139746844"),
    "LOGBOOK": S("https://catalog.archives.gov/id/631635432"),
    "STINNETT": S("https://www.bush41library.gov/"),
    "NHHC": S("https://www.history.navy.mil/research/histories/biographies-list/bios-b/bush-george-h-w.html"),
    "LETTER": S("https://archive.org/details/allbestgeorgebus00bush"),
    "TRIAL": S("https://catalog.archives.gov/id/6997357"),
    "IWG": S("https://www.archives.gov/files/iwg/japanese-war-crimes/introductory-essays.pdf"),
    "TIME": S("https://time.com/archive/"),
    "BRADLEY": S("https://en.wikipedia.org/wiki/Chichijima_incident"),
    "EPISODE": S(EPISODE),
}

# ---------------------------------------------------------------- Short 1: the fire
A = []
beat(A, "hook", "Before he was President, George Bush was shot down over Chichi Jima. His engine was on fire, and he kept diving.",
     P("portrait", (0.5, 0.3), (1.1, 1.2), (0.5, 0.42)), section="hook",
     overlays={"hook": "His engine was on fire. *He kept diving.*"}, captions=False, speed=1.3)
beat(A, "target", "September 2nd, 1944. His target: a radio station on Chichi Jima.",
     C("takeoff", "A VT-51 Avenger leaves USS San Jacinto, 1944"), overlays={"stamp": "September 2, 1944"}, section="story")
beat(A, "flak", "At eight thousand feet, anti-aircraft fire hit his engine.", V("flak", (0.5, 0.5), (1.0, 1.1)))
beat(A, "doc", "The Navy report says the hit caused his engine to smoke and catch on fire. Bush continued in his dive, releasing his bombs on the radio station.",
     C("doc_fire", "VT-51 Aircraft Action Report, 2 Sept 1944 (National Archives)"))
beat(A, "bail", "Then he turned out to sea, and told his crew to bail out.", V("smoke", (0.5, 0.5), (1.0, 1.1)))
beat(A, "chute", "The report says one other man jumped. His parachute did not open.",
     C("doc_chute", "VT-51 Aircraft Action Report, 2 Sept 1944 (National Archives)"))
beat(A, "crew", "Ted White and John Delaney were never found.", C("crew", "John Delaney (left), Leo Nadeau and George Bush"))
beat(A, "sea", "Bush landed in the sea, and paddled his raft away from the island.", V("sea", (0.5, 0.5), (1.0, 1.08)), section="rescue")
beat(A, "film", "The submarine Finback came up beside him. Someone aboard filmed the rescue. This is that film.",
     V("raft", (0.5, 0.5), (1.0, 1.06)))
beat(A, "letter", "He wrote home that he felt terribly responsible for his crew.", V("walk", (0.55, 0.45), (1.1, 1.18)))
beat(A, "missions", "Then he went back to his squadron, and flew fifty-eight combat missions.", P("cockpit", (0.45, 0.4), (1.05, 1.15)))
beat(A, "close", "That was George Bush.", P("portrait", (0.5, 0.3), (1.2, 1.3), (0.5, 0.42)), section="end")
beat(A, "cta", "Follow WWII Frontlines for more.", {"kind": "endcard"}, section="cta", captions=False)

spec_a = spec(
    "reel-wwf-bush-fire", "Navy File Shows What George Bush Did When His Plane Caught Fire", A,
    {
        "flak": {"file": "chichi_b24_1944.mp4", "commons": B24, "start": 290.5, "dur": 6},
        "smoke": {"file": "chichi_bombing_1944.mp4", "commons": BOMB, "start": 73.5, "dur": 7},
        "sea": {"file": "finback_rescue_1944.mp4", "commons": FIN, "start": 44.8, "dur": 6},
        "raft": {"file": "finback_rescue_1944.mp4", "commons": FIN, "start": 22.9, "dur": 11.8},
        "walk": {"file": "finback_rescue_1944.mp4", "commons": FIN, "start": 37.8, "dur": 3.6, "speed": 0.7},
    },
    {"portrait": "George Bush, Navy pilot during World War II - NARA - 186380.tif",
     "takeoff": "General Motors TBM-1C Avenger of VT-51 takes off from USS San Jacinto (CVL-30) on 28 June 1944 (80-G-238783).jpg",
     "crew": "George Bush's flight crew (NARA 485327702)",
     "cockpit": "George Bush in the cockpit of his TBM Avenger during World War II - NARA - 186383.tif",
     "doc_fire": "VT-51 Aircraft Action Report, 2 Sept 1944, sheet 4", "doc_chute": "VT-51 Aircraft Action Report, 2 Sept 1944, sheet 4"},
    SOURCES,
    [
        {"beat": "hook", "sources": ["AAR", "NHHC"], "note": "Engine hit, smoke and fire, continued in his dive (AAR sheet 4; DFC citation via NHHC)."},
        {"beat": "target", "sources": ["AAR", "LOGBOOK"], "note": "Strike Baker, radio station, 2 Sept 1944."},
        {"beat": "flak", "sources": ["AAR", "NHHC"], "note": "Hit in the engine shortly after push-over at 8,000 ft."},
        {"beat": "doc", "sources": ["AAR"], "note": "Verbatim from sheet 4."},
        {"beat": "bail", "sources": ["AAR", "STINNETT"], "note": "Turned east to clear the island; 'Told them to bail out' (Bush, 1992)."},
        {"beat": "chute", "sources": ["AAR", "FINBACK"], "note": "AAR: one other person seen to bail out, chute did not open. Finback report differs (Bush saw no chutes); the Short quotes the AAR as 'the report says'."},
        {"beat": "crew", "sources": ["AAR", "LOGBOOK"], "note": "White and Delaney missing; declared dead 3 Sept 1945."},
        {"beat": "sea", "sources": ["AAR", "STINNETT"]},
        {"beat": "film", "sources": ["FINBACK", "EPISODE"], "note": "Picked up 1156; film from the conning tower, usually credited to Ens. Bill Edwards."},
        {"beat": "letter", "sources": ["LETTER"], "note": "Letter to his parents from Finback, in All the Best (1999)."},
        {"beat": "missions", "sources": ["NHHC", "LOGBOOK"], "note": "58 combat missions, DFC, three Air Medals."},
    ],
)

# ---------------------------------------------------------------- Short 2: the eight airmen
B = []
beat(B, "hook", "During the war, eight American airmen were captured on Chichi Jima. Not one came home. A Navy trial found out why.",
     P("tachibana", (0.42, 0.45), (1.1, 1.2), (0.5, 0.45)), section="hook",
     overlays={"hook": "Eight airmen captured. *Not one came home.*"}, captions=False, speed=1.3)
beat(B, "strike", "February 1945. American carrier planes struck the island, during the invasion of Iwo Jima. Several were shot down.",
     V("coast", (0.5, 0.5), (1.0, 1.08)), overlays={"stamp": "February 1945"}, section="story")
beat(B, "eight", "Eight airmen were captured on and around the island. One was Warren Vaughn, a Marine pilot from Texas.",
     T("Eight airmen", "Captured on and around Chichi Jima"))
beat(B, "shelter", "The trial record says the island's commander, General Tachibana, ordered that two of them get no shelter, food nor water.",
     C("doc_shelter", "U.S. v. Tachibana et al., Navy war crimes trial, Guam, 1946 (National Archives)"))
beat(B, "killed", "One by one, all eight were killed.", V("harbour", (0.5, 0.5), (1.0, 1.08)))
beat(B, "flesh", "And the record says officers ate the flesh of some of the dead.", V("boats", (0.5, 0.5), (1.0, 1.06)))
beat(B, "cover", "After the surrender, the officers claimed the airmen had died in air raids. When a Marine board questioned them, they confessed.",
     V("ladder", (0.45, 0.4), (1.05, 1.12)), overlays={"stamp": "September 1945"}, section="trial")
beat(B, "law", "There was no law against cannibalism. So the Navy charged it as preventing honorable burial.",
     C("doc_revolting", "Prosecution's opening statement, Guam, 1946 (National Archives)"))
beat(B, "hanged", "General Tachibana and Major Matoba were hanged on Guam.", C("guam", "The Navy's war crimes court on Guam"))
beat(B, "bush", "Months earlier, a young pilot was shot down over the same island, and rescued. His name was George Bush.",
     P("rescue", (0.5, 0.45), (1.05, 1.15)), section="end")
beat(B, "close", "Those were the airmen of Chichi Jima.", P("portrait", (0.5, 0.3), (1.15, 1.25), (0.5, 0.42)))
beat(B, "cta", "Follow WWII Frontlines for more.", {"kind": "endcard"}, section="cta", captions=False)

spec_b = spec(
    "reel-wwf-chichi-airmen", "8 Airmen Were Captured on Chichi Jima. None Came Home", B,
    {
        "coast": {"file": "chichi_bombing_1944.mp4", "commons": BOMB, "start": 19.5, "dur": 10},
        "harbour": {"file": "chichi_b24_1945.mp4", "commons": B24B, "start": 175.6, "dur": 3.3, "speed": 0.5},
        "boats": {"file": "chichi_surrender_b.mp4", "commons": SURB, "start": 317.5, "dur": 8},
        "ladder": {"file": "chichi_surrender_a.mp4", "commons": SURA, "start": 143.0, "dur": 11.8},
    },
    {"tachibana": "Yoshio Tachibana surrender.jpg", "guam": "Former Japanese Admiral Chuichi Hara at the War Crimes Trial Building, 1948.jpg", "rescue": "George Bush being rescued by the submarine, the U.S.S. Finback (NARA 186382)",
     "portrait": "George Bush, Navy pilot during World War II - NARA - 186380.tif",
     "doc_shelter": "U.S. v. Tachibana et al., record", "doc_revolting": "U.S. v. Tachibana et al., prosecution's opening"},
    SOURCES,
    [
        {"beat": "hook", "sources": ["TRIAL", "BRADLEY", "IWG"], "note": "Eight airmen captured on and around Chichi Jima and killed there."},
        {"beat": "strike", "sources": ["TRIAL", "BRADLEY"], "note": "18-23 Feb 1945 strikes covering Iwo Jima."},
        {"beat": "eight", "sources": ["TRIAL", "BRADLEY"], "note": "2nd Lt Warren Earl Vaughn, USMC, of Childress, Texas."},
        {"beat": "shelter", "sources": ["TRIAL"], "note": "Verbatim: ordered not to give the prisoners (Hall and Mershon) shelter, food nor water."},
        {"beat": "killed", "sources": ["TRIAL", "BRADLEY"]},
        {"beat": "flesh", "sources": ["TRIAL", "TIME", "BRADLEY"], "note": "Said in words only, no images."},
        {"beat": "cover", "sources": ["TRIAL", "IWG"], "note": "Cover story (air raids / sent to Japan); Rixey board from 21 Dec 1945; Horie and Matoba admitted, Jan 1946."},
        {"beat": "law", "sources": ["TRIAL", "IWG"], "note": "Charged as prevention of honorable burial."},
        {"beat": "hanged", "sources": ["TRIAL", "BRADLEY"], "note": "Tachibana hanged 24 Sept 1947 on Guam; Matoba also hanged (date not said)."},
        {"beat": "bush", "sources": ["AAR", "FINBACK"]},
    ],
)

for s in (spec_a, spec_b):
    (DATA / f"{s['id']}.json").write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(s["id"], len(s["beats"]), "beats,", sum(len(b["text"].split()) for b in s["beats"]), "words")
