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
