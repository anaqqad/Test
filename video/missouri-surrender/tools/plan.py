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
    "NVB": ("navy_victory_bulletin", 1), "UNS": ("un_signing", 1), "M10": ("mo_14510", 1), "M06": ("mo_14506", 1),
    "M18": ("mo_14518", 1), "M19": ("mo_14519", 1), "M13": ("mo_14513", 1), "A98": ("mo_adc9888", 1), "A63": ("mo_adc5163", 1),
    "UNL": ("un_landing", 1), "SM": ("screen_mag68", 0.88), "PRT": ("pow_rescue_tokyo", 1), "PYK": ("pow_yokohama", 1),
    "SHG": ("shinagawa_camp", 1), "WMN": ("wainwright_manila", 1), "ATS": ("atsugi_adc2992", 1), "BET": ("white_bettys", 1),
    "FUJ": ("fleet_fuji", 1), "ATC": ("atsugi_colour", 1), "ASH": ("ashore_japan", 1),
    "R_ARR": ("r3d_s_arrive", 1), "R_DP": ("r3d_s_deck_plan", 1), "R_DS": ("r3d_s_deck_sign", 1), "R_FLY": ("r3d_s_flyover", 1),
    "R_ROAD": ("r3d_s_road", 1), "R_ATS": ("r3d_s_atsugi", 1), "R_DROP": ("r3d_s_drop", 1), "R_OMO": ("r3d_s_omori", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
NHHC = "Naval History and Heritage Command"
RGM = "Reports of General MacArthur, Vol. I Supplement (GHQ SCAP, 1966)"
KASE = "Toshikazu Kase, Journey to the Missouri (Yale, 1950)"
HALSEY = "Admiral Halsey's Story (1947)"
EICH = "Robert L. Eichelberger, Our Jungle Road to Tokyo (1950)"
SPEECH = "MacArthur's speech, 2 Sept 1945 · NHHC (Turner papers)"
NIDS = "National Institute for Defense Studies, Japan Ministry of Defense (2026)"
STAND = "Stand-in · "
REC = "Reconstruction · 3D, positions and figures approximate · "

TAG = {
    "NVB": "USS Missouri, 2 Sept 1945 · U.S. Navy Combat Bulletin No. 7 (NARA 80-MN-9034G)",
    "UNS": "USS Missouri, 2 Sept 1945 · United News 'Japanese Sign Final Surrender' (NARA 208-UN-171B)",
    "M10": "USS Missouri, 2 Sept 1945 · U.S. Navy film (NARA 428-NPC-14510)",
    "M06": "USS Missouri, 2 Sept 1945 · U.S. Navy film (NARA 428-NPC-14506)",
    "M18": "USS Missouri, 2 Sept 1945 · U.S. Navy film (NARA 428-NPC-14518)",
    "M19": "USS Missouri, 2 Sept 1945 · U.S. Navy film (NARA 428-NPC-14519)",
    "M13": "USS Missouri, 2 Sept 1945 · U.S. Navy film (NARA 428-NPC-14513)",
    "A98": "USS Missouri, 2 Sept 1945 · Signal Corps film (NARA 111-ADC-9888)",
    "A63": "USS Missouri, 2 Sept 1945 · Signal Corps film (NARA 111-ADC-5163)",
    "UNL": "Allied forces land in Japan, Aug 1945 · United News (NARA 208-UN-171A)",
    "SM": "Army-Navy Screen Magazine No. 68, 'Surrender in the Pacific', 1945 · Signal Corps (NARA)",
    "PRT": "Prisoners freed from camps near Tokyo, 30 Aug 1945 · U.S. Navy film (NARA 428-NPC-14557)",
    "PYK": "Released prisoners of war, Yokohama, 1 Sept 1945 · AAF film (NARA 18-CS-4554)",
    "SHG": "Shinagawa prison camp, Tokyo, Sept 1945 · U.S. Navy film (NARA 428-NPC-14615)",
    "WMN": "Gen. Wainwright lands at Nichols Field, Manila, 30 Aug 1945 · Signal Corps film (NARA 111-ADC-5188)",
    "ATS": "Atsugi airfield, 30 Aug 1945 · Signal Corps film (NARA 111-ADC-2992)",
    "BET": "Kawabe's envoys in the white Betty bombers, Ie Shima, 19 Aug 1945 · U.S. Navy film (NARA 428-NPC-15471)",
    "FUJ": "The U.S. fleet in Tokyo Bay, 1945 · U.S. Navy film (NARA NPC-15559)",
    "ATC": "Atsugi airfield and Yokohama harbour, 1945 · AAF colour film (CS-9405)",
    "ASH": "Japan, Sept 1945 · U.S. Navy film (NARA 428-NPC-15493)",
    "R_ARR": REC + "the launch from the destroyer to the Missouri, 8:56 a.m.",
    "R_DP": REC + "the deck, after NHHC's deck plan and the ceremony films",
    "R_DS": REC + "the signing table, after the Signal Corps photographs",
    "R_FLY": REC + "the flyover, 9:25 a.m.",
    "R_ROAD": REC + "the road from Atsugi to Yokohama, 30 Aug 1945, after " + RGM + " and " + EICH,
    "R_ATS": REC + "Atsugi, 28 Aug 1945, 8:28 a.m., after " + RGM,
    "R_DROP": REC + "a B-29 supply drop over a prison camp, Aug-Sept 1945",
    "R_OMO": REC + "the landing boats reach Omori camp, 29 Aug 1945",
}


def LQ(file, head, key, who, source, before="", after=""):
    return {"type": "LedgerQuote", "file": file, "head": head, "before": before, "key": key, "after": after, "who": who, "source": source}


def HL(kicker, before, accent, at, source, after=""):
    return {"type": "Headline", "kicker": kicker, "before": before, "accent": accent, "after": after, "at": at, "source": source}


def TL(file, head, rows, source):
    return {"type": "LedgerTimeline", "file": file, "head": head, "rows": [{"date": a, "text": b} for a, b in rows], "source": source}


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


def BIG(value, label, source):
    return {"type": "BigNumber", "value": value, "label": label, "source": source}


# lon/lat
TOK = [139.69, 35.69]; ATSU = [139.45, 35.45]; YOKO = [139.64, 35.44]; OMOR = [139.74, 35.58]; YOKS = [139.67, 35.28]
MO = [139.77, 35.36]; IESH = [127.80, 26.71]; MNL = [120.98, 14.60]; MUK = [123.43, 41.80]; OKI = [127.77, 26.33]

ENVOYS = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [132, 28], "scale": 2.6}, {"t": "flew to the island", "center": [128, 24], "scale": 3.2}],
          "pins": [{"ll": TOK, "label": "Tokyo", "at": 0.3}, {"ll": IESH, "label": "Ie Shima", "at": "flew to the island", "color": "amber"},
                   {"ll": MNL, "label": "Manila · MacArthur's HQ", "at": "From there", "color": "red"}],
          "arcs": [{"from": TOK, "to": IESH, "at": "flew to the island", "style": "dashed", "color": "amber", "loft": 0.05, "draw": 40},
                   {"from": IESH, "to": MNL, "at": "From there", "style": "dashed", "color": "amber", "loft": 0.04, "draw": 40}],
          "cards": [{"at": "flew to the island", "kicker": "19 August 1945", "body": "Two white Betty bombers, call signs Bataan One and Two", "accent": "amber"}],
          "footer": "Route generalised · NHHC H-Gram 053", "year": {"at": 0.1, "year": "1945", "sub": "The envoys to Manila"}}

