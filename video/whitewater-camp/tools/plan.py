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
    "STS": ("stump_to_ship_1930", 1), "WFW": ("wood_for_war_1942", 1), "ADC": ("prisoners_shipped_adc140", 1),
    "CP": ("controlling_german_pows_1944", 1), "TT": ("troop_train_1943", 1), "SC": ("scout_canoes_1937", 1),
    "LS": ("little_smokey_bear", 1), "CML": ("children_must_learn_1940", 1), "WID": ("women_in_defense_1941", 1),
    "PAL": ("power_and_the_land_1940", 1), "WWD": ("when_work_is_done_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

MH = "Bill Waiser, “Riding Mountain POWs: The Teacher's Tale,” Manitoba History 61 (2009)"
OH = "Michael O'Hagan, “Prisoners in the Park,” NiCHE (2013)"
SCOT = "“Camp that held Rommel's men surrenders its secrets,” The Scotsman, Aug. 25, 2011"
CANOE = "Ned Morgan, “Captive Canoemaker,” Canoeroots (2012)"
GAM = "Donna Gamache, Manitoba Co-operator (2010); " + OH
WPW = "Wikipedia, “Whitewater (POW camp)”"
STS_TAG = "Stand-in · winter logging, Maine · from From Stump to Ship (1930)"
CML_TAG = "Stand-in · from The Children Must Learn (1940)"
ADC_TAG = "German prisoners from North Africa board ships · U.S. Army film, c. 1943"
CP_TAG = "Stand-in · from Controlling German Prisoners of War (U.S. Army, 1944)"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
WFW_TAG = "Stand-in · from Wood for War (U.S. Forest Service, 1942)"
SC_TAG = "Stand-in · canoes, 1937 · Ford Motor Co. film, National Archives"
LS_TAG = "Stand-in · a black bear cub · from Little Smokey (U.S. Forest Service)"
WID_TAG = "Stand-in · from Women in Defense (1941)"
PAL_TAG = "Stand-in · from Power and the Land (1940)"
WWD_TAG = "Stand-in · a wartime dance · from When Work Is Done (1943)"
P = [
    # 0 the knock
    [("On", "STS", T(3, 58.3)), ("@", "On a Saturday night", STS_TAG),
     ("#", "On a Saturday night", None, {"type": "Slug", "title": "February 1944", "subtitle": "Manitoba, western Canada · a Saturday night"}),
     ("in a farmhouse", "CML", T(7, 54.3)), ("At about half past ten", "CML", T(2, 14.7)), ("@", "At about half past ten", CML_TAG)],
    # 1 two young men
    [("Two young men", "STS", T(5, 17.0)), ("@", "Two young men", STS_TAG), ("They wore blue denim", "CML", T(8, 17.7)),
     ("#", "They wore blue denim", "They said their names", {"type": "LedgerTimeline", "file": "FILE 01 — THE UNIFORM", "head": "What a prisoner wore at Whitewater",
        "rows": [{"date": "JACKET", "text": "Blue denim, a large red circle on the back"},
                 {"date": "SHIRT", "text": "Blue denim, the same red circle"},
                 {"date": "TROUSERS", "text": "Blue denim, a red stripe down the outer leg"}],
        "source": MH}),
     ("They said their names", "CML", T(2, 3.0)), ("@", "They said their names", CML_TAG)],
    # 2 the puzzle
    [("She let them in", "PAL", T(4, 30.2)), ("@", "She let them in", PAL_TAG), ("They sat at the table", "PAL", T(18, 16.5)), ("Less than an hour later", "CML", T(7, 42.6))],
    # 3 this is the documented story
    [("This is the documented story", "STS", T(4, 4.8)), ("of the men who walked out", "STS", T(5, 17.0)), ("@", "of the men who walked out", STS_TAG),
     ("and of the teacher", "CML", T(8, 29.4)), ("@", "and of the teacher", CML_TAG)],
    # 4 Rommel's men
    [("Most of the prisoners", "ADC", T(1, 40.0)), ("Britain had no room", "ADC", T(5, 13.9)), ("@", "Britain had no room", ADC_TAG), ("Ships carried them", "ADC", T(5, 41.6)),
     ("and trains took them", "TT", T(7, 41.9)), ("@", "and trains took them", TT_TAG)],
    # 5 sixteen thousand
    [("By the end of", "CP", T(12, 37.2)), ("@", "By the end of", CP_TAG),
     ("#", "Canada held more", None, {"type": "LedgerTimeline", "file": "FILE 02 — PRISONERS IN CANADA", "head": "German prisoners of war held in Canada",
        "rows": [{"date": "END OF 1942", "text": "More than 16,000, most at Lethbridge and Medicine Hat"},
                 {"date": "BY 1945", "text": "34,000, at more than two dozen sites"}],
        "source": MH})],
    # 6 Medicine Hat
    [("Medicine Hat was crowded", "CP", T(12, 15.1)), ("@", "Medicine Hat was crowded", CP_TAG), ("In nineteen forty-three", "CP", T(11, 42.0)),
     ("Whitewater would be", "WFW", T(0, 41.6)), ("@", "Whitewater would be", WFW_TAG)],
    # 7 the shortage
    [("In the winter of", "STS", T(4, 31.1)), ("@", "In the winter of", STS_TAG), ("Almost half the homes", "CML", T(1, 16.1)), ("@", "Almost half the homes", CML_TAG),
     ("In May", "WFW", T(0, 35.2)), ("@", "In May", WFW_TAG),
     ("#", "In May", None, {"type": "Slug", "title": "May 1943", "subtitle": "Ottawa approves prisoner of war labour in the forests and on farms"})],
    # 8 Riding Mountain
    [("The government chose", "WFW", T(0, 9.6)), ("@", "The government chose", WFW_TAG), ("Old fires had left", "WFW", T(4, 51.5)),
     ("The camp went up", "WFW", T(3, 15.4))],
    # 9 the camp
    [("It was a well built camp", "WFW", T(3, 21.8)), ("@", "It was a well built camp", WFW_TAG), ("There were about fifteen", "STS", T(4, 4.8)),
     ("#", "There were about fifteen", "It cost about", {"type": "LedgerTimeline", "file": "FILE 03 — THE CAMP", "head": "The Whitewater camp, 1943",
        "rows": [{"date": "ABOUT 15", "text": "Buildings in all"},
                 {"date": "6", "text": "Large bunkhouses, each with washroom and showers"},
                 {"date": "ALSO", "text": "Kitchen and dining hall, small hospital, barns, machine shop"},
                 {"date": "POWER", "text": "Its own power plant, electricity, running water"}],
        "source": GAM}),
     ("It cost about", "WFW", T(0, 54.5))],
    # 10 no fence
    [("It did not have a fence", "WFW", T(0, 41.6)), ("@", "It did not have a fence", WFW_TAG),
     ("#", "The boundary was", "Beyond the trees", {"type": "LedgerQuote", "file": "FILE 04 — THE BOUNDARY", "head": "No fence, no compound, no guard tower",
        "before": "", "key": "blazes on a ring of outlying trees", "after": "",
        "who": "Bill Waiser, historian", "source": MH}),
     ("Some called it", "STS", T(5, 3.9)), ("@", "Some called it", STS_TAG)],
    # 11 arrival
    [("On October", "TT", T(6, 47.6)), ("@", "On October", TT_TAG),
     ("#", "On October", None, {"type": "Slug", "title": "October 26, 1943", "subtitle": "440 prisoners arrive at Whitewater from Medicine Hat"}),
     ("According to the archaeologist", "CP", T(11, 42.0)),
     ("#", "According to the archaeologist", None, {"type": "LedgerQuote", "file": "FILE 05 — VOLUNTEERS", "head": "Why they came",
        "before": "They volunteered to come here on the understanding that ", "key": "they would agree to work hard once they arrived", "after": ".",
        "who": "Adrian Myers, archaeologist of the Whitewater camp", "source": SCOT})],
    # 12 the work
    [("The work was cutting firewood", "STS", T(2, 0.2)), ("@", "The work was cutting firewood", STS_TAG), ("eight hours a day", "STS", T(2, 6.7)),
     ("#", "The men worked in gangs", None, {"type": "LedgerTimeline", "file": "FILE 06 — THE WORK", "head": "Each man, each day",
        "rows": [{"date": "8 HOURS", "text": "A day, six days a week, in gangs"},
                 {"date": "¾ CORD", "text": "Of firewood cut and stacked"},
                 {"date": "50¢", "text": "The day's pay"}],
        "source": OH + "; " + WPW}),
     ("The pay was", "STS", T(4, 37.7))],
    # 13 nineteen missing
    [("Five days after", "STS", T(5, 10.5)), ("@", "Five days after", STS_TAG),
     ("#", "Five days after", None, {"type": "Slug", "title": "Five days later", "subtitle": "Nineteen prisoners are found missing"})],
    # 14 the forest
    [("The planners had counted", "WFW", T(4, 13.1)), ("@", "The planners had counted", WFW_TAG), ("Many years later", "STS", T(5, 30.2)),
     ("#", "Escape, he said", None, {"type": "LedgerQuote", "file": "FILE 07 — THE FOREST", "head": "A former prisoner, decades later",
        "before": "", "key": "Escape was impossible. So we made the best of it.", "after": "",
        "who": "Klaus Meyer, prisoner at Whitewater", "source": SCOT})],
    # 15 trust
    [("The guards were men", "CP", T(1, 22.9)), ("@", "The guards were men", CP_TAG), ("The camp trusted", "STS", T(2, 39.5)), ("@", "The camp trusted", STS_TAG),
     ("and some of them rode", "STS", T(4, 24.5))],
    # 16 Eaton's
    [("The prisoners spent their wages", "CML", T(3, 13.2)), ("@", "The prisoners spent their wages", CML_TAG),
     ("#", "Once, they threatened", "They also ordered", {"type": "LedgerQuote", "file": "FILE 08 — THE STRIKE", "head": "Why the prisoners threatened to strike",
        "before": "", "key": "pyjamas they'd ordered from the Eaton's catalogue failed to arrive on time", "after": "",
        "who": "Whitewater camp history", "source": WPW}),
     ("They also ordered watches", "STS", T(5, 3.9)), ("In the forest", "WFW", T(0, 16.0)), ("@", "In the forest", WFW_TAG)],
    # 17 night trips
    [("South of the park", "CML", T(1, 27.8)), ("@", "South of the park", CML_TAG), ("At night, prisoners", "STS", T(5, 17.0)), ("@", "At night, prisoners", STS_TAG),
     ("and were met by farmers", "STS", T(3, 51.7))],
    # 18 dances
    [("They went to the dances", "WWD", T(8, 6.4)), ("@", "They went to the dances", WWD_TAG), ("They brought sugar", "CML", T(7, 7.5)), ("@", "They brought sugar", CML_TAG),
     ("Some farmers gave them", "CML", T(2, 26.4)), ("Before the morning roll call", "STS", T(1, 33.9)), ("@", "Before the morning roll call", STS_TAG)],
    # 19 the excuse
    [("If they were caught", "STS", T(1, 40.5)), ("@", "If they were caught", STS_TAG),
     ("#", "They had gone for a hike", "And the Mounted Police", {"type": "LedgerQuote", "file": "FILE 09 — THE EXCUSE", "head": "The excuse, when caught",
        "before": "", "key": "simply gone for a hike and become lost", "after": "",
        "who": "The standard explanation, as told by historian Bill Waiser", "source": MH}),
     ("And the Mounted Police", "CML", T(7, 54.3)), ("@", "And the Mounted Police", CML_TAG)],
    # 20 the teacher
    [("Catherine", "CML", T(8, 29.4)), ("@", "Catherine", CML_TAG), ("and was sent to teach", "CML", T(9, 4.6))],
    # 21 lonely
    [("She boarded with", "CML", T(3, 24.9)), ("@", "She boarded with", CML_TAG), ("She was lonely", "CML", T(8, 6.0)),
     ("Early in nineteen forty-four", "WWD", T(8, 12.5)), ("@", "Early in nineteen forty-four", WWD_TAG), ("That was where", "STS", T(4, 4.8))],
    # 22 the night
    [("On February nineteenth", "CML", T(7, 54.3)), ("@", "On February nineteenth", CML_TAG),
     ("#", "On February nineteenth", None, {"type": "Slug", "title": "February 19, 1944", "subtitle": "The Chrun farm, near Seech, Manitoba"}),
     ("Catherine stayed home", "PAL", T(20, 23.7)), ("@", "Catherine stayed home", PAL_TAG), ("It was snowing hard", "CML", T(1, 51.3)), ("At about half past ten", "CML", T(2, 14.7))],
    # 23 the patrol
    [("That same night", "STS", T(4, 4.8)), ("@", "That same night", STS_TAG), ("Less than an hour after", "CML", T(7, 42.6)), ("@", "Less than an hour after", CML_TAG),
     ("Catherine was in tears", "CML", T(3, 24.9))],
    # 24 the wedding
    [("Mann went on", "WWD", T(7, 38.6)), ("@", "Mann went on", WWD_TAG), ("There was shouting", "WWD", T(8, 18.6)),
     ("#", "Mann went on", None, {"type": "LedgerTimeline", "file": "FILE 10 — ONE NIGHT", "head": "Saturday, February 19, 1944",
        "rows": [{"date": "10:30 P.M.", "text": "Willi and Reinhard knock at the Chrun farmhouse"},
                 {"date": "< 1 HOUR", "text": "Lt. Mann's patrol walks in and takes them away"},
                 {"date": "LATER", "text": "Shouting and pushing at the wedding dance in Seech"},
                 {"date": "BY MORNING", "text": "Seven Germans rounded up, back in camp"}],
        "source": MH}),
     ("By the next morning", "STS", T(1, 33.9)), ("@", "By the next morning", STS_TAG)],
    # 25 the report
    [("Mann wrote a report", "CML", T(9, 16.3)), ("@", "Mann wrote a report", CML_TAG),
     ("#", "Mann wrote a report", "He sent word", {"type": "LedgerQuote", "file": "FILE 11 — THE REPORT", "head": "Lt. Mann, Veterans Guard of Canada",
        "before": "The prisoners' visit had evidently been pre-arranged. … the teacher, ", "key": "admitted having previously met them at a dance", "after": "",
        "who": "From the guard officer's report on the raid, as quoted by Bill Waiser", "source": MH}),
     ("He sent word", "TT", T(1, 43.3)), ("@", "He sent word", TT_TAG)],
    # 26 the apology
    [("About two weeks later", "CML", T(8, 6.0)), ("@", "About two weeks later", CML_TAG),
     ("#", "They brought a ship", "Outside a window", {"type": "LedgerTimeline", "file": "FILE 12 — THE APOLOGY", "head": "Two weeks after the raid, at night",
        "rows": [{"date": "A GIFT", "text": "A ship in a bottle"},
                 {"date": "A GIFT", "text": "A handmade wooden box, full of chocolate bars"},
                 {"date": "THE NEWS", "text": "Someone on the road had told the guards"}],
        "source": MH}),
     ("Outside a window", "CML", T(7, 54.3))],
    # 27 the clock
    [("She never saw", "CML", T(9, 28.0)), ("@", "She never saw", CML_TAG), ("In April", "CML", T(8, 29.4)), ("noticed that the classroom clock", "CML", T(8, 41.1)),
     ("Another sat on the school steps", "CML", T(7, 42.6))],
    # 28 the end of school
    [("At the end of the school year", "CML", T(8, 17.7)), ("@", "At the end of the school year", CML_TAG),
     ("That summer she went", "WID", T(6, 41.1)), ("@", "That summer she went", WID_TAG), ("and worked on an assembly line", "WID", T(8, 15.4)),
     ("The record does not show", "CML", T(9, 16.3))],
    # 29 the canoes
    [("Back at Whitewater", "SC", T(1, 54.2)), ("@", "Back at Whitewater", SC_TAG), ("With saws", "STS", T(4, 11.4)), ("@", "With saws", STS_TAG),
     ("One account says", "SC", T(3, 13.6)), ("@", "One account says", SC_TAG)],
    # 30 the lake
    [("The guards let them paddle", "SC", T(1, 24.4)), ("@", "The guards let them paddle", SC_TAG), ("One prisoner", "SC", T(3, 23.6)),
     ("#", "The lake, he wrote", None, {"type": "LedgerQuote", "file": "FILE 13 — THE LAKE", "head": "Out of the reeds, onto the lake",
        "before": "", "key": "The lake was ours.", "after": "", "who": "Unteroffizier Konstantin Schwartz, diary", "source": CANOE})],
    # 31 banned
    [("Then prisoners at other camps", "SC", T(1, 44.3)), ("@", "Then prisoners at other camps", SC_TAG), ("At Whitewater", "SC", T(3, 3.7))],
    # 32 the bear
    [("There was a choir", "CP", T(9, 29.3)), ("@", "There was a choir", CP_TAG), ("The camp had a mascot", "LS", T(1, 26.2)), ("@", "The camp had a mascot", LS_TAG),
     ("which raided the kitchen", "LS", T(1, 41.8)), ("and spent the winter", "LS", T(6, 39.5))],
    # 33 not every day
    [("Not every day was easy", "STS", T(2, 13.3)), ("@", "Not every day was easy", STS_TAG), ("The others went", "STS", T(1, 40.5)),
     ("And not every prisoner", "CP", T(7, 38.8)), ("@", "And not every prisoner", CP_TAG)],
    # 34 the end
    [("In the middle of", "STS", T(4, 50.8)), ("@", "In the middle of", STS_TAG),
     ("#", "In the middle of", None, {"type": "LedgerTimeline", "file": "FILE 14 — THE END OF THE CAMP", "head": "Whitewater, 1943-1946",
        "rows": [{"date": "OCT. 1943", "text": "440 prisoners arrive"},
                 {"date": "MID-1944", "text": "Cut to about 200 men"},
                 {"date": "MAR. 31, 1945", "text": "Woodcutting ends"},
                 {"date": "SUMMER 1945", "text": "Last men loaned to local farmers"},
                 {"date": "SEPT. 1945", "text": "The camp closes"}],
        "source": OH}),
     ("That summer", "PAL", T(11, 23.3)), ("@", "That summer", PAL_TAG), ("In September", "PAL", T(16, 41.2))],
    # 35 erased
    [("The buildings were advertised", "WFW", T(3, 15.4)), ("@", "The buildings were advertised", WFW_TAG), ("By the spring", "WFW", T(0, 41.6)),
     ("The Parks Bureau", "WFW", T(0, 16.0))],
    # 36 Klaus Meyer
    [("Klaus Meyer went home", "TT", T(10, 25.0)), ("@", "Klaus Meyer went home", TT_TAG),
     ("#", "They were not die-hard", None, {"type": "LedgerQuote", "file": "FILE 15 — WHO THEY WERE", "head": "Klaus Meyer, near Cologne, 2011",
        "before": "We weren't die-hard Nazis; ", "key": "we were young soldiers who got caught and wanted to go home", "after": " when the war was finished.",
        "who": "Former prisoner at Whitewater", "source": SCOT})],
    # 37 Catherine Dobrowski
    [("Catherine", "CML", T(7, 54.3)), ("@", "Catherine", CML_TAG), ("Decades later", "CML", T(11, 36.8)),
     ("#", "In 2009", None, {"type": "LedgerQuote", "file": "FILE 16 — THE TEACHER'S TALE", "head": "The last line of Waiser's article",
        "before": "", "key": "The dances at Seech were never quite the same again.", "after": "",
        "who": "Bill Waiser, historian", "source": MH})],
    # 38 the dig
    [("Between 2009 and 2011", "WFW", T(0, 41.6)), ("@", "Between 2009 and 2011", WFW_TAG),
     ("#", "They found Red Cross", "Two of the canoes", {"type": "LedgerTimeline", "file": "FILE 17 — FOUND AT WHITEWATER", "head": "The dig, 2009-2011",
        "rows": [{"date": "FOUND", "text": "Red Cross tins, buttons, letters, photographs"},
                 {"date": "FOUND", "text": "Graves of small dogs kept as pets"},
                 {"date": "FOUND", "text": "Many grooming and hygiene items"},
                 {"date": "FOUND", "text": "Six dugout canoes"}],
        "source": SCOT + "; " + CANOE}),
     ("Two of the canoes", "SC", T(3, 33.5)), ("@", "Two of the canoes", SC_TAG)],
    # 39 comment ask
    [("If your family", "CML", T(1, 16.1)),
     ("#", "If your family", None, {"type": "Slug", "title": "Riding Mountain, 1943-45, in your family's story?", "subtitle": "Tell us in the comments"})],
    # 40 echo
    [("Today there is", "WFW", T(0, 22.4)), ("In the grass", "WFW", T(4, 13.1)), ("And along the old creek", "SC", T(1, 54.2)), ("@", "And along the old creek", SC_TAG),
     ("at a camp where the only wall", "WFW", T(0, 41.6))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (3, "This is the documented story", None, "whitewater_camp_1944.jpg", "01", "Whitewater Lake, 1944", "The prisoner of war camp in Riding Mountain National Park. No fence.", f"Photographer unknown · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "Most of the prisoners", None, "alamein_prisoners_1942.jpg", "02", "El Alamein, Egypt", "German prisoners wait for transport, October 25, 1942", f"No. 1 Army Film & Photographic Unit · public domain · {WC}", {"crop": [0.0, 0.12, 1.0, 0.8]}),
    (4, "Ships carried them", None, "pows_debarking_1942.jpg", "03", "Newport News, Virginia", "Prisoners captured in Libya, on their way to a camp in Canada, Sept. 16, 1942 (insignia blurred)", f"U.S. National Archives · public domain · {WC}", {"crop": [0.0, 0.18, 1.0, 0.82]}),
    (6, "Medicine Hat was crowded", None, "medicine_hat_hockey.jpg", "05", "Camp 132, Medicine Hat", "The prisoners' hockey team. Behind them, the camp's guard towers.", f"Canada, Dept. of National Defence · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (8, "The government chose", None, "rmnp_moon_lake.jpg", "08", "Riding Mountain National Park", "Moon Lake, in the park, today", f"Norm Andreiw · CC BY 3.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.75]}),
    (10, "Beyond the trees", None, "whitewater_camp_1944.jpg", "09", "The bunkhouses", "Whitewater camp, 1944", f"Photographer unknown · public domain · {WC}", {"crop": [0.35, 0.25, 0.4, 0.6]}),
    (16, "The prisoners spent their wages", None, "eatons_1942.jpg", "16", "The Eaton's catalogue", "Spring and Summer, 1942", f"T. Eaton Co. · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (20, "In the summer of", None, "winnipeg_1944.jpg", "20", "Winnipeg", "Where she took her six-week teaching course (city view, July 1944)", f"Dept. of National Defence · Library and Archives Canada · public domain · {WC}", {"crop": [0.0, 0.0, 0.95, 1.0]}),
    (21, "Early in nineteen forty-four", None, "geco_dance_1943.jpg", "21", "A wartime dance", "Stand-in: workers dance at a munitions plant, Ontario, c. 1943", f"Archives of Ontario · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (25, "And on his way back", None, "shoal_lake_elevator.jpg", "25", "Shoal Lake, Manitoba", "Her family's town, today", f"Words in the Wind · CC BY 4.0 · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (28, "That summer she went", None, "munitions_workers_1944.jpg", "28", "Munitions workers, 1944", "Stand-in: Agnes Apostle of Dauphin, Manitoba, and Joyce Horne assemble pistols, Toronto, April 1944", f"Ronny Jaques, National Film Board of Canada · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (40, "Today there is", None, "rmnp_moon_lake.jpg", "40", "Riding Mountain today", "A lake in the park", f"Norm Andreiw · CC BY 3.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.75]}),
    (40, "And along the old creek", None, "rmnp_reflection.jpg", "40", "Riding Mountain National Park", "Dead timber and reeds at the water's edge, today", f"Jamie B. · CC BY 2.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
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
    # a card ends where the next one begins
    full = sorted([o for o in overlays if o["type"] != "ContextTag"], key=lambda o: o["start"])
    for a, b in zip(full, full[1:]):
        if b["start"] < a["end"]:
            a["end"] = b["start"]
    # subscribe card at ~36 % of the runtime (silent, as in the reference), on footage between cards
    sub_t = total * 0.36
    busy = [(o["start"], o["end"]) for o in overlays if o["type"] != "ContextTag"]
    while any(a - 1 < sub_t < b + 1 or a - 1 < sub_t + 5 < b + 1 for a, b in busy):
        sub_t += 1.0
    overlays.append({"type": "Slug", "title": CHANNEL["subscribe"], "subtitle": CHANNEL["tagline"], "start": round(sub_t, 3), "end": round(sub_t + 4.5, 3)})
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
