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
    "RES": ("finback_rescue_1944", 1), "SJ": ("san_jacinto_1944", 0.78), "SJA": ("san_jacinto_attack_1945", 1),
    "IND": ("independence_tbf_1943", 1), "INO": ("independence_ops_1944", 1), "TANG": ("tang_lifeguard_1944", 1),
    "AVR": ("aviator_rescue_1945", 1), "TIG": ("tigrone_guam_1945", 1), "SUA": ("chichi_surrender_a", 1),
    "SUB": ("chichi_surrender_b", 1), "SUC": ("chichi_surrender_c", 1), "B24A": ("chichi_b24_1944", 1),
    "B24B": ("chichi_b24_1945", 1), "CJB": ("chichi_bombing_1944", 1), "FLA": ("fighting_lady_out_a", 0.86),
    "FLB": ("fighting_lady_out_b", 0.86), "KWA": ("kwajalein_strike_1944", 0.78), "WOL": ("wolverine_training_1943", 0.7),
    "K8": ("bush_kilo8_1991", 1), "PH91": ("bush_pearl_1991", 1), "ST": ("bush_stinnett_1992", 1), "PM": ("bush_powmia_1992", 1),
    "IV86": ("bush_interview_1986", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
NARA = "National Archives"
AAR = "VT-51 Aircraft Action Report No. 6, 2 Sept 1944 (NARA 139753048)"
FINR = "USS Finback, Report of Tenth War Patrol (NARA 139746844)"
LOG = "Lt.(jg) G.H.W. Bush, Aviator's Flight Log Book (George Bush Library, NARA 631635432)"
TRIAL = "U.S. v. Yoshio Tachibana et al., Navy war crimes commission, Guam (NARA 6997357)"
IWG = "NARA IWG, Researching Japanese War Crimes Records (2006)"
DFC = "DFC citation, Commander 2d Carrier Task Force Pacific (Dec 1944), via NHHC"

# Evidence labels on every tag (Restricted Files method, inside our ContextTag): FILE / AS HE TOLD IT / STAND-IN
FILE = "FROM THE FILE · "
TOLD = "AS HE TOLD IT · "
STAND = "Stand-in · "
RES_TAG = "The real rescue: Lt.(jg) George Bush pulled aboard USS Finback, 2 Sept 1944 · 8 mm film from Finback · George Bush Library"
SJ_TAG = "USS San Jacinto (CVL-30), Bush's carrier, February 1944 · U.S. Navy film (NARA NPC-1521)"
SJA_TAG = "USS San Jacinto under air attack, 1945 · U.S. Navy film (NARA 428-NPC-7784)"
IND_TAG = "TBF Avengers on USS Independence, San Jacinto's sister ship, 1943 · U.S. Navy film (NARA NPC-800)"
INO_TAG = "Flight operations on USS Independence, a light carrier like San Jacinto, Oct 1944 · U.S. Navy film (NARA NPC-6523)"
TANG_TAG = "Submarine lifeguard rescue of downed airmen by USS Tang, Truk, May 1944 · U.S. Navy film (NARA 428-NPC-4369)"
AVR_TAG = "A downed aviator rescued at sea, Feb 1945 · U.S. Navy film (NARA NPC-8646)"
TIG_TAG = "Rescued airmen arrive on a lifeguard submarine, Guam, July 1945 · U.S. Navy film (NARA 428-NPC-14153)"
SU_TAG = "Surrender of Chichi Jima aboard USS Dunlap, 3 Sept 1945 · U.S. Navy film (NARA 428-NPC-17059/60/62)"
B24_TAG = "Army Air Forces B-24s over Chichi Jima and the Bonins, 1944-45 · AAF combat film (CS-2599, CS-3618)"
CJB_TAG = "Bombing of Chichi Jima, Sept 1944 · Signal Corps film (111-ADC-1817)"
FL_TAG = "Navy torpedo bombers in the 1944 island strikes · U.S. Navy film (NARA NPC-2658/2661)"
KWA_TAG = "Carrier strike on a Japanese-held island, Jan 1944 · U.S. Navy film (NARA NPC-1469)"
WOL_TAG = "Carrier training on Lake Michigan, 1943 · U.S. Navy film (NARA NPC-5074)"
ST_TAG = TOLD + "President George H.W. Bush, White House interview, 2 June 1992 · White House Television (George Bush Library)"
PM_TAG = TOLD + "President Bush to POW/MIA families, 24 July 1992 · White House Television (George Bush Library)"
IV_TAG = TOLD + "Vice President Bush on his naval service, 19 June 1986 · White House Television (Reagan Library, NARA)"
K8_TAG = TOLD + "George H.W. Bush, Kilo 8 Pier, Pearl Harbor, 7 Dec 1991 · White House recording (George Bush Library)"
PH_TAG = TOLD + "George H.W. Bush, National Memorial Cemetery of the Pacific, 7 Dec 1991 · White House recording (George Bush Library)"

# lon/lat
CHI = [142.19, 27.08]; IWO = [141.32, 24.78]; HAHA = [142.16, 26.66]; TOK = [139.69, 35.69]; MAJ = [171.38, 7.09]
MID = [182.63, 28.21]; PEARL = [202.05, 21.35]; WAKE = [166.64, 19.28]; SAI = [145.75, 15.18]; GUAM = [144.79, 13.44]
PALAU = [134.5, 7.5]; ULI = [139.7, 10.0]; KWAJ = [167.73, 8.72]; JOHN = [190.48, 16.73]; MNL = [120.98, 14.6]

WAR44 = {"type": "GlobeMap", "theme": "history",
         "cam": [{"t": 0, "center": [175, 20], "scale": 2.2}, {"t": "Bush's logbook marks", "center": [160, 18], "scale": 3.2}],
         "pins": [{"ll": PEARL, "label": "Pearl Harbor", "at": 0.3}, {"ll": WAKE, "label": "Wake Island", "at": "strike, Wake Island", "color": "amber"},
                  {"ll": SAI, "label": "Saipan", "at": 0.8}, {"ll": GUAM, "label": "Guam", "at": 0.8}],
         "arcs": [{"from": PEARL, "to": WAKE, "at": "strike, Wake Island", "style": "dashed", "color": "amber", "loft": 0.05, "draw": 40},
                  {"from": WAKE, "to": SAI, "at": 0.85, "style": "dashed", "color": "amber", "loft": 0.04, "draw": 40}],
         "cards": [{"at": "strike, Wake Island", "kicker": "23 May 1944", "body": "First combat for Bush: strike on Wake Island", "accent": "amber"}],
         "footer": "Route generalised · Bush's logbook", "year": {"at": 0.1, "year": "1944", "sub": "USS San Jacinto"}}

BONINS = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [150, 22], "scale": 3.0}, {"t": "The largest was", "center": [141.6, 28.5], "scale": 14}],
          "pins": [{"ll": TOK, "label": "Tokyo", "at": 0.4}, {"ll": CHI, "label": "Chichi Jima", "at": "The largest was", "color": "red"},
                   {"ll": HAHA, "label": "Haha Jima", "at": "to their garrison"}, {"ll": IWO, "label": "Iwo Jima", "at": "to their garrison", "color": "amber"}],
          "arcs": [{"from": CHI, "to": IWO, "at": "to their garrison", "style": "dashed", "color": "amber", "loft": 0.0, "draw": 30}],
          "cards": [{"at": "The largest was", "kicker": "The Bonin Islands", "body": "About 600 miles south of Tokyo", "accent": "red"}],
          "footer": "Positions approximate", "year": {"at": 0.1, "year": "1944", "sub": "Bonin Islands"}}

