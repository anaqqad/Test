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

F = {  # film key -> file in assets/footage, crop of burned-in timecode (fraction of height kept)
    "FH": ("freedom_highway_1956", 1), "CHI": ("chicago_1936", 1), "BL": ("bright_lights_1935", 1),
    "POW": ("pow_control_1944", 1), "TT": ("troop_train_1943", 1), "NN": ("newport_news_1943", 0.78),
    "HAM": ("hamburg_bombed_1943", 1), "NAP": ("pows_naples_1943", 0.78), "GGU": ("germany_gives_up_1945", 1),
    "XM": ("x_marks_the_spot_1942", 1), "WO": ("wochenschau_1943", 1), "AH": ("american_harvest_1955", 1),
    "ASL": ("and_so_they_live_1940", 1), "NP": ("news_parade_1945", 1), "SIC": ("sicily_invasion_1943", 1),
    "SP": ("san_pietro_1945", 1), "LON": ("london_can_take_it_1940", 1), "RUS": ("battle_of_russia_1943", 1),
    "CON": ("atlantic_convoy_1942", 1), "CITY": ("the_city_1939", 1), "CAN": ("cannery_calpak_1950", 1),
    "ART": ("arteries_nyc_1941", 1), "TUE": ("tuesday_in_november_1945", 1), "NOD": ("news_of_the_day_1943", 1),
}

def T(m, s=0.0):
    return m * 60 + s

