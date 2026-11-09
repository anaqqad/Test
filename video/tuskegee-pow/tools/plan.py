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
    "W": ("wings_1945", 1), "RT": ("red_tails_1944", 1), "QM": ("queen_mary_1945", 1), "MO": ("moosburg_1945", 1),
    "CB": ("combat_bulletin_17", 1), "PF": ("prisoners_freed_1945", 1), "DA": ("dachau_services_1945", 1),
    "TT": ("target_today_1944", 1), "NC": ("negro_colleges_1944", 1),
}


def T(m, s=0.0):
    return m * 60 + s

S = {}

NPR = "Alexander Jefferson, NPR News & Notes, Nov. 10, 2006"
GOE = "Gathering of Eagles Foundation profile, 2010"
LAW = "Public Law 109-213, April 11, 2006 · Congressional Gold Medal to the Tuskegee Airmen"
HAUL = "Daniel L. Haulman, Air Force Historical Research Agency"
SL3 = "Stalag VII-A records, via Moosburg Online / Wikipedia"
W_TAG = "Stand-in · Tuskegee cadets and pilots · from Wings for This Man (AAF, 1945)"
W_IT = "332nd Fighter Group in Italy · from Wings for This Man (AAF, 1945)"
RT_TAG = "332nd Fighter Group, Ramitelli, Italy, Sept. 1944 · Army film"
QM_TAG = "Troops arrive in New York on the Queen Mary, July 1945 · Army film"
MO_TAG = "U.S. troops cross the river at Moosburg, April 1945 · Army film"
CB_TAG = "Invasion of southern France, August 1944 · Combat Bulletin 17"
PF_TAG = "Stand-in · freed American prisoners, Germany, April 1945 · Army film"
DA_TAG = "Dachau, May 6, 1945 · survivors at a service · Army film"
TT_TAG = "Stand-in · a bomber mission · from Target for Today (1944)"
NC_TAG = "Stand-in · a Black college in wartime · from Negro Colleges in Wartime (OWI, c. 1944)"
P = [
    # 0 the interrogator
    [("In", "W", 116.3), ("@", "In the late summer", W_TAG),
     ("#", "In the late summer", None, {"type": "Slug", "title": "Late summer, 1944", "subtitle": "A German interrogation of a captured American pilot"}),
     ("The pilot was Second", "W", 128.5), ("The German did not wait", "W", 140.8), ("He named the unit", "RT", 443.0), ("@", "He named the unit", RT_TAG)],
    # 1 the book
    [("Then he opened a book", "W", 299.9), ("@", "Then he opened a book", W_TAG),
     ("#", "It had his marks from college", None, {"type": "LedgerTimeline", "file": "FILE 01 — THE BOOK", "head": "What the interrogator had on him",
        "rows": [{"date": "PHOTOGRAPHS", "text": "Every Black pilot class before his"},
                 {"date": "COLLEGE", "text": "His marks, Clark, Atlanta"},
                 {"date": "HIGH SCHOOL", "text": "His marks, Chadsey, Detroit"},
                 {"date": "THE HOUSE", "text": "The tax his father paid"}],
        "source": f"Jefferson's own account · {NPR}"})],
    # 2 knew more
    [("Jefferson said they knew", "W", 128.5), ("He would spend nine months", "PF", 106.0), ("@", "He would spend nine months", PF_TAG), ("And when he came home", "QM", 344.0), ("@", "And when he came home", QM_TAG)],
    # 3 documented story
    [("This is the documented story", "W", 459.0), ("@", "This is the documented story", W_IT), ("told from the interviews", "RT", 34.3)],
    # 4 Detroit boyhood
    [("He was born in Detroit", "W", 55.1), ("@", "He was born in Detroit", W_TAG), ("In third and fourth grade", "NC", 34.6), ("@", "In third and fourth grade", NC_TAG), ("That was where he got", "W", 312.2)],
    # 5 the Army War College
    [("The Army Air Corps refused", "NC", 436.0), ("@", "The Army Air Corps refused", NC_TAG),
     ("#", "In 2006 Congress wrote down why", None, {"type": "LedgerDocument", "file": "FILE 02 — THE STUDIES", "head": "What the Army had concluded", "source": LAW,
        "spans": [{"doc": "doc_law_unfit", "say": "Studies commissioned by the Army War College between nineteen twenty-four and nineteen thirty-nine concluded that Blacks were unfit for leadership roles and incapable of aviation"}]})],
    # 6 1941
    [("That changed in", "W", 189.7), ("@", "That changed in", W_TAG), ("According to the same law", "W", 177.5), ("Because the country was segregated", "W", 42.8)],
    # 7 the weigh-in
    [("Jefferson finished college", "NC", 48.4), ("@", "Jefferson finished college", NC_TAG), ("He went to the armory", "W", 263.2), ("@", "He went to the armory", W_TAG),
     ("#", "The minimum weight was", None, {"type": "LedgerTimeline", "file": "FILE 03 — THE SCALE", "head": "The Detroit armory, 1942",
        "rows": [{"date": "MINIMUM", "text": "116 pounds"}, {"date": "JEFFERSON", "text": "115 pounds and a few ounces"},
                 {"date": "AFTER WATER AND BANANAS", "text": "116 pounds, 2 ounces"}], "source": NPR})],
    # 8 Tuskegee
    [("In April", "W", 238.7), ("@", "In April", W_TAG), ("He would remember following", "W", 336.6), ("then skimming the treetops", "W", 434.6), ("He got his wings", "W", 544.7),
     ("#", "He got his wings", None, {"type": "Slug", "title": "January 1944", "subtitle": "Tuskegee Army Air Field · pilot's wings"})],
    # 9 Ramitelli
    [("That June he reached", "RT", 89.1), ("@", "That June he reached", RT_TAG), ("His group parked", "W", 275.4), ("@", "His group parked", W_TAG), ("He flew his first Mustang", "W", 459.0), ("@", "He flew his first Mustang", W_IT)],
    # 10 escort record
    [("The job was escort", "TT", 3945.3), ("@", "The job was escort", TT_TAG),
     ("#", "Air Force historian", None, {"type": "LedgerBars", "file": "FILE 04 — THE RECORD", "head": "Escorted bombers lost to enemy fighters", "max": 46,
        "bars": [{"label": "332nd Fighter Group", "value": 27, "figure": "27", "note": "179 escort missions"},
                 {"label": "Other P-51 groups, Fifteenth Air Force", "value": 46, "figure": "46", "note": "average, same period"}],
        "source": HAUL})],
    # 11 flak
    [("Jefferson remembered the flak", "TT", 4109.7), ("@", "Jefferson remembered the flak", TT_TAG), ("One day he watched", "TT", 3945.3), ("He got sick inside", "TT", 3739.7)],
    # 12 August 12
    [("On the twelfth of August", "CB", 197.9), ("@", "On the twelfth of August", CB_TAG),
     ("#", "On the twelfth of August", None, {"type": "Slug", "title": "August 12, 1944", "subtitle": "Radar stations near Toulon, France"}),
     ("Jefferson had flown eighteen", "W", 459.0), ("@", "Jefferson had flown eighteen", W_IT), ("He was number four", "W", 385.6), ("@", "He was number four", W_TAG)],
    # 13 the strafing run
    [("They went in at about", "W", 434.6), ("@", "They went in at about", W_TAG), ("By then the side of the cliff", "CB", 482.9), ("@", "By then the side of the cliff", CB_TAG), ("He put his hits", "W", 467.5), ("Then there was a bang", "W", 287.7), ("@", "Then there was a bang", W_TAG)],
    # 14 bailing out
    [("In nine months of training", "W", 263.2), ("@", "In nine months of training", W_TAG), ("He saw the tail go by", "CB", 245.4), ("@", "He saw the tail go by", CB_TAG), ("When the parachute opened", "CB", 546.2)],
    # 15 killed in action
    [("His wingmen did not see", "W", 446.8), ("@", "His wingmen did not see", W_TAG),
     ("#", "In Detroit his parents", None, {"type": "LedgerTimeline", "file": "FILE 05 — DETROIT", "head": "What his parents were told",
        "rows": [{"date": "AUG. 12, 1944", "text": "His wingmen see no parachute"},
                 {"date": "AFTER THAT", "text": "Killed in action"},
                 {"date": "ABOUT A MONTH LATER", "text": "A Red Cross letter: a prisoner"}], "source": GOE})],
    # 16 Stalag Luft III
    [("A train took him", "PF", 4.2), ("@", "A train took him", PF_TAG), ("He arrived in September", "PF", 63.2)],
    # 17 no segregation
    [("The Army that sent him", "W", 422.3), ("@", "The Army that sent him", W_TAG), ("Here there was no such line", "PF", 72.0), ("@", "Here there was no such line", PF_TAG),
     ("#", "In his words", None, {"type": "LedgerQuote", "file": "FILE 06 — THE CAMP", "head": "Stalag Luft III, 1944",
        "before": "All the rights and privileges of an American officer. ", "key": "No segregation, no discrimination.", "after": "",
        "who": "Alexander Jefferson", "source": NPR})],
    # 18 the bomber crew
    [("The men followed the war", "PF", 131.0), ("@", "The men followed the war", PF_TAG), ("And new prisoners kept coming", "PF", 165.0),
     ("#", "One day a bomber crew", None, {"type": "LedgerQuote", "file": "FILE 07 — NEW ARRIVALS", "head": "A B-17 crewman, at the camp",
        "before": "", "key": "“Had you Red Tails been with us, we wouldn't have been shot down.”", "after": "",
        "who": "As Jefferson told it", "source": GOE})],
    # 19 the evacuation
    [("Just before midnight", "W", 153.0), ("@", "Just before midnight", W_TAG),
     ("#", "Just before midnight", None, {"type": "Slug", "title": "January 27, 1945", "subtitle": "Stalag Luft III, just before midnight"})],
    # 20 the march
    [("Jefferson remembered eighty", "PF", 21.1), ("@", "Jefferson remembered eighty", PF_TAG), ("At the end of the road", "W", 153.0), ("@", "At the end of the road", W_TAG)],
    # 21 Moosburg
    [("That camp had opened", "PF", 139.0), ("@", "That camp had opened", PF_TAG),
     ("#", "By the end", None, {"type": "LedgerBars", "file": "FILE 08 — STALAG VII-A", "head": "Moosburg, Bavaria", "max": 76248,
        "bars": [{"label": "Built for", "value": 10000, "figure": "10,000", "note": "Polish prisoners, 1939"},
                 {"label": "Held at liberation", "value": 76248, "figure": "76,248", "note": "main camp, April 29, 1945"}],
        "source": SL3})],
    # 22 liberation
    [("On the twenty-ninth of April", "MO", 146.8), ("@", "On the twenty-ninth of April", MO_TAG),
     ("#", "On the twenty-ninth of April", None, {"type": "Slug", "title": "April 29, 1945", "subtitle": "Stalag VII-A, Moosburg · liberated"}),
     ("After a short fight", "MO", 187.3), ("Jefferson had been a prisoner", "MO", 298.6)],
    # 23 Dachau
    [("The next day", "MO", 339.1), ("@", "The next day", MO_TAG), ("It was Dachau", "DA", 196.0), ("@", "It was Dachau", DA_TAG), ("He remembered a long table", "DA", 31.6), ("Sixty years later", "DA", 107.0)],
    # 24 the voyage
    [("A transport plane", "W", 67.3), ("@", "A transport plane", W_TAG), ("A ship took him", "QM", 19.5), ("@", "A ship took him", QM_TAG), ("into New York", "QM", 84.5)],
    # 25 the sign
    [("He walked down the gangplank", "QM", 344.0), ("@", "He walked down the gangplank", QM_TAG),
     ("#", "In front of him", None, {"type": "LedgerQuote", "file": "FILE 09 — THE GANGPLANK", "head": "New York, 1945",
        "before": "A big sign in front of you says: ", "key": "whites to the right, colored to the left.", "after": "",
        "who": "Alexander Jefferson", "source": NPR}),
     ("Jefferson had a phrase", "QM", 396.0)],
    # 26 NPR verdict
    [("When NPR told his story", "QM", 266.4), ("@", "When NPR told his story", QM_TAG),
     ("#", "He had been given", None, {"type": "LedgerQuote", "file": "FILE 10 — HOME", "head": "NPR, Veterans Day 2006",
        "before": "Ironically, he was given ", "key": "more respect as a POW than as a black man in America.", "after": "",
        "who": "NPR's introduction to his story", "source": NPR})],
    # 27 1948
    [("He went back to Tuskegee", "W", 361.0), ("@", "He went back to Tuskegee", W_TAG), ("Two years later", "W", 324.0),
     ("#", "Two years later", None, {"type": "Slug", "title": "July 26, 1948", "subtitle": "Executive Order 9981 · the armed forces desegregated"})],
    # 28 teacher
    [("Jefferson went home to Detroit", "NC", 256.0), ("@", "Jefferson went home to Detroit", NC_TAG), ("He stayed in the reserves", "NC", 90.0)],
    # 29 the law's count
    [("In 2006 Congress voted", "RT", 226.2), ("@", "In 2006 Congress voted", RT_TAG),
     ("#", "and the law counted", None, {"type": "LedgerDocument", "file": "FILE 11 — THE COST", "head": "The Gold Medal law, 2006", "source": LAW,
        "spans": [{"doc": "doc_law_pows", "say": "Sixty-six of these pilots were killed in combat while another thirty-two were either forced down or shot down and captured to become prisoners of war"}]})],
    # 30 home
    [("Near the end of that NPR", "W", 557.0), ("@", "Near the end of that NPR", W_TAG), ("The only obligation", "RT", 297.0), ("@", "The only obligation", RT_TAG), ("It wasn't perfect", "W", 569.0)],
    # 31 comment ask
    [("If your family", "RT", 340.0), ("@", "If your family", RT_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "A Tuskegee Airman or a POW in your family?", "subtitle": "Tell us in the comments"})],
    # 32 died
    [("Alexander Jefferson died", "W", 238.7), ("@", "Alexander Jefferson died", W_TAG)],
    # 33 the field
    [("Two years later the city", "NC", 34.6), ("@", "Two years later the city", NC_TAG), ("The local club", "W", 312.2), ("@", "The local club", W_TAG), ("So the boy who built", "W", 348.9)],
]

