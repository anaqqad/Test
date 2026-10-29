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
    "RR": ("this_is_my_railroad_1940", 1), "RR2": ("this_is_my_railroad_1940_b", 1), "SKI": ("ski_safety_1942", 1), "SKN": ("ski_newsreel_1946", 1),
    "SF": ("san_francisco_1941", 1), "AZ": ("arizona_1940", 1), "DES": ("land_and_live_desert_1944", 1), "TC": ("tunisian_campaign_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

LA = "D. Holley and C. McGraw, Los Angeles Times, 11 Sept. 1985"
RR_TAG = "Southern Pacific · from This Is My Railroad (1940)"
SKI_TAG = "Stand-in · U.S. Army ski film (1942)"
SF_TAG = "The West Coast, 1941 · San Francisco (Summers collection)"
DES_TAG = "Stand-in · from Land and Live in the Desert (1944)"
AZ_TAG = "The desert Southwest, 1940 · U.S. Bureau of Mines film"
TC_TAG = "German and Italian prisoners, Tunisia, May 1943 · U.S. Army film"
P = [
    # 0 cold open
    [("Early in", "RR2", T(3, 16.8)), ("@", "Early in", "Stand-in · from This Is My Railroad (1940)"),
     ("#", "Early in", None, {"type": "Slug", "title": "Early 1984", "subtitle": "A marriage of twenty years"}),
     ("She had been married", "SF", T(3, 49.6)), ("@", "She had been married", SF_TAG)],
    # 1 the quote
    [("Her bags were packed", "RR2", T(4, 51.2)),
     ("#", "Her bags were packed", "So he told her", {"type": "LedgerQuote", "file": "FILE 01 — THE TAXI", "head": "Why he finally talked",
        "before": "", "key": "Her bags were packed and a taxi was waiting", "after": ".", "who": "Georg Gärtner, 1985", "source": f"Quoted in {LA}"}),
     ("So he told her", "SKI", T(4, 30.6)), ("@", "So he told her", SKI_TAG), ("His name was not", "SKI", T(8, 45.3)),
     ("It was Georg", "TC", T(0, 11.0)), ("@", "It was Georg", TC_TAG), ("The ski instructor", "SKI", T(8, 13.4))],
    # 2
    [("About a year and a half later", "SF", T(4, 55.2)), ("@", "About a year and a half later", SF_TAG),
     ("#", "About a year and a half later", None, {"type": "Slug", "title": "September 1985", "subtitle": "San Pedro, California"}),
     ("He was sixty-four", "SF", T(5, 34.6)), ("This is his documented story", "RR", T(11, 5.9)), ("@", "This is his documented story", RR_TAG)],
    # 3 Silesia
    [("Georg Gärtner was born", "RR", T(2, 37.1)), ("In nineteen forty", "TC", T(2, 22.5)), ("He was sent to North Africa", "TC", T(13, 20.2))],
    # 4 Tunisia
    [("In May", "TC", T(0, 32.9)), ("@", "In May", TC_TAG),
     ("#", "In May", None, {"type": "Slug", "title": "May 1943", "subtitle": "Tunisia: about 275,000 Axis soldiers surrender"}),
     ("Gärtner was one of them", "TC", T(11, 30.6))],
    # 5 Camp Deming
    [("Like hundreds of thousands", "SF", T(3, 23.4)), ("By the end of the war", "TC", T(16, 15.6)),
     ("#", "By the end of the war", None, {"type": "LedgerTimeline", "file": "FILE 02 — PRISONERS IN AMERICA", "head": "Where he ended up",
        "rows": [{"date": "HELD", "text": "About 425,000 German prisoners"}, {"date": "CAMPS", "text": "About 700, across the country"},
                 {"date": "HIS CAMP", "text": "Deming, New Mexico · camp translator"}],
        "source": f"Wikipedia, “German prisoners of war in the United States”; {LA}"}),
     ("He became the camp's translator", "AZ", T(17, 59.0)), ("@", "He became the camp's translator", AZ_TAG)],
    # 6 peace
    [("In May", "RR", T(5, 6.8)), ("@", "In May", RR_TAG), ("For most of the prisoners", "RR2", T(2, 45.3)), ("They expected to be sent", "RR", T(6, 51.5))],
    # 7 not quickly
    [("It did not happen quickly", "RR", T(9, 6.2)), ("@", "It did not happen quickly", RR_TAG),
     ("#", "It did not happen quickly", None, {"type": "LedgerTimeline", "file": "FILE 03 — GOING HOME", "head": "The long way back",
        "rows": [{"date": "MAY 1945", "text": "The war in Europe ends"}, {"date": "TO 1946", "text": "Most still working in the U.S."},
                 {"date": "UP TO 3 YEARS", "text": "Some put to work in Britain and France"}, {"date": "1947", "text": "U.S. asks France to free them by October"}],
        "source": "Wikipedia, “German prisoners of war in the United States” (Carlson 1997); FRUS 1947, vol. III, doc. 401"}),
     ("For Gärtner", "AZ", T(31, 49.2))],
    # 8 horror
    [("Schweidnitz had been taken", "TC", T(12, 58.3)),
     ("#", "Gärtner later said", None, {"type": "LedgerQuote", "file": "FILE 04 — HOME", "head": "Why he ran",
        "before": "What for many was a moment of celebration, was for me ", "key": "a time of horror", "after": " as I visualized the brutality which awaited me at the hands of the Russians.",
        "who": "Georg Gärtner, 1985", "source": f"Quoted in {LA}"}),
     ("He decided that the only way", "DES", T(1, 37.5)), ("@", "He decided that the only way", DES_TAG)],
    # 9 the plan
    [("He studied the railroad", "RR", T(0, 37.4)), ("@", "He studied the railroad", RR_TAG), ("He told no one", "RR", T(15, 35.3))],
    # 10 the boxcar
    [("On the night of", "DES", T(24, 7.5)), ("@", "On the night of", DES_TAG),
     ("#", "On the night of", None, {"type": "Slug", "title": "September 21, 1945", "subtitle": "Camp Deming, New Mexico"}),
     ("he crept under the fences", "DES", T(25, 37.5)), ("The train carried him west", "RR", T(15, 20.3)), ("@", "The train carried him west", RR_TAG),
     ("His first stop", "SF", T(5, 8.3))],
    # 11 escapes
    [("He was one of more than", "DES", T(31, 10.8)),
     ("#", "He was one of more than", None, {"type": "LedgerBars", "file": "FILE 05 — ESCAPES", "head": "German prisoners who ran", "max": 2222,
        "bars": [{"label": "Escaped from U.S. camps", "value": 2222, "figure": "2,222", "note": "most caught within a day"},
                 {"label": "Unaccounted for at repatriation", "value": 7, "figure": "7", "note": "Gärtner among the missing"}],
        "source": f"Wikipedia, “German prisoners of war in the United States”, citing {LA}"}),
     ("Gärtner was one of the men", "RR", T(12, 50.7))],
    # 12 West Coast
    [("For the next year", "SF", T(0, 19.7)), ("@", "For the next year", SF_TAG), ("He washed dishes", "SF", T(7, 6.4)), ("At first he called himself", "RR", T(9, 6.2))],
    # 13 Dennis Whiles
    [("Then he settled on another name", "RR2", T(2, 13.8)), ("@", "Then he settled on another name", "Stand-in · from This Is My Railroad (1940)"),
     ("#", "Then he settled on another name", None, {"type": "LedgerTimeline", "file": "FILE 06 — A NEW MAN", "head": "Becoming someone else",
        "rows": [{"date": "1945", "text": "“Peter Petersen”, a Norwegian immigrant"}, {"date": "LATER", "text": "“Dennis Whiles” · Social Security card"},
                 {"date": "COVER STORY", "text": "Raised in an orphanage"}],
        "source": f"{LA}; Wikipedia, “Georg Gärtner” (after his 1985 memoir)"})],
    # 14 Norden
    [("He moved to Norden", "RR2", T(4, 51.2)), ("In winter he taught skiing", "SKI", T(1, 51.4)), ("@", "In winter he taught skiing", SKI_TAG),
     ("In summer", "RR", T(2, 52.1)),
     ("#", "Meanwhile, the F B I", None, {"type": "LedgerTimeline", "file": "FILE 07 — THE MANHUNT", "head": "Wanted",
        "rows": [{"date": "1947", "text": "FBI wanted posters"}, {"date": "1963", "text": "The Army ends its search"}],
        "source": "Wikipedia, “Georg Gärtner”"})],
    # 15 1952
    [("In January", "RR2", T(5, 7.0)), ("@", "In January", "Sierra Nevada snow · from This Is My Railroad (1940)"),
     ("#", "In January", None, {"type": "Slug", "title": "January 13, 1952", "subtitle": "The City of San Francisco, snowbound near Yuba Pass"}),
     ("It took six days", "RR2", T(7, 12.9)), ("Hundreds of workers", "RR2", T(9, 3.1)), ("Gärtner later wrote", "SKI", T(4, 30.6)),
     ("@", "Gärtner later wrote", SKI_TAG), ("Life magazine", "RR2", T(5, 54.2)), ("Nobody recognized", "SKI", T(22, 1.1))],
    # 16 Jean
    [("At a", "SF", T(1, 25.3)), ("@", "At a", SF_TAG),
     ("#", "They married in", None, {"type": "Slug", "title": "1964", "subtitle": "Dennis Whiles marries Jean Clarke"})],
    # 17
    [("He worked as a tennis pro", "SKN", T(0, 57.7)), ("@", "He worked as a tennis pro", "Stand-in · ski jumping, United News, 1946"), ("With Jean", "SF", T(3, 10.2)),
     ("They moved to Hawaii", "RR", T(7, 21.5)), ("He could not get a passport", "RR2", T(3, 32.5))],
    # 18 family
    [("He believed his family", "TC", T(17, 21.4))],
    # 19 Boulder
    [("By", "RR", T(7, 6.5))],
    # 20 the bags
    [("Early in", "RR2", T(4, 35.5)), ("Jean became so frightened", "RR2", T(3, 16.8)), ("The bags were packed", "SF", T(4, 15.9)), ("Dennis Whiles told her", "RR2", T(5, 22.7))],
    # 21 the book
    [("She did not leave", "SF", T(2, 17.8)),
     ("#", "They called the book", None, {"type": "Slug", "title": "Hitler's Last Soldier in America", "subtitle": "Georg Gaertner with Arnold Krammer, Stein & Day, 1985"}),
     ("He began working with", "RR", T(13, 35.6)), ("Krammer was the scholar", "RR", T(10, 36.0)), ("Now one of those prisoners", "RR", T(14, 20.5))],
    # 22 the surrender
    [("In September", "SF", T(5, 47.7)), ("In front of reporters", "SF", T(7, 45.8))],
    # 23 Today show
    [("The timing was not", "RR", T(10, 51.0)), ("On national television", "SF", T(0, 6.6))],
    # 24 INS
    [("Then came the question", "RR", T(1, 22.3)),
     ("#", "The regional commissioner", None, {"type": "LedgerTimeline", "file": "FILE 08 — WHAT TO DO WITH HIM", "head": "The immigration service's view, 1985",
        "rows": [{"date": "STATUS", "text": "A deportable alien"}, {"date": "BUT", "text": "Married to a U.S. citizen for 20+ years"},
                 {"date": "OUTLOOK", "text": "Chances of staying: excellent"}],
        "source": LA})],
    # 25 citizen
    [("He was never sent away", "RR", T(4, 21.9)), ("He went on living", "RR", T(16, 35.1))],
    # 26 death
    [("Georg Gärtner died", "SKI", T(2, 55.1)),
     ("#", "Georg Gärtner died", None, {"type": "Slug", "title": "Georg Gärtner, 1920–2013", "subtitle": "The last escaped German prisoner of war in America"}),
     ("For forty years", "RR", T(12, 5.8))],
    # 27 comment ask
    [("If someone in your family", "SF", T(3, 49.6)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "A prisoner in your family's story?", "subtitle": "Tell us in the comments"})],
    # 28 echo
    [("In nineteen forty-five", "RR", T(11, 20.9)), ("One man looked at the map", "RR", T(3, 37.0)), ("and jumped on a train", "RR", T(15, 20.3)),
     ("He spent forty years", "RR", T(17, 50.0)), ("It took a packed suitcase", "AZ", T(39, 13.0))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (3, "Georg Gärtner was born", None, "schweidnitz_street.jpg", "03", "Schweidnitz", "Friedrichstraße, Schweidnitz, Silesia, early 1900s postcard (today Świdnica, Poland)", f"Ottmar Zieher · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (10, "and climbed into an open", None, "sp_boxcar.jpg", "10", "Southern Pacific", "A wooden-sided Southern Pacific boxcar of the period", f"DPLA · no known restrictions · {WC}", {"focus": [0.5, 0.5]}),
    (18, "They had not", None, "schweidnitz_church.jpg", "18", "Home", "The parish church of Schweidnitz, early 1900s postcard", f"Trinks & Co. · public domain · {WC}", {"focus": [0.5, 0.35]}),
    (19, "By", None, "flatirons_boulder.jpg", "19", "Boulder, Colorado", "The Flatirons above Boulder, Colorado", f"Jesse Varner · CC BY-SA 2.5 · {WC}", {"focus": [0.6, 0.4]}),
    (22, "In September", None, "terminal_island.jpg", "22", "Terminal Island", "Terminal Island and San Pedro harbor, Los Angeles, 2002", f"P. Alejandro Díaz · CC BY-SA 2.0 · {WC}", {"focus": [0.5, 0.5]}),
    (25, "and in 2009", None, "gaertner_2009.jpg", "25", "Georg Gärtner", "Georg Gärtner, then 89, on the Fourth of July, 2009", f"FaKK · public domain · {WC}", {"focus": [0.5, 0.3]}),
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
