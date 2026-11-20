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
    "LST": ("un-un-5240x2", 0.80), "BAL": ("un-un-5196x2", 0.86), "F3": ("un-un-5196x3", 0.86), "D16": ("111-adc-5680", 1),
    "D16B": ("111-adc-5678", 1), "D4": ("homma_trial_day4", 1), "D4B": ("homma_trial_day4b", 1), "PAT": ("111-adc-3516", 1),
    "NWS": ("homma_newsreel_jan1946", 1), "ZIM": ("pow_interviews_sendai_1945", 1), "REL": ("released_pows_japan_1945", 1),
    "YOK": ("111-adc-5327", 1), "NUR": ("111-adc-3381", 1), "MAC": ("111-adc-9825", 1), "SUR": ("111-adc-5186", 1),
    "JPN": ("npc323_japanese_newsreel_1943", 1), "WAI": ("wainwright_home_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
TR = "Record of trial, U.S.A. v. Masaharu Homma, Manila 1946 (UNWCC microfilm, archive.org)"
TRC = "U.S.A. v. Masaharu Homma, record of trial · UNWCC microfilm, case 184 · archive.org"
AP = "Associated Press, 1946"
MOR = "Louis Morton, The Fall of the Philippines (U.S. Army, 1953)"
COOK = "Peter B. Cook, American History (1996), from Lt. Robert Pelz's diary"
REV = "MacArthur's review of the sentence, 21 March 1946 (AP text)"
SC = "Homma v. Patterson, 327 U.S. 759 (1946)"

LST_TAG = "The Homma trial, Manila, February 1946 · Fox newsreel film (NARA UN-UN-5240)"
FUJ_TAG = "Fujiko Homma on the witness stand, Manila, 7 February 1946 · Fox newsreel film (NARA UN-UN-5240)"
HOM_TAG = "Gen. Homma testifies, Manila, February 1946 · Fox newsreel film (NARA UN-UN-5240)"
BAL_TAG = "A U.S. officer at the Bataan map, Homma trial, January 1946 · Fox newsreel film (NARA UN-UN-5196)"
F3_TAG = "A witness at the Homma trial, Manila, January 1946 · Fox newsreel film (NARA UN-UN-5196)"
D16_TAG = "Prosecution witness, Homma trial, 21 January 1946 · Signal Corps film (111-ADC-5680)"
D4_TAG = "A witness at the Homma trial, 7 January 1946 · Signal Corps film (111-ADC-5637)"
D4B_TAG = "Gen. Homma at the defense table, 7 January 1946 · Signal Corps film (ADC-3516)"
NWS_TAG = "The Homma trial, Manila, January 1946 · United Newsreel"
ZIM_TAG = "Chaplain Leslie Zimmerman, freed POW, Sendai Camp No. 3, Japan, 1945 · Signal Corps film (ADC-5281) · original sound"
REL_TAG = "Freed American prisoners of war, Japan, September 1945 · Army film (CS-4554)"
YOK_TAG = "Freed prisoners of war, Yokohama, 20 September 1945 · Signal Corps film (111-ADC-5327)"
NUR_TAG = "Army nurses captured on Bataan and Corregidor, freed in 1945 · Signal Corps film (111-ADC-3381)"
MAC_TAG = "Gen. Douglas MacArthur in the Philippines, 1945 · Signal Corps film (111-ADC-9825)"
SUR_TAG = "Japanese troops surrender on Luzon, 1945 · Signal Corps film (111-ADC-5186)"
BTN_TAG = "MacArthur's plane, named Bataan, 1945 · Signal Corps film (111-ADC-5186)"
JPN_TAG = "Japanese newsreel of the fall of Corregidor, 1942 (captured film, NARA NPC-323)"
JPNP_TAG = "American prisoners on Corregidor, May 1942 · Japanese newsreel (captured film, NARA NPC-323)"
WAI_TAG = "Gen. Jonathan Wainwright comes home, September 1945 · newsreel"
STAND = "Stand-in · "

MNL = [120.984, 14.599]; LIN = [120.33, 16.05]; MAR = [120.49, 14.44]; BLG = [120.536, 14.677]; SFE = [120.689, 15.035]
CAP = [120.59, 15.335]; ODN = [120.535, 15.36]; COR = [120.575, 14.385]; LMO = [120.51, 14.515]; LBN = [121.24, 14.17]

ROUTE = {"type": "GlobeMap", "theme": "history",
         "cam": [{"t": 0, "center": [120.7, 14.9], "scale": 70}, {"t": "The prisoners would gather", "center": [120.62, 14.88], "scale": 150}],
         "pins": [{"ll": MAR, "label": "Mariveles", "at": 0.6}, {"ll": BLG, "label": "Balanga", "at": "would gather"},
                  {"ll": SFE, "label": "San Fernando", "at": "walk north"}, {"ll": CAP, "label": "Capas", "at": "boxcars", "color": "amber"},
                  {"ll": ODN, "label": "Camp O'Donnell", "at": "a last walk", "color": "red"}, {"ll": COR, "label": "Corregidor", "at": 1.2, "color": "west"}],
         "arcs": [{"from": MAR, "to": BLG, "at": "would gather", "style": "dashed", "color": "red", "loft": 0.0, "draw": 30},
                  {"from": BLG, "to": SFE, "at": "walk north", "style": "dashed", "color": "red", "loft": 0.0, "draw": 40},
                  {"from": SFE, "to": CAP, "at": "boxcars", "style": "solid", "color": "amber", "loft": 0.02, "draw": 30},
                  {"from": CAP, "to": ODN, "at": "a last walk", "style": "dashed", "color": "red", "loft": 0.0, "draw": 20}],
         "cards": [{"at": "sixty-five miles", "kicker": "April 1942", "body": "About 65 miles on foot, Mariveles to San Fernando", "accent": "red"}],
         "footer": "Route generalised · after Morton (1953) and Falk (1962)", "year": {"at": 0.1, "year": "1942", "sub": "The road out of Bataan"}}

LUZON = {"type": "GlobeMap", "theme": "history",
         "cam": [{"t": 0, "center": [121, 15.3], "scale": 18}, {"t": "pulled back into", "center": [120.6, 14.7], "scale": 70}],
         "pins": [{"ll": LIN, "label": "Lingayen Gulf", "at": "came ashore"}, {"ll": MNL, "label": "Manila", "at": "Manila had fallen"},
                  {"ll": [120.5, 14.62], "label": "Bataan", "at": "the Bataan peninsula", "color": "red"},
                  {"ll": COR, "label": "Corregidor", "at": "Manila Bay", "color": "west"}],
         "arcs": [{"from": LIN, "to": MNL, "at": "came ashore", "style": "solid", "color": "red", "loft": 0.03, "draw": 40}],
         "cards": [{"at": "came ashore", "kicker": "22 December 1941", "body": "Homma's 14th Army lands at Lingayen Gulf", "accent": "red"}],
         "footer": "Japanese landing generalised", "year": {"at": 0.1, "year": "1941", "sub": "Luzon"}}

LOSB = {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [121.1, 14.4], "scale": 90}],
        "pins": [{"ll": MNL, "label": "Manila", "at": 0.5}, {"ll": LBN, "label": "Los Baños", "at": 1.0, "color": "red"}],
        "arcs": [{"from": MNL, "to": LBN, "at": 1.0, "style": "dashed", "color": "red", "loft": 0.03, "draw": 30}],
        "footer": "Execution site per AP, 3 April 1946", "year": {"at": 0.1, "year": "1946", "sub": "Los Baños, Laguna"}}

