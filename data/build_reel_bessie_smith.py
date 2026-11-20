"""Builds data/reel-bessie-smith.json: a ~3-minute film-clip reel about Bessie Smith.

Every fact lists at least two sources in "facts". Images and film: public domain or CC0 only
(see public/pd/reel-bessie-smith/credits.json and clips/clips.json).
Film: St. Louis Blues (1929), her only film, public domain on Wikimedia Commons (Library of Congress copy).
Voice: set VOICE below. "kokoro" is free; "elevenlabs" (Andrew, Flash) is paid: ask first.
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).with_name("reel-bessie-smith.json")
VOICE = sys.argv[1] if len(sys.argv) > 1 else "kokoro"

ASSETS = {
    "vv1936": "File:Bessie Smith (1936) by Carl Van Vechten.jpg",
    "vv72": "File:Portrait of Bessie Smith LCCN2004663572.jpg",
    "vv75": "File:Bessie Smith, three-quarter length portrait, standing, facing front, with left hand raised LCCN2004663575.jpg",
    "feathers": "File:Portrait of Bessie Smith holding feathers LCCN2004663573.jpg",
    "young": "File:Bessiesmith3.jpg",
    "rainey": "File:Ma Rainey, 1923.jpg",
    "ad1923": "File:Columbia Records ad, Chicago Tribune, May 19, 1923.jpg",
    "poster": "File:St. Louis Blues (poster for 1929 film).jpg",
    "grave": "File:Bessie Smith grave.jpg",
    "joplin": "File:Janis Joplin seated 1970.JPG",
}

STL = "File:St. Louis Blues.webm"
s = lambda start, dur, **o: {"file": "St._Louis_Blues.webm", "commons": STL, "start": start, "dur": dur, **o}
CLIPS = {
    "close1": s(423, 6),
    "close2": s(429, 5),
    "close3": s(435.5, 4),
    "argue": s(336, 8),
    "floor": s(410, 8),
    "bar3": s(512.5, 7.5),
    "bar8": s(608, 8),
    "bar8b": s(622, 8),
    "bar12": s(885, 10),
    "bar13": s(900, 9),
    "bar14": s(929.5, 6.5),
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


b("hook", "She was the biggest blues star in America. Then she lay in an unmarked grave for thirty-three years.",
  P("vv1936", (0.5, 0.3), (1.0, 1.06), (0.5, 0.4)), section="hook",
  overlays={"hook": "The biggest blues star in America. *Then 33 years in an unmarked grave.*"}, captions=False, speed=1.3)
b("name", "Her name was Bessie Smith. They called her the Empress of the Blues.", V("close1", (0.5, 0.4)), section="who")
b("born", "She was born in Chattanooga, Tennessee. Before she was nine, both of her parents were dead.",
  P("young", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)), overlays={"pin": {"label": "Chattanooga, Tennessee"}}, section="story")
b("busk", "So she sang on the street corners for coins, while her brother Andrew played the guitar.",
  C("vv72", "Bessie Smith, 1936"))
b("rainey", "In 1912 she joined a traveling show as a dancer. The star singer in that company was Ma Rainey, the Mother of the Blues.",
  C("rainey", "Ma Rainey, 1923"), overlays={"stamp": "1912"})
b("columbia", "In 1923, Columbia Records signed her. Her first record, Downhearted Blues, sold about 780,000 copies in six months.",
  C("ad1923", "Columbia Records advertisement, 1923"), overlays={"stamp": "1923"}, section="fame")
b("paid", "She became the highest-paid Black entertainer of her day, earning up to two thousand dollars a week.",
  V("bar8", (0.62, 0.35)))
b("car", "She toured the South in her own private railroad car.", P("feathers", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)))
b("tent", "In July 1927, she was singing in a tent in Concord, North Carolina. Hooded Klansmen came to pull the tent down.",
  T("July 1927", "Concord, North Carolina"), section="klan")
b("faced", "Bessie walked out to them alone. She cursed them and told them to leave. They ran.",
  V("argue", (0.3, 0.3), (1.0, 1.06), (0.5, 0.4)))
b("finished", "Then she went back inside and finished the show.", V("bar3", (0.62, 0.35)))
b("film", "In 1929 she made her only film, St. Louis Blues. This is it.",
  C("poster", "St. Louis Blues, 1929"), overlays={"stamp": "1929"}, section="film")
b("film2", "She played a woman left by the man she loved, singing her heart out at a bar.", V("close2", (0.5, 0.4)))
b("crash1", "Then the Depression hit. Record sales collapsed, and in 1931 Columbia let her go. She had to sell her railroad car.",
  V("floor", (0.35, 0.45), (1.0, 1.06), (0.5, 0.5)), section="fall")
b("comeback", "By the mid-1930s she was fighting her way back, singing swing in New York.", V("bar12", (0.62, 0.35)))
b("crash", "On September 26th, 1937, she was riding down Highway 61 in Mississippi. Her car slammed into the back of a truck.",
  T("September 26, 1937", "Highway 61, Mississippi"), section="crash")
b("arm", "Her right arm was almost torn off. She was taken to the Black hospital in Clarksdale, and died that morning.",
  P("vv75", (0.5, 0.25), (1.05, 1.15), (0.5, 0.4)))
b("myth", "For years, people said a white hospital had turned her away. That story was false. But what came next was true.",
  T("A myth", "a white hospital did not turn her away"))
b("funeral", "In Philadelphia, ten thousand people filed past her coffin.",
  P("vv1936", (0.5, 0.3), (1.15, 1.25), (0.5, 0.42)), overlays={"stamp": "October 1937"}, section="grave")
b("nostone", "But her grave got no headstone. Her estranged husband, Jack Gee, reportedly pocketed money raised to buy one.",
  T("No headstone", "Mount Lawn Cemetery, Pennsylvania"))
b("years", "For thirty-three years, the Empress of the Blues lay in an unmarked grave.", V("close3", (0.5, 0.4)))
b("joplin", "Then in 1970, the rock star Janis Joplin, who idolized her, split the cost of a stone with Juanita Green, who had done housework for Bessie as a girl.",
  C("joplin", "Janis Joplin, 1970"), overlays={"stamp": "August 1970"})
b("stone", "It reads: The greatest blues singer in the world will never stop singing.",
  C("grave", "Bessie Smith's headstone, Mount Lawn Cemetery"))
b("janis", "Two months later, Janis Joplin was dead too.", T("October 1970", "Janis Joplin dies at 27"))
b("close", "That was Bessie Smith.", V("bar14", (0.62, 0.35)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

VOICES = {
    "kokoro": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "elevenlabs": {"engine": "elevenlabs", "voiceId": "gUABw7pXQjhjt0kNFBTF", "voiceName": "Andrew - Smooth audio books",
                   "model": "eleven_flash_v2_5", "stability": 0.6, "similarity": 0.75, "style": 0, "speed": 1.05, "seed": 1234,
                   "leadInSeconds": 0, "sectionGapSeconds": 0.5},
}

S = lambda u: {"url": u}
spec = {
    "id": "reel-bessie-smith",
    "title": "33 Years in an Unmarked Grave",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": VOICES[VOICE],
    "pronounce": {"St. Louis": "Saint Lewis", "Janis": "Jan-iss", "Concord": "Conkerd"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": {
        "WIKI": S("https://en.wikipedia.org/wiki/Bessie_Smith"),
        "ENC": S("https://www.encyclopedia.com/people/literature-and-arts/music-popular-and-jazz-biographies/bessie-smith"),
        "NPS": S("https://www.nps.gov/locations/lowermsdeltaregion/bessie-smith.htm"),
        "AH": S("https://www.americanheritage.com/untitled-230"),
        "CHARLOTTE": S("https://www.aol.com/news/push-commemorate-night-bessie-smith-095600223.html"),
        "UDISC": S("https://www.udiscovermusic.com/stories/janis-joplin-bessie-smith-headstone/"),
        "CURRENT": S("https://thecurrent.org/feature/2017/08/04/today-in-music-history-janis-joplin-bought-a-headstone-for-bessie-smith"),
        "DHB": S("https://en.wikipedia.org/wiki/Downhearted_Blues"),
        "FILM": S("https://commons.wikimedia.org/wiki/File:St._Louis_Blues.webm"),
        "JOPLIN": S("https://en.wikipedia.org/wiki/Janis_Joplin"),
        "PSAUDIO": S("https://psaudio.com/article/bessie-smith-part-2/"),
        "ROCKHALL": S("https://rockhall.com/wp-content/uploads/2024/03/Bessie_Smith_1989.pdf"),
    },
    "facts": [
        {"beat": "born", "sources": ["WIKI", "ENC", "NPS"], "note": "Birth year disputed (1892/1894): not said."},
        {"beat": "busk", "sources": ["WIKI", "ENC"]},
        {"beat": "rainey", "sources": ["WIKI", "ENC", "NPS"]},
        {"beat": "columbia", "sources": ["ENC", "NPS", "DHB"], "note": "Some sources say 750,000; 'about 780,000' per ENC/NPS/DHB."},
        {"beat": "paid", "sources": ["WIKI", "NPS", "ENC"]},
        {"beat": "car", "sources": ["WIKI", "ENC"]},
        {"beat": "tent", "sources": ["AH", "CHARLOTTE", "ENC"]},
        {"beat": "faced", "sources": ["AH", "CHARLOTTE"], "note": "From Chris Albertson's biography; ENC says 'reportedly'."},
        {"beat": "finished", "sources": ["AH", "CHARLOTTE"]},
        {"beat": "film", "sources": ["WIKI", "ENC", "FILM"]},
        {"beat": "crash1", "sources": ["ENC", "PSAUDIO", "ROCKHALL"]},
        {"beat": "comeback", "sources": ["ENC", "WIKI"]},
        {"beat": "crash", "sources": ["WIKI", "NPS", "ENC"]},
        {"beat": "arm", "sources": ["WIKI", "NPS"]},
        {"beat": "myth", "sources": ["WIKI", "ENC"]},
        {"beat": "funeral", "sources": ["WIKI", "ENC"]},
        {"beat": "nostone", "sources": ["WIKI", "UDISC"]},
        {"beat": "years", "sources": ["ENC", "UDISC"]},
        {"beat": "joplin", "sources": ["WIKI", "UDISC", "CURRENT"]},
        {"beat": "stone", "sources": ["ENC", "UDISC"]},
        {"beat": "janis", "sources": ["UDISC", "JOPLIN"]},
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
text = " ".join(x["text"] for x in B)
print(f"{len(B)} beats, {len(text.split())} words, {len(text)} characters, voice {VOICE}")
