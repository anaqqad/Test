"""Builds data/reel-wwf-wainwright.json: a ~2:40 film-clip reel for WWII Frontlines (test of the reel format).

Story: Gen. Jonathan Wainwright, left on Corregidor by MacArthur, surrendered in May 1942, feared disgrace for three
years, then stood behind MacArthur on the Missouri and got the first pen. Long episode: https://youtu.be/uMCYnVyPoLE
Research: WWII Frontlines repo, video/wainwright-pen/research/facts_raw.md (sources [1]-[16] there).
Film: U.S. government film, public domain (NARA 111-ADC-5190; United News ARC-39079; newsreel of 10 Sep 1945).
Photos: the episode's public-domain stills (copied into public/pd/reel-wwf-wainwright/, credits.json).
"""
import json
from pathlib import Path

OUT = Path(__file__).with_name("reel-wwf-wainwright.json")

# photos come from the long episode (already checked public domain), not fetched again
ASSETS = {
    "portrait": "File:80-G-354136 Lieutenant General Jonathan M. Wainwright, USA.jpg",
    "with_mac": "File:Wainwright and MacArthur at Philippine.jpg",
    "adelaide": "File:General Douglas MacArthur and Mrs Jean Marie MacArthur at Adelaide railway station, 20 March 1942.jpg",
    "cabcaben": "File:Americans Surrender Bataan.jpg",
    "generals": "File:American generals in captivity, July 1942.jpg",
    "captive": "File:Jonathan Wainwright under Imperial Japanese army.jpg",
    "reunion": "File:General of the Army Douglas MacArthur and Lieutenant General Jonathan Wainwright greet each other.jpg",
    "signing": "File:Douglas MacArthur signs formal surrender.jpg",
    "official": "File:Jonathan M. Wainwright - Official Portrait.jpg",
}

