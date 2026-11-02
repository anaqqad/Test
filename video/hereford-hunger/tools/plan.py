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
    "PL": ("plow_plains_1936", 1), "FF": ("food_for_fighters_1943", 1), "TT": ("troop_train_1943", 1),
    "CP": ("controlling_german_pows_1944", 1), "TC": ("tunisian_campaign_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

WM = "D. M. Williams, Interlude in Umbarger (1992), as reviewed by R. Phelan, The Texas Observer, Dec. 24, 1999"
KE = "L. E. Keefer, Italian Prisoners of War in America (1992), p. 144, via Wikipedia, “Camp Hereford”"
PL_TAG = "The High Plains · from The Plow That Broke the Plains (1936)"
FF_TAG = "Stand-in · from Food for Fighters (OWI, 1943)"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
CP_TAG = "Stand-in · from Controlling German Prisoners of War (U.S. Army, 1944)"
TC_TAG = "Axis prisoners, Tunisia, May 1943 · U.S. Army film"
P = [
    # 0 the bishop's lunch
    [("On", "PL", T(3, 20.7)), ("@", "On September", PL_TAG),
     ("#", "a Catholic bishop", None, {"type": "Slug", "title": "September 7, 1945", "subtitle": "Camp Hereford, Texas · the bishop's lunch"}),
     ("He had asked", "FF", T(0, 43.1)), ("@", "He had asked", FF_TAG),
     ("#", "They served him", None, {"type": "LedgerQuote", "file": "FILE 01 — THE LUNCH", "head": "What the bishop was served",
        "before": "We were served a bowl of ", "key": "weak, watery soup", "after": ", containing pieces of gummy-like spaghetti.",
        "who": "Bishop Laurence J. FitzSimon, letter to Rep. Eugene Worley, 1945", "source": WM})],
    # 1 the kitchen
    [("He watched the prisoners", "FF", T(1, 7.8)), ("@", "He watched the prisoners", FF_TAG),
     ("#", "Later he walked", None, {"type": "LedgerQuote", "file": "FILE 02 — THE KITCHEN", "head": "What was coming for dinner",
        "before": "I saw some tubs of pig's feet, ", "key": "sacks of moldy-looking potatoes", "after": " and a basket of overripe tomatoes.",
        "who": "Bishop Laurence J. FitzSimon, 1945", "source": WM})],
    # 2 the men at the tables
    [("The men at those tables", "TC", T(4, 37.5)), ("@", "The men at those tables", TC_TAG),
     ("For months they had", "PL", T(17, 44.7)), ("@", "For months they had", PL_TAG), ("whatever birds", "PL", T(18, 22.5)),
     ("This is the documented story", "PL", T(3, 49.6))],
    # 3 Hereford
    [("Hereford was a farm town", "PL", T(4, 4.0)), ("@", "Hereford was a farm town", PL_TAG),
     ("#", "Hereford was a farm town", None, {"type": "Slug", "title": "Hereford, Texas", "subtitle": "Pop. about 2,300 · 45 miles southwest of Amarillo"}),
     ("In nineteen forty-two", "PL", T(3, 35.1)), ("on flat open land", "PL", T(4, 22.1))],
    # 4 first prisoners
    [("The first prisoners arrived", "TC", T(0, 51.4)), ("@", "The first prisoners arrived", TC_TAG),
     ("#", "The first prisoners arrived", None, {"type": "Slug", "title": "April 1943", "subtitle": "The first prisoners reach Camp Hereford"}),
     ("carried by train", "TT", T(6, 32.5)), ("@", "carried by train", TT_TAG), ("Almost all of them", "TC", T(13, 31.9))],
    # 5 the Nons
    [("In September", "TC", T(16, 16.3)), ("@", "In September", TC_TAG),
     ("#", "More than eighty-five", None, {"type": "LedgerBars", "file": "FILE 03 — THE NONS", "head": "Italian prisoners in America after Italy changed sides", "max": 51000,
        "bars": [{"label": "Italian prisoners in the U.S.", "value": 51000, "figure": "51,000", "note": "1943-44"},
                 {"label": "Agreed to work with the Allies", "value": 43400, "figure": "85%+", "note": "Italian Service Units"},
                 {"label": "Refused: the “Nons”", "value": 7600, "figure": "under 15%", "note": "many sent to Hereford"}],
        "source": "J. D. Rogers, Panhandle-Plains Historical Review (1989), p. 91, via Wikipedia, “Camp Hereford”"})],
    # 6 Geneva
    [("At first, the Nons", "FF", T(1, 7.8)), ("@", "At first, the Nons", FF_TAG),
     ("#", "Under Article eleven", "A local newspaper", {"type": "LedgerQuote", "file": "FILE 04 — THE RULE", "head": "Geneva Convention of 1929, Article 11",
        "before": "The food ration of prisoners of war shall be ", "key": "equivalent in quantity and quality", "after": " to that of the depot troops.",
        "who": "Convention relative to the Treatment of Prisoners of War, Geneva, 1929", "source": "Article 11"}),
     ("A local newspaper", "FF", T(3, 35.7)), ("Many of the men gained", "FF", T(2, 58.7))],
    # 7 work and play
    [("They earned camp scrip", "PL", T(8, 19.4)), ("@", "They earned camp scrip", PL_TAG), ("They played soccer", "TC", T(14, 33.5))],
    # 8 Germans elsewhere
    [("It was the same", "FF", T(4, 12.6)), ("@", "It was the same", FF_TAG),
     ("#", "One German later said", None, {"type": "LedgerBars", "file": "FILE 05 — ONE GERMAN PRISONER", "head": "His weight, in pounds", "max": 185,
        "bars": [{"label": "When he was captured", "value": 128, "figure": "128 lb", "note": ""},
                 {"label": "After two years in American camps", "value": 185, "figure": "185 lb", "note": "+57 lb"}],
        "source": "L. H. Carlson, We Were Each Other's Prisoners (1997), p. 208, via Wikipedia"})],
    # 9 V-E Day
    [("Then the war in Europe", "PL", T(19, 19.2)), ("@", "Then the war in Europe", PL_TAG),
     ("#", "Then the war in Europe", None, {"type": "Slug", "title": "May 8, 1945", "subtitle": "The war in Europe ends"}),
     ("Newspapers were accusing", "PL", T(20, 6.4)), ("Now many Americans", "PL", T(19, 56.9))],
    # 10 the order
    [("On May fourth", "TC", T(16, 36.9)), ("@", "On May fourth", TC_TAG),
     ("#", "On May fourth", None, {"type": "LedgerBars", "file": "FILE 06 — THE ORDER", "head": "Eighth Service Command, Dallas, May 4, 1945: calories a day", "max": 3500,
        "bars": [{"label": "Prisoner who does not work", "value": 2500, "figure": "2,300-2,500", "note": ""},
                 {"label": "Prisoner who works", "value": 3500, "figure": "3,500", "note": ""}],
        "source": WM}),
     ("The War Department said", "FF", T(3, 48.0)), ("@", "The War Department said", FF_TAG)],
    # 11 each commander
    [("Two thousand five hundred calories", "FF", T(4, 12.6)), ("It was not starvation", "TC", T(17, 18.0)), ("@", "It was not starvation", TC_TAG)],
    # 12 Carvolth
    [("Hereford's commander", "TC", T(12, 30.2)), ("@", "Hereford's commander", TC_TAG),
     ("#", "Hereford's commander", None, {"type": "Slug", "title": "Col. Joseph R. Carvolth", "subtitle": "Commander, Camp Hereford · formerly at Mexia, Texas"}),
     ("At Hereford, he went", "PL", T(18, 13.1)), ("@", "At Hereford, he went", PL_TAG)],
    # 13 the closures
    [("He closed the canteen", "TC", T(16, 36.9)), ("@", "He closed the canteen", TC_TAG),
     ("#", "reported that the limit", None, {"type": "LedgerBars", "file": "FILE 07 — THE MENUS", "head": "Calories a day at Camp Hereford, 1945", "max": 2500,
        "bars": [{"label": "The Army's limit", "value": 2500, "figure": "2,500", "note": "“rarely achieved”"},
                 {"label": "Many days", "value": 2000, "figure": "about 2,000", "note": ""},
                 {"label": "The worst days", "value": 1500, "figure": "1,500", "note": ""}],
        "source": "Camp physician Maj. Luigi Cabitto; " + KE})],
    # 14 officers' compound
    [("The officers' compound", "PL", T(18, 41.4)), ("@", "The officers' compound", PL_TAG),
     ("#", "A history of the camp", None, {"type": "LedgerQuote", "file": "FILE 08 — THE OFFICERS", "head": "The officers' compound, April to December 1945",
        "before": "From April through December 1945, the compound was under a ", "key": "retaliatory starvation order", "after": ".",
        "who": "L. Henegar, Handbook of Texas Online (1995)", "source": "“Hereford Military Reservation and Reception Center,” TSHA"})],
    # 15 la fame
    [("The prisoners had a name", "PL", T(20, 34.7)), ("@", "The prisoners had a name", PL_TAG),
     ("#", "The prisoners had a name", None, {"type": "Slug", "title": "La fame", "subtitle": "“The hunger” · spring to late fall 1945"})],
    # 16 what they ate
    [("They hunted anything", "PL", T(18, 50.8)), ("@", "They hunted anything", PL_TAG),
     ("#", "Dogs and cats", None, {"type": "LedgerTimeline", "file": "FILE 09 — LA FAME", "head": "What hungry men ate at Hereford",
        "rows": [{"date": "IN THE COMPOUNDS", "text": "Dogs, cats, birds, lizards, rattlesnakes"},
                 {"date": "ON THE STOVES", "text": "Grasshoppers, fried in hair oil from the camp store"},
                 {"date": "IN THE POT", "text": "Broth of fish heads, grass and wildflowers"},
                 {"date": "OVER THE FENCE", "text": "Food thrown to the officers by enlisted men"}],
        "source": WM + "; " + KE})],
    # 17 by the fall
    [("By the fall", "TC", T(1, 53.0)), ("@", "By the fall", TC_TAG), ("Many had given up", "PL", T(21, 31.4)), ("@", "Many had given up", PL_TAG),
     ("They no longer had", "PL", T(24, 58.1))],
    # 18 exhibition
    [("And yet", "PL", T(2, 55.4)), ("@", "And yet", PL_TAG),
     ("#", "And yet", None, {"type": "Slug", "title": "August 1945", "subtitle": "The prisoners' art exhibition, in an empty barracks"}),
     ("One of the visitors", "PL", T(23, 5.8))],
    # 19 the deal
    [("bare white walls", "PL", T(21, 59.7)), ("@", "bare white walls", "Stand-in · " + PL_TAG.split(" · ")[1]),
     ("The women of the parish", "FF", T(4, 37.3)), ("@", "The women of the parish", FF_TAG)],
    # 20 Di Bello
    [("One of the men chosen", "TC", T(4, 16.9)), ("@", "One of the men chosen", "An Italian officer, Tunisia, 1943 (not Di Bello) · U.S. Army film"),
     ("#", "Like everyone at Hereford", None, {"type": "Slug", "title": "Lt. Franco Di Bello", "subtitle": "23 · captured in North Africa, 1943 · a “Non”"}),
     ("Accounts differ", "TC", T(13, 11.3))],
    # 21 the chaplain
    [("Meanwhile", "PL", T(3, 9.9)), ("@", "Meanwhile", PL_TAG),
     ("#", "Meanwhile", None, {"type": "Slug", "title": "Bishop Laurence J. FitzSimon", "subtitle": "Diocese of Amarillo"})],
    # 22 the letter
    [("He wrote to his congressman", "FF", T(2, 9.4)), ("@", "He wrote to his congressman", FF_TAG),
     ("#", "He wrote to his congressman", None, {"type": "LedgerQuote", "file": "FILE 10 — THE LETTER", "head": "To Rep. Eugene Worley",
        "before": "Then we had ", "key": "bread and water", "after": " and that was all.",
        "who": "Bishop Laurence J. FitzSimon, 1945", "source": WM})],
    # 23 the truck
    [("In late October", "PL", T(23, 15.3)), ("@", "In late October", PL_TAG),
     ("#", "In late October", None, {"type": "Slug", "title": "Late October 1945", "subtitle": "Umbarger, Texas · 26 miles from the camp"}),
     ("The man at the wheel", "PL", T(22, 28.1)),
     ("#", "The man at the wheel", None, {"type": "Slug", "title": "Sgt. John Coyle", "subtitle": "Driver and guard · from a Pennsylvania sock mill"}), ("@", "The man at the wheel", "Stand-in · " + PL_TAG.split(" · ")[1])],
    # 24 dinner
    [("Upstairs", "FF", T(5, 26.6)), ("@", "Upstairs", FF_TAG), ("Downstairs", "FF", T(3, 35.7)), ("roasts, hams", "FF", T(4, 0.3)),
     ("The parish was made up", "PL", T(7, 52.4)), ("@", "The parish was made up", PL_TAG)],
    # 25 eating
    [("The Italians ate so much", "FF", T(0, 43.1)), ("@", "The Italians ate so much", FF_TAG), ("Over the weeks", "FF", T(5, 51.2))],
    # 26 jackrabbits
    [("Sergeant Coyle knew", "PL", T(4, 29.3)), ("@", "Sergeant Coyle knew", PL_TAG), ("So he borrowed", "PL", T(4, 7.6)),
     ("#", "where they were a pest", None, {"type": "LedgerTimeline", "file": "FILE 11 — THE RABBITS", "head": "Sgt. John Coyle's smuggling run",
        "rows": [{"date": "PASTURE", "text": "Jackrabbits shot from a Model A fender"},
                 {"date": "CHURCH", "text": "Skinned, cleaned, hung inside trouser legs"},
                 {"date": "THE GATE", "text": "Walked past the guards at night"},
                 {"date": "BARRACKS", "text": "Roasted jackrabbit for a few hungry men"}],
        "source": WM})],
    # 27 smuggling
    [("He and the farmer", "PL", T(9, 40.4)), ("@", "He and the farmer", "Stand-in · " + PL_TAG.split(" · ")[1]), ("In the evening", "TC", T(17, 38.5)), ("@", "In the evening", TC_TAG)],
    # 28 risk
    [("If he had been caught", "TC", T(16, 16.3)), ("The smuggling went on", "PL", T(4, 51.0))],
    # 29 investigation
    [("The bishop's letter worked", "PL", T(3, 42.4)), ("@", "The bishop's letter worked", PL_TAG),
     ("#", "They found that", None, {"type": "LedgerBars", "file": "FILE 12 — THE FINDING", "head": "Weight lost at Hereford, about seven months", "max": 40,
        "bars": [{"label": "Average prisoner", "value": 20, "figure": "20 lb", "note": "found by the investigators"},
                 {"label": "Some prisoners", "value": 40, "figure": "40 lb", "note": ""}],
        "source": WM + "; " + KE})],
    # 30 the Army
    [("The Army also looked", "TC", T(5, 18.6)), ("@", "The Army also looked", TC_TAG),
     ("#", "In a recorded phone call", "Carvolth told investigators", {"type": "LedgerQuote", "file": "FILE 13 — THE PHONE CALL", "head": "Washington calls Hereford",
        "before": "I don't want you to get worried because ", "key": "I am going to bat for you", "after": " whole hog.",
        "who": "Brig. Gen. B. M. Bryan, assistant provost marshal general, to Col. Carvolth", "source": WM}),
     ("Carvolth told investigators", "PL", T(20, 15.8)), ("By November", "FF", T(0, 30.8)), ("@", "By November", FF_TAG)],
    # 31 the walls
    [("The painting at St. Mary's", "PL", T(14, 37.3)), ("@", "The painting at St. Mary's", PL_TAG), ("On the walls", "PL", T(3, 27.9)),
     ("Through the arches", "PL", T(4, 4.0)), ("The farmhouses in the distance", "PL", T(21, 59.7)),
     ("#", "On the walls", None, {"type": "LedgerTimeline", "file": "FILE 14 — THE WALLS", "head": "St. Mary's Catholic Church, Umbarger, 1945",
        "rows": [{"date": "MURAL", "text": "The Annunciation, before Texas wheat fields"},
                 {"date": "MURAL", "text": "The Visitation, with the parishioners' farmhouses"},
                 {"date": "OIL", "text": "The Assumption of Mary"},
                 {"date": "CARVING", "text": "The Last Supper, on the front of the altar"}],
        "source": WM + "; R. Ross, Texas Highways, Nov. 2023"})],
    # 32 dedication
    [("Two wood carvers", "PL", T(8, 19.4)),
     ("#", "In December", None, {"type": "Slug", "title": "December 1945", "subtitle": "The work at St. Mary's is dedicated · 41 working days"})],
    # 33 the chapel
    [("That same autumn", "PL", T(3, 24.3)), ("@", "That same autumn", PL_TAG),
     ("#", "On the floor", None, {"type": "LedgerQuote", "file": "FILE 15 — THE CHAPEL", "head": "Carved in the chapel floor, in Italian",
        "before": "From the Italian prisoners ", "key": "to the companions who will not return", "after": ".",
        "who": "Inscription, Camp Hereford chapel, 1945 (translated)", "source": "R. Ross, “The Bittersweet Legacy of Hereford's POW Camp,” Texas Highways, Nov. 2023"})],
    # 34 going home
    [("In January", "TT", T(5, 44.2)), ("@", "In January", TT_TAG),
     ("#", "In January", None, {"type": "Slug", "title": "January 1946", "subtitle": "The last 3,999 prisoners leave for Italy"}),
     ("The camp was declared", "PL", T(18, 31.9)), ("@", "The camp was declared", PL_TAG)],
    # 35 Di Bello later
    [("Franco Di Bello went back", "TC", T(4, 58.0)), ("@", "Franco Di Bello went back", "Italian officer, Tunisia, 1943 (not Di Bello) · U.S. Army film"),
     ("#", "a Texas newspaperman", None, {"type": "Slug", "title": "Donald Mace Williams", "subtitle": "Interlude in Umbarger: Italian POWs and a Texas Church (1992)"})],
    # 36 comment ask
    [("If someone in your family", "PL", T(4, 14.9)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Hereford or Umbarger in your family's story?", "subtitle": "Tell us in the comments"})],
    # 37 echo
    [("The camp is gone now", "PL", T(2, 59.0)), ("And in Umbarger", "PL", T(4, 4.0))],
]

WC = "Wikimedia Commons"
SC = f"U.S. Army Signal Corps · public domain · {WC}"
PHOTOS = [
    (2, "The men at those tables", "For months they had", "italian_pows_tunisia_171611.jpg", "02", "Tunisia, 1943", "Italian prisoners taken by the 9th Division, Tunisia, 1 May 1943 (SC 171611)", SC, {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "shipped through the Panama Canal", None, "italian_pows_tunisia_171618.jpg", "04", "North Africa", "Italian soldiers taken prisoner in North Africa, May 1943 (SC 171618)", SC, {"crop": [0.0, 0.15, 1.0, 0.62]}),
    (6, "Many of the men gained", None, "italian_pows_us_180068.jpg", "06", "Italian prisoners in America", "Italian prisoners of war at a camp in the United States (SC 180068)", SC, {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (7, "They played soccer", None, "italian_pows_us_180071.jpg", "07", "The garden", "Italian prisoners of war tend a garden at a U.S. camp (SC 180071)", SC, {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (8, "In other camps", "One German later said", "german_pows_wallace_beef.jpg", "08", "Camp Wallace, Texas", "German prisoners cut a side of beef, part of it for their own kitchen, 1943 (SC 184882)", SC, {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (19, "St. Mary's had bare", "The women of the parish", "st_marys_se.jpg", "19", "St. Mary's, Umbarger", "St. Mary's Catholic Church, Umbarger, Texas, built 1929 (photo 2011)", f"Ammodramus · CC0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (31, "The farmhouses in the distance", None, "st_marys_s.jpg", "31", "St. Mary's today", "St. Mary's Catholic Church, Umbarger; the prisoners' work is still inside", f"Ammodramus · CC0 · {WC}", {"crop": [0.0, 0.25, 1.0, 0.6]}),
    (33, "for the five men", "On the floor", "fort_reno_ortelli.jpg", "33", "Pvt. Innocent Ortelli", "Died at Camp Hereford, August 2, 1945; reburied at Fort Reno, Oklahoma", f"H.L.I.T. · CC BY 2.0 · {WC}", {"crop": [0.0, 0.2, 1.0, 0.56]}),
    (34, "The camp was declared", None, "umbarger_elevator.jpg", "34", "The Panhandle", "Grain elevator, Umbarger, Texas (2011)", f"Charles Henry · CC BY 2.0 · {WC}", {"crop": [0.0, 0.2, 1.0, 0.56]}),
    (37, "The camp is gone now", "And in Umbarger", "hereford_chapel_1.jpg", "37", "The chapel", "The prisoners' chapel at the Camp Hereford site, restored 1988", f"Baldyp · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (37, "And in Umbarger", None, "st_marys_cornerstone.jpg", "37", "Umbarger", "Cornerstone of St. Mary's, Umbarger, 1929", f"Ammodramus · CC0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
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
