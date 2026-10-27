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
    "D7": ("december_7th", 1), "KYE": ("know_your_enemy_japan", 1), "NOU": ("pows_noumea_1943", 1),
    "NOUB": ("pows_noumea_b_1943", 1), "IWO": ("iwo_nisei_prisoners_1945", 1), "SAI": ("saipan_prisoners_1944", 0.8),
    "TRN": ("passenger_train_1940", 1), "SUR": ("surrender_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

KR = "A. Krammer, “Japanese Prisoners of War in America”, Pacific Historical Review 52 (1983)"
NOU_TAG = "Stand-in · Japanese prisoners, New Caledonia, 1943"
# (anchor, film, source time). Context tags: ("@", anchor, text). Cards: ("#", anchor, until_anchor|None, {...})
P = [
    # 0 cold open: the lunch
    [("On September sixteenth", "NOU", T(6, 14.1)),
     ("#", "On September sixteenth", None, {"type": "Slug", "title": "September 16, 1944", "subtitle": "Angel Island, San Francisco Bay"}),
     ("Every one of them knew", "NOUB", T(3, 28.4)), ("@", "Every one of them knew", NOU_TAG),
     ("Torture first", "NOUB", T(6, 29.6)), ("Lunch was sukiyaki", "KYE", T(34, 13.1)), ("@", "Lunch was sukiyaki", "Japanese meal · from Know Your Enemy: Japan (1945)")],
    # 1
    [("Nobody had beaten them", "NOU", T(5, 11.8)), ("The prisoners played cards", "KYE", T(43, 39.5)),
     ("@", "The prisoners played cards", "Stand-in · Japan, 1930s · from Know Your Enemy: Japan"), ("and whispered among themselves", "NOUB", T(3, 46.5))],
    # 2
    [("They were right to wonder", "NOUB", T(7, 42.1)), ("It was the first step", "NOUB", T(10, 43.3)),
     ("Within days", "TRN", T(5, 8.8)), ("@", "Within days", "Stand-in · hill country, 1940"), ("where the walls were wired", "D7", T(4, 3.4))],
    # 3 the field code
    [("These men were rare", "SAI", T(6, 46.7)), ("The Japanese military field code", "KYE", T(8, 37.0)),
     ("#", "The Japanese military field code", None, {"type": "LedgerQuote", "file": "FILE 01 — THE FIELD CODE", "head": "What every soldier was told",
        "before": "Rather than live and bear the shame of imprisonment by the enemy, ", "key": "he should die", "after": " and avoid leaving a dishonorable name!",
        "who": "Japanese Military Field Code, 1941", "source": f"Quoted in {KR}"}),
     ("From the first shots", "D7", T(5, 40.8)), ("Midway, Guadalcanal and Tarawa", "KYE", T(60, 26.4))],
    # 4 the ice cream memo
    [("Some of that was the code", "KYE", T(4, 26.3)), ("Some of it was the Americans", "IWO", T(3, 1.0)),
     ("@", "Some of it was the Americans", "U.S. Marines with Japanese prisoners, Iwo Jima, 1945"),
     ("were reluctant to take prisoners", "IWO", T(4, 27.2)), ("One confidential intelligence memo", "IWO", T(6, 45.1)),
     ("#", "One confidential intelligence memo", None, {"type": "LedgerQuote", "file": "FILE 02 — THE FIRST LIVE PRISONER", "head": "What it took",
        "before": "It took the promise of ", "key": "three days leave and some ice cream", "after": " to bring in the first live prisoner.",
        "who": "U.S. Fourth Army, G-2, Intelligence Memo no. 4, 22 July 1943", "source": f"Quoted in {KR}"})],
    # 5
    [("On Guadalcanal", "IWO", T(5, 36.1)), ("@", "On Guadalcanal", "Stand-in · Japanese prisoner, Iwo Jima, 1945"),
     ("Thirty-three of them", "NOU", T(5, 11.8)), ("To army intelligence", "NOUB", T(7, 5.8))],
    # 6
    [("So the Americans kept", "NOUB", T(7, 24.0)), ("Under an agreement with Australia", "D7", T(25, 41.6)),
     ("The men shipped to the United States", "D7", T(26, 14.0)), ("what they might know", "NOUB", T(3, 28.4))],
    # 7 Angel Island
    [("They came ashore", "D7", T(26, 46.5)), ("They were deloused", "NOUB", T(4, 4.6)), ("@", "They were deloused", NOU_TAG),
     ("given serial numbers", "NOUB", T(0, 27.2)), ("examined for malaria", "NOU", T(0, 48.5)), ("worms and wounds", "NOU", T(1, 16.2))],
    # 8 the postal card
    [("Then came a postal card", "NOUB", T(0, 9.1)), ("Every prisoner could send one", "NOU", T(1, 30.1)),
     ("Nearly all of them asked", "IWO", T(2, 43.7)), ("Better to be thought dead", "KYE", T(18, 1.0))],
    # 9 the menu
    [("They expected to be tortured", "NOUB", T(6, 29.6)), ("They despised their captors", "KYE", T(52, 34.4)),
     ("What they got instead", "NOU", T(6, 21.0)), ("Sukiyaki and caramel pudding", "NOUB", T(2, 52.1)), ("Spaghetti and hash", "KYE", T(31, 35.7)),
     ("#", "What they got instead", None, {"type": "LedgerTimeline", "file": "FILE 03 — ANGEL ISLAND, 16 SEPT. 1944", "head": "The menu they were served",
        "rows": [{"date": "BREAKFAST", "text": "Sausages, rice, apples, coffee"}, {"date": "LUNCH", "text": "Sukiyaki, cabbage salad, caramel pudding"},
                 {"date": "DINNER", "text": "Spaghetti and hash, baked tomatoes, cocoa"}],
        "source": f"Red Cross / State Dept. inspection report, 16 Sept. 1944 (RG 389), in {KR}"})],
    # 10
    [("The meals were written down", "SAI", T(7, 19.9)), ("better fed in captivity", "KYE", T(34, 13.1)),
     ("But for a newly captured man", "NOUB", T(3, 10.3))],
    # 11 the plan
    [("The War Department had its reasons", "NOUB", T(10, 43.3)), ("@", "The War Department had its reasons", "Stand-in · U.S. officer and Japanese prisoner, New Caledonia, 1943"),
     ("frightened men made poor sources", "NOUB", T(3, 46.5)), ("Army intelligence had already learned", "IWO", T(7, 2.3)),
     ("Get the timing right", "NOUB", T(8, 0.2))],
    # 12 three phases
    [("In the first forty-eight hours", "IWO", T(5, 53.4)),
     ("#", "In the first forty-eight hours", None, {"type": "LedgerTimeline", "file": "FILE 04 — THE THREE PHASES", "head": "Fear, gratitude, silence",
        "rows": [{"date": "0–48 HOURS", "text": "Sure of torture. Useless as a source"}, {"date": "AFTER SEVERAL DAYS", "text": "Fear turns to gratitude. He talks"},
                 {"date": "10–14 DAYS ON", "text": "Used to kindness. Withdraws into a shell"}],
        "source": f"U.S. Army intelligence findings, in {KR}"}),
     ("He realized nobody was going to hurt him", "NOU", T(4, 57.9)), ("Fear turned into gratitude", "IWO", T(2, 43.7))],
    # 13
    [("That window lasted", "NOUB", T(7, 5.8)), ("Then came the third phase", "NOU", T(5, 25.6)), ("and withdrew into a shell", "NOU", T(5, 39.5)),
     ("The sukiyaki was not the end", "KYE", T(34, 13.1)), ("It started the clock", "D7", T(31, 6.1))],
    # 14 the hotel
    [("The clock ran at a place called", "TRN", T(6, 42.4)), ("@", "The clock ran at a place called", "Stand-in · hill country, 1940"),
     ("In the nineteen-twenties", "TRN", T(7, 1.1))],
    # 15
    [("The resort closed", "TRN", T(6, 23.7)), ("In May nineteen forty-two", "NOUB", T(1, 21.5)), ("The other was Fort Hunt", "NOUB", T(1, 39.7)),
     ("On paper", "TRN", T(5, 27.5)),
     ("#", "On paper", None, {"type": "Slug", "title": "P.O. Box 651, Tracy, California", "subtitle": "Byron Hot Springs · secret interrogation center, 1942–45"})],
    # 16 wired for sound
    [("The construction plans were labeled", "NOUB", T(1, 3.4)), ("eight-foot fences", "NOU", T(3, 48.6)),
     ("Microphones were hidden", "D7", T(4, 3.4)), ("@", "Microphones were hidden", "Stand-in · radio operators · from December 7th (1943)"),
     ("Wires ran through hollow walls", "D7", T(4, 35.9)), ("where the prisoners' conversations", "NOUB", T(2, 15.9))],
    # 17
    [("The camp never held", "NOUB", T(4, 22.8)), ("Some vents let a man", "NOU", T(4, 30.2)), ("Even the trees outside", "TRN", T(5, 8.8))],
    # 18 the interrogators
    [("There were forty-five interrogators", "IWO", T(7, 2.3)), ("@", "There were forty-five interrogators", "Nisei Marine interpreter with Japanese prisoners, Iwo Jima, 1945"),
     ("Each interrogator was given one prisoner", "NOUB", T(10, 43.3))],
    # 19
    [("On the surface", "IWO", T(5, 36.1)), ("two or three times a day", "NOUB", T(0, 27.2)), ("Underneath, every question", "NOU", T(1, 2.4)),
     ("A long checklist covered weapons", "SAI", T(2, 2.6)), ("and what a man expected", "NOUB", T(6, 29.6))],
    # 20 the reports
    [("Every four days or so", "SAI", T(7, 19.9)), ("@", "Every four days or so", "Stand-in · U.S. servicemen, Saipan, 1944"),
     ("the number of boiler rooms", "D7", T(26, 14.0)), ("The camp's report for", "SAI", T(7, 34.3)),
     ("#", "The camp's report for", None, {"type": "LedgerBars", "file": "FILE 05 — P.O. BOX 651", "head": "1,077 questioned in 1944", "max": 174,
        "bars": [{"label": "January 1944", "value": 13, "figure": "13", "note": "Japanese prisoners interrogated"},
                 {"label": "August 1944", "value": 174, "figure": "174", "note": "the busiest month"}],
        "source": f"“Report of Activities, MIS Section, P.O. Box 651, Tracy”, 1944, in {KR}"})],
    # 21 the threat
    [("What made them talk", "NOUB", T(7, 42.1)), ("no threat of violence", "NOU", T(4, 2.5)),
     ("the threat to send", "SAI", T(7, 48.8)), ("The men who had asked", "IWO", T(2, 43.7))],
    # 22
    [("Another lesson surprised", "NOUB", T(8, 18.3)), ("With the Japanese", "NOUB", T(8, 36.4)),
     ("Older prisoners told new arrivals", "NOUB", T(2, 15.9)), ("Some came back the next day", "NOUB", T(0, 9.1))],
    # 23 Geneva
    [("None of this was strictly legal", "NOU", T(3, 48.6)),
     ("#", "The secret centers, the historian", None, {"type": "LedgerQuote", "file": "FILE 06 — BENDING THE RULES", "head": "Worth the risk",
        "before": "These interrogation centers ", "key": "contravened or, at the very least, “bent” a dozen or so articles", "after": " of the Geneva Convention of 1929.",
        "who": "Arnold Krammer, historian, 1983", "source": f"{KR}, p. 74"}),
     ("Japan had never ratified", "KYE", T(9, 39.7)), ("reasoned that the treatment", "KYE", T(55, 43.2)),
     ("@", "reasoned that the treatment", "Prisoners in Japanese hands · from Know Your Enemy: Japan (1945)"), ("The comfort was real", "NOU", T(6, 21.0))],
    # 24
    [("And the questions had an end", "NOUB", T(8, 54.6)), ("shipped out to an ordinary camp", "TRN", T(3, 53.9)),
     ("@", "shipped out to an ordinary camp", "Stand-in · passenger train, 1940")],
    # 25 a new page
    [("For some, the change", "IWO", T(9, 3.0)), ("They had been taught", "KYE", T(4, 57.7)), ("When their requests", "NOUB", T(9, 12.7)), ("many started over", "NOUB", T(9, 30.8)),
     ("In nineteen forty-six", "KYE", T(60, 26.4)),
     ("#", "In nineteen forty-six", "and flew with American", {"type": "LedgerQuote", "file": "FILE 07 — A NEW PAGE", "head": "Guiding the bombers",
        "before": "Old [Japanese] Army hands… wrote our propaganda and ",
        "key": "flew with our bombing pilots", "after": " to guide them to military targets.",
        "who": "Ruth Benedict, The Chrysanthemum and the Sword, 1946", "source": f"Benedict (1946), pp. 28–29, quoted in {KR}"}),
     ("and flew with American", "KYE", T(61, 29.3)), ("@", "and flew with American", "Bombing raid · from Know Your Enemy: Japan (1945)")],
    # 26
    [("One group of prisoners", "IWO", T(3, 1.0)),
     ("#", "One group of prisoners", None, {"type": "Slug", "title": "New York Times, July 8, 1945", "subtitle": "Prisoners ask to fight their way back to Japan"}),
     ("badly misled by the Emperor", "KYE", T(7, 34.3)), ("and asked to fight their way back", "KYE", T(59, 54.9)),
     ("Benedict's explanation", "NOUB", T(9, 48.9)), ("Having put everything", "NOUB", T(3, 28.4))],
    # 27
    [("In September nineteen forty-five", "SUR", T(1, 42.2)),
     ("#", "In September nineteen forty-five", None, {"type": "Slug", "title": "September 1945", "subtitle": "Camp Tracy ordered closed"}),
     ("One of the two centers", "TRN", T(6, 23.7)), ("That same year", "TRN", T(5, 27.5))],
    # 28 comment request
    [("If you know of a prisoner", "IWO", T(2, 43.7)),
     ("#", "If you know of a prisoner", None, {"type": "Slug", "title": "Know a prisoner or interrogator?", "subtitle": "Tell us in the comments"})],
    # 29 echo
    [("The brick hotel still stands", "TRN", T(6, 42.4)), ("The prisoners who arrived there", "NOU", T(6, 14.1)),
     ("What the Americans used instead", "KYE", T(34, 13.1)), ("and someone willing to listen", "D7", T(4, 3.4))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (7, "They came ashore at Angel Island", None, "angel_island_aerial_2019.jpg", "07", "Angel Island", "Angel Island in San Francisco Bay today, with the city behind it", f"Taras Bobrovytsky, 2019 · CC0 · {WC}", {"focus": [0.45, 0.55]}),
    (8, "They asked that their families", None, "angel_island_pow_note.png", "08", "A prisoner's note", "A note left by a Japanese prisoner of war held at Angel Island (exhibit, Angel Island State Park)", f"DPLA · CC BY-SA 3.0 · {WC}", {"focus": [0.35, 0.3]}),
    (14, "A resort had opened there", None, "byron_pre1905.jpg", "14", "Byron Hot Springs", "Founder Lewis Mead at the White Sulphur Spring, before 1905", f"Unknown photographer · public domain · {WC}", {"focus": [0.55, 0.5], "circle": [0.62, 0.6, 0.09, 0.26]}),
    (14, "A four-story brick hotel", None, "byron_1914.jpg", "15", "The brick hotel", "The third hotel building at Byron Hot Springs, 1914 (postcard)", f"Public domain · {WC}", {"focus": [0.5, 0.5]}),
    (18, "trained at the army's Military", None, "camp_savage_1946.jpg", "18", "MIS Language School", "Camp Savage, Minnesota, second home of the Military Intelligence Service Language School", f"MISLS yearbook, 1946 · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (24, "or back to Angel Island", None, "fort_mcdowell_admin_habs.jpg", "24", "Fort McDowell", "Administration building of Fort McDowell, the Army post on Angel Island", f"James W. Rosenthal · HABS CAL,21-ANGEL,2G-1 · {WC}", {"focus": [0.6, 0.5]}),
    (27, "That same year", None, "byron_2008_020.jpg", "27", "Byron Hot Springs", "The hotel that housed Camp Tracy, August 2008", f"Captndelta · CC BY-SA 3.0 · {WC}", {"focus": [0.5, 0.35]}),
    (29, "The brick hotel still stands", None, "byron_2008_024.jpg", "29", "Still standing", "The abandoned hotel at Byron Hot Springs, August 2008", f"Captndelta · CC BY-SA 3.0 · {WC}", {"focus": [0.45, 0.35]}),
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
