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
    "FL": ("interrogation_florence_1945", 1), "F5": ("interrogation_fifth_army_1945", 1), "F5B": ("interrogation_fifth_army_1945_b", 1),
    "RAD": ("radio_at_war_1944", 1), "SND": ("sound_recording_1943", 1),
    "U858": ("u858_surrender_1945", 1), "GRIP": ("gripsholm_red_cross_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

NPS = "National Park Service, “POWs and Intel at Fort Hunt in World War II”"
CIA = "W. Fishbein, review of R. K. Sutton, Nazis on the Potomac, Studies in Intelligence 66/2 (2022)"
WP = "P. Dvorak, Washington Post, 6 Oct. 2007"
CN = "Connection Newspapers, 8 Oct. 2007"
IT_TAG = "Stand-in · U.S. Fifth Army prisoner interrogation, Italy, 1945"
RAD_TAG = "Stand-in · from Radio at War (RCA, 1944)"
SND_TAG = "Stand-in · from Sound Recording and Reproduction (1943)"
U_TAG = "U-858 surrenders to the U.S. Navy, May 1945"
GRIP_TAG = "Real Red Cross parcels, 1943 · the escape kits came in fake ones"
P = [
    # 0 cold open
    [("During", "F5", T(0, 19.7)), ("@", "During the Second World War", IT_TAG),
     ("German prisoners sat", "F5B", T(1, 20.5)), ("U-boat officers", "U858", T(4, 10.0)), ("@", "U-boat officers", U_TAG),
     ("They thought they were only", "F5", T(6, 2.0))],
    # 1 the listeners
    [("In another building", "RAD", T(14, 40.0)), ("@", "In another building", RAD_TAG),
     ("Many of them had been born", "FL", T(4, 20.0)), ("Many were Jewish", "RAD", T(16, 34.1)), ("Now they were listening", "F5B", T(7, 31.0))],
    # 2 the box
    [("The place did not", "F5", T(0, 38.5)),
     ("#", "It had no name", None, {"type": "Slug", "title": "P.O. Box 1142", "subtitle": "Fort Hunt, Virginia · 1942–1945"}),
     ("This is the documented story", "SND", T(1, 20.0)), ("@", "This is the documented story", SND_TAG)],
    # 3 Fort Hunt
    [("The address belonged", "RAD", T(13, 10.0)), ("@", "The address belonged", "Washington, D.C. · from Radio at War (RCA, 1944)"),
     ("In April", "F5", T(1, 25.0)), ("@", "In April", IT_TAG)],
    # 4 the site
    [("The site was chosen", "F5", T(4, 29.9)),
     ("#", "At its height", None, {"type": "LedgerTimeline", "file": "FILE 01 — THE SITE", "head": "Why Fort Hunt",
        "rows": [{"date": "WHERE", "text": "On the Potomac, south of Alexandria"}, {"date": "WHY", "text": "Isolated, yet close to the Pentagon"},
                 {"date": "AT ITS HEIGHT", "text": "87 buildings behind the wire"}],
        "source": f"{NPS}; {CIA}"}),
     ("Neighbors saw unmarked buses", "F5", T(1, 38.0))],
    # 5 processing center
    [("On paper", "FL", T(0, 15.0)), ("@", "On paper", IT_TAG),
     ("#", "That mattered", None, {"type": "LedgerTimeline", "file": "FILE 02 — ON PAPER", "head": "Not a prison camp",
        "rows": [{"date": "OFFICIALLY", "text": "A “processing center”"}, {"date": "IN PRACTICE", "text": "Prisoners held for days or weeks, unreported"},
                 {"date": "GENEVA", "text": "The Red Cross was supposed to be told"}],
        "source": "WETA Boundary Stones, “P.O. Box 1142: The Secrets of Fort Hunt” (2015); Wikipedia, “P. O. Box 1142”"}),
     ("Under the Geneva Convention", "GRIP", T(0, 30.5)), ("@", "Under the Geneva Convention", "American Red Cross supplies, 1943")],
    # 6 refugees
    [("To make it work", "RAD", T(4, 20.0)), ("@", "To make it work", RAD_TAG),
     ("Many of the people it found", "FL", T(4, 40.0)), ("They had fled", "F5B", T(1, 30.0))],
    # 7 the Navy
    [("The Navy was just as choosy", "RAD", T(3, 30.0)),
     ("#", "It interviewed four hundred", "Some of the Army's men", {"type": "LedgerBars", "file": "FILE 03 — THE NAVY", "head": "Chosen to interrogate", "max": 450,
        "bars": [{"label": "Candidates interviewed", "value": 450, "figure": "450", "note": ""},
                 {"label": "Interrogators chosen", "value": 35, "figure": "35", "note": "fewer than one in twelve"}],
        "source": CN}),
     ("Some of the Army's men", "RAD", T(5, 20.0))],
    # 8 Peter Weiss
    [("One of them was Peter Weiss", "FL", T(6, 29.0)), ("@", "One of them was Peter Weiss", IT_TAG),
     ("#", "Decades later", None, {"type": "LedgerQuote", "file": "FILE 04 — THE LISTENER", "head": "Sergeant Peter Weiss, born in Vienna",
        "before": "My job was to ", "key": "listen and listen", "after": " very carefully.", "who": "Peter Weiss, 2007", "source": CN}),
     ("Sometimes that listening", "RAD", T(16, 34.1))],
    # 9 the prisoners
    [("Between", "F5", T(1, 13.0)), ("@", "Between", IT_TAG),
     ("#", "more than three thousand", None, {"type": "LedgerTimeline", "file": "FILE 05 — THE PRISONERS", "head": "Who came through the box",
        "rows": [{"date": "1942–JULY 1945", "text": "3,451 prisoners processed"}, {"date": "PICKED FOR", "text": "What they might know"},
                 {"date": "AMONG THEM", "text": "U-boat crews, senior officers, scientists"}],
        "source": NPS}),
     ("They were picked", "U858", T(6, 48.0)), ("@", "They were picked", U_TAG)],
    # 10 Gehlen
    [("Among them was General", "F5B", T(8, 40.0)), ("@", "Among them was General", IT_TAG),
     ("#", "Among them was General", None, {"type": "Slug", "title": "General Reinhard Gehlen", "subtitle": "German army intelligence on the Eastern Front · questioned at Fort Hunt"}),
     ("For the Americans", "F5B", T(3, 49.0)), ("The war against Germany", "F5B", T(6, 17.0))],
    # 11 microphones
    [("The rooms where", "SND", T(1, 26.0)), ("@", "The rooms where", SND_TAG),
     ("At first, even some", "SND", T(1, 39.0)), ("But the results", "SND", T(4, 46.0))],
    # 12 recordings
    [("The interrogations were useful", "F5B", T(0, 30.0)), ("@", "The interrogations were useful", IT_TAG),
     ("The recordings were often better", "SND", T(0, 15.0)),
     ("#", "Some of the most important", None, {"type": "LedgerTimeline", "file": "FILE 06 — THE METHODS", "head": "Three ways to learn",
        "rows": [{"date": "1", "text": "Interrogation, tailored to each prisoner"}, {"date": "2", "text": "Hidden microphones in the rooms"},
                 {"date": "3", "text": "Stool pigeons placed among the prisoners"}],
        "source": f"{NPS}; WETA Boundary Stones (2015)"}),
     ("There were also stool pigeons", "F5", T(5, 9.0))],
    # 13 not fooled
    [("Not every prisoner was fooled", "F5", T(6, 28.4)), ("leaving American clerks", "FL", T(5, 50.0)), ("@", "leaving American clerks", IT_TAG)],
    # 14 rewards
    [("The veterans of Fort Hunt", "FL", T(9, 27.0)),
     ("#", "Instead, they rewarded", None, {"type": "LedgerTimeline", "file": "FILE 07 — REWARDS", "head": "What cooperation could buy",
        "rows": [{"date": "READING", "text": "Books and newspapers"}, {"date": "COMFORTS", "text": "Cigarettes and liquor"},
                 {"date": "OUTINGS", "text": "Steak dinners"}, {"date": "GAMES", "text": "Chess, Ping-Pong"}],
        "source": f"{WP}; {CIA}"}),
     ("Some prisoners were taken", "F5", T(5, 22.0))],
    # 15 Kolm and Mayer
    [("Henry Kolm", "F5B", T(2, 10.0)), ("@", "Henry Kolm", IT_TAG),
     ("#", "said that a game", None, {"type": "LedgerQuote", "file": "FILE 08 — A BATTLE OF WITS", "head": "Henry Kolm, physicist, later at MIT",
        "before": "We got more information out of a German general with ", "key": "a game of chess or Ping-Pong", "after": " than they do today, with their torture.",
        "who": "Henry Kolm, 90, in 2007", "source": WP}),
     ("Arno Mayer", "F5B", T(1, 57.6))],
    # 16 the bluff
    [("For the most stubborn", "F5B", T(5, 52.0)), ("@", "For the most stubborn", IT_TAG),
     ("#", "Interrogators threatened", None, {"type": "LedgerTimeline", "file": "FILE 09 — THE BLUFF", "head": "The Russian card",
        "rows": [{"date": "THE THREAT", "text": "Hand-over to the Soviet Union"}, {"date": "THE PROPS", "text": "“Red Army officers” in the room"},
                 {"date": "THE ACTORS", "text": "Russian-speaking U.S. soldiers"}],
        "source": f"{CIA}; Wikipedia, “P. O. Box 1142”"}),
     ("It was a bluff", "F5B", T(8, 46.0))],
    # 17 reports
    [("By the end of August", "FL", T(7, 20.0)), ("@", "By the end of August", IT_TAG),
     ("#", "By the end of August", "Interrogations helped point", {"type": "LedgerBars", "file": "FILE 10 — THE OUTPUT", "head": "P.O. Box 1142, to August 1945", "max": 5000,
        "bars": [{"label": "Prisoners processed", "value": 3451, "figure": "3,451", "note": "to July 1945"},
                 {"label": "Intelligence reports", "value": 5000, "figure": "5,000+", "note": ""}],
        "source": NPS}),
     ("Interrogations helped point", "F5B", T(3, 49.0))],
    # 18 discoveries
    [("Interrogations and recordings revealed", "F5B", T(3, 11.9)), ("@", "Interrogations and recordings revealed", IT_TAG),
     ("#", "They revealed that the German navy", None, {"type": "LedgerTimeline", "file": "FILE 11 — WHAT THEY LEARNED", "head": "Overheard, then bombed",
        "rows": [{"date": "RAILWAYS", "text": "Supplies loaded at crossings, not stations"}, {"date": "U-BOAT PENS", "text": "Dummy concrete structures"},
                 {"date": "TORPEDOES", "text": "A defense against the acoustic torpedo"}],
        "source": f"{CIA}; Wikipedia, “P. O. Box 1142”"}),
     ("Questioning U-boat crews", "U858", T(4, 13.0)), ("@", "Questioning U-boat crews", U_TAG)],
    # 19 Henke
    [("One prisoner never left", "U858", T(1, 42.7)), ("@", "One prisoner never left", U_TAG),
     ("#", "Werner Henke commanded", None, {"type": "Slug", "title": "Werner Henke", "subtitle": "Commander of U-515"}),
     ("In December", "RAD", T(15, 6.0)), ("@", "In December", "A warship at sea · from Radio at War (RCA, 1944)"),
     ("Henke believed", "F5B", T(9, 10.8)), ("@", "Henke believed", IT_TAG)],
    # 20 the fence
    [("He was captured in April", "U858", T(4, 26.9)), ("According to his biographer", "F5B", T(5, 15.6)), ("@", "According to his biographer", IT_TAG),
     ("#", "On June fifteenth", None, {"type": "Slug", "title": "June 15, 1944", "subtitle": "Fort Hunt, Virginia"}),
     ("He kept climbing", "F5", T(0, 24.0)), ("No prisoner ever escaped", "F5", T(0, 20.0))],
    # 21 MIS-X
    [("Fort Hunt had a second secret", "GRIP", T(0, 6.0)), ("@", "Fort Hunt had a second secret", GRIP_TAG),
     ("#", "In another part", None, {"type": "Slug", "title": "MIS-X", "subtitle": "Escape kits for American prisoners in Germany"})],
    # 22 the kits
    [("They hid compasses", "GRIP", T(2, 32.6)), ("They packed radio parts", "GRIP", T(4, 22.5)), ("@", "They packed radio parts", GRIP_TAG),
     ("#", "eighty to a hundred", None, {"type": "LedgerTimeline", "file": "FILE 12 — THE KITS", "head": "Mailed to German prison camps",
        "rows": [{"date": "BUTTONS", "text": "5 million, with hidden compasses"}, {"date": "MAPS", "text": "On silk and tissue paper"},
                 {"date": "BY 1944", "text": "80–120 packages a day"}],
        "source": NPS})],
    # 23 burn all records
    [("When the war ended", "FL", T(7, 32.8)), ("@", "When the war ended", IT_TAG),
     ("#", "In August", None, {"type": "LedgerTimeline", "file": "FILE 13 — BURN ALL RECORDS", "head": "How the box disappeared",
        "rows": [{"date": "AUG. 1945", "text": "Escape-program records ordered destroyed"}, {"date": "1946", "text": "Barracks bulldozed"},
                 {"date": "1948", "text": "The land is a park again"}],
        "source": f"{NPS}; Wikipedia, “P. O. Box 1142”"}),
     ("The men who had worked there", "RAD", T(21, 30.0)), ("@", "The men who had worked there", RAD_TAG)],
    # 24 the oath
    [("Most of the veterans kept the oath", "FL", T(9, 40.0)),
     ("#", "As Arno Mayer put it", None, {"type": "LedgerQuote", "file": "FILE 14 — THE OATH", "head": "Arno Mayer, later a historian at Princeton",
        "before": "When you swear to secrecy ", "key": "you don't really know when the oath expires", "after": ".",
        "who": "Arno Mayer, 2007", "source": "History News Network (2007)"})],
    # 25 the Park Service
    [("Sixty years later", "SND", T(0, 15.0)), ("@", "Sixty years later", SND_TAG), ("One ranger", "RAD", T(0, 45.8)), ("@", "One ranger", RAD_TAG),
     ("#", "One ranger", None, {"type": "Slug", "title": "70+ interviews", "subtitle": "Brandon Bies, National Park Service"})],
    # 26 reunion
    [("In October", "RAD", T(21, 39.0)), ("most of them in their eighties", "RAD", T(1, 4.1)), ("A flag was raised", "RAD", T(21, 44.0)), ("@", "In October", "Stand-in · the flag, from Radio at War (RCA, 1944)"),
     ("#", "about two dozen veterans", None, {"type": "Slug", "title": "October 2007", "subtitle": "About two dozen veterans return to Fort Hunt"})],
    # 27 Frenkel
    [("They came back during another war", "F5B", T(2, 59.5)), ("@", "They came back during another war", IT_TAG),
     ("#", "George Frenkel", None, {"type": "LedgerQuote", "file": "FILE 15 — THE LAST WORD", "head": "George Frenkel, 87",
        "before": "We extracted information in a battle of the wits. I'm proud to say ", "key": "I never compromised my humanity", "after": ".",
        "who": "George Frenkel, 2007", "source": WP})],
    # 28 comment ask
    [("If someone in your family", "RAD", T(14, 47.0)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "A secret wartime job in your family?", "subtitle": "Tell us in the comments"})],
    # 29 echo
    [("Today, Fort Hunt is a park", "F5", T(0, 22.0)), ("The microphones are long gone", "SND", T(4, 46.0)), ("@", "The microphones are long gone", SND_TAG),
     ("For sixty years", "F5B", T(9, 23.2))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (3, "The address belonged", None, "fort_hunt_sign.jpg", "03", "Fort Hunt Park", "Fort Hunt Park, Virginia, today: the old battery behind the park signs", f"Slowking4 · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "close enough to the Pentagon", "At its height", "pentagon_vmail_1943.jpg", "04", "The Pentagon, 1943", "A U.S. Army courier delivers letters to the V-mail room at the Pentagon, 1943", f"public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (7, "Some of the Army's men", None, "camp_ritchie_castle.jpg", "07", "Camp Ritchie", "The Castle at Camp (later Fort) Ritchie, Maryland, the Army's intelligence school", f"Preservation Maryland · CC BY-SA 2.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (17, "Interrogations helped point", None, "peenemunde_recon_1943.jpg", "17", "Peenemünde", "RAF reconnaissance photo of Peenemünde, 23 June 1943 (IWM C 4782)", f"public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (20, "He was captured in April", None, "u515_sinking_1944.jpg", "20", "U-515", "U-515 afire and sinking after the attack by U.S. Navy ships and aircraft, 9 April 1944", f"U.S. Navy (80-G-227198) · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (22, "They hid compasses", "They printed maps on silk", "button_compass.jpg", "22", "Button compass", "A wartime button compass: the two halves screw apart", f"Royal Australian Air Force · CC BY 4.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (22, "They printed maps on silk", None, "silk_escape_map.jpg", "22", "Silk map", "A wartime silk escape-and-evasion map (OSS)", f"CIA · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (26, "A flag was raised", None, "fort_hunt_flagpole.jpg", "26", "Fort Hunt Park", "The flagpole and old battery at Fort Hunt Park", f"Slowking4 · CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (29, "Today, Fort Hunt is a park", None, "fort_hunt_battery.jpg", "29", "Fort Hunt today", "Battery Mount Vernon, Fort Hunt Park, 2016", f"Antony-22 · CC BY-SA 4.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
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
