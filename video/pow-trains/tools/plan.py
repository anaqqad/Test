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
    "TT": ("troop_train_1943", 1), "PT": ("passenger_train_1940", 1), "RR": ("this_is_my_railroad_1940", 1),
    "GR": ("great_railroad_1942", 1), "CP": ("controlling_german_pows_1944", 1), "TC": ("tunisian_campaign_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

UB = "uboat.net, “Journey to America” (after A. Krammer, Nazi Prisoners of War in America, 1979)"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
PT_TAG = "Stand-in · from The Passenger Train (1940)"
RR_TAG = "Southern Pacific · from This Is My Railroad (1940)"
GR_TAG = "Stand-in · from A Great Railroad at Work (1942)"
CP_TAG = "German prisoners, France, 1944 · U.S. Army film"
TC_TAG = "Axis prisoners, Tunisia, May 1943 · U.S. Army film"
P = [
    # 0 the number
    [("Three", "TC", T(1, 25.3)),
     ("#", "Three hundred", "Most of them crossed", {"type": "BigNumber", "value": 371683, "label": "German prisoners of war in America",
        "source": "May 1945 · U.S. Army census"}),
     ("Most of them crossed", "TT", T(6, 32.5)), ("@", "Most of them crossed", TT_TAG), ("looking out of a window", "TT", T(7, 45.0))],
    # 1 propaganda
    [("They had been told", "PT", T(0, 18.9)), ("@", "They had been told", "Washington, D.C. · from The Passenger Train (1940)"),
     ("#", "an Iowa newspaper", None, {"type": "LedgerQuote", "file": "FILE 01 — WHAT THEY BELIEVED", "head": "A headline, 1944",
        "before": "German prisoners think ", "key": "New York is bombed every day", "after": "",
        "who": "Headline in an Iowa newspaper, 1944", "source": "Iowa Heritage Digital Collections, item 20899"})],
    # 2 rolled west
    [("Then the trains rolled west", "RR", T(15, 20.3)), ("@", "Then the trains rolled west", RR_TAG),
     ("and the men at the windows", "PT", T(4, 5.9)), ("@", "and the men at the windows", PT_TAG),
     ("This is the documented story", "PT", T(5, 21.6))],
    # 3 Tunisia
    [("It started in North Africa", "TC", T(0, 32.9)), ("@", "It started in North Africa", TC_TAG),
     ("#", "In May", None, {"type": "Slug", "title": "May 1943", "subtitle": "Tunisia: about 275,000 Axis soldiers surrender"}),
     ("Britain could not", "TC", T(13, 20.2)), ("Now they came by the shipload", "TC", T(11, 30.6))],
    # 4 ships
    [("Most crossed the Atlantic", "CP", T(14, 28.4)), ("@", "Most crossed the Atlantic", CP_TAG), ("fifteen thousand prisoners", "CP", T(13, 19.6))],
    # 5 convoys
    [("The convoys zigzagged", "CP", T(13, 21.9)), ("But the meals on board", "TT", T(8, 33.3)), ("@", "But the meals on board", TT_TAG)],
    # 6 ports
    [("The ships landed", "GR", T(0, 13.7)), ("@", "The ships landed", GR_TAG),
     ("#", "At the peak", None, {"type": "LedgerBars", "file": "FILE 02 — ARRIVALS", "head": "Prisoners landing in America", "max": 110000,
        "bars": [{"label": "In one month, at the peak", "value": 30000, "figure": "30,000", "note": "Norfolk, New York, Boston"},
                 {"label": "August to November 1944", "value": 110000, "figure": "110,000+", "note": "four months"}],
        "source": "uboat.net, “German POWs in North America”; Wikipedia (after Robin, The Barbed-Wire College, 1995)"})],
    # 7 Graewe
    [("was eighteen when", "CP", T(7, 52.9)), ("@", "was eighteen when", CP_TAG),
     ("#", "In August", None, {"type": "Slug", "title": "August 1944", "subtitle": "Günter Gräwe, 18 · across on the Queen Mary"}),
     ("Then came a long train ride", "RR", T(2, 37.1)), ("@", "Then came a long train ride", RR_TAG)],
    # 8 Norfolk
    [("On January second", "PT", T(0, 31.5)), ("@", "On January second", PT_TAG),
     ("#", "On January second", None, {"type": "Slug", "title": "January 2, 1944", "subtitle": "Norfolk, Virginia · the Empress of Scotland"}),
     ("The men were deloused", "CP", T(7, 35.7)), ("@", "The men were deloused", CP_TAG)],
    # 9 the coaches
    [("Many of them had ridden", "GR", T(16, 42.9)), ("@", "Many of them had ridden", GR_TAG), ("The train at Norfolk", "PT", T(1, 22.0)),
     ("Some prisoners later", "TT", T(5, 32.1)),
     ("#", "These modern coaches", None, {"type": "LedgerQuote", "file": "FILE 03 — THE COACHES", "head": "Reinhold Pabel, Norfolk, January 1944",
        "before": "These modern upholstered coaches were ", "key": "a pleasant surprise", "after": " to everyone.",
        "who": "Reinhold Pabel, Enemies Are Human (1955)", "source": UB})],
    # 10 the porter
    [("Then a Black porter", "TT", T(9, 45.7)), ("@", "Then a Black porter", TT_TAG), ("Pabel never forgot", "PT", T(7, 40.3)), ("@", "Pabel never forgot", PT_TAG),
     ("Most of us, he wrote", "PT", T(8, 5.6))],
    # 11 the rules
    [("The comfort had limits", "TT", T(6, 8.3)), ("@", "The comfort had limits", TT_TAG), ("A prisoner who needed", "TT", T(9, 21.6))],
    # 12 the guards
    [("The Army told its guards", "CP", T(11, 19.2)), ("@", "The Army told its guards", "U.S. Army guard training film, 1944"),
     ("#", "A model guard", None, {"type": "LedgerQuote", "file": "FILE 04 — THE GUARDS", "head": "How to guard a German prisoner",
        "before": "You don't have to be cruel to these guys, but you have to show them they're ", "key": "not going to get away with anything", "after": ".",
        "who": "A model guard, as quoted by Arnold Krammer", "source": UB}),
     ("One instruction warned", "TT", T(5, 56.3))],
    # 13 the window
    [("And then there was the window", "PT", T(5, 9.0)), ("@", "And then there was the window", PT_TAG),
     ("#", "We pressed our noses", None, {"type": "LedgerQuote", "file": "FILE 05 — THE WINDOW", "head": "Virginia and Kentucky, January 1944",
        "before": "En route through Virginia and Kentucky we ", "key": "pressed our noses", "after": " against the windowpanes to take in the sights.",
        "who": "Reinhold Pabel, Enemies Are Human (1955)", "source": "Pabel, ch. 8, “Prisonerland, U.S.A.”"}),
     ("The first thing that struck them", "PT", T(4, 43.8)), ("They were everywhere", "PT", T(10, 49.5)), ("So were the wooden frame houses", "PT", T(8, 30.8))],
    # 14 untouched
    [("The prisoners had come from", "TC", T(20, 30.2)), ("@", "The prisoners had come from", TC_TAG), ("Out here", "PT", T(5, 34.2)), ("@", "Out here", PT_TAG),
     ("The sheer size", "PT", T(6, 24.7)), ("and so did its prosperity", "GR", T(17, 37.8))],
    # 15 paper plates
    [("Some of them saw Black Americans", "PT", T(8, 56.0)), ("@", "Some of them saw Black Americans", PT_TAG), ("Many saw paper plates", "GR", T(15, 47.9)),
     ("@", "Many saw paper plates", GR_TAG),
     ("#", "Many saw paper plates", "One museum exhibit says", {"type": "LedgerTimeline", "file": "FILE 06 — FIRSTS", "head": "New on the train",
        "rows": [{"date": "FOR SOME", "text": "Black Americans, seen for the first time"}, {"date": "FOR MANY", "text": "Paper plates"},
                 {"date": "THE RULE", "text": "Throw them out of the window"}],
        "source": "TRACES, “Held in the Heartland” exhibit panels"}), ("After a meal", "GR", T(14, 25.5)), ("One museum exhibit says", "RR", T(11, 5.9)), ("@", "One museum exhibit says", RR_TAG)],
    # 16 Galhard
    [("Not every journey", "RR", T(9, 6.2)), ("rode to a camp in Colorado", "RR", T(15, 35.3)),
     ("#", "It lasted about", None, {"type": "LedgerTimeline", "file": "FILE 07 — THE HARD RIDE", "head": "Hans Galhard's trip",
        "rows": [{"date": "TO", "text": "Camp Trinidad, Colorado"}, {"date": "LENGTH", "text": "About one hundred hours"},
                 {"date": "NIGHTS", "text": "Slept sitting up"}, {"date": "EACH COACH", "text": "Two pistols, two clubs"}],
        "source": f"Hans Galhard, quoted in {UB}"}),
     ("The men slept sitting up", "TT", T(6, 56.7)), ("@", "The men slept sitting up", TT_TAG)],
    # 17 rare claims
    [("A few prisoners later", "GR", T(16, 15.4)), ("@", "A few prisoners later", GR_TAG), ("Historian Arnold Krammer", "RR", T(12, 50.7))],
    # 18 stations
    [("At every stop", "GR", T(8, 28.3)), ("@", "At every stop", GR_TAG), ("captured in Africa", "PT", T(10, 36.9)), ("@", "captured in Africa", PT_TAG),
     ("#", "They came, he said", None, {"type": "LedgerQuote", "file": "FILE 08 — THE PLATFORMS", "head": "William Oberdieck, on the way to Kansas",
        "before": "They came ", "key": "to see if we had horns", "after": " or something.",
        "who": "William Oberdieck, 1992", "source": "C. Mayer, Knight-Ridder, in the Seattle Times, 29 Nov. 1992"})],
    # 19 letters
    [("Not everyone was curious", "TT", T(1, 30.6)), ("@", "Not everyone was curious", TT_TAG),
     ("#", "One suggested", None, {"type": "LedgerQuote", "file": "FILE 09 — THE MAIL", "head": "One of hundreds of letters a week",
        "before": "", "key": "Put them in Death Valley", "after": ", chuck in a side of beef, and let them starve to death.",
        "who": "A letter to the Army's prisoner of war division", "source": f"Collier's, quoted in {UB}"})],
    # 20 Mexia
    [("in Texas, three thousand", "TC", T(0, 11.0)), ("@", "in Texas, three thousand", TC_TAG),
     ("#", "in Texas, three thousand", None, {"type": "Slug", "title": "Mexia, Texas", "subtitle": "3,250 prisoners · a town of about 6,000"}),
     ("Still wearing their desert khaki", "TC", T(13, 38.0))],
    # 21 last meal
    [("In Kansas", "TT", T(6, 44.6)), ("@", "In Kansas", TT_TAG), ("are they going to shoot us", "PT", T(7, 2.5)), ("@", "are they going to shoot us", PT_TAG),
     ("The tables were set", "GR", T(15, 20.4))],
    # 22 Trimmingham
    [("There were other men", "TT", T(8, 45.3)), ("@", "There were other men", TT_TAG),
     ("#", "and eight other Black soldiers", None, {"type": "Slug", "title": "1944", "subtitle": "Cpl. Rupert Trimmingham and eight other Black soldiers"}),
     ("At a lunchroom", "PT", T(7, 52.9)), ("@", "At a lunchroom", PT_TAG), ("while about two dozen", "PT", T(8, 5.6))],
    # 23 the letter
    [("wrote to the Army magazine", "PT", T(9, 21.2)),
     ("#", "wrote to the Army magazine", "The historian John Hope Franklin", {"type": "LedgerQuote", "file": "FILE 10 — THE LETTER", "head": "To Yank, the Army weekly, April 1944",
        "before": "Then why are they ", "key": "treated better than we are?", "after": "",
        "who": "Cpl. Rupert Trimmingham", "source": "M. Taub, TIME, 28 July 2020 (after M. Reiss)"}),
     ("He was not alone", "TT", T(7, 32.9)), ("@", "He was not alone", TT_TAG)],
    # 24 1948
    [("The Army would stay", "TT", T(10, 22.0)),
     ("#", "The Army would stay", None, {"type": "Slug", "title": "1948", "subtitle": "President Truman orders the armed forces desegregated"})],
    # 25 the camps
    [("In the camps", "CP", T(11, 53.6)), ("@", "In the camps", CP_TAG), ("Most were still in America", "RR", T(4, 21.9)), ("@", "Most were still in America", RR_TAG)],
    # 26 Graewe
    [("Decades later", "RR", T(16, 35.1)),
     ("#", "We were always treated", None, {"type": "LedgerQuote", "file": "FILE 11 — LOOKING BACK", "head": "Günter Gräwe, back at Fort Lewis, 2017",
        "before": "We always were ", "key": "treated with fairness", "after": ", got sufficient food and 80 cents a day.",
        "who": "Günter Gräwe", "source": "M. McCaffrey, HistoryLink.org essay 20472 (2017)"})],
    # 27 Pabel
    [("the prisoner from the Norfolk train", "PT", T(1, 59.8)), ("@", "the prisoner from the Norfolk train", PT_TAG), ("In September", "RR", T(13, 35.6))],
    # 28 comment ask
    [("If someone in your family", "TT", T(5, 44.2)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "A train ride in your family's story?", "subtitle": "Tell us in the comments"})],
    # 29 echo
    [("Three hundred seventy thousand men", "PT", T(11, 2.1)), ("They found out the truth", "PT", T(4, 5.9))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (3, "Britain could not", None, "tunisia_stockade_1943.jpg", "03", "Tunisia", "German prisoners arrive at a stockade in Tunisia, May 1943 (Signal Corps SC 171622)", f"U.S. Army · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "Most crossed the Atlantic", "Some came on great ocean liners", "liberty_convoy_1943.jpg", "04", "Liberty ship", "An American Liberty ship in a convoy to North Africa, April 1943 (IWM A 16335)", f"C. H. Parnall · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "Some came on great ocean liners", None, "queen_mary_1945.jpg", "04", "Queen Mary", "The Queen Mary in wartime gray, New York harbor, June 1945", f"U.S. Navy · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (23, "The historian John Hope Franklin", None, "john_hope_franklin.jpg", "23", "John Hope Franklin", "Historian John Hope Franklin at a National Archives council meeting", f"National Archives · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
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