BAY = {"type": "GlobeMap", "theme": "history",
       "cam": [{"t": 0, "center": [139.6, 35.5], "scale": 40}, {"t": 3.0, "center": [139.62, 35.48], "scale": 55}],
       "pins": [{"ll": TOK, "label": "Tokyo", "at": 0.2}, {"ll": ATSU, "label": "Atsugi airfield", "at": 0.8, "color": "red"},
                {"ll": YOKS, "label": "Yokosuka", "at": 2.0}],
       "footer": "Positions approximate", "year": {"at": 0.1, "year": "1945", "sub": "Atsugi, Kanagawa"}}

RESCUE = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [139.7, 35.45], "scale": 45}, {"t": 3.0, "center": [139.72, 35.5], "scale": 60}],
          "pins": [{"ll": TOK, "label": "Tokyo", "at": 0.2}, {"ll": OMOR, "label": "Omori camp", "at": 0.8, "color": "red"},
                   {"ll": MO, "label": "Third Fleet anchorage", "at": 1.4, "color": "amber"}],
          "arcs": [{"from": MO, "to": OMOR, "at": 1.6, "style": "dashed", "color": "amber", "loft": 0.0, "draw": 30}],
          "footer": "Positions approximate · " + HALSEY, "year": {"at": 0.1, "year": "29 Aug", "sub": "Tokyo Bay"}}

WAINMAP = {"type": "GlobeMap", "theme": "history",
           "cam": [{"t": 0, "center": [128, 32], "scale": 2.4}, {"t": 6.0, "center": [128, 27], "scale": 2.4}],
           "pins": [{"ll": MUK, "label": "Mukden, Manchuria", "at": 0.3, "color": "red"}, {"ll": MNL, "label": "Manila", "at": 6.0, "color": "amber"},
                    {"ll": ATSU, "label": "Atsugi", "at": 9.5, "color": "amber"}],
           "arcs": [{"from": MUK, "to": MNL, "at": 6.0, "style": "dashed", "color": "amber", "loft": 0.05, "draw": 40},
                    {"from": MNL, "to": ATSU, "at": 9.5, "style": "dashed", "color": "amber", "loft": 0.05, "draw": 40}],
           "footer": "Route generalised · Wainwright's own story (1945)", "year": {"at": 0.1, "year": "1945", "sub": "Out of Manchuria"}}

MILLION = QC("stills/delegation_arrives.jpg", [("A million eyes seemed to beat on us", "A million eyes"),
              ("Never had I realized that staring eyes could hurt so much.", "staring eyes could hurt")],
             "Toshikazu Kase, Journey to the Missouri (1950)", "staring eyes could hurt")
FEARS_SRC = RGM + ", p. 24, citing Yomiuri, 19 Aug 1945"
ROOFS = QC("stills/drop_hanawa_roofs.jpg", [("S O S", "S O S"), ("Have hospital cases here", "Have hospital cases"),
            ("Drop radio please", "Drop radio please"), ("Men from Corregidor, Bataan thank Wasp", "thank Wasp")],
           "Messages painted on prison camp roofs, Aug-Sept 1945 · " + RGM + ", p. 100", "thank Wasp")
GOAHEAD = QC("stills/missouri_anchored.jpg", [("Go ahead.", "Go ahead"), ("General MacArthur will understand.", "will understand")],
             "Fleet Admiral Nimitz to Admiral Halsey, 29 Aug 1945 · " + HALSEY, "will understand")
PERIOD = QC("stills/pows_flags.jpg", [("I have no authority to release these men.", "I have no authority"),
             ("You have no authority, period!", "You have no authority")],
            "The commandant of Omori camp, and Cdr. Harold Stassen, 29 Aug 1945 · " + HALSEY, "You have no authority")
