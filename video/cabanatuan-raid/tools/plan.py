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


F = {  # film key -> (file in assets/footage, fraction of height kept)
    "NR": ("cabanatuan_newsreel_1945", 1), "LA": ("pow_interviews_leyte_a", 1), "LB": ("pow_interviews_leyte_b", 1),
    "H": ("pows_118th_hospital", 1), "TAC": ("pows_arrive_tacloban", 1), "P61": ("p61_black_widow_1945", 1),
    "KRU": ("krueger_1945", 1), "TNK": ("japanese_tanks_binalonan", 1), "LIN": ("lingayen_invasion_1945", 0.74),
    "COR": ("corregidor_newsreel_feb1945", 1), "FRE": ("freedom_philippines", 0.86), "CEB": ("cebu_prisoners_1945", 1), "AIT": ("appointment_in_tokyo_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
KING = "Michael J. King, Rangers: Selected Combat Operations in WWII, Leavenworth Paper 11 (1985)"
VER = "Michael E. Krivdo, Veritas 14:2 (USASOC, 2018)"
WD = "War Department release 'Philippine Rescue Mission' (1945)"
AP45 = "Associated Press, 1 February 1945"
USMC = "Frank & Shaw, Victory and Occupation (USMC, 1968)"
MCR = "McRaven, NPS thesis (1993)"

NR_TAG = "Freed prisoners and their rescuers, Luzon, February 1945 · Universal Newsreel (NARA UN-UN-18-375)"
NRV_TAG = "Freed prisoner, February 1945 · Universal Newsreel · original sound"
LA_TAG = "A freed Cabanatuan prisoner, 118th General Hospital, Leyte, 13 Feb 1945 · Signal Corps film (111-ADC-3330) · original sound"
LB_TAG = "Freed prisoners, 118th General Hospital, Leyte, February 1945 · Signal Corps film (111-ADC-3377)"
H_TAG = "American prisoners freed on Luzon, 118th General Hospital, Leyte, February 1945 · Signal Corps film (111-ADC-3332)"
TAC_TAG = "Freed prisoners flown to Leyte, February 1945 · Signal Corps film (111-ADC-3381)"
P61_TAG = "Stand-in · A P-61 Black Widow night fighter (another aircraft), 1945 · U.S. Navy film (NARA NPC-11083)"
KRU_TAG = "Lt. Gen. Walter Krueger, Sixth Army, Luzon, 1945 · Signal Corps film (111-ADC-5005)"
TNK_TAG = "U.S. troops on Luzon, January 1945 · Signal Corps film (111-ADC-3231)"
TNKS_TAG = "Stand-in · U.S. infantry wade a river by a broken bridge, Luzon, January 1945 · Signal Corps film (111-ADC-3231)"
JTK_TAG = "Japanese tanks knocked out on Luzon, January 1945 · Signal Corps film (111-ADC-3231)"
LIN_TAG = "Sixth Army lands at Lingayen Gulf, January 1945 · U.S. Navy film (NARA NPC-4938)"
COR_TAG = "The Philippines, February 1945 · United News newsreel"
FRE_TAG = "Bataan, 1942 · from 'Freedom for the Philippines' (U.S. archive film)"
FREL_TAG = "Luzon, 1945 · from 'Freedom for the Philippines' (U.S. archive film)"
CEB_TAG = "Stand-in · American prisoners freed on Cebu, 1945 · Signal Corps film (111-ADC-3273)"
STAND = "Stand-in · "
AIT_TAG = "The Cabanatuan raid, January 1945 · Signal Corps film, from 'Appointment in Tokyo' (1945)"
AITF_TAG = "Freed prisoners of Cabanatuan walk out, 31 January 1945 · Signal Corps film, from 'Appointment in Tokyo' (1945)"

LIN = [120.33, 16.05]; GUI = [120.77, 15.66]; CAB = [120.97, 15.49]; CAMP = [121.05, 15.53]; MNL = [120.984, 14.599]
BAT = [120.5, 14.62]; COR = [120.575, 14.385]; PAL = [118.74, 9.74]; LEY = [125.0, 11.24]; SFO = [-122.42, 37.77]

LUZON45 = {"type": "GlobeMap", "theme": "history",
           "cam": [{"t": 0, "center": [121.0, 15.2], "scale": 22}, {"t": "Within three weeks", "center": [120.75, 15.6], "scale": 95}],
           "pins": [{"ll": LIN, "label": "Lingayen Gulf", "at": "landed at"}, {"ll": GUI, "label": "Guimba", "at": "the town of", "color": "amber"},
                    {"ll": CAMP, "label": "Cabanatuan prison camp", "at": "from the prison camp", "color": "red"},
                    {"ll": MNL, "label": "Manila", "at": 0.6}],
           "arcs": [{"from": LIN, "to": GUI, "at": "Within three weeks", "style": "solid", "color": "amber", "loft": 0.01, "draw": 40},
                    {"from": GUI, "to": CAMP, "at": "about twenty-five miles", "style": "dashed", "color": "red", "loft": 0.0, "draw": 30}],
           "cards": [{"at": "landed at", "kicker": "9 January 1945", "body": "Sixth Army lands at Lingayen Gulf", "accent": "amber"},
                     {"at": "about twenty-five miles", "kicker": "Late January 1945", "body": "Front line at Guimba, about 25 miles from the camp", "accent": "red"}],
           "footer": "Positions approximate · front line after King (1985)", "year": {"at": 0.1, "year": "1945", "sub": "Luzon"}}

PALAWAN = {"type": "GlobeMap", "theme": "history",
           "cam": [{"t": 0, "center": [121.0, 15.0], "scale": 14}, {"t": "on the island of", "center": [119.5, 11.0], "scale": 16}],
           "pins": [{"ll": CAMP, "label": "Cabanatuan", "at": 0.3}, {"ll": PAL, "label": "Palawan · Puerto Princesa", "at": "on the island of", "color": "red"}],
           "cards": [{"at": "set them on fire", "kicker": "14 December 1944", "body": "139 prisoners killed · 11 escaped", "accent": "red"}],
           "footer": "Figures: Krivdo, Veritas 14:1 (2018)", "year": {"at": 0.1, "year": "1944", "sub": "Palawan"}}

HOME = {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [125, 12], "scale": 6}, {"t": "They reached", "center": [181, 24], "scale": 1.0}],
        "pins": [{"ll": LEY, "label": "Leyte", "at": 0.4}, {"ll": SFO, "label": "San Francisco", "at": "They reached", "color": "amber"}],
        "arcs": [{"from": LEY, "to": SFO, "at": "sailed from", "style": "dashed", "color": "amber", "loft": 0.12, "draw": 80}],
        "cards": [{"at": "sailed from", "kicker": "11 Feb – 8 Mar 1945", "body": "About 280 freed prisoners sail home", "accent": "amber"}],
        "footer": "Route generalised", "year": {"at": 0.1, "year": "1945", "sub": "Home"}}