# (anchor, film, source time). Context labels: ("@label", anchor, text). Cards: ("#card", anchor, until_anchor|None, {...})
P = [
    # 0 cold open
    [("Early one morning", "FH", T(2, 47)), ("@", "Early one morning", "Bus travel context — United States, 1950s"),
     ("a German prisoner of war sat", "FH", T(2, 51)), ("three dollars", "FH", T(2, 35)),
     ("He had walked out", "POW", T(12, 5)), ("@", "He had walked out", "Prisoner of war context — 1944"),
     ("Nobody on the bus", "FH", T(4, 37)), ("He wore ordinary clothes", "FH", T(6, 46)), ("kept his face", "FH", T(3, 44))],
    # 1
    [("For six years", "HAM", T(2, 49)), ("@", "For six years", "Hamburg from a bomber — 1943"),
     ("Since the first day", "WO", T(10, 47)), ("@", "Since the first day", "German newsreel — 1943–44"),
     ("Windows were covered", "LON", T(0, 22)), ("@", "Windows were covered", "Blackout context — London, 1940"),
     ("Streetlamps were hooded", "LON", T(0, 52)), ("A lit window", "LON", T(4, 20))],
    # 2
    [("Then the road reached", "CHI", T(12, 26)), ("@", "Then the road reached", "Chicago at night — 1936"),
     ("a million lights", "BL", T(6, 47)), ("everywhere", "BL", T(0, 49))],
    # 3
    [("His name was", "CHI", T(12, 30)),
     ("#", "His name was", "A single lit skyline", {"type": "LedgerQuote", "file": "FILE 01 — THE MEMOIR", "head": "What he saw",
        "before": "These must be some of Chicago’s suburbs. ", "key": "A million lights pop up everywhere.", "after": "",
        "who": "Reinhold Pabel, Enemies Are Human, 1955", "source": "Pabel, Enemies Are Human (1955), ch. 9 “Operation Vapor”"}),
     ("A single lit skyline", "CHI", T(12, 40)), ("But Pabel had been watching", "TT", T(6, 29)), ("and that night", "FH", T(6, 57))],
    # 4
    [("Pabel was born", "HAM", T(1, 12)), ("@", "Pabel was born", "Hamburg — aerial view, 1943"),
     ("He studied", "CITY", T(7, 4)), ("In nineteen forty he was drafted", "GGU", T(1, 59)),
     ("He fought in the invasion", "WO", T(13, 15)), ("@", "He fought in the invasion", "German newsreel — Eastern Front"),
     ("was wounded", "WO", T(5, 14)), ("and in nineteen forty-three", "SIC", T(1, 10)), ("@", "and in nineteen forty-three", "Sicily — 1943"),
     ("and then to the Italian", "SP", T(4, 1))],
    # 5
    [("Near the Volturno", "SP", T(3, 7)), ("@", "Near the Volturno", "Italian front — 1943"),
     ("his squad stumbled", "SP", T(9, 23)), ("Pabel spoke English", "POW", T(2, 5)),
     ("He started talking", "POW", T(2, 25)), ("For a few minutes", "POW", T(3, 3)),
     ("Soon after", "SP", T(19, 12)), ("He crawled back", "SP", T(21, 0)), ("and their medics", "SP", T(28, 9))],
    # 6
    [("By the end of November", "NAP", T(1, 27)), ("@", "By the end of November", "German prisoners — Naples, 1943"),
     ("Then came a ship", "CON", T(1, 10)), ("@", "Then came a ship", "Atlantic convoy — 1942"),
     ("On the morning of January", "NN", T(2, 12)), ("went ashore", "NN", T(1, 4)),
     ("#", "On the morning of January", None, {"type": "Slug", "title": "January 2, 1944", "subtitle": "The prisoners go ashore at Norfolk, Virginia"})],
    # 7
    [("The guards put them", "TT", T(6, 11)), ("@", "The guards put them", "Train travel context — United States, 1943"),
     ("Pabel wrote that, crossing", "TT", T(6, 29.5)), ("the men pressed", "TT", T(8, 54)),
     ("The first thing", "ART", T(6, 10)), ("@", "The first thing", "American street — 1941"),
     ("abundance of automobiles", "ART", T(2, 45)), ("Then the frame houses", "ASL", T(13, 48)), ("@", "Then the frame houses", "Kentucky — 1940"),
     ("mile after mile", "ASL", T(3, 1))],
    # 8
    [("When a porter", "TT", T(9, 48)),
     ("#", "Pabel wrote that most", None, {"type": "LedgerQuote", "file": "FILE 03 — THE TRAIN FROM NORFOLK", "head": "Coffee and sandwiches",
        "before": "… the porter came through with coffee and sandwiches and politely offered them to us ", "key": "as though we were human beings", "after": " …",
        "who": "Reinhold Pabel, on the train west, January 1944", "source": "Pabel, Enemies Are Human (1955), ch. 8 “Prisonerland, U.S.A.”"}),
     ("Pabel wrote that most", "TT", T(9, 30))],
    # 9
    [("Their destination", "POW", T(14, 40)), ("@", "Their destination", "Prisoner of war camp context — 1944"),
     ("barracks, wire", "POW", T(12, 6)), ("and a library", "ASL", T(5, 3)), ("He took language", "ASL", T(6, 23)),
     ("He read American", "GGU", T(6, 21)), ("Later he was chosen", "POW", T(9, 11))],
    # 10
    [("The news from home", "HAM", T(1, 44)), ("Hamburg had been struck", "HAM", T(3, 5)), ("@", "Hamburg had been struck", "Raid on Hamburg — 1943"),
     ("that started a firestorm", "GGU", T(3, 53)), ("Pabel received a telegram", "POW", T(8, 52)), ("It was the second", "GGU", T(1, 14))],
    # 11
    [("In Germany, darkness", "LON", T(2, 21)), ("It was the law", "WO", T(10, 10)),
     ("Blackout rules", "LON", T(3, 50)), ("@", "Blackout rules", "Blackout context — London, 1940"),
     ("sirens, cellars", "LON", T(1, 21)), ("and searchlights", "LON", T(2, 36)), ("Men who had lived", "WO", T(12, 1))],
    # 12
    [("America had its own", "ART", T(2, 29)), ("@", "America had its own", "American coast — 1941"),
     ("In nineteen forty-two the coastal", "CON", T(2, 47)),
     ("In early nineteen forty-five", "ART", T(5, 23))],
    # 13
    [("But a dim-out", "BL", T(0, 49)), ("Nobody in Illinois", "CITY", T(1, 36)),
     ("And on V E Day", "GGU", T(0, 51)), ("even the dim-out", "GGU", T(5, 1)),
     ("#", "But a dim-out", None, {"type": "LedgerBars", "file": "FILE 04 — DARKNESS BY LAW", "head": "How long the lights stayed off", "max": 68,
        "bars": [{"label": "Germany — total blackout", "value": 68, "figure": "68 MONTHS", "note": "1 September 1939 – 8 May 1945"},
                 {"label": "United States — national dim-out", "value": 3.8, "figure": "< 4 MONTHS", "note": "15 January – 8 May 1945 · neon off, streetlights reduced"}],
        "source": "DHM LeMO · EBSCO Research Starters, “Dim-out of 1945”"})],
    # 14
    [("The war in Europe", "NP", T(2, 5.5)), ("but the prisoners", "POW", T(11, 7)), ("After May", "POW", T(10, 9)),
     ("In the first week", "CAN", T(15, 17)), ("@", "In the first week", "Canning crop harvest — 1950"),
     ("#", "In the first week", None, {"type": "LedgerTimeline", "file": "FILE 05 — PRISONERLAND, U.S.A.", "head": "Twenty months in custody",
        "rows": [{"date": "2 JAN 1944", "text": "Ashore at Norfolk, Virginia"}, {"date": "1944", "text": "Camp Grant, Rockford, Illinois"},
                 {"date": "1945", "text": "Camp Ellis, Illinois"}, {"date": "SEPT 1945", "text": "Branch camp, Washington, Illinois"}],
        "source": "Reinhold Pabel, Enemies Are Human (1955), ch. 8–9"}),
     ("where a cannery", "CAN", T(16, 47))],
    # 15
    [("It was not much", "POW", T(14, 40)), ("Pabel noticed", "POW", T(14, 59)),
     ("Peoria was nineteen", "AH", T(2, 23)), ("He asked to switch", "AH", T(10, 26)), ("@", "He asked to switch", "Shift change context — 1950s"),
     ("During the change", "CITY", T(13, 0)), ("he walked away", "XM", T(25, 35))],
    # 16
    [("An Associated Press", "XM", T(46, 4)),
     ("#", "An Associated Press", "By then Pabel", {"type": "LedgerClipping", "file": "FILE 06 — THE WIRE", "head": "The escape is reported",
        "kicker": "ASSOCIATED PRESS · SEPTEMBER 11, 1945", "headline": "War Prisoner Flees Camp Near Peoria", "dateline": "CAMP ELLIS, Ill., Sept. 11 (AP).—",
        "body": "A German prisoner … last night from an army branch camp at Washington, Ill., 19 miles east of Peoria, Col. C. P. Evers, Camp Ellis commander, announced today.",
        "source": "AP report as quoted in Pabel, Enemies Are Human (1955), ch. 9"}),
     ("By then Pabel", "XM", T(25, 40)),
     ("#", "By then Pabel", None, {"type": "LedgerMap", "file": "FILE 07 — OPERATION VAPOR", "head": "One night, two rides",
        "stops": ["Washington, Ill.", "Peoria", "Chicago"], "legs": ["19 miles by car", "bus, overnight"], "extra": ["Camp Ellis", "Camp Grant"],
        "source": "Route as described in Pabel, Enemies Are Human (1955)"}),],
    # 17
    [("A driver gave him", "FH", T(12, 17.6)),
     ("he waited", "FH", T(7, 9)), ("@", "he waited", "Bus terminal context — 1950s"),
     ("At two o'clock", "FH", T(7, 31)), ("It cost more", "FH", T(8, 6)),
     ("While he waited", "XM", T(2, 11)), ("He called it", "XM", T(0, 44))],
    # 18
    [("He wrote that with every mile", "FH", T(17, 17)), ("Fields and small towns", "TT", T(9, 30.5)),
     ("Then came the suburbs", "CHI", T(12, 45)), ("@", "Then came the suburbs", "Chicago at night — 1936")],
    # 19
    [("In Hamburg, a city", "HAM", T(3, 5.5)), ("Here it was simply", "CHI", T(12, 31)), ("Nobody was hiding", "BL", T(6, 20))],
    # 20
    [("Downtown, Pabel saw", "FH", T(13, 12)), ("@", "Downtown, Pabel saw", "Night street context — United States, 1950s"),
     ("and window displays", "FH", T(12, 31)),
     ("He later described", "CHI", T(1, 14.5)), ("@", "He later described", "Merchandise Mart, Chicago — 1936"),
     ("reflected in the Chicago River", "CHI", T(1, 31)), ("So this is my new home", "CHI", T(2, 37)), ("Bewildered", "CHI", T(4, 0))],
    # 21
    [("Freedom did not", "CHI", T(3, 10)), ("An escaped prisoner had no papers", "POW", T(8, 32)),
     ("Pabel took a new name", "XM", T(12, 26)),
     ("#", "Pabel took a new name", "He washed dishes", {"type": "Slug", "title": "“Phil Brick”", "subtitle": "The name Pabel lived under in Chicago, 1945–1953"}),
     ("He washed dishes", "CITY", T(11, 38)), ("@", "He washed dishes", "Kitchen context — 1939"),
     ("one of them on North Clark", "CITY", T(15, 17)), ("and saved what he could", "CITY", T(15, 44))],
    # 22
    [("Most escapes ended", "POW", T(11, 27)), ("The F B I published", "TUE", T(8, 44)), ("He tried to avoid", "XM", T(5, 7)),
     ("He saved enough", "TUE", T(2, 8)), ("@", "He saved enough", "Shop interior context — 1945"),
     ("He married", "FH", T(17, 31)), ("They had a child", "TUE", T(14, 53))],
    # 23
    [("On the morning of March", "TUE", T(1, 39)),
     ("#", "On the morning of March", None, {"type": "Slug", "title": "March 9, 1953", "subtitle": "Chicago Book Mart, North Side"}),
     ("a customer walked", "XM", T(9, 30)), ("The customer was", "XM", T(6, 35)), ("After almost eight", "XM", T(10, 58))],
    # 24
    [("The case became", "XM", T(16, 49)), ("The government wanted", "TUE", T(9, 41)),
     ("Pabel had not entered", "NN", T(0, 26)), ("The United States Army", "TT", T(4, 58)),
     ("Old friends spoke", "XM", T(37, 17)), ("Pabel left for Germany", "CON", T(6, 12)), ("and then returned", "CHI", T(6, 45))],
    # 25
    [("In his memoir", "WO", T(11, 24)), ("What changed his mind", "TT", T(9, 48.5)),
     ("and the view from a bus", "FH", T(3, 44.5))],
    # 26 comment CTA
    [("If you know", "TUE", T(15, 49)),
     ("#", "If you know", None, {"type": "Slug", "title": "Know another prisoner account?", "subtitle": "Tell us in the comments"})],
    # 27 echo close
    [("A blackout can hide", "LON", T(2, 51)), ("It can also hide", "GGU", T(2, 56.5)),
     ("Reinhold Pabel came", "HAM", T(2, 50)), ("At the edge of Chicago", "CHI", T(12, 26.5)), ("and nobody bothered", "BL", T(6, 47.5))],
]


