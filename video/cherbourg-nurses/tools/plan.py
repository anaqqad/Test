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
    "E": ("evac_hospital_1945", 1), "N": ("normandy_medical_1944", 1), "P": ("cherbourg_pows_1944", 1),
    "D": ("cherbourg_damage_1944", 0.78), "C": ("evac128_1944", 1), "H": ("hospital2_1944", 1), "HB": ("cherbourg_harbor_1944", 1),
}


def T(m, s=0.0):
    return m * 60 + s

S = {}

MED = "WW2 US Medical Research Centre, 45th Evacuation Hospital account (citing Yank, British ed., July 30, 1944)"
SC = "U.S. Army Signal Corps caption, ETO HQ 44 6419, July 2, 1944"
GEN = "Geneva Convention on the Wounded and Sick, July 27, 1929 · Bevans, vol. 2 · Library of Congress"
N_TAG = "Stand-in · Army ambulances and aid in Normandy, 1944 · from Medical Service in the Invasion of Normandy (War Dept.)"
C_TAG = "Stand-in · the 128th Evacuation Hospital, Normandy, June 1944 · Army film"
CP_TAG = "German prisoners at work at the 128th Evacuation Hospital, June 1944 · Army film"
H_TAG = "Stand-in · American Army nurses and medics set up a hospital, Normandy, July 1944 · Army film"
E_TAG = "Stand-in · an evacuation hospital at work · from The Evacuation Hospital (War Dept., 1945)"
P_TAG = "German prisoners, Cherbourg, June 28, 1944 · Army film"
D_TAG = "Cherbourg after the battle, June 27, 1944 · Navy film"
HB_TAG = "The wrecked port of Cherbourg, June 29 – July 1, 1944 · Army film"
WC = "Wikimedia Commons"
P = [
    # 0 the ambulances
    [("On", "N", T(9, 59.1)), ("@", "On the second of July", N_TAG),
     ("#", "On the second of July", None, {"type": "Slug", "title": "July 2, 1944", "subtitle": "Normandy · toward the front line"}),
     ("They were prisoners", "C", T(1, 13.4)), ("@", "They were prisoners", C_TAG)],
    # 1 the truce, briefly
    [("A short cease-fire", "N", 51.8), ("@", "A short cease-fire", N_TAG), ("One of the Americans", "H", T(2, 47.0)), ("@", "One of the Americans", H_TAG), ("At about six", "C", T(1, 58.1))],
    # 2 documented story
    [("Online there are many", "H", 47.3), ("@", "Online there are many", H_TAG), ("This is the documented story", "C", T(1, 19.8))],
    # 3 Cherbourg
    [("After D-Day", "HB", 2.0), ("@", "After D-Day", HB_TAG), ("American troops attacked", "D", T(3, 21.9)), ("@", "American troops attacked", D_TAG), ("Four days later", "D", T(5, 24.3))],
    # 4 the arsenal
    [("The arsenal held out", "D", T(3, 46.4)), ("Before they gave up", "HB", 17.8), ("@", "Before they gave up", HB_TAG), ("It would be weeks", "HB", 45.5)],
    # 5 the prisoners
    [("Tens of thousands", "P", 8.4), ("@", "Tens of thousands", P_TAG), ("And in an underground hospital", "D", T(5, 48.7)),
     ("#", "An Army photographer's caption", None, {"type": "LedgerQuote", "file": "FILE 01 — THE CAPTION", "head": "Signal Corps, July 2, 1944",
        "before": "", "key": "The first German Army nurses to fall into American hands,", "after": " captured in an underground hospital in a cave near Cherbourg.",
        "who": "U.S. Army Signal Corps photo caption", "source": SC})],
    # 6 Red Cross and navy
    [("Some of them were nurses", "N", T(11, 13.1)), ("@", "Some of them were nurses", N_TAG), ("The Allied papers", "D", T(4, 23.1)), ("@", "The Allied papers", D_TAG)],
    # 7 the treaty
    [("The question was", "N", T(11, 27.9)), ("@", "The question was", N_TAG),
     ("#", "The answer was in a treaty", None, {"type": "Slug", "title": "July 27, 1929", "subtitle": "Geneva · the wounded and sick of armies in the field"}),
     ("It protected the wounded", "N", T(5, 18.0))],
    # 8 article 9
    [("Its ninth article", "N", T(5, 18.0)),
     ("#", "Its ninth article", None, {"type": "LedgerDocument", "file": "FILE 02 — ARTICLE 9", "head": "Captured medical staff", "source": GEN,
        "spans": [{"doc": "doc_art9", "say": "If they fall into the hands of the enemy they shall not be treated as prisoners of war"}]})],
    # 9 article 12
    [("Its twelfth article", "N", T(11, 27.9)),
     ("#", "Its twelfth article", None, {"type": "LedgerDocument", "file": "FILE 03 — ARTICLE 12", "head": "Sent back", "source": GEN,
        "spans": [{"doc": "doc_art12", "say": "They shall be sent back to the belligerent to whose service they are attached as soon as a way is open for their return and military exigencies permit"}]})],
    # 10 until then
    [("Until then", "C", 54.3), ("@", "Until then", CP_TAG), ("Red Cross nurses were covered", "N", T(11, 13.1))],
    # 11 the 45th Evac
    [("On the second of July nine", "C", 47.9), ("@", "On the second of July nine", C_TAG),
     ("#", "On the second of July nine", None, {"type": "Slug", "title": "45th Evacuation Hospital", "subtitle": "Near La Cambe, Normandy · July 2, 1944"}),
     ("They did not know", "C", T(1, 26.2)), ("According to the hospital's account", "C", T(1, 38.9))],
    # 12 the tour
    [("Before they left", "E", T(5, 25.1)), ("@", "Before they left", E_TAG), ("They talked to German patients", "E", T(7, 7.1)), ("What they wanted to know", "E", T(7, 45.3))],
    # 13 the hope
    [("The American staff", "E", T(10, 43.8)), ("@", "The American staff", E_TAG)],
    # 14 subscribe (midpoint)
    [("If you want more", "C", T(1, 45.3)), ("@", "If you want more", C_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 15 Balleroy
    [("Then they waited", "C", T(1, 13.4)), ("@", "Then they waited", C_TAG),
     ("#", "Closed ambulances took them", None, {"type": "Slug", "title": "Balleroy, Normandy", "subtitle": "About two hours' wait · July 2, 1944"}),
     ("There they waited", "H", 9.5), ("@", "There they waited", H_TAG)],
    # 16 the three officers
    [("The cease-fire was agreed", "H", T(2, 34.4)), ("@", "The cease-fire was agreed", H_TAG),
     ("#", "The account names three officers", None, {"type": "LedgerTimeline", "file": "FILE 04 — THE TRUCE", "head": "Agreed by radio, July 2, 1944",
        "rows": [{"date": "U.S. ARMY", "text": "Capt. Fred Ghercke, POW Interrogation Team No. 24"},
                 {"date": "U.S. ARMY", "text": "Capt. Quentin Roosevelt, 1st Infantry Division"},
                 {"date": "GERMAN ARMY", "text": "Maj. F. Heeren, reconnaissance battalion, 2nd Panzer Division"},
                 {"date": "ABOUT 1800 HOURS", "text": "Through the lines at Caumont"}],
        "source": MED})],
    # 17 the photo at Balleroy
    [("An Army photographer was at", "C", T(1, 51.7)), ("@", "An Army photographer was at", C_TAG), ("At about six in the evening the women", "N", T(9, 59.1)), ("@", "At about six in the evening the women", N_TAG)],
    # 18 Quentin
    [("Quentin Roosevelt was twenty-four", "H", T(2, 47.0)), ("@", "Quentin Roosevelt was twenty-four", H_TAG), ("On D-Day he had landed", "N", T(4, 4.1)), ("@", "On D-Day he had landed", "Normandy beach, June 1944 · from Medical Service in the Invasion of Normandy (War Dept.)")],
    # 19 his father
    [("His father General", "N", T(3, 4.9)), ("Ten days after the truce", "H", 3.2), ("@", "Ten days after the truce", H_TAG)],
    # 20 the funeral
    [("Three days later", "H", 22.1), ("Quentin survived the war", "N", T(12, 41.8)), ("@", "Quentin survived the war", "A transport plane, 1944 · from Medical Service in the Invasion of Normandy (War Dept.)")],
    # 21 the second crossing
    [("A week after the first", "N", T(11, 57.4)), ("@", "A week after the first", N_TAG),
     ("On the ninth of July", "C", T(1, 19.8)), ("Sixteen German nurses", "H", 28.4), ("#", "On the ninth of July", None, {"type": "Slug", "title": "July 9, 1944", "subtitle": "The second crossing · Balleroy to Caumont"})],
    # 22 the MP
    [("An Army photo dated", "P", T(1, 54.7)), ("@", "An Army photo dated", "Stand-in · an American MP, Cherbourg, June 1944 · Army film")],
    # 23 the papers
    [("The story reached the papers", "D", T(5, 36.5)), ("@", "The story reached the papers", D_TAG),
     ("#", "Yank the Army's own", None, {"type": "LedgerTimeline", "file": "FILE 05 — THE RECORD", "head": "What was published, and when",
        "rows": [{"date": "JULY 2 & 9, 1944", "text": "Two crossings, sixteen women"},
                 {"date": "JULY 30, 1944", "text": "Yank, British edition, tells the story"},
                 {"date": "MAY 14, 1945", "text": "A Signal Corps caption cleared without restriction"}],
        "source": f"{MED}; {SC}"})],
    # 24 what is left
    [("What the sixteen women", "H", 34.7), ("@", "What the sixteen women", H_TAG)],
    # 25 the rule held
    [("The rule they were sent", "C", 47.9), ("@", "The rule they were sent", C_TAG), ("In a war that broke", "N", T(9, 59.1))],
    # 26 comment ask
    [("If your family", "H", T(2, 55.0)), ("@", "If your family", H_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "A nurse in your family's war story?", "subtitle": "Either side · tell us in the comments"})],
    # 27 Caumont today
    [("Co-mon was liberated", "N", T(9, 59.1)), ("The road from Bal-roy", "C", T(1, 13.4)), ("@", "The road from Bal-roy", C_TAG), ("long enough for sixteen", "N", T(11, 57.4))],
]

PHOTOS = [
    (2, "This is the documented story", None, "nurses_balleroy.jpg", "02", "Balleroy, July 2, 1944", "German nurses and navy auxiliaries with American soldiers, before the crossing", f"U.S. Army Signal Corps · via PhotosNormandie · CC BY-SA 2.0 · {WC}", {}),
    (5, "Tens of thousands", None, "cherbourg_prisoners.jpg", "05", "Cherbourg, 1944", "German prisoners after the city fell", f"U.S. Army · public domain · {WC}", {}),
    (12, "They saw its supplies", None, "evac_nurse_1944.jpg", "12", "An evacuation hospital", "Normandy, July 5, 1944: Lt. Gertrude A. Nolan, Army nurse, with Sgt. Charles A. Comar", f"U.S. Army Signal Corps SC 191000 · public domain · {WC}", {}),
    (17, "One of his pictures shows", None, "nurses_balleroy.jpg", "17", "The photograph", "An American ambulance, four of the women, and GIs · Balleroy, July 2, 1944", f"U.S. Army Signal Corps · via PhotosNormandie · CC BY-SA 2.0 · {WC}", {}),
    (18, "He was the grandson", None, "roosevelt_family_1925.jpg", "18", "The Roosevelts, 1925", "Theodore Roosevelt Jr. with his family", f"Bain News Service · Library of Congress · public domain · {WC}", {}),
    (20, "Three days later", None, "quentin_funeral.jpg", "20", "Capt. Quentin Roosevelt", "At his father's funeral, Sainte-Mère-Église, July 15, 1944 (left)", f"U.S. Army Signal Corps SC 191974 · public domain · {WC}", {}),
    (27, "Today a memorial", None, "caumont_memorial.jpg", "27", "Caumont-l'Éventé", "The memorial to the liberation, June 13, 1944", f"Dave osm · CC BY-SA 4.0 · {WC}", {}),
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
