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
    "TT": ("troop_train_1943", 1), "UTA": ("this_land_utah_1950", 1), "RST": ("restaurant_operator_1946", 1),
    "COM": ("communications_our_town_1947", 1), "SHO": ("shoshone_irrigation_1938", 1), "FOO": ("food_for_america_1941", 1),
    "MEM": ("memorial_day_1945", 1), "HOS": ("general_hospital_1945", 1), "TUN": ("tunisian_campaign_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

TEL = "Salt Lake Telegram, July 9, 1945"
OGD = "Ogden Standard-Examiner, July 10, 1945"
SUN = "Salina Sun, July 13, 1945"
TRIB = "Salt Lake Tribune, July 10, 1945"
HN = "HistoryNet, “The Deadliest Nazi POW Massacre on U.S. Soil”"
WP = "Wikipedia, “1945 Utah prisoner of war massacre”"
DN = "Deseret News, July 4, 1995"
FL = "Christian Flanders, Intermountain Histories"
TIME = "Time, July 23, 1945"
UTA_TAG = "Utah · from This Land of Ours: Utah (1950)"
RST_TAG = "Stand-in · a restaurant, 1946 · from The Restaurant Operator"
COM_TAG = "Stand-in · from Communications and Our Town (1947)"
TUNS_TAG = "Stand-in · German prisoners in Tunisia, May 1943 · U.S. Army film"
NIGHT_TAG = "Stand-in · sleeping berths at night · from Troop Train (OWI, 1943)"
SHO_TAG = "Stand-in · beet and farm country, Wyoming · Interior Dept. film, 1938"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
HOS_TAG = "Stand-in · an Army hospital · from The General Hospital (1945)"
MEM_TAG = "Stand-in · a national cemetery, Memorial Day 1945"
FOO_TAG = "Stand-in · from Food for America (1941)"
P = [
    # 0 the waitress
    [("On", "UTA", T(0, 58.2)), ("@", "On a Saturday night", UTA_TAG),
     ("#", "On a Saturday night", None, {"type": "Slug", "title": "July 7, 1945", "subtitle": "Salina, Utah · a Saturday night"}),
     ("an American soldier sat", "RST", T(5, 1.9)), ("@", "an American soldier sat", RST_TAG), ("Before he left", "RST", T(0, 38.0))],
    # 1 the camp
    [("He walked a few blocks", "COM", T(6, 21.6)), ("@", "He walked a few blocks", COM_TAG), ("to a camp behind barbed wire", "TUN", T(16, 12.8)), ("@", "to a camp behind barbed wire", TUNS_TAG),
     ("The war in Europe", "TUN", T(13, 1.7))],
    # 2 the tower
    [("At midnight", "TT", T(9, 5.8)), ("@", "At midnight", NIGHT_TAG), ("He climbed", "TT", T(9, 22.2)), ("It was not loaded", "TT", T(9, 19.8))],
    # 3 documented story
    [("This is the documented story", "UTA", T(3, 33.3)), ("of the fifteen seconds", "TT", T(9, 24.5)), ("and of the American who", "TT", T(9, 12.8)), ("@", "and of the American who", NIGHT_TAG)],
    # 4 Salina
    [("was a farm town", "UTA", T(4, 6.5)), ("@", "was a farm town", UTA_TAG), ("With so many men", "SHO", T(1, 26.2)), ("@", "With so many men", SHO_TAG), ("The farmers needed hands", "SHO", T(3, 21.1))],
    # 5 the Army had the hands
    [("The Army had the hands", "TUN", T(12, 58.3)), ("@", "The Army had the hands", TUNS_TAG), ("Utah alone held", "UTA", T(0, 58.2)), ("@", "Utah alone held", UTA_TAG)],
    # 6 the camp
    [("On the eighth of June", "UTA", T(3, 33.3)),
     ("#", "a new branch camp", "It was strange", {"type": "LedgerTimeline", "file": "FILE 01 — THE CAMP", "head": "Branch camp, Salina, Utah",
        "rows": [{"date": "JUNE 8, 1945", "text": "Opens, a month after Germany surrenders"},
                 {"date": "ABOUT 250", "text": "German prisoners, in 43 tents"},
                 {"date": "3", "text": "Guard towers, one machine gun in each"},
                 {"date": "4 BLOCKS", "text": "East of Salina's main street"}],
        "source": TEL + "; " + SUN}),
     ("It was strange", "COM", T(6, 21.6))],
    # 7 the fields
    [("The prisoners were sent out", "UTA", T(4, 7.5)), ("@", "The prisoners were sent out", UTA_TAG), ("A prisoner was paid", "SHO", T(3, 21.1)), ("Germany had surrendered", "UTA", T(4, 50.9)), ("@", "Germany had surrendered", UTA_TAG),
     ("They were waiting for a ship", "FOO", T(2, 6.3)), ("@", "They were waiting for a ship", FOO_TAG)],
    # 8 the guards
    [("The men who guarded them", "TUN", T(16, 20.2)), ("@", "The men who guarded them", TUNS_TAG), ("They were soldiers judged", "TUN", T(14, 8.3))],
    # 9 Bertucci
    [("was born in New Orleans", "TT", T(5, 26.7)), ("and joined the Army", "TT", T(4, 49.8)), ("@", "and joined the Army", TT_TAG), ("Two of his brothers", "TT", T(5, 39.0))],
    # 10 the record
    [("He spent eight months", "TT", T(5, 27.0)), ("@", "He spent eight months", TT_TAG),
     ("#", "After five years", None, {"type": "LedgerTimeline", "file": "FILE 02 — THE RECORD", "head": "Pvt. Clarence V. Bertucci, age 23",
        "rows": [{"date": "1940", "text": "Enlists, with a sixth-grade education"},
                 {"date": "1943-44", "text": "Eight months in England, never in combat"},
                 {"date": "3 TIMES", "text": "Punished: AWOL, refused guard duty, missed a train"},
                 {"date": "12 TIMES", "text": "In the hospital"}],
        "source": TEL})],
    # 11 said later
    [("said later that he talked", "COM", T(6, 21.6)), ("@", "said later that he talked", COM_TAG), ("Whether he really", "UTA", T(0, 58.2)), ("The Army's own record", "COM", T(6, 48.4))],
    # 12 July seventh
    [("July seventh was a Saturday", "SHO", T(3, 21.1)), ("@", "July seventh was a Saturday", SHO_TAG), ("The prisoners spent", "UTA", T(4, 7.5)), ("By midnight", "TT", T(9, 5.8)), ("@", "By midnight", NIGHT_TAG)],
    # 13 the belt
    [("The machine guns in the towers", "TT", T(9, 8.2)), ("took a belt", "TT", T(9, 22.2))],
    # 14 the shooting
    [("Shortly after midnight", "TT", T(9, 29.2)), ("he pulled the trigger", "TT", T(9, 24.5)),
     ("#", "He fired three bursts", "In one tent alone", {"type": "LedgerTimeline", "file": "FILE 03 — FIFTEEN SECONDS", "head": "After midnight, July 8, 1945",
        "rows": [{"date": "15 SECONDS", "text": "Three bursts, left to right"},
                 {"date": "250", "text": "Rounds, one full belt"},
                 {"date": "30 OF 43", "text": "Tents hit"},
                 {"date": "THROUGH", "text": "Canvas, beds and wooden floors"}],
        "source": TEL}),
     ("In one tent alone", "TT", T(9, 12.8))],
    # 15 Cornell
    [("The camp commander", "TT", T(9, 19.8)), ("@", "The camp commander", NIGHT_TAG),
     ("#", "He ran outside", "Up in the tower", {"type": "LedgerQuote", "file": "FILE 04 — THE LIEUTENANT", "head": "Lt. Albert I. Cornell, camp commander",
        "before": "I heard the shots and ran out. ", "key": "I saw no attempt at a prison camp break.", "after": "",
        "who": "Testimony to the Army board", "source": TEL}),
     ("Up in the tower", "TT", T(9, 5.8))],
    # 16 brought down
    [("A corporal climbed", "TT", T(9, 22.2))],
    # 17 the town wakes
    [("The noise woke nearly", "COM", T(5, 41.5)), ("@", "The noise woke nearly", COM_TAG), ("Many people thought", "TT", T(9, 15.2)), ("A boy of six", "UTA", T(3, 33.3)),
     ("#", "They could hear", None, {"type": "LedgerQuote", "file": "FILE 05 — THE FRONT PORCH", "head": "Three hundred feet from the camp",
        "before": "We came out on the front porch and ", "key": "we could hear the cries of the prisoners", "after": ".",
        "who": "Rodney Rasmussen, then six years old", "source": HN})],
    # 18 the doctor
    [("The town's doctor", "HOS", T(4, 44.4)), ("@", "The town's doctor", HOS_TAG), ("Guards and prisoners", "HOS", T(10, 31.3)), ("The men were carried", "HOS", T(1, 2.4))],
    # 19 the hospital
    [("It filled up", "HOS", T(4, 58.3)), ("@", "It filled up", HOS_TAG), ("Nurses and townspeople", "HOS", T(6, 21.6)),
     ("#", "The dead were laid out", None, {"type": "LedgerQuote", "file": "FILE 06 — THE HOSPITAL", "head": "The town's own newspaper",
        "before": "", "key": "The dead were placed on the west lawn of the hospital grounds.", "after": "",
        "who": "The Salina Sun", "source": SUN})],
    # 20 the toll
    [("Six men had died", "HOS", T(7, 58.7)),
     ("#", "Six men had died", None, {"type": "LedgerTimeline", "file": "FILE 07 — THE TOLL", "head": "Salina, July 8, 1945",
        "rows": [{"date": "6", "text": "Killed outright in the camp"},
                 {"date": "2", "text": "Died in the Salina hospital"},
                 {"date": "1", "text": "Died days later at Kearns: Friedrich Ritter, 48"},
                 {"date": "19", "text": "Wounded"}],
        "source": TEL + "; Salt Lake Telegram, July 16 and Aug. 17, 1945"})],
    # 21 survived the war
    [("These men had survived", "UTA", T(0, 58.2)), ("@", "These men had survived", UTA_TAG)],
    # 22 the board
    [("The Army sent a board", "UTA", T(3, 20.4)), ("@", "The Army sent a board", UTA_TAG), ("testified before it", "TT", T(2, 4.5)), ("@", "testified before it", TT_TAG),
     ("#", "But the machine guns", None, {"type": "LedgerQuote", "file": "FILE 08 — THE SPOKESMAN", "head": "Sgt. Hans Fertig, for the prisoners",
        "before": "", "key": "the presence of machine guns in the hands of guards had made them fear something serious might happen", "after": "",
        "who": "As reported by the Salt Lake Telegram", "source": TEL})],
    # 23 two days off
    [("asked for one thing", "TUN", T(13, 31.7)), ("@", "asked for one thing", TUNS_TAG)],
    # 24 Monday
    [("The colonel told him", "TT", T(2, 4.5)),
     ("#", "The colonel told him", "On Monday morning", {"type": "LedgerQuote", "file": "FILE 09 — MONDAY", "head": "Col. Arthur J. Ericsson to the prisoners",
        "before": "", "key": "highly desirable that the men do their work as usual", "after": "",
        "who": "Salt Lake Telegram", "source": TEL}),
     ("On Monday morning", "SHO", T(3, 21.1)), ("@", "On Monday morning", SHO_TAG)],
    # 25 no remorse
    [("They questioned", "TT", T(1, 41.9)), ("@", "They questioned", TT_TAG),
     ("#", "He said he had often", None, {"type": "LedgerQuote", "file": "FILE 10 — THE REASON", "head": "Pvt. Bertucci to the Army board",
        "before": "", "key": "He just didn't like Germans", "after": "",
        "who": "Col. Arthur J. Ericsson, on what Bertucci told the board. Bertucci was “not at all sorry.”", "source": OGD})],
    # 26 Time
    [("Time magazine", "COM", T(6, 48.4)),
     ("#", "He had hated Germans", None, {"type": "Slug", "title": "“He had hated Germans, so he had killed Germans.”", "subtitle": "Time magazine, July 23, 1945"})],
    # 27 the front page
    [("The front page", "COM", T(6, 50.5)), ("@", "The front page", COM_TAG)],
    # 28 Leavenworth
    [("That morning", "TUN", T(13, 5.0)),
     ("#", "They had murdered", "In the Ogden paper", {"type": "LedgerQuote", "file": "FILE 11 — THE SAME PAGE", "head": "Fort Leavenworth, Kansas, July 10, 1945",
        "before": "Five German prisoners of war who murdered a fellow prisoner in an Oklahoma internment camp ", "key": "were hanged this morning", "after": "",
        "who": "United Press, on the same front page as the Salina story", "source": OGD}),
     ("In the Ogden paper", "COM", T(6, 53.0))],
    # 29 Tribune
    [("The Salt Lake Tribune called", "COM", T(8, 8.7)), ("@", "The Salt Lake Tribune called", COM_TAG),
     ("#", "The Salt Lake Tribune called", "But some telegrams", {"type": "LedgerQuote", "file": "FILE 12 — THE EDITORIAL", "head": "Salt Lake Tribune, July 10, 1945",
        "before": "This outbreak at the Salina prison camp in Utah is ", "key": "not only deplorable but damnable", "after": ".",
        "who": "Editorial", "source": TRIB}),
     ("But some telegrams", "COM", T(8, 3.0))],
    # 30 the funeral
    [("On Thursday", "MEM", T(0, 27.3)), ("@", "On Thursday", MEM_TAG),
     ("#", "On Thursday", None, {"type": "Slug", "title": "July 12, 1945", "subtitle": "Fort Douglas, Salt Lake City · closed to the public"}),
     ("They wore American khaki", "MEM", T(1, 58.4)), ("An American chaplain", "MEM", T(0, 9.1))],
    # 31 the choir
    [("The public was not allowed", "TUN", T(13, 38.3)), ("@", "The public was not allowed", TUNS_TAG), ("A choir of German", "MEM", T(1, 58.4)), ("@", "A choir of German", UTA_TAG)],
    # 32 Ritter
    [("The next day", "HOS", T(7, 58.7)), ("@", "The next day", HOS_TAG)],
    # 33 the nine
    [("The rest of the dead", "MEM", T(0, 27.3)),
     ("#", "The rest of the dead", None, {"type": "LedgerTimeline", "file": "FILE 13 — THE NINE", "head": "Killed at Salina, July 1945",
        "rows": [{"date": "AGE 24-25", "text": "Ernst Fuchs · Hans Meyer · Fritz Stockmann · Otto Bross"},
                 {"date": "AGE 28-29", "text": "Adolf Paul · Gottfried Gaag"},
                 {"date": "AGE 31-32", "text": "Georg Liske · Walter Vogel"},
                 {"date": "AGE 48", "text": "Friedrich Ritter"}],
        "source": WP + "; " + TEL})],
    # 34 Owens
    [("An Army captain", "TT", T(1, 55.5)), ("@", "An Army captain", TT_TAG), ("He looked at the evidence", "TT", T(2, 4.5))],
    # 35 the evidence
    [("His superiors", "TT", T(1, 28.3)),
     ("#", "told officers he had planned", None, {"type": "LedgerTimeline", "file": "FILE 14 — THE EVIDENCE", "head": "What the Army knew",
        "rows": [{"date": "PLANNED", "text": "He told of planning the shootings in advance"},
                 {"date": "A WAITRESS", "text": "“Something exciting” would happen that night"},
                 {"date": "THE GUN", "text": "Kept empty; he loaded it himself"},
                 {"date": "SOBER", "text": "No evidence he was drunk or unfit for duty"}],
        "source": "Salt Lake Telegram, Aug. 17, 1945; " + WP})],
    # 36 insane
    [("Doctors at Bushnell", "HOS", T(4, 44.4)), ("@", "Doctors at Bushnell", HOS_TAG),
     ("#", "In August", None, {"type": "Slug", "title": "August 1945", "subtitle": "Army doctors find Pvt. Bertucci “mentally unbalanced”"}),
     ("There was no court-martial", "HOS", T(10, 17.4)), ("He was sent to", "TT", T(10, 30.8)), ("@", "He was sent to", TT_TAG)],
    # 37 never tried
    [("He spent much of", "HOS", T(7, 58.7)), ("@", "He spent much of", HOS_TAG), ("Nobody was ever tried", "MEM", T(1, 58.4))],
    # 38 the wounded
    [("The wounded recovered", "HOS", T(6, 21.6)), ("@", "The wounded recovered", HOS_TAG), ("A later agreement", "TT", T(10, 31.8)), ("@", "A later agreement", TT_TAG)],
    # 39 the camp empties
    [("The camp emptied", "SHO", T(1, 26.2)), ("The next spring", "SHO", T(3, 1.9)), ("@", "The next spring", SHO_TAG), ("Later, farm workers", "SHO", T(3, 59.4)), ("Decades on", "UTA", T(4, 20.5)), ("@", "Decades on", UTA_TAG)],
    # 40 Lampe
    [("In nineteen seventy-seven", "UTA", T(0, 58.2)), ("@", "In nineteen seventy-seven", UTA_TAG),
     ("#", "He said he had received", None, {"type": "LedgerQuote", "file": "FILE 15 — THE RETURN", "head": "Dieter Lampe, wounded at Salina, back in 1977",
        "before": "He said he ", "key": "received excellent care", "after": ", and left strongly opposed to war.",
        "who": "Deseret News", "source": DN})],
    # 41 memory
    [("In nineteen eighty-eight", "MEM", T(0, 27.3)), ("@", "In nineteen eighty-eight", MEM_TAG), ("Two men wounded", "MEM", T(1, 58.4)), ("In 2016", "UTA", T(3, 33.3)), ("@", "In 2016", UTA_TAG)],
    # 42 comment ask
    [("If your family", "SHO", T(1, 26.2)), ("@", "If your family", SHO_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "POWs in the beet fields, in your family's story?", "subtitle": "Tell us in the comments"})],
    # 43 echo
    [("In the back corner", "MEM", T(0, 27.3)), ("They had outlived", "UTA", T(3, 33.3)), ("@", "They had outlived", UTA_TAG)],
]

