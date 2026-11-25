# Cowra breakout: films, tags and cards. exec()'d by tools/plan.py (shares its helpers).
F = {  # film key -> (file in assets/footage, fraction of height kept)
    "NA": ("jpow_noumea_a", 1), "NB": ("jpow_noumea_b", 1), "SAI": ("jpow_saipan", 1), "AIR": ("jpow_airman", 1),
    "JN": ("jp_newsreel42", 1), "JR": ("jp_navy_review", 1), "RT": ("jp_radio_tokyo", 1), "CAP": ("jpow_capture45", 1),
    "KYE": ("know_enemy_r2", 1), "AUV": ("au_veterans43", 1), "OE": ("our_enemy", 1),
    "R_ZERO": ("r3d_s_zero", 1), "R_DAY": ("r3d_s_camp_day", 1), "R_NIGHT": ("r3d_s_camp_night", 1), "R_BUG": ("r3d_s_bugle", 1),
    "R_CHG": ("r3d_s_charge", 1), "R_VK": ("r3d_s_vickers", 1), "R_BW": ("r3d_s_broadway", 1), "R_DAWN": ("r3d_s_dawn", 1),
    "R_FARM": ("r3d_s_farm", 1), "R_TOWER": ("r3d_s_night_tower", 1), "R_BDAY": ("r3d_s_broadway_day", 1),
    "R_SIDE": ("r3d_s_charge_side", 1), "R_ASH": ("r3d_s_ash_walk", 1), "R_VER": ("r3d_s_farm_verandah", 1),
}

WC = "Wikimedia Commons"
AWM = "Australian War Memorial"
LONG = "Gavin Long, The Final Campaigns (AWM, 1963), App. 5"
CURTIN = "John Curtin, House of Representatives, 8 Sept 1944 (Hansard vol. 179, p. 650)"
STAND = "Stand-in · "
REC = "Reconstruction · 3D, positions and figures approximate · "
NOUMEA = "Japanese prisoners of war in a U.S. camp, Noumea, New Caledonia, 1943"

TAG = {
    "NA": STAND + NOUMEA + " · U.S. Navy film (NARA 428-NPC-740)",
    "NB": STAND + NOUMEA + " · U.S. Navy film (NARA 428-NPC-738)",
    "SAI": STAND + "Japanese prisoner camp, Saipan, Jan 1945 · U.S. Navy film (NARA 428-NPC-6897)",
    "AIR": STAND + "a Japanese airman taken from the sea by USS Charrette · U.S. Navy film (NARA NPC-5315)",
    "JN": "Japanese newsreel, 1942 (captured; NARA NPC-10134)",
    "JR": "Japanese Navy newsreel, Feb 1942 (captured; NARA 428-NPC-322)",
    "RT": "Japanese newsreels, 1942 (AWM F06933)",
    "CAP": STAND + "Japanese soldiers taken prisoner, 1945 · U.S. Navy film (NARA 428-NPC-8925)",
    "KYE": "'Know Your Enemy: Japan', U.S. War Department, 1945 (NARA 111-OF-10)",
    "AUV": "Australian troops parade in Sydney, 1943 · United News (NARA)",
    "OE": "'Our Enemy: The Japanese', U.S. government film, 1943",
    "R_ZERO": REC + "Toyoshima's Zero comes down on Melville Island, 19 Feb 1942",
    "R_DAY": REC + "No. 12 POW Compound, Cowra: an octagon about 800 yards across (" + LONG + ")",
    "R_NIGHT": REC + "Cowra at night: lamps on the wire, towers over B camp",
    "R_BUG": REC + "B camp, just before 2 a.m., 5 Aug 1944",
    "R_CHG": REC + "about 2 a.m.: the mobs go for the wire with blankets; the huts are set alight",
    "R_VK": REC + "a Vickers gun on its trailer outside the north-west wire (Cooper, AWM S01027)",
    "R_BW": REC + "the road through the compound: men in the side ditch until dawn",
    "R_DAWN": REC + "B camp at first light, 5 Aug 1944",
    "R_FARM": REC + "a farm outside Cowra, 5 Aug 1944 (Weir family, AWM S00932)",
    "R_TOWER": REC + "from a guard tower over B camp at night",
    "R_BDAY": REC + "the road through the compound ('Broadway'), by day",
    "R_SIDE": REC + "blankets over the wire of B camp, about 2 a.m.",
    "R_ASH": REC + "the burnt floors of B camp's huts, morning of 5 Aug 1944",
    "R_VER": REC + "the Weir farm verandah, 5 Aug 1944 (AWM S00932)",
}

# lon/lat
DAR = [130.84, -12.46]; MEL = [131.0, -11.6]; LOV = [140.35, -34.28]; HAY = [144.84, -34.51]; COW = [148.69, -33.83]
SYD = [151.21, -33.87]; JAP = [139.7, 35.7]

