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
    "BR": ("brest_surrender_1944", 1), "TC": ("tunisian_campaign_1943", 1), "TV": ("tunisian_victory_1944", 1),
    "PA": ("paris_aug_1944", 1), "RV": ("the_river_1938", 1), "TRN": ("passenger_train_1940", 1),
}


def T(m, s=0.0):
    return m * 60 + s

ML = "D. R. Mallett, Hitler's Generals in America (2013)"
SK = "J. R. Skates, “German Prisoners of War in Mississippi 1943–1946”, Mississippi History Now (MDAH, 2001)"
RV_TAG = "The Mississippi · from The River (Farm Security Administration, 1938)"
TC_TAG = "German and Italian prisoners, Tunisia, May 1943 · U.S. Army film"
BR_TAG = "German prisoners after the surrender of Brest, September 1944 · U.S. Army film"
TRN_TAG = "Stand-in · from The Passenger Train (1940)"
# (anchor, film, source time). Context tags: ("@", anchor, text). Cards: ("#", anchor, until_anchor|None, {...})
P = [
    # 0 cold open
    [("On New Year's Day", "RV", T(2, 7.8)), ("@", "On New Year's Day", RV_TAG),
     ("#", "On New Year's Day", None, {"type": "Slug", "title": "January 1, 1946", "subtitle": "Camp Clinton, Mississippi"}),
     ("He was a paratrooper", "BR", T(0, 25.6)), ("@", "He was a paratrooper", "Brest, France, September 1944 · U.S. Army film"),
     ("He was not trying to get home", "TRN", T(5, 8.8)), ("@", "He was not trying to get home", TRN_TAG)],
    # 1 the letters
    [("One was addressed to", "RV", T(11, 57.7)), ("The letters complained", "BR", T(9, 17.1)), ("@", "The letters complained", BR_TAG),
     ("He mailed them", "TRN", T(6, 42.4))],
    # 2
    [("His name was", "BR", T(4, 41.1)), ("This is the documented story", "RV", T(4, 5.8)), ("@", "This is the documented story", RV_TAG),
     ("and what their men built", "RV", T(15, 14.3))],
    # 3 Tunisia
    [("It began with a surrender", "TC", T(0, 11.0)), ("@", "It began with a surrender", TC_TAG),
     ("#", "In May", None, {"type": "Slug", "title": "May 1943", "subtitle": "Tunisia: the Axis armies in Africa surrender"}),
     ("About two hundred", "TC", T(2, 22.5)), ("Their commander", "TC", T(13, 20.2))],
    # 4 Trent Park
    [("The most senior prisoners", "TC", T(11, 30.6)), ("They were treated almost like guests", "TC", T(7, 29.4)),
     ("And in the rooms", "PA", T(1, 21.0)), ("@", "And in the rooms", "Stand-in · U.S. soldiers, Paris, August 1944"),
     ("By the end of the war", "TC", T(13, 42.2))],
    # 5 55 generals
    [("Many of the generals", "RV", T(2, 27.5)),
     ("#", "Between", None, {"type": "Slug", "title": "55 German generals", "subtitle": "held as prisoners in the United States, 1943–1946"}),
     ("Most of them ended up", "TRN", T(7, 1.1))],
    # 6 the diary
    [("Their soldiers crossed too", "TC", T(0, 54.8)), ("He surrendered on May", "TC", T(1, 16.7)), ("Four weeks later", "TC", T(16, 15.6)),
     ("@", "Four weeks later", TC_TAG)],
    # 7 Norfolk, the train
    [("The ship docked", "RV", T(12, 17.3)), ("@", "The ship docked", "Stand-in · freighter · from The River (1938)"),
     ("#", "The ship docked", None, {"type": "LedgerTimeline", "file": "FILE 01 — ONE SOLDIER'S DIARY", "head": "From Tunisia to Mississippi",
        "rows": [{"date": "MAY 13, 1943", "text": "Surrenders in Tunisia"}, {"date": "FOUR WEEKS ON", "text": "Shipped out of Oran"},
                 {"date": "AUG. 4", "text": "Docks at Norfolk, Virginia"}, {"date": "TWO DAYS LATER", "text": "Camp Clinton, by passenger train"}],
        "source": SK}),
     ("Instead, they boarded", "TRN", T(3, 53.9)), ("@", "Instead, they boarded", TRN_TAG), ("Two days later", "TRN", T(6, 23.7))],
    # 8 Camp Clinton
    [("Camp Clinton stood", "RV", T(6, 43.1)), ("@", "Camp Clinton stood", "Mississippi, 1930s · from The River (1938)"),
     ("#", "It was one of four", None, {"type": "LedgerBars", "file": "FILE 02 — MISSISSIPPI", "head": "The state's large prisoner camps", "max": 7700,
        "bars": [{"label": "Camp McCain", "value": 7700, "figure": "7,700", "note": "near Grenada"},
                 {"label": "Camp Shelby", "value": 5300, "figure": "5,300", "note": "near Hattiesburg"},
                 {"label": "Camp Clinton", "value": 3400, "figure": "3,400", "note": "near Jackson · the generals"}],
        "source": SK})],
    # 9 the compound
    [("Inside the camp", "RV", T(21, 27.8)),
     ("#", "Inside the camp", None, {"type": "LedgerTimeline", "file": "FILE 03 — THE GENERALS' COMPOUND", "head": "How the generals lived",
        "rows": [{"date": "HOUSING", "text": "Private bungalows, two generals each"}, {"date": "AIDES", "text": "One aide per bungalow"},
                 {"date": "WORK", "text": "Not required"}],
        "source": "Jackson Clarion-Ledger, 1996; " + SK})],
    # 10 von Arnim
    [("the senior general", "TRN", T(5, 27.5)), ("@", "the senior general", TRN_TAG), ("Some people in Jackson", "RV", T(11, 57.7)), ("It may only be a story", "RV", T(6, 43.1))],
    # 11 food, music
    [("The rest of the camp", "TC", T(13, 20.2)), ("@", "The rest of the camp", TC_TAG), ("There was beer", "TC", T(15, 31.8)), ("The most popular class", "TC", T(4, 34.1))],
    # 12 the plan
    [("Their men were put to work", "RV", T(21, 47.5)), ("@", "Their men were put to work", "Cotton pickers · from The River (1938)"), ("The Army Corps of Engineers", "RV", T(15, 33.9)),
     ("@", "The Army Corps of Engineers", "Mississippi flood · from The River (1938)"), ("It wanted to build", "RV", T(19, 29.9))],
    # 13 the workers
    [("In August", "RV", T(17, 51.6)), ("@", "In August", "Stand-in · levee work · from The River (1938)"),
     ("#", "In August", None, {"type": "LedgerBars", "file": "FILE 04 — THE RIVER MODEL", "head": "Prisoners on the job, 1943", "max": 1800,
        "bars": [{"label": "August 1943", "value": 200, "figure": "200", "note": "the first Afrika Korps prisoners"},
                 {"label": "December 1943", "value": 1800, "figure": "~1,800", "note": "paid 90 cents for 8 hours"}],
        "source": "Wikipedia, “Mississippi River Basin Model” (U.S. Army Corps of Engineers history)"})],
    # 14 digging
    [("With hundreds of wheelbarrows", "RV", T(20, 28.9)), ("The finished model", "RV", T(21, 8.2)), ("The river's path", "RV", T(2, 7.8))],
    # 15 it worked
    [("It worked", "RV", T(15, 53.6)), ("#", "It worked", None, {"type": "Slug", "title": "1952", "subtitle": "Missouri River flood: about $65 million in damage avoided"}),
     ("By one estimate", "RV", T(19, 10.2)), ("The men who dug it", "RV", T(19, 49.5))],
    # 16 what the Americans wanted
    [("At first", "BR", T(7, 54.0)), ("@", "At first", "U.S. generals at Brest, September 1944 · U.S. Army film"), ("A few were questioned", "BR", T(8, 56.6)), ("The rest were treated", "BR", T(9, 47.7)),
     ("The British, with their microphones", "PA", T(1, 31.8))],
    # 17
    [("As the war ended", "BR", T(2, 6.0)), ("The Soviet Union was about", "TC", T(13, 42.2)),
     ("#", "As the war ended", None, {"type": "LedgerTimeline", "file": "FILE 05 — WHAT THE AMERICANS WANTED", "head": "From prisoners to sources",
        "rows": [{"date": "1943–44", "text": "A few weeks of questioning, then little interest"}, {"date": "1945", "text": "Generals who fought the Red Army"},
                 {"date": "IN SECRET", "text": "Studies written in breach of the Geneva Convention"}],
        "source": f"{ML}; review by P. J. Springer, FPRI (2016)"})],
    # 18
    [("The generals were not all alike", "TC", T(12, 58.3)), ("@", "The generals were not all alike", TC_TAG), ("Those captured after", "BR", T(8, 46.4)),
     ("@", "Those captured after", BR_TAG), ("Generals who doubted Hitler", "BR", T(9, 37.5)), ("Some were set to work", "PA", T(1, 21.0))],
    # 19 Paris
    [("One of the men", "PA", T(2, 58.2)), ("@", "One of the men", "Paris, August 1944 · U.S. Army film"),
     ("#", "In August", None, {"type": "LedgerQuote", "file": "FILE 06 — PARIS", "head": "Hitler's order, 23 August 1944",
        "before": "Paris must not fall into the hands of the enemy, ", "key": "except as a field of ruins", "after": ".",
        "who": "Adolf Hitler to General Dietrich von Choltitz", "source": "Order of 23 Aug. 1944 (“…nur als Trümmerfeld…”), Wikipedia, “Dietrich von Choltitz”"})],
    # 20
    [("On August twenty-fifth", "PA", T(2, 4.2)), ("In his memoir", "PA", T(6, 55.9)), ("Either way", "PA", T(3, 41.4))],
    # 21 Brest
    [("Ramcke had made", "BR", T(3, 29.5)), ("@", "Ramcke had made", "Brest, September 1944 · U.S. Army film"), ("Hitler ordered him", "BR", T(3, 39.8)),
     ("The siege lasted", "BR", T(1, 6.4))],
    # 22 credentials
    [("On September nineteenth", "BR", T(4, 20.6)), ("Ramcke surrendered", "BR", T(7, 24.6)),
     ("#", "When he asked", None, {"type": "LedgerQuote", "file": "FILE 07 — BREST, 19 SEPT. 1944", "head": "Ramcke asked for credentials",
        "before": "", "key": "These are my credentials", "after": ".", "who": "Brig. Gen. Charles Canham, U.S. 8th Infantry Division, pointing to his soldiers",
        "source": "Wikipedia, “Battle for Brest”"}),
     ("Thirty-eight thousand", "BR", T(9, 27.3))],
    # 23 the reports
    [("An American interrogator", "BR", T(4, 51.3)), ("There, he boasted", "BR", T(3, 50.0)), ("Choltitz thought", "BR", T(0, 46.0)),
     ("#", "At Trent Park", None, {"type": "LedgerQuote", "file": "FILE 08 — TRENT PARK REPORT", "head": "On General Ramcke",
        "before": "If there [was] to be such a thing as a list of especially dangerous men to be kept under surveillance, General Ramcke ought to qualify as ",
        "key": "one of the first candidates", "after": ".", "who": "British report, Trent Park, 1944", "source": f"Quoted in {ML}, p. 44"})],
    # 24
    [("By the end of", "RV", T(13, 16.3)), ("@", "By the end of", RV_TAG), ("The comforts were shrinking", "TRN", T(6, 42.4))],
    # 25 the escape
    [("On January first", "RV", T(11, 18.3)),
     ("#", "On January first", None, {"type": "LedgerTimeline", "file": "FILE 09 — RAMCKE, 1946", "head": "The escape",
        "rows": [{"date": "JAN. 1, 1946", "text": "Slips out, posts letters to Eastland and Price"}, {"date": "DISCOVERED", "text": "Moved to Camp Shelby"},
                 {"date": "FOUR DAYS", "text": "Solitary confinement, bread and water"}],
        "source": f"{ML}, pp. 128–129"})],
    # 26 the other version
    [("A local newspaper", "RV", T(10, 58.7)),
     ("#", "A local newspaper", None, {"type": "Slug", "title": "Another version", "subtitle": "Jackson Clarion-Ledger, 1996"}),
     ("checked into the Heidelberg", "TRN", T(5, 27.5)), ("@", "checked into the Heidelberg", TRN_TAG), ("No copy of that letter", "RV", T(13, 36.0))],
    # 27 Ramcke's trial
    [("In March", "BR", T(0, 35.8)), ("France put him on trial", "BR", T(5, 52.6)), ("@", "France put him on trial", "Brest, September 1944 · U.S. Army film"),
     ("#", "he was convicted", None, {"type": "Slug", "title": "March 21, 1951", "subtitle": "Ramcke convicted in France · free three months later"})],
    # 28 release
    [("Von Arnim was freed", "TRN", T(3, 53.9)), ("Many of the ordinary prisoners", "RV", T(22, 26.8)), ("@", "Many of the ordinary prisoners", "Cotton pickers · from The River (1938)"),
     ("One state historian", "RV", T(2, 27.5))],
    # 29 the model today
    [("The river model stayed", "RV", T(20, 28.9)), ("The city of Jackson", "RV", T(7, 2.7)), ("In 2018", "RV", T(4, 45.1)), ("Volunteers are still", "RV", T(21, 27.8))],
    # 30 comment ask
    [("If your family", "RV", T(4, 25.4)),
     ("#", "If your family", None, {"type": "Slug", "title": "A Camp Clinton story in your family?", "subtitle": "Tell us in the comments"})],
    # 31 echo
    [("In nineteen ninety-six", "RV", T(3, 6.8)), ("The bungalows are gone", "RV", T(6, 43.1)), ("The river they never saw", "RV", T(2, 7.8))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (1, "One was addressed to", None, "eastland.jpg", "01", "James Eastland", "U.S. Senator James O. Eastland of Mississippi", f"U.S. Senate · public domain · {WC}", {"focus": [0.5, 0.35]}),
    (1, "Another went to", None, "byron_price.jpg", "02", "Byron Price", "Byron Price, director of the U.S. Office of Censorship during the war", f"Public domain · {WC}", {"focus": [0.5, 0.25]}),
    (2, "His name was", None, "ramcke_brest_1944.jpg", "03", "Hermann-Bernhard Ramcke", "Ramcke under American guard after the surrender of Brest, September 1944 (badges blurred)", f"U.S. Army Signal Corps · public domain · {WC}", {"focus": [0.45, 0.3]}),
    (3, "About two hundred", None, "tunisia_pow_trucks_1943.jpg", "04", "Tunisia, May 1943", "U.S. Army trucks carry German prisoners to a camp near Mateur, Tunisia, 10 May 1943", f"U.S. Army Signal Corps · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (4, "to a country house", None, "trent_park_house.jpg", "05", "Trent Park", "Trent Park, north London, where captured German generals were secretly recorded", f"Poliphilo · CC0 · {WC}", {"focus": [0.5, 0.5]}),
    (6, "and was held in a barbed-wire", None, "tunisia_pow_camp_aerial_1943.jpg", "06", "The cage", "A prisoner-of-war enclosure four miles west of Mateur, Tunisia, 9 May 1943", f"U.S. Army Signal Corps · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (12, "It wanted to build", None, "river_model_overview.jpg", "12", "The river model", "Part of the Mississippi River Basin Model near Jackson, looking up the Ohio River", f"U.S. Army Corps of Engineers · public domain · {WC}", {"focus": [0.5, 0.45]}),
    (14, "The finished model", None, "river_model_aerial.jpg", "14", "200 acres", "The Mississippi River Basin Model from the air", f"U.S. Army Corps of Engineers · public domain · {WC}", {"focus": [0.45, 0.5]}),
]


def photo_items():
    import json as _j
    from PIL import Image
    crops = _j.load(open(ROOT / "tools/crops.json", encoding="utf-8"))
    for k, (pi, a, b, img, no, title, cap, src, extra) in enumerate(PHOTOS):
        W, H = Image.open(ROOT / f"assets/stills/{img}").size
        extra = dict(extra)
        x, y, w, h = extra.pop("crop", None) or crops[img]
        card = {"type": "PhotoCard", "image": img, "aspect": round(w * W / (h * H), 3), "crop": [x, y, w, h], "frameNo": no,
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
                elif card["type"] == "PhotoCard":
                    card["dur"] = 6.5
                else:  # full card runs to the end of its paragraph (7-12 s)
                    card["end"] = min(card["start"] + 12.0, max(card["start"] + 7.0, paras[pi]["end"] + 0.3))
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
    # subscribe card at ~36 % of the runtime (silent, as in the reference), on footage between cards
    sub_t = total * 0.36
    busy = [(o["start"], o["end"]) for o in overlays if o["type"] != "ContextTag"]
    while any(a - 1 < sub_t < b + 1 or a - 1 < sub_t + 5 < b + 1 for a, b in busy):
        sub_t += 1.0
    overlays.append({"type": "Slug", "title": CHANNEL["subscribe"], "subtitle": CHANNEL["tagline"], "start": round(sub_t, 3), "end": round(sub_t + 4.5, 3)})
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