# Archive photographs shown as contact frames: (paragraph, start anchor, end anchor | None, still, frame no, title, caption, source, extras)
LOC = "Library of Congress"
PHOTOS = [
    (0, "Nobody on the bus", None, "bus_passenger_1943.jpg", "02", "A night bus", "Greyhound bus between Cincinnati and Chicago, September 1943", f"Esther Bubley · {LOC} · LC-USW3-037808-E", {"focus": [0.45, 0.4]}),
    (6, "By the end of November", "Then came a ship", "axis_pows_tunis_1943.jpg", "05", "Prisoners of the Axis", "Axis prisoners marched out of Tunis, May 1943", f"Nick Parrino · {LOC} · LC-USW3-029246-E", {"focus": [0.5, 0.45]}),
    (9, "Their destination", "barracks, wire", "camp_grant_1942.jpg", "09", "Camp Grant, Illinois", "Army camp near Rockford, June 1942 — before the prisoners came", f"{LOC} · PAN US MILITARY - Army no. 229", {"focus": [0.35, 0.35]}),
    (15, "Peoria was nineteen", "He asked to switch", "peoria_courthouse_1938.jpg", "14", "Peoria", "Street opposite the courthouse, Peoria, Illinois, May 1938", f"Arthur Rothstein · {LOC} · LC-USF33-002794-M2", {"focus": [0.5, 0.45]}),
    (17, "At the bus depot", "trying not to look", "bus_terminal_chicago_1943.jpg", "21", "Waiting for the bus", "Passengers at a Greyhound terminal, September 1943", f"Esther Bubley · {LOC} · LC-USW3-037675-E", {"focus": [0.4, 0.6], "circle": [0.4, 0.62, 0.13, 0.2]}),
    (17, "trying not to look", "At two o'clock", "bus_tickets_chicago_1943.jpg", "22", "One ticket", "A driver collecting tickets, Greyhound terminal, September 1943", f"Esther Bubley · {LOC} · LC-USW3-037784-E", {"focus": [0.5, 0.55]}),
    (17, "At two o'clock", "While he waited", "bus_lounge_4am_1943.jpg", "23", "Small hours", "Between buses at four in the morning, Greyhound terminal, Chicago, 1943", f"Esther Bubley · {LOC} · LC-USW3-037670-E", {"focus": [0.45, 0.5], "circle": [0.43, 0.42, 0.33, 0.2]}),
    (18, "Then came the suburbs", None, "freight_terminal_night_1943.jpg", "24", "Chicago at night", "Illinois Central freight terminal and the Loop, May 1943", f"Jack Delano · {LOC} · LC-USW36-606", {"focus": [0.6, 0.4], "circle": [0.8, 0.42, 0.17, 0.2]}),
    (19, "Nobody was hiding", None, "times_square_1942.jpg", "25", "Nothing to hide", "“No blackout” at Times Square, New York, winter 1941–42", f"Alfred T. Palmer · {LOC} · LC-USE6-D-001369", {"focus": [0.5, 0.35]}),
    (20, "Bewildered", None, "union_station_night_1943.jpg", "27", "A city awake", "Chicago Union Station on a Sunday night, February 1943", f"Jack Delano · {LOC} · LC-USW3-015945-D", {"focus": [0.5, 0.55]}),
    (21, "one of them on North Clark", None, "thompsons_restaurant_chicago_1941.jpg", "29", "Behind the counter", "Thompson’s Restaurant, Chicago, July 1941", f"John Vachon · {LOC} · LC-USF33-016151-M1", {"focus": [0.5, 0.5]}),
]