FINBACK = {"type": "GlobeMap", "theme": "history",
           "cam": [{"t": 0, "center": [160, 15], "scale": 3.0}, {"t": "with orders", "center": [155, 18], "scale": 3.3}],
           "pins": [{"ll": MAJ, "label": "Majuro", "at": 0.3}, {"ll": CHI, "label": "Bonin Islands", "at": "with orders", "color": "red"}],
           "arcs": [{"from": MAJ, "to": CHI, "at": "with orders", "style": "dashed", "color": "amber", "loft": 0.05, "draw": 50}],
           "cards": [{"at": "with orders", "kicker": "16 August 1944", "body": "USS Finback leaves Majuro for lifeguard duty off the Bonins", "accent": "amber"}],
           "footer": f"Route generalised · {FINR}", "year": {"at": 0.1, "year": "1944", "sub": "USS Finback"}}

HOMEBACK = {"type": "GlobeMap", "theme": "history",
            "cam": [{"t": 0, "center": [165, 22], "scale": 2.2}, {"t": "He hitched rides", "center": [165, 14], "scale": 2.2}],
            "pins": [{"ll": MID, "label": "Midway", "at": 0.2}, {"ll": PEARL, "label": "Pearl Harbor", "at": 0.5},
                     {"ll": JOHN, "label": "Johnston", "at": "Johnston Island"}, {"ll": KWAJ, "label": "Kwajalein", "at": "by johnston island"},
                     {"ll": GUAM, "label": "Guam", "at": "and rejoined torpedo"}, {"ll": ULI, "label": "Ulithi", "at": "and rejoined torpedo", "color": "amber"}],
            "arcs": [{"from": MID, "to": PEARL, "at": 0.3, "style": "solid", "color": "amber", "loft": 0.04, "draw": 30},
                     {"from": PEARL, "to": JOHN, "at": "Johnston Island", "style": "dashed", "color": "amber", "loft": 0.03, "draw": 25},
                     {"from": JOHN, "to": KWAJ, "at": "by johnston island", "style": "dashed", "color": "amber", "loft": 0.03, "draw": 25},
                     {"from": KWAJ, "to": GUAM, "at": "and rejoined torpedo", "style": "dashed", "color": "amber", "loft": 0.03, "draw": 25},
                     {"from": GUAM, "to": ULI, "at": "rejoined Torpedo Squadron", "style": "dashed", "color": "amber", "loft": 0.02, "draw": 20}],
            "footer": f"Route from {LOG}", "year": {"at": 0.1, "year": "1944", "sub": "Back to the squadron"}}

GUAMTRIAL = {"type": "GlobeMap", "theme": "history",
             "cam": [{"t": 0, "center": [142.5, 22], "scale": 5}, {"t": 2.5, "center": [144.0, 18], "scale": 5.5}],
             "pins": [{"ll": CHI, "label": "Chichi Jima", "at": 0.2, "color": "red"}, {"ll": GUAM, "label": "Guam · Navy war crimes trials", "at": 1.0, "color": "amber"}],
             "arcs": [{"from": CHI, "to": GUAM, "at": 1.0, "style": "dashed", "color": "amber", "loft": 0.03, "draw": 30}],
             "footer": IWG, "year": {"at": 0.1, "year": "1946", "sub": "Guam"}}

# ── Reconstruction chart: Strike Baker and the rescue (screen px from the 2014 aerial photo's island outline) ──
import json as _json
_co = _json.load(open(ROOT / "build/coast.json"))
_S = 0.13
def _m(x, y):
    return [round(960 + _S * (x - 960), 1), round(540 + _S * (y - 2035), 1)]
_isl = [[_m(x, y) for x, y in poly] for poly in _co["polys"][:2]]
MINAMI = (140, 2200)
BAIL = (MINAMI[0] + 3790, MINAMI[1] - 3790)  # 9 statute miles bearing 045 from Minami Jima (~370 photo px per km)
STRIKE = {"type": "Chart", "head": "Strike Baker · 2 September 1944", "date": "Reconstruction · schematic, after the VT-51 action report and Finback's patrol report",
          "clock": {"t0": 1.0, "t1": 24.0, "from": "09:25", "to": "11:56"},
          "islands": [{"pts": _isl[0], "label": "Chichi Jima", "lx": _m(1300, 300)[0] + 60, "ly": _m(1300, 300)[1]},
                      {"pts": _isl[1], "label": "Minami Jima", "lx": _m(140, 2200)[0] - 230, "ly": _m(140, 2200)[1] + 60}],
          "tracks": [
              {"kind": "plane", "label": "Melvin", "pts": [_m(900, 4300), _m(900, 900), _m(700, -300)], "t0": 0.5, "t1": 5.0},
              {"kind": "plane", "label": "West", "pts": [_m(1000, 4500), _m(1000, 1000), _m(800, -200)], "t0": 0.8, "t1": 5.3},
              {"kind": "plane", "label": "Bush", "labelAt": 1.2, "pts": [_m(1100, 4700), _m(1100, 1100), _m(1800, 400), _m(*BAIL)], "t0": 1.1, "t1": 8.0},
              {"kind": "plane", "label": "Moore", "pts": [_m(1200, 4900), _m(1200, 1200), _m(1300, -100)], "t0": 1.4, "t1": 6.2},
              {"kind": "sub", "label": "Finback", "labelAt": 10.0, "pts": [_m(-3700, 1600), _m(-2700, 4500), _m(960, 5700), _m(4300, 4300), _m(5200, 1300), _m(4500, -900), _m(*BAIL)], "t0": 9.6, "t1": 23.5}],
          "contacts": [{"t": 2.6, "x": _m(1100, 1100)[0], "y": _m(1100, 1100)[1], "label": "Radio station · hit at 8,000 ft"},
                       {"t": 8.2, "x": _m(*BAIL)[0], "y": _m(*BAIL)[1], "label": "Bail-out · about 3,000 ft"}],
          "stamps": [{"t": 1.0, "x": _m(1100, 4700)[0] + 40, "y": _m(1100, 4700)[1], "text": "09:25"},
                     {"t": 9.8, "x": _m(-3700, 1600)[0] - 40, "y": _m(-3700, 1600)[1] + 50, "text": "09:33"},
                     {"t": 23.6, "x": _m(*BAIL)[0] - 160, "y": _m(*BAIL)[1] + 60, "text": "11:56"}],
          "zoom": [1.0, 1.06],
          "source": "Times in Finback's zone (VT-51's clock + 1 h) · " + AAR + " · " + FINR}