# reconstruction: Homma's headquarters near the road at Balanga (ground world 3000 x 1500, surface 820)
HQ = {"type": "Section", "world": "ground", "W": 3000, "H": 1500, "surface": 820,
      "date": "Balanga, Bataan · April 1942", "place": "Reconstruction · distance from Takatsu's testimony, 3 January 1946",
      "cam": [{"t": 0, "x": 1500, "y": 760, "z": 0.62}, {"t": "put it about five hundred", "x": 1500, "y": 760, "z": 0.7}],
      "items": [{"kind": "hut", "x": 2500, "y": 820, "w": 520, "label": "14th Army headquarters", "labelAt": "headquarters was at", "labelTo": 30},
                {"kind": "man", "x": 200, "y": 820, "pose": "walk", "move": [{"t": 0, "x": 200, "y": 820}, {"t": 17, "x": 1300, "y": 820}]},
                {"kind": "man", "x": 80, "y": 820, "pose": "walk", "move": [{"t": 0, "x": 80, "y": 820}, {"t": 17, "x": 1180, "y": 820}]},
                {"kind": "man", "x": -40, "y": 820, "pose": "walk", "label": "Prisoners on the road", "labelAt": "on the route", "labelTo": 30,
                 "move": [{"t": 0, "x": -40, "y": 820}, {"t": 17, "x": 1060, "y": 820}]},
                {"kind": "man", "x": -160, "y": 820, "pose": "walk", "move": [{"t": 0, "x": -160, "y": 820}, {"t": 17, "x": 940, "y": 820}]},
                {"kind": "man", "x": -280, "y": 820, "pose": "walk", "move": [{"t": 0, "x": -280, "y": 820}, {"t": 17, "x": 820, "y": 820}]}],
      "pills": [{"t0": "five hundred meters", "t1": 30, "text": "About 500 m from the road", "y": 230}],
      "source": f"{TR}, 3 Jan 1946 (Takatsu)"}

CHAPTER_DATES = [("9 Apr 1942", "Bataan surrenders · the march begins"), ("Aug 1942", "Homma relieved, sent home to Japan"),
                 ("3 Jan 1946", "The trial opens"), ("11 Feb 1946", "Verdict and sentence"),
                 ("3 Apr 1946", "Shot at Los Baños")]