PROTEST = QC("stills/pows_flags.jpg", [("A U.S. Naval landing unit of about 150 men", "landing unit"),
              ("broke into the Shinagawa camp of the Allied War Prisoners", "broke into the"),
              ("and forcibly led away the prisoners.", "forcibly led away")],
             "Japanese government protest, radio of 1 Sept 1945 · " + RGM + ", p. 100", "forcibly led away")
PAYOFF = QC("stills/atsugi_mac_press.jpg", [("Melbourne to Tokyo was a long road,", "Melbourne to"), ("but this looks like the payoff.", "looks like the payoff")],
            "General MacArthur at Atsugi, 30 Aug 1945 · GHQ summary, via " + RGM + ", p. 29", "looks like the payoff")
NOFLAG = QC("stills/delegation_bw.jpg", [("Diplomats without flag", "Diplomats without flag"), ("and soldiers without sword", "soldiers without sword")],
            "Toshikazu Kase, Journey to the Missouri (1950)", "soldiers without sword")
MALICE = QC("stills/mac_speaking_bw.jpg", [("Nor is it for us here to meet", "Nor is it for us"), ("in a spirit of distrust, malice or hatred.", "distrust, malice or hatred")],
            "General Douglas MacArthur, USS Missouri, 2 Sept 1945 · " + SPEECH, "distrust, malice or hatred")
HOPE = QC("stills/mac_speaking_colour.jpg", [("a world dedicated to the dignity of man", "dignity of man"),
           ("and the fulfillment of his most cherished wish", "most cherished wish"), ("for freedom, tolerance and justice.", "tolerance and justice")],
          "General Douglas MacArthur, USS Missouri, 2 Sept 1945 · " + SPEECH, "tolerance and justice")
SURPRISE = QC("stills/delegation_colour.jpg", [("For me, who expected the worst humiliation,", "the worst humiliation"),
               ("this was a complete surprise.", "complete surprise")], "Toshikazu Kase, Journey to the Missouri (1950)", "complete surprise")
GUNS = QC("stills/flyover_fleet.jpg", [("Today the guns are silent.", "Today the guns"), ("A great tragedy has ended.", "great tragedy"),
           ("A great victory has been won.", "victory has been won")],
          "General MacArthur, radio address to America, 2 Sept 1945 · NHHC (Turner papers)", "victory has been won")
QUESTION = QC("stills/envoys_leave.jpg", [("Would it have been possible for us,", "Would it have been"), ("had we been victorious,", "had we been victorious"),
               ("to embrace the vanquished with a similar magnanimity?", "similar magnanimity"), ("Clearly, it would have been different.", "Clearly, it would")],
              "Toshikazu Kase, on his report to the Emperor · Journey to the Missouri (1950)", "Clearly, it would")
NOBLER = QC("stills/delegation_departs_colour.jpg", [("We were defeated by a nobler ideal.", "nobler ideal")],
            "Toshikazu Kase, Journey to the Missouri (1950)", "nobler ideal")
REBEL = HL("THE ATSUGI REBELLION · 15-21 AUGUST 1945", "A divine nation", "does not surrender", "told them the Emperor", NIDS)
SORTIES = BIG(158, "Prison camps reached by B-29 supply drops · 900 sorties · 4,470 tons", RGM + ", pp. 94-98")
BEDRIDDEN = BIG(417, "Tokyo-area prisoners who could not get out of bed (Japanese count)", RGM + ", p. 100")
FREED = BIG(32624, "Allied prisoners of war freed in Japan within three weeks", RGM + ", p. 101")
CLOCK = TL("2 SEPTEMBER 1945", "Thirty-three minutes on the Missouri", [
    ("8:56", "The Japanese delegation comes aboard"), ("9:02", "MacArthur opens the ceremony"),
    ("9:04", "Shigemitsu signs · 9:06 Umezu · 9:08 MacArthur"), ("9:25", "'These proceedings are closed'"),
    ("9:29", "The delegation leaves the ship")],
    "NHHC, 'Japan Capitulates' · " + KASE)
# ── shots: sh() adds the film's source tag when the film changes; tag=False for a repeat, or a custom tag ──
GENERIC = set()  # every film here is of the event itself (Tokyo Bay, Aug-Sept 1945); stand-ins are tagged by hand


def sh(anchor, key, t, tag=True):
    out = [(anchor, key, t)]
    if tag:
        txt = tag if isinstance(tag, str) else ((STAND if key in GENERIC else "") + TAG[key])
        out.append(("@", anchor, txt))
    return out


def card(anchor, c, until=None):
    return [("#", anchor, until, c)]


def LDOC(file, head, spans, source):
    return {"type": "LedgerDocument", "file": file, "head": head, "source": source, "spans": [{"doc": d, "say": s} for d, s in spans]}


