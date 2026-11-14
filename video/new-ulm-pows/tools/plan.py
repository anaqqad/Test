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
    "PP": ("pick_of_the_pod_1939", 1), "PL": ("power_and_the_land_1940", 1), "DN": ("detroit_news_1917", 1),
    "BM": ("better_minnesota_1937", 1), "CP": ("controlling_german_pows_1944", 1), "ADC": ("prisoners_shipped_adc140", 1),
    "TC": ("tunisian_campaign_1943", 1), "GGU": ("germany_gives_up_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

S = {}

BUCK = "Anita A. Buck, Behind Barbed Wire (1998), ch. 13"
BUCKJ = "Brown County Journal, June 1944 · quoted in Anita A. Buck, Behind Barbed Wire (1998)"
PLUTH = "Edward J. Pluth, Minnesota History 44:8 (Winter 1975)"
MNOP = "MNopedia, New Ulm Military Draft Meeting, 1917 · Minnesota Historical Society"
GEN = "Convention relative to the Treatment of Prisoners of War, Geneva, July 27, 1929 · Bevans, vol. 2 · Library of Congress"
SIM = "Dean B. Simmons, Swords into Plowshares (2000), as cited by Wikipedia"
PPF_TAG = "Stand-in · pea harvest, 1939 · from Pick of the Pod (California Packing Corp.)"
PPC_TAG = "Stand-in · a California Packing Corp. pea cannery, 1939 · from Pick of the Pod"
PL_TAG = "Stand-in · a Midwest farm, 1940 · from Power and the Land"
DN_TAG = "Stand-in · crowds in a Midwest town, late 1910s · Detroit News newsreel"
BM_TAG = "Stand-in · Depression work crews in Minnesota · from A Better Minnesota (WPA, 1937)"
BMD_TAG = "WPA crews build a dam in Minnesota, 1930s · from A Better Minnesota (WPA, 1937)"
CP_TAG = "Stand-in · German prisoners in U.S. Army hands · from Controlling German Prisoners of War (War Dept., 1944)"
ADC_TAG = "Stand-in · German prisoners board ships in North Africa · U.S. Army film, 1943"
TC_TAG = "Stand-in · German prisoners on trucks, Tunisia, May 1943 · U.S. Army film"
GGU_TAG = "Germany surrenders, May 1945 · Universal Newsreel"
WC = "Wikimedia Commons"
DOCU = "Flip Schulke · DOCUMERICA, National Archives · public domain"
P = [
    # 0 Broadway
    [("In", "TC", T(13, 20.2)), ("@", "In June", TC_TAG),
     ("#", "In June", None, {"type": "Slug", "title": "June 1944", "subtitle": "New Ulm, Minnesota · Broadway"}),
     ("In the back sat", "ADC", T(5, 16.5)), ("@", "In the back sat", ADC_TAG), ("and the prisoners stared", "CP", T(12, 5.5))],
    # 1 the local paper
    [("The local paper", "CP", T(7, 38.0)), ("@", "The local paper", CP_TAG),
     ("#", "The local paper", None, {"type": "LedgerQuote", "file": "FILE 01 — BROADWAY", "head": "Brown County Journal, June 1944",
        "before": "", "key": "Excitement reigned along Broadway for a short time this morning", "after": " as the first detachment of Nazi war prisoners rolled into the city.",
        "who": "Brown County Journal, New Ulm", "source": BUCKJ})],
    # 2 no translator
    [("In this town", "PL", T(21, 23.5)), ("@", "In this town", PL_TAG), ("This is the documented story", "CP", T(7, 54.0)), ("@", "This is the documented story", CP_TAG)],
    # 3 the town
    [("New Ullm was founded", "PL", T(7, 18.6)), ("By nineteen forty", "PL", T(8, 34.9)), ("@", "By nineteen forty", PL_TAG)],
    # 4 1917
    [("The town had paid", "DN", T(0, 6.6)), ("@", "The town had paid", DN_TAG),
     ("#", "In July nineteen seventeen", None, {"type": "Slug", "title": "July 25, 1917", "subtitle": "New Ulm · a meeting about the new draft"}),
     ("told the young men", "DN", T(3, 10.9))],
    # 5 removed
    [("The state's Commission", "PL", T(7, 18.6)),
     ("#", "The state's Commission", None, {"type": "LedgerTimeline", "file": "FILE 02 — 1917", "head": "New Ulm and the draft",
        "rows": [{"date": "JULY 25, 1917", "text": "About 8,000 at the draft meeting, in a town of 6,000"},
                 {"date": "AUG. 21, 1917", "text": "Mayor Fritsche and attorney Pfaender suspended"},
                 {"date": "DEC. 1, 1917", "text": "Both removed from office"},
                 {"date": "BY 1920", "text": "Both back in office"}],
        "source": MNOP}),
     ("Twenty-seven years later", "TC", T(0, 11.0)), ("@", "Twenty-seven years later", TC_TAG)],
    # 6 peas
    [("The reason was peas", "PP", T(7, 19.7)), ("@", "The reason was peas", PPF_TAG),
     ("#", "With so many men", None, {"type": "LedgerBars", "file": "FILE 03 — THE LABOR", "head": "Minnesota's canneries, 1944", "max": 31000,
        "bars": [{"label": "Workers the canners expected to need", "value": 31000, "figure": "31,000+", "note": ""},
                 {"label": "Prisoners they said they could use", "value": 3000, "figure": "3,000+", "note": ""},
                 {"label": "German prisoners sent to Minnesota", "value": 1275, "figure": "about 1,275", "note": "1944"}],
        "source": PLUTH})],
    # 7 the camp
    [("The camp outside", "BM", T(7, 54.3)), ("@", "The camp outside", BM_TAG), ("The Army rented it", "PL", T(9, 51.2)), ("In June about", "TC", T(13, 42.2)), ("@", "In June about", TC_TAG)],
    # 8 Sleepy Eye
    [("They worked twelve-hour", "PP", T(11, 36.3)), ("@", "They worked twelve-hour", PPC_TAG),
     ("#", "They worked twelve-hour", None, {"type": "Slug", "title": "Sleepy Eye, Minnesota", "subtitle": "The cannery · twelve-hour shifts"}),
     ("packing peas and corn", "PP", T(16, 50.3)), ("The prisoners were paid", "PP", T(19, 35.6))],
    # 9 the warning
    [("The Army warned", "CP", T(7, 34.6)),
     ("#", "The Army warned", None, {"type": "LedgerQuote", "file": "FILE 04 — THE WARNING", "head": "Army notice to residents near the camps, 1944",
        "before": "", "key": "communicate, consort with, give aid or comfort", "after": "",
        "who": "Lt. Col. Arthur T. Lobdell, commander, Camp Algona, Iowa", "source": PLUTH}),
     ("The camp's commander", "CP", T(12, 5.5)), ("@", "The camp's commander", CP_TAG)],
    # 10 article 2
    [("The rules came", "CP", T(0, 32.2)),
     ("#", "Its second article", None, {"type": "LedgerDocument", "file": "FILE 05 — ARTICLE 2", "head": "Prisoners of war", "source": GEN,
        "spans": [{"doc": "doc_art2", "say": "must at all times be humanely treated and protected particularly against acts of violence insults and public curiosity"}]})],
    # 11 article 11
    [("And its eleventh", "CP", T(12, 5.5)),
     ("#", "And its eleventh", None, {"type": "LedgerDocument", "file": "FILE 06 — ARTICLE 11", "head": "Food", "source": GEN,
        "spans": [{"doc": "doc_art11", "say": "the food ration of prisoners of war shall be equal in quantity and quality to that of troops at base camps"}]}),
     ("The prisoners' spokesman", "CP", T(11, 42.9)), ("@", "The prisoners' spokesman", CP_TAG)],
    # 12 the eggs
    [("Within days", "PL", T(16, 12.5)), ("@", "Within days", PL_TAG), ("One told them in German", "CP", T(12, 34.5)), ("@", "One told them in German", CP_TAG),
     ("The prisoners wanted to know", "CP", T(11, 33.9))],
    # 13 the pastor
    [("A Lutheran pastor", "PL", T(21, 52.9)), ("@", "A Lutheran pastor", PL_TAG),
     ("#", "He said he would treat", None, {"type": "LedgerQuote", "file": "FILE 07 — THE PASTOR", "head": "Services in German at the camp",
        "before": "", "key": "I will treat them as I would like my son treated if he were captured.", "after": "",
        "who": "The Rev. E. J. Markhausen, Emanuel Lutheran Church, Courtland", "source": BUCK}),
     ("At the cannery American", "PP", T(18, 29.5)), ("@", "At the cannery American", PPC_TAG)],
    # 14 the concerts
    [("On Sunday afternoons", "CP", T(11, 33.9)), ("@", "On Sunday afternoons", CP_TAG), ("People from New Ullm came", "PL", T(24, 34.9)), ("@", "People from New Ullm came", PL_TAG),
     ("One former prisoner", "CP", T(7, 37.8))],
    # 15 subscribe (midpoint)
    [("If you want more", "PP", T(9, 30.9)), ("@", "If you want more", PPF_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 16 the guards
    [("The guards could not", "CP", T(12, 8.7)), ("@", "The guards could not", CP_TAG), ("At the cannery they", "PP", T(11, 52.8)), ("@", "At the cannery they", PPC_TAG),
     ("#", "Sometimes the prisoners", None, {"type": "LedgerQuote", "file": "FILE 08 — THE GUARDS", "head": "Sleepy Eye cannery, 1944",
        "before": "", "key": "We can't go home without the guards.", "after": "",
        "who": "German prisoners at the cannery, as the staff remembered it", "source": BUCK})],
    # 17 the farms
    [("Then farmers began", "PL", T(11, 7.4)), ("@", "Then farmers began", PL_TAG), ("They ate meat", "PL", T(18, 12.1)), ("@", "They ate meat", PL_TAG)],
    # 18 Ramberg
    [("One farmer Carl", "PL", T(23, 36.0)),
     ("#", "He said they weren't", None, {"type": "LedgerQuote", "file": "FILE 09 — THE FARMER", "head": "Remembered in 1985",
        "before": "", "key": "We weren't supposed to feed them, but you couldn't expect them to work on an empty stomach.",
        "after": " We weren't supposed to visit with them, either, which was rather cruel.",
        "who": "Carl Ramberg, farmer near New Ulm", "source": BUCK})],
    # 19 the weekend
    [("One family went further", "PL", T(18, 26.8)), ("@", "One family went further", PL_TAG),
     ("#", "One family went further", None, {"type": "Slug", "title": "The weekend", "subtitle": "Camp New Ulm · the only recorded escape"}),
     ("On Sunday afternoon", "PL", T(9, 13.0))],
    # 20 the fine
    [("Lick-ten-berg went into", "CP", T(7, 50.7)), ("@", "Lick-ten-berg went into", CP_TAG),
     ("#", "The Americans went to court", None, {"type": "LedgerTimeline", "file": "FILE 10 — THE WEEKEND", "head": "Camp New Ulm, 1944",
        "rows": [{"date": "THE PRISONER", "text": "Helmut Lichtenberg: solitary confinement"},
                 {"date": "THE FAMILY", "text": "Fined $300 and lectured by the judge"},
                 {"date": "ONE ACCOUNT", "text": "They had also taken him to church"}],
        "source": SIM})],
    # 21 Joyce
    [("Not everyone", "PL", T(19, 25.7)),
     ("#", "A woman named Joyce", None, {"type": "LedgerQuote", "file": "FILE 11 — NOT EVERYONE", "head": "New Ulm, remembered in 1985",
        "before": "", "key": "They made me angry. My husband was over there. I was bitter.", "after": "",
        "who": "Joyce Aufderheide", "source": BUCK})],
    # 22 Jack
    [("Her husband Jack", "PL", T(16, 50.7)), ("@", "Her husband Jack", PL_TAG), ("He found German prisoners", "CP", T(12, 5.5)), ("@", "He found German prisoners", CP_TAG),
     ("A few weeks after", "PL", T(13, 40.0))],
    # 23 the letters
    [("In the spring", "PL", T(20, 24.6)), ("@", "In the spring", PL_TAG), ("One local history", "PL", T(22, 22.4))],
    # 24 the end of the camp
    [("The prisoners stayed", "PP", T(8, 51.6)), ("@", "The prisoners stayed", PPF_TAG),
     ("#", "That summer the prisoners", None, {"type": "LedgerTimeline", "file": "FILE 12 — THE CAMP", "head": "Camp New Ulm, 1944–1945",
        "rows": [{"date": "JUNE 1944", "text": "About 150 prisoners arrive"},
                 {"date": "WINTER 1944–45", "text": "Kept over the winter: brick and tile yards"},
                 {"date": "JULY 1945", "text": "317 prisoners at the camp"},
                 {"date": "SUMMER 1945", "text": "Prisoners credited with saving 65% of Minnesota's record pea crop"},
                 {"date": "DECEMBER 1945", "text": "The camp closes"}],
        "source": f"{BUCK}; {PLUTH}"})],
    # 25 none stayed
    [("Fifty years later", "PL", T(25, 4.3)), ("@", "Fifty years later", PL_TAG)],
    # 26 Richter
    [("Some did come back", "ADC", T(5, 41.6)), ("@", "Some did come back", ADC_TAG), ("In nineteen eighty-five", "PL", T(25, 19.0)), ("@", "In nineteen eighty-five", PL_TAG)],
    # 27 comment ask
    [("If your family", "PL", T(23, 21.2)), ("@", "If your family", PL_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "German at home, during the war?", "subtitle": "Or beside prisoners on a farm · tell us in the comments"})],
    # 28 the cabins
    [("The log cabins", "BM", T(4, 48.5)), ("@", "The log cabins", BMD_TAG), ("The camp is now", "PL", T(16, 12.5)), ("Visitors can ask", "PL", T(6, 40.5)), ("Its dam was taken down", "BM", T(4, 16.9)), ("and the river runs", "PL", T(7, 56.7))],
]

PHOTOS = [
    (0, "People stopped", None, "new_ulm_1918.jpg", "00", "Broadway, New Ulm", "\"A Daily Scene in Busy New Ulm, 1918\" (postcard)", f"Public domain · {WC}", {}),
    (2, "New Ullm had been founded", None, "new_ulm_houses_1975.jpg", "02", "New Ulm, 1974", "Founded in 1854 by German immigrants", f"{DOCU} · {WC}", {}),
    (3, "New Ullm was founded", None, "new_ulm_1906.jpg", "03", "New Ulm, about 1906", "Panorama by George R. Lawrence", f"Library of Congress · public domain · {WC}", {}),
    (3, "On a hill above", None, "hermann_close_1975.jpg", "03B", "Hermann", "The Hermann statue above New Ulm, built 1888–1897 (photo 1974)", f"{DOCU} · {WC}", {}),
    (4, "The mayor Louis", None, "fritsche.jpg", "04", "Dr. Louis A. Fritsche", "Mayor of New Ulm, 1912–1920", f"Bain News Service · Library of Congress · public domain · {WC}", {}),
    (7, "log cabins in the", None, "flandrau_group_camp.jpg", "07", "The same cabins", "Camp New Ulm's buildings today, Flandrau State Park", f"McGhiever · CC BY-SA 3.0 · {WC}", {}),
    (7, "Most were young airmen", None, "young_pows_1944.jpg", "07B", "Stand-in · young German prisoners", "Captured near Kinzweiler, Germany, Nov. 21, 1944 (not New Ulm)", f"U.S. Army Signal Corps SC 196558 · public domain · badges blurred · {WC}", {}),
    (17, "A farmer would pick", None, "camp_wallace_a.jpg", "17", "Stand-in · a farm detail", "German prisoners mowing near Camp Wallace, Texas, 1943 (not Minnesota)", f"U.S. Army Signal Corps SC 184879 · public domain · {WC}", {}),
    (23, "letters from New", None, "vmail_poster.jpg", "23", "Mail from the front", "Army V-mail poster, World War II", f"Boston Public Library · CC BY 2.0 · {WC}", {}),
    (25, "Fifty years later", None, "new_ulm_street.jpg", "25", "New Ulm today", "Minnesota Street, July 2021", f"Greg Gjerdingen · CC BY 2.0 · {WC}", {}),
    (28, "The camp is now", None, "flandrau_group_camp.jpg", "28", "Flandrau State Park", "The group center: Camp New Ulm's cabins, 2011", f"McGhiever · CC BY-SA 3.0 · {WC}", {}),
    (28, "The lake where", None, "cottonwood_river.jpg", "28B", "The Cottonwood River", "Flandrau State Park, 2007", f"Tim Kiser · CC BY-SA 2.5 · {WC}", {}),
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
