"""Builds data/reel-jackie-robinson.json: a ~3-minute film-clip reel about Jackie Robinson.

Every fact lists at least two sources in "facts". Images: public domain / CC0 only
(see public/pd/reel-jackie-robinson/credits.json and clips/clips.json).
Film: The Jackie Robinson Story (1950), in which he plays himself; public domain on Wikimedia Commons
(File:The Jackie Robinson Story (1950).ogv). The black-and-white copy used for the cuts is the Internet Archive item
Jackie_Robinson_Story_The, file jrs.mp4 (640x480, the
source named on the Commons file page); save it as film.mp4 in a scratch folder before running cut_clips.py.
Colorized versions are NOT used (the colorization is a later work).
Voice: Kokoro am_michael (free).
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-jackie-robinson.json")

ASSETS = {
    "npg49": "File:Jackie Robinson, NPG 97 135.jpg",
    "mack49": "File:Mack and Jackie Robinson with their mother 1949.jpg",
    "bball": "File:Jackie Robinson basketball.jpg",
    "army": "File:Jackie Robinson in army uniform.jpg",
    "royals46": "File:Baseball. Jack Robinson BAnQ P48S1P12829.jpg",
    "hate": "File:Hate mail sent to Jackie Robinson.jpg",
    "mvp49": "File:Jackie Robinson 1949 National League MVP.jpg",
    "b54": "File:Jackie Robinson, Brooklyn Dodgers, 1954.jpg",
    "march63": "File:Civil Rights March on Washington, D.C. (Former National Baseball League player, Jackie Robinson with his son.) - NARA - 542024.tif",
    "family50": "File:Jackie, Rachel and Sharon Robinson 1950.jpg",
    "look55": "File:Jrobinson.jpg",
}

FILM = "File:The Jackie Robinson Story (1950).ogv"
f = lambda start, dur, **k: {"file": "film.mp4", "commons": FILM, "start": start, "dur": dur, **k}
CLIPS = {  # times in jrs.mp4 (each shot checked at 1 fps: his face is on screen throughout)
    "film_close": f(1008, 5),   # close-up in a light suit
    "army_film": f(736, 6),     # in Army uniform (right of frame)
    "field": f(816, 4),         # in uniform on the field
    "rickey": f(1357, 7),       # close-up in the meeting with Rickey
    "dodgers": f(4506, 4),      # close-up in a Dodgers uniform
    "abuse": f(3150, 7),        # close-up, eyes down
    "play": f(2869, 6),         # batting, Montreal uniform
    "dodgers2": f(3871, 5),     # Dodgers, on the field
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


b("hook", "He broke baseball's color line. But three years before, the Army put him on trial, for refusing to move to the back of a bus.",
  P("look55", (0.3, 0.38), (1.0, 1.06), (0.5, 0.42)), section="hook",
  overlays={"hook": "He broke baseball's color line. *First, the Army put him on trial.*"}, captions=False, speed=1.3)
b("name", "His name was Jackie Robinson. And in 1950, he played himself, in a movie about his own life.",
  V("film_close", (0.5, 0.3), (1.2, 1.28), (0.5, 0.32)), section="who")
b("born", "He was born in 1919 in Cairo, Georgia, the youngest of five children of sharecroppers. His father left the family.",
  T("1919", "Cairo, Georgia"), section="story")
b("pasadena", "His mother moved them all to Pasadena, California, and raised them on her own.",
  C("mack49", "Jackie and Mack Robinson with their mother, 1949"))
b("mack", "His older brother Mack won silver at the 1936 Olympics, in the 200 meters. Right behind Jesse Owens.",
  P("mack49", (0.5, 0.35), (1.1, 1.2), (0.5, 0.4)), overlays={"stamp": "1936"})
b("ucla", "Jackie went to UCLA, and became its first athlete to letter in four sports.",
  P("bball", (0.5, 0.25), (1.05, 1.15), (0.5, 0.35)))
b("army", "In 1942 he was drafted. The Army kept Black soldiers out of officer school, until the boxing champion Joe Louis protested. Jackie became a lieutenant.",
  V("army_film", (0.5, 0.3), (1.1, 1.18), (0.5, 0.34)), section="army")
b("bus", "Then, on July 6th, 1944, at an Army base in Texas, a bus driver ordered him to move to the back. He refused.",
  T("July 6, 1944", "Texas"), section="bus")
b("trial", "He was arrested and court-martialed. A panel of nine white officers heard the case. They found him not guilty.",
  C("army", "Lieutenant Jack Robinson"))
b("monarchs", "In 1945 he played for the Kansas City Monarchs, in the Negro leagues.",
  V("field", (0.5, 0.3), (1.0, 1.08), (0.5, 0.34)), overlays={"stamp": "1945"}, section="break")
b("rickey", "That August, Branch Rickey of the Brooklyn Dodgers called him in. He told Jackie he needed a player with guts enough not to fight back.",
  V("rickey", (0.5, 0.3), (1.1, 1.18), (0.5, 0.32)))
b("montreal", "Rickey signed him. In 1946 he played for the Montreal Royals, and led the whole league in hitting.",
  C("royals46", "Montreal Royals, 1946"), overlays={"stamp": "1946"})
b("debut", "Then, on April 15th, 1947, Jackie Robinson walked onto the field for the Brooklyn Dodgers. The color line was broken.",
  V("dodgers", (0.5, 0.3), (1.15, 1.22), (0.5, 0.32)), overlays={"stamp": "1947"}, section="debut")
b("abuse", "It was brutal. The Phillies manager and his players screamed racial slurs at him from the dugout.",
  V("abuse", (0.5, 0.3), (1.05, 1.12), (0.5, 0.34)), section="insult")
b("mail", "Hate mail poured in. So did death threats.", C("hate", "Hate mail sent to Jackie Robinson, 1947"))
b("held", "He did not fight back. He answered with his bat, and with his speed.", V("play", (0.5, 0.35), (1.0, 1.06), (0.5, 0.4)))
b("held2", "That season, he led the whole National League in stolen bases.", V("dodgers2", (0.5, 0.35), (1.0, 1.06), (0.5, 0.4)))
b("rookie", "That year, he won baseball's first Rookie of the Year award. In 1949 he was the league's Most Valuable Player.",
  C("mvp49", "National League MVP, 1949"), section="triumph")
b("series", "In 1955, the Dodgers won the World Series.", P("b54", (0.45, 0.28), (1.05, 1.15), (0.5, 0.36)), overlays={"stamp": "1955"})
b("hall", "In 1962 he was elected to the Hall of Fame, the first Black player ever inducted.", T("1962", "Hall of Fame"))
b("march", "He kept fighting off the field. In 1963 he marched on Washington, with his son beside him.",
  C("march63", "March on Washington, 1963"), section="later")
b("last", "In October 1972 he threw out the first pitch at the World Series. That day, he said he still wanted to see a Black manager in baseball.",
  P("look55", (0.3, 0.38), (1.1, 1.2), (0.5, 0.42)), section="end")
b("died", "Nine days later, he died of a heart attack. He was 53.", C("family50", "With Rachel and Sharon, 1950"))
b("fortytwo", "In 1997, baseball retired his number, 42, for every team. Every April 15th, every player wears it.",
  T("42", "Retired by every team"), section="legacy")
b("close", "That was Jackie Robinson.", P("npg49", (0.5, 0.3), (1.1, 1.18), (0.5, 0.38)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
SOURCES = {
    "WP": S("https://en.wikipedia.org/wiki/Jackie_Robinson"),
    "SABR": S("https://sabr.org/bioproj/person/jackie-robinson/"),
    "HOF": S("https://baseballhall.org/hall-of-famers/robinson-jackie"),
    "NARA": S("https://www.archives.gov/publications/prologue/2008/spring/robinson.html"),
    "WPMACK": S("https://en.wikipedia.org/wiki/Mack_Robinson_(athlete)"),
    "MLB": S("https://www.mlb.com/news/jackie-robinson-day"),
    "NARAPHOTO": S("https://catalog.archives.gov/id/542024"),
    "FILM": S("https://commons.wikimedia.org/wiki/File:The_Jackie_Robinson_Story_(1950).ogv"),
}
FACTS = [
    {"beat": "hook", "sources": ["WP", "SABR", "NARA"]},
    {"beat": "name", "sources": ["FILM", "WP"]},
    {"beat": "born", "sources": ["WP", "SABR", "HOF"], "note": "When the father left differs (1919 vs 1920): no year said."},
    {"beat": "pasadena", "sources": ["WP", "SABR"]},
    {"beat": "mack", "sources": ["WP", "WPMACK"], "note": "SABR says 200-yard dash; the Olympic event was 200 m."},
    {"beat": "ucla", "sources": ["WP", "SABR"]},
    {"beat": "army", "sources": ["WP", "SABR"], "note": "WP also credits Truman Gibson; commissioned January 1943."},
    {"beat": "bus", "sources": ["WP", "SABR", "NARA"], "note": "Base was Camp Hood (Fort Hood from 1950): said only as 'an Army base in Texas'."},
    {"beat": "trial", "sources": ["WP", "NARA", "SABR"], "note": "Panel of nine white officers: WP and NARA Prologue."},
    {"beat": "monarchs", "sources": ["WP", "SABR"]},
    {"beat": "rickey", "sources": ["WP", "SABR"], "note": "Meeting August 28, 1945; quote as in WP."},
    {"beat": "montreal", "sources": ["WP", "SABR"], "note": "Led the International League with a .349 average."},
    {"beat": "debut", "sources": ["WP", "SABR", "HOF"]},
    {"beat": "abuse", "sources": ["WP", "SABR"], "note": "April 22, 1947, Ben Chapman. The Cardinals strike threat is disputed: not said."},
    {"beat": "mail", "sources": ["WP", "SABR"]},
    {"beat": "held", "sources": ["WP", "HOF"]},
    {"beat": "held2", "sources": ["WP", "SABR"], "note": "29 steals in 1947."},
    {"beat": "rookie", "sources": ["WP", "HOF", "SABR"]},
    {"beat": "series", "sources": ["WP", "HOF", "SABR"]},
    {"beat": "hall", "sources": ["WP", "HOF", "SABR"]},
    {"beat": "march", "sources": ["NARAPHOTO", "WP"]},
    {"beat": "last", "sources": ["WP", "SABR"], "note": "October 15, 1972, Cincinnati."},
    {"beat": "died", "sources": ["WP", "SABR", "HOF"], "note": "'Nearly blind' is in no checked source: not said."},
    {"beat": "fortytwo", "sources": ["WP", "MLB", "HOF"]},
]

spec = {
    "id": "reel-jackie-robinson",
    "title": "He Broke Baseball's Color Line. First, the Army Put Him on Trial.",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"Cairo, Georgia": "Kay-ro, Georgia"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": SOURCES,
    "facts": FACTS,
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
text = " ".join(x["text"] for x in B)
print(f"{len(B)} beats, {len(text.split())} words, {len(text)} characters")
