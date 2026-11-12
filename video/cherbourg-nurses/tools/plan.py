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
    "A": ("u505_capture_a", 1), "B": ("u505_capture_b", 1), "I": ("u505_interior_1945", 1), "CHI": ("u505_chicago_1954", 1),
    "CP": ("controlling_pows_1944", 1), "GR": ("gripsholm_red_cross_1943", 1), "CT": ("cotton_1937", 1),
}


def T(m, s=0.0):
    return m * 60 + s

S = {}

TG = "Task Group 22.3 report, Capture of German Submarine U-505, June 1944"
LANGE = "Statement of Oblt. Harald Lange, CO of U-505, June 1944 (TG 22.3 report, encl. A8)"
MEMO = "Capt. D. V. Gallery, memo to Task Group 22.3, Top Secret, June 14, 1944"
NWW2 = "Kali Martin, National WWII Museum, 2020"
MSI = "Museum of Science and Industry, Chicago; Navy press release, May 16, 1945"
A_TAG = "The capture of U-505, June 4, 1944 · U.S. Navy film"
I_TAG = "Inside U-505 after her capture · U.S. Navy film, 1945"
CHI_TAG = "U-505 arrives in Chicago, June 26, 1954 · U.S. Navy film"
CP_TAG = "Stand-in · German prisoners in U.S. Army hands · from Controlling German Prisoners of War (War Dept., 1944)"
GR_TAG = "Red Cross parcels for prisoners of war, New York, 1943 · U.S. Navy film"
CT_TAG = "Stand-in · cotton fields, 1937 · U.S. Department of Agriculture film"
WC = "Wikimedia Commons"
P = [
    # 0 families told
    [("In", "A", 106.8), ("@", "In the summer of", A_TAG),
     ("#", "In the summer of", None, {"type": "Slug", "title": "Summer, 1944", "subtitle": "Germany · the families of U-505's crew"}),
     ("The submarine U", "A", 130.0)],
    # 1 not dead
    [("They were not dead", "CP", T(12, 8.7)), ("@", "They were not dead", CP_TAG), ("in a corner of a prison camp", "CP", T(11, 42.9)), ("No letter of theirs", "CP", T(8, 42.3)), ("The Red Cross was not told", "GR", T(4, 28.6)), ("@", "The Red Cross was not told", GR_TAG)],
    # 2 the rules
    [("The rules of war said", "CP", T(0, 58.0)), ("@", "The rules of war said", "U.S. Army field manual FM 27-10, Rules of Land Warfare · from Controlling German Prisoners of War (1944)"), ("The United States Navy decided", "B", 4.0), ("@", "The United States Navy decided", A_TAG)],
    # 3 documented story
    [("This is the documented story", "A", 151.8), ("@", "This is the documented story", A_TAG), ("told from the Navy's own", "I", 17.2), ("@", "told from the Navy's own", I_TAG)],
    # 4 the boat
    [("U five-oh-five was a long-range", "I", 28.7), ("@", "U five-oh-five was a long-range", I_TAG), ("In November nineteen forty-two", "A", 500.4), ("@", "In November nineteen forty-two", "Stand-in · a Navy patrol plane, 1944 · U.S. Navy film"), ("She limped home", "A", 106.8)],
    # 5 six times
    [("After months of repairs", "I", T(2, 0.7)), ("@", "After months of repairs", I_TAG), ("Six times in a row", "I", T(5, 4.7)), ("Sabotage by French", "I", T(5, 27.7))],
    # 6 Zschech
    [("In October nineteen forty-three", "I", 40.2), ("@", "In October nineteen forty-three", I_TAG), ("His second in command", "I", T(3, 21.2))],
    # 7 Lange
    [("In November nineteen forty-three she got", "A", 607.0), ("@", "In November nineteen forty-three she got", A_TAG), ("By late spring", "A", 141.0)],
    # 8 the hunters
    [("The Americans hunting her", "B", 52.4), ("@", "The Americans hunting her", A_TAG), ("He did not want to sink", "A", 343.0)],
    # 9 the plan
    [("Before the cruise", "A", 185.5), ("@", "Before the cruise", A_TAG),
     ("#", "Before the cruise", None, {"type": "LedgerTimeline", "file": "FILE 01 — THE PLAN", "head": "Task Group 22.3, May–June 1944",
        "rows": [{"date": "BEFORE THE CRUISE", "text": "Every ship: plan a capture, organize boarding parties"},
                 {"date": "JUNE 3, EVENING", "text": "The plan of the day for June 4 is printed"},
                 {"date": "ON IT", "text": "The crew for a captured German submarine"}],
        "source": TG})],
    # 10 contact
    [("At ten past eleven", "A", 126.0),
     ("#", "At ten past eleven", None, {"type": "Slug", "title": "June 4, 1944 · 11:10 a.m.", "subtitle": "Off West Africa · two days before D-Day"}),
     ("Six minutes later", "A", 196.8), ("@", "Six minutes later", A_TAG)],
    # 11 inside
    [("Inside the boat", "I", T(4, 7.2)), ("@", "Inside the boat", I_TAG), ("Then came two heavy shocks", "I", T(2, 46.7)), ("Not knowing how bad", "I", T(1, 49.2))],
    # 12 surfaced
    [("She came up eight hundred", "A", 151.8), ("@", "She came up eight hundred", A_TAG),
     ("#", "He ordered his men", None, {"type": "LedgerQuote", "file": "FILE 02 — THE ORDER", "head": "Oblt. Harald Lange, wounded on deck",
        "before": "At once I gave the order ", "key": "to leave the boat and to sink her", "after": ".", "who": "Harald Lange, U-505's captain", "source": LANGE})],
    # 13 circling
    [("They opened valves", "A", 264.2), ("@", "They opened valves", A_TAG),
     ("#", "From a life raft", None, {"type": "LedgerQuote", "file": "FILE 03 — THE RAFT", "head": "Watching from a pipe boat",
        "before": "I ordered the men around me to give ", "key": "three cheers for our sinking boat", "after": ".", "who": "Harald Lange", "source": LANGE}),
     ("At eleven twenty-seven", "A", 286.7)],
    # 14 Pillsbury
    [("A boat from the destroyer escort", "B", 100.7), ("@", "A boat from the destroyer escort", A_TAG), ("One German sailor lay dead", "B", 128.0)],
    # 15 down the hatch
    [("David went down the hatch", "I", T(1, 26.2)), ("@", "David went down the hatch", I_TAG), ("and started passing up papers", "B", 141.0), ("@", "and started passing up papers", A_TAG), ("A second boarding party", "B", 149.1)],
    # 16 Trosino and the tow
    [("The carrier's chief engineer", "I", T(4, 53.2)), ("@", "The carrier's chief engineer", I_TAG), ("The Guadalcanal took her in tow", "A", 624.1), ("@", "The Guadalcanal took her in tow", A_TAG)],
    # 17 subscribe (midpoint)
    [("If you want more", "A", 421.7),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 18 the problem
    [("Now the Navy had a problem", "B", 36.3), ("@", "Now the Navy had a problem", A_TAG), ("About three thousand", "A", 354.2)],
    # 19 the memo
    [("On the fourteenth of June", "A", 365.4), ("@", "On the fourteenth of June", A_TAG),
     ("#", "On the fourteenth of June", None, {"type": "LedgerDocument", "file": "FILE 04 — TOP SECRET", "head": "To all hands, June 14, 1944", "source": MEMO,
        "spans": [{"doc": "doc_memo", "say": "The capture of the U five-oh-five can be one of the major turning points in World War number two provided repeat provided we keep our mouths shut about it"}]})],
    # 20 silence
    [("The enemy must not learn", "A", 376.7), ("In Bermuda the crews", "A", 389.0), ("According to the historian", "A", 118.1)],
    # 21 the prisoners
    [("The bigger risk", "A", 545.4), ("@", "The bigger risk", A_TAG), ("One letter home", "A", 556.6)],
    # 22 Camp Ruston
    [("In the summer of nineteen forty-four they were", "CP", T(11, 17.1)), ("@", "In the summer of nineteen forty-four they were", CP_TAG),
     ("#", "In the summer of nineteen forty-four they were", None, {"type": "Slug", "title": "Camp Ruston, Louisiana", "subtitle": "Summer 1944 · about 7 miles west of Ruston"}),
     ("At its peak", "CP", T(7, 37.8))],
    # 23 isolated
    [("The U five-oh-five men did not", "CP", T(11, 42.9)), ("@", "The U five-oh-five men did not", CP_TAG), ("Their names were withheld", "GR", T(7, 27.7)), ("@", "Their names were withheld", GR_TAG), ("The letters they tried", "CP", T(8, 42.3))],
    # 24 no chances
    [("The rules of war said prisoners", "CP", T(0, 32.2)), ("@", "The rules of war said prisoners", "The 1929 Geneva Convention · from Controlling German Prisoners of War (1944)"),
     ("#", "The National World War Two Museum", None, {"type": "LedgerQuote", "file": "FILE 05 — THE RULES", "head": "Why the Red Cross was not told",
        "before": "", "key": "could take no chances", "after": "", "who": "The National WWII Museum, on why the military kept the Red Cross out", "source": NWW2})],
    # 25 camp life
    [("Around them other prisoners", "CT", 3.0), ("@", "Around them other prisoners", CT_TAG), ("They had an orchestra", "CP", T(7, 50.7)), ("@", "They had an orchestra", CP_TAG), ("How much of that life", "CP", T(12, 34.5))],
    # 26 dead on paper
    [("In Germany the boat", "A", 118.0), ("@", "In Germany the boat", A_TAG),
     ("#", "By August", None, {"type": "LedgerTimeline", "file": "FILE 06 — DEAD ON PAPER", "head": "What the families were told",
        "rows": [{"date": "JUNE 4, 1944", "text": "U-505 captured; 58 of 59 men alive"},
                 {"date": "BY AUGUST 1944", "text": "Their men “must be considered dead”"},
                 {"date": "MAY 16, 1945", "text": "The U.S. Navy reveals the capture"},
                 {"date": "1947", "text": "The crew reaches Germany"}],
        "source": MSI})],
    # 27 the Navy tells the world
    [("On the eighth of May", "A", 343.0), ("@", "On the eighth of May", A_TAG),
     ("#", "Eight days later", None, {"type": "Slug", "title": "May 16, 1945", "subtitle": "Navy press release: the capture revealed"}),
     ("It called the capture", "A", 624.1)],
    # 28 David
    [("Albert David received", "A", 590.3), ("@", "Albert David received", A_TAG)],
    # 29 home in 1947
    [("Only after the war", "CP", T(11, 33.9)), ("@", "Only after the war", CP_TAG), ("The crew of U five-oh-five did not", "A", 596.0)],
    # 30 Chicago
    [("The Navy kept the submarine", "CHI", 81.7), ("@", "The Navy kept the submarine", CHI_TAG), ("In nineteen fifty-four", "CHI", 207.4), ("and people in Chicago", "CHI", 245.1)],
    # 31 reunion
    [("In nineteen sixty-four", "CHI", 257.7), ("@", "In nineteen sixty-four", CHI_TAG)],
    # 32 the museum corrected
    [("For years the museum", "CHI", 320.6), ("@", "For years the museum", CHI_TAG), ("In nineteen ninety-eight", "CHI", 433.7)],
    # 33 comment ask
    [("If your family", "CHI", 408.5), ("@", "If your family", CHI_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "A sailor or a POW in your family's story?", "subtitle": "Tell us in the comments"})],
    # 34 underground
    [("In 2004 the museum", "CHI", 81.7), ("In Louisiana two buildings", "CT", 1.0), ("@", "In Louisiana two buildings", CT_TAG), ("They are what is left", "CP", T(7, 37.8)), ("@", "They are what is left", CP_TAG)],
]