# reconstruction: the crawl across the open field (King: a mile, 75 minutes, a tower sentry lowers his rifle)
CRAWL = {"type": "Section", "world": "ground", "W": 3400, "H": 1500, "surface": 820,
         "date": "Pangatian camp · 30 January 1945 · about 6:00 p.m.", "place": "Reconstruction · after King (1985), schematic, not to scale",
         "cam": [{"t": 0, "x": 1300, "y": 740, "z": 0.62}, {"t": 14, "x": 1900, "y": 740, "z": 0.78}],
         "items": [{"kind": "fence", "x": 2700, "y": 820, "w": 300}, {"kind": "tower", "x": 2560, "y": 820, "label": "Guard tower", "labelAt": 2.5, "labelTo": 7},
                   {"kind": "hut", "x": 3120, "y": 820, "w": 420},
                   {"kind": "man", "pose": "crawl", "move": [{"t": 0, "x": 300, "y": 820}, {"t": 16, "x": 2050, "y": 820}], "linear": True, "label": "Rangers", "labelAt": 1, "labelTo": 6},
                   {"kind": "man", "pose": "crawl", "move": [{"t": 0, "x": 120, "y": 820}, {"t": 16, "x": 1870, "y": 820}], "linear": True},
                   {"kind": "man", "pose": "crawl", "move": [{"t": 0, "x": -60, "y": 820}, {"t": 16, "x": 1690, "y": 820}], "linear": True},
                   {"kind": "man", "pose": "crawl", "move": [{"t": 0, "x": -240, "y": 820}, {"t": 16, "x": 1510, "y": 820}], "linear": True}],
         "pills": [{"t0": "The camp was a mile", "t1": 30, "text": "About one mile of open ground", "y": 230},
                   {"t0": "seventy-five minutes", "t1": 30, "text": "75 minutes on their bellies", "y": 300}],
         "source": KING}

# schematic of the plan (King's Map 6): columns to the gate and the rear, roadblocks, the Cabu bridge
PLAN = {"type": "Chart", "head": "The plan · 30 January 1945", "date": "Schematic after King (1985), Map 6",
        "zoom": [1.0, 1.08],
        "tracks": [{"kind": "column", "label": "Prince · Company C", "pts": [[880, 1060], [940, 700], [960, 610]], "t0": 0.5, "t1": 5, "labelAt": 1},
                   {"kind": "column", "label": "Murphy · F Company platoon", "pts": [[880, 1060], [700, 760], [640, 420], [900, 300]], "t0": 1, "t1": 6, "labelAt": 2},
                   {"kind": "column", "label": "Joson's guerrillas", "pts": [[880, 1060], [520, 900], [380, 820]], "t0": 2.5, "t1": 7, "labelAt": 3},
                   {"kind": "column", "label": "Pajota's guerrillas", "pts": [[880, 1060], [1300, 700], [1500, 380]], "t0": "would hold the bridge", "t1": "Under the far end", "labelAt": "would hold the bridge"}],
        "contacts": [{"t": 0.3, "x": 960, "y": 520, "label": "Prison camp"}, {"t": "southwest", "x": 380, "y": 820, "label": "Roadblock"},
                     {"t": "would hold the bridge", "x": 1520, "y": 340, "label": "Cabu bridge"}, {"t": "between the camp", "x": 1700, "y": 200, "label": "Japanese battalion"}],
        "booms": [{"t": "time bomb", "x": 1520, "y": 340, "n": 3}],
        "source": f"{KING} · schematic, not to scale"}

COUNT = {"type": "IconCount", "icon": "man", "total": 511, "label": "Prisoners brought out", "accent": "out",
         "highlight": {"n": 225, "label": "Had to be carried", "accent": "carried", "at": "had to be carried"},
         "file": "FILE 09 — THE NUMBERS", "source": f"511: {KING} · 225: Capt. Prince, {WD}"}