LETTER = QC("stills/bush_flight_gear.jpg", [("There was no sign of Del or Ted anywhere around.", "no sign of Del"), ("I sat in my raft and sobbed for a while.", "sobbed"),
            ("I feel so terribly responsible for their fate.", "terribly responsible")],
            "Lt.(jg) George Bush, letter to his parents from USS Finback, September 1944", "terribly responsible")
WATCH = QC("stills/finback_launch.jpg", [("And I would think about friends I lost,", "friends he had lost"), ("a country I loved,", "friends he had lost"),
            ("and about a girl named Barbara.", "friends he had lost")],
           "George H.W. Bush, acceptance speech, Houston, 20 August 1992 (Public Papers)", "friends he had lost")
FLYNN = QC("stills/guam_trial_building.jpg", [("It is our hope that never again", "It is our hope"), ("will the like of these cases", "will the like"), ("have to be presented.", "have to be presented")],
           "Lt. Daniel Flynn, USNR, opening argument for the prosecution, Guam, 1946 · " + TRIAL, "have to be presented")
MATOBA = QC("stills/marines_search_1946.jpg", [("Yes, I was a madman due to the war", "madman")], "Maj. Sueo Matoba, testimony to the Chichi Jima board of investigation, 1946 (per NARA IWG, 2006)", "madman")
GUNNER = QC("stills/tbm_flak_damage.jpg", [("The plane was never on fire.", "had not been on fire")], "Chester Mierzejewski, former VT-51 gunner, to the New York Post, August 1988", "save his crew")
BURNING = QC("stills/bush_1994_tbm.jpg", [("The plane was burning.", "the plane was burning"), ("I know I did the right thing.", "the right thing")], "George H.W. Bush, CNN interview, 2003", "the right thing")
BOYS = QC("stills/futami_pano.jpg", [("God bless those boys.", "dropped wreaths")], "George H.W. Bush, laying wreaths at sea off Chichi Jima, June 2002 (CNN)", "and he met")
IWATAKE = QC("stills/chichi_fortress_hq.jpg", [("I can never forget this place.", "Warren Iwatake")], "Nobuaki 'Warren' Iwatake, Chichi Jima, 2002", "Warren Iwatake")

VERDICT = {"type": "Verdict", "file": "FROM THE FILE · 2 SEPTEMBER 1944", "head": "Three claims, three verdicts",
           "rows": [{"claim": "His plane was on fire", "stamp": "Confirmed", "note": "Action report, Sept 1944 · DFC citation, Dec 1944", "at": "The fire"},
                    {"claim": "Four hours in the raft", "stamp": "Shortened", "note": "Finback's clock: about two and a half", "at": "shortened"},
                    {"claim": "His crew bailed out with him", "stamp": "Records differ", "note": "One other chute · no chutes seen · only one man", "at": "the papers disagree"}],
           "source": AAR + " · " + FINR + " · " + DFC}

EIGHT = TL("FILE 07 — THE EIGHT", "Airmen killed on Chichi Jima", [
    ("Aug 1944", "ARM2c Lloyd R. Woellhof, VB-1, USS Yorktown · and an unnamed American"),
    ("Feb 1945", "Ens. Floyd E. Hall and ARM3c Marve W. Mershon, VT-12, USS Randolph"),
    ("Feb 1945", "AOM2c Glenn J. Frazier, VT-12, USS Randolph"),
    ("Feb 1945", "AOM3c Grady A. York and ARM3c James W. Dye, VT-82, USS Bennington"),
    ("Mar 1945", "2nd Lt. Warren E. Vaughn, USMCR, VMF-123, USS Bennington")], TRIAL + " · Pacific Wrecks")
HOURS = {"type": "BigNumber", "value": 1228, "label": "Hours in the air · 126 carrier landings", "source": LOG}
MISSIONS = {"type": "BigNumber", "value": 58, "label": "Combat missions", "source": "NHHC · George Bush Library"}


def _scale_times(o, k):
    if isinstance(o, dict):
        return {a: (round(b * k, 2) if a in ("t", "t0", "t1", "labelAt") and isinstance(b, (int, float)) else _scale_times(b, k)) for a, b in o.items()}
    if isinstance(o, list):
        return [_scale_times(v, k) for v in o]
    return o
STRIKE = {**_scale_times({x: STRIKE[x] for x in ("tracks", "contacts", "stamps", "clock")}, 0.74), **{x: STRIKE[x] for x in STRIKE if x not in ("tracks", "contacts", "stamps", "clock")}}

# ── shots: sh() adds the film's source tag when the film changes; tag=False for a repeat, or a custom tag ──
TAG = {"RES": RES_TAG, "SJ": SJ_TAG, "SJA": SJA_TAG, "IND": IND_TAG, "INO": INO_TAG, "AVR": AVR_TAG, "TIG": TIG_TAG,
       "SUA": SU_TAG, "SUB": SU_TAG, "SUC": "Japanese envoys aboard USS Dunlap off Chichi Jima, 31 Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)",
       "B24A": B24_TAG, "B24B": "Chichi Jima from an AAF B-24, 22 March 1945 · AAF combat film (CS-3618)", "CJB": CJB_TAG,
       "FLA": FL_TAG, "FLB": FL_TAG, "KWA": KWA_TAG, "WOL": WOL_TAG, "K8": K8_TAG, "PH91": PH_TAG, "ST": ST_TAG, "PM": PM_TAG,
       "IV86": "Vice President George H.W. Bush, interview on his naval service, 19 June 1986 · White House Television (Reagan Library, NARA)",
       "STF": "President George H.W. Bush, White House interview on his war service, 2 June 1992 · White House Television (George Bush Library)"}