PHOTOS = [
    (2, "One American captain", None, "gallery_portrait.jpg", "02", "Capt. Daniel V. Gallery", "Commander, Task Group 22.3", f"U.S. Navy · public domain · {WC}", {}),
    (7, "Harald Lange", None, "U-505POWsLangeXfer2.jpg", "07", "Oblt. Harald Lange", "Hoisted aboard the Guadalcanal, wounded, June 4, 1944", "U.S. Navy · public domain · uboatarchive.net", {}),
    (8, "Captain Daniel Gallery commanded", None, "u505_near_guadalcanal.jpg", "08", "USS Guadalcanal", "With the captured U-505, June 4, 1944", f"U.S. Navy 80-G-49170 · public domain · {WC}", {}),
    (12, "She came up eight hundred", None, "u505_under_fire.jpg", "12", "U-505 under fire", "June 4, 1944", f"U.S. Navy · public domain · {WC}", {}),
    (14, "Lieutenant Albert David led", None, "pillsbury_alongside.jpg", "14", "USS Pillsbury", "Alongside the captured U-505", f"U.S. Navy 80-G-324310 · public domain · {WC}", {}),
    (16, "The Guadalcanal took her in tow", None, "towline_party.jpg", "16", "The tow line", "Americans on U-505's deck, under the U.S. flag", f"U.S. Navy 80-G-49172 · public domain · {WC}", {}),
    (20, "In Bermuda the crews", None, "abnaki_tow.jpg", "20", "Under tow", "The tug Abnaki takes over the tow", f"U.S. Navy 80-G-324351 · public domain · {WC}", {}),
    (21, "The bigger risk", None, "pows_exercise.jpg", "21", "U-505's crew", "Prisoners exercise on the Guadalcanal's deck, June 1944", f"U.S. Navy · public domain · {WC}", {}),
    (28, "Albert David received", None, "david_portrait.jpg", "28", "Lt. Albert L. David", "Medal of Honor · died Sept. 17, 1945", f"U.S. Navy · public domain · {WC}", {}),
    (31, "Gallery gave the German captain", None, "binoculars_msi.jpg", "31", "U-505's binoculars", "On display in Chicago today", f"Daderot · CC0 · {WC}", {}),
    (34, "In 2004 the museum", None, "u505_msi_01.jpg", "34", "U-505 today", "Museum of Science and Industry, Chicago", f"GualdimG · CC BY-SA 4.0 · {WC}", {}),
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
