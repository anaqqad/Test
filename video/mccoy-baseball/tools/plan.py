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
    "SNOW": ("snow_1945", 1), "TRN": ("passenger_train_1940", 1), "TT": ("troop_train_1943", 1),
    "CHD": ("challenge_democracy_1944", 1), "POW": ("pow_control_1944", 1), "SUR": ("surrender_1945", 1),
    "MID": ("midget_sub_1945", 1), "CITY": ("the_city_1939", 1), "AH": ("american_harvest_1955", 1),
    "ASL": ("and_so_they_live_1940", 1), "XM": ("x_marks_the_spot_1942", 1), "TUE": ("tuesday_in_november_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

# (anchor, film, source time). Context tags: ("@", anchor, text). Cards: ("#", anchor, until_anchor|None, {...})
P = [
    # 0 cold open
    [("On the morning after", "D7", T(22, 10.6)), ("@", "On the morning after", "Oahu, Hawaii · from December 7th (1943)"),
     ("found an American rifle", "IWO", T(6, 43)), ("His name was", "KYE", T(34, 40.5)),
     ("#", "His name was", None, {"type": "Slug", "title": "Ensign Kazuo Sakamaki", "subtitle": "Imperial Japanese Navy · midget submarine HA-19"}),
     ("The day before", "D7", T(8, 6.8)), ("The submarine had failed", "D7", T(16, 42.5)), ("@", "The submarine had failed", "Sakamaki's submarine aground off Oahu, December 1941"),
     ("He had jumped into the sea", "D7", T(16, 47.5))],
    # 1
    [("He asked his captors", "NOUB", T(3, 26.6)), ("They refused", "NOU", T(1, 48.1))],
    # 2
    [("Ten young men", "D7", T(12, 26.4)), ("Japan would soon celebrate", "KYE", T(13, 44.4)), ("@", "Japan would soon celebrate", "Japan · from Know Your Enemy: Japan (1945)"),
     ("There was no place", "KYE", T(18, 58.4))],
    # 3
    [("Sakamaki had been taught", "KYE", T(17, 39.9)),
     ("#", "Sakamaki had been taught", None, {"type": "LedgerQuote", "file": "FILE 01 — THE FIELD CODE", "head": "What every soldier was told",
        "before": "Rather than live and bear the shame of imprisonment by the enemy, ", "key": "he should die", "after": " and avoid leaving a dishonorable name!",
        "who": "Japanese Military Field Code, 1941", "source": "Quoted in A. Krammer, Pacific Historical Review 52 (1983)"}),
     ("A soldier was expected", "KYE", T(4, 34.8))],
    # 4
    [("The rule worked", "KYE", T(55, 36.7)),
     ("#", "In the Burma campaign", None, {"type": "LedgerBars", "file": "FILE 02 — THE RULE WORKED", "head": "Burma campaign: dead vs. captured", "max": 17466,
        "bars": [{"label": "Japanese dead", "value": 17466, "figure": "17,466", "note": "Allied count, Burma campaign"},
                 {"label": "Japanese captured", "value": 142, "figure": "142", "note": "fewer than 1 in 120"}],
        "source": "A. Krammer, “Japanese Prisoners of War in America”, Pacific Historical Review 52 (1983)"}),
     ("Across the whole war", "SAI", T(6, 46.7)), ("So what do you do", "NOUB", T(8, 31.0)), ("In Wisconsin", "SNOW", T(4, 59.7)),
     ("@", "In Wisconsin", "Stand-in · northern winter, 1940s")],
    # 5
    [("Sakamaki spent his first weeks", "NOU", T(3, 44.5)), ("@", "Sakamaki spent his first weeks", "Stand-in · prisoner compound, Pacific, 1943"),
     ("He later called it", "NOU", T(4, 1.1)), ("He thought constantly", "NOUB", T(3, 30.0))],
    # 6
    [("On February twenty-ninth", "TT", T(6, 11)), ("@", "On February twenty-ninth", "Stand-in · wartime train, 1943"),
     ("held briefly at Angel Island", "TRN", T(5, 3.2)), ("and put on a train", "TT", T(8, 54)), ("Nobody told him", "TT", T(9, 48)),
     ("When he finally stepped down", "SNOW", T(1, 33.0))],
    # 7
    [("He was at Camp McCoy", "SNOW", T(5, 20.4)), ("For the next six months", "POW", T(14, 40)), ("@", "For the next six months", "Prisoner of war camp, 1944"),
     ("In July nineteen forty-two", "NOUB", T(6, 42.3)), ("By the summer", "SAI", T(6, 50.0))],
    # 8
    [("Japanese soldiers had been told", "KYE", T(5, 53.3)), ("What they found at McCoy", "NOU", T(6, 14.1)),
     ("Steamed rice was served", "NOU", T(6, 30.7)), ("The prisoners were allowed to plant", "CHD", T(4, 5.2)), ("@", "The prisoners were allowed to plant", "Stand-in · camp garden plots, 1944")],
    # 9
    [("None of this made", "NOUB", T(9, 14.5)),
     ("#", "Sakamaki later wrote", None, {"type": "LedgerQuote", "file": "FILE 04 — I ATTACKED PEARL HARBOR", "head": "In his own words",
        "before": "We had no knives to cut our throats. We had no ropes to hang ourselves with… ", "key": "We wanted to die and yet we could not die.", "after": "",
        "who": "Kazuo Sakamaki, I Attacked Pearl Harbor, 1949", "source": "Sakamaki (1949), pp. 81–82, quoted in Krammer (1983)"})],
    # 10
    [("The Americans discovered", "POW", T(8, 32)), ("Prisoners were allowed to write", "TUE", T(8, 44)), ("@", "Prisoners were allowed to write", "Stand-in · wartime mail, 1945"),
     ("A letter would tell", "NOUB", T(3, 30.0)), ("So when a Japanese prisoner", "POW", T(11, 27)), ("It usually ended", "NOU", T(1, 31.5))],
    # 11
    [("The camp commander", "POW", T(2, 5)),
     ("#", "The camp commander", None, {"type": "Slug", "title": "Lt. Col. Horace I. Rogers", "subtitle": "Commandant, Camp McCoy, from 1943"}),
     ("At first, many", "NOUB", T(7, 4.0)), ("Then boredom won", "NOUB", T(7, 25.8))],
    # 12
    [("They built a stage", "KYE", T(21, 35.4)), ("@", "They built a stage", "Japanese theatre · from Know Your Enemy: Japan"),
     ("Up to three productions", "KYE", T(22, 53.9)), ("Rogers had one condition", "POW", T(3, 3)), ("Without tools for wood", "CHD", T(9, 36.2)),
     ("@", "Without tools for wood", "Stand-in · camp crafts, 1944")],
    # 13
    [("Then the YMCA donated", "CHD", T(9, 16.2)), ("@", "Then the YMCA donated", "Stand-in · baseball in a Japanese American camp, 1944"),
     ("Baseball became", "CHD", T(9, 21.2)), ("Teams formed", "CHD", T(9, 33.8)), ("and met in a camp championship", "CHD", T(9, 18.8)),
     ("When inspectors toured", "CHD", T(9, 31.2))],
    # 14
    [("On Saturdays", "POW", T(10, 9)), ("The War Department had expected", "POW", T(12, 6)), ("On the way to the movies", "NOUB", T(9, 36.2))],
    # 15
    [("McCoy was not a holiday camp", "POW", T(14, 59)), ("The Japanese prisoners complained", "NOUB", T(10, 19.7)),
     ("They did not want to wash", "ASL", T(5, 3)), ("On one morning in May", "POW", T(11, 7)),
     ("#", "On one morning in May", None, {"type": "Slug", "title": "May 31, 1944", "subtitle": "Sit-down strike in the Japanese compound"}),
     ("Rogers sent in", "POW", T(12, 5)), ("The men went to work", "AH", T(10, 26))],
    # 16
    [("And some still ran", "POW", T(14, 40)),
     ("#", "Across the whole country", None, {"type": "LedgerTimeline", "file": "FILE 06 — THE ESCAPES", "head": "Fourteen tries, no way home",
        "rows": [{"date": "22 MAY 1945", "text": "Three dig under the fence"}, {"date": "JULY 1945", "text": "A knock at a farmhouse door"},
                 {"date": "29 AUG 1945", "text": "Yuzo Ohashi heads for “Mexico”"}, {"date": "TOTAL", "text": "14 attempts · 0 successful"}],
        "source": "Krammer (1983); Fournier, Fort McCoy (2003); Monroe County Democrat; Sparta Herald"}),
     ("In May nineteen forty-five", "XM", T(25, 35)), ("A farmer spotted", "TRN", T(5, 25.7)), ("@", "A farmer spotted", "Stand-in · river country, 1940"),
     ("The other two were caught", "AH", T(2, 23))],
    # 17
    [("In July, another escapee", "ASL", T(13, 48)), ("@", "In July, another escapee", "Stand-in · farm country, 1940"),
     ("The farm wife gave him bread", "XM", T(2, 11)), ("When the highway patrol", "XM", T(9, 30))],
    # 18
    [("The last Japanese prisoner", "IWO", T(2, 35.1)), ("@", "The last Japanese prisoner", "Japanese prisoner, Iwo Jima, March 1945"),
     ("He believed Mexico", "SNOW", T(9, 49.1)), ("He was caught", "SUR", T(0, 46.5)),
     ("#", "He was caught", None, {"type": "Slug", "title": "September 2, 1945", "subtitle": "Japan surrenders · Ohashi caught at Cashton, Wisconsin"}),
     ("He told his guards", "IWO", T(2, 40.0)), ("It was escape", "NOUB", T(3, 26.6))],
    # 19
    [("That was exactly", "SUR", T(1, 42.2)), ("A Japanese language newspaper", "TUE", T(8, 44))],
    # 20
    [("It never happened", "NOUB", T(8, 52.8)), ("Before the prisoners were sent home", "CHD", T(10, 6.5)), ("@", "Before the prisoners were sent home", "Stand-in · wartime classroom, 1944"),
     ("There were no suicides", "TRN", T(5, 25.7))],
    # 21
    [("Kazuo Sakamaki went home", "SUR", T(2, 38.0)), ("He became a lifelong pacifist", "KYE", T(32, 3.5)), ("For decades", "D7", T(1, 37.4))],
    # 22
    [("In nineteen sixty-six", "SNOW", T(4, 39.0)),
     ("#", "For him, he wrote", None, {"type": "LedgerQuote", "file": "FILE 07 — A LETTER, 1966", "head": "Twenty-one years later",
        "before": "I have been longing to visit [Camp McCoy] again… for me this place signifies ", "key": "a second starting point in my life.", "after": "",
        "who": "Yasuichiro Hayashi, former prisoner, 21 September 1966", "source": "Letter to Fort McCoy, quoted in B. J. Scott, University of Wisconsin (2010)"})],
    # 23
    [("If you know", "SNOW", T(5, 41.0)),
     ("#", "put it in the comments", None, {"type": "Slug", "title": "Know another prisoner account?", "subtitle": "Tell us in the comments"})],
    # 24
    [("The field code", "KYE", T(17, 39.9)), ("In the middle of Wisconsin", "SNOW", T(5, 20.4)), ("Someone handed them", "CHD", T(9, 21.2))],
]

LOC = "Library of Congress"
PHOTOS = [
    (2, "Ten young men", None, "midget_sub_raised_1943.jpg", "03", "A midget submarine", "A Japanese midget submarine raised by a U.S. Navy tug, 1943", f"{LOC} · LC-USZ62-106360", {"focus": [0.5, 0.5]}),
    (4, "Across the whole war", None, "saipan_cave_surrender_1944.jpg", "05", "Coming out", "A Japanese soldier surrenders from a cave on Saipan, July 1944", f"{LOC} · LC-USZ6-1891", {"focus": [0.55, 0.5], "circle": [0.56, 0.48, 0.12, 0.2]}),
    (5, "He thought constantly", None, "wounded_prisoner_newcaledonia_1942.jpg", "06", "Alive, against orders", "A wounded Japanese prisoner in an American clearing station, New Caledonia, 1942", f"U.S. Army · {LOC} · LC-USW33-000299-ZC", {"focus": [0.6, 0.45]}),
    (7, "He was at Camp McCoy", None, "mccoy_north_gate_habs.jpg", "08", "Camp McCoy", "North entrance gate, Camp McCoy near Sparta, Wisconsin", f"Fort McCoy photograph · HABS WI-229 · {LOC}", {"focus": [0.5, 0.55]}),
    (9, "None of this made", "Sakamaki later wrote", "brodie_prisoner_sketch_1943.jpg", "10", "“Wanted to die”", "Three soldiers carry a Japanese prisoner “who wouldn't walk and wanted to die.” Guadalcanal, 1943", f"Howard Brodie, Yank magazine · {LOC} · LC-DIG-ppmsca-22726", {"focus": [0.4, 0.35], "crop": [0.2, 0.05, 0.6, 0.6]}),
    (11, "At first, many", None, "mccoy_pow_barracks_c.jpg", "13", "Compound under snow", "Prisoner of War Area 'A', barracks and fences, Camp McCoy", f"Fort McCoy photograph B-36 · HABS WI-229 · {LOC}", {"focus": [0.5, 0.5]}),
    (15, "McCoy was not a holiday camp", None, "mccoy_pow_tower5.jpg", "16", "Guard Tower No. 5", "Prisoner of War Area 'A', Camp McCoy, Wisconsin", f"Fort McCoy photograph B-33 · HABS WI-229 · {LOC}", {"focus": [0.5, 0.4], "circle": [0.42, 0.35, 0.12, 0.2]}),
    (20, "It never happened", None, "prisoners_guarded_1944.jpg", "21", "Going home", "Japanese prisoners of war under American guard, probably the Philippines", f"{LOC} · LC-USW33-058838", {"focus": [0.5, 0.5]}),
    (21, "He finally spoke", None, "ha19_submarine_highsmith.jpg", "22", "HA-19 today", "Sakamaki's submarine, National Museum of the Pacific War, Fredericksburg, Texas", f"Carol M. Highsmith, 2014 · {LOC}", {"focus": [0.35, 0.6]}),
]


def photo_items():
    import json as _j, subprocess as _sp
    crops = _j.load(open(ROOT / "tools/crops.json"))
    for k, (pi, a, b, img, no, title, cap, src, extra) in enumerate(PHOTOS):
        W, H = map(int, _sp.check_output(["identify", "-format", "%w %h", str(ROOT / f"assets/stills/{img}")]).split())
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