P = [
    # 0 the plane
    [("Luzon, the Philippines", "P61", 60.0), ("@", "Luzon, the Philippines", P61_TAG), ("#", "Luzon, the Philippines", None, SLUG("30 January 1945 · 6:40 p.m.", "Pangatian prison camp, near Cabanatuan, Luzon")),
     ("comes in low", "P61", 66.0), ("It crosses the camp", "P61", 80.0), ("On the ground", "TNK", 556.0), ("@", "On the ground", STAND + TNK_TAG)],
    # 1 the crawl
    [("Nobody is looking", "AIT", 2056.9), ("@", "Nobody is looking", AIT_TAG), ("Out there", "TNK", 559.0), ("@", "Out there", STAND + TNK_TAG), ("They are Rangers", "AIT", 2047.0), ("One guard in a tower", "FRE", 320.0), ("@", "One guard in a tower", STAND + FRE_TAG)],
    # 2 inside the wire
    [("Inside the wire", "H", 30.0), ("@", "Inside the wire", H_TAG), ("Many of them", "H", 40.0), ("Most are sick", "LB", 45.0), ("At a quarter to eight", "NR", 262.0), ("@", "At a quarter to eight", NR_TAG), ("Two weeks later", "LA", 70.0)],
    # 3 CLIP massacre
    [("Shortly after dark", "LA", 102.3), ("@", "Shortly after dark", LA_TAG)],
    # 4 documented story
    [("This is the documented", "AIT", 2045.8), ("@", "This is the documented", AIT_TAG), ("a dozen Alamo Scouts", "AIT", 2050.5), ("to bring out", "AIT", 2072.0), ("You will hear it", "AIT", 2109.6), ("the newspapers", "NR", 262.0), ("@", "the newspapers", NR_TAG)],
    # 5 Bataan to Cabanatuan
    [("To understand that night", "FRE", 312.0), ("@", "To understand that night", FRE_TAG), ("In April", "FRE", 327.0), ("The men who survived", "FRE", 335.0), ("From there", "H", 30.0), ("@", "From there", STAND + H_TAG)],
    # 6 grim place
    [("It was a grim place", "CEB", 40.0), ("@", "It was a grim place", CEB_TAG), ("#", "It records one date", None, LQ("FILE 01 — CABANATUAN", "U.S. MARINE CORPS OFFICIAL HISTORY", "the first day in the history of the camp without a death.", "On 16 January 1943", USMC, before="…until 16 January 1943, which was "))],
    # 7 rice
    [("The men lived on rice", "LB", 380.0), ("@", "The men lived on rice", STAND + LB_TAG), ("#", "One of them", None, QC("stills/camp_sick_drink.jpg", [("We were down to as low as", "down to about eight hundred"), ("800 calories a day", "calories a day"), ("and you had to work on it.", "and still had to work")],
        "Dr. Herbert Ott, former Cabanatuan prisoner · interview, 1993 (McRaven, NPS thesis)", "It took twelve hundred"))],
    # 8 barracks
    [("The barracks were long", "LB", 40.0)],
    # 9 hell ships
    [("In October", "FRE", 327.0), ("@", "In October", STAND + FRE_TAG), ("The Japanese were shipping", "FRE", 312.0), ("In December", "LIN", 300.0), ("@", "In December", STAND + "Ships off Luzon, January 1945 · U.S. Navy film (NARA NPC-4938)")],
    # 10 left behind
    [("Those left behind", "H", 120.0), ("@", "Those left behind", H_TAG), ("There were a little", "H", 133.0), ("Most were Americans", "H", 150.0), ("There were also British", "H", 175.0)],
    # 11 recipes
    [("They kept themselves", "H", 190.0), ("An Associated Press", "H", 200.0), ("And they had built", "H", 215.0)],
    # 12 guards leave
    [("Early in January", "CEB", 115.0), ("@", "Early in January", CEB_TAG), ("Then Japanese troops", "TNK", 33.0), ("@", "Then Japanese troops", JTK_TAG), ("The prisoners could hear", "TNK", 380.0), ("@", "The prisoners could hear", STAND + TNK_TAG),
     ("#", "The prisoners could hear", None, TL("FILE 02 — THE LAST WEEKS", "Cabanatuan, 1944-45", [("Oct 1944", "About 1,600 prisoners marched out"), ("13 Dec 1944", "1,619 prisoners loaded on the Oryoku Maru, Manila"),
        ("14 Dec 1944", "Massacre at Palawan"), ("Early Jan 1945", "The guard company leaves the camp"), ("9 Jan 1945", "Sixth Army lands at Lingayen Gulf")], f"{USMC}; AP 1945; {VER}"))],
    # 13 Lingayen
    [("On the ninth", "LIN", 20.0), ("@", "On the ninth", LIN_TAG), ("General MacArthur had", "LIN", 75.0), ("#", "Within three weeks", None, LUZON45)],
    # 14 DSC motive
    [("That was the danger", "TNK", 395.0), ("#", "When the Distinguished", None, LQ("FILE 03 — THE CITATION", "DISTINGUISHED SERVICE CROSS · LT. COL. HENRY A. MUCCI", "It was believed that the enemy would kill or remove the prisoners", "HQ USAFFE, General Orders No. 39, 21 February 1945",
        "Citation text, General Orders No. 39 (via Military Times Hall of Valor)", after=" when our attack was launched in that area."))],
    # 15 Palawan
    [("There was reason", "CEB", 365.0), ("#", "A month earlier", None, PALAWAN), ("Whether Palawan", "CEB", 370.0), ("@", "Whether Palawan", CEB_TAG)],
    # 16 Lapham
    [("On the twenty-sixth", "TNK", 410.0), ("@", "On the twenty-sixth", STAND + TNK_TAG), ("His Filipino runners", "TNK", 573.0), ("On the recommendation", "TNK", 420.0)],
    # 17 the battalion
    [("The Sixth Ranger Battalion", "TNK", 410.0), ("@", "The Sixth Ranger Battalion", STAND + TNK_TAG), ("In April", "TNK", 423.0), ("He turned the gunners", "TNK", 300.0)],
    # 18 Leyte landing
    [("In September", "COR", 52.0), ("@", "In September", COR_TAG), ("On the seventeenth", "LIN", 90.0), ("@", "On the seventeenth", STAND + LIN_TAG)],
    # 19 Company C
    [("For the camp", "TNK", 160.0), ("@", "For the camp", STAND + TNK_TAG), ("He added the second", "TNK", 509.0), ("With a few others", "TNK", 488.0), ("The newspapers would", "TNK", 520.0)],
    # 20 soft caps
    [("They went in soft caps", "TNK", 530.0), ("himself took only", "TNK", 532.0), ("Years later", "TNK", 551.0)],
    # 21 Alamo Scouts
    [("Ahead of the Rangers", "TNK", 551.0), ("@", "Ahead of the Rangers", STAND + TNK_TAG), ("They were small teams", "TNK", 560.0), ("The Army says", "TNK", 563.0)],
    # 22 Nellist and Rounsaville
    [("The two teams", "TNK", 575.0), ("They left the American", "TNK", 592.0)],
    # 23 the hut
    [("found a way", "TNK", 584.0), ("@", "found a way", STAND + TNK_TAG), ("From there they could", "TNK", 590.0)],
    # 24 the march begins
    [("The Rangers left their base", "TNK", 390.0), ("@", "The Rangers left their base", STAND + TNK_TAG), ("#", "The Rangers left their base", None, SLUG("28 January 1945 · 5:00 a.m.", "The Rangers leave by truck")), ("At the village", "TNK", 470.0)],
    # 25 behind the lines
    [("After dark", "TNK", 610.0), ("Late that night", "TNK", 22.0), ("@", "Late that night", JTK_TAG), ("At midnight they waded", "TNK", 474.0), ("@", "At midnight they waded", TNKS_TAG), ("At four in the morning", "TNK", 395.0)],
    # 26 Balincarin
    [("At six in the morning", "TNK", 600.0), ("There they met", "TNK", 588.0), ("He also brought news", "TNK", 592.0)],
    # 27 Pajota
    [("was from", "TNK", 576.0), ("His men knew", "FRE", 1311.0), ("@", "His men knew", STAND + "Filipino men, Luzon, 1945 · from 'Freedom for the Philippines' (U.S. archive film)"), ("And what he told", "TNK", 25.0), ("@", "And what he told", JTK_TAG)],
    # 28 Japanese at Cabu
    [("About a mile north", "TNK", 25.0), ("@", "About a mile north", STAND + JTK_TAG), ("Later reports", "TNK", 101.0), ("And in", "TNK", 112.0)],
    # 29 postponed
    [("made his decision", "FRE", 1305.0), ("#", "He postponed", None, SLUG("29 January 1945", "The raid is postponed 24 hours"))],
    # 30 carts and dogs
    [("asked the guerrillas", "FRE", 1308.5), ("@", "asked the guerrillas", STAND + "Filipino men, Luzon, 1945 · from 'Freedom for the Philippines' (U.S. archive film)"), ("He asked the villagers", "FRE", 1315.0), ("Captain Prince later said", "FRE", 1332.5)],
    # 31 Platero
    [("That afternoon", "FRE", 1335.5), ("@", "That afternoon", STAND + FREL_TAG)],
    # 32 camp drawn
    [("By the morning", "H", 95.0), ("#", "By the morning", None, DESK("stills/album_map_paper.png", 1.2912, [(0, "wide", [0.5, 0.55]), ("The main gate", "glide", [0.55, 0.15, 0.7]), ("The prisoners were kept", "glide", [0.3, 0.12, 0.6])],
        "Map of Cabanatuan prison camp · U.S. Navy BuMed, 'Prisoner of War Photographs: Cabanatuan' (1946), archive.org"))],
    # 33 guards
    [("There were seventy-three", "AIT", 2062.0), ("@", "There were seventy-three", AIT_TAG), ("But at eleven", "TNK", 412.0), ("@", "But at eleven", STAND + TNK_TAG)],
    # 34 Prince's plan
    [("Captain Prince drew up", "TNK", 433.0), ("His company would", "TNK", 448.0), ("Lieutenant Murphy's platoon", "TNK", 455.0), ("When the prisoners were out", "TNK", 462.0)],
    # 35 roadblocks, bridge (schematic)
    [("The guerrillas would hold", "TNK", 470.0), ("#", "The guerrillas would hold", None, PLAN)],
    # 36 the open field
    [("There was one problem", "TNK", 551.0), ("@", "There was one problem", STAND + TNK_TAG), ("For more than a mile", "TNK", 556.0), ("The Rangers would have", "TNK", 561.0)],
    # 37 the plane idea
    [("The answer came", "P61", 8.0), ("@", "The answer came", P61_TAG), ("The Special Operations", "COR", 101.0), ("@", "The Special Operations", COR_TAG), ("The night fighters", "P61", 60.0)],
    # 38 doubts
    [("Prince had his doubts", "COR", 108.0)],
    # 39 leave Platero
    [("At five in the afternoon", "AIT", 2046.2), ("@", "At five in the afternoon", AIT_TAG), ("With the guerrillas", "AIT", 2051.0), ("#", "last order is quoted", None, QC("stills/sc396864_rangers.jpg", [("Remember, all of the prisoners go.", "all of the prisoners go"), ("No one is left behind.", "no one is left behind")],
        "Lt. Col. Henry Mucci, 1945 article (via Krivdo, Veritas, 2018)", "no one is left behind"))],
    # 40 subscribe
    [("If you want more", "TNK", 462.0), ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented"}), ("Now, back to the field", "TNK", 551.0)],
    # 41 the crawl (reconstruction)
    [("At six o'clock", "AIT", 2057.0), ("@", "At six o'clock", AIT_TAG), ("#", "went down on their bellies", None, CRAWL)],
    # 42 the P-61
    [("At twenty to seven", "P61", 62.0), ("@", "At twenty to seven", P61_TAG), ("It came over the bridge", "P61", 66.0), ("One account says", "P61", 26.0), ("#", "At twenty to seven", None, SLUG("6:40 p.m.", "The P-61 'Hard to Get' over the camp")),
     ("#", "Prince remembered", None, QC("stills/rangers_tall_grass.jpg", [("…cutting his motor,", "cutting his motor"), ("doing every crazy thing he could", "every crazy thing"), ("to attract attention.", "to attract attention")],
        "Capt. Robert Prince, 2005 (via Krivdo, Veritas, 2018)", "watching from his hut"))],
    # 43 culvert
    [("It worked", "TNK", 480.0), ("Murphy's platoon slipped", "TNK", 486.0), ("@", "Murphy's platoon slipped", TNKS_TAG), ("Prince's men crawled", "TNK", 554.0), ("At twenty-five past", "TNK", 563.0)],
    # 44 the moon
    [("The plan said", "TNK", 572.0), ("The moon was up", "AIT", 2057.0), ("@", "The moon was up", AIT_TAG)],
    # 45 the shot
    [("At a quarter to eight", "TNK", 395.0), ("#", "At a quarter to eight", None, LQ("FILE 04 — 7:45 P.M.", "THE ARMY'S STUDY OF THE RAID", "His shot was the signal.", "Michael J. King, U.S. Army Combat Studies Institute, 1985", KING,
        before="At 1945, Murphy aimed his M-1 rifle at an open window in the nearest barrack and fired. "))],
    # 46 thirty seconds, the lock
    [("Every Ranger opened fire", "FRE", 365.0), ("@", "Every Ranger opened fire", STAND + FRE_TAG), ("At the main gate", "AIT", 2060.8), ("@", "At the main gate", AIT_TAG),
     ("#", "He said a Japanese soldier", None, QC("stills/sc396864_rangers.jpg", [("What's going on here?", "what was going on")], "A Japanese soldier at the gate, as recalled by S/Sgt. Theodore Richardson · " + WD, "what was going on"))],
    # 47 bazookas, first prisoner
    [("The Rangers poured in", "FRE", 373.0), ("A bazooka section", "TNK", 108.0), ("@", "A bazooka section", STAND + JTK_TAG), ("Private First Class", "H", 60.0), ("@", "Private First Class", H_TAG)],
    # 48 panic
    [("Inside the prisoners' huts", "LB", 60.0), ("@", "Inside the prisoners' huts", LB_TAG), ("#", "A Navy warrant officer", None, QC("stills/album_hospital_ward.png", [("When the firing started,", "when the firing started"), ("most of us thought it was the [Japanese]", "most of them thought"), ("coming in to kill us.", "coming to kill them")],
        "Navy WO Paul Jackson, letter of 15 March 1945 (via Krivdo, Veritas, 2018)", "A marine from"))],
    # 49 CLIP blind
    [("I can't see very well", "LA", 164.6), ("@", "I can't see very well", LA_TAG)],
    # 50 carried
    [("Prince said they found", "H", 253.0), ("#", "Prince said they found", None, COUNT), ("And", "CEB", 30.0)],
    # 51 the British
    [("The British prisoners", "H", 330.0), ("#", "The British prisoners", None, QC("stills/rescued_from_japs.jpg", [("we're not Americans,", "we're not Americans"), ("but we're coming too!", "but we're coming too")], "British prisoners at Cabanatuan, as quoted by Lt. Col. Mucci, 1945 (via Krivdo, Veritas)", "but we're coming too"))],
    # 52 the bridge
    [("At the same moment", "TNK", 507.5), ("@", "At the same moment", TNKS_TAG), ("When the first shots", "TNK", 515.0), ("The time bomb went off", "TNK", 530.0)],
    # 53 Pajota's secret
    [("had kept a secret", "TNK", 560.0), ("@", "had kept a secret", STAND + TNK_TAG), ("Besides the men", "FRE", 1303.0), ("@", "Besides the men", STAND + FREL_TAG), ("Now they were all", "TNK", 520.0)],
    # 54 tanks knocked out
    [("Ranger bazooka men", "TNK", 25.0), ("@", "Ranger bazooka men", JTK_TAG), ("men held the bridge", "TNK", 30.0), ("The Army's study says", "TNK", 536.0)],
    # 55 mortar
    [("About twelve minutes", "FRE", 366.0), ("@", "About twelve minutes", STAND + FRE_TAG), ("Then a Japanese light", "TNK", 300.0), ("Six men were wounded", "TAC", 158.0), ("@", "Six men were wounded", STAND + TAC_TAG)],
    # 56 Fisher
    [("Two of them were officers", "TAC", 160.0), ("The other was the battalion", "TAC", 165.0), ("The Rangers called him", "TAC", 175.0)],
    # 57 red flare, Sweezy
    [("At a quarter past eight", "TNK", 470.0), ("#", "At a quarter past eight", None, SLUG("8:15 p.m.", "The red flare · withdrawal")), ("As the last Rangers", "TNK", 488.0), ("@", "As the last Rangers", STAND + TNK_TAG), ("He and Captain Fisher", "TNK", 496.0)],
    # 58 left behind
    [("One prisoner died", "H", 400.0), ("@", "One prisoner died", H_TAG), ("In the confusion", "H", 410.0), ("He woke up", "H", 420.0)],
    # 59 river, Platero
    [("By half past eight", "AIT", 2072.5), ("@", "By half past eight", AITF_TAG), ("A second flare", "AIT", 2079.0), ("a Filipino doctor", "AIT", 2086.0)],
    # 60 carts (bars)
    [("Then came the carts", "NR", 276.0), ("#", "Then came the carts", None, BARS("FILE 05 — THE CART TRAIN", "Carabao carts, 30-31 January", [("Platero, evening", 25, "25", "about 115 men aboard"),
        ("2:30 a.m.", 51, "51", "column a mile and a half long"), ("Sibul, morning", 71, "71", "three times the plan")], 80, f"{KING}; {VER}"))],
    # 61 Rizal highway
    [("The most dangerous", "AIT", 2105.8), ("@", "The most dangerous", AITF_TAG), ("The column had to march", "AIT", 2093.0), ("The last man", "NR", 262.0), ("@", "The last man", NR_TAG)],
    # 62 Jackson's leg
    [("The Rangers walked", "NR", 300.0), ("#", "The Navy warrant officer", None, QC("stills/album_wagon_road.png", [("The Rangers further helped", "the Rangers pushed"), ("by pushing the carabao carts…", "through the night"), ("and never a complaint.", "and never a complaint")],
        "Navy WO Paul Jackson, letter of 15 March 1945 (via Krivdo, Veritas, 2018)", "and never a complaint"))],
    # 63 Fisher operated on
    [("could not be moved", "TAC", 214.0), ("@", "could not be moved", STAND + TAC_TAG), ("When he needed blood", "TAC", 222.0), ("The scouts cleared", "TAC", 137.0)],
    # 64 the plane never came
    [("The plane never came", "TAC", 145.0), ("Filipino guerrillas buried", "FRE", 1306.0), ("@", "Filipino guerrillas buried", STAND + FREL_TAG)],
    # 65 cemetery
    [("His body was later", "FRE", 1340.0)],
    # 66 Sibul, patrol
    [("At", "NR", 305.0), ("#", "At", None, SLUG("31 January 1945 · 8:00 a.m.", "Sibul: radio contact with Sixth Army")), ("Around eleven", "AIT", 2097.0), ("@", "Around eleven", AITF_TAG), ("Trucks and ambulances", "AIT", 2102.0), ("An hour later", "NR", 307.0), ("@", "An hour later", NR_TAG)],
    # 67 Goodbla
    [("Staff Sergeant Clinton", "NR", 340.0), ("#", "It cut right through me", None, QC("stills/sc201653_wing.jpg", [("It cut right through me;", "It cut right through me"), ("the flag, it cut right through me.", "The flag, it cut"), ("Being free cut right through me.", "Being free cut")],
        "S/Sgt. Clinton Goodbla, 60th Coast Artillery, freed at Cabanatuan · AP, 1 February 1945", "Being free cut")), ("A corporal from the same", "NR", 356.0)],
    # 68 CLIP Hay
    [("You people do not", "NR", 360.3), ("@", "You people do not", "Cpl. Cecil Hay, freed at Cabanatuan, February 1945 · Universal Newsreel · original sound")],
    # 69 Krueger, Potter
    [("General Krueger came", "H", 60.0), ("@", "General Krueger came", H_TAG), ("#", "He wrote later", None, QC("stills/pows_hospital.jpg", [("Most of them were in pitiable condition", "most of them were in pitiable"), ("and could not realize", "and could not realize"), ("they were actually safe.", "actually safe")],
        "Lt. Gen. Walter Krueger, From Down Under to Nippon (1953), via Krivdo", "Some had lost")), ("A British signalman", "NR", 338.0), ("@", "A British signalman", NR_TAG)],
    # 70 MacArthur
    [("On the first of February", "COR", 66.0), ("@", "On the first of February", COR_TAG), ("#", "In a special", None, QC("stills/sc201655_abbott.jpg", [("No incident of the campaign", "no incident of the campaign"), ("has given me such", "has given me such"), ("personal satisfaction.", "personal satisfaction")],
        "Gen. Douglas MacArthur, special communiqué · AP, 1 February 1945", "He awarded the commander"))],
    # 71 front pages
    [("The story hit", "COR", 70.0), ("The Associated Press wrote", "NR", 300.0), ("#", "The Associated Press wrote", None, HL("ASSOCIATED PRESS · 31 JANUARY 1945", "Men of Bataan, Corregidor and Singapore —", "513 of them", "five hundred and thirteen", AP45, after=" — were snatched from the Japanese last night in an exploit of unmatched daring.")),
     ("#", "Another reporter wrote", None, QC("stills/album_wagon_road.png", [("There is a long, dirty, twisting lane", "a long, dirty, twisting lane"), ("which should become a war monument,", "should become a war monument"), ("for today it bridged two worlds.", "bridged two worlds")],
        "Russell Brines, AP, 31 January 1945 (St. Louis Post-Dispatch, 1 Feb 1945)", "bridged two worlds"))],
    # 72 Ranger log
    [("Not everything", "H", 260.0), ("#", "The Rangers' own log", None, LQ("FILE 06 — 6TH RANGER BATTALION LOG", "31 JANUARY 1945", "Mission completed. Casualties: Capt Fisher and Corporal Sweezy killed in action;", "6th Ranger Battalion log, 31 January 1945", MCR,
        after=" Pvt Peters, Jack wounded. … 510 prisoners released from Japanese prison."))],
    # 73 the count (bars)
    [("Even the count", "H", 270.0), ("#", "Even the count", None, BARS("FILE 07 — HOW MANY WERE FREED", "Prisoners brought out, by source", [("Ranger log, 31 Jan 1945", 510, "510", ""), ("Army study (King, 1985)", 511, "511", "also the War Department, 1945"),
        ("Rosters (Veritas, 2018)", 516, "516", "489 Americans, 23 British, 4 others")], 540, f"{MCR}; {KING}; {VER}"))],
    # 74 voices
    [("Within two weeks", "LB", 380.0), ("@", "Within two weeks", LB_TAG), ("This is Sergeant", "NR", 405.0)],
    # 75 CLIP Goldie
    [("Well, we're finally", "NR", 407.7), ("@", "Well, we're finally", "Sgt. Samuel Goldie, freed at Cabanatuan, February 1945 · Universal Newsreel · original sound")],
    # 76 home
    [("On the eleventh", "NR", 431.0), ("#", "On the eleventh", None, HOME), ("They reached", "TAC", 140.0), ("The day before", "CEB", 380.0)],
    # 77 Prince's tour (desk)
    [("Captain Prince and eleven", "H", 326.0), ("#", "The War Department printed", None, DESK("stills/prm_p1_paper.png", 1.4706, [(0, "wide", [0.5, 0.2]), ("they fed us", "glide", [0.80, 0.08, 0.7]), ("And he said", "glide", [0.83, 0.1, 0.6])],
        "War Department, Bureau of Public Relations, 'Philippine Rescue Mission' (1945) · archive.org"))],
    # 78 verdicts
    [("Sixth Army's intelligence", "CEB", 195.0), ("@", "Sixth Army's intelligence", CEB_TAG), ("#", "An Army historian", None, QC("stills/sc396864_rangers.jpg", [("perhaps the best conceived", "perhaps the best conceived"), ("and executed Ranger mission", "and executed Ranger mission"), ("of World War II.", "of the Second World War")],
        "David W. Hogan Jr., U.S. Army historian, 1992 (via Krivdo, Veritas)", "of the Second World War"))],
    # 79 Mucci
    [("was promoted to colonel", "KRU", 102.0), ("@", "was promoted to colonel", STAND + "An awards ceremony, Luzon, 1945 · Signal Corps film (111-ADC-5005)")],
    # 80 Prince
    [("Robert Prince left", "TNK", 562.0), ("@", "Robert Prince left", STAND + TNK_TAG), ("His son Steve", "TNK", 568.0)],
    # 81 Rounsaville, Kittleson
    [("recovered from his wound", "TNK", 573.0), ("The Alamo Scout", "AIT", 2047.5), ("@", "The Alamo Scout", AIT_TAG)],
    # 82 Joson, Pajota
    [("became governor of", "FRE", 1330.0), ("@", "became governor of", STAND + FREL_TAG), ("moved to the United States", "FRE", 1329.5)],
    # 83 the dead
    [("lie in the Manila", "FRE", 1340.0), ("The Filipino guerrillas", "NR", 262.0), ("Their losses", "NR", 270.0)],
    # 84 your family
    [("If your father", "NR", 380.0), ("@", "If your father", NR_TAG), ("#", "If your father", None, HL("YOUR FAMILY", "Was he at Cabanatuan, on Bataan or on Corregidor?", "Tell us his name", "tell us his name", "WWII Frontlines", after=" in the comments."))],
    # 85 memorial
    [("The camp is gone", "AIT", 2104.0), ("@", "The camp is gone", AITF_TAG), ("On the site stands", "TNK", 556.0), ("Its wall carries", "TNK", 562.0)],
    # 86 the end
    [("On the first of February, 2025", "NR", 256.0), ("@", "On the first of February, 2025", NR_TAG), ("Around them", "AIT", 2057.0)],
]

PHOTOS = [
    (1, "One guard in a tower", None, "map_actions_objectives.jpg", "01", "", "", f"U.S. Army · {KING}, Map 6 · public domain · {WC}", {"style": "print", "label": "The camp and the field in front of it, Army map, 1985"}),
    (6, "It was a grim place", None, "prison_hut.jpg", "06", "", "", f"Public domain · {WC}", {"style": "print", "label": "A prisoners' barracks at Cabanatuan"}),
    (7, "The men lived on rice", None, "album_cooking_rice.png", "07", "", "", "Prisoner's drawing · U.S. Navy BuMed album 'Cabanatuan' (1946) · public domain", {"style": "print", "label": "'Cooking Rice', a prisoner's drawing, Cabanatuan"}),
    (8, "The barracks were long", None, "album_morgue.png", "08", "", "", "Prisoner's drawing · U.S. Navy BuMed album 'Cabanatuan' (1946) · public domain", {"style": "print", "label": "'To the Morgue', a prisoner's drawing, Cabanatuan"}),
    (11, "They kept themselves", None, "camp_sick_drink.jpg", "11", "", "", f"Ben Steele, former Bataan POW · Library of Congress · public domain · {WC}", {"style": "print", "label": "A prisoner gives his buddy a drink, Cabanatuan · drawing by Ben Steele"}),
    (16, "On the recommendation", None, "krueger_alamo_scouts.jpg", "16", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Gen. Krueger with Alamo Scouts"}),
    (17, "In April", None, "mucci.jpg", "17", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Lt. Col. Henry Mucci (left), 6th Ranger Battalion, with Capt. Vaughn Moss"}),
    (19, "For the camp", None, "sc396864_rangers.jpg", "19", "", "", f"Signal Corps SC 396864 · NARA · public domain · {WC}", {"style": "print", "label": "Rangers of the 6th Ranger Battalion head for the camp, January 1945"}),
    (21, "Ahead of the Rangers", None, "alamo_scouts_feb1945.jpg", "21", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Alamo Scouts of the Cabanatuan raid, February 1945"}),
    (26, "He also brought news", None, "pajota_guerrillas.jpg", "26", "", "", f"Public domain · {WC}", {"style": "print", "label": "Capt. Juan Pajota's guerrillas"}),
    (30, "asked the guerrillas", None, "album_wagon_road.png", "30", "", "", "Signal Corps photo · U.S. Navy BuMed album 'Cabanatuan' (1946) · public domain", {"style": "print", "label": "'The Wagon Road': carts and freed prisoners, Luzon, 1945"}),
    (34, "Captain Prince drew up", None, "map_actions_objectives.jpg", "34", "", "", f"U.S. Army · {KING}, Map 6 · public domain · {WC}", {"style": "print", "label": "Actions at the objective, 30 January 1945 (Army map)"}),
    (36, "There was one problem", None, "rangers_tall_grass.jpg", "36", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Rangers move through tall grass, January 1945"}),
    (44, "The plan said", None, "map_routes_objectives.jpg", "44", "", "", f"U.S. Army · {KING}, Map 5 · public domain · {WC}", {"style": "print", "label": "Routes to and from the camp (Army map)"}),
    (47, "The Rangers poured in", None, "sc201654_lautman.jpg", "47", "", "", f"Signal Corps SC 201654 · NARA · public domain · {WC}", {"style": "print", "label": "Signal Corps photographer Robert Lautman, who went in with the Rangers, talks to a freed prisoner"}),
    (50, "Some Rangers took off", None, "sc201655_abbott.jpg", "50", "", "", f"Signal Corps SC 201655 · NARA · public domain · {WC}", {"style": "print", "label": "Pfc. Vernon Abbott, 6th Ranger Bn., carries a freed prisoner"}),
    (56, "He had argued", None, "alamo_scouts_feb1945.jpg", "56", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Alamo Scouts, February 1945; one of them gave Fisher his blood"}),
    (60, "There fifteen more carts", None, "album_wagon_road.png", "60", "", "", "Signal Corps photo · U.S. Navy BuMed album 'Cabanatuan' (1946) · public domain", {"style": "print", "label": "'The Wagon Road', Luzon, 1945"}),
    (66, "Around eleven", None, "rescued_from_japs.jpg", "66", "", "", f"Public domain · DPLA · {WC}", {"style": "print", "label": "A 6th Ranger Battalion sergeant visits a freed prisoner, 1945"}),
    (67, "Staff Sergeant Clinton", None, "sc201653_wing.jpg", "67", "", "", f"Signal Corps SC 201653 · NARA · public domain · {WC}", {"style": "print", "label": "Maj. Paul W. Wing (bareheaded) with two friends after his release from Cabanatuan"}),
    (69, "Some had lost", None, "pows_hospital.jpg", "69", "", "", f"Signal Corps · NARA 531251 · public domain · {WC}", {"style": "print", "label": "Freed Cabanatuan prisoners on the porch of an emergency hospital, 1945"}),
    (79, "He died in Florida", None, "mucci_grave.jpg", "79", "", "", f"Public domain · {WC}", {"style": "print", "label": "Col. Henry A. Mucci's grave, West Point"}),
    (85, "The camp is gone", None, "raid_site_jf.jpg", "85", "", "", f"Ramon FVelasquez · CC0 · {WC}", {"style": "print", "label": "The Camp Pangatian memorial shrine today"}),
    (85, "On the site stands", None, "memorial_flickr.jpg", "85", "", "", f"U.S. Embassy in the Philippines · public domain · {WC}", {"style": "print", "label": "The Cabanatuan American Memorial"}),
    (85, "Its wall carries", None, "memorial_flickr1.jpg", "85", "", "", f"U.S. Embassy in the Philippines · public domain · {WC}", {"style": "print", "label": "A plaque at the memorial"}),
    (86, "Among them were Rangers", None, "wreath_2014.jpg", "86", "", "", f"U.S. Marine Corps photo · public domain · {WC}", {"style": "print", "label": "U.S. and Philippine troops at the Pangatian memorial, 2014"}),
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
                    card["end"] = min(card["start"] + (15.0 if card["type"] == "QuoteCard" else 12.0), max(card["start"] + 7.0, paras[pi]["end"] + 0.3))
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