WC = "Wikimedia Commons"
UDN = "Utah Digital Newspapers, J. Willard Marriott Library · no copyright"
PHOTOS = [
    (2, "There was a machine gun", None, "gun_tower_1945.jpg", "02", "This weapon dealt death", "The tower gun at Salina, as printed the next day", f"Salt Lake Telegram, July 9, 1945 · {UDN}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (3, "This is the documented story", None, "salina_sun_1945.jpg", "03", "The Salina Sun", "The town's own newspaper, July 13, 1945", f"{UDN}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (6, "It was strange", None, "salina_pow_camp.png", "06", "Salina, Utah", "The camp sat at the east end of Main Street", f"CC0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (9, "was born in New Orleans", None, "bertucci_1945.jpg", "09", "Clarence V. Bertucci", "As printed in the Salt Lake Telegram, July 9, 1945", f"{UDN}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (27, "The front page", None, "headline_telegram_1945.jpg", "27", "Monday, July 9, 1945", "The first report, in the Salt Lake Telegram", f"{UDN}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (28, "That morning", None, "leavenworth_prison.jpg", "28", "Fort Leavenworth, Kansas", "The military prison, in an older photograph", f"Library of Congress · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (31, "A choir of German", None, "fort_douglas_b.jpg", "31", "Fort Douglas Cemetery", "Salt Lake City, in winter", f"CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.75]}),
    (39, "The camp emptied", None, "camp_salina_site.jpg", "39", "Camp Salina today", "A rebuilt guard tower and restored buildings", f"CC BY 2.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (41, "In 2016", None, "salina_town.jpg", "41", "Salina, Utah", "Main Street today", f"CC BY 4.0 · {WC}", {"crop": [0.0, 0.08, 1.0, 0.85]}),
    (43, "In the back corner", None, "fort_douglas_cemetery.jpg", "43", "Fort Douglas Post Cemetery", "Salt Lake City, 2020", f"CC0 · {WC}", {"crop": [0.0, 0.05, 1.0, 0.85]}),
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
