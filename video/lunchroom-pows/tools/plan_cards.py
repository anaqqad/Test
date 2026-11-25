# Lunchroom POWs: films, tags and cards. exec()'d by tools/plan.py (shares its helpers).
# Owner rules: no 3D renders (25 Nov 2026); documents full frame on their own; no film/photo second shown more than twice.
F = {  # film key -> (file in assets/footage, fraction of height kept)
    "NS": ("negro_soldier_1944", 1), "NP": ("negro_personnel_1945", 1), "TW": ("teamwork_1946", 1),
    "TT": ("troop_train_1943", 1), "RS": ("restaurant_1946", 1), "CG": ("controlling_german_pows_1944", 1),
    "PS": ("prisoners_shipped_adc140", 1),
}

WC = "Wikimedia Commons"
STAND = "Stand-in · "
YANK1 = "Cpl. Rupert Trimmingham, letter to Yank, the Army Weekly, 28 April 1944"
YANK2 = "Yank, the Army Weekly, 28 July 1944, p. 14 · U.S. Army, public domain"
LOA = "Library of America, Reporting World War II (1995), pp. 470-73"

TAG = {
    "NS": "'The Negro Soldier', U.S. War Department, 1944 (NARA 111-OF-51)",
    "NP": "Black WACs sort Army mail, 1945 · Signal Corps film (NARA 111-ADC-3998)",
    "TW": "'Teamwork', U.S. War Department, 1946 (NARA 111-OF-14)",
    "TT": STAND + "'Troop Train', U.S. government film, 1943",
    "RS": STAND + "a lunchroom in a 1946 training film ('The Restaurant Operator')",
    "CG": "German prisoners of war in the U.S. · War Department Film Bulletin 164, c. 1944",
    "PS": "German prisoners shipped to the U.S. from North Africa · Signal Corps film (NARA 111-ADC-140)",
}

# lon/lat
CLA = [-92.56, 31.10]; HUA = [-110.35, 31.55]; SAL = [-97.61, 38.84]; ROB = [-92.30, 34.85]; FLO = [-111.39, 33.03]

TRIP = {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [-100, 33], "scale": 3.2}, {"t": "Somewhere on the way", "center": [-101, 32], "scale": 4.2}],
        "pins": [{"ll": CLA, "label": "Camp Claiborne, La.", "at": "Camp Claiborne", "color": "amber"},
                 {"ll": HUA, "label": "Fort Huachuca, Ariz.", "at": "Fort Huachuca", "color": "red"}],
        "arcs": [{"from": CLA, "to": HUA, "at": "Fort Huachuca", "style": "dashed", "color": "amber", "loft": 0.04, "draw": 45}],
        "footer": "Route generalised; the letter names no town · " + YANK1, "year": {"at": 0.1, "year": "1944", "sub": "Nine soldiers"}}

PLACES = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [-98, 36], "scale": 2.6}, {"t": "many parts of the country", "center": [-102, 35], "scale": 3.0}],
          "pins": [{"ll": SAL, "label": "Salina, Kans.", "at": 0.15, "color": "red"},
                   {"ll": ROB, "label": "Camp Robinson, Ark.", "at": 0.3, "color": "amber", "below": True},
                   {"ll": FLO, "label": "Florence, Ariz.", "at": "many parts of the country", "color": "red"}],
          "footer": "Brown (NYT, 1973) · Omaha Guide, 13 & 20 Jan 1945 · TIME, 28 Jul 2020", "year": {"at": 0.1, "year": "1942-45", "sub": "Not one town"}}

# ── quote cards (lines appear when the narrator says the phrase in the second string)
SWELL = QC("stills/colored_waiting.jpg", [("They entered the lunchroom, sat at the tables,", "entered the lunchroom"),
                                          ("had their meals served, talked, smoked,", "had their meals served"),
                                          ("in fact had quite a swell time.", "quite a swell time")], YANK1, "quite a swell time")
WHY = QC("stills/huachuca_93rd.jpg", [("Are we not American soldiers,", "Are we not American"),
                                      ("sworn to fight for and die if need be for this our country?", "die if need be"),
                                      ("Then why are they treated better than we are?", "Then why are they")], YANK1, "Then why are they")
