"""Shot plan -> build/storyboard.json.

Every paragraph lists its shots as (anchor phrase, film, source second). A cut lands ~0.1 s before
the first word of its anchor phrase (word times from audio/words.json), the way the reference
lands cuts on the spoken noun. Overlays (cards, lower thirds, context labels) are anchored the same
way. Shots longer than MAX_SHOT are split at the source film's own shot boundaries so the picture
keeps changing every few seconds, as in the reference (median shot ~4 s).
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
# Channel branding for the silent subscribe card; set to your own channel name before publishing.
CHANNEL = {"subscribe": "Subscribe to WWII Frontlines", "tagline": "Prisoner of war stories, documented"}
MAX_SHOT = 6.5
CUT_LEAD = 0.1

F = {  # film key -> (file in assets/footage, fraction of height kept)
    "SN": ("surrender_newsreel_1945", 1), "ADC": ("missouri_adc_1945", 1), "NPC": ("missouri_npc_1945", 1),
    "YOK": ("wainwright_yokohama_1945", 1), "HOME": ("wainwright_home_1945", 1), "MAN": ("macarthur_manila_1945", 1),
    "CR": ("corregidor_newsreel_1945", 1), "RP": ("rescued_pows_leyte_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


MOR = "Louis Morton, The Fall of the Philippines (U.S. Army, 1953)"
WOS = "Wainwright's own story, King Features newspaper serial, 1945"
WGS = "General Wainwright's Story (1946)"
MAC = "Douglas MacArthur, Reminiscences (1964)"
HOH = "MacArthur's radiogram to Marshall, 1942, as quoted by C. Douglas Sterner (Home of Heroes)"
WC = "Wikimedia Commons"
SN_TAG = "USS Missouri, Tokyo Bay, 2 September 1945 · United News newsreel"
ADC_TAG = "USS Missouri, 2 September 1945 · U.S. Army Signal Corps film"
YOK_TAG = "General Wainwright, Yokohama, September 1945 · U.S. Army Signal Corps film"
HOME_TAG = "Wainwright comes home, September 1945 · newsreel"
MAN_TAG = "MacArthur's plane Bataan, Manila, August 1945 · U.S. Army Signal Corps film"
CR_TAG = "Corregidor · United News newsreel, February 1945"
CRW_TAG = "Corregidor in ruins, February 1945 · United News newsreel"
RP_TAG = "Stand-in · an American prisoner freed from a Japanese camp, 1945 · U.S. Army film"
P = [
    # 0 the Missouri
    [("The", "SN", T(0, 40.0)), ("@", "aboard the battleship", SN_TAG),
     ("#", "The second of September", None, {"type": "Slug", "title": "September 2, 1945", "subtitle": "USS Missouri · Tokyo Bay"}),
     ("The Japanese delegation has signed", "SN", T(4, 32.0)), ("General Douglas MacArthur steps", "SN", T(2, 40.0)),
     ("Will General Percival", "SN", T(3, 23.0)), ("A thin officer", "SN", T(5, 40.5))],
    # 1 the pen
    [("MacArthur sits down", "SN", T(5, 57.5)), ("Halfway through", "SN", T(6, 15.0)),
     ("#", "Three years earlier", None, {"type": "LedgerQuote", "file": "FILE 01 — THE RADIOGRAM", "head": "MacArthur on Wainwright's Medal of Honor, July 1942",
        "before": "", "key": "The citation proposed does not represent the truth.", "after": " … award of the Medal of Honor to General Wainwright would be a grave injustice …",
        "who": "Gen. Douglas MacArthur to Gen. George C. Marshall", "source": HOH}),
     ("And for three years", "YOK", T(6, 14.5)), ("@", "And for three years", YOK_TAG)],
    # 2 this is the story
    [("This is the documented", "CR", T(4, 14.0)), ("@", "This is the documented", CR_TAG), ("the man MacArthur left", "SN", T(2, 48.0)),
     ("the surrender he never", "YOK", T(6, 39.0)), ("@", "the surrender he never", YOK_TAG),
     ("and the day he found out", "HOME", T(0, 22.0)), ("@", "and the day he found out", HOME_TAG)],
    # 3 March 1942
    [("March", "CR", T(0, 47.5)), ("@", "March", CR_TAG),
     ("#", "March", None, {"type": "Slug", "title": "March 1942", "subtitle": "Corregidor · Manila Bay, Philippines"}),
     ("On the island fortress", "CR", T(0, 53.5)), ("MacArthur has orders", "MAN", T(7, 6.0)), ("@", "MacArthur has orders", "General MacArthur · U.S. Army Signal Corps film, 1945"),
     ("Before he goes", "YOK", T(4, 37.0))],
    # 4 the promise
    [("MacArthur tells him", "CR", T(4, 38.5)), ("He hands Wainwright a box", "SN", T(2, 51.0)),
     ("And he promises him a third star", "YOK", T(5, 40.0)), ("@", "And he promises him a third star", "General Wainwright, September 1945 · U.S. Army Signal Corps film"),
     ("Wainwright answers that he will", "YOK", T(6, 10.0))],
    # 5 the PT boats
    [("That night", "CR", T(4, 50.5)), ("@", "That night", "Stand-in · ships off Corregidor, 1945 · United News newsreel"), ("A week later", "MAN", T(7, 25.0)),
     ("Behind him", "CR", T(4, 14.0)), ("@", "Behind him", CR_TAG), ("with no help on the way", "CR", T(4, 39.0))],
    # 6 the surrender
    [("On the ninth of April", "CR", T(4, 41.0)), ("@", "On the ninth of April", "Stand-in · bombardment of Corregidor, February 1945 · United News newsreel"), ("Ko-reg-ih-door holds on", "CR", T(4, 45.0)),
     ("On the morning", "YOK", T(7, 15.0)), ("@", "On the morning", YOK_TAG),
     ("#", "He will sacrifice", None, {"type": "LedgerQuote", "file": "FILE 02 — THE DECISION", "head": "Corregidor, 6 May 1942, 10 a.m.",
        "before": "Wainwright decided ", "key": "to sacrifice one day of freedom in exchange for several thousand lives.", "after": "",
        "who": "The U.S. Army's official history", "source": f"{MOR}, ch. XXXI"})],
    # 7 the message
    [("He sends a last message", "RP", T(1, 30.5)),
     ("#", "He sends a last message", None, {"type": "LedgerQuote", "file": "FILE 03 — LAST MESSAGE", "head": "Wainwright to President Roosevelt, 6 May 1942",
        "before": "With broken heart and head bowed in sadness ", "key": "but not in shame", "after": " … my troops and I have accomplished all that is humanly possible …",
        "who": "Lt. Gen. Jonathan M. Wainwright", "source": f"Radiogram quoted in {MOR}"}),
     ("At noon the white flag", "CR", T(4, 51.0)), ("@", "At noon the white flag", CR_TAG)],
    # 8 Homma
    [("But that is not enough", "CR", T(0, 48.0)), ("@", "But that is not enough", CR_TAG), ("He wants every American", "CR", T(0, 53.5)),
     ("When Wainwright tries", "YOK", T(8, 4.0)), ("@", "When Wainwright tries", YOK_TAG),
     ("Wainwright thinks of the eleven", "RP", T(6, 46.3)), ("@", "Wainwright thinks of the eleven", RP_TAG), ("The next night", "YOK", T(4, 37.0)), ("@", "The next night", YOK_TAG)],
    # 9 MacArthur's reaction
    [("In Australia", "MAN", T(7, 24.0)), ("@", "In Australia", "General MacArthur · U.S. Army Signal Corps film, 1945"),
     ("#", "To General Marshall", None, {"type": "LedgerQuote", "file": "FILE 04 — UNBALANCED", "head": "MacArthur to Marshall, 9 May 1942",
        "before": "I believe ", "key": "Wainwright has temporarily become unbalanced.", "after": "",
        "who": "Gen. Douglas MacArthur", "source": f"Radiogram quoted in {MOR}, ch. XXXII"})],
    # 10 the medal refused
    [("Two months later", "YOK", T(5, 45.0)), ("@", "Two months later", "General Wainwright, September 1945 · U.S. Army Signal Corps film"),
     ("#", "MacArthur answers with a radiogram", None, {"type": "LedgerQuote", "file": "FILE 05 — THE VETO", "head": "MacArthur on the Medal of Honor, July 1942",
        "before": "", "key": "It would be a grave mistake which later on might well lead to embarrassing repercussions to make this award.", "after": "",
        "who": "Gen. Douglas MacArthur to Gen. George C. Marshall", "source": HOH}),
     ("Marshall withdraws", "YOK", T(6, 20.0))],
    # 11 never sees it
    [("Wainwright never sees", "YOK", T(6, 27.0))],
    # 12 the camps
    [("He is held first", "RP", T(1, 30.5)), ("@", "He is held first", RP_TAG),
     ("By October", "RP", T(6, 46.3))],
    # 13 Karenko
    [("At Kah-ren-ko a Japanese correspondent", "YOK", T(6, 51.0)), ("@", "At Kah-ren-ko a Japanese correspondent", YOK_TAG),
     ("#", "But afterwards he sits down", None, {"type": "LedgerTimeline", "file": "FILE 06 — THE DIARY", "head": "His reasons, written at Karenko, 1942",
        "rows": [{"date": "NO HELP", "text": "None was coming to Corregidor"}, {"date": "A DAY OR TWO", "text": "The island would have fallen anyway"},
                 {"date": "MALINTA TUNNEL", "text": "About 1,000 sick and wounded, and 125 nurses"},
                 {"date": "IF HE FOUGHT ON", "text": "Some would have called him a fool, or a criminal"}],
        "source": f"{WOS} (as paraphrased)"})],
    # 14 moved again
    [("He is moved again", "RP", T(6, 52.0)),
     ("#", "He is moved again", None, {"type": "LedgerTimeline", "file": "FILE 07 — THE CAMPS", "head": "Wainwright's captivity, 1942–1945",
        "rows": [{"date": "JUNE 1942", "text": "Tarlac, Luzon"}, {"date": "AUG 1942", "text": "Karenko, Formosa"},
                 {"date": "1943–1944", "text": "Tamazato and Muksaq, Formosa"}, {"date": "DEC 1944", "text": "Sian, Manchuria, with 15 other senior prisoners"}],
        "source": f"{WOS}; {WGS}"})],
    # 15 subscribe
    [("If you want more", "YOK", T(7, 28.0)),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 16 the OSS
    [("On the sixteenth of August", "CR", T(3, 29.0)), ("@", "On the sixteenth of August", "Stand-in · parachutes over Corregidor, February 1945 · United News newsreel"),
     ("#", "On the sixteenth of August", None, {"type": "Slug", "title": "August 16, 1945", "subtitle": "An OSS team parachutes onto Mukden airfield, Manchuria"}),
     ("Three days later", "YOK", T(4, 50.0)), ("@", "Three days later", YOK_TAG)],
    # 17 the question
    [("He has one question", "YOK", T(7, 40.0)),
     ("#", "He has one question", None, {"type": "LedgerQuote", "file": "FILE 08 — THE QUESTION", "head": "Sian, Manchuria, 19 August 1945",
        "before": "Wainwright asked ", "key": "what people at home thought of him.", "after": " He was told he was a hero. He was not convinced.",
        "who": "As told by the OSS men who found him", "source": "John Mancini, Warfare History Network; Hal Leith oral history, National WWII Museum"})],
    # 18 the way out
    [("It takes them a week", "MAN", T(8, 21.0)), ("@", "It takes them a week", "Stand-in · a transport plane, 1945 · U.S. Army Signal Corps film"),
     ("On the twenty-eighth of August", "YOK", T(8, 5.0)), ("@", "On the twenty-eighth of August", YOK_TAG)],
    # 19 Bataan lands
    [("Two days later MacArthur lands", "MAN", T(8, 0.5)), ("@", "Two days later MacArthur lands", MAN_TAG), ("On the evening", "MAN", T(8, 19.0)),
     ("#", "On the evening of the thirty-first", None, {"type": "Slug", "title": "August 31, 1945", "subtitle": "New Grand Hotel · Yokohama"})],
    # 20 two versions
    [("What happened next", "YOK", T(5, 40.0)), ("@", "What happened next", YOK_TAG),
     ("#", "In his memoirs", None, {"type": "LedgerQuote", "file": "FILE 09 — TWO VERSIONS", "head": "The reunion, as each man told it",
        "before": "Wainwright, 1945: MacArthur said only that he was glad to see him. MacArthur, 1964: ", "key": "your old corps is yours when you want it.", "after": "",
        "who": "Wainwright's own story (1945); MacArthur's Reminiscences (1964)", "source": f"{WOS}; {MAC}"})],
    # 21 the photograph
    [("The photograph", "YOK", T(6, 2.0)),],
    # 22 the pens
    [("Two days later he stands", "SN", T(5, 41.0)), ("@", "Two days later he stands", SN_TAG),
     ("#", "MacArthur took five pens", None, {"type": "LedgerTimeline", "file": "FILE 10 — THE PENS", "head": "USS Missouri, 2 September 1945",
        "rows": [{"date": "PEN 1", "text": "Halfway through his name · to Gen. Wainwright"}, {"date": "PEN 2", "text": "To Gen. Percival, who surrendered Singapore"},
                 {"date": "THREE MORE", "text": "Set aside for American institutions"}, {"date": "LAST", "text": "His wife's small red pen"}],
        "source": f"{WOS}; National WWII Museum (2020)"}),
     ("Two men who had signed", "SN", T(6, 23.0))],
    # 23 Baguio
    [("The next day", "ADC", T(8, 49.0)), ("@", "The next day", ADC_TAG),
     ("The American general who took", "ADC", T(9, 29.0))],
    # 24 the medal revived
    [("On the fifth of September", "HOME", T(0, 34.0)), ("@", "On the fifth of September", HOME_TAG)],
    # 25 Washington
    [("On the tenth", "HOME", T(0, 15.5)),
     ("#", "On the tenth", None, {"type": "Slug", "title": "September 10, 1945", "subtitle": "Washington, D.C."}),
     ("More than a hundred thousand", "HOME", T(1, 17.0)), ("Remember Bataan", "HOME", T(1, 24.0)),
     ("Then he went to the White House", "HOME", T(1, 54.0)), ("In the Rose Garden", "HOME", T(2, 6.5)),
     ("#", "fastened the Medal of Honor", None, {"type": "LedgerQuote", "file": "FILE 11 — THE CITATION", "head": "Medal of Honor, 10 September 1945",
        "before": "", "key": "The final stand on beleaguered Corregidor … commanded the admiration of the nation's allies.", "after": "",
        "who": "Citation read by President Truman", "source": "Truman Library, Public Papers, 1945"}),
     ("Three days later", "HOME", T(2, 25.0))],
    # 26 Truman's diary
    [("In his private diary", "HOME", T(2, 37.0)),
     ("#", "In his private diary", None, {"type": "LedgerQuote", "file": "FILE 12 — TRUMAN'S DIARY", "head": "17 June 1945",
        "before": "", "key": "We'd have had a real general and a fighting man if we had Wainwright …", "after": "",
        "who": "President Harry S. Truman, private diary", "source": "Truman Library transcript, via PBS American Experience"})],
    # 27 comments
    [("If someone in your family", "HOME", T(0, 59.0)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Was your family there?", "subtitle": "Bataan, Corregidor or the camps · tell us in the comments"})],
    # 28 after the war
    [("Jonathan Wainwright commanded", "HOME", T(2, 50.0)),],
    # 29 the date
    [("He died on the second", "SN", T(8, 15.0)), ("@", "He died on the second", SN_TAG),
     ("In nineteen forty-five", "SN", T(6, 16.0))],
]

PHOTOS = [
    (3, "Before he goes", None, "wainwright_portrait.jpg", "03", "Lt. Gen. Jonathan M. Wainwright", "\"Skinny\" · U.S. Navy photograph", f"National Archives 80-G-354136 · public domain · {WC}", {}),
    (4, "MacArthur tells him", None, "wainwright_macarthur_1941.jpg", "04", "MacArthur and Wainwright", "The Philippines, 10 October 1941", f"U.S. Army · public domain · {WC}", {}),
    (8, "That afternoon", None, "bataan_surrender_1942.jpg", "08", "Cabcaben, 6 May 1942", "Wainwright (left) faces General Homma's officers · captured Japanese photograph", f"public domain · {WC}", {}),
    (12, "He is held first", None, "generals_captivity_1942.jpg", "12", "American generals in captivity", "July 1942 · Wainwright seated third from left, beside the Japanese commandant", f"public domain · {WC}", {}),
    (13, "Wainwright answers", None, "wainwright_captive_1942.jpg", "13", "A prisoner at the microphone", "Wainwright reading a statement under Japanese guard, 1943", f"public domain · {WC}", {}),
    (21, "The photograph", None, "reunion_1945.jpg", "21", "Yokohama, 31 August 1945", "MacArthur and Wainwright at the New Grand Hotel, their first meeting since Corregidor", f"U.S. Army Signal Corps 111-SC-210621 · public domain · {WC}", {}),
    (22, "Two days later he stands", None, "missouri_signing.jpg", "22", "USS Missouri, 2 September 1945", "Wainwright and Percival stand behind MacArthur as he signs", f"U.S. Navy · public domain · {WC}", {}),
    (23, "At Bah-gee-oh", None, "baguio_1945.jpg", "23", "Baguio, 3 September 1945", "General Yamashita surrenders the Japanese forces in the Philippines", f"U.S. Navy NH 97276 · public domain · {WC}", {}),
    (25, "Three days later", None, "broadway_1945.jpg", "25", "New York, 13 September 1945", "The Wainwright motorcade on lower Broadway", f"Al Aumuller, NYWT&S · Library of Congress · no known restrictions · {WC}", {}),
    (28, "Jonathan Wainwright commanded", None, "wainwright_official.jpg", "28", "Gen. Jonathan M. Wainwright", "Commanding the Fourth Army, about 1946", f"U.S. Army · public domain · {WC}", {}),
    (5, "A week later", None, "adelaide_1942.jpg", "05", "Adelaide, 20 March 1942", "MacArthur and his wife on their way to Melbourne after leaving the Philippines", f"public domain · {WC}", {}),
]


def photo_items():
    import json as _j
    from PIL import Image
    crops = _j.load(open(ROOT / "tools/crops.json", encoding="utf-8"))
    for k, (pi, a, b, img, no, title, cap, src, extra) in enumerate(PHOTOS):
        W, H = Image.open(ROOT / f"assets/stills/{img}").size
        extra = dict(extra)
        x, y, w, h = extra.pop("crop", None) or crops[img]
        aspect = round(w * W / (h * H), 3)
        if extra.pop("style", None) == "print":  # ArchivePrint: print on dark graph paper, tab "ARCHIVE · <label>"
            card = {"type": "ArchivePrint", "image": img, "aspect": aspect, "crop": [x, y, w, h],
                    "label": extra.pop("label", title), "source": src, **extra}
        else:
            card = {"type": "PhotoCard", "image": img, "aspect": aspect, "crop": [x, y, w, h], "frameNo": no,
                    "title": title, "caption": cap, "source": src, "side": "left" if k % 2 == 0 else "right", **extra}
        P[pi].append(("#", a, b, card))


def tag(t):
    return t


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def main():
    photo_items()
    paras = json.load(open(ROOT / "audio/paragraphs.json", encoding="utf-8"))
    words = json.load(open(ROOT / "audio/words.json", encoding="utf-8"))  # per paragraph: [{text, start, end}] (spoken form)
    total = max(p["end"] for p in paras) + 1.5
    assert len(paras) == len(P), (len(paras), len(P))

    def at(pi, phrase):
        ws = words[pi]
        target = [norm(x) for x in phrase.split()]
        toks = [norm(w["text"]) for w in ws]
        for i in range(len(toks) - len(target) + 1):
            if toks[i:i + len(target)] == target:
                return max(0.0, ws[i]["start"] - CUT_LEAD)
        raise SystemExit(f"anchor not found in paragraph {pi}: {phrase!r}\n{' '.join(toks)}")

    SCENES = {"Section", "Chart", "IconCount", "ObjectTurn"}  # remotion/src/scenes.tsx
    TIMEKEYS = {"t", "t0", "t1", "at", "labelAt", "labelTo", "beamAt"}

    def sync_times(o, when, key=None):
        if isinstance(o, dict):
            return {k: sync_times(v, when, k) for k, v in o.items()}
        if isinstance(o, list):
            if key == "dig":
                return [when(v) if isinstance(v, str) else v for v in o]
            return [sync_times(v, when) for v in o]
        if key in TIMEKEYS and isinstance(o, str):
            return when(o)
        return o

    def said(pi, phrase):  # first and last word times of a phrase in the spoken text
        ws, target = words[pi], [norm(x) for x in phrase.split()]
        toks = [norm(w["text"]) for w in ws]
        for i in range(len(toks) - len(target) + 1):
            if toks[i:i + len(target)] == target:
                return ws[i]["start"], ws[i + len(target) - 1]["end"]
        raise SystemExit(f"highlight not spoken in paragraph {pi}: {phrase!r}; spoken: {' '.join(toks)}")

    docs = json.load(open(ROOT / "tools/doc_spans.json", encoding="utf-8")) if (ROOT / "tools/doc_spans.json").exists() else {}
    cuts, overlays = [], []
    for pi, items in enumerate(P):
        for it in items:
            if it[0] == "@":
                overlays.append({"type": "ContextTag", "text": tag(it[2]), "start": at(pi, it[1]) + 0.4, "dur": 4.5})
            elif it[0] == "#":
                card = dict(it[3]); card["start"] = at(pi, it[1])
                if it[2]:
                    card["end"] = at(pi, it[2]) + 0.35
                elif card["type"] == "Slug":
                    card["dur"] = 5.5
                elif card["type"] in ("PhotoCard", "ArchivePrint"):
                    card["dur"] = 6.5
                elif card["type"] in SCENES:  # reconstruction scenes may run the whole paragraph (up to 30 s)
                    card["end"] = min(card["start"] + 30.0, max(card["start"] + 8.0, paras[pi]["end"] + 0.3))
                else:  # full card runs to the end of its paragraph (7-12 s)
                    card["end"] = min(card["start"] + 12.0, max(card["start"] + 7.0, paras[pi]["end"] + 0.3))
                if card["type"] in SCENES:  # any time field given as a phrase = when that phrase is spoken (s from card start)
                    card = sync_times(card, lambda ph, pi=pi, c0=card["start"]: round(said(pi, ph)[0] - c0, 3))
                if card["type"] == "LedgerDocument":  # spans: [{"doc": key in tools/doc_spans.json, "say": spoken words}]
                    spans = []
                    for sp in card["spans"]:
                        d = docs[sp["doc"]]
                        t0, t1 = said(pi, sp["say"])
                        card.update(image=d["image"], pw=d["pw"], ph=d["ph"])
                        spans.append({"rects": d["rects"], "at": round(t0 - card["start"], 3), "dur": round(t1 - t0, 3)})
                    card["spans"] = spans
                    card["end"] = max(card["end"], card["start"] + spans[-1]["at"] + spans[-1]["dur"] + 0.7)
                overlays.append(card)
            else:
                t = 0.0 if (pi == 0 and it is items[0]) else at(pi, it[0])
                cuts.append({"t": t, "film": it[1], "in": it[2], "anchor": it[0]})
    cuts.sort(key=lambda c: c["t"])
    shots = []
    for i, c in enumerate(cuts):
        end = cuts[i + 1]["t"] if i + 1 < len(cuts) else total
        shots.append({"start": round(c["t"], 3), "end": round(end, 3), "film": c["film"], "file": F[c["film"]][0], "keep": F[c["film"]][1], "in": c["in"], "anchor": c["anchor"]})
    # split long shots at the source film's own cut points
    out = []
    for s in shots:
        bounds = [float(x) for x in open(ROOT / f"build/shots/{s['file']}.txt", encoding="utf-8").read().split()] if (ROOT / f"build/shots/{s['file']}.txt").exists() else []
        t, src = s["start"], s["in"]
        while s["end"] - t > MAX_SHOT:
            nxt = [b for b in bounds if src + 2.5 < b < src + MAX_SHOT]
            step = (nxt[-1] - src) if nxt else 4.5
            jump = [b for b in bounds if b > src + step + 0.05]
            out.append({**s, "start": round(t, 3), "end": round(t + step, 3), "in": round(src, 3)})
            t += step
            src = (jump[0] + 0.1) if (nxt and jump and jump[0] - (src + step) < 1.0) else src + step
        out.append({**s, "start": round(t, 3), "in": round(src, 3)})
    for o in overlays:
        if "dur" in o:
            o["end"] = o["start"] + o.pop("dur")
        o["start"], o["end"] = round(o["start"], 3), round(o["end"], 3)
    # a context tag ends before the next one starts
    ctags = sorted([o for o in overlays if o["type"] == "ContextTag"], key=lambda o: o["start"])
    for a, b in zip(ctags, ctags[1:]):
        if b["start"] < a["end"]:
            a["end"] = round(b["start"] - 0.05, 3)
    # a card ends where the next one begins
    full = sorted([o for o in overlays if o["type"] != "ContextTag"], key=lambda o: o["start"])
    for a, b in zip(full, full[1:]):
        if b["start"] < a["end"]:
            a["end"] = b["start"]
    # subscribe card at ~36 % of the runtime (silent, as in the reference), on footage between cards
    sub_t = total * 0.5
    busy = [(o["start"], o["end"]) for o in overlays if o["type"] != "ContextTag"]
    while any(a - 1 < sub_t < b + 1 or a - 1 < sub_t + 5 < b + 1 for a, b in busy):
        sub_t += 1.0
    if not any(o["type"] == "SubscribeButton" for o in overlays):  # the script's own spoken ask places it; else ~50 %
        overlays.append({"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": CHANNEL["tagline"], "start": round(sub_t, 3), "end": round(sub_t + 6.0, 3)})
    # context labels never sit under a full-frame card or lower third
    cards = [(o["start"], o["end"]) for o in overlays if o["type"] != "ContextTag"]
    overlays = [o for o in overlays if o["type"] != "ContextTag" or not any(a - 0.5 < o["start"] < b or a < o["end"] < b + 0.5 for a, b in cards)]
    overlays.sort(key=lambda o: o["start"])
    for i, o in enumerate(overlays):
        o["id"] = f"o{i:02d}_{o['type']}"
    sb = {"fps": FPS, "width": 1920, "height": 1080, "duration": round(total, 3), "shots": out, "overlays": overlays}
    (ROOT / "build").mkdir(exist_ok=True)
    json.dump(sb, open(ROOT / "build/storyboard.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    lens = sorted(s["end"] - s["start"] for s in out)
    print(f"{len(out)} shots, median {lens[len(lens)//2]:.1f}s, max {lens[-1]:.1f}s, {len(overlays)} overlays, {total:.1f}s")


if __name__ == "__main__":
    main()