DARWIN = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [134, -20], "scale": 2.6}, {"t": "attacked the port", "center": [131, -12.8], "scale": 9}],
          "pins": [{"ll": DAR, "label": "Darwin", "at": "attacked the port", "color": "red"},
                   {"ll": SYD, "label": "Sydney", "at": 0.6}],
          "cards": [{"at": "attacked the port", "kicker": "19 February 1942", "body": "The first air raid on Darwin", "accent": "red"}],
          "footer": "AWM, 'The bugle and the breakout' (2019)", "year": {"at": 0.1, "year": "1942", "sub": "Northern Australia"}}

MELVILLE = {"type": "GlobeMap", "theme": "history",
            "cam": [{"t": 0, "center": [131.0, -12.3], "scale": 14}, {"t": "He came down", "center": [131.0, -11.8], "scale": 20}],
            "pins": [{"ll": DAR, "label": "Darwin", "at": 0.3}, {"ll": MEL, "label": "Melville Island", "at": "He came down", "color": "amber"}],
            "footer": "Positions approximate · AWM P00022.002", "year": {"at": 0.1, "year": "1942", "sub": "Melville Island"}}

JOURNEY = {"type": "GlobeMap", "theme": "history",
           "cam": [{"t": 0, "center": [138, -24], "scale": 2.5}, {"t": "On January ninth", "center": [144, -30], "scale": 3.4}],
           "pins": [{"ll": DAR, "label": "Darwin", "at": 0.3}, {"ll": LOV, "label": "Loveday", "at": "a camp at Loveday", "color": "amber", "below": True},
                    {"ll": HAY, "label": "Hay", "at": "then to Hay", "color": "amber"},
                    {"ll": COW, "label": "Cowra", "at": "On January ninth", "color": "red"}],
           "arcs": [{"from": DAR, "to": LOV, "at": "a camp at Loveday", "style": "dashed", "color": "amber", "loft": 0.06, "draw": 40},
                    {"from": LOV, "to": HAY, "at": "then to Hay", "style": "dashed", "color": "amber", "loft": 0.03, "draw": 30},
                    {"from": HAY, "to": COW, "at": "On January ninth", "style": "dashed", "color": "red", "loft": 0.03, "draw": 30}],
           "footer": "Route generalised · Cowra Japanese War Cemetery database, grave 510", "year": {"at": 0.1, "year": "1942-43", "sub": "'Tadao Minami'"}}

HAYMAP = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [148.5, -33.9], "scale": 16}, {"t": "to the big prisoner", "center": [146.8, -34.1], "scale": 9}],
          "pins": [{"ll": COW, "label": "Cowra · No. 12 POW Compound", "at": 0.3, "color": "red"}, {"ll": SYD, "label": "Sydney", "at": 0.8, "below": True},
                   {"ll": HAY, "label": "Hay", "at": "to the big prisoner", "color": "amber"}],
          "arcs": [{"from": COW, "to": HAY, "at": "to the big prisoner", "style": "dashed", "color": "amber", "loft": 0.02, "draw": 40}],
          "footer": LONG + ", p. 623", "year": {"at": 0.1, "year": "Aug 1944", "sub": "The move to Hay"}}

HOME = {"type": "GlobeMap", "theme": "history",
        "cam": [{"t": 0, "center": [146, -32], "scale": 4}, {"t": "they were shipped home", "center": [142, 2], "scale": 1.7}],
        "pins": [{"ll": HAY, "label": "Hay", "at": 0.3}, {"ll": [145.0, -36.62], "label": "Murchison", "at": "at Murchison", "color": "amber"},
                 {"ll": SYD, "label": "Sydney", "at": "they were shipped home"}, {"ll": JAP, "label": "Japan", "at": "a defeated Japan", "color": "red"}],
        "arcs": [{"from": SYD, "to": JAP, "at": "they were shipped home", "style": "dashed", "color": "amber", "loft": 0.06, "draw": 50}],
        "footer": "Route generalised · AWM 126121 (Balmain, 2 Mar 1946)", "year": {"at": 0.1, "year": "1946", "sub": "Repatriation"}}

# ── quote cards (lines appear when the narrator says the phrase in the second string)
CODE = QC("stills/bowing_sun.jpg", [("If alive, do not suffer the disgrace", "If alive"), ("of becoming a prisoner.", "becoming a prisoner")],
          "Field Service Code (Senjinkun), 1941 · Tokyo Gazette translation", "becoming a prisoner")
STICK = QC("stills/zero_melville.jpg", [("I see him through the bushes and I go first.", "I see him through"),
                                       ("I sneak up quick and wait behind a tree.", "I sneak up quick")],
           "Matthias Ulungura · Library & Archives NT, 'Tiwi Heroes'", "wait behind a tree")
FALSE = QC("stills/jpows_brisbane.jpg", [("Many of us had false names", "Many of us had"), ("and we just didn't talk about the past.", "talk about the past")],
           "Marekuni Takahara, Cowra survivor · AWM oral history S03331, 2004", "talk about the past")
NEVER = QC("stills/guard_tower.jpg", [("We'd never ever thought", "We'd never ever"), ("they'd even try it.", "even try it")],
           "Sgt Ashley Cooper, 22nd Garrison Battalion · AWM S01027, p. 19", "even try it")