P = [
    # 0 the ballroom
    [("Manila, the ninth", "NWS", 15.8), ("@", "Manila, the ninth", NWS_TAG), ("#", "Manila, the ninth", None, SLUG("9 January 1946 · Manila", "U.S.A. v. Masaharu Homma, sixth day")),
     ("Five generals sit", "NWS", 30.4), ("In front of them", "BAL", 44.0), ("@", "In front of them", BAL_TAG)],
    # 1 Baldassarre
    [("His name is", "BAL", 93.0), ("Four years earlier", "D16B", 394.0), ("@", "Four years earlier", "The courtroom, 21 January 1946 · Signal Corps film (111-ADC-5678)"), ("The prosecutor asks", "BAL", 118.0),
     ("#", "The prosecutor asks", None, LQ("FILE 01 — TESTIMONY", "BETWEEN MARIVELES AND BALANGA", "No food, no water.", "M/Sgt. James Baldassarre, 9 January 1946", TR, before="No, sir; ", after=""))],
    # 2 the bodies
    [("He describes the bodies", "BAL", 131.0), ("#", "He describes the bodies", None, QC("stills/odonnell_litters.jpg", [("Many of them;", "Many of them"), ("hundreds of them.", "Hundreds of them"), ("God knows how many of them!", "God knows how many")],
        "M/Sgt. James Baldassarre, testimony, 9 January 1946", "God knows how many"))],
    # 3 identification
    [("There is one right", "D4B", 26.5), ("@", "There is one right", D4B_TAG),
     ("#", "There is one right", None, DESK("stills/tr_baldassarre_paper.png", 1.6376, [(0, "wide", [0.5, 0.75]), ("that I can recognize", "glide", [0.94, 0.12, 0.75])], "Record of trial, U.S.A. v. Homma, p. 876 (9 Jan 1946) · UNWCC microfilm, archive.org")),
     ("A reporter for", "D4B", 59.5)],
    # 4 this is the documented story
    [("This is the documented", "LST", 5.0), ("@", "This is the documented", LST_TAG), ("the young lawyers", "D4B", 112.0), ("the wife who stood", "LST", 214.0),
     ("a Supreme Court justice", "SUR", 410.0), ("and General Douglas", "MAC", 21.0), ("@", "and General Douglas", MAC_TAG)],
    # 5 sources
    [("Most of what you", "LST", 476.0), ("#", "Most of what you", None, TL("FILE 02 — THE CASE", "From Bataan to the firing squad", CHAPTER_DATES, f"{TR}; {AP}"))],
    # 6 poet general (photo)
    [("was not the kind", "NWS", 40.4), ("@", "was not the kind", "Gen. Homma at his trial, Manila, January 1946 · United Newsreel"), ("He wrote poetry", "NWS", 26.0)],
    # 7 Lingayen (map)
    [("In December", "SUR", 30.0), ("#", "In December", None, LUZON)],
    # 8 held Bataan
    [("They held Bataan", "NUR", 126.0), ("@", "They held Bataan", NUR_TAG), ("Malaria and dysentery", "NUR", 30.0),
     ("In March", "MAC", 313.0), ("@", "In March", STAND + MAC_TAG), ("The men he left", "NUR", 255.5)],
    # 9 finished
    [("By early April", "NUR", 277.0), ("@", "By early April", STAND + "Casualties evacuated, Philippines, 1945 · Signal Corps film (111-ADC-3381)"), ("#", "Major", None, BARS("FILE 03 — BATAAN, APRIL 1942", "The army that surrendered", [
        ("Sick: malaria, dysentery, exhaustion", 43, "43 %", "Maj. Achille Tisdelle, testimony"), ("Rations", 25, "1/4", "King's sworn statement"),
        ("Food left at the surrender", 2, "2 days", "King's sworn statement")], 100, f"{TR}, 21 Jan and 7 Feb 1946"))],
    # 10 King goes forward
    [("The commander on", "BAL", 160.0), ("@", "The commander on", BAL_TAG), ("#", "The commander on", None, SLUG("9 April 1942 · Lamao, Bataan", "Maj. Gen. Edward King goes forward under a white flag")),
     ("Later that morning", "D16B", 45.0), ("Japanese planes strafed", "BAL", 180.0)],
    # 11 Nakayama
    [("Near the village", "D16", 107.0), ("first question was whether", "WAI", 79.0), ("@", "first question was whether", WAI_TAG), ("He was not", "WAI", 12.0)],
    # 12 not barbarians
    [("King had come", "D16", 140.0), ("#", "In a sworn statement", None, QC("stills/corregidor_surrender_1942.jpg", [("The Imperial Japanese Army", "The Imperial Japanese Army"), ("are not barbarians.", "are not barbarians")],
        "Japanese envoy to Maj. Gen. Edward King, 9 April 1942 · King's sworn statement, read at the trial", "With that assurance"))],
    # 13 cigarette
    [("At the table", "D16B", 394.0), ("King and his staff", "D16B", 410.0)],
    # 14 largest force
    [("General King knew", "BAL", 205.0), ("#", "The Army's official history", None, BARS("FILE 04 — THE SURRENDER", "Forces left on Bataan, 9 April 1942", [
        ("Filipino troops", 66, "~66,000", ""), ("American troops", 12, "~12,000", "")], 80, f"{MOR}; estimates differ"))],
    # 15 the plan
    [("The Japanese plan", "SUR", 30.0), ("@", "The Japanese plan", STAND + SUR_TAG),
     ("#", "staff officer", None, BARS("FILE 05 — THE PLAN", "Prisoners the Japanese planned for, and got", [
         ("Japanese plan, March 1942", 40, "40,000", ""), ("Expected (Takatsu)", 30, "30,000", ""), ("Appeared (Takatsu)", 60, "60,000+", "")], 80,
         "Plan: Falk (1962) via Herman (2002); Takatsu, testimony 4 Jan 1946"))],
    # 16 route map
    [("The plan itself", "BAL", 56.0), ("#", "The plan itself", None, ROUTE)],
    # 17 John Ball
    [("What it was like", "BAL", 160.0), ("Colonel John Ball", "BAL", 205.0), ("He marched bareheaded", "F3", 197.0)],
    # 18 baby crying
    [("Ball saw a Filipino", "F3", 210.0), ("@", "Ball saw a Filipino", F3_TAG),
     ("#", "This Filipino made", None, DESK("stills/tr_ball_paper.png", 1.6324, [(0, "glide", [0.33, 0.12, 0.7]), ("Made a noise like", "glide", [0.36, 0.1, 0.6])], "Record of trial, U.S.A. v. Homma, p. 908 (10 Jan 1946) · UNWCC microfilm, archive.org"))],
    # 19 Waterous / Clark
    [("Lieutenant Colonel Willard", "NUR", 159.0), ("@", "Lieutenant Colonel Willard", STAND + "Bataan and Corregidor casualties evacuated, 1945 · Signal Corps film (111-ADC-3381)"),
     ("Technical Sergeant Horace", "F3", 230.0)],
    # 20 Pantingan
    [("The Filipino officers", "F3", 100.0), ("@", "The Filipino officers", F3_TAG), ("The guards put", "F3", 116.0),
     ("#", "I was bayoneted", None, QC("stills/death_march_tied.jpg", [("I was bayoneted", "I was bayoneted"), ("four times, sir.", "four times")], "Capt. Pedro L. Felix, Pantingan River survivor · testimony, 10 January 1946", "four times"))],
    # 21 Vargas
    [("His countryman", "F3", 300.0), ("#", "His countryman", None, LQ("FILE 06 — PANTINGAN RIVER", "MAJ. EDUARDO T. VARGAS, 11 JAN 1946", "even tried not to breathe", "Maj. Eduardo T. Vargas, testimony", TR,
        before="I didn't move, and ", after=" so that they wouldn't notice that I was alive."))],
    # 22 Zimmerman intro
    [("Three years after", "YOK", 40.0), ("@", "Three years after", YOK_TAG), ("He was a chaplain", "ZIM", 30.0), ("@", "He was a chaplain", ZIM_TAG)],
    # 23 Zimmerman's own voice (clip: source 89.4 s plays in sync)
    [("Well, after the", "ZIM", 89.3)],
    # 24 O'Donnell
    [("The march ended", "REL", 25.0), ("@", "The march ended", STAND + REL_TAG),
     ("#", "An Army report written", None, BARS("FILE 07 — CAMP O'DONNELL", "Dead at Camp O'Donnell, 1942", [
         ("Filipino prisoners", 22000, "about 22,000", ""), ("American prisoners", 1500, "about 1,500", "")], 24000,
         "Provost Marshal General, report of 19 Nov 1945 (variants up to 2,200 and 27,000)")),
     ("Men collapsed from", "REL", 35.0)],
    # 25 how many died
    [("How many died", "REL", 105.0), ("#", "Historians' estimates", None, BARS("FILE 08 — THE MARCH", "Estimates of the dead on the march itself", [
        ("Lower estimate", 5000, "about 5,000", "historians"), ("Higher estimate", 10000, "10,000+", "historians"),
        ("Prosecution, 1946 (march and first camp)", 17000, "17,000", "")], 18000, "Falk (1962) via Herman (2002); prosecution charge, AP 9 Jan 1946")),
     ("None of them is exact", "REL", 124.0)],
    # 26 the HQ (reconstruction)
    [("And where was", "LST", 85.0), ("#", "headquarters was at", None, HQ)],
    # 27 January 1944
    [("For almost two years", "NUR", 300.0), ("#", "Only in January", None, HL("JANUARY 1944", "The words", "Death March", "entered American newspapers", "Herman (2002): War Department release of escapees' accounts"))],
    # 28 MacArthur back
    [("MacArthur came back", "MAC", 290.0), ("@", "MacArthur came back", MAC_TAG), ("Manila was retaken", "MAC", 330.0), ("In August Japan", "SUR", 160.0), ("@", "In August Japan", SUR_TAG),
     ("In September", "SUR", 400.0), ("@", "In September", BTN_TAG)],
    # 29 the commission (photo)
    [("On the fifth of December", "SUR", 415.0), ("On the twelfth", "PAT", 238.0), ("@", "On the twelfth", "Arrival at the Homma trial, Manila, January 1946 · Signal Corps film (111-ADC-3516)"), ("Five generals were appointed", "D4", 21.0), ("Brigadier Generals Robert", "NWS", 30.4)],
    # 30 the charge
    [("The charge was", "D4B", 6.0), ("#", "The charge was", None, HL("THE CHARGE", "One charge,", "48 specifications", "forty-eight specifications", TR)),
     ("Nobody claimed", "D4B", 79.0), ("The question in front", "NWS", 45.0)],
    # 31 defense lawyers
    [("His defense was given", "NWS", 40.0), ("@", "His defense was given", NWS_TAG), ("The chief was Major", "D4B", 35.0), ("According to a", "D4B", 46.0), ("One of his team", "NWS", 26.0)],
    # 32 Pelz diary
    [("Pelz wrote that", "D4B", 59.0), ("#", "Pelz wrote that", None, QC("stills/homma_kuroda_1945.jpg", [("a tired-out grandfather", "a tired-out grandfather"), ("who has girded his loins", "girded his loins"), ("for a last battle", "for a last battle")],
        "Lt. Robert Pelz, defense counsel · diary, 16 December 1945 (via Cook, 1996)", "for a last battle")),
     ("The lawyers had", "D4B", 120.0)],
    # 33 defense objection
    [("The defense also", "NWS", 51.0), ("The man who had ordered", "MAC", 300.0), ("@", "The man who had ordered", MAC_TAG), ("#", "Their motion said", None, LQ("FILE 09 — DEFENSE MOTION", "MANILA, DECEMBER 1945", "accuser, prosecutor, defense counsel, judge, jury, court of review and court of final appeal",
        "The defense, objecting to MacArthur's role", COOK, before="No one man should be ", after="")), ("The trial went ahead", "D4B", 120.0)],
    # 34 the trial opens
    [("The trial opened", "LST", 5.0), ("@", "The trial opened", LST_TAG), ("#", "The trial opened", None, SLUG("3 January 1946 · Manila", "The High Commissioner's Residence")),
     ("He told the court", "D4B", 26.0), ("He then described", "LST", 30.0)],
    # 35 136 witnesses
    [("Over the next three", "D4", 49.0), ("@", "Over the next three", D4_TAG),
     ("#", "Over the next three", None, {"type": "IconCount", "icon": "man", "total": 136, "label": "Prosecution witnesses, 3 to 21 January 1946",
        "accent": "witnesses", "file": "FILE 10 — THE WITNESSES", "source": "Herman (2002), after Hanson (1977) and Taylor (1981)"}),
     ("Americans and Filipinos", "D4", 70.0)],
    # 36 Taylor
    [("The historian Lawrence", "D4", 120.0), ("#", "The historian Lawrence", None, LQ("FILE 11 — THE OBJECTION", "WHAT THE WITNESSES DID NOT SAY", "Not one witness mentioned Homma in connection with any particular atrocity.",
        "Lawrence Taylor, A Trial of Generals (1981)", "Quoted in Herman, Military Law Review (2002)")), ("Its case was", "D4", 180.0)],
    # 37 Baldassarre again
    [("On the ninth of January", "BAL", 68.0), ("@", "On the ninth of January", BAL_TAG), ("The reporters wrote", "D4B", 112.0), ("@", "The reporters wrote", D4B_TAG),
     ("#", "Outside the courtroom", None, QC("stills/death_march_tied.jpg", [("They should never give him a trial.", "They should never give"), ("He never gave us no trial.", "He never gave us")],
        "M/Sgt. James Baldassarre to a reporter, January 1946 (Time, via Cook 1996)", "He never gave us"))],
    # 38 Felix's scars
    [("The next day it was", "F3", 143.0), ("@", "The next day it was", F3_TAG), ("He stood, turned", "F3", 156.0), ("On the same day", "BAL", 220.0)],
    # 39 Fujiko arrives
    [("On the fourteenth", "LST", 436.0), ("@", "On the fourteenth", "Outside the High Commissioner's Residence, Manila, 1946 · Fox newsreel film (NARA UN-UN-5240)"), ("She was", "LST", 342.0)],
    # 40 Pugh
    [("On the twenty-first", "D16", 22.0), ("@", "On the twenty-first", D16_TAG), ("The other was Colonel", "D16", 40.0), ("was shown a captured", "D16", 60.0)],
    # 41 Pugh's nightmare
    [("General", "D16", 80.0), ("#", "Of those last days", None, DESK("stills/tr_pugh_paper.png", 1.6441, [(0, "glide", [0.44, 0.12, 0.72])], "Record of trial, U.S.A. v. Homma, p. 2365 (21 Jan 1946) · UNWCC microfilm, archive.org")),
     ("With that, the prosecution", "D16", 140.0)],
    # 42 defense witnesses
    [("The defense called Japanese", "LST", 20.0), ("A Japanese censor", "LST", 45.0)],
    # 43 Homma on the stand
    [("Then, on the fifth", "LST", 62.0), ("@", "Then, on the fifth", HOM_TAG), ("He told the court", "LST", 85.0), ("He had trained", "LST", 112.0)],
    # 44 not looking
    [("He was asked about", "LST", 130.0), ("#", "He was asked about", None, DESK("stills/tr_homma_notlooking_paper.png", 1.5406, [(0, "wide", [0.5, 0.5]), ("However", "glide", [0.511, 0.15, 0.7])], "Record of trial, U.S.A. v. Homma, p. 3080 (5 Feb 1946) · UNWCC microfilm, archive.org"))],
    # 45 Meek
    [("The next day the chief", "LST", 160.0), ("#", "You knew you had", None, LQ("FILE 12 — CROSS-EXAMINATION", "6 FEBRUARY 1946", "I did not.", "Gen. Homma, asked by Col. Frank Meek", AP,
        before="Did you inquire as to the physical condition of the prisoners? — ", after=""))],
    # 46 morally responsible
    [("admitted that a general", "LST", 172.0), ("#", "And he said a sentence", None, DESK("stills/tr_homma_moral_paper.png", 1.6218, [(0, "glide", [0.53, 0.1, 0.62])], "Record of trial, U.S.A. v. Homma, p. 3144 (6 Feb 1946) · UNWCC microfilm, archive.org"))],
    # 47 ashamed
    [("On the morning of the seventh", "LST", 100.0), ("#", "I came to know", None, QC("stills/homma_stand_b.jpg", [("I came to know for the first time", "I came to know"), ("in the court of such atrocities,", "in the court of such"),
        ("and I am ashamed of myself", "and I am ashamed")], "Gen. Masaharu Homma, testimony, 7 February 1946", "should these atrocities"))],
    # 48 Fujiko testifies
    [("That afternoon", "LST", 208.0), ("@", "That afternoon", FUJ_TAG), ("He had disagreed", "LST", 233.0), ("Japan had politicians", "LST", 246.0)],
    # 49 his views
    [("Military force", "LST", 260.0), ("He liked reading", "LST", 274.0), ("Then she said the line", "LST", 288.0)],
    # 50 the line (transcript page)
    [("I have come from", "LST", 301.0), ("#", "I have come from", None, DESK("stills/tr_fujiko_paper.png", 1.5365, [(0, "glide", [0.77, 0.15, 0.68]), ("I have one daughter", "glide", [0.80, 0.1, 0.7])], "Record of trial, U.S.A. v. Homma, p. 3281 (7 Feb 1946) · UNWCC microfilm, archive.org"))],
    # 51 tears, no questions
    [("Lieutenant Pelz wrote", "LST", 342.0), ("Colonel Meek said", "LST", 355.0), ("Major Skeen announced", "LST", 369.0)],
    # 52 King's statement
    [("A few minutes later", "LST", 382.0), ("#", "In it King said", None, LQ("FILE 13 — EXHIBIT 425", "SWORN STATEMENT OF MAJ. GEN. EDWARD P. KING JR., 14 JAN 1946", "I have never seen him in my life", "Maj. Gen. Edward King, on General Homma", TR, after=" so far as I know."))],
    # 53 subscribe
    [("If stories like this", "D4", 340.0), ("#", "take a moment", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": CHANNEL["tagline"]})],
    # 54 closing arguments
    [("The closing arguments", "LST", 476.0), ("#", "Major Skeen told", None, QC("stills/homma_commission_listen.jpg", [("an indictment not of an individual", "an indictment"), ("but of the system", "but of the system"), ("of the Japanese Army", "of the Japanese Army")],
        "Maj. John H. Skeen Jr., defense closing, 9 February 1946", "Lieutenant Pelz said")), ("in civilian clothes", "LST", 490.0)],
    # 55 Meek answers
    [("Then Colonel Meek", "LST", 503.0), ("#", "Someone is to blame", None, DESK("stills/tr_meek_paper.png", 1.5429, [(0, "glide", [0.42, 0.12, 0.72])], "Record of trial, U.S.A. v. Homma, p. 3358 (9 Feb 1946) · UNWCC microfilm, archive.org"))],
    # 56 screams
    [("Meek reminded the court", "LST", 516.0), ("#", "If he had cared", None, QC("stills/odonnell_litters.jpg", [("he could have heard the screams", "he could have heard the screams"), ("of the wounded and the dying.", "of the wounded")],
        "Col. Frank E. Meek, prosecution closing, 9 February 1946", "And water, he said"))],
    # 57 the verdict
    [("On the eleventh of February", "LST", 556.0), ("@", "On the eleventh of February", "Gen. Homma before the commission, 11 February 1946 · Fox newsreel film (NARA UN-UN-5240)"),
     ("#", "On the eleventh of February", None, SLUG("11 February 1946 · 3:00 p.m.", "The verdict")), ("The record shows", "LST", 570.0)],
    # 58 the sentence
    [("was allowed to speak", "LST", 608.0), ("#", "Then General Donovan", None, DESK("stills/tr_sentence_paper.png", 1.4771, [(0, "wide", [0.5, 0.6]), ("to be shot", "glide", [0.745, 0.1, 0.7])], "Record of trial, U.S.A. v. Homma, p. 3365 (11 Feb 1946) · UNWCC microfilm, archive.org"))],
    # 59 firing squad, Trudeau
    [("A firing squad", "LST", 622.0), ("One of his lawyers", "D4B", 6.0), ("#", "Years later one of", None, QC("stills/homma_commission_standing.jpg", [("I would not vote to hang him.", "he would not vote"), ("I thought he was an outstanding soldier.", "That is his memory")],
        "Brig. Gen. Arthur Trudeau, commission member · Engineer Memoirs (1986), via Cook 1996", "That is his memory"))],
    # 60 Tisdelle
    [("Major", "LST", 530.0), ("#", "There are twenty-four hundred", None, QC("stills/death_march_tied.jpg", [("There are 2,400 Americans", "There are twenty-four hundred"), ("and 29,000 Filipinos", "and twenty-nine thousand"),
        ("in this court room, too,", "in this court room"), ("but you can't see them.", "but you can't see")], "Maj. Achille C. Tisdelle, 11 February 1946 (AP)", "but you can't see"))],
    # 61 Supreme Court
    [("On the very same day", "LST", 7.0), ("#", "On the very same day", None, HL("SUPREME COURT OF THE UNITED STATES · 11 FEB 1946", "Homma v. Patterson:", "denied, 6 to 2", "six votes to two", SC))],
    # 62 Murphy
    [("Justice Frank Murphy", "LST", 30.0), ("#", "Justice Frank Murphy", None, QC("stills/supreme_court_stone.jpg", [("Either we conduct such a trial", "Either we conduct"), ("in the noble spirit of our Constitution,", "in the noble spirit"),
        ("or we abandon all pretense to justice", "or we abandon"), ("and descend to the level", "and descend"), ("of revengeful blood purges.", "revengeful blood purges")], "Justice Frank Murphy, dissenting · Homma v. Patterson, 11 February 1946", "revengeful blood purges"))],
    # 63 not innocent
    [("Murphy did not say", "NWS", 20.0), ("What troubled him", "NWS", 33.0),
     ("#", "But tomorrow the precedent", None, LQ("FILE 14 — THE DISSENT", "JUSTICE FRANK MURPHY", "tomorrow the precedent here established can be turned against others.", "Justice Frank Murphy, dissenting", SC, before="There will be few to protest. But "))],
    # 64 Rutledge
    [("Justice Wiley Rutledge", "NWS", 45.0), ("#", "Justice Wiley Rutledge", None, LQ("FILE 15 — THE DISSENT", "JUSTICE WILEY RUTLEDGE", "vitiate the entire proceeding.", "Justice Wiley Rutledge, dissenting", SC,
        before="These provisions of the directive ordering the creation of the commission in my judgment "))],
    # 65 MacArthur's review
    [("There was one man", "MAC", 313.0), ("@", "There was one man", MAC_TAG), ("The sentence had to", "SUR", 450.0), ("@", "The sentence had to", BTN_TAG)],
    # 66 Fujiko meets MacArthur
    [("On the eleventh of March", "LST", 221.0), ("#", "On the eleventh of March", None, SLUG("11 March 1946 · Tokyo", "Fujiko Homma is received by General MacArthur")),
     ("According to the Associated", "LST", 246.0), ("@", "According to the Associated", FUJ_TAG), ("But she did not ask", "LST", 260.0)],
    # 67 Furness
    [("She asked him to look", "NWS", 40.0), ("#", "He told reporters", None, LQ("FILE 16 — TOKYO, 11 MARCH 1946", "CAPT. GEORGE FURNESS, DEFENSE COUNSEL", "This was not a plea for mercy", "Capt. George A. Furness", AP, after=" and no begging for Homma's life.")),
     ("MacArthur, he said", "MAC", 21.0)],
    # 68 most trying
    [("MacArthur's own statement", "MAC", 340.0), ("#", "No incident, he said", None, LQ("FILE 17 — MACARTHUR TO THE PRESS", "ON MRS. HOMMA", "the utter evil of war", "Gen. Douglas MacArthur, press statement, March 1946", "Quoted in Cook (1996)",
        before="No incident could more deeply illustrate ", after=" and its dreadful consequences upon those like her who had no part in it."))],
    # 69 repugnant duty
    [("Ten days later", "MAC", 313.0), ("#", "It began", None, QC("stills/macarthur_manila_1945.jpg", [("I am again confronted", "I am again confronted"), ("with the repugnant duty", "with the repugnant duty"),
        ("of passing final judgment", "of passing final judgment"), ("on a former adversary.", "on a former adversary")], "Gen. Douglas MacArthur, review of the sentence, 21 March 1946", "in a major military"))],
    # 70 honors of war
    [("The proceedings showed", "MAC", 326.0), ("#", "Of the men who had", None, LQ("FILE 18 — THE REVIEW", "ON THE DEFENDERS OF BATAAN", "none deserved more the honors of war in their final hour of final agony.", "Gen. Douglas MacArthur, 21 March 1946", REV,
        before="Of all fighting men of all time, "))],
    # 71 the leader is the essence
    [("Then he set down", "MAC", 340.0), ("#", "Soldiers of an army", None, QC("stills/macarthur_1945.jpg", [("Soldiers of an army invariably reflect", "Soldiers of an army"), ("the attitude of their general.", "the attitude of their general"),
        ("The leader is the essence.", "The leader is the essence")], "Gen. Douglas MacArthur, review of the sentence, 21 March 1946", "Isolated crimes"))],
    # 72 judicial fate
    [("He answered the two", "MAC", 355.0), ("#", "If this defendant", None, HL("MACARTHUR, 21 MARCH 1946", "If this defendant does not deserve his", "judicial fate,", "his judicial fate", REV, after=" none in jurisdictional history ever did."))],
    # 73 confirmed; Narahashi
    [("MacArthur confirmed", "SUR", 450.0), ("@", "MacArthur confirmed", BTN_TAG), ("#", "In Tokyo the chief", None, LQ("FILE 19 — TOKYO", "WATARU NARAHASHI, CHIEF CABINET SECRETARY", "a commanding general, even if he himself doesn't issue orders, must assume responsibility for illegal acts of his subordinates.",
        "Wataru Narahashi, 21 March 1946", AP, before="The Japanese now know that "))],
    # 74 Hisako
    [("daughter", "LST", 288.0), ("#", "Today's verdict", None, LQ("FILE 20 — TOKYO", "HOMMA'S DAUGHTER, 18", "Today's verdict is of human making, not of God's.", "Hisako Homma, 21 March 1946", AP))],
    # 75 letter to lawyers
    [("had already written", "D4B", 59.0), ("@", "had already written", D4B_TAG), ("#", "they had left no stone", None, LQ("FILE 21 — HOMMA TO HIS LAWYERS", "THE EVE OF THE VERDICT", "a fair trial which I know is denied to me from the outset",
        "Gen. Masaharu Homma, letter to his defense team", COOK, before="…leaving no stone unturned to give me ", after="."))],
    # 76 message home
    [("Through the Japanese", "LST", 60.0), ("#", "I know I cannot", None, QC("stills/homma_portrait.jpg", [("I want to go, the earlier the better,", "I want to go"), ("to the place where Japanese soldiers fell", "to the place where"),
        ("and where American soldiers sleep.", "and where American soldiers")], "Gen. Masaharu Homma, message to Japan's chief cabinet secretary, March 1946 (AP)", "and where American soldiers"))],
    # 77 Los Baños (map)
    [("He was taken to", "LST", 449.0), ("#", "He was taken to", None, LOSB)],
    # 78 the execution
    [("Shortly before one", "LST", 462.0), ("#", "Shortly before one", None, SLUG("3 April 1946 · about 1:00 a.m.", "Los Baños, Laguna")), ("An officer read", "LST", 436.0)],
    # 79 no final statement
    [("He made no final", "LST", 449.0), ("Not far away", "NUR", 378.0), ("@", "Not far away", STAND + "Army ambulances, Philippines, 1945 · Signal Corps film (111-ADC-3381)")],
    # 80 Kawane and Hirano
    [("was not the only one", "LST", 7.0), ("#", "The two officers", None, TL("FILE 22 — AFTER HOMMA", "The others", [("23 Feb 1946", "Gen. Tomoyuki Yamashita hanged at Los Baños"),
        ("3 Apr 1946", "Lt. Gen. Hikotaro Tajima hanged, 30 minutes after Homma"), ("12 Jun 1949", "Kawane and Hirano, who planned the prisoners' movement, hanged at Sugamo")], f"{AP}; Ginn, Sugamo Prison (via Wikipedia)"))],
    # 81 justice or revenge
    [("Was it justice", "NWS", 20.0), ("#", "Was it justice", None, LQ("FILE 23 — THE VERDICT OF HISTORY", "D. CLAYTON JAMES, MACARTHUR'S BIOGRAPHER", "a miscarriage of justice", "D. Clayton James", "Via Connor, HistoryNet (2022)")),
     ("The survivors had", "BAL", 260.0), ("Robert Pelz", "D4B", 35.0)],
    # 82 command responsibility
    [("What lasted was", "NWS", 30.0)],
    # 83 Hisako's memorial
    [("In", "LST", 395.0), ("#", "she told him", None, QC("stills/homma_execution_site.jpg", [("Never forget there were", "never forget there were"), ("the honorable gentlemen,", "the honorable gentlemen"), ("the lawyers who fought for me", "the lawyers who fought"),
        ("at the Manila trial.", "at the Manila trial")], "Homma's last letter to his daughter, as she wrote in 1973 (via Cook, 1996)", "at the Manila trial"))],
    # 84 comments
    [("If your father", "YOK", 200.0), ("@", "If your father", YOK_TAG), ("#", "If your father", None, HL("YOUR FAMILY", "Was he on Bataan or Corregidor?", "Tell us his name", "tell us his name", "WWII Frontlines", after=" in the comments."))],
    # 85 the march today
    [("Every spring", "YOK", 272.6), ("@", "Every spring", STAND + YOK_TAG), ("New Mexico remembers", "REL", 186.0), ("@", "New Mexico remembers", STAND + REL_TAG)],
    # 86 the end
    [("The trial record survives", "LST", 476.0), ("@", "The trial record survives", LST_TAG), ("As Major", "BAL", 106.0)],
]

PHOTOS = [
    (6, "was not the kind", None, "homma_portrait.jpg", "06", "Masaharu Homma", "Commander, Japanese 14th Army, 1941-42", f"Public domain · {WC}", {"focus": [0.5, 0.3]}),
    (6, "He wrote poetry", None, "homma_poet_general.jpg", "06", "", "", f"Public domain · {WC}", {"style": "print", "label": "Homma on an inspection tour of the Philippines, 1942"}),
    (11, "Near the village", None, "king_nakayama_1942.jpg", "11", "", "", f"Public domain · {WC} (Morton, p. 465)", {"style": "print", "label": "King (center) questioned by Col. Nakayama, 9 April 1942"}),
    (13, "King and his staff", None, "generals_captivity_1942.jpg", "13", "", "", f"Public domain · {WC}", {"style": "print", "label": "Captured U.S. generals, King and Wainwright among them, July 1942"}),
    (17, "He marched bareheaded", None, "death_march_tied.jpg", "17", "", "", f"Captured Japanese photo · USMC 127-N-114541 · public domain · {WC}", {"style": "print", "label": "American prisoners on the march, hands tied, April 1942"}),
    (19, "Technical Sergeant Horace", None, "odonnell_litters.jpg", "19", "", "", f"Captured Japanese photo · NARA 535564 · public domain · {WC}", {"style": "print", "label": "Prisoners carry comrades on improvised litters, May 1942"}),
    (29, "Five generals were appointed", None, "homma_commission_standing.jpg", "29", "The Military Commission", "Donovan, Valdes, Gard, Trudeau, McNaught · Manila, 9 Feb 1946", "Signal Corps, album 111-SCA-2919 · public domain", {"focus": [0.5, 0.35]}),
    (34, "Its first witness", None, "homma_trial_opening_1946.jpg", "34", "", "", "NARA 292610 · public domain", {"style": "print", "label": "Opening day, 3 January 1946: defense counsel George Furness objects"}),
    (40, "was shown a captured", None, "surrender_negotiation_1942.jpg", "40", "", "", f"Captured Japanese photo · public domain · {WC}", {"style": "print", "label": "Wainwright (left) faces Homma across the table, 6 May 1942"}),
    (43, "He told the court he", None, "homma_stand_a.jpg", "43", "Homma on the stand", "Testifying in his own defense, Manila, 6 Feb 1946", "Signal Corps, album 111-SCA-2919 · public domain", {"focus": [0.5, 0.35]}),
    (57, "The record shows", None, "homma_sentence_1946.jpg", "57", "", "", "Signal Corps, album 111-SCA-2919 · public domain", {"style": "print", "label": "Homma (center) hears his sentence, 11 February 1946"}),
    (58, "The record notes", None, "homma_bows_mp_1946.jpg", "58", "", "", "Signal Corps, album 111-SCA-2919 · public domain", {"style": "print", "label": "Homma bows to his MP escort after the sentence, 11 Feb 1946"}),
    (64, "In his judgment", None, "rutledge.jpg", "64", "Wiley Rutledge", "Associate Justice, U.S. Supreme Court", f"Public domain · {WC}", {"focus": [0.5, 0.35]}),
    (65, "now ruling occupied Japan", None, "macarthur_1945.jpg", "65", "Douglas MacArthur", "Supreme Commander for the Allied Powers, Tokyo", f"U.S. Army · public domain · {WC}", {"focus": [0.5, 0.35]}),
    (79, "The Associated Press wrote", None, "homma_execution_site.jpg", "79", "", "", f"Bootkinero · CC BY-SA 4.0 · {WC}", {"style": "print", "label": "The execution site at Los Baños today"}),
    (85, "In March", None, "bmdm_2016_survivor.jpg", "85", "", "", f"U.S. Army photo · public domain · {WC}", {"style": "print", "label": "A Bataan survivor greets a marcher, White Sands, 2016"}),
    (85, "The Army says", None, "bmdm_2012_finish.jpg", "85", "", "", f"U.S. Army photo · public domain · {WC}", {"style": "print", "label": "Guardsmen shake hands with Bataan survivors at the finish, 2012"}),
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