GENERIC = {"SJA", "IND", "INO", "AVR", "TIG", "FLA", "FLB", "KWA", "WOL", "B24A", "SUC"}  # not the event itself: marked as stand-ins


def sh(anchor, key, t, tag=True):
    film = "ST" if key == "STF" else key
    out = [(anchor, film, t)]
    if tag:
        txt = tag if isinstance(tag, str) else ((STAND if key in GENERIC else "") + TAG[key])
        out.append(("@", anchor, txt))
    return out


def card(anchor, c, until=None):
    return [("#", anchor, until, c)]


def LDOC(file, head, spans, source):
    return {"type": "LedgerDocument", "file": file, "head": head, "source": source, "spans": [{"doc": d, "say": s} for d, s in spans]}


P = [
    # 0 the raft
    sh("The Pacific Ocean", "RES", 44.8) + card("The Pacific Ocean", SLUG("2 September 1944 · late morning", "Off Chichi Jima, Bonin Islands")) +
    sh("A few miles off", "CJB", 43.5) + sh("Minutes earlier", "FLA", 113.5, STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("He paddles as hard", "AVR", 12.5),
    # 1 the periscope
    sh("Above him", "SUC", 79.3, STAND + "Hellcats low over the sea off Chichi Jima, Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)") + sh("Then, a little before noon", "RES", 16.8) +
    sh("First a periscope", "TIG", 113.5) + sh("Sailors run out", "RES", 17.6) + sh("and up on the conning", "RES", 42.6, False),
    # 2 the patrol report (LedgerDocument)
    sh("The submarine's captain", "RES", 27.2) + sh("It gives the time", "AVR", T(1, 58.0)) + card("The submarine's captain", LDOC("FROM THE FILE · USS FINBACK", "Patrol report, 2 Sept 1944, 1156",
        [("fin_rescue", "he failed to see his crew's parachutes and believed they had jumped when plane was still over")], FINR)),
    # 3 two young men
    sh("Two young men", "IND", 12.5) + sh("And on the island", "CJB", 19.5) + sh("What happened to those", "B24B", T(2, 51.0)),
    # 4 documented story
    sh("This is the documented", "RES", 38.0) + sh("the squadron's secret", "SJ", T(1, 22.0)) + sh("Where the papers agree", "IV86", T(6, 0.0)),
    # 5 three claims
    sh("You will often read", "FLA", 114.0, STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("that he sat in the raft", "RES", 23.2) +
    sh("and that his crew", "IND", 13.5) + sh("The file backs one", "IV86", T(6, 20.0)),
    # 6 the file
    sh("A man who later became", "IV86", T(7, 0.0)) + sh("To them he was one pilot", "SJ", T(1, 36.0)),
    # 7 the documents
    sh("The first is Form", "IND", T(2, 38.0)) + card("The first is Form", DESK("stills/doc_aar_s1_paper.png", 1.3306, [(0, "wide", [0.5, 0.3]), ("stamped secret", "heading", [0.78, 0.04]),
        ("five sheets", "glide", [0.12, 0.2, 0.7])], AAR)) + sh("The second is the war patrol", "TIG", 63.5) + sh("The third is a small", "IND", T(2, 47.5)),
    # 8 the fourth file
    sh("The fourth file", "SUA", T(1, 13.5)) + sh("Bush never appears", "CJB", 31.5) + sh("But it describes", "CJB", 43.8, False),
    # 9 7 Dec 1941
    sh("The story starts", "IV86", T(1, 30.0)) + card("The story starts", SLUG("7 December 1941", "Phillips Academy, Andover, Massachusetts")) + sh("He heard the news", "IV86", T(2, 10.0), False),
    # 10 CLIP Kilo 8
    sh("Like all American", "K8", 8.5),
    # 11 seaman second class
    sh("Seaman second class", "WOL", 6.5) + sh("He had signed up", "WOL", 74.5, False),
    # 12 preflight
    sh("The Navy turned schoolboys", "WOL", 14.5) + sh("Bush started at", "WOL", 54.5, False) + sh("Then came primary", "WOL", T(2, 35.0), False) + sh("His logbook shows", "WOL", T(2, 47.0), False),
    # 13 commissioned
    sh("From there he went", "WOL", T(3, 30.0)) + sh("He was one of the youngest", "IND", 66.5),
    # 14 Avenger, Sable
    sh("He was sent to fly", "IND", 0.5) + sh("He learned it", "IND", 99.5, False) + sh("In August", "WOL", T(3, 0.5), STAND + "USS Wolverine, a Lake Michigan training carrier like Sable, 1943 · U.S. Navy film (NARA NPC-5074)") +
    sh("A stamp in his logbook", "WOL", T(3, 20.5), False),
    # 15 VT-51
    sh("That September", "IND", T(2, 17.5)) + sh("Ensign Bush became", "IND", 12.5, False),
    # 16 San Jacinto
    sh("The squadron's ship", "SJ", T(0, 55.5)) + sh("She was a light carrier", "SJ", T(1, 7.5), False) + sh("fast, narrow", "SJ", T(1, 47.5), False),
    # 17 three men
    sh("The Avenger carried", "IND", 13.0) + sh("Behind him", "FLB", 80.5) + sh("Down in the belly", "IND", T(2, 18.0)) + sh("He talked to them", "FLB", 87.5),
    # 18 crew
    sh("Bush's regular crew", "FLB", 60.0) + sh("The three of them", "FLB", 66.0, False),
    # 19 Barbara
    sh("In December", "IND", T(2, 38.5)) + sh("He named his planes", "FLA", T(2, 22.0)),
    # 20 Wake
    sh("reached the war", "INO", T(5, 38.5)) + card("reached the war", WAR44) + sh("Bush's logbook marks", "INO", T(5, 2.0), False),
    # 21 roommate
    sh("The same operation", "SJ", 3.0, "Burial at sea aboard USS San Jacinto, Feb 1944 (not Wykes) · U.S. Navy film (NARA NPC-1521)") + sh("Forty-seven years later", "SJ", 20.0, False),
    # 22 CLIP Pearl 1991
    sh("My roommate", "PH91", 10.1),
    # 23 Marianas
    sh("In June the carriers", "SJA", 13.5) + sh("On the fifteenth of June", "FLB", T(2, 30.5)),
    # 24 Philippine Sea
    sh("Four days later", "SJA", 21.5) + sh("American fighter pilots", "SJA", T(2, 58.2), False) + sh("For Bush it was", "IND", 56.3),
    # 25 red ink
    sh("His logbook entry", "IND", 51.0) + sh("Emergency crash landing", "AVR", 62.5),
    # 26 Bronson
    sh("He set the crippled", "AVR", 66.0) + sh("For the next four days", "SJ", T(3, 2.0)),
    # 27 back to work
    sh("Then it was back", "KWA", 20.5) + sh("On the twenty-fifth", "FLB", 36.5) + sh("On the first of August", "KWA", 6.5) + sh("He had already been lucky", "KWA", 16.0, False),
    # 28 the Bonins
    sh("At the end of August", "CJB", T(1, 49.5)) + card("At the end of August", BONINS) + sh("The Japanese called", "SUA", T(1, 1.5)) + sh("and it mattered", "CJB", 44.0, False),
    # 29 fortress
    sh("The island was a fortress", "SUA", T(1, 13.5)) + sh("The Navy had a base", "SUA", T(1, 2.0), False) + sh("The prosecutor's opening", "CJB", 31.5),
    # 30 Woellhof (DocDesk on the trial page)
    sh("The same record shows", "CJB", 19.6) + card("On or about the fourth", DESK("stills/doc_trial_p2_paper.png", 1.7076, [(0, "wide", [0.5, 0.6]),
        ("He was Lloyd", "glide", [0.6, 0.15, 0.75])], TRIAL + ", prosecution opening, p. F-2")),
    # 31 garage, Aug 1944
    sh("The record says", "SUB", T(3, 28.0)) + sh("Then, on or about", "CJB", T(1, 32.0)) + sh("Nobody in Bush's squadron", "SJA", T(1, 5.5)) + sh("To the pilots", "SJA", T(1, 9.5), False),
    # 32 lifeguard idea
    sh("The Navy did know", "AVR", 3.5) + sh("So when the carriers struck", "TIG", 114.0),
    # 33 Finback sails
    sh("On the sixteenth of August", "TIG", 47.5) + card("On the sixteenth of August", FINBACK),
    # 34 1 Sept
    sh("On the first of September", "TIG", 103.0) + sh("The same day", "IND", 67.0) + sh("His logbook says", "KWA", 16.3),
    # 35 Strike Baker
    sh("On the morning", "INO", T(5, 39.0)) + card("On the morning", SLUG("2 September 1944 · Strike Baker", "VT-51, USS San Jacinto · target: radio station, Chichi Jima")) +
    sh("The target was", "CJB", 31.8) + sh("Four Avengers would", "FLB", T(2, 58.5)) + sh("escorted by twelve", "INO", 21.5),
    # 36 Ted White
    sh("That morning Bush's crew", "FLB", 81.0) + sh("In his place", "IND", 14.0) + sh("He was twenty-six", "IND", T(2, 19.0), False) + sh("took his usual seat", "FLB", 90.0),
    # 37 take-off
    sh("According to the action report", "IND", 1.0) + sh("In the lead", "IND", 99.5, False) + sh("The weather was good", "FLA", 1.0),
    # 38 push-over
    sh("At about twenty-five", "KWA", 21.0) + sh("and pushed over", "FLA", 20.0) + sh("The report describes", "SJA", T(1, 5.5)),
    # 39 the line (LedgerDocument)
    sh("and the second pilot", "CJB", T(1, 13.5), "Bombs on Chichi Jima, 27 Sept 1944, three weeks after Bush's strike · Signal Corps film (111-ADC-1817)") +
    card("Then the report turns", LDOC("FROM THE FILE · VT-51 ACTION REPORT", "Sheet 4: the dive",
        [("aar_fire", "In spite of this hit which caused his engine to smoke and catch on fire Lieutenant junior grade Bush continued in his dive releasing his bombs on the radio station")], AAR)),
    # 40 1992 intro
    sh("Forty-eight years later", "STF", 540.5),
    # 41 CLIP dive
    sh("About halfway", "ST", 553.7),
    # 42 the DFC
    sh("In other words", "FLA", T(2, 45.0)) + sh("He held a diving plane", "FLA", T(3, 4.0), False) +
    card("That is what his", LQ("FILE 03 — THE CITATION", "DISTINGUISHED FLYING CROSS · LT.(JG) G.H.W. BUSH", "in spite of smoke and flames from the fire in his plane, he continued in his dive",
        "Commander, Second Carrier Task Force, Pacific, December 1944", DFC, after=" …")),
    # 43 turn east
    sh("After the bombs fell", "FLA", T(1, 54.0), STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("He told his skipper", "KWA", T(1, 40.5), False) + sh("He also ordered", "KWA", T(1, 44.5)),
    # 44 the bail-out (LedgerDocument, two spans)
    sh("Then the report says", "AVR", T(1, 58.0)) + card("Then the report says", LDOC("FROM THE FILE · VT-51 ACTION REPORT", "Sheet 4: the bail-out",
        [("aar_bail", "Bush and one other person were seen to bail out"), ("aar_chute", "The chute of the other person either Lieutenant junior grade White or J L")], AAR)),
    # 45 incomplete
    sh("The report adds", "AVR", T(2, 3.0)) + sh("And it closes", "AVR", T(2, 12.0), False),
    # 46 1992 intro 2
    sh("In the same", "STF", 598.0),
    # 47 CLIP bail
    sh("Told them to bail", "ST", 609.7),
    # 48 the tail
    sh("Bush himself had hit", "AVR", 12.8) + sh("He came down", "AVR", 35.0, False),
    # 49 fighters overhead
    sh("From the air", "SUC", 79.5, STAND + "Hellcats low over the sea off Chichi Jima, Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)") + sh("Somewhere off the island", "TIG", 115.0),
    # 50 reconstruction chart
    sh("Her patrol report", "TIG", 116.0, False) + card("Her patrol report", STRIKE),
    # 51 the film
    sh("At four minutes", "RES", 22.9) + sh("A sailor named", "RES", 27.1, False) + sh("This is that film", "RES", 31.3, False) + sh("It runs less", "RES", 37.8, False),
    # 52 how long
    sh("How long was Bush", "RES", 41.6) + sh("Popular accounts", "RES", 44.8, False) + sh("Either way", "AVR", T(1, 58.0)),
    # 53 CLIP raft
    sh("I remember being sick", "ST", 748.95),
    # 54 search
    sh("The submarine did not leave", "RES", 45.0) + sh("Her report says", "AVR", T(1, 36.0)) + sh("She found nothing", "AVR", T(2, 6.0)),
    # 55 what does the file say
    sh("So, what does the file", "IV86", T(13, 15.0)),
    # 56 two reports (desk)
    sh("The squadron report", "IND", 99.5) + card("The squadron report", DESK("stills/doc_aar_s4_paper.png", 1.3235, [(0, "wide", [0.5, 0.45]), ("says Bush and one", "glide", [0.5, 0.3, 0.8])], AAR)),
    # 57 Beckman (desk)
    sh("And there is a third", "AVR", 53.5) + card("Once aboard", DESK("stills/doc_finback_beckman_paper.png", 1.3594, [(0, "wide", [0.5, 0.15]), ("The report says it", "glide", [0.11, 0.3, 0.8])], FINR)),
    # 58 the logbook (desk)
    sh("Bush's own logbook", "INO", T(4, 16.5)) + card("On the line", DESK("stills/doc_logbook_paper.png", 0.7915, [(0, "wide", [0.5, 0.2]),
        ("the plane's number", "glide", [0.08, 0.1, 0.5]), ("and then", "heading", [0.78, 0.07])], LOG)),
    # 59 on patrol
    sh("Finback could not", "RES", 43.7) + sh("So for about a month", "TIG", T(2, 9.0)),
    # 60 watches
    sh("He stood watches", "TIG", 63.0) + sh("He was there when", "TIG", 103.5, False) + card("Forty-eight years later", WATCH),
    # 61 the letter
    sh("From the submarine", "RES", 45.5) + card("From the submarine", LETTER) + sh("He wrote that there", "TIG", 63.5),
    # 62 Midway
    sh("On the thirtieth", "TIG", 88.5, STAND + "A lifeguard submarine ties up with rescued airmen, Guam, July 1945 · U.S. Navy film (NARA 428-NPC-14153)") + sh("A Navy photographer", "TIG", T(2, 8.5), False),
    # 63 back
    sh("From Midway", "INO", T(5, 2.0)) + card("From Midway", HOMEBACK),
    # 64 eight more
    sh("He flew eight more", "FLB", 61.0) + sh("including strikes", "FLA", T(3, 32.0)) + sh("By the end of its tour", "FLB", T(1, 47.0)),
    # 65 decorations
    sh("In all, his file", "IND", 67.5) + card("In all, his file", MISSIONS, "He was awarded") + sh("He was awarded", "SJ", T(2, 16.0)) + sh("On the sixth of January", "IV86", T(0, 20.0)),
    # 66 VT-153, totals
    sh("He spent the rest", "IND", T(1, 57.0)) + sh("The last page", "IND", 67.0, False),
    # 67 subscribe
    sh("If you want more", "INO", T(5, 3.0)) + card("If you want more", {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented"}) +
    sh("And now, back", "SUA", T(1, 2.5)),
    # 68 Feb 1945
    sh("In February", "B24B", T(2, 41.8)) + sh("this time to cover", "B24B", T(2, 50.6), False) + sh("On the eighteenth", "B24B", T(2, 55.6), False),
    # 69 Randolph
    sh("An Avenger from the carrier", "FLB", T(4, 9.0)) + sh("Their gunner", "CJB", 31.5),
    # 70 Bennington
    sh("Another Avenger", "FLA", 2.0) + sh("Its pilot ditched", "AVR", 4.0) + sh("His two crewmen", "CJB", 20.5),
    # 71 Vaughn
    sh("Then, on the twenty-third", "B24A", 82.6) + sh("On the island he was", "B24B", T(2, 51.0)) + sh("The two became friends", "CJB", 44.5),
    # 72 the record
    sh("The trial record describes", "CJB", T(1, 32.0)) + sh("These are the facts", "CJB", T(1, 40.0), False),
    # 73 shelter (LedgerDocument)
    sh("were taken to General", "SUB", T(3, 28.0)) + card("were taken to General", LDOC("FROM THE FILE · THE TRIAL RECORD", "Prosecution opening, p. F-3",
        [("trial_shelter", "ordered not to give the prisoners shelter food nor water")], TRIAL)),
    # 74 executions
    sh("On or about the twenty-third", "SUA", T(1, 14.0)) + sh("York was put", "CJB", 21.5) + sh("Dye was kept alive", "CJB", 34.0, False) + sh("Hall was executed", "SUB", T(5, 20.0)),
    # 75 cannibalism
    sh("The trial record also", "SUB", T(5, 30.0)) + sh("The prosecution said", "CJB", T(1, 44.0)),
    # 76 the eight
    sh("In all, eight", "AVR", T(1, 57.0)) + card("In all, eight", EIGHT),
    # 77 cover story
    sh("When the war ended", "SUA", 42.0) + sh("American investigators", "SUC", T(4, 29.5)) + sh("or sent away", "SUC", T(5, 43.5), False),
    # 78 Savory, Rixey
    sh("The story did not hold", "SUB", T(3, 30.0)) + sh("On the twenty-first", "SUC", T(2, 29.5)),
    # 79 Matoba testifies
    sh("On the seventh of January", "SUA", T(4, 35.5)) + card("He admitted ordering", MATOBA),
    # 80 Guam
    sh("The cases were tried", "TIG", T(3, 35.5), STAND + "Guam, July 1945 · U.S. Navy film (NARA 428-NPC-14153)") + card("The cases were tried", GUAMTRIAL),
    # 81 the charges
    sh("The charges were murder", "TIG", T(3, 36.0)) + sh("One problem had", "SUA", T(4, 28.0), "Japanese officers aboard USS Dunlap, 3 Sept 1945 · U.S. Navy film (NARA 428-NPC-17059)"),
    # 82 Flynn (LedgerDocument)
    sh("The prosecutor", "SUA", T(4, 36.0), False) + card("The prosecutor", LDOC("FROM THE FILE · THE TRIAL RECORD", "Opening argument for the prosecution",
        [("trial_revolting", "so revolting to the human mind that man long ago decided it unnecessary to legislate directly against their commission")], TRIAL)),
    # 83 never again
    sh("He went on", "SUA", T(5, 44.0), False) + card("He went on", FLYNN),
    # 84 Time
    sh("It was not a secret", "TIG", T(3, 40.0)) + sh("But the Navy did not", "AVR", T(2, 0.0)),
    # 85 verdicts
    sh("Of the fourteen", "SUA", T(5, 46.0)) + sh("received a life sentence", "SUA", T(4, 40.0), False),
    # 86 hanged
    sh("On the twenty-fourth", "SUB", T(5, 18.0)) + sh("The Navy's own", "SUB", T(5, 33.0), False),
    # 87 surrender, 1945
    sh("Two years before", "SUA", T(1, 25.0)) + sh("A Navy cameraman", "SUA", T(2, 23.2), "Surrender of the Bonin Islands aboard USS Dunlap, 3 Sept 1945 · the senior officer is probably Lt. Gen. Tachibana · U.S. Navy film (NARA 428-NPC-17059)") +
    sh("and signing", "SUA", T(5, 59.5), False) + sh("It was one day after", "SUA", T(6, 12.0), False),
    # 88 the gunner
    sh("when Bush was running", "IV86", T(11, 35.0)) + sh("A former Torpedo", "FLB", 62.0) + card("He said the plane", GUNNER),
    # 89 absurd
    sh("Bush's campaign", "STF", 525.0) + card("In 2003", BURNING),
    # 90 what the file shows
    sh("So what does the file show", "IND", 100.0) + sh("comes from one man", "FLB", 64.0),
    # 91 parachutes
    sh("On the parachutes", "AVR", T(1, 35.5)) + sh("Whether Ted White", "AVR", T(2, 8.0)) + sh("That is the honest", "AVR", T(2, 16.0), False),
    # 92 verdict
    sh("So here are the three", "SJ", T(1, 7.5)) + sh("The four hours in", "SJ", T(3, 2.0), False) + card("So here are the three", VERDICT),
    # 93 declared dead
    sh("were officially declared", "AVR", T(1, 58.5)) + sh("the gunner who stayed", "IND", T(2, 48.0)),
    # 94 scrapped
    sh("Finback was decommissioned", "TIG", 64.0) + sh("was scrapped in", "SJ", T(2, 49.5)) + sh("guard and friend", "CJB", 45.5),
    # 95 1984
    sh("On the second of September", "IV86", T(3, 10.0)),
    # 96 2002
    sh("In June 2002", "SUB", T(3, 32.0)) + card("He dropped wreaths", BOYS),
    # 97 died
    sh("George Herbert Walker Bush died", "STF", 900.0),
    # 98 your family
    sh("Torpedo Squadron Fifty-One, the", "FLB", 66.5) + sh("If your father", "IND", 104.0),
    # 99 today
    sh("went back to Japan", "SUB", T(5, 17.5)) + sh("Boats come and go", "SUA", T(1, 2.0)) + sh("and in a bay", "AVR", T(1, 59.0)),
    # 100 the place
    sh("Somewhere off the north-east", "AVR", T(1, 57.5)) + sh("There is no marker", "AVR", T(1, 36.5), False) + card("There is only the line", DESK("stills/doc_logbook_paper.png", 0.7915, [(0, "heading", [0.75, 0.07]), ("crash landing", "glide", [0.07, 0.62, 0.95])], LOG)),
]

PC = f"U.S. Navy · public domain · {WC}"
BL = "George Bush Presidential Library and Museum · NARA · public domain"
PHOTOS = [
    (3, "Two young men", None, "bl_H080-01.jpg", "03", "", "", BL, {"style": "print", "label": "John Delaney, Leo Nadeau and George Bush"}),
    (4, "the pilot's own logbook", None, "doc_logbook_cover.png", "04", "", "", LOG, {"style": "print", "label": "Bush's Aviator's Flight Log Book"}),
    (4, "and the record of", None, "trial_folder_tab.jpg", "04", "", "", TRIAL, {"style": "print", "label": "U.S. v. Tachibana et al., case file"}),
    (6, "But the papers", None, "bush_flight_gear.jpg", "06", "", "", f"U.S. Navy · NARA 186380 · public domain · {WC}", {"style": "print", "label": "Lt.(jg) George H.W. Bush, Navy pilot, 1944"}),
    (7, "The third is a small", None, "doc_logbook_cover.png", "07", "", "", LOG, {"style": "print", "label": "Aviator's Flight Log Book, 'Bush G.H.W.'"}),
    (8, "a case called", None, "trial_folder_tab.jpg", "08", "", "", TRIAL, {"style": "print", "label": "'Tachibana, Yoshio et al.' · Navy JAG, Pacific war crimes trials"}),
    (11, "He had signed up", None, "bl_H077.jpg", "11", "", "", BL, {"style": "print", "label": "George Bush as a naval aviation cadet"}),
    (12, "Bush started at", None, "corpus_christi_cadets.jpg", "12", "", "", f"U.S. Navy · NARA 520975 · public domain · {WC}", {"style": "print", "label": "Aviation cadets check the flight boards, NATC Corpus Christi"}),
    (13, "On the ninth of June", None, "bush_flight_gear.jpg", "13", "", "", f"U.S. Navy · NARA 186380 · public domain · {WC}", {"style": "print", "label": "George Bush, naval aviator"}),
    (15, "That September", None, "bl_H048.jpg", "15", "", "", BL, {"style": "print", "label": "Torpedo Squadron 51 (VT-51)"}),
    (16, "commissioned at Philadelphia", None, "sanjac_philly.jpg", "16", "", "", f"U.S. Navy · NH 43506 · public domain · {WC}", {"style": "print", "label": "USS San Jacinto (CVL-30), Philadelphia, January 1944"}),
    (17, "The pilot sat up front", None, "bush_cockpit_wide.jpg", "17", "", "", f"U.S. Navy · NARA 186383 · public domain · {WC}", {"style": "print", "label": "Bush in the cockpit of his TBM Avenger"}),
    (18, "His radioman was", None, "bl_H080-01.jpg", "18", "", "", BL, {"style": "print", "label": "John 'Del' Delaney (left), Leo Nadeau and George Bush"}),
    (19, "He named his planes", None, "bush_cockpit_wide.jpg", "19", "", "", f"U.S. Navy · NARA 186383 · public domain · {WC}", {"style": "print", "label": "'Barbara' painted on the side of a Bush Avenger"}),
    (23, "Marines invaded", None, "doc_logbook_jun44.png", "23", "", "", LOG, {"style": "print", "label": "Logbook, June 1944: 'Marines invaded Saipan'"}),
    (25, "is written in red ink", None, "doc_logbook_jun44.png", "25", "", "", LOG, {"style": "print", "label": "Logbook, 19 June 1944, in red: 'Emergency crash landing in sea near Guam'"}),
    (27, "Bush and another pilot", None, "vt51_majuro.jpg", "27", "", "", PC, {"style": "print", "label": "A VT-51 Avenger over Majuro, May 1944"}),
    (29, "An Army brigade", None, "chichi_fortress_hq.jpg", "29", "", "", f"Public domain · {WC}", {"style": "print", "label": "Japanese brigade headquarters, Chichi Jima"}),
    (29, "The prosecutor's opening", None, "ams_chichi_map.jpg", "29", "", "", f"U.S. Army Map Service, 1943-44 · public domain · {WC}", {"style": "print", "label": "U.S. Army map of Chichi Jima"}),
    (32, "could be saved", None, "kingfisher_truk.jpg", "32", "", "", f"U.S. Navy · 80-G-227991 · public domain · {WC}", {"style": "print", "label": "Downed airmen await a lifeguard submarine, Truk, May 1944"}),
    (33, "She had a new captain", None, "bl_H062.jpg", "33", "", "", BL, {"style": "print", "label": "USS Finback (SS-230)"}),
    (34, "Finback picked up", None, "harder_rescue.jpg", "34", "", "", PC, {"style": "print", "label": "A submarine picks up a downed pilot (USS Harder, Woleai, 1944)"}),
    (35, "Four Avengers would", None, "vt51_takeoff_jun44.jpg", "35", "", "", f"U.S. Navy · 80-G-238783 · public domain · {WC}", {"style": "print", "label": "A VT-51 TBM-1C takes off from San Jacinto, June 1944"}),
    (36, "In his place", None, "vt51_launch_may44.jpg", "36", "", "", PC, {"style": "print", "label": "VT-51 Avenger launch, USS San Jacinto, May 1944"}),
    (37, "In the lead", None, "tbm_saipan.jpg", "37", "", "", f"U.S. Navy · 80-G-428459 · public domain · {WC}", {"style": "print", "label": "TBM-1C Avenger, the model Bush flew, June 1944"}),
    (43, "smoke and flames", None, "tbm_flak_damage.jpg", "43", "", "", f"U.S. Navy · NH 89380 · public domain · {WC}", {"style": "print", "label": "Stand-in · a flak-damaged Avenger, 1945 (not Bush's)"}),
    (45, "the words every family", None, "doc_casualty_list.jpg", "45", "", "", f"NARA 305178 · public domain · {WC}", {"style": "print", "label": "Casualty list by aircraft type, TBM-1C, 2 Sept 1944"}),
    (51, "This is that film", None, "bush_rescue_400dpi.jpg", "51", "", "", BL, {"style": "print", "label": "Frame from the rescue film: Bush pulled aboard Finback"}),
    (59, "with five rescued", None, "finback_officers_aviators.jpg", "59", "", "", BL, {"style": "print", "label": "The rescued airmen with Finback's officers"}),
    (62, "A Navy photographer", None, "finback_officers_aviators.jpg", "62", "", "", BL, {"style": "print", "label": "Midway, 30 Sept 1944: Bush kneels second from left"}),
    (65, "received the Presidential", None, "bl_H079-02.jpg", "65", "", "", BL, {"style": "print", "label": "USS San Jacinto"}),
    (66, "The last page", None, "doc_logbook_totals.png", "66", "", "", LOG, {"style": "print", "label": "Logbook totals: 1,228.3 hours, 126 carrier landings"}),
    (68, "this time to cover", None, "b24_chichi_harbour.jpg", "68", "", "", f"U.S. Army Air Forces · NARA 204981413 · public domain", {"style": "print", "label": "B-24s over Chichi Jima harbour, Nov 1944"}),
    (75, "The trial record also", None, "marines_search_1946.jpg", "75", "", "", f"U.S. Marine Corps · public domain · {WC}", {"style": "print", "label": "Marines search for the remains of murdered airmen, Chichi Jima, 1946"}),
    (78, "Among the people", None, "futami_1920s.jpg", "78", "", "", f"Public domain · {WC}", {"style": "print", "label": "Futami harbour, Chichi Jima, 1920s"}),
    (80, "The main case opened", None, "guam_trial_building.jpg", "80", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "The war crimes trial building, Guam"}),
    (81, "There were thirty-eight", None, "trial_folder_tab.jpg", "81", "", "", TRIAL, {"style": "print", "label": "Case file: 'Tachibana, Yoshio et al.'"}),
    (81, "So the Navy lawyers", None, "koso_abe_guam.jpg", "81", "", "", f"NARA · public domain · {WC}", {"style": "print", "label": "A defendant before the Navy commission, Guam, 1947 (another case)"}),
    (85, "was sentenced to death", None, "guam_sentence.jpg", "85", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "A sentence is read, Navy war crimes commission, Guam"}),
    (87, "It was one day after", None, "tachibana_surrender.jpg", "87", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Lt. Gen. Tachibana signs the surrender of the Bonins, USS Dunlap, 3 Sept 1945"}),
    (93, "Their names are carved", None, "bl_H080-01.jpg", "93", "", "", BL, {"style": "print", "label": "John Delaney (left), Leo Nadeau and George Bush"}),
    (94, "Finback was decommissioned", None, "finback_launch.jpg", "94", "", "", f"U.S. Navy · NARA · public domain · {WC}", {"style": "print", "label": "USS Finback launched, Portsmouth, 1941"}),
    (94, "was scrapped in", None, "sanjac_underway.jpg", "94", "", "", f"U.S. Navy · 80-G-212798 · public domain · {WC}", {"style": "print", "label": "USS San Jacinto, January 1944"}),
    (95, "forty years to the day", None, "bush_1984_anniv.jpg", "95", "", "", "White House photo · George Bush Library · NARA · public domain", {"style": "print", "label": "Vice President Bush, 2 Sept 1984, forty years after"}),
    (95, "The signatures are still", None, "doc_logbook_sig1984.png", "95", "", "", LOG, {"style": "print", "label": "Logbook: 'Sept 2, 1984 · 40 years later'"}),
    (96, "In June 2002", None, "bush_2002_japan.jpg", "96", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Former President Bush in Japan, June 2002"}),
    (97, "George Herbert Walker Bush died", None, "bush_1994_tbm.jpg", "97", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Bush in an Avenger cockpit again, 1994"}),
    (98, "If your father", None, "bl_H048.jpg", "98", "", "", BL, {"style": "print", "label": "Torpedo Squadron 51"}),
    (99, "Today it belongs", None, "futami_pano.jpg", "99", "", "", f"CC BY-SA 3.0 · {WC}", {"style": "print", "label": "Futami Bay, Chichi Jima, today"}),
    (99, "and in a bay", None, "hinko_maru_wreck.jpg", "99", "", "", f"CC0 · {WC}", {"style": "print", "label": "Wreck of the Hinko Maru, Chichi Jima"}),
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
    SYNCED = SCENES | {"Headline", "QuoteCard", "DocDesk", "Verdict"}  # time fields may be spoken phrases (scenes.tsx, cards.tsx)
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
                elif card["type"] in SCENES or card["type"] == "Verdict":  # reconstruction scenes may run the whole paragraph (up to 30 s)
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