SUB = {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented"}

P = [
    # ── 1. The little flags
    # 0
    sh("Tokyo Bay, the second", "A98", 8.0) + card("Tokyo Bay, the second", SLUG("2 September 1945 · 8:56 a.m.", "USS Missouri, Tokyo Bay")) +
    sh("A small boat", "R_ARR", 0.0) + sh("Eleven Japanese men", "UNS", 111.0) + sh("The first of them", "M18", 402.0),
    # 1
    sh("At the top of the ladder", "M18", 60.0, False) + sh("Sailors fill every", "A98", 93.0, False) + sh("Photographers hang", "A98", 107.0, False) +
    sh("Admiral Nimitz wrote", "M18", 145.0, False) + sh("More than two hundred", "A98", 79.0, False),
    # 2
    sh("One of the eleven", "UNS", 129.0, False) + sh("Years later he wrote", "M13", 103.0) + card("He felt, he wrote", MILLION),
    # 3
    sh("They are led to", "M19", 130.0) + sh("waited like penitent", "M19", 200.0, False) + sh("While he waited", "A98", 107.0, False) +
    sh("Painted on it", "M13", 7.6),
    # 4
    sh("He tried to count", "M13", 8.5, False) + sh("He thought of the young", "UNS", 180.0, False) + sh("He had been brought", "M19", 260.0, False),
    # 5
    sh("He was wrong", "R_DP", 120.0 / 30) + sh("And before that day", "UNS", 163.0, False) + sh("This is the documented", "A63", 300.0) +
    sh("the memoirs of the men", "NVB", 527.0) + sh("To understand", "M10", 30.0),
    # ── 2. What Japan feared
    # 6
    sh("On the fifteenth of August", "SM", 18.0) + card("On the fifteenth of August", SLUG("15 August 1945", "Japan hears the Emperor's broadcast")) +
    sh("He told them", "SM", 56.0, False) + sh("For the first time", "SM", 93.0, False),
    # 7
    sh("Nobody knew", "SM", 93.0, False) + sh("The newspaper", "ASH", 441.0) + card("The newspaper", LDOC("FROM THE FILE · MACARTHUR'S STAFF HISTORY", "What Tokyo feared, August 1945",
        [("rgm_fears", "American soldiers would loot Japan. Americans would rob Japan of all the food. Women and girls would be violated. All men would be killed. What was left of Tokyo would be devastated.")], FEARS_SRC)),
    # 8
    sh("The government that had", "ASH", 106.0) + sh("His job was to hand", "UNL", 120.0) + sh("Three to four million", "UNL", 175.0, False),
    # 9
    sh("His first test", "UNL", 138.0, False) + sh("The Allies had ordered", "BET", 401.0),
    # ── 3. The white bombers
    # 10
    sh("On the nineteenth of August", "BET", 87.0, False) + card("On the nineteenth of August", SLUG("19 August 1945", "Envoys to Manila")) +
    sh("The Allies had ordered how", "BET", 436.0, False) + sh("They flew in two", "BET", 401.0, False),
    # 11
    sh("Their call signs", "BET", 262.0, False) + card("Their call signs", ENVOYS),
    # 12
    sh("summed up the talks", "BET", 541.0, False) + sh("there were no negotiations", "BET", 576.0, False) + sh("Then they started home", "BET", 611.0, False),
    # 13
    sh("They did not arrive", "BET", 506.0, False) + sh("In Tokyo, Prime Minister", "ASH", 380.0) + sh("He later wrote", "SM", 56.0),
    # 14
    sh("When", "ASH", 319.0) + sh("says the Emperor", "SM", 93.0) + sh("But", "ATS", 426.0) + sh("At the very airfield", "R_ATS", 0.5),
    # ── 4. A divine nation does not surrender
    # 15
    sh("The airfield was called", "R_ATS", 1.0, False) + card("The airfield was called", BAY) + sh("It was the home of the", "ATS", 284.0) +
    sh("It had fought right up", "UNL", 120.0) + sh("It had only ever", "ATS", 376.0),
    # 16
    sh("After the Emperor's broadcast", "ATS", 376.0) + card("he told them the Emperor", REBEL) + sh("Then he sent a radio", "M19", 27.0),
    # 17
    sh("He had about a thousand", "R_ATS", 3.0) + sh("From the sixteenth", "ATS", 426.0),
    # 18
    sh("A rear admiral", "ATS", 444.0, False) + sh("later wrote that men", "A98", 7.0) + sh("plane was supposed to land", "R_ATS", 2.0),
    # 19
    sh("The navy did not dare", "ATS", 398.0) + sh("It was something much smaller", "ATS", 376.0, False),
    # ── 5. Fever
    # 20
    sh("had malaria", "ATS", 398.0, False) + sh("By the eighteenth", "ASH", 289.0),
    # 21
    sh("On the evening of the twentieth", "ASH", 319.0, False) + sh("The prince told them", "ASH", 380.0, False),
    # 22
    sh("Early the next morning", "UNL", 120.0) + sh("Without him", "ATS", 444.0) + sh("They were brought back", "ATS", 398.0) +
    sh("The propellers were taken", "R_ATS", 0.0) + sh("That afternoon the", "UNL", 194.0),
    # 23
    sh("A week later", "R_ATS", 0.0) + sh("was court-martialed", "ATS", 307.0) + sh("But while", "R_DROP", 0.0),
    # ── 6. Bombers without bombs
    # 24
    sh("From the twenty-seventh", "R_DROP", 2.0, False) + card("From the twenty-seventh", SLUG("27 August 1945", "The B-29s come back")) +
    sh("They flew low over", "SM", 206.0) + sh("MacArthur's staff wrote", "R_DROP", 5.0, False),
    # 25
    sh("The planes had words", "SM", 281.0) + sh("Under every camp roof", "SHG", 62.0) + sh("Now the", "R_DROP", 1.5),
    # 26
    sh("The prisoners painted answers", "SHG", 71.0, False) + card("The staff history lists", ROOFS),
    # 27
    sh("Not every drop", "SHG", 223.0, False) + sh("Eight of the bombers", "SHG", 233.0, False) + card("Over the next three weeks", SORTIES),
    # 28
    sh("But food could be", "SHG", 24.0, False) + sh("Men who could not walk", "SHG", 185.0, False) + card("The Japanese government's own", BEDRIDDEN),
    # ── 7. The first one hundred and fifty
    # 29
    sh("The first landing was set", "UNL", 157.0) + sh("A typhoon pushed", "UNL", 46.0, False) + sh("In the meantime", "ATS", 330.0),
    # 30
    sh("At eight twenty-eight", "R_ATS", 0.0) + card("At eight twenty-eight", SLUG("28 August 1945 · 8:28 a.m.", "Atsugi airfield")) +
    sh("On board was the advance", "UNL", 434.0) + sh("The Japanese officer in charge", "R_ATS", 4.0, False) + sh("later wrote in his memoir", "ATS", 307.0) + sh("ignoring the wind sock", "R_ATS", 6.5, False),
    # 31
    sh("walked up to Colonel Tench", "ATS", 307.0) + sh("He offered the Americans", "UNL", 120.0) + sh("Within forty-five minutes", "M19", 46.0),
    # 32
    sh("Fewer than two hundred", "UNL", 342.0) + sh("wrote that he had never", "UNL", 416.0, False),
    # 33
    sh("That same morning", "FUJ", 10.0) + sh("And that night", "UNL", 268.0),
    # ── 8. Go ahead
    # 34
    sh("The voices belonged", "UNL", 212.0, False) + sh("Their story reached", "PRT", 8.0) + sh("The next day a Swiss", "PRT", 150.0, False),
    # 35
    sh("The Red Cross gave", "PRT", 166.0, False) + card("The Red Cross gave", RESCUE) + sh("At the hospital of a camp", "SHG", 24.0),
    # 36
    sh("Halsey had three hospital", "SM", 1067.0) + sh("But he had an order", "M19", 64.0),
    # 37
    sh("On the twenty-ninth", "FUJ", 60.0) + sh("He sent MacArthur a radio", "M19", 82.0) + sh("Then he added", "M19", 46.0, False) + card("In Halsey's memoir", GOAHEAD),
    # ── 9. No authority
    # 38
    sh("That afternoon, landing boats", "R_OMO", 0.0) + card("That afternoon, landing boats", SLUG("29 August 1945 · afternoon", "Tokyo Bay")) +
    sh("The rescue was led", "PRT", 309.0) + sh("chief of staff was Commander", "PRT", 214.0, False),
    # 39
    sh("At the gate of the camp", "R_OMO", 4.0, False) + sh("records what he said", "PRT", 150.0, False) + card("records what he said", PERIOD),
    # 40
    sh("Inside the wire", "PRT", 103.0) + sh("The Navy's photographs show", "R_OMO", 2.0) + sh("The Associated Press", "PRT", 198.0),
    # 41
    sh("Among them was Major", "PRT", 230.0, False) + sh("The senior prisoner", "PRT", 166.0, False),
    # 42
    sh("At ten past seven", "PRT", 309.0, False) + sh("The Navy gave them", "PRT", 340.0, False) + sh("By midnight", "PRT", 380.0, False) +
    sh("The next morning, Commodore", "M19", 64.0),
    # ── 10. The blackest hellhole
    # 43
    sh("The message survives", "PRT", 420.0) + card("The message survives", LDOC("FROM THE FILE · COMMANDER TASK GROUP 30.6", "Radio to the Third Fleet, 30 August 1945",
        [("rgm_hellhole", "There has never been a blacker hellhole than the P O W hospital we are now evacuating")], RGM + ", p. 100")),
    # 44
    sh("Simpson went on", "PRT", 440.0, False) + sh("Then came the line", "PRT", 103.0, False) + sh("The cheers of", "SM", 955.0),
    # 45
    sh("The Navy photographed", "PRT", 20.0) + sh("Another shows a man", "PRT", 360.0, False),
    # 46
    sh("Two days later", "SHG", 156.0) + card("Two days later", PROTEST),
    # 47
    sh("If you want more", "SM", 992.0) + card("If you want more", SUB) + sh("And now, back to", "ATS", 284.0),
    # ── 11. The Bataan lands
    # 48
    sh("On the thirtieth of August", "WMN", 9.0) + card("On the thirtieth of August", SLUG("30 August 1945", "Atsugi airfield")) +
    sh("They brought the paratroopers", "WMN", 27.0) + sh("By nightfall", "ATC", 17.0) + sh("General Robert", "UNL", 398.0) +
    sh("he was supposed to land", "UNL", 509.0, False),
    # 49
    sh("About two in the afternoon", "ATS", 284.0) + sh("wrote down its name", "SM", 318.0) + sh("had ordered that there be", "UNL", 471.0),
    # 50
    sh("came out with his corncob", "SM", 330.0) + sh("and walked over", "UNL", 538.0) + sh("recorded what he told them", "ATS", 307.0, False) + card("recorded what he told them", PAYOFF),
    # 51
    sh("There is a famous story", "UNL", 528.0, False) + sh("The story appears", "SM", 330.0) + sh("What the records", "UNL", 509.0, False) +
    sh("Then he got into a car", "ATS", 353.0),
    # ── 12. Backs to the road
    # 52
    sh("The road from", "R_ROAD", 0.0) + sh("staff wrote that it was lined", "ATS", 353.0) + card("wrote that it was lined", LDOC("FROM THE FILE · MACARTHUR'S STAFF HISTORY", "The road to Yokohama, 30 August 1945",
        [("rgm_road", "They stood at attention but faced away from the road")], RGM + ", p. 30")),
    # 53
    sh("It was a security measure", "R_ROAD", 4.0, False) + sh("In Japan, guards", "R_ROAD", 1.0, False) + sh("riding in the convoy", "ATS", 360.0),
    # 54
    sh("The convoy was not", "ATS", 353.0, False) + sh("The Navy's historian notes", "ATS", 365.0, False) + sh("wrote that it took them", "R_ROAD", 2.0) +
    sh("He also wrote", "ASH", 441.0),
    # 55
    sh("That night", "ATC", 51.0) + sh("Hamburgers and grapes", "UNL", 398.0) + sh("Five hundred paratroopers", "UNL", 360.0) + sh("And the next evening", "WMN", 300.0),
    # ── 13. Out of Manchuria
    # 56
    sh("Lieutenant General Jonathan", "WMN", 280.0, False) + sh("For more than three years", "PYK", 6.0) + sh("With him at the end", "WMN", 300.0),
    # 57
    sh("wrote that in the middle", "WMN", 276.0, False) + card("wrote that in the middle", WAINMAP),
    # 58
    sh("he landed in Manila", "WMN", 418.0, False) + sh("An Associated Press", "WMN", 276.0, False) + sh("said three words", "WMN", 312.0, False),
    # 59
    sh("The next afternoon he landed", "ATS", 444.0) + sh("He wrote that this came", "PYK", 305.0) + sh("That evening at the New", "WMN", 290.0) +
    sh("Their reunion", "PYK", 328.0) + sh("That night, in Tokyo", "ASH", 380.0),
    # ── 14. Nobody volunteers
    # 60
    sh("was blunt about it", "M13", 103.0) + sh("The prime minister, Prince", "ASH", 319.0) + sh("In the end the task", "UNS", 129.0),
    # 61
    sh("had lost a leg", "M18", 402.0) + sh("The army had to send", "UNS", 301.0) + sh("a man who had opposed", "M13", 121.0),
    # 62
    sh("recorded what happened", "M19", 160.0) + sh("went white with anger", "M13", 121.0, False) + sh("It took the Emperor's", "ASH", 330.0),
    # 63
    sh("Nine aides went with them", "M18", 418.0) + sh("The trip was kept secret", "ASH", 441.0),
    # ── 15. Without flag or sword
    # 64
    sh("They left Tokyo", "SM", 56.0) + card("They left Tokyo", SLUG("2 September 1945 · 5 a.m.", "Tokyo to Yokohama")) +
    sh("The road to", "ASH", 472.0) + sh("On the cars", "ATS", 353.0) + sh("the officers left their swords", "UNS", 129.0) + card("he clearly never forgot", NOFLAG),
    # 65
    sh("At the quay four", "A63", 540.0) + sh("The Japanese were taken aboard", "R_ARR", 3.0) + sh("The ride out", "A98", 8.0),
    # 66
    sh("On the battleship", "M18", 42.0) + sh("Sailors had rehearsed", "M18", 111.0, False) + sh("And in a frame", "A63", 180.0) +
    sh("A Navy courier", "A63", 180.0) + sh("It was too fragile", "A98", 32.0) + sh("so it had been backed", "A63", 178.5, False),
    # 67
    sh("On the deck that morning", "M18", 247.0) + sh("The NBC radio announcer", "A98", 236.0) + sh("A Navy torpedo pilot", "A98", 222.0, False) +
    sh("And, just behind the place", "R_DP", 0.0) + sh("the Japanese came up the ladder", "M13", 103.0) + sh("began to count", "M13", 9.0, False),
    # ── 16. The speech nobody expected
    # 68
    sh("At two minutes past nine", "NVB", 563.0) + card("At two minutes past nine", CLOCK) +
    sh("was surprised by that", "UNS", 180.0) + sh("Halsey, standing nearby", "UNS", 215.0),
    # 69
    sh("This is his voice", "UNS", 245.0, False),
    # 70 CLIP Navy bulletin 567.6
    sh("We are gathered here", "NVB", 567.6),
    # 71 CLIP United News 179.7
    sh("The issues, involving", "UNS", 179.7),
    # 72
    sh("Then he said something", "M19", 220.0) + card("Nor is it for us", MALICE),
    # 73
    sh("It is my earnest hope", "UNS", 230.0) + card("a world dedicated to", HOPE),
    # 74
    sh("listened, and he understood", "M19", 280.0) + sh("could exact his pound", "UNS", 260.0) + card("And yet he pleaded", SURPRISE),
    # 75
    sh("Then MacArthur turned", "UNS", 163.0),
    # 76 CLIP Navy bulletin 616.6
    sh("I now invite", "NVB", 616.6),
    # 77
    sh("The crowded deck went silent", "M19", 300.0),
    # ── 17. Two prisoners at the table
    # 78
    sh("walked to the table first", "NVB", 651.0) + sh("He took off his silk", "UNS", 284.0) + sh("He seemed not to know", "A63", 204.0) +
    sh("MacArthur turned and told", "NVB", 669.0) + sh("Then he paused", "UNS", 290.0) + sh("It was four minutes past nine", "M13", 177.0),
    # 79
    sh("came next", "UNS", 301.0) + sh("He did not sit down", "UNS", 318.0, False) + sh("The radio announcer said", "M13", 234.0),
    # 80
    sh("Then MacArthur stepped", "NVB", 704.0) + sh("The radio recording", "R_DS", 0.0) + sh("said the Supreme Commander would", "NVB", 704.0) + sh("Then he said: Will General", "R_DS", 0.5, False),
    # 81
    sh("these two men had surrendered", "UNS", 335.0) + sh("Now they stood at", "UNS", 340.0, False) + sh("He used several pens", "M13", 290.0) +
    sh("Halfway through", "UNS", 352.0),
    # 82
    sh("The rest of the signing", "M06", 32.0) + sh("then China, Britain", "M06", 54.0, False) + sh("The Canadian, Colonel", "A98", 365.0) +
    sh("signed the Japanese copy", "M06", 130.0) + sh("The New Zealander", "UNS", 438.0),
    # ── 18. These proceedings are closed
    # 83
    sh("At twenty-two minutes past", "UNS", 456.0) + sh("went back to the microphones", "M06", 421.0),
    # 84 CLIP United News 471.9
    sh("Let us pray that peace", "UNS", 471.9),
    # 85
    sh("wrote that MacArthur faced", "M06", 266.0),
    # 86
    sh("As he said it", "R_FLY", 0.0) + sh("The NBC announcer described", "SM", 18.0) + sh("Then came the sound", "UNS", 490.0) + sh("The Navy's figure is", "R_FLY", 3.0, False) +
    sh("flying over the Missouri", "M06", 616.0) + sh("A few minutes later", "R_FLY", 7.0, False),
    # 87
    sh("Before they left", "A63", 276.0) + sh("would not accept a document", "A63", 324.0, False) + sh("General Sutherland sat down", "A63", 348.0, False) +
    sh("Only then did the Japanese", "A63", 444.0, False),
    # 88
    sh("At nine twenty-nine", "M19", 345.0) + sh("No one saluted them", "M10", 400.0) + sh("After the cease-fire", "A63", 540.0),
    # 89
    sh("On the way back", "A63", 612.0) + sh("heard MacArthur on the radio", "M19", 100.0) + card("Today the guns", GUNS) + sh("And in that gun room", "M19", 27.0),
    # ── 19. The question
    # 90
    sh("What he was writing", "ASH", 319.0) + sh("never published the report", "ASH", 350.0),
    # 91
    sh("He had described the speech", "UNS", 245.0) + card("Would it have been", QUESTION),
    # 92
    sh("came back from the palace", "ASH", 330.0) + sh("We know this only", "ASH", 502.0),
    # 93
    sh("ended that chapter", "M10", 314.0) + card("We were defeated", NOBLER) + sh("He was writing in", "ASH", 441.0) + sh("Neither of them", "ASH", 106.0),
    # ── 20. What became of them
    # 94
    sh("was tried by the Tokyo", "M13", 121.0) + sh("became Japan's first ambassador", "M10", 385.0),
    # 95
    sh("Wainwright was flown home", "WMN", 296.0) + sh("He died in", "UNS", 340.0) + sh("Harold", "PRT", 214.0),
    # 96
    sh("In the three weeks", "PYK", 78.0) + card("In the three weeks", FREED) + sh("Some of them had been", "SM", 955.0),
    # 97
    sh("If your father", "PRT", 92.0) + sh("tell us his name", "PYK", 138.0),
    # 98
    sh("is a museum ship now", "A98", 21.0) + sh("Set into her deck", "A63", 540.0) + sh("on the morning a Japanese", "M18", 402.0),
]

PC = f"U.S. Navy · public domain · {WC}"
SC = f"U.S. Army Signal Corps · public domain · {WC}"
PHOTOS = [
    (1, "Photographers hang", None, "spectators_vantage.jpg", "01", "", "", f"U.S. Navy · DoD HD-SN-99-03020 · public domain", {"style": "print", "label": "Spectators and photographers on the Missouri, 2 Sept 1945"}),
    (3, "They are led to", None, "delegation_colour.jpg", "03", "", "", f"Army Signal Corps · USA C-2719 · public domain · {WC}", {"style": "print", "label": "The Japanese delegation before the table, 2 Sept 1945"}),
    (8, "The Emperor's uncle", None, "higashikuni_portrait.jpg", "08", "", "", f"National Diet Library · public domain · {WC}", {"style": "print", "label": "Prince Naruhiko Higashikuni, prime minister from 17 Aug 1945"}),
    (25, "packed in bundles", None, "drop_b29_cheer.jpg", "25", "", "", "U.S. Army Air Forces · NARA 342-FH-3A02512 · public domain", {"style": "print", "label": "Internees cheer as a B-29 drops supplies, 1945"}),
    (26, "big enough to read", None, "drop_hanawa_roofs.jpg", "26", "", "", "U.S. Army Air Forces · NARA 342-FH-3A03305 · public domain", {"style": "print", "label": "'P W' painted on the roofs of Hanawa camp, Honshu, with supply parachutes"}),
    (27, "fell straight through", None, "drop_supplies_gathered.jpg", "27", "", "", f"U.S. Army Signal Corps · NARA 6200936 · public domain", {"style": "print", "label": "Air-dropped clothing and food gathered by released prisoners, 30 Aug 1945"}),
    (34, "Admiral William Halsey", None, "halsey_portrait.jpg", "34", "", "", PC, {"style": "print", "label": "Admiral William F. Halsey, Third Fleet"}),
    (37, "Fleet Admiral Chester", None, "nimitz_portrait.jpg", "37", "", "", PC, {"style": "print", "label": "Fleet Admiral Chester W. Nimitz"}),
    (38, "Simpson's chief of staff", None, "stassen_navy.jpg", "38", "", "", PC, {"style": "print", "label": "Harold E. Stassen in Navy uniform"}),
    (40, "The Navy's photographs show", None, "pows_flags.jpg", "40", "", "", f"U.S. Navy · NARA 520992 · public domain · {WC}", {"style": "print", "label": "Prisoners wave U.S., British and Dutch flags at their rescuers, 29 Aug 1945"}),
    (41, "Among them was Major", None, "boyington_rescued.jpg", "41", "", "", f"U.S. Navy · 80-G-490443 · public domain · {WC}", {"style": "print", "label": "Maj. Gregory 'Pappy' Boyington after his rescue, 29 Aug 1945"}),
    (42, "carried aboard the", None, "benevolence_ship.jpg", "42", "", "", PC, {"style": "print", "label": "Hospital ship USS Benevolence (AH-13)"}),
    (45, "One picture shows", None, "benevolence_nurse.jpg", "45", "", "", PC, {"style": "print", "label": "Pvt. Alfred Sorenson, captured on Corregidor, aboard Benevolence, 30 Aug 1945"}),
    (45, "Another shows a man", None, "benevolence_pow_rest.jpg", "45", "", "", f"Wayne Miller, U.S. Navy · NARA 520929 · public domain", {"style": "print", "label": "A rescued prisoner aboard USS Benevolence, Aug 1945"}),
    (49, "MacArthur had ordered", None, "atsugi_mac_staff.jpg", "49", "", "", SC, {"style": "print", "label": "MacArthur and his officers at Atsugi, 30 Aug 1945"}),
    (51, "It is not in the records", None, "atsugi_mac_colour.jpg", "51", "", "", f"Army Signal Corps · USA C-1732 · public domain · {WC}", {"style": "print", "label": "MacArthur arrives at Atsugi, 30 Aug 1945"}),
    (56, "With him at the end", None, "wainwright_portrait.jpg", "56", "", "", f"U.S. Navy · 80-G-354136 · public domain", {"style": "print", "label": "Lt. Gen. Jonathan M. Wainwright, Yokohama, 1 Sept 1945"}),
    (59, "That evening at the New", None, "mac_wainwright_newgrand.jpg", "59", "", "", f"U.S. Army · 111-SC-210621 · public domain", {"style": "print", "label": "MacArthur and Wainwright, New Grand Hotel, Yokohama, 31 Aug 1945"}),
    (60, "In the end the task", None, "shigemitsu_portrait.jpg", "60", "", "", f"National Diet Library · public domain · {WC}", {"style": "print", "label": "Foreign Minister Mamoru Shigemitsu"}),
    (63, "Nine aides went", None, "delegation_arrives.jpg", "63", "", "", f"U.S. Army · NARA 531311 · public domain · {WC}", {"style": "print", "label": "The eleven on the Missouri's deck, 2 Sept 1945"}),
    (68, "Halsey, standing nearby", None, "mac_speaking_colour.jpg", "68", "", "", f"U.S. Navy · USA C-2717 · public domain · {WC}", {"style": "print", "label": "MacArthur reads his speech; Perry's flag framed behind"}),
    (78, "who checked his wristwatch", None, "shigemitsu_signs_kase.jpg", "78", "", "", f"Lt. Stephen E. Korpanty, Army Signal Corps · SC 213700 · public domain", {"style": "print", "label": "Shigemitsu signs; Kase stands behind him, 9:04 a.m."}),
    (79, "Halsey wrote that he signed", None, "umezu_signs.jpg", "79", "", "", f"U.S. Navy · 80-G-332701 · public domain · {WC}", {"style": "print", "label": "Gen. Umezu signs for Imperial General Headquarters, 9:06 a.m."}),
    (81, "The announcer said", None, "mac_signs_wp_colour.jpg", "81", "", "", f"U.S. Army · USA C-4627 · public domain · {WC}", {"style": "print", "label": "MacArthur signs; Wainwright and Percival stand behind him"}),
    (82, "who was blind in one eye", None, "cosgrave_signs.jpg", "82", "", "", f"U.S. Army · public domain · {WC}", {"style": "print", "label": "Col. Lawrence Moore Cosgrave signs for Canada"}),
    (86, "mast high", None, "flyover_missouri.jpg", "86", "", "", f"U.S. Navy · NARA 520775 · public domain · {WC}", {"style": "print", "label": "Corsairs and Hellcats over the Missouri, 2 Sept 1945"}),
    (87, "crossed out the country", None, "sutherland_corrects.jpg", "87", "", "", f"U.S. Army · SC 212246 · public domain · {WC}", {"style": "print", "label": "Sutherland corrects the Japanese copy of the Instrument of Surrender"}),
    (88, "they were piped over the side", None, "delegation_honours.jpg", "88", "", "", f"U.S. Navy · 80-G-472629 · public domain · {WC}", {"style": "print", "label": "The delegation leaves the Missouri, 9:29 a.m."}),
    (90, "took it straight to", None, "envoys_leave.jpg", "90", "", "", f"U.S. Navy · NARA 520922 · public domain · {WC}", {"style": "print", "label": "The envoys leave the Missouri after signing"}),
    (92, "We know this only", None, "hirohito_macarthur.jpg", "92", "", "", f"Gaetano Faillace, U.S. Army · public domain · {WC}", {"style": "print", "label": "The Emperor and MacArthur, 27 Sept 1945 (three weeks later)"}),
    (94, "was sentenced to seven years", None, "shigemitsu_portrait.jpg", "94", "", "", f"National Diet Library · public domain · {WC}", {"style": "print", "label": "Mamoru Shigemitsu"}),
    (95, "Wainwright was flown home", None, "wainwright_portrait.jpg", "95", "", "", "Jerome Zerbe, U.S. Navy · 80-G-354136 · public domain", {"style": "print", "label": "Lt. Gen. Jonathan M. Wainwright, Yokohama, 1 Sept 1945"}),
    (98, "The Missouri is a museum", None, "missouri_anchored.jpg", "98", "", "", f"U.S. Navy · 80-G-490436 · public domain · {WC}", {"style": "print", "label": "USS Missouri at anchor in Tokyo Bay, 30 Aug 1945"}),
    (98, "Set into her deck", None, "instrument_p2.jpg", "98", "", "", f"National Archives · public domain · {WC}", {"style": "print", "label": "The Instrument of Surrender, Tokyo Bay, 2 Sept 1945"}),
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