FEAR = QC("stills/parade_1115.jpg", [("They read into our humane treatment of them", "humane treatment"),
                                    ("our secret fear of them.", "secret fear")],
          "Maj. E. V. Timms, 22nd Garrison Battalion, 1946 · " + LONG + ", p. 623", "secret fear")
VOTE = QC("stills/sportsground.jpg", [("I said I voted yes,", "I said I voted"), ("but to be honest, I didn't think it was a good idea.", "to be honest"),
                                     ("I wanted to vote no.", "wanted to vote no")],
          "Teruo Murakami, Cowra survivor · AWM oral history S03331, 2004", "wanted to vote no")
ALONG = QC("stills/parade_sports.jpg", [("I felt, okay,", "I felt, okay"), ("I come along with you.", "come along with you")],
           "Masayoshi Yamada, Cowra survivor · AWM S03331, 2004", "come along with you")
FIREWOOD = QC("stills/blankets_wire.jpg", [("Just like a pile of firewood,", "Just like a pile"), ("with dead bodies.", "with dead bodies")],
              "Sgt Ashley Cooper · AWM S01027, p. 23", "with dead bodies")
DITCH = QC("stills/aerial_b_after.jpg", [("We will not harm you,", "We will not harm"), ("but you have to come back.", "you have to come back"),
                                        ("Get out of the ditch.", "Get out of the ditch")],
           "An Australian guard, as Teruo Murakami remembered it · SBS News, 2019", "Get out of the ditch")
SCONES = QC("stills/camp_southeast.jpg", [("Well, just take them round to the side verandah", "just take them round"),
                                         ("I'll just finish making these scones.", "finish making these scones")],
            "May Weir, as her daughter Margaret told it · AWM S00932, 1990", "finish making these scones")
MISERABLE = QC("stills/jcem_rows.jpg", [("I don't want any young person", "I don't want any"), ("to do the things we have done,", "the things we have done"),
                                       ("because it's such a miserable thing.", "such a miserable thing")],
               "Teruo Murakami, at Cowra, 2019 · SBS News", "such a miserable thing")
NEVERAGAIN = QC("stills/garden_lake.jpg", [("No war.", "No war"), ("Never, never again.", "Never, never again")], "Teruo Murakami, 2019 · SBS News", "Never, never again")
ALIVE = QC("stills/garden_cherry.jpg", [("Everybody thought we would die,", "Everybody thought"), ("but something happened,", "something happened"),
                                       ("and we are still alive.", "still alive")],
           "Masayoshi Yamada · AWM S03331, 2004", "still alive")

SUICIDAL = HL("MILITARY COURT OF INQUIRY · AUGUST 1944", "", "a suicidal disregard of life", "a suicidal disregard", CURTIN)
INCIDENT = HL("AUSTRALIA, 1944", "Known only as", "the Cowra incident", "the Cowra incident", "SMH, 1993, 'True story behind the Cowra breakout'")

PRISONERS = BIG(2223, "Japanese POWs in Australia, Aug 1944 (544 of them seamen)", LONG + ", p. 623")
CAMPB = BIG(1104, "Japanese prisoners in No. 12 POW Compound, Cowra, August 1944", LONG + ", p. 623")
BROUGHT = BIG(334, "Brought back in nine days after the breakout (25 dead)", AWM + " · SMH, 1993")
DEAD = {"type": "IconCount", "icon": "man", "total": 1104, "label": "Japanese prisoners in B camp", "accent": "B camp",
        "highlight": {"n": 231, "label": "Dead (court of inquiry)", "accent": "Dead", "at": "two hundred and thirty-one"},
        "file": "COWRA · 5 AUGUST 1944", "source": CURTIN + " · " + LONG}

NIGHT = TL("5 AUGUST 1944", "The night at Cowra", [
    ("4 Aug", "Notice: the privates are to go to Hay on the 7th"), ("Midnight", "The leaders meet; the men vote"),
    ("About 2 a.m.", "A man runs to the gate; the bugle"), ("5:30 a.m.", "The shooting dies down at dawn"),
    ("7 a.m.", "The town of Cowra hears")], LONG + " · " + CURTIN + " · AWM S01027")

DOC_BASEBALL = LDOC("THE FINAL CAMPAIGNS · 1963", "The official history", [("long_baseball", "constant wrestling and baseball")], LONG + ", p. 623")
DOC_WEAPONS = LDOC("THE FINAL CAMPAIGNS · 1963", "The official history",
                   [("long_weapons", "knives, baseball bats, clubs studded with nails and hooks, wire stilettos and garotting cords")], LONG + ", p. 624")
DOC_GAZETTE = LDOC("THE LONDON GAZETTE · 1 SEPT 1950", "George Cross",
                   [("gazette_gc", "stood their ground and continued to work the gun until bashed to death")],
                   "The London Gazette, issue 39008, p. 4431 · Crown copyright, Open Government Licence")
