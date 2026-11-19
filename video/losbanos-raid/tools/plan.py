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
    "LBR": ("losbanos_rescue_1945", 1), "LBC": ("losbanos_camp_feb1945", 1), "BIL": ("losbanos_bilibid_1945", 1),
    "JMP": ("airborne_jump_lipa_1945", 1), "COR": ("paratroop_corregidor_1945", 1), "STI": ("santo_tomas_internees_1945", 1),
    "STN": ("santo_tomas_newsreel_1945", 1), "TRV": ("philippines_travelogue_1940s", 0.85), "INT": ("internee_interviews_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
HEN = "Bruce Henderson, Rescue at Los Baños (2015)"
ROT = "Gordon L. Rottman, The Los Baños Prison Camp Raid (Osprey, 2010)"
FL48 = "E. M. Flanagan, The Angels: 11th Airborne Division (1948)"
TRIAL = "U.S. v. Sadaaki Konishi, Manila 1946–47 (record quoted in Henderson 2015)"
LBR_TAG = "Los Baños, 23 February 1945 · U.S. Army Air Forces film (NARA CS-3274)"
LBRB_TAG = "Freed Los Baños internees, New Bilibid, 23 Feb 1945 · AAF film (NARA CS-3274)"
LBC_TAG = "Los Baños, 23 February 1945 · U.S. Army Signal Corps film (NARA 111-ADC-3487)"
BIL_TAG = "Freed Los Baños internees, March 1945 · Signal Corps film (111-ADC-3616)"
JMP_TAG = "Stand-in · 11th Airborne paratroopers, Luzon, May 1945 · Signal Corps film"
COR_TAG = "Stand-in · paratroopers drop on Corregidor, 16 Feb 1945 · Signal Corps film"
STI_TAG = "Stand-in · a freed internee, Santo Tomas, Manila, Feb 1945 · Signal Corps film"
STN_TAG = "Santo Tomas internment camp, Manila, February 1945 · newsreel"
TRV_TAG = "Manila before the war · Peoples of the Philippines (Canadian Pacific)"
TRVS_TAG = "Stand-in · Luzon farmland · Peoples of the Philippines (Canadian Pacific)"
MNL_TAG = "Manila from the air, February 1945 · AAF film (NARA CS-3274)"
AIR_TAG = "Luzon from the air, February 1945 · AAF film (NARA CS-3274)"
INT_TAG = "Stand-in · freed prisoners and internees, 1945 · War Department film (BPR 1083)"
BAN_TAG = "Stand-in · a banca on Laguna de Bay, 23 Feb 1945 · Signal Corps film"
BIB_TAG = "New Bilibid Prison, Muntinlupa, 1945 · AAF film (NARA CS-3274)"


def LQ(file, head, key, who, source, before="", after=""):
    return {"type": "LedgerQuote", "file": file, "head": head, "before": before, "key": key, "after": after, "who": who, "source": source}


def HL(kicker, before, accent, at, source, after=""):
    return {"type": "Headline", "kicker": kicker, "before": before, "accent": accent, "after": after, "at": at, "source": source}


def TL(file, head, rows, source):
    return {"type": "LedgerTimeline", "file": file, "head": head, "rows": [{"date": a, "text": b} for a, b in rows], "source": source}


def BARS(file, head, bars, mx, source):
    return {"type": "LedgerBars", "file": file, "head": head, "bars": [{"label": a, "value": b, "figure": c, "note": d} for a, b, c, d in bars], "max": mx, "source": source}


def SLUG(title, sub):
    return {"type": "Slug", "title": title, "subtitle": sub}


def QC(bg, lines, by, by_at, portrait=None):
    c = {"type": "QuoteCard", "bg": bg, "lines": [{"text": a, "at": b} for a, b in lines], "by": by, "byAt": by_at}
    if portrait:
        c["portrait"] = portrait
    return c


def DESK(page, aspect, shots, credit):
    return {"type": "DocDesk", "page": page, "aspect": aspect, "desk": "stills/desk.jpg", "credit": credit,
            "shots": [{"t": t, "kind": k, "args": a} for t, k, a in shots]}


LB = [121.243, 14.170]   # Los Baños camp (UP College of Agriculture)
MNL = [120.984, 14.599]  # Manila
PAR = [121.019, 14.479]  # Parañaque (11th Airborne HQ)

# reconstruction of the exercise field / camp (ground world, 3000 x 1500, surface 820)
FIELD = {"type": "Section", "world": "ground", "W": 3000, "H": 1500, "surface": 820,
         "date": "Los Baños · 23 February 1945, 6:45 a.m.", "place": "Reconstruction · from Army reports and internee accounts",
         "cam": [{"t": 0, "x": 1500, "y": 760, "z": 0.75}, {"t": 7, "x": 1450, "y": 760, "z": 0.95}, {"t": 16, "x": 1400, "y": 780, "z": 1.1}],
         "items": [{"kind": "hut", "x": 420, "y": 820, "w": 460, "label": "Arms room", "labelAt": "Their rifles are locked", "labelTo": 16},
                   {"kind": "hut", "x": 2450, "y": 820, "w": 520, "label": "Hospital", "labelAt": 0.6, "labelTo": 5},
                   {"kind": "fence", "x": 2900, "y": 820, "w": 300}, {"kind": "tower", "x": 120, "y": 820},
                   {"kind": "man", "x": 1050, "y": 820}, {"kind": "man", "x": 1200, "y": 820}, {"kind": "man", "x": 1350, "y": 820, "label": "Off-duty guards", "labelAt": "the off-duty Japanese guards", "labelTo": 16},
                   {"kind": "man", "x": 1500, "y": 820}, {"kind": "man", "x": 1650, "y": 820}, {"kind": "man", "x": 1800, "y": 820}],
         "pills": [{"t0": "loincloths and sandals", "t1": "Their rifles are locked", "text": "Loincloths and sandals"},
                   {"t0": "Their rifles are locked", "t1": 30, "text": "Rifles locked in the arms room", "y": 230}],
         "source": f"{HEN}; {ROT}"}

ESCAPE = {"type": "Section", "world": "ground", "W": 3000, "H": 1500, "surface": 820,
          "date": "Los Baños · 18 February 1945, 9 p.m.", "place": "Reconstruction · from Ben Edwards' account (Henderson 2015)",
          "cam": [{"t": 0, "x": 1300, "y": 760, "z": 0.8}, {"t": "They walked toward", "x": 1700, "y": 760, "z": 0.95}, {"t": "A manned guard post", "x": 2150, "y": 780, "z": 1.15}],
          "items": [{"kind": "hut", "x": 450, "y": 820, "w": 480, "label": "Barracks", "labelAt": 0.5, "labelTo": "They walked toward"},
                    {"kind": "hut", "x": 1650, "y": 820, "w": 460, "label": "Hospital", "labelAt": "toward the hospital", "labelTo": "then crawled under"},
                    {"kind": "fence", "x": 2250, "y": 820, "w": 500}, {"kind": "tower", "x": 2700, "y": 820, "label": "Guard post · about 40 ft", "labelAt": "A manned guard post", "labelTo": 30},
                    {"kind": "man", "x": 600, "y": 820, "pose": "walk", "move": [{"t": "At nine at night", "x": 600}, {"t": "toward the hospital", "x": 1450}, {"t": "then crawled under", "x": 1950}]},
                    {"kind": "man", "x": 680, "y": 820, "pose": "walk", "label": "Miles, 'ill'", "labelAt": "Miles limped", "labelTo": "then crawled under",
                     "move": [{"t": "At nine at night", "x": 680}, {"t": "toward the hospital", "x": 1530}, {"t": "then crawled under", "x": 2030}]},
                    {"kind": "man", "x": 760, "y": 820, "pose": "walk", "move": [{"t": "At nine at night", "x": 760}, {"t": "toward the hospital", "x": 1610}, {"t": "then crawled under", "x": 2110}]}],
          "pills": [{"t0": "carrying a lantern", "t1": "then crawled under", "text": "Out the door with a lantern"},
                    {"t0": "then crawled under", "t1": 30, "text": "Under the wire behind the hospital", "y": 230}],
          "source": HEN}

P = [
    # 0 quarter to seven (reconstruction)
    [("It is a quarter", "LBC", T(4, 18.0)), ("#", "It is a quarter", None, FIELD)],
    # 1 Dorothy Still (quote)
    [("In the camp hospital", "INT", T(0, 25.0)), ("@", "In the camp hospital", INT_TAG), ("Her name is", "INT", T(3, 15.0)),
     ("#", "She later wrote", None, QC("stills/navy_nurses_b_1945.jpg", [("We could do calisthenics too,", "We could do calisthenics"), ("if we were as well fed", "if we were as well"), ("as they are.", "as they are")],
        "Navy nurse Dorothy Still, 23 Feb 1945 · from her memoir", "as they are"))],
    # 2 smoke, engines, parachutes
    [("A patient beside her", "LBC", T(3, 40.0)), ("@", "A patient beside her", "Smoke over Los Baños, 23 February 1945 · Signal Corps film (111-ADC-3487)"),
     ("Then comes the sound", "JMP", T(3, 37.0)), ("@", "Then comes the sound", JMP_TAG), ("Nine American transport planes", "COR", T(6, 22.0)),
     ("@", "Nine American transport planes", COR_TAG), ("And the sky", "JMP", T(4, 39.0))],
    # 3 not luck
    [("The guards have been caught", "JMP", T(8, 12.0)), ("That is not luck", "LBC", T(4, 19.0)), ("@", "That is not luck", LBC_TAG),
     ("#", "Someone told the Americans", None, SLUG("February 23, 1945 · 7:00 a.m.", "Los Baños internment camp, Luzon"))],
    # 4 two thousand names (icon count)
    [("This is the true story", "LBR", T(0, 51.0)), ("@", "This is the true story", LBR_TAG),
     ("#", "Inside the camp were", None, {"type": "IconCount", "icon": "man", "total": 2147, "label": "Names on the camp roll, February 1945",
        "accent": "camp roll", "highlight": {"n": 11, "label": "Navy nurses", "accent": "nurses", "at": "eleven Navy nurses"},
        "file": "FILE 01 — THE ROLL", "source": f"Camp roll typed by internee Carol Terry ({HEN}); War Dept GO 71, 1945"})],
    # 5 what the version leaves out
    [("The version you may", "LBR", T(1, 2.0)), ("@", "The version you may", LBR_TAG), ("The documented story", "LBR", T(1, 25.0)),
     ("The man who really ran", "LBC", T(4, 9.0)), ("And the town", "TRV", T(10, 56.0)), ("@", "And the town", TRVS_TAG)],
    # 6 sources
    [("Some of it comes", "BIL", T(2, 31.0)), ("@", "Some of it comes", BIL_TAG), ("When a scene rests", "BIL", T(7, 33.0)),
     ("#", "When a scene rests", None, HL("HOW THIS STORY IS TOLD", "When a scene rests on one memory,", "we will tell you whose", "we will tell you whose", "WWII Frontlines"))],
    # 7 Manila 1942
    [("The story starts", "TRV", T(1, 13.0)), ("@", "The story starts", TRV_TAG), ("#", "The story starts", None, SLUG("January 1942 · Manila", "The Japanese occupation begins")),
     ("and thousands of American", "STN", T(0, 4.0)), ("@", "and thousands of American", STN_TAG)],
    # 8 to Los Baños (map)
    [("By nineteen forty-three", "STN", T(0, 56.0)),
     ("#", "In May, the Japanese", None, {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [122, 13], "scale": 7}, {"t": "south to build", "center": [121.1, 14.4], "scale": 110}],
        "fills": [{"ids": ["608"], "color": "ally", "stroke": "allyStroke", "at": 0.2, "label": "Luzon", "labelAt": [121.0, 16.2]}],
        "pins": [{"ll": MNL, "label": "Manila · Santo Tomas", "at": 0.8}, {"ll": LB, "label": "Los Baños", "at": "The site was the College"},
                 {"ll": [121.2, 14.13], "label": "Mount Makiling", "at": "green slopes", "color": "amber"},
                 {"ll": [121.25, 14.38], "label": "Laguna de Bay", "at": "a wide lake", "color": "west"}],
        "arcs": [{"from": MNL, "to": LB, "at": "south to build", "style": "dashed", "color": "red", "loft": 0.05, "draw": 30}],
        "cards": [{"at": "eight hundred able-bodied men", "kicker": "May 1943", "body": "800 men sent from Santo Tomas to build a second camp", "accent": "red"}],
        "footer": "Route generalised", "year": {"at": 0.1, "year": "1943", "sub": "Santo Tomas to Los Baños"}})],
    # 9 Ben Edwards
    [("One of the eight hundred", "LBR", T(13, 18.0)), ("@", "One of the eight hundred", LBRB_TAG), ("Remember his name", "LBR", T(12, 44.0)),
     ("women and children", "LBR", T(15, 56.0)), ("and by early", "LBR", T(23, 5.0))],
    # 10 Vatican City / Hell's Half-Acre
    [("About three hundred Catholic", "LBR", T(21, 46.0)), ("@", "About three hundred Catholic", LBRB_TAG), ("The rest of the camp", "LBR", T(20, 5.0)),
     ("#", "The rest of the camp", None, HL("THE INTERNEES' OWN NAMES", "Vatican City  ·", "Hell's Half-Acre", "Hell's Half-Acre", "Jeremy C. Holm, 511pir.com (2020)"))],
    # 11 nurses, Buckles
    [("And there was Frank", "LBR", T(21, 24.0)), ("@", "And there was Frank", LBRB_TAG), ("He would lose", "LBR", T(19, 42.0))],
    # 12 lenient, then July 1944
    [("According to the military", "LBC", T(4, 9.0)), ("@", "According to the military", LBC_TAG),
     ("#", "Then, in July", None, SLUG("July 1944 · Los Baños", "A new commandant, and a new supply officer"))],
    # 13 Iwanaka
    [("The commandant was Major", "LBC", T(4, 28.0)), ("@", "The commandant was Major", "Stand-in · an internee in a pith helmet, Los Baños, Feb 1945 · Signal Corps film"),
     ("He was never known", "LBC", T(4, 19.0))],
    # 14 Konishi (who's who)
    [("#", "His name was", None, TL("FILE 02 — WHO RAN THE CAMP", "Los Baños, from July 1944",
        [("Commandant", "Maj. Iwanaka · geraniums, watercolors, haiku (internees)"), ("Supply officer", "W.O. Sadaaki Konishi, 28, a farmer from Fukuoka"),
         ("In practice", "Iwanaka never overruled Konishi"), ("Internee's view", "“a sadist and terribly mean” — Robert Wheeler")],
        f"{HEN}; {ROT}; Holm (2020)"))],
    # 15 rice sacks
    [("Internees told the historian", "LBR", T(14, 48.0)), ("@", "Internees told the historian", "Stand-in · supplies unloaded, New Bilibid, 1945 · AAF film (CS-3274)"),
     ("Then he ordered them", "LBR", T(14, 59.0)), ("What is documented", "LBR", T(26, 6.0))],
    # 16 Nance's count (bars)
    [("The camp doctor", "INT", T(36, 36.0)), ("@", "The camp doctor", INT_TAG),
     ("#", "In October", None, BARS("FILE 03 — THE CAMP DOCTOR", "Calories a day, October 1944",
        [("Internee ration (Dr. Nance)", 881, "881", "a fall of almost two thirds in a month"), ("Guards (internees' estimate)", 3500, "3,000–4,000", "")], 4000, HEN))],
    # 17 THE CAMP URGENTLY NEEDS MORE FOOD + grams
    [("#", "The camp urgently needs", "After the war", HL("DR. DANA NANCE TO THE COMMANDANT · 1 NOV 1944", "", "THE CAMP URGENTLY NEEDS MORE FOOD.", "urgently needs more food", HEN)),
     ("#", "After the war", None, BARS("FILE 03 — ARMY WAR CRIMES FINDINGS", "Food per person, per day",
        [("September 1944", 400, "400 g", "about 14 oz"), ("February 1945", 150, "150 g or less", "about 5 oz")], 400, TRIAL))],
    # 18 eating dirt / keep off the grass
    [("At Thanksgiving", "INT", T(37, 18.0)), ("@", "At Thanksgiving", INT_TAG),
     ("#", "They remembered", "Someone put up a sign", QC("stills/grave_hell_1945.jpg", [("Before I'm done,", "Before I'm done"), ("you'll be eating dirt.", "eating dirt")],
        "W.O. Sadaaki Konishi, Thanksgiving 1944 · as internees recalled it", "eating dirt")),
     ("#", "Someone put up a sign", None, HL("A SIGN IN THE CAMP · 1944", "KEEP OFF THE GRASS.", "WE EAT IT.", "We eat it", HEN))],
    # 19 Nance to Konishi
    [("They did eat it", "STI", T(6, 11.0)), ("@", "They did eat it", STI_TAG),
     ("#", "In late November", None, LQ("FILE 03 — NOVEMBER 1944", "Dr. Dana Nance to Konishi", "deliberately adopting a starvation policy.",
        "Dr. Dana Nance · Konishi's reply: “Nothing can be done.”", HEN, before="If you fail to remedy this situation, it can only mean that you are "))],
    # 20 dying every week
    [("By the start of", "BIL", T(7, 33.0)), ("@", "By the start of", BIL_TAG), ("A girl named Sally", "LBR", T(16, 7.0)), ("@", "A girl named Sally", LBRB_TAG),
     ("Others collected recipes", "LBR", T(17, 49.0)),
     ("#", "said many years later", None, HL("SALLY BATEMAN MORGAN, INTERNEE · ORAL HISTORY, 2008", "Some people died", "with food under their beds", "with food under their beds", "National Museum of the Pacific War oral history (2008)"))],
    # 21 Freedom Week
    [("Then, in January", "STN", T(1, 2.0)), ("@", "Then, in January", "Stand-in · Santo Tomas internees, Manila, February 1945 · newsreel"),
     ("#", "The next morning", None, SLUG("January 7, 1945 · Los Baños", "The guards march away"))],
    # 22 flags, guards back, shoot on sight
    [("For one week", "STN", T(1, 32.0)), ("@", "For one week", "Stand-in · internees with an American flag, Santo Tomas, 1945 · newsreel"),
     ("American Navy fighter", "JMP", T(7, 10.0)), ("@", "American Navy fighter", "Stand-in · an American plane over Luzon, 1945 · Signal Corps film"),
     ("Then, on the fourteenth", "LBC", T(4, 19.0)),
     ("#", "And the commandant gave", None, HL("THE COMMANDANT'S ORDER · 14 JAN 1945", "Anyone outside the fence:", "shot on sight", "shot on sight", ROT))],
    # 23 Pat Hell (print)
    [("Hungry men kept slipping", "TRV", T(11, 25.0)), ("@", "Hungry men kept slipping", TRVS_TAG)],
    # 24 George Louis (print + caption on the desk)
    [("Eight days later", "LBC", T(4, 19.0)), ("@", "Eight days later", LBC_TAG),
     ("#", "The caption calls him", None, DESK("stills/caption_louis_1945_paper.png", 2.6481, [(0, "wide", [0.5, 0.4]), ("an American civilian", "glide", [0.3, 0.12, 0.6])],
        "Signal Corps caption SC 269119-R, 18 May 1945 · National Archives 111-SCA album 2895"))],
    # 25 trenches
    [("Around that time", "LBC", T(5, 7.0)), ("@", "Around that time", LBC_TAG), ("But a rumor spread", "LBC", T(4, 9.0))],
    # 26 guerrillas
    [("The internees were not", "TRV", T(10, 56.0)), ("@", "The internees were not", TRVS_TAG),
     ("#", "There were the Hunters", None, TL("FILE 04 — OUTSIDE THE WIRE", "Guerrilla groups around Los Baños",
        [("Hunters ROTC", "Founded 1942 by cadets and students"), ("PQOG", "President Quezon's Own Guerrillas"), ("Marking's", "Marking's Guerrillas"),
         ("Huks", "Hukbalahap · 48th Chinese Squadron")], "NHI marker, Los Baños (2005); Hunters ROTC (Wikipedia)"))],
    # 27 Ingles
    [("One of the leaders", "TRV", T(3, 10.0)), ("@", "One of the leaders", "Intramuros, Manila, before the war · Peoples of the Philippines (Canadian Pacific)"),
     ("In June", "LBR", T(3, 7.0)), ("@", "In June", BIB_TAG),
     ("#", "In June", None, SLUG("June 1944 · New Bilibid Prison", "The Hunters ROTC free Gustavo Ingles and fifty others"))],
    # 28 Freddy slips out
    [("On the twelfth", "LBC", T(4, 19.0)), ("@", "On the twelfth", LBC_TAG), ("The guerrillas wanted", "TRV", T(11, 54.0)), ("@", "The guerrillas wanted", TRVS_TAG)],
    # 29 the committee says no
    [("The answer was no", "INT", T(36, 40.0)), ("@", "The answer was no", INT_TAG),
     ("#", "And he asked", None, LQ("FILE 05 — THE COMMITTEE", "George Gray to Gustavo Ingles, February 1945", "Do you have any way to transport more than two thousand people",
        "George Gray, internee committee (as quoted by Henderson)", HEN, after=", some sick and feeble, out of enemy territory to U.S. lines?"))],
    # 30 twenty-five miles away
    [("They did not", "LBR", T(9, 43.0)), ("@", "They did not", MNL_TAG), ("Somebody would have", "LBR", T(10, 39.0))],
    # 31 three men
    [("On the night of the eighteenth", "TRV", T(10, 26.0)), ("@", "On the night of the eighteenth", "Stand-in · Luzon, 1940s · Peoples of the Philippines (Canadian Pacific)"),
     ("#", "One was Freddy", None, TL("FILE 06 — THE ESCAPE · 18 FEB 1945", "Three men under the wire",
        [("Pete Miles", "Engineer, a Texan in his early thirties"), ("Ben Edwards", "Pan Am mechanic"), ("Freddy Zervoulakos", "Greek-Filipino, about 20")], f"{HEN}; {ROT}"))],
    # 32 the lantern (reconstruction)
    [("Ben Edwards described", "LBC", T(4, 19.0)), ("#", "Ben Edwards described", None, ESCAPE)],
    # 33 tin can, banca
    [("Edwards kicked", "LBC", T(4, 9.0)), ("@", "Edwards kicked", LBC_TAG), ("The three men reached", "TRV", T(13, 21.0)), ("@", "The three men reached", TRVS_TAG),
     ("And the next morning", "LBC", T(3, 20.0)), ("@", "And the next morning", BAN_TAG)],
    # 34 Miles at headquarters (map)
    [("On the nineteenth", "JMP", T(0, 50.0)),
     ("#", "On the nineteenth", None, {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [121.1, 14.38], "scale": 160}],
        "fills": [{"ids": ["608"], "color": "ally", "stroke": "allyStroke", "at": 0.1}],
        "pins": [{"ll": PAR, "label": "11th Airborne HQ · Parañaque", "at": 0.6}, {"ll": LB, "label": "Los Baños camp", "at": 1.2, "color": "red"},
                 {"ll": MNL, "label": "Manila", "at": 0.8, "color": "west"}],
        "arcs": [{"from": [121.22, 14.2], "to": PAR, "at": 1.6, "style": "dashed", "color": "amber", "fromLabel": "Miles, by banca", "loft": 0.05, "draw": 40}],
        "cards": [{"at": "He marked the quarters", "kicker": "Pete Miles' map", "body": "Barracks, guard houses, sentries, pillboxes", "accent": "amber"},
                  {"at": "He even estimated", "kicker": "And", "body": "How many would need stretchers", "accent": "red"}],
        "footer": "Route generalised", "year": {"at": 0.1, "year": "19 FEB", "sub": "Pete Miles reaches the Americans"}})],
    # 35 quarter to seven (quote card)
    [("#", "Then Muller asked", None, QC("stills/co511_cp_1945.jpg",
        [("“Every morning?”", "Every morning"), ("“Yes, and always at the same time.”", "always at the same time"), ("“What time?”", "What time"),
         ("“They start exercising at a quarter to seven.”", "They start exercising")],
        "Lt. Col. Henry Muller and Pete Miles, 19 Feb 1945 · Muller's account (Henderson 2015)", "a quarter to seven"))],
    # 36 H-hour moved
    [("#", "Muller moved the attack", "The division's history said", HL("H-HOUR MOVED · 19 FEB 1945", "8:00 a.m.  →", "7:00 a.m.", "to seven", HEN)),
     ("The division's history said", "JMP", T(0, 58.0)), ("@", "The division's history said", JMP_TAG)],
    # 37 Swing (photo)
    [("The division's commander", "JMP", T(3, 46.0)), ("@", "The division's commander", JMP_TAG), ("So the plan", "JMP", T(1, 6.0))],
    # 38 four parts
    [("#", "It had four parts", None, TL("FILE 07 — THE PLAN", "Los Baños Force, 23 February 1945",
        [("1 · Recon", "About 30 men cross the lake with guerrillas"), ("2 · Air", "B Co., 511th PIR jumps from nine C-47s"),
         ("3 · Water", "1st Bn, 511th in 54 amtracs"), ("4 · Road", "Diversion with artillery and tank destroyers")], f"{FL48}; {ROT}"))],
    # 39 guerrillas (painting + Army map)
    [("The guerrillas, mostly men", "TRV", T(11, 54.0)), ("@", "The guerrillas, mostly men", TRVS_TAG)],
    # 40 8,000-15,000
    [("#", "Swing's staff estimated", None, HL("WITHIN FOUR HOURS' MARCH OF THE CAMP", "", "8,000–15,000 Japanese troops", "between eight thousand", FL48)),
     ("Henderson writes", "COR", T(2, 8.0)), ("@", "Henderson writes", COR_TAG)],
    # 41 subscribe
    [("We are about halfway", "LBR", T(1, 25.0)), ("@", "We are about halfway", LBR_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 42 scheduled for massacre
    [("On the twenty-first", "TRV", T(10, 56.0)), ("@", "On the twenty-first", TRVS_TAG),
     ("#", "radioed the Americans", None, HL("COL. ROMEO ESPINO, GUERRILLA RADIO MESSAGE · 21 FEB 1945", "Los Baños", "scheduled for massacre", "scheduled for massacre", ROT)),
     ("But nobody could", "LBC", T(4, 19.0))],
    # 43 bancas, the schoolhouse
    [("That night, in a storm", "LBC", T(3, 21.0)), ("@", "That night, in a storm", BAN_TAG),
     ("#", "That night, in a storm", None, SLUG("February 21, 1945 · Laguna de Bay", "The reconnaissance platoon crosses by banca")),
     ("On the far shore", "LBC", T(3, 30.0)), ("Edwards drew the camp", "TRV", T(13, 21.0)), ("@", "Edwards drew the camp", TRVS_TAG)],
    # 44 three feet
    [("On the night of the twenty-second", "TRV", T(11, 25.0)), ("@", "On the night of the twenty-second", TRVS_TAG),
     ("#", "Some of them", None, HL("THE DIVISION HISTORY, 1948", "Some scouts lay", "three feet", "three feet", FL48, after=" from their sentry"))],
    # 45 Nichols Field, midnight report
    [("At Nichols Field", "JMP", T(3, 37.0)), ("@", "At Nichols Field", JMP_TAG), ("And at about midnight", "JMP", T(3, 46.0)),
     ("Night fighter pilots", "LBR", T(6, 19.0)), ("@", "Night fighter pilots", AIR_TAG)],
    # 46 Swing ignores it
    [("If it was true", "JMP", T(4, 4.0)), ("@", "If it was true", JMP_TAG), ("He did not pass", "LBR", T(1, 48.0)), ("@", "He did not pass", LBR_TAG)],
    # 47 the morning (timeline)
    [("#", "At a quarter past five", None, TL("FILE 08 — 23 FEBRUARY 1945", "The morning of the raid",
        [("05:15", "54 amtracs head out onto the lake"), ("06:00–06:30", "Nine C-47s take off"), ("06:45", "Guards begin their exercises"),
         ("06:58", "Smoke on the drop zone"), ("07:00", "B Company jumps · amtracs land")], f"{ROT}; {FL48}"))],
    # 48 a sentry fires
    [("A few minutes before", "JMP", T(4, 5.0)), ("@", "A few minutes before", JMP_TAG), ("A Filipino officer", "COR", T(6, 46.0)), ("@", "A Filipino officer", COR_TAG),
     ("At two minutes to seven", "JMP", T(4, 13.0)), ("@", "At two minutes to seven", JMP_TAG)],
    # 49 seven o'clock: the jump
    [("At seven o'clock", "JMP", T(4, 40.0)), ("@", "At seven o'clock", JMP_TAG), ("It belonged to", "JMP", T(4, 48.0)), ("In less than a minute", "JMP", T(8, 21.0))],
    # 50 amtracs land; the report page on the desk
    [("At the same moment", "LBR", T(0, 18.0)), ("@", "At the same moment", LBR_TAG), ("and the first American", "LBR", T(2, 11.0)),
     ("#", "On the exercise field", None, DESK("stills/report_p1_1945_paper.png", 0.7268,
        [(0, "wide", [0.5, 0.45]), ("the guards ran", "glide", [0.475, 0.2, 0.75])],
        "188th Glider Infantry narrative history, 1945 · NARA 111-SCA album 2895"))],
    # 51 paratrooper boots (quote)
    [("Inside the barracks", "LBR", T(15, 56.0)), ("@", "Inside the barracks", LBRB_TAG),
     ("#", "Sally remembered what", None, QC("stills/bowie_family_1945.jpg", [("I looked out and saw paratrooper boots.", "I looked out"), ("It was the most beautiful sight", "It was the most"), ("you can ever imagine.", "you can ever imagine")],
        "Sally Bateman Morgan, internee, about 13 · oral history, 2008", "you can ever imagine"))],
    # 52 Sorry, sister
    [("A young internee named Jerry", "LBC", T(4, 9.0)), ("@", "A young internee named Jerry", LBC_TAG), ("In the women's barracks", "LBC", T(4, 48.0)),
     ("#", "He said", None, HL("23 FEBRUARY 1945 · THE WOMEN'S BARRACKS", "“Sorry, sister.", "Army paratroopers.”", "Army paratroopers", HEN))],
    # 53 the amtracs arrive
    [("Within about fifteen minutes", "LBC", T(5, 17.0)), ("@", "Within about fifteen minutes", LBC_TAG), ("Then the amtracs arrived", "LBC", T(6, 6.0)),
     ("The fighting in the camp", "LBC", T(5, 27.0)), ("Now the hardest part", "LBC", T(5, 46.0))],
    # 54 five minutes (barracks burning)
    [("But the internees did not", "LBC", T(4, 38.0)), ("@", "But the internees did not", LBC_TAG), ("So they set the barracks", "LBC", T(3, 40.0)),
     ("#", "An internee named Carol", None, HL("CAROL TALBOT, INTERNEE", "“Lady, you've got", "five minutes", "five minutes", "Jeremy C. Holm, 511pir.com (2020)", after=" to get into an amtrac.”"))],
    # 55 baby Lois, stretchers
    [("Among the people carried", "LBR", T(13, 52.0)), ("@", "Among the people carried", LBRB_TAG), ("The sick and the old", "LBC", T(7, 4.0)), ("@", "The sick and the old", LBC_TAG),
     ("By about a quarter to nine", "LBC", T(6, 55.0))],
    # 56 across the lake; the after-action report on the desk
    [("The battalion commander", "LBC", T(7, 24.0)), ("@", "The battalion commander", LBC_TAG), ("The first lift", "LBR", T(1, 59.0)), ("@", "The first lift", LBR_TAG),
     ("The others waited", "LBC", T(7, 34.0)), ("And at five o'clock", "LBR", T(3, 7.0)),
     ("#", "And at five o'clock", None, DESK("stills/report_p2_1945_paper.png", 0.7463,
        [(0, "wide", [0.5, 0.42]), ("were safe behind", "glide", [0.37, 0.2, 0.75]), ("with one internee", "glide", [0.5, 0.2, 0.75])],
        "11th Airborne Division report after action, Luzon 1945 · NARA 111-SCA album 2895"))],
    # 57 the dead
    [("The price was paid", "COR", T(4, 57.0)), ("@", "The price was paid", COR_TAG),
     ("#", "In the diversion", None, TL("FILE 09 — THE DEAD, 23 FEBRUARY 1945", "Killed in the raid",
        [("U.S. Army", "Tank destroyer company captain + 2 men, Lecheria (diversion)"), ("Hunters ROTC", "Atanacio Castillo · Anselmo Soler"),
         ("Internees", "None killed · one lightly wounded")], f"{HEN}; {FL48}"))],
    # 58 Japanese dead
    [("How many Japanese died", "LBC", T(5, 46.0)), ("@", "How many Japanese died", LBC_TAG),
     ("#", "Reports in", None, BARS("FILE 09 — THE GARRISON", "Japanese guards killed: two counts",
        [("AP report, 24 Feb 1945", 243, "243", "“to the last man”"), ("Rottman, 2010", 75, "70–80", "in the camp")], 250, f"AP, 24 Feb 1945; {ROT}")),
     ("Two men in particular", "LBC", T(4, 19.0))],
    # 59 MacArthur (quote)
    [("#", "General Douglas MacArthur", None, QC("stills/macarthur_1945.jpg", [("Nothing could be more satisfying", "Nothing could be more"), ("to a soldier's heart than this rescue.", "to a soldier's heart"), ("God was certainly with us today.", "God was certainly")],
        "Gen. Douglas MacArthur, 23 February 1945", "with us today"))],
    # 60 front pages
    [("The next day", "LBR", T(24, 59.0)), ("@", "The next day", LBRB_TAG),
     ("#", "One paper in Ohio", None, HL("WASHINGTON C. H. RECORD-HERALD, OHIO · 24 FEB 1945", "“Yanks Free 2,146 More From … Prison", "and Break Iwo Stalemate”", "broken the stalemate", "AP, 24 Feb 1945 (front page)"))],
    # 61 Iwo Jima
    [("On the same morning", "COR", T(8, 35.0)), ("@", "On the same morning", "Stand-in · an island from the air, 1945 · Signal Corps film"),
     ("#", "On the same morning", None, SLUG("February 23, 1945 · Iwo Jima", "Mount Suribachi"))],
    # 62 the photo took over
    [("It became the most famous", "LBR", T(23, 5.0)), ("@", "It became the most famous", LBRB_TAG), ("It made the front pages", "LBR", T(25, 10.0))],
    # 63 the town (timeline of the killings)
    [("For the people of", "TRV", T(10, 56.0)), ("@", "For the people of", TRVS_TAG),
     ("#", "Army war crimes investigators", None, TL("FILE 10 — ARMY WAR CRIMES REPORT NO. 214", "Around Los Baños, 1945",
        [("21 Feb", "Tadlak: 65 killed from ten families"), ("22 Feb", "Maahas: 45 killed from five families"), ("23 Feb", "The raid"),
         ("27 Feb", "College church: 60+ sheltering, burned"), ("6 Mar", "Anos: 26 killed")], TRIAL))],
    # 64 Fujishige's order (quote)
    [("The Japanese commander", "TRV", T(11, 26.0)), ("@", "The Japanese commander", TRVS_TAG),
     ("#", "A captured order", "And after the Americans", QC("stills/xiv_corps_map_1945.jpg", [("Kill all American soldiers brutally.", "Kill all American"), ("Kill all Filipinos who oppose our Emperor.", "Kill all Filipinos")],
        "Captured order of Col. Fujishige's command · printed in The Angels (1948)", "our Emperor")),
     ("And after the Americans", "TRV", T(13, 22.0))],
    # 65 the church
    [("In the early hours", "TRV", T(14, 19.0)), ("@", "In the early hours", "Stand-in · Luzon · Peoples of the Philippines (Canadian Pacific)"),
     ("#", "More than sixty people", None, LQ("FILE 10 — REPORT NO. 214", "College grounds, Los Baños, 27 Feb 1945", "were immolated.",
        "U.S. Army War Crimes Report No. 214", TRIAL, before="More than sixty residents … took refuge in the Roman Catholic church on the college grounds… The remainder refused to leave the church and "))],
    # 66 the boy tied to his mother (quote)
    [("The next day", "TRV", T(13, 22.0)), ("@", "The next day", TRVS_TAG),
     ("#", "Among the bodies", None, QC("stills/grave_louis_1945.jpg", [("I heard him call, “Mama,”", "I heard him call"), ("and tell her he was hungry.", "and tell her")],
        "Fernando Bernardo, testimony at the Konishi trial, 1946", "he was hungry"))],
    # 67 the Ang family (quote + the caption on the desk)
    [("On the sixth of March", "TRV", T(10, 56.0)), ("@", "On the sixth of March", TRVS_TAG),
     ("#", "At the trial he said", "His grandparents", QC("stills/grave_hell_1945.jpg", [("I heard my sister whining,", "I heard my sister"), ("and I crawled out from under the dead bodies", "and I crawled out"), ("and dug her out.", "and dug her out")],
        "Ang Kim Ling, testimony at the Konishi trial, 1946", "and dug her out")),
     ("#", "In May, an Army photographer", None, DESK("stills/caption_ang_1945_paper.png", 3.6508, [(0, "wide", [0.5, 0.45]), ("he and his sister", "glide", [0.45, 0.12, 0.75])],
        "Signal Corps caption SC 210419, 19 May 1945 · National Archives 111-SCA album 2895"))],
    # 68 how many (bars)
    [("#", "How many people were killed", None, BARS("FILE 10 — THE DEAD AROUND LOS BAÑOS", "Estimates, 21 February – 6 March 1945",
        [("Acting mayor's estimate", 650, "600–700", "deposition, Konishi trial"), ("Other estimates", 1500, "1,500+", "Rottman; Wikipedia; Gaerlan")], 1500, f"{TRIAL}; {ROT}"))],
    # 69 revenge?
    [("Was it revenge", "TRV", T(11, 54.0)), ("@", "Was it revenge", TRVS_TAG),
     ("#", "Ben Edwards, who escaped", None, HL("BEN EDWARDS, FORMER INTERNEE", "The atrocities were", "not the direct result", "did not believe", "Donald J. Roberts II, Military Heritage (2001)", after=" of the liberation"))],
    # 70 Rottman
    [("#", "Guerrilla leaders later", None, HL("GORDON ROTTMAN, 2010", "Security after the raid was", "inadequately addressed by all parties", "inadequately addressed", ROT))],
    # 71 the ravine
    [("And Koh-nee-shee", "TRV", T(13, 22.0)), ("@", "And Koh-nee-shee", "Stand-in · Luzon hillside · Peoples of the Philippines (Canadian Pacific)"),
     ("#", "he said later", None, LQ("FILE 11 — SWORN STATEMENT, 28 NOV 1945", "W.O. Sadaaki Konishi on 23 February 1945", "I was still in bed at that time,",
        "Sadaaki Konishi to Army war crimes investigators", HEN, after=" and then I heard that paratroops had landed."))],
    # 72 "Yes, actually it caused deaths" (quote)
    [("In September", "LBR", T(10, 16.0)), ("@", "In September", MNL_TAG), ("In November", "LBR", T(10, 50.0)),
     ("#", "Then they asked him", None, QC("stills/grave_louis_1945.jpg", [("“Did the order cause starvation?”", "Then they asked him"), ("“Yes, actually it caused deaths.”", "Yes, actually")],
        "Sadaaki Konishi, sworn statement, 28 November 1945", "caused deaths"))],
    # 73 the trial
    [("His trial opened", "LBR", T(10, 39.0)), ("@", "His trial opened", MNL_TAG),
     ("#", "His trial opened", None, SLUG("November 1946 · Manila", "U.S. Military Commission: United States v. Sadaaki Konishi")),
     ("The witnesses came", "TRV", T(10, 56.0)), ("@", "The witnesses came", TRVS_TAG)],
    # 74 the verdict
    [("#", "On the fifteenth of January", None, TL("FILE 11 — VERDICT, 15 JANUARY 1947", "U.S. v. Sadaaki Konishi",
        [("Guilty", "Killing of George Louis"), ("Guilty", "Killing of a child tied to his mother"), ("Guilty", "Attack on the Ang children"),
         ("Guilty", "61 civilians killed, 6 March 1945"), ("Guilty", "Aiding a policy of starvation"), ("Sentence", "Death by hanging")], TRIAL))],
    # 75 Iwanaka, Fujishige
    [("The commandant, Major", "LBR", T(11, 30.0)), ("@", "The commandant, Major", MNL_TAG), ("Colonel Foo-jee-shee-geh was", "LBR", T(11, 2.0))],
    # 76 the wrong date
    [("For more than thirty years", "LBR", T(9, 20.0)), ("#", "For more than thirty years", None, HL("REPEATED FOR DECADES", "Konishi hanged:", "17 June 1947", "seventeenth of June", "Chaplain's letter (1983); Flanagan (1986); Rottman (2010)"))],
    # 77 what the records show
    [("It was not true", "LBR", T(10, 5.0)), ("#", "It was not true", None, TL("FILE 12 — WHAT THE ARMY RECORDS SHOW", "Sadaaki Konishi",
        [("15 Jan 1947", "Sentenced to hang"), ("17 Jun 1947", "Baptized — not hanged"), ("14 Aug 1947", "MacArthur stays the execution"),
         ("20 Sep 1948", "Sugamo Prison, Tokyo"), ("30 Apr 1949", "Hanged at 00:33")], f"{HEN} (Army records)"))],
    # 78 Sugamo
    [("#", "In April", None, HL("SUGAMO PRISON, TOKYO", "30 April 1949  ·", "00:33", "thirty-three minutes past midnight", HEN)),
     ("The man convicted", "LBR", T(10, 28.0)), ("@", "The man convicted", MNL_TAG)],
    # 79 the camp today (print)
    [("Today, the camp grounds", "TRV", T(10, 56.0)), ("@", "Today, the camp grounds", TRVS_TAG)],
    # 80 the U.S. citation
    [("#", "The American record", None, LQ("FILE 13 — WAR DEPARTMENT GENERAL ORDERS NO. 71, 22 AUG 1945", "Distinguished Unit Citation",
        "a coordinated thrust 25 miles behind enemy lines", "Recon Platoon, 11th Airborne Division · Company B, 511th PIR", FL48,
        after=", which made possible the liberation of 2,147 Allied civilians and prisoners of war"))],
    # 81 the Filipino markers (print + quote)
    [("#", "It says the camp", None, LQ("FILE 14 — NATIONAL HISTORICAL INSTITUTE MARKER, 2005", "Baker Hall, UP Los Baños",
        "The initial raid was led by Lt. Col. Honorio Guerrero and the ROTC Hunters.", "NHI marker (English text)", "HMdb.org marker 63618",
        after=" … with the assistance of the members of Company B, 511th"))],
    # 82 enough glory (quote)
    [("Each version leaves", "LBC", T(5, 56.0)), ("@", "Each version leaves", LBC_TAG),
     ("#", "Colonel Jay Vanderpool", None, QC("stills/bowie_family_1945.jpg", [("There was enough glory", "There was enough glory"), ("for everyone involved that day.", "for everyone involved")],
        "Col. Jay Vanderpool, oral history, 1984", "that day"))],
    # 83 afterward
    [("#", "Lieutenant George", None, TL("FILE 15 — AFTERWARD", "What became of them",
        [("George Skau", "Killed in a plane crash on Okinawa, 13 Aug 1945"), ("Pete Miles", "Stayed in Manila · died 1962"),
         ("Freddy Zervoulakos", "Ten years in the U.S. Navy · died 1998"), ("Ben Edwards", "Farmed near Los Baños · died 2010, aged 91")],
        f"{HEN}; Pacific Historic Parks (2024)"))],
    # 84 Muller, Lois
    [("Henry Muller", "LBR", T(18, 34.0)), ("@", "Henry Muller", LBRB_TAG), ("And Lois McCoy", "LBR", T(18, 45.0)),
     ("#", "And Lois McCoy", None, SLUG("Lois McCoy", "Born in the camp three days before the raid · later a nurse"))],
    # 85 the phone call (quote)
    [("In nineteen ninety-eight", "LBC", T(6, 6.0)), ("@", "In nineteen ninety-eight", LBC_TAG),
     ("#", "He asked her", None, QC("stills/bowie_family_1945.jpg", [("I heard you cry.", "I heard you cry"), ("Do you have a scar on your face?", "Do you have a scar")],
        "Former amtrac gunner Dwight Clark to Lois McCoy, 1998 (Henderson 2015)", "on your face"))],
    # 86 comments
    [("If someone in your family", "BIL", T(8, 36.0)), ("@", "If someone in your family", BIL_TAG)],
    # 87 the field today
    [("Every year", "LBR", T(9, 20.0)), ("@", "Every year", AIR_TAG), ("Students at the", "TRV", T(10, 56.0)), ("@", "Students at the", TRVS_TAG),
     ("And the field where", "LBC", T(7, 43.0)), ("@", "And the field where", "Laguna de Bay from Los Baños, 23 Feb 1945 · Signal Corps film")],
]

PHOTOS = [
    (7, "were locked inside", None, "santo_tomas_aerial_1945.jpg", "07", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Santo Tomas internment camp, Manila, 1945"}),
    (11, "Among them were eleven", None, "navy_nurses_kinkaid_1945.jpg", "11", "Navy nurses freed from Los Baños", "Chief Nurse Laura Cobb with Adm. Thomas Kinkaid, March 1945", f"U.S. Navy · public domain · {WC}", {"focus": [0.5, 0.4]}),
    (19, "They did eat it", None, "santo_tomas_men_1945.jpg", "19", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Starved internees, Santo Tomas, February 1945"}),
    (23, "an internee named Pat", None, "grave_hell_1945.jpg", "23", "", "", "Signal Corps SC 269120-R, May 1945 · NARA 111-SCA album 2895 · public domain", {"style": "print", "label": "Grave of Pat Hell, Los Baños · photographed May 1945"}),
    (24, "In May", None, "grave_louis_1945.jpg", "24", "", "", "Signal Corps SC 269119-R, May 1945 · NARA 111-SCA album 2895 · public domain", {"style": "print", "label": "Grave of George Louis, Los Baños · May 1945"}),
    (37, "Major General Joseph Swing", None, "swing.jpg", "37", "Joseph Swing", "Commander, 11th Airborne Division (photo c. 1951)", f"U.S. Army · public domain · {WC}", {"focus": [0.45, 0.4]}),
    (39, "would wait in the grass", None, "american_soldier_painting.jpg", "39", "", "", f"U.S. Army art, 1945 · public domain · {WC}", {"style": "print", "label": "Army painting of the Los Baños raid · The American Soldier, 1945"}),
    (49, "They jumped from", None, "paradrop_aparri_1945.jpg", "49", "", "", f"11th Airborne Division, 1945 · CC BY-SA 4.0 · {WC}", {"style": "print", "label": "11th Airborne jump at Aparri, June 1945 (not Los Baños)"}),
    (61, "and a photographer named", None, "iwo_flag_rosenthal.jpg", "61", "Iwo Jima, 23 February 1945", "Raising the Flag on Iwo Jima, by Joe Rosenthal (AP)", f"public domain · {WC}", {"focus": [0.5, 0.45]}),
    (62, "Then the photograph", None, "bowie_family_1945.jpg", "62", "Los Baños, 23 February 1945", "Hal Bowie, his wife and baby Lea with two 11th Airborne paratroopers", f"U.S. Army Signal Corps · public domain · {WC}", {"focus": [0.5, 0.35]}),
    (79, "In front of Baker Hall", None, "camp_marker_uplb.jpg", "79", "", "", f"Ralff Nestor Nacor · CC BY-SA 4.0 · {WC}", {"style": "print", "label": "The camp marker, UP Los Baños"}),
    (81, "A marker put up", None, "baker_hall_marker.jpg", "81", "", "", f"Kej Andrés · CC BY-SA 4.0 · {WC}", {"style": "print", "label": "National Historical Institute marker, 2005 (Tagalog)"}),
]


def photo_items():
    import json as _j
    from PIL import Image
    crops = _j.load(open(ROOT / "tools/crops.json", encoding="utf-8"))
    for k, (pi, a, b, img, no, title, cap, src, extra) in enumerate(PHOTOS):
        W, H = Image.open(ROOT / f"assets/stills/{img}").size
        extra = dict(extra)
        x, y, w, h = extra.pop("crop", None) or crops.get(img, [0, 0, 1, 1])
        aspect = round(w * W / (h * H), 3)
        if extra.pop("style", None) == "print":  # ArchivePrint: print on dark graph paper, tab "ARCHIVE · <label>"
            card = {"type": "ArchivePrint", "image": img, "aspect": aspect, "crop": [x, y, w, h],
                    "label": extra.pop("label", title), "source": src, **extra}
        else:
            card = {"type": "PhotoCard", "image": img, "aspect": aspect, "crop": [x, y, w, h], "frameNo": no,
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

    SCENES = {"Section", "Chart", "IconCount", "ObjectTurn", "CodeWord", "GlobeMap"}
    SYNCED = SCENES | {"Headline", "QuoteCard", "DocDesk"}  # time fields may be spoken phrases (scenes.tsx, cards.tsx)
    TIMEKEYS = {"t", "t0", "t1", "at", "labelAt", "labelTo", "beamAt", "byAt", "out", "show", "cardsOut"}

    def sync_times(o, when, key=None):
        if isinstance(o, dict):
            return {k: sync_times(v, when, k) for k, v in o.items()}
        if isinstance(o, list):
            if key == "dig":
                return [when(v) if isinstance(v, str) else v for v in o]
            return [sync_times(v, when) for v in o]
        if key in TIMEKEYS and isinstance(o, str):
            return when(o)
        return o

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
                elif card["type"] in ("PhotoCard", "ArchivePrint"):
                    card["dur"] = 6.5
                elif card["type"] in SCENES:  # reconstruction scenes may run the whole paragraph (up to 30 s)
                    card["end"] = min(card["start"] + 30.0, max(card["start"] + 8.0, paras[pi]["end"] + 0.3))
                else:  # full card runs to the end of its paragraph (7-12 s)
                    card["end"] = min(card["start"] + 12.0, max(card["start"] + 7.0, paras[pi]["end"] + 0.3))
                if card["type"] in SYNCED:  # any time field given as a phrase = when that phrase is spoken (s from card start)
                    card = sync_times(card, lambda ph, pi=pi, c0=card["start"]: round(said(pi, ph)[0] - c0, 3))
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