YOK = "NARA 111-ADC-5190: General Wainwright speaks from Yokohama, Japan (Sept 1945)"
SN = "United News, Sept 1945: Japanese Sign Final Surrender (NARA ARC-39079)"
HOME = "Newsreel, 10 Sept 1945: Nation Welcomes Hero of Corregidor"
CLIPS = {
    "yok_med": {"file": "yok.mp4", "commons": YOK, "start": 327, "dur": 8},
    "yok_c1": {"file": "yok.mp4", "commons": YOK, "start": 362, "dur": 9},
    "yok_c2": {"file": "yok.mp4", "commons": YOK, "start": 390, "dur": 10},
    "yok_c3": {"file": "yok.mp4", "commons": YOK, "start": 418, "dur": 10},
    "home_speech2": {"file": "home.mp4", "commons": HOME, "start": 89, "dur": 8},
    "home_speech": {"file": "home.mp4", "commons": HOME, "start": 77.5, "dur": 10},
    "home_truman": {"file": "home.mp4", "commons": HOME, "start": 121.5, "dur": 7},
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


b("hook", "He surrendered Corregidor to the Japanese, and for three years he feared America would call him a disgrace. Then MacArthur handed him the pen that ended the war.",
  P("portrait", (0.5, 0.3), (1.1, 1.2), (0.5, 0.42)), section="hook",
  overlays={"hook": "He surrendered Corregidor and feared disgrace. *Then MacArthur handed him the pen.*"}, captions=False, speed=1.3)
b("name", "His name was Jonathan Wainwright.", T("Wainwright", "General Jonathan M. Wainwright"), section="who")
b("march", "March 1942, the Philippines. Roosevelt ordered MacArthur out to Australia. He left Wainwright behind, with Bataan and Corregidor under siege.",
  C("with_mac", "Wainwright and MacArthur, Philippines"), overlays={"stamp": "March 1942"}, section="story")
b("farewell", "Before he left, MacArthur gave him a box of cigars and two jars of shaving cream. Wainwright promised to be on Bataan when MacArthur came back, if he was alive.",
  V("yok_med", (0.5, 0.4), (1.0, 1.08)))
b("australia", "In Australia, MacArthur told the world: I came through, and I shall return.",
  C("adelaide", "MacArthur in Adelaide, March 20, 1942"))
b("bataan", "Wainwright's men were starving. On April 9th, Bataan fell.",
  T("Bataan falls", "April 9, 1942"), section="fall")
b("corregidor", "On May 6th, the Japanese were on Corregidor. Wainwright surrendered, to save, he wrote later, close to eleven thousand men, the wounded and the nurses.",
  C("cabcaben", "Surrender talks, Cabcaben, May 6, 1942"), overlays={"stamp": "May 6, 1942"})
b("radio", "The next night, he had to read the surrender of every American in the Philippines on the radio, in a voice, the Army's history says, husky with suppressed emotion.",
  P("captive", (0.6, 0.3), (1.05, 1.12), (0.55, 0.45)))
b("cable", "MacArthur cabled Washington: I believe Wainwright has temporarily become unbalanced.",
  T("Unbalanced", "MacArthur to Washington, May 9, 1942"), section="blame")
b("medal", "That summer, General Marshall proposed Wainwright for the Medal of Honor. MacArthur blocked it. The citation, he wrote, does not represent the truth.",
  V("yok_c1", (0.3, 0.42), (1.22, 1.28), (0.5, 0.3)))
b("camps", "Wainwright was moved from camp to camp, to Formosa, then to Manchuria. By October 1942 he weighed one hundred thirty-two pounds, forty pounds under normal.",
  C("generals", "American generals in captivity, July 1942"), section="prison")
b("diary", "A Japanese reporter asked him if he would be court-martialed for surrendering. In his diary, he wrote down why he had done it.",
  V("yok_c2", (0.5, 0.42), (1.22, 1.28), (0.5, 0.3)))
b("rescue", "In August 1945, an American team parachuted into Manchuria and found him. He asked them one question: what did people at home think of him? They told him he was a hero. He did not believe it.",
  V("yok_c3", (0.5, 0.42), (1.22, 1.28), (0.5, 0.3)), overlays={"stamp": "August 1945"}, section="free")
b("reunion", "On August 31st, he walked into MacArthur's dining room in Yokohama, on a cane. MacArthur rose and embraced him. Wainwright could barely speak.",
  P("reunion", (0.6, 0.22), (1.05, 1.15), (0.55, 0.4)))
b("missouri", "Two days later, aboard the battleship Missouri, MacArthur called him forward to stand behind him as he signed Japan's surrender.",
  C("signing", "USS Missouri, Tokyo Bay. Behind MacArthur: Wainwright and Percival"), overlays={"stamp": "September 2, 1945"}, section="pen")
b("pen", "Halfway through his signature, MacArthur stopped, and handed Wainwright the pen.",
  P("signing", (0.38, 0.62), (1.25, 1.35), (0.45, 0.5)))
b("home", "On September 10th, more than a hundred thousand people waited for him in Washington. The banner behind him read: Skinny.",
  V("home_speech", (0.5, 0.45), (1.15, 1.2), (0.5, 0.3)), section="home")
b("truman", "In the White House garden, President Truman fastened the Medal of Honor around his neck. The medal MacArthur had blocked.",
  V("home_truman", (0.45, 0.4), (1.0, 1.06)))
b("diary2", "Months earlier, Truman had written in his private diary: we'd have had a real general and a fighting man, if we had Wainwright.",
  V("home_speech2", (0.5, 0.45), (1.15, 1.2), (0.5, 0.3)))
b("death", "Jonathan Wainwright died on September 2nd, 1953, eight years to the day after the surrender on the Missouri.",
  P("official", (0.45, 0.35), (1.1, 1.2), (0.5, 0.45)), overlays={"stamp": "September 2, 1953"}, section="end")
b("close", "That was Jonathan Wainwright.", P("portrait", (0.5, 0.3), (1.2, 1.3), (0.5, 0.42)))
b("cta", "Follow WWII Frontlines for more.", {"kind": "endcard"}, section="cta", captions=False)

S = lambda u: {"url": u}
spec = {
    "id": "reel-wwf-wainwright",
    "title": "He Surrendered Corregidor. Then MacArthur Handed Him the Pen.",
    "format": "reel", "fps": 30, "width": 1080, "height": 1920,
    "music": {"volume": 0.06},
    "mix": {"targetLufs": -14, "ceilingDbtp": -1.5, "musicUnderVoiceDb": 21, "duckDb": 3, "hookBoostDb": 2},
    "brand": {"page": "WWII Frontlines", "cta": "Follow WWII Frontlines for more.", "theme": "wwf"},
    "voice": {"engine": "kokoro", "voice": "bm_george", "speed": 1.2, "leadInSeconds": 0.4, "sectionGapSeconds": 1},
    "pronounce": {"Corregidor": "Ko-reg-ih-door", "Bataan": "Bah-tahn"},
    "assets": {k: {"commons": v} for k, v in ASSETS.items()},
    "clips": CLIPS,
    "beats": B,
    "sources": {
        "SERIAL": S("https://archive.org/details/wainwrights-own-story"),
        "HOPE": S("https://archive.org/details/hope-star-1945-11-15"),
        "MEMOIR": S("https://archive.org/details/generalwainwrigh0000edit"),
        "MORTON": S("https://www.ibiblio.org/hyperwar/USA/USA-P-PI/USA-P-PI-32.html"),
        "TRUMANCIT": S("https://www.trumanlibrary.gov/library/public-papers/131/citation-accompanying-congressional-medal-honor-presented-general"),
        "DIARY": S("https://www.pbs.org/wgbh/americanexperience/features/pacific-invade-or-bomb"),
        "STERNER": S("https://www.homeofheroes.com/?p=55866"),
        "CITINO": S("https://www.nationalww2museum.org/war/articles/general-percival-general-wainwright-vj-day"),
        "WOLF": S("https://www.nationalww2museum.org/war/articles/parker-pens-ended-world-war-ii"),
        "LUDAN": S("https://armchairgeneral.com/yokohamas-new-grand-hotel-macarthurs-first-japanese-home.htm"),
        "MANCINI": S("https://warfarehistorynetwork.com/article/the-oss-operation-cardinal-locating-general-jonathan-wainwright/"),
        "LEITH": S("https://www.ww2online.org/view/hal-leith"),
        "HORN": S("https://www.wlrn.org/2025-05-26/author-jonathan-horn-discusses-his-new-book-the-fate-of-the-generals"),
        "WIKI": S("https://en.wikipedia.org/wiki/Jonathan_M._Wainwright_IV"),
        "BRIT": S("https://www.britannica.com/biography/Jonathan-M-Wainwright"),
        "HOMEFILM": S("https://archive.org/details/September101945Newsreel-NationWelcomesHeroOfCorregidor"),
    },
    "facts": [
        {"beat": "hook", "sources": ["HOPE", "LEITH", "MANCINI", "CITINO"], "note": "Feared disgrace: court-martial question at Karenko (HOPE), Leith and Lamar (LEITH, MANCINI). First pen: HOPE, CITINO."},
        {"beat": "march", "sources": ["SERIAL", "MORTON", "WIKI"]},
        {"beat": "farewell", "sources": ["SERIAL", "MORTON"], "note": "Cigars and two jars of shaving cream (SERIAL); 'if I'm alive' (MORTON citing the memoir pp. 2-4)."},
        {"beat": "australia", "sources": ["MORTON", "WIKI"], "note": "NYT 21 Mar 1942 as cited by Morton."},
        {"beat": "bataan", "sources": ["MORTON", "WIKI"]},
        {"beat": "corregidor", "sources": ["MORTON", "HOPE"], "note": "'close to 11,000 men and the wounded and nurses' (Wainwright as quoted by Morton); diary reasons (HOPE)."},
        {"beat": "radio", "sources": ["MORTON", "WIKI"], "note": "KZRH, shortly before midnight 7 May 1942, 'in a voice husky with suppressed emotion' (MORTON)."},
        {"beat": "cable", "sources": ["MORTON", "WIKI"], "note": "Radiogram to Marshall, 9 May 1942, verbatim."},
        {"beat": "medal", "sources": ["STERNER", "HORN", "WIKI"], "note": "Marshall proposed 30 Jul 1942; radiogram 'does not represent the truth' (STERNER)."},
        {"beat": "camps", "sources": ["HOPE", "MEMOIR"], "note": "132 lb on 3 Oct 1942, 'forty pounds under normal' (MEMOIR); camps Karenko (Formosa) to Manchuria (HOPE map caption)."},
        {"beat": "diary", "sources": ["HOPE", "MEMOIR"]},
        {"beat": "rescue", "sources": ["MANCINI", "LEITH", "HOPE"], "note": "OSS team jumped 16 Aug at Mukden; Lamar and Leith reached Sian 19 Aug."},
        {"beat": "reunion", "sources": ["HOPE", "LUDAN"], "note": "Cane, New Grand Hotel (HOPE); MacArthur rose and embraced him (Casey letter, LUDAN)."},
        {"beat": "missouri", "sources": ["CITINO", "HOPE"]},
        {"beat": "pen", "sources": ["HOPE", "CITINO", "WOLF"], "note": "First pen mid-signature (HOPE); a pen each to Wainwright and Percival (CITINO, WOLF)."},
        {"beat": "home", "sources": ["HOPE", "MEMOIR", "HOMEFILM"], "note": "More than 100,000 at the Monument; the 'SKINNY' banner is visible in the newsreel."},
        {"beat": "truman", "sources": ["TRUMANCIT", "MEMOIR", "STERNER"]},
        {"beat": "diary2", "sources": ["DIARY", "WIKI"], "note": "Truman diary 17 Jun 1945, verbatim."},
        {"beat": "death", "sources": ["WIKI", "BRIT"], "note": "Died 2 Sep 1953 in San Antonio."},
    ],
    "notUsed": [
        "MacArthur's departure date (11 or 12 March 1942): not said.",
        "Reunion wording ('your old corps' vs 'glad to see you'): not quoted.",
        "Number of pens (five, plus Mrs. MacArthur's red one): not said.",
    ],
}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
words = sum(len(x["text"].split()) for x in B)
print(f"{len(B)} beats, {words} words")