BET = QC("stills/huachuca_patrol.jpg", [("Some of the boys are saying", "Some of the boys"), ("that you will not print this letter.", "will not print this letter"),
                                        ("I'm saying that you will.", "saying that you will")], YANK1, "saying that you will")
REBEL = QC("stills/durham_bus.jpg", [("I am a Southern rebel...", "Southern rebel"), ("If this incident is democracy,", "If this incident"),
                                     ("I don't want any part of it!", "any part of it")],
           "Cpl. Henry S. Wootton Jr., Fairfield-Suisun AAF, Calif. · Yank, 9 June 1944 (" + LOA + ")", "any part of it")
SERVE = QC("stills/durham_hitler.jpg", [("You boys know", "You boys know"), ("we don't serve colored here.", "serve colored here")],
           "Lloyd L. Brown, 'Brown v. Salina, Kansas', New York Times, 26 Feb 1973", "serve colored here")
HEARTS = QC("stills/huachuca_kitchen.jpg", [("If we were untermenschen in Nazi Germany,", "If we were untermenschen"),
                                           ("they would break our bones.", "break our bones"),
                                           ("As 'colored' men in Salina,", "colored' men in Salina"), ("they only break our hearts.", "break our hearts")],
            "Lloyd L. Brown, 'Brown v. Salina, Kansas', New York Times, 26 Feb 1973", "break our hearts")
BACK = QC("stills/horne_fuel.jpg", [("I went to the back where they were sitting", "I went to the back"),
                                    ("and sang with my back to all the other people.", "sang with my back")],
          "Lena Horne, interview for American Masters, PBS, 27 Feb 1996", "sang with my back")
GENEVA = HL("GENEVA CONVENTION · 27 JULY 1929 · ARTICLE 11", "The food ration of prisoners of war", "shall be equal",
            "shall be equal", "Convention relative to the Treatment of Prisoners of War (Avalon Project, Yale)", "in quantity and quality to that of troops at base camps.")
GLEE = HL("OMAHA GUIDE · 20 JANUARY 1945", "The German prisoners, of course, looked on", "with great glee",
          "looked on with great glee", "NAACP letter to Asst. Secretary of War McCloy, as printed in the Omaha Guide, 20 Jan 1945, p. 1")

SERVED = BIG(900000, "African Americans who served in uniform in World War II", "Jennifer D. Keene, Teaching American History, 'Letters to Yank Magazine'")
GERMANS = BIG(371000, "German prisoners of war held in the United States", "Matthias Reiss, via JSTOR Daily, 25 Feb 2023")
COPIES = BIG(2600000, "copies of every issue of Yank at its peak", LOA + " (introduction)")
LETTERS = {"type": "LedgerBars", "file": "YANK · 28 JULY 1944", "head": "Letters to Cpl. Trimmingham",
           "bars": [{"label": "Letters received", "value": 287, "figure": "287", "note": "by July 1944"},
                    {"label": "From white men and women in the armed service", "value": 183, "figure": "183", "note": "most from the Deep South"}],
           "max": 300, "source": YANK2}

AFTER = TL("1944-1948", "What came after", [
    ("28 Apr 1944", "Yank prints Trimmingham's letter"),
    ("Jun 1944", "The New Yorker: 'A Short Wait between Trains'"), ("Jan 1945", "Lena Horne's tour ends after Camp Robinson"),
    ("Jul 1946", "The last German prisoners leave the U.S."), ("26 Jul 1948", "Executive Order 9981")],
    YANK2 + " · JSTOR Daily (Reiss) · Omaha Guide · Truman Library")

DOC_LETTERS = LDOC("YANK · 28 JULY 1944", "Mail Call: 'Democracy?'", [("yank_287", "To date I've received 287 letters, and, strange as it may seem, 183 are from white men and women in the armed service")], YANK2)
DOC_BURMA = LDOC("YANK · 28 JULY 1944", "Mail Call: 'Democracy?'", [("yank_burma", "we the white soldiers will begin to wonder: What are we fighting for?")], YANK2)
DOC_EO = LDOC("EXECUTIVE ORDER 9981 · 26 JULY 1948", "Harry S. Truman", [("eo_equal", "there shall be equality of treatment and opportunity for all persons in the armed services without regard to race, color, religion or national origin")],
              "National Archives, via DPLA / Wikimedia Commons · public domain")
