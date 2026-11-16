"""Builds data/reel-hattie-mcdaniel.json: a ~3-minute reel (Black History Unfiltered length) about Hattie McDaniel.

Every fact lists at least two sources in "facts". Images: public domain only (see public/pd/reel-hattie-mcdaniel/credits.json).
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-hattie-mcdaniel.json")

ASSETS = {
    "mammy": 'File:Hattie McDaniel as "Mammy" in Gone With the Wind promotional image.webp',
    "h1941": "File:1941hattie.jpg",
    "studio": "File:Studio publicity Hattie McDaniel.jpg",
    "gwtw": "File:Gone With The Wind featuring McDaniel & de Havilland & Leigh.jpg",
    "beulah48": "File:Hattie Mc Daniel Beulah 1948.jpg",
    "victory": 'File:"Hattie McDaniel (center), Chairman of the Negro Division of the Hollywood Victory Committee, takes time off from rehear - NARA - 535875.jpg',
    "jet1": "File:Jet 20 Nov 1952 pg PA61.jpg",
    "grove": "File:World famous cocoanut grove at the Ambassador Hotel, Los Angeles, California (62250).jpg",
    "premiere": "File:Gone With the Wind Atlanta premiere 1939.jpg",
    "poster": "File:Gone With the Wind Poster 1939.jpg",
    "rosedale": "File:Rosedale pyramid.jpg",
}


JP = "File:Judge Priest (1934).webm"
CLIPS = {
    "porch": {"file": "judge_priest.webm", "commons": JP, "start": 2334, "dur": 9},
    "laundry": {"file": "judge_priest.webm", "commons": JP, "start": 393, "dur": 10},
    "festival": {"file": "judge_priest.webm", "commons": JP, "start": 2384, "dur": 7},
    "kitchen": {"file": "judge_priest.webm", "commons": JP, "start": 2583, "dur": 7},
    "laugh": {"file": "judge_priest.webm", "commons": JP, "start": 397, "dur": 4},
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


b("hook", "She won an Oscar. And Hollywood still wouldn't let her be buried in its cemetery.",
  P("mammy", (0.5, 0.38), (1.1, 1.22), (0.5, 0.32)), section="hook",
  overlays={"hook": "She won an Oscar. *Hollywood still wouldn't let her be buried there.*"}, captions=False, speed=1.3)
b("name", "Her name was Hattie McDaniel.", T("Hattie McDaniel", "the first Black Oscar winner"), section="who")
b("born", "She was born in Wichita, Kansas, the youngest of thirteen children. Her parents had been enslaved, and her father fought in the Civil War.",
  V("porch", (0.3, 0.32)), overlays={"pin": {"label": "Wichita, Kansas"}}, section="story")
b("radio", "She grew up in Denver, singing. In the 1920s she sang on Denver radio, and she is often called the first Black woman to sing on American radio.",
  V("laundry", (0.42, 0.35)))
b("crash", "Then came the crash of 1929. Her touring show went broke, and she was stranded.", T("1929", "the crash"))
b("washroom", "The only job she could find was washroom attendant, at a nightclub outside Milwaukee.", T("Washroom attendant", "Club Madrid, Milwaukee"))
b("stage", "The club kept Black performers off the stage. She talked her way onto it anyway, and became a regular.",
  V("festival", (0.27, 0.32)))
b("hollywood", "In 1931, she moved to Hollywood. And again and again, the studios cast her as a maid.", V("kitchen", (0.3, 0.32)))
b("quote", "When people criticized her for it, she reportedly said: Why should I complain about making seven hundred dollars a week playing a maid? If I didn't, I'd be making seven dollars a week being one.",
  T("$700 a week playing a maid", "or $7 a week being one"))
b("gwtw", "Then, in 1939, she was cast as Mammy, in Gone with the Wind.", P("gwtw", (0.14, 0.2), (1.15, 1.3), (0.45, 0.3)))
b("premiere", "But when the movie premiered in Atlanta, she couldn't go. The theater was for white people only.",
  C("premiere", "Loew's Grand Theatre, Atlanta, 1939"), overlays={"stamp": "December 15, 1939"})
b("gable", "Her co-star Clark Gable was so angry, he threatened to boycott. She talked him into going anyway.",
  P("poster", (0.5, 0.12), (1.3, 1.4), (0.45, 0.3)))
b("nominated", "Then she was nominated for an Oscar, the first Black actor ever nominated.",
  P("mammy", (0.5, 0.35), (1.45, 1.6), (0.5, 0.35)), section="oscar")
b("grove", "The ceremony was at the Ambassador Hotel's Cocoanut Grove. She was seated at a separate table, on the far side of the room, away from her co-stars.",
  C("grove", "The Cocoanut Grove, Ambassador Hotel"))
b("won", "On February 29th, 1940, they called her name. She became the first Black person ever to win an Oscar.",
  P("h1941", (0.5, 0.12), (1.05, 1.15), (0.5, 0.3)), overlays={"stamp": "February 29, 1940"})
b("speech", "She said she hoped to always be a credit to her race, and to the motion picture industry.", T("\"A credit to my race\"", "Hattie McDaniel, 1940"))
b("plaque", "Her award wasn't even the famous statue. Supporting winners got a small plaque.",
  C("jet1", "Hattie McDaniel and her Oscar plaque", crop=[0.0, 0.0, 1.0, 0.42]))
b("sugarhill", "In 1945, white neighbors sued to force her and other Black homeowners out of their Los Angeles neighborhood. She rallied them to fight back, and the judge threw the case out.",
  C("victory", "Hattie McDaniel (center), 1940s"), overlays={"stamp": "1945"}, section="later")
b("beulah", "She went on to star in her own radio show, Beulah, and then on television.", P("beulah48", (0.6, 0.22), (1.3, 1.42), (0.55, 0.32)))
b("death", "In 1952, she died of breast cancer. She was 59.", P("studio", (0.47, 0.3), (1.15, 1.25), (0.5, 0.32)))
b("wish", "Her last wish was to be buried in Hollywood Cemetery.", T("Her last wish", "Hollywood Cemetery"), section="end")
b("refused", "The cemetery said no. It was for white people only.", T("Whites only", "Hollywood Cemetery, 1952"))
b("rosedale", "She was buried across town, at Rosedale Cemetery.", C("rosedale", "Rosedale Cemetery, Los Angeles"))
b("lost", "She left her Oscar to Howard University. Decades ago, it disappeared. It has never been found.",
  C("jet1", "Jet magazine, November 1952", crop=[0.0, 0.0, 1.0, 0.62], clip=True))
b("cassity", "In 1999, the cemetery's new owner offered to move her there. Her family said no. So he built a memorial to her instead.", T("1999", "Hollywood Forever"))
b("replace", "And in 2023, the Academy finally gave Howard a replacement Oscar.", T("2023", "\"Hattie's Come Home\""))
b("close", "That was Hattie McDaniel.", V("laugh", (0.4, 0.35)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
spec = {
    "id": "reel-hattie-mcdaniel",
    "title": "Hollywood Wouldn't Let Her Be Buried There",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"Cocoanut": "Coconut"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "faces": {"mammy": [[0.28, 0.12, 0.74, 0.62]]},
    "beats": B,
    "sources": {
        "WIKI": S("https://en.wikipedia.org/wiki/Hattie_McDaniel"),
        "KSHS": S("https://www.kansashistory.gov/kansapedia/hattie-mcdaniel/12142"),
        "ENC": S("https://www.encyclopedia.com/history/encyclopedias-almanacs-transcripts-and-maps/mcdaniel-hattie"),
        "MKE": S("https://milwaukeebronzevillehistories.org/items/show/7"),
        "AJC": S("https://www.ajc.com/news/years-ago-actress-hattie-mcdaniel-broke-the-color-barrier-the-oscars/vtEEXYKtaeJqKIEFPhIjAM/"),
        "WEEK": S("https://theweek.com/articles/539316/remembering-hattie-mcdaniel-75-years-since-historic-oscar-win"),
        "AND": S("https://andscape.com/features/film-academy-replaces-hattie-mcdaniels-long-lost-oscar/"),
        "CBS": S("https://www.cbsnews.com/colorado/news/hattie-mcdaniel-missing-academy-award-replacement-gift-howard-university"),
        "NBCLA": S("https://nbclosangeles.com/news/local/monique-hattie-mcdaniel-and-west-adams/1867946"),
        "HF": S("https://en.wikipedia.org/wiki/Hollywood_Forever_Cemetery"),
        "JET": S("https://commons.wikimedia.org/wiki/File:Jet_20_Nov_1952_pg_PA61.jpg"),
        "AMS": S("https://amsterdamnews.com/news/2017/03/02/film-immortal-hattie-mcdaniel/"),
    },
    "facts": [
        {"beat": "born", "sources": ["WIKI", "KSHS"], "note": "youngest of 13; formerly enslaved parents; father a Civil War veteran. Birth year differs (1893/1895), so not said."},
        {"beat": "radio", "sources": ["WIKI", "ENC"], "note": "'reputedly the first Black woman soloist on radio', said as 'often called'"},
        {"beat": "crash", "sources": ["WIKI", "MKE"]},
        {"beat": "washroom", "sources": ["WIKI", "MKE"]},
        {"beat": "stage", "sources": ["WIKI", "MKE"]},
        {"beat": "hollywood", "sources": ["WIKI", "KSHS", "JET"]},
        {"beat": "quote", "sources": ["WIKI", "AMS"], "note": "wording varies between sources; said as 'reportedly'"},
        {"beat": "premiere", "sources": ["WIKI", "ENC", "AJC"]},
        {"beat": "gable", "sources": ["WIKI", "AJC", "WEEK"]},
        {"beat": "nominated", "sources": ["WIKI", "AND"]},
        {"beat": "grove", "sources": ["WIKI", "AND", "CBS"]},
        {"beat": "won", "sources": ["WIKI", "AND", "KSHS"]},
        {"beat": "speech", "sources": ["WIKI", "AND"]},
        {"beat": "plaque", "sources": ["WIKI", "AND"]},
        {"beat": "sugarhill", "sources": ["WIKI", "NBCLA"]},
        {"beat": "beulah", "sources": ["WIKI", "ENC"]},
        {"beat": "death", "sources": ["WIKI", "AND"]},
        {"beat": "wish", "sources": ["WIKI", "NBCLA"]},
        {"beat": "refused", "sources": ["WIKI", "NBCLA"]},
        {"beat": "rosedale", "sources": ["WIKI", "NBCLA"]},
        {"beat": "lost", "sources": ["WIKI", "AND", "JET"]},
        {"beat": "cassity", "sources": ["WIKI", "HF"]},
        {"beat": "replace", "sources": ["WIKI", "AND", "CBS"]},
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False), encoding="utf-8")
print(sum(len(x["text"].split()) for x in B), "words,", len(B), "beats")
