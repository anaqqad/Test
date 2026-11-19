"""Builds data/reel-lena-horne.json: a ~3-minute film-clip reel about Lena Horne.

Every fact lists at least two sources in "facts". Images and film: public domain only
(see public/pd/reel-lena-horne/credits.json and clips/clips.json).
Film: The Duke Is Tops (1938) and Boogie Woogie Dream (1944), both public domain on Wikimedia Commons.
Voice: set VOICE below. "kokoro" is free; "elevenlabs" (Andrew, Flash) is paid: ask first.
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).with_name("reel-lena-horne.json")
VOICE = sys.argv[1] if len(sys.argv) > 1 else "kokoro"

ASSETS = {
    "p1941": "File:Lena Horne - 1941.jpg",
    "vv1941": "File:Portrait of Lena Horne LCCN2004663037.jpg",
    "p1946": "File:Lena Horne, 1946.jpg",
    "gottlieb": "File:(Portrait of Lena Horne, New York, N.Y., between 1946 and 1948) (LOC) (4843132965).jpg",
    "hayton": "File:(Portrait of Lena Horne and Lennie Hayton, New York, N.Y., between 1946 and 1948) (LOC) (5354168293).jpg",
    "stormy": "File:Stormy Weather (1943 film poster).jpg",
    "stormylc": "File:Stormy Weather (1943 lobby card - Horne & Robinson).jpg",
    "cabin": "File:Cabin in the Sky (1943) 1.jpg",
    "tuskegee": "File:Lena Horne with Tuskegee airmen.png",
    "march": "File:Civil Rights March on Washington, D.C. (Actor Lena Horne, a close-up view.) - NARA - 542057.tif",
    "p1955": "File:Lena Horne 1955.JPG",
    "p1947": "File:Lena Horne 1947.JPG",
}

DUKE = "File:The Duke is Tops (1938).webm"
BWD = "File:Boogie Woogie Dream (1944).webm"
d = lambda start, dur, **o: {"file": "The_Duke_is_Tops_(1938).webm", "commons": DUKE, "start": start, "dur": dur, **o}
CLIPS = {
    "stage": d(430, 8),
    "sing1": d(446, 8),
    "sing2": d(467.5, 6.5),
    "sing3": d(479, 8),
    "sing4": d(488, 4.5),
    "sing5": d(497, 4.5),
    "cooper": d(864, 10),
    "cooper2": d(886, 9),
    "bwd1": {"file": "Boogie_Woogie_Dream_(1944).webm", "commons": BWD, "start": 249, "dur": 3, "speed": 0.6},
    "bwd2": {"file": "Boogie_Woogie_Dream_(1944).webm", "commons": BWD, "start": 262, "dur": 4.8},
}


def V(clip, focus, zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap):
    return {"kind": "card", "image": img, "caption": cap}


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


B = []


def b(id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


b("hook", "Hollywood made her a star. Then it filmed her songs so that theaters in the South could cut her out of the movie.",
  P("p1946", (0.5, 0.3), (1.0, 1.06), (0.5, 0.4)), section="hook",
  overlays={"hook": "Hollywood made her a star. *Then filmed her so the South could cut her out.*"}, captions=False, speed=1.3)
b("name", "Her name was Lena Horne.", V("sing1", (0.5, 0.35)), section="who")
b("born", "She was born in Brooklyn in 1917. Her father left when she was three, and she was raised mostly by her grandparents.",
  P("p1941", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)), overlays={"pin": {"label": "Brooklyn, New York"}}, section="story")
b("family", "Her family were middle-class Black New Yorkers, active in the NAACP.", P("p1947", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)))
b("cotton", "At sixteen she was dancing in the chorus at Harlem's Cotton Club. Black performers on stage, a whites-only audience.",
  V("stage", (0.5, 0.3)), overlays={"stamp": "1933"})
b("band", "She sang with Noble Sissle's orchestra, then toured with Charlie Barnet's white band.",
  V("sing2", (0.5, 0.32)))
b("cafe", "In 1941 she sang at Cafe Society, New York's first integrated nightclub.", V("cooper2", (0.62, 0.32)))
b("duke", "In 1938 she starred in her first feature film, The Duke Is Tops, made for Black audiences.",
  V("cooper", (0.62, 0.32)), overlays={"lowerThird": {"name": "The Duke Is Tops", "sub": "1938"}})
b("mgm", "In 1942, MGM signed her to a seven-year contract, almost unheard of for a Black performer at a major studio. The deal said she would not play maids.",
  C("vv1941", "Lena Horne, 1941"), overlays={"stamp": "1942"}, section="mgm")
b("naacp", "The NAACP saw her as a test case for how Hollywood would treat Black women.",
  T("A test case", "for Hollywood"))
b("cut", "But MGM rarely put her in the story. She sang in her own scenes, apart from the white stars.",
  V("sing3", (0.5, 0.32)))
b("south", "That way, theaters in the South could cut her out, and some did.",
  T("Cut out", "of films shown in the South"))
b("stormy", "On loan to another studio, she starred in Stormy Weather in 1943. The title song became hers for life.",
  C("stormy", "Stormy Weather, 1943"), overlays={"stamp": "1943"})
b("war", "During the war, she sang for the troops. At one Army camp, German prisoners of war were seated in front of the Black soldiers.",
  C("tuskegee", "Lena Horne with Tuskegee airmen, 1945"), section="war")
b("walked", "So she walked off the stage, past the prisoners, and sang to the Black soldiers in the back.",
  V("sing4", (0.5, 0.32)))
b("julie", "When MGM remade Show Boat, the mixed-race role of Julie went to Ava Gardner, a white actress.",
  P("gottlieb", (0.5, 0.35), (1.05, 1.15), (0.5, 0.45)), section="after")
b("married", "In 1947 she married Lennie Hayton, a white music director. They wed in Paris, because their marriage was against the law in California.",
  C("hayton", "Lena Horne and Lennie Hayton, about 1947"))
b("blacklist", "In the early 1950s, she was blacklisted for her political ties.",
  P("p1955", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)), overlays={"stamp": "1950s"})
b("nightclubs", "So she went back to nightclubs, and became one of the biggest singers in America.",
  V("bwd2", (0.55, 0.35)))
b("jamaica", "In 1957 she starred on Broadway, in the musical Jamaica.", P("p1955", (0.5, 0.3), (1.2, 1.3), (0.5, 0.42)), overlays={"stamp": "1957"})
b("march", "In 1963 she marched on Washington for civil rights.",
  C("march", "Lena Horne at the March on Washington, 1963"), overlays={"stamp": "August 28, 1963"}, section="rights")
b("losses", "Then, within two years, she lost her son, her father, and her husband.",
  T("1970 to 1971", "her son, her father, her husband"))
b("broadway", "In 1981, at sixty-three, she opened her own show on Broadway, Lena Horne: The Lady and Her Music. It won her a special Tony and two Grammys.",
  V("sing5", (0.5, 0.32)), overlays={"stamp": "1981"}, section="end")
b("kennedy", "In 1984 she received the Kennedy Center Honors.", T("Kennedy Center Honors", "1984"))
b("death", "Lena Horne died on May 9th, 2010. She was 92.",
  P("vv1941", (0.5, 0.3), (1.15, 1.25), (0.5, 0.42)), overlays={"stamp": "May 9, 2010"})
b("close", "That was Lena Horne.", V("bwd1", (0.55, 0.35)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

VOICES = {
    "kokoro": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "elevenlabs": {"engine": "elevenlabs", "voiceId": "gUABw7pXQjhjt0kNFBTF", "voiceName": "Andrew - Smooth audio books",
                   "model": "eleven_flash_v2_5", "stability": 0.6, "similarity": 0.75, "style": 0, "speed": 1.05, "seed": 1234,
                   "leadInSeconds": 0, "sectionGapSeconds": 0.5},
}

S = lambda u: {"url": u}
spec = {
    "id": "reel-lena-horne",
    "title": "Filmed So the South Could Cut Her Out",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": VOICES[VOICE],
    "pronounce": {"Sissle": "Sissel", "Hayton": "Hay-ton"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": {
        "WIKI": S("https://en.wikipedia.org/wiki/Lena_Horne"),
        "ENC": S("https://www.encyclopedia.com/people/literature-and-arts/music-popular-and-jazz-biographies/lena-horne"),
        "TCM": S("https://www.tcm.com/articles/featured-actors/021865/lena-horne-goddess-reclaimed"),
        "HEINZ": S("https://www.heinzhistorycenter.org/blog/western-pennsylvania-history-words-and-music-a-holiday-turning-point/"),
        "THR": S("https://www.hollywoodreporter.com/lifestyle/lifestyle-news/lena-horne-book-excerpt-actress-singer-mgm-1235613032/"),
        "SCPR": S("https://www.southcarolinapublicradio.org/2023-10-31/a-new-book-tells-the-life-story-of-screen-and-song-legend-lena-horne"),
        "ARMY": S("https://www.army.mil/article/217981/fort_knox_general_club_director_host_black_entertainers_ease_tensions_in_pre_integrated_army"),
        "NPS": S("https://home.nps.gov/features/malu/feat0002/wof/Lena_Horne.htm"),
        "DUKE": S("https://commons.wikimedia.org/wiki/File:The_Duke_is_Tops_(1938).webm"),
        "NARA": S("https://commons.wikimedia.org/wiki/File:Civil_Rights_March_on_Washington,_D.C._(Actor_Lena_Horne,_a_close-up_view.)_-_NARA_-_542057.tif"),
    },
    "facts": [
        {"beat": "born", "sources": ["WIKI", "ENC"]},
        {"beat": "cotton", "sources": ["WIKI", "ENC", "TCM"]},
        {"beat": "band", "sources": ["WIKI", "ENC"]},
        {"beat": "duke", "sources": ["TCM", "DUKE"]},
        {"beat": "mgm", "sources": ["ENC", "TCM", "SCPR"], "note": "Seven-year contract (ENC, TCM); no maid/servant roles (TCM, SCPR)."},
        {"beat": "naacp", "sources": ["THR", "SCPR"]},
        {"beat": "cut", "sources": ["WIKI", "TCM"]},
        {"beat": "south", "sources": ["WIKI", "TCM", "HEINZ"]},
        {"beat": "stormy", "sources": ["WIKI", "TCM", "ENC"]},
        {"beat": "war", "sources": ["ARMY", "NPS", "WIKI"], "note": "Venue disputed (Fort Riley vs Camp Robinson): said as 'one Army camp'."},
        {"beat": "walked", "sources": ["ARMY", "NPS"]},
        {"beat": "julie", "sources": ["WIKI", "TCM"]},
        {"beat": "married", "sources": ["ENC", "WIKI"]},
        {"beat": "blacklist", "sources": ["WIKI", "ENC"]},
        {"beat": "nightclubs", "sources": ["TCM", "WIKI"]},
        {"beat": "march", "sources": ["WIKI", "ENC", "NARA"]},
        {"beat": "losses", "sources": ["ENC", "WIKI"]},
        {"beat": "broadway", "sources": ["WIKI", "ENC"]},
        {"beat": "death", "sources": ["WIKI", "TCM"]},
        {"beat": "family", "sources": ["ENC", "WIKI"]},
        {"beat": "cafe", "sources": ["WIKI", "ENC"]},
        {"beat": "jamaica", "sources": ["TCM", "ENC", "WIKI"]},
        {"beat": "kennedy", "sources": ["WIKI", "ENC"]},
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
text = " ".join(x["text"] for x in B)
print(f"{len(B)} beats, {len(text.split())} words, {len(text)} characters, voice {VOICE}")
