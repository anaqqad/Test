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
    "IWO": ("shores_iwo_jima_1945", 1), "IWF": ("iwo_flag_newsreel_1945", 1), "SAI": ("saipan_invasion_1944", 1),
    "SAN": ("saipan_newsreel_1944", 1), "GUA": ("guadalcanal_newsreel_1942", 1), "OKI": ("okinawa_landings_1945", 1),
    "NAV": ("navajo_canyon_1954", 1), "JAP": ("my_japan_1945", 1), "TTC": ("tale_two_cities_1946", 1),
    "REL": ("released_pows_japan_1945", 1), "YOK": ("pows_yokohama_1945", 1), "RP": ("rescued_pows_leyte_1945", 1),
    "CR": ("corregidor_newsreel_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


WC = "Wikimedia Commons"
AP95 = "Joe Kieyoomia to the Associated Press (Tim Korte), 28 Sep 1995"
MCC = "Sally McClain, Navajo Weapon (1994)"
NHHC = "Navajo Code Talkers' Dictionary, revised 15 June 1945 (U.S. Navy, NHHC)"
FACT = "Navajo Code Talkers: World War II Fact Sheet (Navy & Marine Corps, 1992)"
PRO = "Adam Jevec, Semper Fidelis, Code Talkers, Prologue (NARA), 2001"
NARA = "NARA, Access to Archival Databases: WWII Army enlistment and POW records"
NAV_TAG = "Stand-in · the Navajo country, 1954 · Navajo Canyon Country (Prelinger Archives)"
JAP_TAG = "Stand-in · Japanese soldiers · captured Japanese film in My Japan (U.S. Treasury, 1945)"
JPN_TAG = "Stand-in · Japan · captured Japanese film in My Japan (1945)"
IWO_TAG = "Iwo Jima, February 1945 · To the Shores of Iwo Jima (U.S. Navy and Marine Corps, 1945)"
GUA_TAG = "Guadalcanal, 1942 · United News newsreel"
SAI_TAG = "Saipan, June 1944 · U.S. Army Signal Corps film"
SAN_TAG = "Saipan, June 1944 · newsreel"
OKI_TAG = "Okinawa, April 1945 · newsreel"
RADIO_TAG = "Stand-in · a field radio, 1945 · newsreel"
MAR_TAG = "Stand-in · Marines, 1942 · United News newsreel"
TTC_TAG = "Hiroshima and Nagasaki after the bombs · A Tale of Two Cities (U.S. Army, 1946)"
REL_TAG = "Freed Allied prisoners, Japan, 31 August 1945 · U.S. Army film"
RELS_TAG = "Stand-in · freed prisoners, Japan, August 1945 · U.S. Army film"
YOK_TAG = "Freed prisoners, Yokohama, 20–21 September 1945 · U.S. Army Signal Corps film"
RP_TAG = "Stand-in · an American prisoner freed from a Japanese camp, 1945 · U.S. Army film"
CR42_TAG = "The surrender in the Philippines, 1942 · Japanese film in a United News newsreel"
CR_TAG = "Corregidor · United News newsreel, February 1945"
K = "Kee-oh-mee"  # spoken form of Kieyoomia (anchors use the spoken text)


def LQ(file, head, key, who, source, before="", after=""):
    return {"type": "LedgerQuote", "file": file, "head": head, "before": before, "key": key, "after": after, "who": who, "source": source}


def HL(kicker, before, accent, at, source, after=""):
    return {"type": "Headline", "kicker": kicker, "before": before, "accent": accent, "after": after, "at": at, "source": source}


def TL(file, head, rows, source):
    return {"type": "LedgerTimeline", "file": file, "head": head, "rows": [{"date": a, "text": b} for a, b in rows], "source": source}


def SLUG(title, sub):
    return {"type": "Slug", "title": title, "subtitle": sub}


P = [
    # 0 a winter day
    [("A winter day", "JAP", T(9, 45.0)), ("@", "A winter day", JAP_TAG), ("A guard opens a cell", "JAP", T(9, 22.0)),
     ("He walks him onto", "JAP", T(9, 52.0)), ("The prisoner is told", "REL", T(4, 6.0)), ("@", "The prisoner is told", RELS_TAG)],
    # 1 twenty-seven degrees (reconstruction)
    [("He later said", "JAP", T(12, 34.0)),
     ("#", "He later said", None, {"type": "Section", "world": "ground", "W": 3000, "H": 1500, "surface": 820,
        "date": "Japan · a winter day, 1943–45", "place": "Reconstruction · from Kieyoomia's 1995 account",
        "cam": [{"t": 0, "x": 1500, "y": 760, "z": 0.8}, {"t": 6, "x": 1550, "y": 760, "z": 1.0}, {"t": 30, "x": 1600, "y": 780, "z": 1.25}],
        "items": [{"kind": "hut", "x": 520, "y": 820, "w": 520, "label": "Cells", "labelAt": 0.8, "labelTo": 4},
                  {"kind": "fence", "x": 2250, "y": 820, "w": 520}, {"kind": "tower", "x": 2600, "y": 820},
                  {"kind": "man", "x": 1720, "y": 820, "flip": True, "label": "Guard", "labelAt": "The guard told him", "labelTo": "He stood there"},
                  {"kind": "man", "x": 1450, "y": 820, "label": "The prisoner", "labelAt": 1.0, "labelTo": "The guard told him"}],
        "pills": [{"t0": "twenty-seven degrees", "t1": "The guard told him", "text": "27°F"},
                  {"t0": "six inches deep", "t1": "He stood there", "text": "Six inches of snow", "y": 230}],
        "ring": {"t0": "He stood there", "t1": "When they finally", "label": "One hour in the snow"},
        "source": AP95})],
    # 2 the prisoner was Joe Kieyoomia
    [("The prisoner was", "NAV", T(11, 26.0)), ("@", "The prisoner was", NAV_TAG),
     ("#", "The prisoner was", "The code the Japanese", {"type": "ObjectTurn", "shape": "tag", "lines": ["38012443", "KIEYOOMIA JOE L"], "w": 660, "h": 360,
        "title": "Joe Kieyoomia", "caption": "His Army serial number · drafted at Santa Fe, 28 March 1941", "source": NARA}),
     ("The code the Japanese", "IWO", T(7, 36.0)), ("@", "The code the Japanese", IWO_TAG),
     ("And Joe", "OKI", T(5, 17.0)), ("@", "And Joe", RADIO_TAG)],
    # 3 this is the true story
    [("This is the true story", "IWO", T(4, 52.0)), ("@", "This is the true story", IWO_TAG), ("the Marines who carried it", "IWO", T(5, 8.5)),
     ("and the one Navajo prisoner", "REL", T(3, 55.0)), ("@", "and the one Navajo prisoner", RELS_TAG),
     ("Most of what we know", "NAV", T(11, 26.0)), ("We will tell you where", "NAV", T(1, 1.0)), ("@", "We will tell you where", NAV_TAG)],
    # 4 classrooms
    [("To understand this story", "NAV", T(3, 25.0)), ("@", "To understand this story", NAV_TAG), ("In the years before the war", "NAV", T(5, 2.0)),
     ("Chester Nez", "NAV", T(7, 27.0)), ("He remembered", "NAV", T(1, 25.0))],
    # 5 Laura Tohe
    [("The daughter of another", "NAV", T(6, 38.5)), ("@", "The daughter of another", NAV_TAG),
     ("#", "She calls what happened", None, HL("THE CONTRADICTION", "The language the schools punished", "became the code", "huge contradiction",
        "Laura Tohe to the Associated Press, Aug 2026"))],
    # 6 fifty thousand Navajo
    [("In", "NAV", T(1, 0.5)), ("@", "In", NAV_TAG), ("Their language had no written", "NAV", T(9, 30.0)), ("Outside the tribe", "NAV", T(2, 37.0)),
     ("#", "A Navy fact sheet", None, HL("WHO COULD UNDERSTAND IT, 1941", "Outside the Navajo:", "fewer than thirty", "fewer than thirty", FACT))],
    # 7 Kieyoomia's record
    [("#", f"Joe {K} grew up", None, TL("FILE 01 — ARMY RECORD", "Kieyoomia, Joe L.",
        [("Serial", "38012443"), ("Born", "1917 (Army) · 1919 (other sources)"), ("28 Mar 1941", "Drafted at Santa Fe, N.M."),
         ("Listed as", "American Indian, citizen"), ("Civilian job", "Silversmith")], NARA))],
    # 8 the 200th
    [(f"{K} was sent to fill out", "IWO", T(2, 38.0)), ("@", f"{K} was sent to fill out", "Stand-in · an anti-aircraft gun crew, 1945 · To the Shores of Iwo Jima"),
     ("At Fort Bliss", "SAI", T(0, 40.0)), ("@", "At Fort Bliss", "Stand-in · Army trucks, 1944 · U.S. Army Signal Corps film"),
     ("Almost all of its men", "SAI", T(6, 39.5)), ("@", "Almost all of its men", "Stand-in · an American soldier, Saipan 1944 · U.S. Army Signal Corps film")],
    # 9 Clark Field
    [("They landed there", "CR", T(0, 52.0)), ("@", "They landed there", CR_TAG), ("set up their guns", "GUA", T(0, 47.0)),
     ("@", "set up their guns", "Stand-in · an American airfield in the Pacific, 1942 · United News"),
     ("On the eighth of December", "IWO", T(8, 8.0)), ("@", "On the eighth of December", "Stand-in · a Japanese plane over the fleet, 1945 · To the Shores of Iwo Jima"),
     ("The New Mexico gunners", "IWO", T(2, 39.0)), ("State records", "IWO", T(2, 46.0))],
    # 10 the 515th
    [("In the weeks after", "IWO", T(2, 22.0)), ("@", "In the weeks after", "Stand-in · anti-aircraft fire, 1945 · To the Shores of Iwo Jima"),
     ("#", "By the state's count", None, {"type": "LedgerBars", "file": "FILE 02 — NEW MEXICO", "head": "The New Mexico gunners, 1941–42",
        "bars": [{"label": "Men of the 200th and 515th", "value": 1800, "figure": "1,800", "note": "after the draftees joined"},
                 {"label": "Enemy aircraft shot down", "value": 86, "figure": "86", "note": "by the state's count"}], "max": 1800,
        "source": "New Mexico Blue Book 2011–2012 (Secretary of State)"})],
    # 11 Bataan surrenders
    [("For four months", "CR", T(1, 13.0)), ("@", "For four months", CR42_TAG), ("On the ninth of April", "CR", T(1, 34.0)),
     ("#", "On the ninth of April", None, SLUG("April 9, 1942", "Bataan · the surrender")),
     ("The two hundredth Coast Artillery", "CR", T(1, 55.0)), ("@", "The two hundredth Coast Artillery", "The Japanese flag over Corregidor, 1942 · Japanese film in a United News newsreel")],
    # 12 King
    [("#", "General King", None, LQ("FILE 03 — BATAAN", "Maj. Gen. Edward P. King, 9 April 1942", "You men remember this. You did not surrender…",
        "General King to his men, as quoted", "Bataan Death March (Wikipedia, citing Knox, Death March)", after=" you had no alternative but to obey my order."))],
    # 13 the Death March
    [("What followed", "CR", T(1, 20.0)), ("@", "What followed", CR42_TAG),
     ("Estimates of the dead", "RP", T(0, 30.0)), ("@", "Estimates of the dead", RP_TAG)],
    # 14 eighteen hundred
    [(f"{K} survived the march", "RP", T(5, 30.0)), ("@", f"{K} survived the march", RP_TAG),
     ("#", "Of the eighteen hundred", None, {"type": "IconCount", "icon": "man", "total": 1800, "label": "New Mexicans sent to the Philippines",
        "accent": "New Mexicans", "highlight": {"n": 900, "label": "Came home alive", "accent": "alive", "at": "about half would never"},
        "file": "FILE 02 — NEW MEXICO", "source": "New Mexico Blue Book 2011–2012"})],
    # 15 Johnston reads the newspaper
    [("#", "Seven thousand miles away", None, SLUG("Los Angeles · early 1942", "Philip Johnston reads the newspaper")),
     ("Seven thousand miles away", "OKI", T(5, 2.0)), ("The story said", "OKI", T(5, 17.0)), ("@", "The story said", RADIO_TAG)],
    # 16 a missionary's son
    [("Johnston was the son", "NAV", T(5, 50.0)), ("@", "Johnston was the son", NAV_TAG), ("As a boy of about nine", "NAV", T(7, 27.0)),
     ("He had served in France", "NAV", T(10, 16.0)), ("And he knew", "NAV", T(2, 37.0))],
    # 17 Camp Elliott
    [("He took his idea", "GUA", T(1, 32.0)), ("@", "He took his idea", "Stand-in · Marine officers, 1942 · United News newsreel"),
     ("On the twenty-eighth of February", "GUA", T(1, 47.0)), ("he brought four Navajo men", "GUA", T(2, 2.0)),
     ("#", "On the twenty-eighth of February", None, SLUG("February 28, 1942", "Camp Elliott · the demonstration"))],
    # 18 the test message
    [("#", "Vogel's staff", "In a later test", LQ("FILE 04 — THE TEST", "Camp Elliott, 28 February 1942", "Enemy tank dive bomber expected to attack this morning.",
        "Gen. Vogel's test message, in and out of Navajo", PRO, before="Sent: Enemy expected to make tank and dive bomber attack at dawn. — Received: ")),
     ("#", "In a later test", None, {"type": "LedgerBars", "file": "FILE 04 — THE TEST", "head": "A three-line message",
        "bars": [{"label": "Coding machine", "value": 1800, "figure": "30 MIN", "note": "machines of the time"},
                 {"label": "Navajo talkers", "value": 20, "figure": "20 SEC", "note": "encode, send, decode"}], "max": 1800, "source": FACT})],
    # 19 Vogel's letter
    [("#", "On the sixth of March", None, {"type": "LedgerDocument", "file": "FILE 05 — THE LETTER", "head": "Gen. Vogel to the Commandant, 6 March 1942",
        "spans": [{"doc": "doc_vogel", "say": "This dialect is thus equivalent to a secret code to the enemy"}],
        "source": "Vogel to Commandant, 6 Mar 1942 · NARA RG 127 · Wikimedia Commons"}),
     ("Vogel asked for", "GUA", T(2, 43.7)), ("@", "Vogel asked for", MAR_TAG)],
    # 20 the bus
    [("On the morning of the fourth", "NAV", T(7, 50.0)), ("@", "On the morning of the fourth", NAV_TAG),
     ("#", "At Fort Wingate", None, SLUG("May 4, 1942", "Fort Wingate, New Mexico")), ("One had dropped out", "NAV", T(8, 15.0))],
    # 21 the 29 (photo)
    [("The youngest", "NAV", T(8, 15.0))],
    # 22 Chester Nez
    [("#", "Nez's story was typical", None, TL("FILE 06 — ONE OF THE 29", "Chester Nez",
        [("1921", "Born at Chi Chil Tah, N.M."), ("Age 3", "His mother dies"), ("Age 8", "Boarding school · named after Chester Arthur"),
         ("1942", "Recruited at Tuba City school"), ("2014", "Dies at 93, the last of the 29")],
        "Chester Nez (Wikipedia, citing Nez and Avila, Code Talker, 2011)"))],
    # 23 look at the dates
    [("#", "Look at the dates", None, TL("FILE 07 — THE SAME WEEK", "May 1942",
        [("4 May", "29 Navajos sworn into the Marines"), ("6 May", "Corregidor surrenders"), ("7 May", "Kieyoomia's capture date on his POW card")],
        "NARA POW data file (RG 389); Code talker (Wikipedia)"))],
    # 24 the job
    [("The platoon graduated", "GUA", T(2, 1.0)), ("@", "The platoon graduated", MAR_TAG),
     ("#", "invent a code", None, HL("CAMP ELLIOTT, 1942", "A code in a language", "never written down", "never been written down", PRO))],
    # 25 what they knew
    [("They started with", "NAV", T(6, 14.0)), ("@", "They started with", NAV_TAG), ("The first code", "NAV", T(9, 27.5)),
     ("Instead of inventing", "NAV", T(6, 2.0))],
    # 26 animals
    [("#", "A tank became", None, {"type": "CodeWord", "file": "FILE 08 — THE CODE", "head": "From home to the battlefield",
        "rows": [{"word": "chay-da-gahi", "lit": "tortoise", "mil": "Tank", "at": "A tank became"},
                 {"word": "besh-lo", "lit": "iron fish", "mil": "Submarine", "at": "A submarine was"},
                 {"word": "gini", "lit": "chicken hawk", "mil": "Dive bomber", "at": "A dive bomber was"},
                 {"word": "da-he-tih-hi", "lit": "hummingbird", "mil": "Fighter plane", "at": "A fighter plane was"},
                 {"word": "lo-tso", "lit": "whale", "mil": "Battleship", "at": "A battleship was"},
                 {"word": "ca-lo", "lit": "shark", "mil": "Destroyer", "at": "A destroyer was"}], "source": NHHC})],
    # 27 countries
    [("#", "Countries got names too", None, {"type": "CodeWord", "file": "FILE 08 — THE CODE", "head": "Countries",
        "rows": [{"word": "toh-ta", "lit": "between waters", "mil": "Britain", "at": "Britain was"},
                 {"word": "ke-yah-da-na-lhe", "lit": "floating island", "mil": "Philippines", "at": "The Philippines were"},
                 {"word": "besh-be-cha-he", "lit": "iron hat", "mil": "Germany", "at": "Germany was"},
                 {"word": "ne-he-mah", "lit": "our mother", "mil": "America", "at": "And America"}], "source": NHHC})],
    # 28 spelling
    [("#", "For words that had no code term", None, {"type": "CodeWord", "file": "FILE 08 — THE CODE", "head": "Spelling", "colHeads": ["Navajo", "Literally", "Letter"],
        "rows": [{"word": "wol-la-chee", "lit": "ant", "mil": "A", "at": "wol-lah-chee"}, {"word": "be-la-sana", "lit": "apple", "mil": "A", "at": "beh-lah-sahnah"},
                 {"word": "tse-nill", "lit": "axe", "mil": "A", "at": "tseh-nill"},
                 {"word": "tsah · wol-la-chee · ah-keh-di-glini · tsah-ah-dzoh", "lit": "needle, ant, victor, yucca", "mil": "NAVY", "at": "The word Navy"}], "source": FACT})],
    # 29 double lock
    [("#", "That was the double lock", None, HL("THE DOUBLE LOCK", "Even to a Navajo,", "words with no meaning", "with no meaning",
        "Lin Poyer, War at the Margins (2022); Ed Gilbert, Native American Code Talker (2008)")),
     ("Remember that", "JAP", T(9, 54.0)), ("@", "Remember that", JAP_TAG)],
    # 30 the code grew
    [("The code grew", "IWO", T(7, 38.3)), ("@", "The code grew", "Stand-in · a Marine command post, Iwo Jima 1945 · To the Shores of Iwo Jima"),
     ("The code talkers learned it", "OKI", T(5, 17.0)), ("@", "The code talkers learned it", OKI_TAG), ("A Navy dictionary", "OKI", T(5, 2.0))],
    # 31 Hawaii, Gorman
    [("The spelling alphabet grew", "SAN", T(0, 5.0)), ("@", "The spelling alphabet grew", SAN_TAG),
     ("#", "One of the original twenty-nine", None, LQ("FILE 09 — VOICES", "Carl Gorman, one of the original 29", "Everybody was shooting at each other,",
        "Carl Gorman", "Ron McCoy, The American West, Nov/Dec 1981", before="You had to be able to use English and Navajo pretty fast. ",
        after=" and you really had to be on the ball."))],
    # 32 the later test
    [("In one later test", "IWO", T(7, 40.0)), ("@", "In one later test", "Stand-in · Marines at a command post, 1945 · To the Shores of Iwo Jima"),
     ("Without the code", "OKI", T(5, 22.0))],
    # 33 Guadalcanal
    [("In August", "GUA", T(0, 47.0)), ("@", "In August", GUA_TAG), ("#", "In August", None, SLUG("Guadalcanal · 1942", "The first code talkers go to war")),
     ("The first Navajo code talkers", "GUA", T(2, 43.7))],
    # 34 not every officer trusted them
    [("Not every officer", "GUA", T(1, 32.5)), ("@", "Not every officer", GUA_TAG), ("The Marines' own director", "GUA", T(2, 0.5)),
     ("In the field", "GUA", T(2, 15.0)), ("the code talkers had to prove", "GUA", T(2, 30.0))],
    # 35 mistaken for Japanese (photo Bake and Kirk)
    [("They had another problem", "GUA", T(2, 44.0)), ("@", "They had another problem", GUA_TAG), ("Code talker Bill Toledo", "GUA", T(2, 58.0))],
    # 36 the darker story
    [("There is a darker story", "IWO", T(6, 15.0)), ("@", "There is a darker story", IWO_TAG),
     ("#", "Toledo said he was told so", None, TL("FILE 10 — THE KILL ORDER", "Documented or not?",
        [("Bill Toledo", "Says he was told so"), ("Congress, 2000", "Repeats it in the law"), ("Bodyguard", "No direct order was ever given"),
         ("Marine Corps", "Has always denied it"), ("Records", "No written order ever found")], "CBS News, 29 May 2002; Public Law 106-554 (2000)"))],
    # 37 Johnston enlists
    [("Meanwhile", "GUA", T(1, 50.0)), ("@", "Meanwhile", MAR_TAG),
     ("#", "In June", None, {"type": "LedgerClipping", "file": "FILE 11 — THE LEAK", "head": "June 1943", "kicker": "ARIZONA HIGHWAYS · JUNE 1943",
        "headline": "Navajos Serve as Marine Radiomen", "dateline": "A government official's article reveals the program",
        "body": "Philip Johnston is reprimanded and threatened with a court-martial. The secret holds.",
        "source": "Ron McCoy, The American West, Nov/Dec 1981 (headline paraphrased)"})],
    # 38 the school
    [("A Navajo communication school", "OKI", T(5, 17.0)), ("@", "A Navajo communication school", RADIO_TAG),
     ("a year to the day", "OKI", T(5, 2.5)), ("The Marines asked for", "GUA", T(2, 1.0)), ("@", "The Marines asked for", MAR_TAG)],
    # 39 Camp O'Donnell
    [("Back in the Philippines", "RP", T(0, 30.0)), ("@", "Back in the Philippines", RP_TAG),
     ("#", "In", None, LQ("FILE 12 — THE PRISONER", "Joe Kieyoomia, 1995", "rice laced with weevils", "Kieyoomia's account (AP paraphrase)", AP95,
        before="He said he lived on ", after=", and watched weakened Americans ordered to dig their graves, then shot."))],
    # 40 put on a ship
    [("He said that at the end", "RP", T(6, 41.0)), ("@", "He said that at the end", RP_TAG),
     ("A few days later", "IWO", T(1, 30.0)), ("@", "A few days later", "Stand-in · ships at sea, 1945 · To the Shores of Iwo Jima"),
     ("No record we have found", "IWO", T(1, 48.0))],
    # 41 the wrong face
    [("Why him", "JAP", T(9, 52.0)), ("@", "Why him", JAP_TAG),
     ("#", "In his words", None, LQ("FILE 12 — THE PRISONER", "Joe Kieyoomia, 1995", "I told them I was Navajo. They didn't believe me.",
        "Joe Kieyoomia", AP95, after=" … I guess they didn't know about Indians."))],
    # 42 things got worse
    [("In time", "JAP", T(9, 25.0)), ("He said that was when", "JAP", T(4, 2.0))],
    # 43 radio monitors
    [("By then", "IWO", T(7, 38.3)), ("@", "By then", "Stand-in · Marines with radios and headsets, Iwo Jima 1945 · To the Shores of Iwo Jima"),
     ("Marines were talking", "OKI", T(5, 22.0)), ("@", "Marines were talking", OKI_TAG),
     ("A", "JAP", T(2, 56.0)), ("@", "A", JPN_TAG)],
    # 44 the recordings
    [("In Japan they had", "JAP", T(2, 56.0)), ("@", "In Japan they had", JPN_TAG),
     ("#", "He said he could not believe", None, LQ("FILE 12 — THE PRISONER", "Kieyoomia on the broadcasts", "It sounded like Navajo…", "Joe Kieyoomia",
        "Samuel Holiday and Robert McPherson, Under the Eagle (2013), citing Doris Duke oral history #664",
        before="When they first made me listen to the broadcasts, I couldn't believe what I was hearing. "))],
    # 45 random jumble
    [("It was Navajo", "IWO", T(7, 42.0)),
     ("#", "He heard words he knew", None, {"type": "CodeWord", "file": "FILE 13 — WHAT HE HEARD", "head": "What a Navajo heard",
        "colHeads": ["He heard", "It means", "It meant"],
        "rows": [{"word": "tsah", "lit": "needle", "mil": "N"}, {"word": "wol-la-chee", "lit": "ant", "mil": "A"},
                 {"word": "ah-keh-di-glini", "lit": "victor", "mil": "V"}, {"word": "tsah-ah-dzoh", "lit": "yucca", "mil": "Y"}], "source": FACT})],
    # 46 bird, turtle, water
    [("In the", "JAP", T(4, 2.0)), ("@", "In the", JPN_TAG),
     ("#", "So he told them", None, HL("JOE KIEYOOMIA, 1995", "This means bird, this means turtle,", "this means water", "this means water", AP95))],
    # 47 the truth
    [("He told them the truth", "JAP", T(9, 23.0)), ("@", "He told them the truth", JAP_TAG), ("They did not believe", "JAP", T(9, 52.0))],
    # 48 broken ribs
    [("What followed", "JAP", T(12, 35.0)), ("@", "What followed", JPN_TAG),
     ("#", "an interrogator hit him", None, LQ("FILE 12 — THE PRISONER", "Kieyoomia to Sally McClain", "hit me with a club, broke my ribs and then my wrist.",
        "Joe Kieyoomia", MCC, before="He "))],
    # 49 the parade ground (quote)
    [("Then came the winter day", "JAP", T(12, 36.0)),
     ("#", "When he was finally moved", None, LQ("FILE 12 — THE PRISONER", "Joe Kieyoomia, 1995", "I left my soles on that parade ground.",
        "Joe Kieyoomia · his widow later: He left his soles overseas.", AP95))],
    # 50 I wanted to die
    [("He said the beatings", "RP", T(1, 5.0)), ("@", "He said the beatings", RP_TAG), ("He said he tried", "RP", T(3, 15.0)),
     ("I wanted to die", "RP", T(5, 26.0))],
    # 51 hope
    [("There is one more detail", "IWO", T(4, 18.0)), ("@", "There is one more detail", "Stand-in · the American fleet, 1945 · To the Shores of Iwo Jima"),
     ("He could hear", "IWO", T(4, 52.0))],
    # 52 subscribe
    [("We are about halfway", "IWO", T(1, 32.0)), ("@", "We are about halfway", IWO_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 53 Saipan (photo)
    [("In June", "SAN", T(0, 38.0)), ("@", "In June", SAN_TAG), ("A Marine Corps photograph", "SAN", T(0, 49.0))],
    # 54 every division
    [("By then there were code talkers", "SAI", T(4, 54.0)), ("@", "By then there were code talkers", SAI_TAG),
     ("A Navy history says", "SAN", T(1, 21.5)), ("@", "A Navy history says", SAN_TAG), ("At Bougainville", "SAI", T(5, 39.0))],
    # 55 friendly fire
    [("Being mistaken", "IWO", T(6, 15.0)), ("@", "Being mistaken", IWO_TAG), ("A", "IWO", T(6, 31.5)), ("To the men on the other end", "IWO", T(9, 3.0))],
    # 56 Iwo Jima
    [("On the nineteenth of February", "IWO", T(4, 35.0)), ("@", "On the nineteenth of February", IWO_TAG),
     ("#", "On the nineteenth of February", None, SLUG("February 19, 1945", "Iwo Jima")), ("Major Howard Connor", "IWO", T(5, 25.0))],
    # 57 800 messages
    [("According to Connor", "IWO", T(7, 38.3)), ("@", "According to Connor", "Marines at a command post, Iwo Jima 1945 · To the Shores of Iwo Jima"),
     ("#", "They sent and received", None, HL("IWO JIMA · THE FIRST TWO DAYS", "Six code talkers.", "800 messages", "more than eight hundred", FACT, after="No errors."))],
    # 58 Connor's verdict
    [("#", "Connor's verdict", None, LQ("FILE 14 — IWO JIMA", "Maj. Howard Connor, 5th Marine Division",
        "Were it not for the Navajos, the Marines would never have taken Iwo Jima.", "Signal officer, 5th Marine Division", FACT)),
     ("A captain's report", "IWO", T(10, 7.0)), ("@", "A captain's report", IWO_TAG)],
    # 59 400 code talkers, 13 killed
    [("By the end of the war", "IWO", T(16, 57.0)), ("@", "By the end of the war", IWO_TAG),
     ("#", "By the end of the war", None, {"type": "IconCount", "icon": "man", "total": 400, "label": "Navajo code talkers",
        "accent": "code talkers", "highlight": {"n": 13, "label": "Killed in action", "accent": "killed", "at": "Thirteen were killed"},
        "file": "FILE 14 — THE COST", "source": "Remarks by President George W. Bush, 26 July 2001"})],
    # 60 other tribes
    [("They were not the only", "IWO", T(4, 35.0)), ("@", "They were not the only", IWO_TAG), ("One history puts", "SAI", T(8, 10.0)),
     ("@", "One history puts", SAI_TAG), ("Choctaw", "IWO", T(9, 35.0)), ("But the Navajo code", "IWO", T(13, 40.0))],
    # 61 Arisue
    [("And Japan never broke", "IWO", T(11, 23.6)), ("@", "And Japan never broke", IWO_TAG),
     ("#", "After the war", None, HL("GEN. SEIZO ARISUE, JAPANESE ARMY INTELLIGENCE (PARAPHRASED)", "Army codes: read.", "Marine code: never cracked", "never cracked", FACT))],
    # 62 Nagasaki
    [("The ninth of August", "TTC", T(9, 32.0)), ("@", "The ninth of August", TTC_TAG),
     ("#", "The ninth of August", None, SLUG("August 9, 1945", "Nagasaki")), (f"Where was Joe {K}", "TTC", T(10, 12.0))],
    # 63 three versions
    [("Here the accounts split", "TTC", T(10, 52.0)), ("@", "Here the accounts split", TTC_TAG),
     ("#", "In his", None, TL("FILE 15 — WHERE WAS HE?", "9 August 1945: three versions",
        [("AP, 1995", "In a concrete cell in Nagasaki"), ("McClain, 1994", "Moved 60 miles south the day before"), ("Army card", "Liberated · Tokyo-area camp code")],
        "AP 28 Sep 1995; McClain, Navajo Weapon (1994); NARA RG 389"))],
    # 64 McClain version
    [("But in an earlier interview", "TTC", T(2, 10.5)), ("@", "But in an earlier interview", TTC_TAG), ("He said he had been moved", "TTC", T(11, 12.0))],
    # 65 Tokyo-area
    [("The American records", "REL", T(5, 4.0)), ("@", "The American records", REL_TAG), ("That may only be where", "REL", T(2, 5.5))],
    # 66 he lived through the war
    [("So we cannot tell you", "TTC", T(1, 50.0)), ("@", "So we cannot tell you", TTC_TAG),
     ("What we can tell you", "REL", T(0, 30.0)), ("@", "What we can tell you", REL_TAG), ("By the calendar", "REL", T(4, 5.0))],
    # 67 Yokohama
    [("All across Japan", "YOK", T(2, 37.0)), ("@", "All across Japan", YOK_TAG), ("In Yokohama", "YOK", T(0, 18.0)),
     ("thin grinning men", "YOK", T(1, 34.0)), ("eating smoking", "YOK", T(1, 59.0)), ("climbing into the planes", "YOK", T(5, 50.0))],
    # 68 four years in hospitals
    [("According to the book", "YOK", T(4, 55.0)), ("@", "According to the book", YOK_TAG), ("His leg recovered", "NAV", T(4, 37.7)),
     ("@", "His leg recovered", NAV_TAG), ("He went back to the reservation", "NAV", T(4, 13.6))],
    # 69 buses without parades
    [("The code talkers came home too", "IWO", T(18, 13.8)), ("@", "The code talkers came home too", IWO_TAG),
     ("#", "Bill Toledo said", None, LQ("FILE 16 — THE SECRET", "Bill Toledo, code talker", "keep my mouth shut", "Bill Toledo", "CBS News, 29 May 2002",
        before="They just told me to ", after=" about what I did."))],
    # 70 nine hundred came back
    [("Of the New Mexico gunners", "REL", T(4, 54.0)), ("@", "Of the New Mexico gunners", RELS_TAG), ("A state history says", "REL", T(5, 30.0))],
    # 71 declassified
    [("#", "The Navajo code stayed classified", None, TL("FILE 16 — THE SECRET", "After the war",
        [("1945–68", "The code stays classified"), ("1968", "Declassified"), ("1971", "Nixon's letter of thanks"), ("14 Aug 1982", "National Navajo Code Talkers Day")],
        "Prologue (NARA) 2001; AP 14 Aug 2026; Proclamation 4954 (1982)"))],
    # 72 Reagan
    [("Reagan's proclamation", "NAV", T(0, 55.0)), ("@", "Reagan's proclamation", NAV_TAG),
     ("#", "It called theirs", None, HL("PROCLAMATION 4954 · 1982", "The only foolproof,", "unbreakable code", "unbreakable code",
        "Ronald Reagan, Proclamation 4954, 28 July 1982", after="in the history of warfare")),
     ("In nineteen seventy-six", "NAV", T(2, 12.8))],
    # 73 the unnamed prisoner
    [(f"{K} said he only learned", "NAV", T(11, 28.2)), ("@", f"{K} said he only learned", NAV_TAG),
     ("#", "But what he said fits", None, LQ("FILE 17 — AFTER THE WAR", "A Navajo prisoner from Bataan, to a code talker",
        "I never figured out what you guys who got me into all that trouble were saying.", "Unnamed in the sources; almost certainly Kieyoomia",
        "Ron McCoy, The American West, 1981; Navy and Marine Corps fact sheet, 1992"))],
    # 74 I salute the code talkers
    [("He never blamed them", "NAV", T(4, 13.6)), ("@", "He never blamed them", NAV_TAG),
     ("#", "he told the reporter", None, LQ("FILE 17 — AFTER THE WAR", "Joe Kieyoomia, 1995", "And even if I knew about their code, I wouldn't tell the Japanese.",
        "Joe Kieyoomia", AP95, before="I salute the Code Talkers. "))],
    # 75 silversmith
    [("For the rest of his life", "NAV", T(6, 38.5)), ("@", "For the rest of his life", NAV_TAG), ("In nineteen eighty-three", "NAV", T(4, 30.0)),
     ("He was listed for years", "NAV", T(7, 2.6))],
    # 76 Lita
    [("He was married", "NAV", T(5, 1.9)), ("@", "He was married", NAV_TAG), ("He belonged to", "NAV", T(7, 26.7))],
    # 77 death
    [("#", f"Joe {K} died", None, TL("FILE 18 — JOE LEE KIEYOOMIA", "Silversmith · veteran",
        [("1941", "Drafted at Santa Fe"), ("1942–45", "Prisoner of the Japanese"), ("Married", "42 years to Lita · 8 children"),
         ("17 Feb 1997", "Dies at Shiprock · buried at Farmington")],
        "Farmington Daily News, 20–21 Feb 1997, via Bataan-Corregidor Memorial Foundation of New Mexico"))],
    # 78 he left his soles overseas
    [("In", "NAV", T(11, 28.2)), ("@", "In", NAV_TAG),
     ("#", "Lita", None, HL("LITA KIEYOOMIA, BATAAN MEMORIAL, 7 APRIL 2002", "He left his", "soles overseas", "He left his soles",
        "Bataan-Corregidor Memorial Foundation of New Mexico"))],
    # 79 the law
    [("In December", "IWO", T(10, 7.6)), ("@", "In December", IWO_TAG),
     ("#", "The original twenty-nine would receive", None, {"type": "LedgerClipping", "file": "FILE 19 — THE MEDALS", "head": "Public Law 106-554",
        "kicker": "SEC. 1101 · HONORING THE NAVAJO CODE TALKERS", "headline": "A gold medal for each of the original 29", "dateline": "Approved 21 December 2000",
        "body": "A silver medal to each person who qualified as a Navajo Code Talker.", "source": "Public Law 106-554, 114 Stat. 2763A-311"})],
    # 80 the Rotunda (photo)
    [("On the twenty-sixth of July", "IWO", T(18, 44.0)), ("@", "On the twenty-sixth of July", IWO_TAG)],
    # 81 our mother
    [("#", "The President told the room", None, LQ("FILE 19 — THE MEDALS", "President George W. Bush, 26 July 2001",
        "At home, they carried for decades the secret of their own heroism.", "Capitol Rotunda", "Remarks by the President, 26 July 2001 (White House archive)"))],
    # 82 Maybe Japan is listening
    [("#", "When John Brown spoke", None, HL("JOHN BROWN JR., ONE OF THE 29 · 2001", "", "Maybe Japan is listening", "Maybe Japan is listening", PRO))],
    # 83 Chester Nez
    [("Chester Nez", "NAV", T(11, 28.2)), ("@", "Chester Nez", NAV_TAG),
     ("#", "The Japanese pulled out", None, LQ("FILE 20 — THE LAST WORD", "Chester Nez, 2002", "but they never could break it.", "Chester Nez", "CBS News, 29 May 2002",
        before="The Japanese pull up all their hair and they got baldy, "))],
    # 84 two left (photo Begay)
    [("As of August", "NAV", T(1, 0.4)), ("@", "As of August", NAV_TAG)],
    # 85 2025 / museum
    [("Their story is still", "NAV", T(8, 15.0)), ("@", "Their story is still", NAV_TAG), ("In August", "NAV", T(9, 51.6))],
    # 86 comments
    [("If someone in your family", "YOK", T(0, 18.9)), ("@", "If someone in your family", YOK_TAG), ("We read every one", "YOK", T(4, 55.4))],
    # 87 Shiprock (photo)
    [("On the high desert", "NAV", T(1, 0.4)), ("@", "On the high desert", NAV_TAG)],
    # 88 the end
    [("The language spoken", "NAV", T(11, 28.2)), ("@", "The language spoken", NAV_TAG), ("In the war", "IWO", T(4, 52.0)),
     ("@", "In the war", IWO_TAG), ("And of all the people", "JAP", T(12, 34.0)), ("who knew every word", "NAV", T(1, 25.0)), ("@", "who knew every word", NAV_TAG)],
]

PHOTOS = [
    (13, f"{K} survived", None, "death_march_hands_tied.jpg", "13", "Bataan, April 1942", "Prisoners on the march from Bataan to the prison camp", f"NARA 127-N-114541 · public domain · {WC}", {"style": "print", "label": "On the march from Bataan, April 1942"}),
    (13, "Around seventy-five thousand", None, "litters_1942.jpg", "13", "The Death March", "Prisoners carry comrades on improvised litters", f"NARA 535564 · captured Japanese photo · public domain · {WC}", {"style": "print", "label": "Prisoners carrying comrades, April 1942"}),
    (20, "they were sworn", None, "first29_1942.jpg", "20", "Fort Wingate", "", f"NARA 295175 · public domain · {WC}", {"style": "print", "label": "The first 29 · Fort Wingate, 1942"}),
    (21, "The youngest", None, "first29_1942.jpg", "21", "Fort Wingate, May 1942", "The first 29 Navajo Marine recruits are sworn in", f"NARA 295175 · public domain · {WC}", {"focus": [0.6, 0.5]}),
    (35, "After that", None, "blake_kirk_1943.jpg", "35", "Bougainville, December 1943", "", f"U.S. Marine Corps · public domain · {WC}", {"style": "print", "label": "Navajo Marines with a radio, 1943"}),
    (53, "and its caption says", None, "saipan_navajo_1944.jpg", "53", "Saipan, June 1944", "Navajo communication men with the Marines, landed with the first assault waves", f"NARA 532526 · public domain · {WC}", {"focus": [0.5, 0.45]}),
    (54, "the radio traffic", None, "saipan_codetalkers_small.jpg", "54", "Saipan, 1944", "", f"public domain · {WC}", {"style": "print", "label": "Navajo code talkers, Saipan 1944"}),
    (58, "A captain's report", None, "iwo_first_flag.jpg", "58", "Iwo Jima", "", f"SSgt. Louis R. Lowery, USMC · public domain · {WC}", {"style": "print", "label": "Mount Suribachi, 23 February 1945"}),
    (62, "An American bomber", None, "nagasaki_cloud.jpg", "62", "Nagasaki", "", f"Charles Levy, U.S. Army Air Forces · public domain · {WC}", {"style": "print", "label": "Nagasaki, 9 August 1945"}),
    (63, "He said the concrete walls", None, "nagasaki_temple_1945.jpg", "63", "Nagasaki", "", f"Cpl. Lynn P. Walker Jr., USMC · public domain · {WC}", {"style": "print", "label": "Nagasaki, 24 September 1945"}),
    (64, "about sixty miles south", None, "nagasaki_before_after.jpg", "64", "Nagasaki", "", f"public domain · {WC}", {"style": "print", "label": "Nagasaki before and after"}),
    (66, "His card says", None, "nagasaki_pows_1945.jpg", "66", "Nagasaki", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Freed prisoners, Fukuoka 2-B, Nagasaki Bay, Sept 1945"}),
    (80, "By then only five", None, "medal_2001.jpg", "80", "Capitol Rotunda, 26 July 2001", "President George W. Bush salutes the Navajo Code Talkers", f"White House Photo Office · public domain · {WC}", {"focus": [0.6, 0.4]}),
    (83, "died in", None, "nez_funeral_2014.jpg", "83", "", "", f"U.S. Marine Corps · public domain · {WC}", {"style": "print", "label": "Chester Nez at Quantico, April 2014"}),
    (84, "Thomas Begay", None, "thomas_begay.jpg", "84", "Thomas Begay", "", f"U.S. Department of Veterans Affairs · public domain · {WC}", {"style": "print", "label": "Thomas Begay, code talker"}),
    (87, "In English it is called", None, "shiprock.jpg", "87", "Shiprock", "", f"Christian David · CC BY-SA 4.0 · {WC}", {"style": "print", "label": "Shiprock, New Mexico"}),
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

    SCENES = {"Section", "Chart", "IconCount", "ObjectTurn", "CodeWord"}
    SYNCED = SCENES | {"Headline"}  # time fields may be spoken phrases (scenes.tsx, cards.tsx)
    TIMEKEYS = {"t", "t0", "t1", "at", "labelAt", "labelTo", "beamAt"}

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
