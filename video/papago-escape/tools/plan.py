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
    "DES": ("land_and_live_desert_1944", 1), "AZ": ("arizona_1940", 1), "SURV": ("uboat_survivors_1943", 1),
    "U858": ("u858_surrender_1945", 1), "U505": ("u505_capture_1944", 1), "XMAS": ("christmas_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

BA = "R. H. Bailey, “The Not-So-Great Escape”, World War II (Nov. 2007), after J. H. Moore, The Faustball Tunnel (1978)"
DES_TAG = "Stand-in · from Land and Live in the Desert (U.S. Army Air Forces, 1944)"
AZ_TAG = "Arizona, 1940 · from Arizona: Its Mineral Resources and Scenic Wonders"
SURV_TAG = "German U-boat survivors taken prisoner by the U.S. Navy, 1943"
U858_TAG = "German U-boat crew surrendering to the U.S. Navy, 1945"
XMAS_TAG = "Christmas, 1945 · Universal Newsreel"
# (anchor, film, source time). Context tags: ("@", anchor, text). Cards: ("#", anchor, until_anchor|None, {...})
P = [
    # 0 cold open
    [("On the night of", "DES", T(24, 7.5)), ("@", "On the night of", DES_TAG),
     ("#", "On the night of", None, {"type": "Slug", "title": "December 23, 1944", "subtitle": "Camp Papago Park, Phoenix, Arizona"}),
     ("crawled out of a camp", "DES", T(25, 37.5)), ("Three of them took a boat", "DES", T(31, 2.5)), ("They meant to paddle", "AZ", T(25, 23.3)),
     ("@", "They meant to paddle", AZ_TAG)],
    # 1 the route
    [("The boat had been built", "AZ", T(25, 36.7)), ("@", "The boat had been built", "Canal gates, Arizona, 1940"), ("The route came from a map", "AZ", T(2, 0.8)),
     ("#", "The route came from a map", None, {"type": "LedgerMap", "file": "FILE 01 — THE PLAN", "head": "Water all the way to the sea",
        "stops": ["Papago Park", "Gila Bend", "Yuma", "Gulf of California"], "legs": ["Canal, Salt, Gila", "Gila River", "Colorado River"],
        "source": f"Route as planned by the escapees, in {BA}"})],
    # 2
    [("On the ground", "DES", T(1, 37.5)), ("This is the documented story", "SURV", T(1, 46.3)), ("@", "This is the documented story", SURV_TAG),
     ("and of the desert", "DES", T(1, 17.5))],
    # 3 the camp
    [("Camp Papago Park sat", "AZ", T(38, 38.1)), ("most of them sailors", "SURV", T(0, 43.8)), ("At its peak", "U858", T(4, 13.3)),
     ("#", "At its peak", None, {"type": "LedgerBars", "file": "FILE 02 — CAMP PAPAGO PARK", "head": "Who was inside the wire", "max": 3100,
        "bars": [{"label": "Prisoners", "value": 3100, "figure": "~3,100", "note": "German, mostly navy"},
                 {"label": "Americans", "value": 371, "figure": "371", "note": "guards and officers"}],
        "source": "Peak strength, 1944 · Wikipedia, “Great Papago Escape” (after K. W. Lloyd, The Great Desert Escape, 2019)"})],
    # 4 Wattenberg
    [("Many of them were", "U858", T(6, 43.8)), ("@", "Many of them were", U858_TAG), ("Their senior officer", "SURV", T(0, 43.8)),
     ("@", "Their senior officer", SURV_TAG), ("At forty-one", "U505", T(2, 21.0)),
     ("@", "At forty-one", "A U-boat at sea, 1944 · U.S. Navy film"), ("until three British destroyers", "U858", T(9, 28.1)), ("The camp's commander would call", "U858", T(8, 33.4))],
    # 5 Drechsler
    [("The camp had already seen", "AZ", T(37, 43.1)), ("On March twelfth", "SURV", T(3, 26.4)),
     ("#", "On March twelfth", None, {"type": "Slug", "title": "March 12, 1944", "subtitle": "Werner Drechsler arrives at Papago Park"}),
     ("He had been informing", "SURV", T(3, 51.4)), ("Within hours", "DES", T(30, 12.5)), ("@", "Within hours", DES_TAG), ("Seven prisoners were later hanged", "DES", T(30, 46.0))],
    # 6
    [("For everyone else", "AZ", T(27, 10.0)), ("@", "For everyone else", "Farm work near Phoenix, 1940"), ("The prisoners called the camp", "AZ", T(37, 1.9)),
     ("But the officers had time", "SURV", T(1, 58.8)), ("One of them", "DES", T(1, 42.5)),
     ("#", "One of them", None, {"type": "LedgerQuote", "file": "FILE 03 — THE FENCE", "head": "Three ways past it",
        "before": "Go through it, fly over it, ", "key": "or dig under it", "after": ".", "who": "Lt. Wolfgang Clarus, U-boat officer, Papago Park", "source": f"Quoted in {BA}"})],
    # 7 the blind spot
    [("The camp's provost marshal", "AZ", T(17, 59.0)), ("@", "The camp's provost marshal", AZ_TAG), ("Part of the officers", "DES", T(1, 42.5)),
     ("#", "I knew they would", "In September", {"type": "LedgerQuote", "file": "FILE 04 — THE BLIND SPOT", "head": "What the provost marshal knew",
        "before": "I knew they would discover ", "key": "that blind spot", "after": ".", "who": "Capt. Cecil Parshall, provost marshal, Camp Papago Park", "source": f"Quoted in {BA}"}),
     ("In September", "SURV", T(5, 18.9))],
    # 8 the entrance
    [("The entrance was in", "DES", T(1, 47.5)), ("They loosened a board", "AZ", T(4, 52.5)), ("The Americans even lent them", "AZ", T(26, 3.3)),
     ("@", "The Americans even lent them", "Irrigated field, Arizona, 1940")],
    # 9 digging
    [("They dug at night", "AZ", T(8, 16.7)), ("@", "They dug at night", "Stand-in · Arizona mine tunnel, 1940"), ("One man dug", "DES", T(1, 52.5)),
     ("#", "The tunnel was less than", None, {"type": "LedgerTimeline", "file": "FILE 05 — THE DIG", "head": "How the tunnel was made",
        "rows": [{"date": "CREWS", "text": "Three men, 90-minute night shifts"}, {"date": "WIDTH", "text": "Less than three feet across"},
                 {"date": "DEPTH", "text": "Down to 14 feet, under a ditch and a road"}, {"date": "PACE", "text": "Up to three feet a night"}],
        "source": BA}),
     ("On a good night", "DES", T(31, 10.8))],
    # 10 the dirt
    [("The hardest problem was the dirt", "DES", T(1, 57.5)), ("They carried it out", "DES", T(25, 7.5)), ("@", "They carried it out", DES_TAG),
     ("Then one of the captains", "SURV", T(2, 36.3)), ("@", "Then one of the captains", SURV_TAG)],
    # 11 faustball
    [("The game was faustball", "DES", T(26, 37.5)),
     ("#", "The guards were delighted", "Every day", {"type": "LedgerQuote", "file": "FILE 06 — THE FAUSTBALL COURT", "head": "A sports field, please",
        "before": "Their guards were delighted; it was ", "key": "the first cooperative gesture", "after": " these particular die-hard Nazis had made.",
        "who": "American Heritage, June/July 1978, on Moore's account", "source": "American Heritage 29, no. 4 (1978)"}),
     ("Every day", "DES", T(1, 52.5)), ("In late November", "AZ", T(31, 49.2))],
    # 12 finished
    [("On December twentieth", "AZ", T(8, 16.7)),
     ("#", "On December twentieth", None, {"type": "Slug", "title": "178 feet", "subtitle": "Finished December 20, 1944"}),
     ("It ran one hundred", "DES", T(1, 32.5)), ("The exit was hidden", "DES", T(26, 37.5))],
    # 13 supplies
    [("They had been saving food", "DES", T(2, 37.5)), ("@", "They had been saving food", "Stand-in · survival rations · Land and Live in the Desert (1944)"),
     ("Photographs were turned into", "DES", T(2, 42.5))],
    # 14 the boatmen
    [("Three officers had", "U505", T(1, 48.8)), ("@", "Three officers had", "U.S. Navy boarding party, 1944"),
     ("#", "Three officers had", "They became known", {"type": "LedgerTimeline", "file": "FILE 07 — THE THREE MAD BOATMEN", "head": "A boat that folds",
        "rows": [{"date": "CAPTAIN", "text": "Wilhelm Günther"}, {"date": "LIEUTENANT", "text": "Wolfgang Clarus"}, {"date": "LIEUTENANT", "text": "Friedrich Utzolino"},
                 {"date": "THE BOAT", "text": "Scrap wood, canvas, tar · no piece over 18 inches"}],
        "source": BA}),
     ("They became known", "U858", T(5, 8.0))],
    # 15 the night
    [("The date was Saturday", "XMAS", T(0, 4.8)), ("@", "The date was Saturday", XMAS_TAG), ("In the next compound", "DES", T(7, 54.3)),
     ("@", "In the next compound", DES_TAG), ("At nine", "DES", T(24, 12.5)),
     ("#", "By two thirty in the morning", None, {"type": "LedgerTimeline", "file": "FILE 08 — DECEMBER 23–24, 1944", "head": "Twenty-five men out",
        "rows": [{"date": "9:00 P.M.", "text": "First team goes down the shaft"}, {"date": "2:30 A.M.", "text": "All 25 out: 12 officers, 13 enlisted men"},
                 {"date": "AHEAD", "text": "Mexico, about 130 miles south"}],
        "source": BA}),
     ("They waded through", "DES", T(24, 22.5)), ("Most of them headed south", "DES", T(25, 47.5))],
    # 16 Christmas Eve
    [("They spent Christmas Eve", "DES", T(30, 29.2)), ("One group rested", "XMAS", T(0, 14.4)), ("while a Mexican family", "XMAS", T(0, 52.8)),
     ("@", "while a Mexican family", XMAS_TAG), ("In another group", "DES", T(30, 54.2))],
    # 17 discovery
    [("Back at the camp", "SURV", T(1, 46.3)), ("The German officers stalled", "SURV", T(1, 33.8)), ("By about seven", "AZ", T(38, 24.4)),
     ("@", "By about seven", "Phoenix, 1940"),
     ("#", "Hundreds of soldiers", None, {"type": "LedgerQuote", "file": "FILE 09 — THE MANHUNT", "head": "Soldiers, FBI agents, Papago trackers · $25 a man",
        "before": "", "key": "the greatest manhunt in Arizona history", "after": "", "who": "Phoenix Gazette, December 1944", "source": f"Quoted in {BA}"})],
    # 18 the desert
    [("The desert did most of the work", "DES", T(31, 44.2)), ("@", "The desert did most of the work", DES_TAG), ("The nights were cold", "DES", T(32, 17.5)),
     ("A twenty-two-year-old", "SURV", T(6, 59.0)), ("Two more surrendered", "AZ", T(39, 5.6)), ("@", "Two more surrendered", AZ_TAG), ("One stepped on a cactus", "AZ", T(31, 40.8))],
    # 19 Phoenix
    [("The people of Phoenix", "AZ", T(37, 1.9)),
     ("#", "One resident complained", None, {"type": "LedgerQuote", "file": "FILE 10 — WHAT ANGERED PHOENIX", "head": "Rationed goods in the prisoners' packs",
        "before": "Citizens ", "key": "cannot get a single slice of bacon", "after": " for weeks on end.", "who": "A Phoenix resident, 1945", "source": f"Quoted in {BA}"})],
    # 20 the hunt
    [("The best of them came close", "DES", T(32, 50.8)), ("@", "The best of them came close", DES_TAG),
     ("#", "The best of them came close", "Three years earlier", {"type": "LedgerTimeline", "file": "FILE 11 — RECAPTURED", "head": "How far they got",
        "rows": [{"date": "DEC. 24–26", "text": "Many give up: cold, rain, hunger"}, {"date": "JAN. 1", "text": "Two found asleep < 30 miles from the border"},
                 {"date": "JAN. 6", "text": "Quaet-Faslem, Guggenberger: within 10 miles"}, {"date": "JAN. 8", "text": "The boatmen, near Gila Bend"},
                 {"date": "JAN. 28", "text": "Wattenberg, in Phoenix"}],
        "source": f"{BA}; uboat.net"}),
     ("Three years earlier", "U858", T(9, 28.1))],
    # 21 the river
    [("The boatmen never got", "AZ", T(25, 23.3)), ("@", "The boatmen never got", "A dam on an Arizona river, 1940"), ("The rain shrank", "DES", T(33, 7.5)),
     ("They left the boat behind", "DES", T(32, 59.2)), ("@", "They left the boat behind", DES_TAG)],
    # 22 Gila Bend
    [("On January eighth", "AZ", T(31, 57.5)), ("Cowboys saw it", "AZ", T(38, 10.6)), ("@", "Cowboys saw it", "Riders near Phoenix, 1940"),
     ("#", "Clarus put it simply", None, {"type": "LedgerQuote", "file": "FILE 12 — THE GILA", "head": "The boatmen's verdict",
        "before": "We should have known that ", "key": "the Gila wasn't much of a river", "after": ".", "who": "Lt. Wolfgang Clarus", "source": f"Quoted in {BA}"})],
    # 23 the cave
    [("Wattenberg never went south", "AZ", T(37, 43.1)), ("he hid in a cave", "AZ", T(4, 52.5)), ("@", "he hid in a cave", "Stand-in · Arizona, 1940"),
     ("Every few days", "AZ", T(26, 16.7)), ("@", "Every few days", "Farm work near Phoenix, 1940"), ("would walk back into the camp", "SURV", T(1, 58.8))],
    # 24
    [("The trick worked", "DES", T(30, 37.5)), ("@", "The trick worked", DES_TAG), ("Then, late in January", "U858", T(8, 33.4)),
     ("The next night", "DES", T(31, 19.2)), ("three soldiers were waiting", "DES", T(25, 42.5))],
    # 25 Phoenix
    [("On January twenty-seventh", "AZ", T(38, 24.4)), ("@", "On January twenty-seventh", "Phoenix, 1940"), ("walked into Phoenix", "AZ", T(37, 15.6)),
     ("slept in a chair", "AZ", T(38, 51.9)), ("Then he asked a street cleaner", "AZ", T(39, 5.6)), ("By nine the next morning", "SURV", T(3, 1.4)),
     ("#", "By nine the next morning", None, {"type": "Slug", "title": "January 28, 1945", "subtitle": "The last escapee, back at Papago Park"})],
    # 26 punishment
    [("Some of the escapees", "SURV", T(3, 26.4)),
     ("#", "Instead, each man got", None, {"type": "Slug", "title": "Bread and water", "subtitle": "One day for every day gone"}),
     ("No American officer", "AZ", T(17, 59.0)), ("The F B I looked into", "AZ", T(37, 29.4))],
    # 27
    [("Clarus later said", "DES", T(32, 17.5)), ("In May", "U858", T(4, 13.3)),
     ("#", "In May", None, {"type": "Slug", "title": "May 1945", "subtitle": "Germany surrenders"}),
     ("After the war", "U858", T(9, 28.1))],
    # 28 reunion
    [("Wattenberg came back", "AZ", T(39, 13.0)), ("At one of them", "AZ", T(37, 43.1)), ("He died in Hamburg", "AZ", T(31, 49.2)), ("@", "Wattenberg came back", AZ_TAG),
     ("#", "At one of them", None, {"type": "LedgerQuote", "file": "FILE 13 — 1985", "head": "At a reunion in Arizona",
        "before": "Strange we have to ", "key": "kill each other before we become friends", "after": ".", "who": "Jürgen Wattenberg, 1985",
        "source": "Quoted in D. Towne, “Nazis in Papago”, PHOENIX magazine (Nov. 2023)"})],
    # 29 comment request
    [("If someone in your family", "AZ", T(38, 38.1)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Lived near Phoenix in the war?", "subtitle": "Tell us in the comments"})],
    # 30 echo
    [("A plaque on the bank", "AZ", T(25, 36.7)), ("Twenty-five men dug", "DES", T(1, 52.5)), ("They planned for the guards", "DES", T(1, 37.5)),
     ("What they could not see", "AZ", T(25, 23.3))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (3, "Camp Papago Park sat", None, "papago_buttes_2013.jpg", "03", "Papago Park", "The red sandstone buttes of Papago Park, where the camp stood, in 2013", f"Chris English · CC BY-SA 3.0 · {WC}", {"focus": [0.5, 0.4]}),
    (3, "It opened in", None, "italian_pows_arizona_canal_1943.jpg", "04", "The first prisoners", "Italian prisoners of war working on the Arizona Canal near Phoenix, December 1943", f"HAER ARIZ,7-PHEN.V,1-19 · public domain · {WC}", {"focus": [0.6, 0.5]}),
    (4, "He had been navigation officer", None, "graf_spee_scuttled_1939.jpg", "05", "Graf Spee", "The Admiral Graf Spee, scuttled off Montevideo, December 1939", f"National Archives 197095 · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (7, "Part of the officers", None, "dade_city_pow_camp_1944.jpg", "07", "A camp from the air", "A German prisoner-of-war camp seen from the air: Dade City, Florida, December 1944 (not Papago Park)", f"National Archives 23936579 · public domain · {WC}", {"focus": [0.65, 0.4]}),
    (8, "The entrance was in", None, "tunnel_entrance_1944.jpg", "08", "The entrance", "The entrance to the escape tunnel at Camp Papago Park, 1944", f"U.S. Army · public domain · {WC}", {"focus": [0.5, 0.5]}),
    (12, "to the bank of the Crosscut", None, "crosscut_canal_haer.jpg", "12", "The Crosscut Canal", "The Crosscut Canal, Phoenix, where the tunnel came up", f"HAER ARIZ,7-PHEN,17-17 · public domain · {WC}", {"focus": [0.5, 0.55]}),
    (20, "Three years earlier", None, "ark_royal_sinking_1941.jpg", "20", "HMS Ark Royal", "HMS Ark Royal, November 1941, the month Guggenberger's U-81 sank her", f"Royal Navy official photographer · IWM A6318 · public domain · {WC}", {"focus": [0.5, 0.6]}),
    (21, "When they reached the Gila", None, "gila_river_komatke.jpg", "21", "The Gila River", "The Gila River just south of Phoenix, seen from the air", f"Dicklyon · CC BY-SA 4.0 · {WC}", {"focus": [0.5, 0.5]}),
    (25, "He spent most of it", None, "phoenix_hotel_1940.jpg", "25", "Downtown Phoenix", "A hotel in downtown Phoenix, May 1940", f"Russell Lee, FSA · public domain · {WC}", {"focus": [0.5, 0.4]}),
    (30, "A plaque on the bank", None, "tunnel_marker.jpg", "30", "Where it came up", "The marker by the Crosscut Canal at the tunnel's exit", f"Marine 69-71 · CC BY-SA 4.0 · {WC}", {"focus": [0.5, 0.45]}),
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
