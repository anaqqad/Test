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
    "PO": ("palawan_operation_1945", 1), "NJ": ("newsreel_jan_1945", 1), "CAB": ("cabanatuan_newsreel_1945", 1),
    "BC": ("black_cats_pby", 1), "YT": ("yokohama_trials_1948", 1), "RP": ("rescued_pows_leyte_1945", 1),
    "CB": ("cebu_prisoners_1945", 1), "JH": ("jungle_health_1944", 1), "SURF": ("beach_activities_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


REP = "War Crimes Branch report, 18 Aug 1945 · IMTFE Pros. Doc. 2869 · National Diet Library"
BOG = "Sworn statement of Sgt. Douglas W. Bogue, USMC, 17 Feb 1945 · IMTFE Pros. Doc. 8259"
BAR = "Sworn statement of Fern J. Barta, USN, 1945 · IMTFE Pros. Doc. 8260"
SMI = "Statement of Rufus W. Smith, sworn 20 Sep 1946 · IMTFE Pros. Doc. 8350"
MOO = "Stephen L. Moore, As Good as Dead (2016)"
SC = "U.S. Army Signal Corps · National Archives, 111-SCA album 2985 · public domain"
WC = "Wikimedia Commons"
CAMP_TAG = "The prison camp at Puerto Princesa, March 1945 · U.S. Army Signal Corps film"
SHELTER_TAG = "One of the camp's air raid shelters, March 1945 · U.S. Army Signal Corps film"
BAY_TAG = "Puerto Princesa Bay, February 1945 · U.S. Army Signal Corps film"
PAL_TAG = "Palawan, March 1945 · U.S. Army Signal Corps film"
GUER_TAG = "Palawan guerrillas with U.S. officers, March 1945 · U.S. Army Signal Corps film"
NJ_TAG = "American bombers over Puerto Princesa · United News newsreel, January 1945"
SHIP_TAG = "Stand-in · an American landing ship at sea · United News newsreel, January 1945"
CAB_TAG = "Prisoners freed at Cabanatuan · Universal Newsreel, February 1945"
SEA_TAG = "Stand-in · the sea at night · from Story of the Black Cats (U.S. Navy, 1945)"
WAVE_TAG = "Stand-in · open water · from Story of the Black Cats (U.S. Navy, 1945)"
SWIM_TAG = "Stand-in · a swimmer · from Story of the Black Cats (U.S. Navy, 1945)"
PBY_TAG = "A Catalina flying boat · from Story of the Black Cats (U.S. Navy, 1945)"
YT_TAG = "Stand-in · a U.S. war crimes court at Yokohama, March 1948 (another case) · U.S. Army film"
RP_TAG = "Stand-in · American prisoners freed from Japanese camps, Leyte, 1945 · U.S. Army film"
CB_TAG = "Stand-in · American prisoners of the Japanese, freed on Cebu, 1945 · U.S. Army film"
SURF_TAG = "Stand-in · surf on a Pacific beach, 1945 · U.S. Navy film"
DUSK_TAG = "Stand-in · the sea at dusk · from Story of the Black Cats (U.S. Navy, 1945)"
JH_TAG = "Stand-in · jungle and mangrove · from Personal Health in the Jungle (War Dept., 1944)"
P = [
    # 0 the alarm
    [("Two", "NJ", T(5, 30.5)), ("@", "An air raid alarm", NJ_TAG),
     ("#", "Two o'clock", None, {"type": "Slug", "title": "December 14, 1944 · 2 p.m.", "subtitle": "Prison camp 10-A · Puerto Princesa, Palawan, Philippines"}),
     ("An air raid alarm", "NJ", T(5, 33.0)), ("over a prison camp", "PO", T(0, 39.5)), ("@", "over a prison camp", CAMP_TAG),
     ("The guards shout", "NJ", T(6, 0.5)), ("And for the first time", "PO", T(1, 14.0)), ("@", "And for the first time", SHELTER_TAG)],
    # 1 hope
    [("The men in the trenches", "PO", T(1, 33.0)),
     ("#", "Sergeant Douglas", None, {"type": "LedgerDocument", "file": "FILE 01 — THE ALARM", "head": "Sgt. Douglas Bogue, sworn statement", "source": BOG,
        "spans": [{"doc": "doc_bogue", "say": "they thought it might be the real thing"}]}),
     ("Then through the narrow", "PO", T(1, 21.5)), ("They carried machine guns", "PO", T(1, 47.0)),
     ("Some of them carried buckets", "PO", T(0, 50.0))],
    # 2 out of 150
    [("Out of one hundred", "PO", T(0, 56.0)),
     ("#", "Out of one hundred", None, {"type": "LedgerBars", "file": "FILE 02 — THE COUNT", "head": "American prisoners at Puerto Princesa, 14 December 1944", "max": 150,
        "bars": [{"label": "In the camp that afternoon", "value": 150, "figure": "150", "note": ""},
                 {"label": "Alive at the end of the war", "value": 11, "figure": "11", "note": ""}],
        "source": f"{REP}; {BAR}"}),
     ("how eleven men got out", "PO", T(0, 26.0)), ("@", "how eleven men got out", BAY_TAG),
     ("across five miles", "BC", T(0, 42.0)), ("@", "across five miles", WAVE_TAG),
     ("helped save five hundred", "CAB", T(4, 45.5)), ("@", "helped save five hundred", CAB_TAG)],
    # 3 August 1942
    [("The story starts", "CB", T(4, 28.4)), ("@", "The story starts", "Stand-in · American prisoners on trucks, Cebu, 1945 · U.S. Army film"),
     ("#", "The story starts", None, {"type": "Slug", "title": "August 1942", "subtitle": "350 American prisoners arrive at Puerto Princesa"}),
     ("about three hundred and fifty", "CB", T(2, 28.5)), ("@", "about three hundred and fifty", CB_TAG), ("a long narrow island", "PO", T(0, 23.0)), ("@", "a long narrow island", BAY_TAG),
     ("Their job was to build", "PO", T(5, 28.5))],
    # 4 two years
    [("For two years", "JH", T(8, 34.0)), ("@", "For two years", JH_TAG), ("They lived on wormy", "CB", T(2, 31.0)),
     ("A camp cook", "RP", T(1, 30.5)), ("@", "A camp cook", RP_TAG), ("And the camp had one rule", "PO", T(2, 4.0)),
     ("#", "And the camp had one rule", None, {"type": "LedgerDocument", "file": "FILE 03 — THE RULE", "head": "U.S. Army war crimes report, 1945", "source": REP,
        "spans": [{"doc": "doc_tenrule", "say": "For every prisoner who escaped ten would be executed"}]})],
    # 5 September 1944
    [("In September", "PO", T(1, 0.5)), ("@", "In September", CAMP_TAG), ("One hundred and fifty stayed", "PO", T(0, 53.0)),
     ("Nobody knew it yet", "PO", T(0, 13.0)), ("@", "Nobody knew it yet", "Stand-in · a landing ship in Puerto Princesa Bay, 1945 · U.S. Army Signal Corps film")],
    # 6 October raids
    [("On the nineteenth", "NJ", T(5, 30.0)), ("@", "On the nineteenth", NJ_TAG),
     ("#", "On the nineteenth", None, {"type": "Slug", "title": "October 19, 1944", "subtitle": "The first American bombers over Palawan"}),
     ("then went on to bomb", "NJ", T(5, 40.0)), ("On the twenty-eighth", "NJ", T(5, 50.0)), ("The guards took it out", "PO", T(0, 42.0)),
     ("After every raid", "PO", T(0, 44.0))],
    # 7 the trenches
    [("After the raids", "PO", T(1, 15.0)), ("@", "After the raids", SHELTER_TAG), ("covered over with logs", "PO", T(1, 35.0)),
     ("The Japanese wanted one", "PO", T(1, 49.0)), ("Marine Rufus Smith", "PO", T(1, 55.0)),
     ("#", "Marine Rufus Smith", None, {"type": "LedgerDocument", "file": "FILE 04 — OVER THE FENCE", "head": "Rufus W. Smith, USMC, sworn statement", "source": SMI,
        "spans": [{"doc": "doc_smith", "say": "stood drums of gasoline"}]})],
    # 8 the warnings
    [("The guards had been saying", "PO", T(0, 48.0)),
     ("#", "The guards had been saying", None, {"type": "LedgerQuote", "file": "FILE 05 — THE WARNING", "head": "What the guards told the prisoners, 1944",
        "before": "He even went so far as to say ", "key": "if they made a landing we would never live to see the American Army.", "after": "",
        "who": "Rufus W. Smith, USMC, survivor", "source": SMI}),
     ("On the tenth of December", "NJ", T(7, 21.0)), ("@", "On the tenth of December", SHIP_TAG), ("It was heading", "NJ", T(7, 11.0)),
     ("But on Pa-lah-wan", "PO", T(1, 50.0)),
     ("#", "According to the historian", None, {"type": "LedgerQuote", "file": "FILE 06 — THE ORDER", "head": "Message from the Japanese 2nd Air Division, 13 December 1944",
        "before": "", "key": "If the POWs are harboring an enemy feeling, dispose of them at the appropriate time.", "after": "",
        "who": "Lt. Gen. Seiichi Terada's headquarters, as quoted by Stephen L. Moore", "source": f"{MOO}, p. 150"})],
    # 9 morning of the 14th
    [("At about two in the morning", "PO", T(0, 31.0)), ("@", "At about two in the morning", BAY_TAG),
     ("#", "At about two in the morning", None, {"type": "Slug", "title": "December 14, 1944", "subtitle": "2 a.m. · Japanese troops moving outside the compound"}),
     ("At dawn they went", "PO", T(0, 44.0)), ("At noon all the work", "PO", T(0, 41.0)),
     ("Fern Barta", "NJ", T(6, 1.0)),
     ("#", "Fern Barta", None, {"type": "LedgerDocument", "file": "FILE 07 — NO PLANES", "head": "Fern J. Barta, USN, sworn statement", "source": BAR,
        "spans": [{"doc": "doc_barta", "say": "he never saw a single plane"}]})],
    # 10 the attack
    [("At about two o'clock", "PO", T(1, 36.0)), ("@", "At about two o'clock", SHELTER_TAG), ("Then the soldiers came", "PO", T(0, 46.8)),
     ("#", "They went to the shelter", None, {"type": "LedgerDocument", "file": "FILE 08 — A COMPANY", "head": "U.S. Army war crimes report, 1945", "source": REP,
        "spans": [{"doc": "doc_torch", "say": "They threw a lit torch into the entrance followed by a bucket or two of gasoline"}]})],
    # 11 the fence
    [("Men ran out", "PO", T(0, 52.0)), ("@", "Men ran out", CAMP_TAG), ("Four American officers", "PO", T(1, 16.0)),
     ("In the other shelters", "PO", T(1, 34.0)), ("Bohg turned", "PO", T(1, 52.0))],
    # 12 through the wire
    [("Some men clawed", "PO", T(1, 57.0)), ("@", "Some men clawed", CAMP_TAG), ("Others dug out", "PO", T(1, 40.0)),
     ("Barta crawled", "PO", T(0, 27.0)), ("@", "Barta crawled", BAY_TAG), ("Thirty or forty men", "PO", T(0, 34.0)),
     ("For most of them", "BC", T(0, 41.5)), ("@", "For most of them", WAVE_TAG)],
    # 13 the beach
    [("The soldiers came down", "PO", T(0, 29.0)), ("@", "The soldiers came down", BAY_TAG), ("They blasted men", "PO", T(1, 48.0)), ("@", "They blasted men", CAMP_TAG),
     ("A barge moved slowly", "PO", T(0, 16.0)), ("Bohg wedged himself", "BC", T(16, 1.5)), ("@", "Bohg wedged himself", WAVE_TAG),
     ("#", "Bohg wedged himself", None, {"type": "LedgerDocument", "file": "FILE 09 — THE ROCKS", "head": "Sgt. Douglas Bogue, sworn statement", "source": BOG,
        "spans": [{"doc": "doc_bogue2", "say": "He stayed there for seven hours listening"}]})],
    # 14 Nielsen
    [("Army private Eugene", "JH", T(8, 33.5)), ("@", "Army private Eugene", JH_TAG), ("The soldiers found him", "PO", T(0, 25.5)), ("@", "The soldiers found him", BAY_TAG),
     ("He crawled into a cove", "PO", T(0, 33.0)),
     ("When the soldiers came for the rest", "BC", T(1, 14.5)), ("@", "When the soldiers came for the rest", WAVE_TAG),
     ("#", "Bullets hit him", None, {"type": "LedgerDocument", "file": "FILE 10 — NIELSEN", "head": "U.S. Army war crimes report, 1945", "source": REP,
        "spans": [{"doc": "doc_nielsen", "say": "Bullets hit him in the leg in the head and in the ribs He kept swimming"}]}),
     ("A strong current", "BC", T(0, 42.0)), ("@", "A strong current", WAVE_TAG)],
    # 15 the cliff
    [("On the cliff above", "PO", T(1, 46.0)), ("@", "On the cliff above", CAMP_TAG), ("Bal-kus hit the first one", "PO", T(1, 51.0)),
     ("#", "Bal-kus hit the first one", None, {"type": "LedgerDocument", "file": "FILE 11 — THE CORAL", "head": "U.S. Army war crimes report, 1945", "source": REP,
        "spans": [{"doc": "doc_coral", "say": "hit the first one on the head with a big piece of coral"}]}),
     ("More soldiers came", "PO", T(0, 36.0)), ("Bal-kus ran down", "BC", T(0, 47.0)), ("@", "Bal-kus ran down", WAVE_TAG)],
    # 16 subscribe
    [("If you want more", "PO", T(0, 18.0)), ("@", "If you want more", BAY_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 17 nine p.m.
    [("At about nine that night", "BC", T(13, 28.8)), ("@", "At about nine that night", DUSK_TAG), ("and found three more", "PO", T(0, 27.5)),
     ("#", "A fifth man", None, {"type": "LedgerTimeline", "file": "FILE 12 — THE SWIM", "head": "Into the bay, about 9 p.m., 14 December",
        "rows": [{"date": "SGT. DOUGLAS BOGUE", "text": "U.S. Marine Corps"}, {"date": "FERN BARTA", "text": "U.S. Navy, radioman"},
                 {"date": "EDWIN PETRY", "text": "Army Air Forces"}, {"date": "ALBERTO PACHECO", "text": "U.S. Army, New Mexico"},
                 {"date": "DONALD MARTYN", "text": "U.S. Marine Corps · never seen again"}],
        "source": f"{REP}; {BOG}"}),
     ("Behind them", "BC", T(0, 50.0)), ("@", "Behind them", WAVE_TAG)],
    # 18 halfway
    [("Halfway across", "BC", T(1, 14.5)), ("@", "Halfway across", WAVE_TAG),
     ("#", "Halfway across", None, {"type": "LedgerDocument", "file": "FILE 13 — HALFWAY", "head": "Fern J. Barta, USN, sworn statement", "source": BAR,
        "spans": [{"doc": "doc_barta2", "say": "Halfway across Barta passed out"}]}),
     ("He reached it at sunrise", "PO", T(0, 24.0)), ("@", "He reached it at sunrise", BAY_TAG),
     ("Rufus Smith crossed too", "BC", T(0, 53.0)), ("@", "Rufus Smith crossed too", WAVE_TAG), ("and that he made it", "PO", T(0, 21.0)), ("@", "and that he made it", BAY_TAG)],
    # 19 McDole
    [("Glenn Mac-Dole hid", "PO", T(0, 24.5)), ("@", "Glenn Mac-Dole hid", BAY_TAG), ("Mac-Dole stayed with him", "PO", T(0, 30.0)), ("@", "Mac-Dole stayed with him", BAY_TAG),
     ("Then Mac-Dole swam", "BC", T(0, 44.0)), ("@", "Then Mac-Dole swam", WAVE_TAG),
     ("#", "Too exhausted", None, {"type": "LedgerDocument", "file": "FILE 14 — THE FISH TRAP", "head": "U.S. Army war crimes report, 1945", "source": REP,
        "spans": [{"doc": "doc_fishtrap", "say": "he spent a whole night clinging to a fish trap in the water"}]})],
    # 20 the convicts
    [("The men who found", "PO", T(6, 20.0)), ("@", "The men who found", PAL_TAG), ("Bohg after five days", "JH", T(8, 32.5)), ("@", "Bohg after five days", JH_TAG),
     ("The prisoners of one camp", "PO", T(7, 36.0)), ("@", "The prisoners of one camp", GUER_TAG)],
    # 21 the guerrillas
    [("From there", "PO", T(9, 10.0)), ("@", "From there", GUER_TAG), ("They dressed the Americans", "PO", T(6, 54.0)),
     ("On the sixth of January", "BC", T(3, 43.0)), ("@", "On the sixth of January", PBY_TAG),
     ("#", "On the sixth of January", None, {"type": "Slug", "title": "January 6, 1945", "subtitle": "Brooke's Point · a flying boat takes out the first six survivors"}),
     ("On the twenty-first", "BC", T(2, 20.5)), ("@", "On the twenty-first", PBY_TAG)],
    # 22 the eleven
    [("Eleven men had made it", "RP", T(6, 46.3)), ("@", "Eleven men had made it", RP_TAG),
     ("#", "Eleven men had made it", None, {"type": "LedgerTimeline", "file": "FILE 15 — THE ELEVEN", "head": "The survivors of Palawan",
        "rows": [{"date": "U.S. ARMY", "text": "Willie Balchus · Elmo Deal · Ernest Koblos · Eugene Nielsen · Alberto Pacheco"},
                 {"date": "U.S. MARINES", "text": "Douglas Bogue · Glenn McDole · Rufus Smith"},
                 {"date": "ARMY AIR FORCES", "text": "Tommy Daniels · Edwin Petry"},
                 {"date": "U.S. NAVY", "text": "Fern Barta"}],
        "source": "Palawan roster (Nielsen family, from National Archives records); " + REP})],
    # 23 the seventh of January
    [("By the seventh of January", "RP", T(1, 30.5)), ("@", "By the seventh of January", RP_TAG), ("Japanese guards facing", "PO", T(0, 40.0)),
     ("And on Luzon", "CAB", T(4, 31.0)), ("@", "And on Luzon", CAB_TAG)],
    # 24 Cabanatuan
    [("On the twenty-sixth of January", "CAB", T(4, 34.5)), ("@", "On the twenty-sixth of January", CAB_TAG),
     ("Four days later", "CAB", T(4, 45.2)),
     ("#", "Four days later", None, {"type": "Slug", "title": "January 30, 1945", "subtitle": "Cabanatuan · Rangers and Filipino guerrillas free 513 prisoners"}),
     ("and carried out", "CAB", T(4, 48.8)), ("Historians link", "CAB", T(4, 52.3)), ("The records do not", "CAB", T(5, 42.7)),
     ("But by then", "CAB", T(6, 0.0))],
    # 25 the landing
    [("On the twenty-eighth of February", "PO", T(0, 12.5)), ("@", "On the twenty-eighth of February", "The landing at Puerto Princesa, February 1945 · U.S. Army Signal Corps film"),
     ("#", "On the twenty-eighth of February", None, {"type": "Slug", "title": "February 28, 1945", "subtitle": "41st Infantry Division lands at Puerto Princesa"}),
     ("In the empty prison camp", "PO", T(0, 39.0)), ("@", "In the empty prison camp", CAMP_TAG), ("In March", "PO", T(0, 38.7))],
    # 26 June
    [("In early June", "PO", T(2, 2.0)), ("@", "In early June", "Puerto Princesa, 1945 · U.S. Army Signal Corps film")],
    # 27 the trial
    [("In August", "YT", T(2, 41.5)), ("@", "In August", YT_TAG),
     ("#", "In August", None, {"type": "Slug", "title": "August 1948", "subtitle": "Yokohama · sixteen men on trial for Palawan"}),
     ("Six were acquitted", "YT", T(3, 19.5)), ("The camp commander", "PO", T(0, 44.0)),
     ("#", "The air division commander", None, {"type": "LedgerTimeline", "file": "FILE 16 — THE VERDICT", "head": "U.S. Eighth Army trial, Yokohama, 1948",
        "rows": [{"date": "16 TRIED", "text": "6 acquitted"}, {"date": "LT. GEN. SEIICHI TERADA", "text": "Life imprisonment"},
                 {"date": "M/SGT. TAICHI DEGUCHI", "text": "Death · cut to 30 years in 1950"},
                 {"date": "CAPT. NAGAYOSHI KOJIMA", "text": "\"The Weasel\" · never tried"},
                 {"date": "LT. YOSHIKAZU SATO", "text": "Led the soldiers · never tried"}],
        "source": "V. Dennis Wrynn, World War II magazine (1997); Michael S. Bell, National WWII Museum (2022)"})],
    # 28 1958
    [("On the thirty-first", "PO", T(2, 1.5)), ("@", "On the thirty-first", "Puerto Princesa, 1945 · U.S. Army Signal Corps film"),
     ("#", "On the thirty-first", None, {"type": "Slug", "title": "December 31, 1958", "subtitle": "The last men convicted for Palawan leave Sugamo prison"}),
     ("Fourteen years after", "PO", T(0, 21.0)), ("@", "Fourteen years after", BAY_TAG)],
    # 29 comments
    [("If someone in your family", "RP", T(6, 48.0)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Was your family there?", "subtitle": "A prisoner of the Japanese, or a Filipino who helped · tell us in the comments"})],
    # 30 the grave
    [("In nineteen fifty-two", "PO", T(0, 32.0)), ("@", "In nineteen fifty-two", BAY_TAG), ("One hundred and twenty-three", "PO", T(0, 48.0)),
     ("In Pwair-toh", "PO", T(1, 50.5)), ("@", "In Pwair-toh", CAMP_TAG)],
    # 31 the map
    [("And in the files", "PO", T(0, 19.0)), ("@", "And in the files", BAY_TAG), ("And underneath", "PO", T(0, 35.0))],
]

PHOTOS = [
    (3, "Their job was to build", None, "airfield_1946.jpg", "03", "The airfield the prisoners built", "Puerto Princesa airdrome from the air, surveyed by the Army in June 1946", SC, {}),
    (4, "They lived on wormy", None, "cook_shed_1945.jpg", "04", "The prisoners' cooking shed", "Puerto Princesa prison camp, March 1945", SC, {}),
    (5, "One hundred and fifty stayed", None, "barracks_interior_1945.jpg", "05", "Inside the prison barracks", "Where the last 150 prisoners slept · photographed March 1945", SC, {}),
    (9, "At noon all the work", None, "camp_side_1945.jpg", "09", "The prison compound", "Side view of the American prison building, Puerto Princesa · March 1945", SC, {}),
    (12, "Some men clawed", None, "prison_yard_1945.jpg", "12", "The prison compound", "Seen from outside, the day after the landing · 1 March 1945", SC, {}),
    (11, "In the other shelters", None, "shelter_1945.jpg", "11", "One of the shelters", "Its entrance, photographed after the landing, March 1945", SC, {}),
    (7, "Three trenches", None, "shelter_fence_1945.jpg", "07", "One of the air raid shelters", "A few steps from the fence, with the bay behind it · photographed 1945", "U.S. Army Air Forces 58405AC · National Archives 342-FH · public domain", {}),
    (11, "Bohg turned to", None, "bogue_sketch.jpg", "11", "POW Camp No. 10A, Puerto Princesa", "\"on 14 December 1944\" · sketched by Sgt. Douglas Bogue, USMC, for the war crimes prosecutors", "IMTFE Pros. Doc. 8487 · National Diet Library, Japan", {}),
    (14, "he reached the far side", None, "aerial_bay_1945.jpg", "14", "Puerto Princesa Bay", "From the air, February 1945 · Nielsen swam it with three bullet wounds", SC, {}),
    (20, "The men who found", None, "iwahig_1945.jpg", "20", "Iwahig Penal Colony", "A Philippine prison farm across the bay · its gate in June 1945", SC, {}),
    (21, "From there Filipino guerrillas", None, "guerrillas_1945.jpg", "21", "Palawan guerrillas", "With U.S. soldiers north of Puerto Princesa, March 1945", SC, {}),
    (25, "In the empty prison camp", None, "camp_front_1945.jpg", "25", "The prison camp, March 1945", "Signal Corps caption: \"where 150 Yank war prisoners were burned alive in December\"", SC, {}),
    (25, "In March", None, "graves_1945.jpg", "25", "Puerto Princesa, March 1945", "Graves of the prisoners, after a military funeral with full honors", SC, {}),
    (26, "A few days later", None, "macarthur_site_1945.jpg", "26", "MacArthur at the camp", "Puerto Princesa, 8 June 1945", SC, {}),
    (31, "the map that Sergeant", None, "bogue_sketch.jpg", "31", "POW Camp No. 10A", "\"at Puerto Princesa, Palawan Island, on 14 December 1944\" · sketch by Sgt. Douglas Bogue, USMC", "IMTFE Pros. Doc. 8487 · National Diet Library, Japan", {}),
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
