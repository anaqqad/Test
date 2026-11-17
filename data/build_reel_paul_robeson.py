"""Builds data/reel-paul-robeson.json: a ~3-minute film-clip reel about Paul Robeson.

Every fact lists at least two sources in "facts". Images and film: public domain only
(see public/pd/reel-paul-robeson/credits.json and clips/clips.json).
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-paul-robeson.json")

ASSETS = {
    "p1942": "File:Paul Robeson 1942 crop.jpg",
    "senior": "File:Paul Robeson, senior photo from the Scarlet Letter yearbook.jpg",
    "capskull": "File:Photograph of Paul Robeson with fellow Cap and Skull inductees.jpg",
    "othello": "File:Scene from Othello with Paul Robeson as Othello 8e07912v.jpg",
    "othello2": "File:Scene from Othello with Paul Robeson 8e07911v.jpg",
    "shipyard": 'File:"Paul Robeson, world famous Negro baritone, leading Moore Shipyard (Oakland, CA) workers in singing the Star Spangled Ba - NARA - 535874.jpg',
    "nara": "File:Paul Robeson - NARA - 559205.jpg",
    "ejstill": "File:Paul Robeson in The Emperor Jones.jpg",
    "p1930s": "File:Paul Robeson - 1930s.JPG",
    "bham": "File:Paul Robeson - Birmingham Town Hall - 1939-03-07.jpg",
}

EJ = "File:The Emperor Jones (1933) by Dudley Murphy and William Churchill de Mille.webm"
BS = "File:Body and Soul (1925).webm"
CLIPS = {
    "pulpit": {"file": "body_and_soul.webm", "commons": BS, "start": 511.5, "dur": 5.5},
    "pulpit2": {"file": "body_and_soul.webm", "commons": BS, "start": 482, "dur": 5},
    "suit": {"file": "body_and_soul.webm", "commons": BS, "start": 846, "dur": 4},
    "shoes": {"file": "emperor_jones.webm", "commons": EJ, "start": 514, "dur": 4},
    "sofa": {"file": "emperor_jones.webm", "commons": EJ, "start": 914, "dur": 10},
    "tux": {"file": "emperor_jones.webm", "commons": EJ, "start": 980, "dur": 8},
    "club": {"file": "emperor_jones.webm", "commons": EJ, "start": 1054, "dur": 8},
    "close": {"file": "emperor_jones.webm", "commons": EJ, "start": 2632, "dur": 10},
    "boss": {"file": "emperor_jones.webm", "commons": EJ, "start": 2534, "dur": 10},
}


def V(clip, focus, zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap, crop=None, clip=False):
    v = {"kind": "card", "image": img, "caption": cap}
    if crop:
        v["crop"] = crop
    if clip:
        v["clipping"] = True
    return v


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


B = []


def b(id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


b("hook", "He was one of the most famous men in the world. Then America took away his passport.",
  P("p1942", (0.5, 0.3), (1.1, 1.22), (0.5, 0.3)), section="hook",
  overlays={"hook": "One of the most famous men alive. *Then America took his passport.*"}, captions=False, speed=1.3)
b("name", "His name was Paul Robeson.", T("Paul Robeson", "singer, actor, athlete, activist"), section="who")
b("born", "He was born in Princeton, New Jersey, in 1898. His father had escaped slavery and became a minister. When Paul was six, his mother died in a fire.",
  P("senior", (0.5, 0.35), (1.05, 1.15), (0.5, 0.35)), overlays={"pin": {"label": "Princeton, New Jersey"}}, section="story")
b("rutgers", "He won a scholarship to Rutgers, where he was the only Black student at the time.",
  C("capskull", "Robeson with Cap and Skull inductees, Rutgers, 1919"), overlays={"stamp": "1915"})
b("tryouts", "At football tryouts, his own teammates broke his nose and dislocated his shoulder. He made the team anyway.",
  T("A broken nose", "and a dislocated shoulder"))
b("star", "He became an All-American twice, joined Phi Beta Kappa, and graduated as class valedictorian.",
  P("senior", (0.5, 0.3), (1.3, 1.45), (0.5, 0.3)))
b("law", "Then he earned a law degree from Columbia and joined a New York law firm.", V("suit", (0.5, 0.3)))
b("secretary", "But a white secretary refused to take dictation from him. So he quit. Not just the job, but the law.",
  T("She refused", "to take his dictation"))
b("stage", "He turned to the stage, and to film.", V("pulpit", (0.5, 0.3)), section="fame")
b("voice", "His deep voice made him a star. In Show Boat he sang Ol' Man River, and it became his song.",
  V("sofa", (0.33, 0.32)))
b("othello", "In 1943 he played Othello on Broadway. It ran 296 performances, a Broadway record for Shakespeare.",
  P("othello", (0.5, 0.3), (1.05, 1.15), (0.5, 0.3)), overlays={"stamp": "1943"})
b("movies", "He starred in films in America and Britain, in leading roles.",
  V("tux", (0.7, 0.3)))
b("fight", "And he used his fame. He sang for workers, and spoke out against lynching and segregation.",
  C("shipyard", "Robeson leads shipyard workers in song, Oakland, 1942"))
b("soviet", "He also praised the Soviet Union. In Cold War America, that made him a target.",
  P("nara", (0.5, 0.3), (1.1, 1.2), (0.5, 0.3)), section="target")
b("peekskill", "In 1949, rioters shut down his concert in Peekskill, New York.",
  T("Peekskill, 1949", "the concert was shut down"))
b("passport", "In 1950, the State Department took his passport. He could no longer perform abroad.",
  T("Passport cancelled", "U.S. State Department, 1950"), overlays={"stamp": "1950"})
b("blacklist", "At home he was blacklisted. His records and films were pulled. His income fell from over a hundred thousand dollars a year to almost nothing.",
  V("close", (0.5, 0.3)))
b("border", "In 1952, he was even turned back at the Canadian border, though no passport was needed to enter Canada.",
  T("Turned back", "U.S.-Canada border, 1952"))
b("peacearch", "So the union that invited him set up a concert at the Peace Arch. He stood on a flatbed truck on the American side and sang across the border to tens of thousands of people.",
  C("bham", "Paul Robeson in concert"), overlays={"stamp": "May 18, 1952"})
b("huac", "In 1956, Congress called him in. Asked why he didn't just stay in Russia, he answered:",
  P("p1930s", (0.5, 0.3), (1.05, 1.15), (0.5, 0.3)), section="hearing", overlays={"stamp": "June 12, 1956"})
b("father", "Because my father was a slave, and my people died to build this country, and I am going to stay here, and have a part of it, just like you.",
  T("\"My father was a slave\"", "Paul Robeson to Congress, 1956"))
b("unamerican", "Then he told them: You are the un-Americans, and you ought to be ashamed of yourselves.",
  V("boss", (0.62, 0.3)))
b("returned", "In 1958, after a Supreme Court ruling, he finally got his passport back.",
  C("ejstill", "Paul Robeson, The Emperor Jones, 1933"), overlays={"stamp": "1958"}, section="end")
b("decline", "But his health broke down, and his career never recovered. He died in Philadelphia in 1976. He was 77.",
  P("p1942", (0.5, 0.3), (1.3, 1.4), (0.5, 0.3)))
b("hof", "In 1995, he was finally named to the College Football Hall of Fame.", T("1995", "College Football Hall of Fame"))
b("close", "That was Paul Robeson.", V("shoes", (0.5, 0.3)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
spec = {
    "id": "reel-paul-robeson",
    "title": "Then America Took His Passport",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"Robeson": "Robe-son", "Ol' Man River": "Old Man River"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": {
        "WIKI": S("https://en.wikipedia.org/wiki/Paul_Robeson"),
        "ENC": S("https://www.encyclopedia.com/education/news-wires-white-papers-and-books/robeson-paul"),
        "RU": S("https://www.rutgers.edu/news/paul-robeson-launched-career-singer-and-stage-actor-after-rutgers-graduation"),
        "COL": S("https://www.law.columbia.edu/news/archive/activist-global-stage-paul-robeson-1923"),
        "SWAN": S("https://collections.swansea.ac.uk/s/paul-robeson-wales/page/passport-withdrawal"),
        "PAN": S("https://www.peacearchnews.com/community/look-back-at-political-statement-at-peace-arch-border/"),
        "MNW": S("https://mynorthwest.com/local/washingtons-forgotten-woodstock-of-the-mccarthy-era/294843"),
        "HUAC": S("https://www.marxists.org/archive/robeson/1956/06/12.htm"),
        "GMU": S("https://historymatters.gmu.edu/d/6440"),
        "NARA": S("https://commons.wikimedia.org/wiki/File:%22Paul_Robeson,_world_famous_Negro_baritone,_leading_Moore_Shipyard_(Oakland,_CA)_workers_in_singing_the_Star_Spangled_Ba_-_NARA_-_535874.jpg"),
        "COMMONS_FILMS": S("https://commons.wikimedia.org/wiki/File:The_Emperor_Jones_(1933)_by_Dudley_Murphy_and_William_Churchill_de_Mille.webm"),
        "CFHOF": S("https://cfbhall.com/inductees/paul-robeson-1995"),
    },
    "facts": [
        {"beat": "born", "sources": ["WIKI", "ENC"], "note": "Wiki: house fire; ENC: stove-fire accident. Said as 'a fire'."},
        {"beat": "rutgers", "sources": ["WIKI", "RU"], "note": "Wiki: third Black student ever, the only one at the time."},
        {"beat": "tryouts", "sources": ["WIKI", "RU"]},
        {"beat": "star", "sources": ["WIKI", "ENC"]},
        {"beat": "law", "sources": ["WIKI", "ENC", "COL"]},
        {"beat": "secretary", "sources": ["ENC", "RU", "COL"], "note": "exact words vary (Duberman); card says 'as reported'"},
        {"beat": "voice", "sources": ["WIKI", "ENC", "RU"]},
        {"beat": "movies", "sources": ["WIKI", "COMMONS_FILMS"], "note": "Body and Soul 1925, The Emperor Jones 1933; British films 1930s per Wiki"},
        {"beat": "othello", "sources": ["WIKI", "RU"]},
        {"beat": "fight", "sources": ["WIKI", "NARA"]},
        {"beat": "soviet", "sources": ["ENC", "RU"]},
        {"beat": "peekskill", "sources": ["WIKI", "ENC"]},
        {"beat": "passport", "sources": ["WIKI", "ENC", "SWAN", "RU"]},
        {"beat": "blacklist", "sources": ["WIKI", "ENC"], "note": "Wiki: ~$150,000 to under $3,000; ENC: $104,000 (1947) to $2,000. Said as 'over a hundred thousand ... almost nothing'."},
        {"beat": "border", "sources": ["PAN", "MNW"]},
        {"beat": "peacearch", "sources": ["WIKI", "PAN", "MNW"], "note": "crowd 25,000-35,000 by source; said 'tens of thousands'"},
        {"beat": "huac", "sources": ["WIKI", "HUAC"]},
        {"beat": "father", "sources": ["HUAC", "GMU"]},
        {"beat": "unamerican", "sources": ["HUAC", "GMU"]},
        {"beat": "returned", "sources": ["WIKI", "ENC"]},
        {"beat": "decline", "sources": ["WIKI", "ENC", "RU"]},
        {"beat": "hof", "sources": ["WIKI", "CFHOF"]},
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
print(sum(len(x["text"].split()) for x in B), "words,", len(B), "beats")