WC = "Wikimedia Commons"
FR = f"Toni Frissell · Library of Congress · public domain · {WC}"
PHOTOS = [
    (3, "This is the documented story", None, "jefferson_2013.jpg", "03", "Alexander Jefferson", "Veterans Day, Clio, Michigan, 2013", f"Master Sgt. Denice Rankin · U.S. Air National Guard · public domain · {WC}", {}),
    (6, "Because the country was segregated", None, "first_class.jpg", "06", "The first class", "Tuskegee, 1941: Maj. James A. Ellison returns the salute of Mac Ross", f"U.S. Air Force · public domain · {WC}", {}),
    (9, "He flew his first Mustang", None, "briefing_ramitelli.jpg", "09", "Ramitelli, Italy", "332nd Fighter Group pilots at a briefing, March 1945", FR, {}),
    (10, "The tails of their fighters", None, "gleed_p51.jpg", "10", "A red tail", "Edward Gleed and his P-51, Ramitelli, 1945", FR, {}),
    (16, "It is the camp", None, "stalag_luft3_drawing.jpg", "16", "Stalag Luft III", "Drawn by a prisoner in the camp", f"Lt. Robert M. Polich, Sr. · public domain · {WC}", {}),
    (18, "The men followed the war", None, "stalag_luft3.jpg", "18", "Block 29, South Compound", "Stalag Luft III, drawn by a prisoner", f"Lt. Robert M. Polich, Sr. · public domain · {WC}", {}),
    (21, "That camp had opened", None, "moosburg_b.jpg", "21", "Stalag VII-A, Moosburg", "Prisoners living in tents beside the crowded barracks, 1945", f"No. 5 Army Film & Photographic Unit · public domain · {WC}", {}),
    (23, "The next day", None, "moosburg_a.jpg", "23", "After the liberation", "Freed prisoners with Red Cross parcels, Moosburg", f"No. 5 Army Film & Photographic Unit · public domain · {WC}", {}),
    (24, "from there he crossed", None, "queen_mary_1945.jpg", "24", "The Queen Mary", "New York harbor, June 20, 1945, with U.S. troops from Europe", f"U.S. Navy · public domain · {WC}", {}),
    (28, "In 2005 he published", None, "jefferson_cc.jpg", "28", "The memoir", "Jefferson promoting his book, Ypsilanti, Michigan, 2012", f"Audrey Neuvirth · CC BY-SA 3.0 · {WC}", {}),
    (30, "He called it the best country", None, "jefferson_2013.jpg", "30", "Alexander Jefferson", "Detroit, 1921 – 2022", f"Master Sgt. Denice Rankin · U.S. Air National Guard · public domain · {WC}", {}),
    (32, "Alexander Jefferson died", None, "pilots_frissell.jpg", "32", "The 332nd Fighter Group", "Ramitelli, Italy, March 1945", FR, {}),
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
                elif card["type"] == "PhotoCard":
                    card["dur"] = 6.5
                else:  # full card runs to the end of its paragraph (7-12 s)
                    card["end"] = min(card["start"] + 12.0, max(card["start"] + 7.0, paras[pi]["end"] + 0.3))
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
