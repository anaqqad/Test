"""Builds data/reel-bert-williams.json: a ~3-minute film-clip reel about Bert Williams.

Every fact lists at least two sources in "facts". Images and film: public domain only
(see public/pd/reel-bert-williams/credits.json and clips/clips.json).
Film: A Natural Born Gambler (Biograph, 1916), public domain on Wikimedia Commons; it holds his famous
silent poker routine. Download it to a scratch folder as "gambler.webm" before running cut_clips.py.
Voice: set VOICE below. "kokoro" is free; "elevenlabs" (Andrew, Flash) is paid: ask first.
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).with_name("reel-bert-williams.json")
VOICE = sys.argv[1] if len(sys.argv) > 1 else "kokoro"

ASSETS = {
    "suit1921": "File:BertWilliamsPhotoPortraitWithCigarette.jpg",
    "suit1921b": "File:Bert Williams -31 LCCN2004674530.jpg",
    "cork": "File:Bert Williams blackface 2.jpg",
    "young1896": "File:BertWilliams1896.jpg",
    "young1902": "File:Bert Williams, stage actor (SAYRE 11054).jpg",
    "ww": "File:Maud Cuney Hare-williams and walker-159.jpg",
    "coons": "File:Williams and Walker poster 1903.jpg",
    "dahomey": "File:In Dahomey 1903.jpg",
    "jonah": "File:WilliamsWalkerJohnahMan.jpg",
    "palace": "File:Charles B. Falls - Bert Williams Palace Theatre poster.jpg",
    "follies1919": "File:Johnny Dooley, Eddie Cantor, Gus Van, Bert Williams, Joe Schenck, Eddie Dowling, & Ray Dooley, Follies of 1919.jpg",
    "uniform": "File:1916 United States Army Captain Bert Williams, portrait, facing right, singing a psalm at the first regimental open air service for the 15th Regiment of the New York National Guard - LCCN96521643 (cropped).jpg",
    "tophat": "File:BertWilliamsBlackfaceTophatSmile.jpg",
}

NBG = "File:A Natural Born Gambler (1916).webm"
g = lambda start, dur, **o: {"file": "gambler.webm", "commons": NBG, "start": start, "dur": dur, **o}
CLIPS = {
    "bar1": g(68, 8),
    "bar2": g(78, 12),
    "bar3": g(96, 8),
    "court1": g(1110, 12),
    "court3": g(1164, 5),
    "cell": g(1205, 13),
    "pk1": g(1223, 13),
    "pk2": g(1239, 11),
    "pk3": g(1251, 7),
    "pk4": g(1257, 11),
    "pk5": g(1269, 17),
    "pk6": g(1287, 13),
    "pk7": g(1303, 13),
    "pk8": g(1317, 18),
    "pk9": g(1337, 13),
    "pk10": g(1350, 6),
}


def V(clip, focus, zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap):
    return {"kind": "card", "image": img, "caption": cap}


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


PK = (0.7, 0.3)   # Bert's face in the poker routine (he stands right of centre)
B = []


def b(id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


b("hook", "He was the highest-paid Black entertainer in America. And every night, he had to paint his face black to go on stage.",
  P("suit1921", (0.5, 0.22), (1.0, 1.06), (0.5, 0.36)), section="hook",
  overlays={"hook": "America's highest-paid Black star. *Every night, he had to black up.*"}, captions=False, speed=1.3)
b("name", "His name was Bert Williams. W. C. Fields called him the funniest man he ever saw, and the saddest man he ever knew.",
  V("pk4", PK), section="who")
b("born", "He was born in Nassau, in the Bahamas, in 1874, and grew up in California.",
  P("young1896", (0.5, 0.22), (1.05, 1.15), (0.5, 0.4)), overlays={"pin": {"label": "Nassau, Bahamas"}}, section="story")
b("walker", "In 1893, in a minstrel show in San Francisco, he met George Walker. Together they became the most famous Black performers in the world.",
  C("ww", "Bert Williams and George Walker"), overlays={"stamp": "1893"})
b("cork", "But on stage, they had to wear blackface. Bert was light-skinned. Before every show, he blackened his face with burnt cork.",
  P("cork", (0.4, 0.4), (1.05, 1.15), (0.45, 0.5)), section="mask")
b("billing", "They even called themselves Two Real Coons, to set themselves apart from the white men in blackface.",
  C("coons", "Williams and Walker poster, 1903"))
b("dahomey", "In 1903, their show In Dahomey became the first all-Black musical at a major Broadway theater. They even played Buckingham Palace.",
  C("dahomey", "In Dahomey, 1903"), overlays={"stamp": "1903"}, section="fame")
b("seats", "Yet inside that theater, Black fans had to sit in a separate section.", V("bar3", (0.65, 0.3)))
b("walkerdies", "Then George Walker fell ill. He died in 1911, and Bert was on his own.", C("jonah", "Williams and Walker"))
b("ziegfeld", "In 1910, Florenz Ziegfeld hired him for the Follies, the biggest show on Broadway. Bert was the only Black star in an all-white cast.",
  V("bar1", (0.65, 0.3)), overlays={"stamp": "1910"}, section="follies")
b("ultimatum", "Cast members demanded that he be fired. Ziegfeld refused. He reportedly told them, I can replace every one of you, except him.",
  V("court1", (0.25, 0.3), (1.0, 1.06), (0.4, 0.4)))
b("star", "Bert became the star of the show. His sad song Nobody became his signature.", V("pk1", PK))
b("paid", "He was the highest-paid Black entertainer in America.", C("palace", "Palace Theatre poster, about 1918"))
b("elevator", "But when he walked into a hotel, he had to ride the freight elevator.",
  P("suit1921b", (0.5, 0.2), (1.05, 1.15), (0.5, 0.36)), section="insult")
b("applause", "He told his friend Eddie Cantor: It wouldn't be so bad, if I didn't still hear the applause ringing in my ears.",
  C("follies1919", "Ziegfeld Follies of 1919, with Eddie Cantor"))
b("bar", "Once, a bartender told him a drink would cost fifty dollars. Bert laid a pile of big bills on the bar, and kept ordering.",
  V("bar2", (0.65, 0.3)))
b("gambler", "In 1916 he filmed his famous poker routine. This is it. One man, no words, a whole card game in his face.",
  V("pk2", PK), overlays={"stamp": "1916"}, section="film")
b("strike", "In 1919, Broadway's actors went on strike, and the whole cast walked out. Nobody told Bert. He walked into an empty theater.",
  V("court3", (0.25, 0.3), (1.0, 1.06), (0.3, 0.4)), section="alone")
b("collapse", "In February 1922, sick with pneumonia, he collapsed on stage in Detroit. At first, the audience thought it was part of the act.",
  T("February 1922", "Detroit, Michigan"), section="end")
b("last", "Backstage, he reportedly said: That's a nice way to die. They was laughing when I made my last exit.", V("pk6", PK))
b("died", "On March 4th, 1922, Bert Williams died in New York.", P("uniform", (0.45, 0.3), (1.05, 1.15), (0.45, 0.42)))
b("funeral", "Thousands came to see his coffin. He was the first Black man buried with Masonic honors in New York.",
  P("young1902", (0.5, 0.3), (1.05, 1.15), (0.5, 0.42)))
b("essay", "He once wrote: I have never been able to discover that there was anything disgraceful in being a colored man. But I have often found it inconvenient, in America.",
  V("pk9", PK), section="legacy")
b("close", "That was Bert Williams.", P("suit1921", (0.5, 0.22), (1.1, 1.2), (0.5, 0.36)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

VOICES = {
    "kokoro": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "elevenlabs": {"engine": "elevenlabs", "voiceId": "gUABw7pXQjhjt0kNFBTF", "voiceName": "Andrew - Smooth audio books",
                   "model": "eleven_flash_v2_5", "stability": 0.6, "similarity": 0.75, "style": 0, "speed": 1.05, "seed": 1234,
                   "leadInSeconds": 0, "sectionGapSeconds": 0.5},
}

S = lambda u: {"url": u}
SOURCES = {
    "WIKI": S("https://en.wikipedia.org/wiki/Bert_Williams"),
    "ENC": S("https://www.encyclopedia.com/people/literature-and-arts/theater-biographies/bert-williams"),
    "PBS": S("https://www.pbs.org/wnet/broadway/stars/bert-williams/"),
    "UA": S("https://sites.arizona.edu/vaudeville/bert-williams-vaudevilles-biggest-black-superstar-by-david-soren"),
    "FASSLER": S("https://ronfassler.org/post/2418/A-COMEDIAN-S-TRAGEDY-THE-STORY-OF-BERT-WILLIAMS"),
    "TMANIA": S("https://www.theatermania.com/news/bert-williams-americas-first-black-star-part-ii_70442"),
    "FIELDS": S("https://rd.springer.com/chapter/10.1057/978-1-349-94986-1_9"),
    "NORMAN": S("https://normanstudios.org/blog/2017/01/26/the-iconic-mr-nobody-an-analysis-of-silent-film-legend-bert-williams/"),
    "WHIP": S("https://cablecarguy.blogspot.com/2022/03/bert-williams-100-years-march-4-2022.html"),
    "FILM": S("https://commons.wikimedia.org/wiki/File:A_Natural_Born_Gambler_(1916).webm"),
}
FACTS = [
    {"beat": "hook", "sources": ["WIKI", "UA", "ENC"]},
    {"beat": "name", "sources": ["WIKI", "ENC", "PBS", "TMANIA"]},
    {"beat": "born", "sources": ["WIKI", "ENC", "PBS"], "note": "ENC notes Antigua as an unconfirmed alternative birthplace."},
    {"beat": "walker", "sources": ["WIKI", "ENC", "PBS"]},
    {"beat": "cork", "sources": ["WIKI", "UA", "ENC"]},
    {"beat": "billing", "sources": ["WIKI", "ENC"]},
    {"beat": "dahomey", "sources": ["WIKI", "ENC", "PBS"], "note": "Palace year differs (1903 vs 1904): no year said."},
    {"beat": "seats", "sources": ["WIKI", "UA"]},
    {"beat": "walkerdies", "sources": ["WIKI", "PBS", "ENC"]},
    {"beat": "ziegfeld", "sources": ["WIKI", "UA", "FASSLER", "ENC"]},
    {"beat": "ultimatum", "sources": ["WIKI", "FASSLER"]},
    {"beat": "star", "sources": ["WIKI", "ENC", "TMANIA"]},
    {"beat": "paid", "sources": ["WIKI", "ENC"], "note": "ENC: salary reportedly exceeded the President's."},
    {"beat": "elevator", "sources": ["ENC", "PBS"]},
    {"beat": "applause", "sources": ["ENC", "PBS"]},
    {"beat": "bar", "sources": ["WIKI", "TMANIA"], "note": "Details differ (roll of hundreds / a $500 bill): kept general."},
    {"beat": "gambler", "sources": ["WIKI", "UA", "FASSLER", "FILM"]},
    {"beat": "strike", "sources": ["WIKI", "FIELDS", "NORMAN"]},
    {"beat": "collapse", "sources": ["WIKI", "ENC", "FASSLER"], "note": "Exact date differs (Feb 21/25/27): month only."},
    {"beat": "last", "sources": ["WIKI", "FASSLER"]},
    {"beat": "died", "sources": ["WIKI", "ENC", "PBS"], "note": "Age 46 or 47 differs: not said."},
    {"beat": "funeral", "sources": ["WIKI", "UA", "WHIP"], "note": "Crowd 5,000 (WIKI) vs 7,000 (WHIP): 'thousands'."},
    {"beat": "essay", "sources": ["WIKI", "ENC"]},
]

spec = {
    "id": "reel-bert-williams",
    "title": "He Had to Black Up Every Night",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": VOICES[VOICE],
    "pronounce": {"Nassau": "Nassaw", "Ziegfeld": "Zigfeld", "Florenz": "Florents", "Dahomey": "Da-homey"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": SOURCES,
    "facts": FACTS,
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
text = " ".join(x["text"] for x in B)
print(f"{len(B)} beats, {len(text.split())} words, {len(text)} characters, voice {VOICE}")