def photo_items():
    import json as _j, subprocess as _sp
    crops = _j.load(open(ROOT / "tools/crops.json"))
    for k, (pi, a, b, img, no, title, cap, src, extra) in enumerate(PHOTOS):
        W, H = map(int, _sp.check_output(["identify", "-format", "%w %h", str(ROOT / f"assets/stills/{img}")]).split())
        x, y, w, h = crops[img]
        card = {"type": "PhotoCard", "image": img, "aspect": round(w * W / (h * H), 3), "crop": crops[img], "frameNo": no,
                "title": title, "caption": cap, "source": src, "side": "left" if k % 2 == 0 else "right", **extra}
        P[pi].append(("#", a, b, card))


def tag(t):
    """'Bus travel context — United States, 1950s' -> 'Stand-in · bus travel, United States, 1950s'."""
    if " context — " in t:
        what, where = t.split(" context — ", 1)
        return f"Stand-in · {what.lower()}, {where}"
    return t.replace(" — ", " · ")


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def main():
    photo_items()
    paras = json.load(open(ROOT / "audio/paragraphs.json"))
    words = json.load(open(ROOT / "audio/words.json"))  # per paragraph: [{text, start, end}] (spoken form)
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
        bounds = [float(x) for x in open(ROOT / f"build/shots/{s['file']}.txt").read().split()] if (ROOT / f"build/shots/{s['file']}.txt").exists() else []
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
    json.dump(sb, open(ROOT / "build/storyboard.json", "w"), indent=1, ensure_ascii=False)
    lens = sorted(s["end"] - s["start"] for s in out)
    print(f"{len(out)} shots, median {lens[len(lens)//2]:.1f}s, max {lens[-1]:.1f}s, {len(overlays)} overlays, {total:.1f}s")


if __name__ == "__main__":
    main()
