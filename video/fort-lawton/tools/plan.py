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
    "NEG": ("negro_soldier_1944", 1), "TEAM": ("teamwork_1946", 1), "SPE": ("seattle_poe_1951", 1),
    "TUN": ("tunisian_campaign_1943", 1), "FDR": ("fdr_tour_1942", 1), "PRES": ("president_tour_1945", 1),
    "MEM": ("memorial_day_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

# in-points of the films still to be checked frame by frame (filled from the contact sheets)
S = {"TUN_march": 11.0, "TUN_b": 98.7, "TUN_c": 33.0, "TUN_d": 142.5, "TUN_e": 120.6, "FDR_water": 282.0, "FDR_seattle": 229.5, "FDR_b": 268.9, "FDR_c": 242.7, "PRES_b": 68.7, "PRES_d": 72.0, "PRES_e": 72.0}

ABCMR = "Army Board for Correction of Military Records, AR20070009496, Oct. 2007"
HR = "H.R. 3174, 109th Congress (Rep. Jim McDermott), June 30, 2005"
NELSON = "Congressional Record, Senate, July 29, 2008, p. 16657"
REICH = "Congressional Record, July 17, 2008, p. E1493"
NRHP = "National Register nomination, Fort Lawton, 1978 · National Archives"
ISU = "National Archives, “The Italian Service Units of World War II”"
NPR05 = "Jack Hamann, NPR Weekend Edition, May 22, 2005"
AP08 = "Associated Press, July 27, 2008"
NEG_TAG = "Stand-in · Black soldiers in training · from The Negro Soldier (War Dept., 1944)"
TEAM_TAG = "Stand-in · a Black port unit at work · from Teamwork (Army, 1946)"
SPE_TAG = "Seattle Port of Embarkation, 1951 · U.S. Army film"
TUN_TAG = "Italian prisoners, Tunisia, May 1943 · U.S. Army film"
FDR_TAG = "Pacific Northwest, 1942 · President's tour (FDR Library)"
PRES_TAG = "Mount Rainier, Washington, June 1945 · Universal Newsreel"
MEM_TAG = "Stand-in · a national cemetery, Memorial Day 1945"
P = [
    # 0 the cable
    [("At", "FDR", S["FDR_water"]), ("@", "At about six", FDR_TAG),
     ("#", "At about six", None, {"type": "Slug", "title": "August 15, 1944", "subtitle": "Fort Lawton, Seattle · about 6 a.m."}),
     ("two military policemen", "NEG", T(27, 17.1)), ("@", "two military policemen", NEG_TAG), ("came to the obstacle course", "NEG", T(29, 25.4))],
    # 1 Olivotto
    [("He was an Italian", "TUN", S["TUN_march"]), ("@", "He was an Italian", TUN_TAG), ("A few hours earlier", "NEG", T(26, 3.8)), ("@", "A few hours earlier", NEG_TAG)],
    # 2 the trial
    [("Within three months", "NEG", T(26, 12.9)), ("It was the largest", "NEG", T(29, 43.8)), ("The prosecutor would later", "SPE", T(7, 22.9)), ("@", "The prosecutor would later", SPE_TAG)],
    # 3 documented story
    [("This is the documented story", "SPE", T(1, 7.6)), ("of the report the defense", "NEG", T(30, 2.1)), ("@", "of the report the defense", NEG_TAG), ("and of the sixty-three years", "MEM", T(0, 27.3)), ("@", "and of the sixty-three years", MEM_TAG), ("to admit that the trial", "FDR", T(4, 55.1))],
    # 4 the fort
    [("Fort Lawton sat", "FDR", S["FDR_seattle"]), ("@", "Fort Lawton sat", FDR_TAG), ("In the war it became", "SPE", T(1, 22.6)), ("@", "In the war it became", SPE_TAG),
     ("#", "A National Register report", None, {"type": "LedgerDocument", "file": "FILE 01 — THE FORT", "head": "The last stop before the Pacific", "source": NRHP,
        "spans": [{"doc": "doc_nrhp_million", "say": "over one million servicemen were processed through Fort Lawton for the combat zones of the Pacific and the Far East"}]})],
    # 5 Italy changes sides
    [("The Italians were there", "TUN", S["TUN_b"]), ("@", "The Italians were there", TUN_TAG),
     ("#", "Of about fifty-one thousand", None, {"type": "LedgerBars", "file": "FILE 02 — THE VOLUNTEERS", "head": "Italian prisoners in America, 1944", "max": 51000,
        "bars": [{"label": "Italian prisoners in the U.S.", "value": 51000, "figure": "51,000", "note": "about"},
                 {"label": "Joined the service units", "value": 45000, "figure": "45,000+", "note": "from February 1944"}],
        "source": ISU})],
    # 6 service units
    [("They were still prisoners", "TEAM", T(5, 0.7)), ("@", "They were still prisoners", TEAM_TAG), ("They were paid", "TEAM", T(8, 28.1))],
    # 7 the 28th
    [("At Fort Lawton the twenty-eighth", "TUN", S["TUN_c"]), ("@", "At Fort Lawton the twenty-eighth", TUN_TAG), ("On some evenings", "SPE", T(7, 52.9)), ("@", "On some evenings", SPE_TAG)],
    # 8 port companies
    [("Next to them lived", "NEG", T(26, 22.1)), ("@", "Next to them lived", NEG_TAG),
     ("#", "The Army was segregated", None, {"type": "LedgerTimeline", "file": "FILE 03 — NEIGHBOURS", "head": "Fort Lawton, August 14, 1944",
        "rows": [{"date": "≈ 612 MEN", "text": "Three Black port companies"},
                 {"date": "≈ 206 MEN", "text": "28th Italian Service Unit, next door"},
                 {"date": "NEXT MORNING", "text": "The port companies ship out"}],
        "source": ABCMR})],
    # 9 shipping out
    [("On the night of the fourteenth", "TEAM", T(5, 36.3)), ("@", "On the night of the fourteenth", TEAM_TAG), ("the next morning", "SPE", T(1, 52.6))],
    # 10 segregated
    [("The Black soldiers served", "NEG", T(28, 12.1)), ("@", "The Black soldiers served", NEG_TAG), ("The men next door", "TUN", S["TUN_d"]), ("@", "The men next door", TUN_TAG), ("Newspapers at the time", "NEG", T(26, 31.2))],
    # 11 the punch
    [("At about eleven that night", "NEG", T(37, 16.7)), ("@", "At about eleven that night", NEG_TAG), ("They met a group of Italians", "TUN", T(0, 33.0)),
     ("#", "The account the Army later accepted", None, {"type": "LedgerQuote", "file": "FILE 04 — 11 P.M.", "head": "How it started, in the Army's account",
        "before": "As the two groups passed, at least one of the American Soldiers swore at the Italians, and one of them shouted, ", "key": "“Hey, Italian.”", "after": "",
        "who": "The Army board, summing up the 1944 Inspector General record", "source": ABCMR}),
     ("The Italian hit him", "TEAM", T(9, 3.7))],
    # 12 accounts differ
    [("Accounts differ", "NEG", T(26, 40.4))],
    # 13 the riot
    [("What came next", "NEG", T(26, 49.6)),
     ("#", "Between one hundred", None, {"type": "LedgerQuote", "file": "FILE 05 — THE RIOT", "head": "Between 100 and 200 men",
        "before": "The Americans were armed with ", "key": "stones, knives, shovels, clubs of all sizes and description, and at least one ax", "after": ".",
        "who": "The Army board's summary of the evidence", "source": ABCMR})],
    # 14 the MPs
    [("Some of the military police", "NEG", T(25, 36.2)), ("@", "Some of the military police", NEG_TAG), ("They took the injured", "NEG", T(27, 4.0)), ("The riot went on", "NEG", T(32, 28.8)), ("Twenty-four men", "NEG", T(27, 10.0))],
    # 15 the body
    [("At six the next morning", "SPE", T(0, 37.5)), ("@", "At six the next morning", SPE_TAG)],
    # 16 no evidence
    [("The doctor who examined", "NEG", T(24, 4.0)), ("Nobody photographed", "TEAM", T(7, 23.0)), ("Later the rope itself", "SPE", T(0, 40.0)),
     ("#", "Nobody photographed", None, {"type": "LedgerTimeline", "file": "FILE 06 — THE SCENE", "head": "What nobody did",
        "rows": [{"date": "PHOTOGRAPHS", "text": "None, while the body was still hanging"},
                 {"date": "FINGERPRINTS", "text": "None taken"},
                 {"date": "FOOTPRINTS", "text": "Covered with cardboard, never cast"},
                 {"date": "THE ROPE", "text": "Lost"}],
        "source": f"{ABCMR}; {NPR05}"})],
    # 17 the charges
    [("By the fall", "NEG", T(26, 3.8)), ("Three of them", "NEG", T(27, 35.4)), ("That carried a maximum", "SPE", T(2, 52.6))],
    # 18 Cooke
    [("At the same time", "NEG", T(33, 51.2)), ("@", "At the same time", NEG_TAG), ("to find out what had gone wrong", "NEG", T(32, 19.6)), ("Brigadier General Elliot", "NEG", T(30, 29.6)), ("@", "Brigadier General Elliot", NEG_TAG),
     ("#", "He called the fort's", None, {"type": "LedgerQuote", "file": "FILE 07 — THE COOKE REPORT", "head": "Brig. Gen. Elliot D. Cooke, Oct. 28, 1944",
        "before": "The Army's investigation was deeply flawed and, in the words of the General himself, was ", "key": "“reprehensible”", "after": ".",
        "who": "Congress's findings on the report, 164 witnesses", "source": HR})],
    # 19 consequences
    [("The report had consequences", "TEAM", T(5, 38.3)), ("@", "The report had consequences", TEAM_TAG), ("and two white military policemen", "NEG", T(24, 22.0)), ("The report itself", "TEAM", T(8, 34.1))],
    # 20 the trial
    [("The trial began", "NEG", T(30, 44.0)), ("@", "The trial began", NEG_TAG)],
    # 21 two lawyers
    [("The defense was a Seattle lawyer", "NEG", T(22, 40.0)), ("@", "The defense was a Seattle lawyer", NEG_TAG), ("In the words a congressman", "NEG", T(30, 20.4)),
     ("#", "In the words a congressman", None, {"type": "LedgerDocument", "file": "FILE 08 — THE DEFENSE", "head": "43 men, two lawyers", "source": HR,
        "spans": [{"doc": "doc_hr_tendays", "say": "all forty-three shared two Army defense counsel who were given just ten days to prepare the defense"}]})],
    # 22 the report refused
    [("In open court", "SPE", T(3, 7.7)), ("@", "In open court", SPE_TAG), ("The prosecution was still", "NEG", T(31, 24.6)), ("@", "The prosecution was still", NEG_TAG)],
    # 23 pro-Nazi witness
    [("The central witness", "TUN", S["TUN_e"]), ("@", "The central witness", TUN_TAG),
     ("#", "The congressman's bill", None, {"type": "LedgerDocument", "file": "FILE 09 — THE WITNESS", "head": "What the defense was not told", "source": HR,
        "spans": [{"doc": "doc_hr_pronazi", "say": "probably pro-Nazi a fact not made available to the defense"}]})],
    # 24 no weapon
    [("There was no murder weapon", "NEG", T(29, 7.1)), ("@", "There was no murder weapon", NEG_TAG)],
    # 25 verdicts
    [("On the eighteenth of December", "NEG", T(29, 16.2)),
     ("#", "Twenty-eight men", None, {"type": "LedgerBars", "file": "FILE 10 — THE VERDICTS", "head": "December 18, 1944", "max": 43,
        "bars": [{"label": "Charged", "value": 43, "figure": "43", "note": "all Black soldiers"},
                 {"label": "Convicted of rioting", "value": 28, "figure": "28", "note": "two also of manslaughter"},
                 {"label": "Acquitted", "value": 13, "figure": "13", "note": ""}],
        "source": HR})],
    # 26 sentences, appeal
    [("The sentences ran", "NEG", T(32, 10.4)), ("On the nineteenth of April", "TEAM", T(9, 3.7)), ("@", "On the nineteenth of April", TEAM_TAG),
     ("#", "On the nineteenth of April", None, {"type": "Slug", "title": "April 19, 1945", "subtitle": "All appeals dismissed, without comment"})],
    # 27 prison
    [("The men went to prison", "NEG", T(26, 46.0)), ("@", "The men went to prison", NEG_TAG), ("By the end of the decade", "SPE", T(0, 46.0))],
    # 28 Jaworski
    [("After the war", "SPE", T(8, 22.9)), ("@", "After the war", SPE_TAG), ("He took the President's tapes", "SPE", T(7, 7.8))],
    # 29 the grave
    [("was buried in the small post cemetery", "MEM", T(1, 56.0)), ("@", "was buried in the small post cemetery", MEM_TAG)],
    # 30 Hamann
    [("In nineteen eighty-six", "FDR", S["FDR_b"]), ("@", "In nineteen eighty-six", FDR_TAG), ("At the time", "MEM", T(0, 27.3))],
    # 31 the report found
    [("Years later", "PRES", S["PRES_b"]), ("@", "Years later", PRES_TAG), ("At the National Archives", "TEAM", T(8, 28.1)), ("@", "At the National Archives", TEAM_TAG)],
    # 32 the book, the bill
    [("In 2005", "SPE", T(0, 52.5)), ("@", "In 2005", SPE_TAG), ("That summer", "TEAM", T(5, 0.7)), ("@", "That summer", TEAM_TAG)],
    # 33 the ruling
    [("The families of the convicted", "NEG", T(30, 11.2)), ("@", "The families of the convicted", NEG_TAG),
     ("#", "gave its answer", None, {"type": "Slug", "title": "October 2007", "subtitle": "Army Board for Correction of Military Records"})],
    # 34 the words
    [("The board wrote", "SPE", T(0, 22.5)), ("@", "The board wrote", SPE_TAG),
     ("#", "Its conclusion was", None, {"type": "LedgerQuote", "file": "FILE 11 — THE RULING", "head": "The Army board, October 2007",
        "before": "The factors described above, overall, ", "key": "rendered the trial fundamentally unfair and improper", "after": ".",
        "who": "Unanimous decision, three members", "source": ABCMR})],
    # 35 what it did
    [("The board did not say", "MEM", T(0, 27.3)), ("@", "The board did not say", MEM_TAG), ("and it did not rule on guilt", "NEG", T(25, 8.8)), ("@", "and it did not rule on guilt", NEG_TAG), ("It set aside", "SPE", T(6, 22.8)), ("@", "It set aside", SPE_TAG)],
    # 36 Samuel Snow
    [("Samuel Snow of", "TEAM", T(5, 4.5)), ("@", "Samuel Snow of", TEAM_TAG), ("After prison", "TEAM", T(7, 11.1))],
    # 37 the check
    [("On the floor", "SPE", T(3, 52.7)), ("@", "On the floor", SPE_TAG),
     ("#", "On the floor", None, {"type": "LedgerDocument", "file": "FILE 12 — THE BACK PAY", "head": "Samuel Snow's check", "source": NELSON,
        "spans": [{"doc": "doc_nelson_725", "say": "Mr President do you know how much that was It was seven hundred and twenty-five dollars nineteen forty-four dollars"}]})],
    # 38 interest
    [("There was no interest", "SPE", T(5, 37.8)), ("@", "There was no interest", SPE_TAG),
     ("#", "Congress added it", None, {"type": "Slug", "title": "October 14, 2008", "subtitle": "Interest on the back pay, by law"})],
    # 39 the apology
    [("On Saturday", "SPE", T(2, 37.6)), ("@", "On Saturday", SPE_TAG),
     ("#", "On Saturday", None, {"type": "Slug", "title": "July 26, 2008", "subtitle": "Fort Lawton, now Discovery Park, Seattle"}),
     ("He told them", "SPE", T(6, 37.8)), ("@", "He told them", SPE_TAG)],
    # 40 two of 28
    [("A few days before", "SPE", T(7, 22.9)),
     ("#", "A few days before", None, {"type": "LedgerDocument", "file": "FILE 13 — TWO OF 28", "head": "Too late for 26 men", "source": REICH,
        "spans": [{"doc": "doc_reichert_two", "say": "only two of the original twenty-eight soldiers are alive today meaning twenty-six Army veterans passed away before an extreme personal injustice was rectified"}]})],
    # 41 Snow in Seattle
    [("Samuel Snow had come", "SPE", T(6, 57.6)), ("@", "Samuel Snow had come", SPE_TAG), ("His son went", "SPE", T(5, 52.8))],
    # 42 died
    [("According to Senator Nelson", "PRES", S["PRES_d"]), ("@", "According to Senator Nelson", PRES_TAG)],
    # 43 the question
    [("Today nobody stands", "NEG", T(37, 16.7)), ("@", "Today nobody stands", NEG_TAG), ("The two manslaughter convictions", "FDR", T(5, 34.5)), ("@", "The two manslaughter convictions", FDR_TAG), ("points to a white military policeman", "NEG", T(25, 47.5)), ("@", "points to a white military policeman", NEG_TAG)],
    # 44 comment ask
    [("If your family", "SPE", T(5, 22.8)), ("@", "If your family", SPE_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "Italian prisoners or port companies in your family's story?", "subtitle": "Tell us in the comments"})],
    # 45 Discovery Park
    [("Most of Fort Lawton", "SPE", T(1, 0.0)), ("@", "Most of Fort Lawton", SPE_TAG)],
    # 46 the stone
    [("The cemetery stayed", "MEM", T(1, 56.0)), ("@", "The cemetery stayed", MEM_TAG), ("a long way from Italy", "FDR", T(4, 42.0)), ("@", "a long way from Italy", FDR_TAG)],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (1, "His gravestone says", None, "olivotto_grave.jpg", "01", "Soldato italiano", "His stone: Olivotto Guglielmo, October 1911 – 14 August 1944", f"Joe Mabel · CC BY-SA 3.0 · {WC}", {"crop": [0.18, 0.55, 0.7, 0.42]}),
    (2, "It was the largest", None, "obstacle_course_1944.jpg", "02", "The obstacle course", "S/Sgt. Charles M. Robinson where Olivotto was found, 1944", f"U.S. Army Signal Corps · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (6, "They were still prisoners", None, "italian_pows_a.jpg", "06", "Italian prisoners in America", "A U.S. camp, 1943 (not Fort Lawton)", f"Signal Corps SC 180068 · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 0.94]}),
    (7, "On some evenings", None, "seattle_1944.gif", "07", "Seattle, 1944", "Second Avenue", f"Seattle Municipal Archives · CC BY 2.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (20, "The prosecutor was a lawyer from Texas", None, "court_panel_1944.jpg", "20", "The court, 1944", "The panel (top), the defense (left) and the prosecution (right)", f"U.S. Army Signal Corps · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (28, "On the first of November", None, "jaworski_1977.jpg", "28", "Leon Jaworski", "In 1977, three years after Watergate", f"Bernard Gotfryd · Library of Congress · public domain · {WC}", {"crop": [0.02, 0.08, 0.62, 0.92]}),
    (29, "was buried in the small post cemetery", None, "fort_lawton_cemetery.jpg", "29", "Fort Lawton Post Cemetery", "Seattle, 2009", f"Joe Mabel · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.25, 1.0, 0.6]}),
    (30, "found his headstone", None, "olivotto_headstone.jpg", "30", "Olivotto's grave", "Apart from the American graves", f"Jack Hamann · CC BY 3.0 · {WC}", {"crop": [0.0, 0.15, 1.0, 0.7]}),
    (45, "Most of Fort Lawton", None, "discovery_park_meadow.jpg", "45", "Discovery Park", "Seattle, above Puget Sound, 2007", f"Joe Mabel · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (46, "In it away from", None, "olivotto_grave.jpg", "46", "Fort Lawton, today", "The grave of Guglielmo Olivotto", f"Joe Mabel · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
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
