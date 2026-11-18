"""Builds data/reel-joe-louis.json: a ~3-minute film-clip reel about Joe Louis.

Every fact lists at least two sources in "facts". Images and film: public domain only
(see public/pd/reel-joe-louis/credits.json and clips/clips.json).
Film: real fight footage only. The Negro Soldier (1944, U.S. War Department) holds the 1938
Louis-Schmeling rematch; The Joe Louis Story (1953) holds real newsreels of the 1937 Braddock
and 1951 Marciano fights. Its scenes with the actor Coley Wallace are NOT used.
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-joe-louis.json")

ASSETS = {
    "p1935": "File:Joe Louis 1935 headshot by ACME Newspictures.jpg",
    "vanvechten": "File:Joe Louis by van Vechten.jpg",
    "fist1937": "File:International News Photos Portrait of Joe Louis with fist, 1937.jpg",
    "smile1937": "File:Joe Louis smiling 1937 portrait by ACME Newspictures.jpg",
    "loss1936": "File:Joe Louis counted out against Max Schmeling 1936.jpg",
    "braddock": "File:Hal Totten raising the hand of Joe Louis after his victory over Jim Braddock.jpg",
    "standing": "File:Joe Louis standing over Max Schmeling 1938.jpg",
    "harlem": "File:Celebrations in Harlem after Joe Louis knocked out Max Schmeling (1).jpg",
    "reading": "File:Joe Louis reading about his victory over Max Schmeling in the New York Daily News.jpg",
    "army": "File:Joe Louis army ACME 1942.jpg",
    "alston": "File:SGT. JOE LOUIS - CHAMPION OF CHAMPIONS - NARA - 535687.jpg",
    "sewing": "File:Joe louis barrow.jpg",
    "charles": "File:Ezzard Charles vs Joe Louis 1950.jpg",
    "p1951": "File:Joe Louis June 1951 by International News Photos.jpg",
    "schmeling71": "File:Joe Louis and Max Schmeling 1971 Press Photo.jpg",
    "medal": "File:1981 Joe Louis Congressional Gold Medal front.jpg",
}

NS = 'File:"The Negro Soldier" 1944.webm'
JLS = "File:The Joe Louis Story (1953).ogv"
CLIPS = {
    "ring38a": {"file": "negro_soldier.webm", "commons": NS, "start": 177.6, "dur": 5.4},
    "ring38b": {"file": "negro_soldier.webm", "commons": NS, "start": 184, "dur": 6},
    "down38": {"file": "negro_soldier.webm", "commons": NS, "start": 194.2, "dur": 2.6, "speed": 0.5},
    "crowd37": {"file": "joe_louis_story.ogv", "commons": JLS, "start": 2670, "dur": 3, "speed": 0.7},
    "braddock": {"file": "joe_louis_story.ogv", "commons": JLS, "start": 2680, "dur": 8},
    "marciano": {"file": "joe_louis_story.ogv", "commons": JLS, "start": 5054, "dur": 10},
    "ropes": {"file": "joe_louis_story.ogv", "commons": JLS, "start": 5068, "dur": 10},
}


def V(clip, focus, zoom=(1.0, 1.08), anchor=None):
    return {"kind": "video", "clip": clip, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or (0.5, focus[1]))}


def P(img, focus, zoom=(1.05, 1.15), anchor=None):
    return {"kind": "photo", "image": img, "focus": list(focus), "zoom": list(zoom), "anchor": list(anchor or focus)}


def C(img, cap, crop=None):
    v = {"kind": "card", "image": img, "caption": cap}
    if crop:
        v["crop"] = crop
    return v


def T(t, s):
    return {"kind": "title", "title": t, "sub": s}


B = []


def b(id, text, vis, **kw):
    x = {"id": id, "text": text, "visual": vis}
    x.update(kw)
    B.append(x)


b("hook", "He knocked out the Nazis' favorite boxer in two minutes and four seconds. Then his own government chased him for a debt he could never pay.",
  P("p1935", (0.5, 0.36), (1.1, 1.2), (0.5, 0.4)), section="hook",
  overlays={"hook": "He beat the Nazis' champion in 124 seconds. *Then his own government came for everything.*"}, captions=False, speed=1.3)
b("name", "His name was Joe Louis.", T("Joe Louis", "the Brown Bomber"), section="who")
b("born", "He was born in Alabama in 1914, the grandson of enslaved people. His parents were sharecroppers. When he was two, his father was sent to a mental hospital.",
  P("smile1937", (0.5, 0.35), (1.05, 1.15), (0.5, 0.5)), overlays={"pin": {"label": "Alabama"}}, section="story")
b("detroit", "In 1926 the family moved north, to Detroit. As an amateur, he won fifty of fifty-four fights.",
  P("fist1937", (0.55, 0.4), (1.05, 1.15), (0.55, 0.5)), overlays={"stamp": "1926"})
b("rules", "When he turned pro, his managers gave him rules. Never be photographed with a white woman. Never gloat over a beaten opponent.",
  T("The rules", "set by his managers"))
b("why", "The last Black champion, Jack Johnson, had enraged white America. They wanted to give no one an excuse.",
  P("vanvechten", (0.5, 0.3), (1.05, 1.15), (0.5, 0.45)))
b("loss", "In 1936 he fought the German Max Schmeling, and was knocked out in the twelfth round.",
  C("loss1936", "Louis counted out against Schmeling, 1936"), overlays={"stamp": "1936"}, section="fall")
b("nazi", "In Germany, the Nazi regime turned Schmeling into a national hero.",
  T("A Nazi hero", "Max Schmeling, 1936"))
b("title", "A year later, Louis won the heavyweight title in Chicago, the first Black heavyweight champion in twenty-two years.",
  V("braddock", (0.5, 0.45), (1.0, 1.08)), overlays={"stamp": "June 22, 1937"})
b("rematch", "Then came the rematch. June 22nd, 1938, Yankee Stadium. Seventy thousand people. Millions more on the radio, in America and in Germany.",
  V("ring38a", (0.5, 0.42)), section="rematch", overlays={"stamp": "June 22, 1938"})
b("fight", "Louis came out punching, and never stopped.", V("ring38b", (0.5, 0.42)))
b("ko", "Schmeling went down. His corner threw in the towel. It was over in two minutes and four seconds.",
  V("down38", (0.5, 0.6), (1.05, 1.12)))
b("harlem", "In Harlem, people poured into the streets.", P("harlem", (0.5, 0.45), (1.05, 1.15)))
b("reign", "He held the title for almost twelve years and defended it twenty-five times. Both are still records.",
  P("standing", (0.17, 0.35), (1.0, 1.08), (0.5, 0.45)))
b("war", "Then came the war. In 1942 he gave the purses from two title fights to the Navy and Army relief funds, and joined the Army.",
  P("army", (0.5, 0.3), (1.05, 1.15), (0.5, 0.45)), section="war", overlays={"stamp": "1942"})
b("troops", "He fought almost a hundred exhibitions for the troops.",
  C("alston", "Sgt. Joe Louis, Office of War Information, 1943"))
b("taxed", "But the government counted the money he gave away as his income.",
  T("Taxed", "on the money he gave away"), section="debt")
b("debt", "His tax bill kept growing. With interest and penalties, it passed one million dollars.",
  P("p1951", (0.5, 0.35), (1.1, 1.2), (0.5, 0.45)))
b("comeback", "So he came back to the ring in his late thirties. He lost to Ezzard Charles.",
  C("charles", "Ezzard Charles vs. Joe Louis, 1950"), overlays={"stamp": "1950"})
b("marciano", "Then, in 1951, Rocky Marciano knocked him out of the ring. He never fought again.",
  V("ropes", (0.5, 0.5), (1.0, 1.06)), overlays={"stamp": "October 26, 1951"})
b("greeter", "He became a pro wrestler. Later, he worked as a greeter at Caesars Palace in Las Vegas.",
  V("marciano", (0.5, 0.45)), section="after")
b("friend", "Max Schmeling, the man he beat in 1938, became his friend.",
  C("schmeling71", "Joe Louis and Max Schmeling, 1971"))
b("death", "Joe Louis died on April 12th, 1981. He was 66.",
  P("vanvechten", (0.5, 0.28), (1.2, 1.3), (0.5, 0.45)), overlays={"stamp": "April 12, 1981"}, section="end")
b("arlington", "President Reagan waived the rules so he could be buried at Arlington National Cemetery, with full military honors. Max Schmeling was a pallbearer.",
  T("Arlington", "full military honors, 1981"))
b("medal", "The next year, Congress awarded him its Gold Medal.", C("medal", "Joe Louis Congressional Gold Medal"))
b("close", "That was Joe Louis.", V("crowd37", (0.5, 0.5)))
b("cta", "Follow The Black History Room for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
spec = {
    "id": "reel-joe-louis",
    "title": "He Beat the Nazis' Champion in 124 Seconds",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "The Black History Room", "cta": "Follow The Black History Room for more.", "theme": "bhr"},
    "voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"Schmeling": "Shmelling", "Ezzard": "Ezzerd", "Caesars": "Seezers"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": {
        "WIKI": S("https://en.wikipedia.org/wiki/Joe_Louis"),
        "ENC": S("https://www.encyclopedia.com/people/sports-and-games/sports-biographies/joe-louis"),
        "HIST": S("https://www.history.com/topics/boxing/joe-louis"),
        "PBS": S("https://www.pbs.org/wgbh/americanexperience/features/fight-john-roxborough-and-julian-black"),
        "PBS2": S("https://www.pbs.org/wgbh/americanexperience/features/fight-black-boxers-and-idea-great-white-hope/"),
        "NPR": S("https://www.npr.org/transcripts/6515548"),
        "ESPN": S("https://www.espn.in/boxing/story/_/id/9404398/more-just-fight"),
        "HNN": S("https://www.historynewsnetwork.org/article/on-this-day-in-1938-joe-louis-and-max-schmeling-we"),
        "LIB": S("https://libertarianinstitute.org/articles/joe-louis-vs-the-tax-man"),
        "CRB": S("https://claremontreviewofbooks.com/digital/terminator-irs-hounded-joe-louis-into-poverty"),
        "ANC": S("https://www.arlingtoncemetery.mil/Explore/Notable-Graves/Sports/Joe-Louis"),
        "MOSAIC": S("https://mosaicmagazine.com/picks/history-ideas/2023/07/although-made-into-an-avatar-of-nazi-germany-max-schmeling-was-among-the-righteous/"),
        "MEDAL": S("https://commons.wikimedia.org/wiki/File:1981_Joe_Louis_Congressional_Gold_Medal_front.jpg"),
        "HARLEM": S("https://commons.wikimedia.org/wiki/File:Celebrations_in_Harlem_after_Joe_Louis_knocked_out_Max_Schmeling_(1).jpg"),
    },
    "facts": [
        {"beat": "hook", "sources": ["WIKI", "HIST", "ESPN"], "note": "2:04 in round one; Nazi regime made Schmeling a hero (WIKI, HNN)."},
        {"beat": "born", "sources": ["WIKI", "ENC", "HIST"], "note": "Parents were children of former slaves (WIKI); father committed when Joe was two (ENC, HIST)."},
        {"beat": "detroit", "sources": ["WIKI", "ENC", "HIST"], "note": "Amateur 50-4 (WIKI), 50 of 54 (HIST)."},
        {"beat": "rules", "sources": ["WIKI", "PBS"]},
        {"beat": "why", "sources": ["WIKI", "PBS2"]},
        {"beat": "loss", "sources": ["WIKI", "HIST", "ENC"]},
        {"beat": "nazi", "sources": ["WIKI", "HNN"]},
        {"beat": "title", "sources": ["WIKI", "HIST", "ENC"], "note": "First Black heavyweight champion in 22 years (HIST); Johnson lost the title in 1915 (WIKI)."},
        {"beat": "rematch", "sources": ["WIKI", "HIST", "NPR"], "note": "70,043 (HIST), about 70,000 (WIKI); radio hookups to Germany (NPR)."},
        {"beat": "ko", "sources": ["WIKI", "HIST", "ESPN"], "note": "Knockdown count differs (three vs two): not said."},
        {"beat": "harlem", "sources": ["HARLEM", "HNN"]},
        {"beat": "reign", "sources": ["WIKI", "ENC", "HIST"], "note": "11 years 8 months; 25 defenses."},
        {"beat": "war", "sources": ["WIKI", "HIST", "ENC"]},
        {"beat": "troops", "sources": ["ENC", "HIST"], "note": "96 exhibitions (ENC), over 96 (HIST): said 'almost a hundred'."},
        {"beat": "taxed", "sources": ["WIKI", "LIB", "CRB"]},
        {"beat": "debt", "sources": ["WIKI", "ENC", "LIB"], "note": "Over $1M by late 1950s (WIKI); 'by 1949' (ENC) not used."},
        {"beat": "comeback", "sources": ["WIKI", "ENC", "HIST"]},
        {"beat": "marciano", "sources": ["WIKI", "ENC", "HIST"]},
        {"beat": "greeter", "sources": ["WIKI", "ENC", "HIST"]},
        {"beat": "friend", "sources": ["WIKI", "MOSAIC"]},
        {"beat": "death", "sources": ["WIKI", "ENC", "HIST"]},
        {"beat": "arlington", "sources": ["WIKI", "HIST", "ANC", "MOSAIC"]},
        {"beat": "medal", "sources": ["WIKI", "MEDAL"]},
    ],
    "notUsed": [
        "Tax debt resolution: 'special act of Congress forgave' (HIST) vs a 1962 settlement (other accounts): left out.",
        "Final record 66-3 (WIKI) vs 68-3 (HIST): left out.",
        "Exact charity amounts differ by source: left out.",
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
words = sum(len(x["text"].split()) for x in B)
print(f"{len(B)} beats, {words} words")
