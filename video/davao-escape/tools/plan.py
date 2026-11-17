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
    "CB": ("cebu_prisoners_1945", 1), "BG": ("baguio_mindanao_1945", 1), "PM": ("parachute_mindanao_1945", 1),
    "EV": ("evac_mindanao_1945", 1), "SR": ("mindanao_san_roque_1945", 1), "RL": ("rice_line_manila_1945", 1),
    "JH": ("jungle_health_1944", 1), "P38": ("p38_flight_1943", 1), "NEWS": ("seventeen_days_1945", 1),
    "SW": ("submarine_warfare_1946", 1), "CR": ("corregidor_newsreel_1945", 1), "RP": ("rescued_pows_leyte_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s


LU = "John D. Lukacs, Escape from Davao (2010)"
TE = "Melvyn H. McCoy and S. M. Mellnik, Ten Escape from Tojo (1944)"
DMN = "Dwight Jon Zimmerman, \"POW Escape from Davao,\" Defense Media Network (2013)"
WC = "Wikimedia Commons"
CB_TAG = "Stand-in · American prisoners of the Japanese, freed on Cebu, 1945 · U.S. Army film"
BG_TAG = "Mindanao, near Davao, 1945 · U.S. Army film"
PM_TAG = "Mindanao from the air, 1945 · U.S. Army film"
EV_TAG = "Stand-in · a transport plane, Mindanao, 1945 · U.S. Army film"
SR_TAG = "Stand-in · a coconut grove, Mindanao, 1945 · U.S. Army film"
RL_TAG = "Filipino civilians, Manila, 1945 · U.S. Army film"
JH_TAG = "Stand-in · jungle and swamp · from Personal Health in the Jungle (War Dept., 1944)"
P38_TAG = "Stand-in · a P-38 fighter · from P-38: Flight Characteristics (AAF, 1943)"
P40_TAG = "Stand-in · an Army fighter (a P-38, not Dyess's P-40) · from P-38: Flight Characteristics (1943)"
NEWS_TAG = "Stand-in · a New York newspaper, 1945 · from 17 Days: The Story of Newspaper History in the Making"
SW_TAG = "Stand-in · a U.S. fleet submarine · from Submarine Warfare (U.S. Navy, 1946)"
SEA_TAG = "Stand-in · the sea · from Submarine Warfare (U.S. Navy, 1946)"
CR_TAG = "The Philippines · United News newsreel, February 1945"
RP_TAG = "Stand-in · an American prisoner freed from a Japanese camp, Leyte, 1945 · U.S. Army film"
WARD_TAG = "Stand-in · an Army hospital ward, Leyte, 1945 · U.S. Army film"
CHURCH_TAG = "Stand-in · a church, 1945 · U.S. Army film"
P = [
    # 0 the gate
    [("On", "PM", T(0, 45.9)), ("@", "One by one", PM_TAG),
     ("#", "On Sunday morning", None, {"type": "Slug", "title": "April 4, 1943", "subtitle": "Davao Penal Colony · Mindanao, Philippines"}),
     ("One by one the work", "CB", T(5, 56.1)), ("@", "Among them walked", CB_TAG),
     ("Among them walked", "CB", T(0, 16.4)), ("Across the compound", "CB", T(0, 26.2)),
     ("#", "Hey Steve", None, {"type": "LedgerQuote", "file": "FILE 01 — THE GATE", "head": "Sunday, April 4, 1943, as the work details left",
        "before": "Hey, Steve! ", "key": "Your toothbrush is sticking out of the back of your musette bag.", "after": " Are you planning to escape?",
        "who": "Frank Carpenter, a fellow prisoner, to Maj. Stephen Mellnik", "source": f"{LU}, p. 205"})],
    # 1 roll call
    [("He was", "CB", T(4, 17.5)), ("Then they counted", "CB", T(2, 27.9)), ("Ten Americans and two", "JH", T(8, 33.0)), ("@", "Ten Americans and two", JH_TAG),
     ("In the ten years", "BG", T(3, 29.5)), ("@", "In the ten years", BG_TAG)],
    # 2 this is the story
    [("This is the documented", "CR", T(0, 46.5)), ("@", "This is the documented", CR_TAG),
     ("ten men who walked", "JH", T(5, 45.1)), ("@", "ten men who walked", JH_TAG),
     ("and the months", "NEWS", T(2, 14.5)), ("@", "and the months", NEWS_TAG)],
    # 3 Bataan
    [("Most of them had", "RP", T(6, 46.3)),
     ("#", "On the ninth of April", None, {"type": "Slug", "title": "April 9, 1942", "subtitle": "Bataan peninsula · the American and Filipino army surrenders"}),
     ("Its men were marched", "CB", T(4, 28.4)),
     ("#", "Nearly seven hundred", None, {"type": "LedgerBars", "file": "FILE 02 — THE HIKE", "head": "Deaths on the Bataan Death March, April 1942 (estimates)", "max": 10000,
        "bars": [{"label": "American prisoners", "value": 700, "figure": "nearly 700", "note": ""},
                 {"label": "Filipino prisoners", "value": 10000, "figure": "up to 10,000", "note": ""}],
        "source": f"{LU}, p. 89"})],
    # 4 O'Donnell
    [("At the end of it", "CB", T(0, 46.2)), ("Then came", "CB", T(5, 1.3)),
     ("In November", "SW", T(4, 52.0)), ("@", "In November", SEA_TAG), ("to a prison farm", "PM", T(0, 53.0)), ("@", "to a prison farm", PM_TAG),
     ("#", "The Japanese commandant", None, {"type": "LedgerQuote", "file": "FILE 03 — DAVAO PENAL COLONY", "head": "November 1942: about 2,000 prisoners arrive from Cabanatuan",
        "before": "He stormed about, declaring that he had asked for prisoners capable of doing hard labor. ", "key": "Instead, he shouted, he had been sent a batch of walking corpses.", "after": "",
        "who": "Maj. Stephen Mellnik, on the commandant, Maj. Kazuo Maeda", "source": f"{LU}, p. 135"})],
    # 5 Dyess
    [("Ed Dice was one", "CB", T(6, 18.0)), ("He was a fighter pilot", "P38", T(2, 32.9)), ("@", "He was a fighter pilot", P40_TAG),
     ("and then fought on the ground", "JH", T(1, 5.3)), ("@", "and then fought on the ground", JH_TAG), ("He was captured", "RP", T(1, 0.0)), ("@", "He was captured", RP_TAG)],
    # 6 the ten
    [("The others came", "CB", T(5, 23.2)), ("He would navigate", "SW", T(41, 6.8)), ("@", "He would navigate", SW_TAG),
     ("Austin Shofner Jack", "CB", T(4, 39.4)),
     ("#", "Sam Grash-ee-oh was a pilot", None, {"type": "LedgerTimeline", "file": "FILE 04 — THE TEN", "head": "The ten Americans who escaped, April 4, 1943",
        "rows": [{"date": "ARMY AIR", "text": "Capt. William E. \"Ed\" Dyess · 2nd Lt. Samuel Grashio · 2nd Lt. Leo Boelens"},
                 {"date": "NAVY", "text": "Lt. Cmdr. Melvyn H. McCoy"},
                 {"date": "ARMY", "text": "Maj. Stephen M. Mellnik · Sgt. Paul Marshall · Sgt. Robert Spielman"},
                 {"date": "MARINES", "text": "Capt. Austin C. Shofner · 1st Lt. Jack Hawkins · 1st Lt. Michael Dobervich"}],
        "source": f"{TE}, foreword · {LU}"})],
    # 7 the two Filipinos
    [("Two Filipinos completed", "RL", T(2, 3.6)), ("@", "Two Filipinos completed", "Stand-in · " + RL_TAG),
     ("Jumarong had once", "JH", T(2, 38.6)), ("@", "Jumarong had once", JH_TAG), ("Without that trail", "JH", T(14, 8.8))],
    # 8 shooting squads
    [("The plan was dangerous", "CB", T(2, 38.9)), ("If one man escaped", "CB", T(3, 22.7)), ("Nobody at Dah-vow", "PM", T(0, 36.0)), ("@", "Nobody at Dah-vow", PM_TAG),
     ("#", "Mel-nik put the reason", None, {"type": "LedgerQuote", "file": "FILE 05 — WHY THEY WENT", "head": "The plan to escape, early 1943",
        "before": "", "key": "We must make the horrors of O'Donnell, Cabanatuan, and Davao a matter of record.", "after": "",
        "who": "Maj. Stephen Mellnik", "source": DMN})],
    # 9 the morning
    [("For weeks they had", "BG", T(7, 33.5)), ("On the morning of the escape", "JH", T(11, 39.5)), ("@", "On the morning of the escape", JH_TAG),
     ("Then they waited", "JH", T(4, 30.5)), ("@", "Then they waited", JH_TAG), ("Ten minutes passed", "JH", T(13, 12.8)), ("At nine o'clock", "JH", T(1, 23.9))],
    # 10 the swamp
    [("Then came the swamp", "JH", T(3, 53.2)), ("@", "Then came the swamp", JH_TAG),
     ("#", "The first night", None, {"type": "LedgerQuote", "file": "FILE 06 — THE SWAMP", "head": "The first night out, April 4, 1943",
        "before": "At night we finally found a place to camp — here the water was only ankle deep... ", "key": "we awoke to find ourselves half-floating in our beds.", "after": "",
        "who": "Melvyn McCoy and Stephen Mellnik", "source": TE})],
    # 11 the boy
    [("On the fourth day", "BG", T(8, 26.8)), ("@", "On the fourth day", BG_TAG), ("He ran then stopped", "RL", T(1, 40.1)), ("@", "He ran then stopped", "Stand-in · " + RL_TAG),
     ("His village he said", "BG", T(9, 7.4)), ("@", "His village he said", BG_TAG)],
    # 12 Lungaog
    [("The whole village", "BG", T(7, 46.3)), ("@", "The whole village", "Stand-in · Filipinos greet American troops, Mindanao, 1945 · U.S. Army film"),
     ("#", "Days later", "Not every meeting", {"type": "LedgerQuote", "file": "FILE 07 — LUNGAOG", "head": "Austin Shofner's diary, April 10, 1943",
        "before": "As I am writing this, ", "key": "I am listening to phonograph play the first American music I heard in a long time.", "after": "",
        "who": "Capt. Austin Shofner, USMC", "source": f"{LU}, p. 235"}),
     ("Not every meeting", "JH", T(7, 18.4)), ("@", "Not every meeting", JH_TAG)],
    # 13 the submarine
    [("Guerrilla bands passed", "PM", T(0, 38.5)), ("@", "Guerrilla bands passed", PM_TAG), ("across some three hundred", "PM", T(1, 40.6)),
     ("#", "On the ninth of July", None, {"type": "Slug", "title": "July 9, 1943", "subtitle": "The submarine Trout takes Dyess, McCoy and Mellnik off Mindanao"}),
     ("Most of the others", "SW", T(21, 23.8)), ("@", "Most of the others", SW_TAG), ("Three stayed on", "BG", T(9, 20.9)), ("@", "Three stayed on", "Stand-in · " + BG_TAG)],
    # 14 MacArthur
    [("In Australia they told", "SW", T(14, 48.1)), ("@", "In Australia they told", SW_TAG),
     ("#", "The Japanese he said", "Dice's account was typed", {"type": "LedgerQuote", "file": "FILE 08 — BRISBANE", "head": "Gen. Douglas MacArthur hears the escapees, July 1943",
        "before": "", "key": "The Japanese will pay for that humiliation and suffering.", "after": "",
        "who": "Gen. Douglas MacArthur", "source": DMN}),
     ("Dice's account was typed", "EV", T(1, 33.5)), ("@", "Dice's account was typed", EV_TAG),
     ("#", "The War Department would", None, {"type": "LedgerQuote", "file": "FILE 09 — THE DEPOSITION", "head": "Ed Dyess's account, as the War Department later described it",
        "before": "", "key": "the greatest story of the war in the Pacific", "after": "",
        "who": "U.S. War Department, January 1944", "source": f"Fort Worth Star-Telegram, January 29, 1944 · {LU}, p. 266"})],
    # 15 nothing happened
    [("And then nothing", "SW", T(35, 37.9)), ("@", "And then nothing", SEA_TAG)],
    # 16 subscribe
    [("If you want more", "NEWS", T(15, 41.7)),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 17 August 9
    [("Ed Dice landed", "P38", T(14, 55.7)), ("@", "Nobody met him", P38_TAG),
     ("#", "Ed Dice landed", None, {"type": "Slug", "title": "August 9, 1943", "subtitle": "Washington · Ed Dyess's twenty-seventh birthday"}),
     ("Nobody met him", "NEWS", T(5, 0.1)), ("@", "There were no reporters", NEWS_TAG), ("He gave a long statement", "RP", T(0, 33.3)), ("@", "He gave a long statement", "Stand-in · a freed American prisoner is interviewed, Leyte, 1945 · U.S. Army film"),
     ("#", "It was absolutely necessary", None, {"type": "LedgerQuote", "file": "FILE 10 — THE STATEMENT", "head": "Ed Dyess's deposition to the War Department, August 1943",
        "before": "In my opinion, it is not only advisable, but ", "key": "absolutely necessary that all civilized people of the world know the conditions of the Japanese prison camps", "after": " and the atrocities against American prisoners of war.",
        "who": "Maj. William E. Dyess", "source": f"{LU}, p. 302"})],
    # 18 Ashford
    [("Instead he was sent", "RP", T(9, 0.0)), ("@", "Instead he was sent", WARD_TAG), ("If he told his story", "CB", T(3, 44.6)), ("McCoy and Mel-nik", "SW", T(11, 30.7)), ("@", "McCoy and Mel-nik", SW_TAG)],
    # 19 Roosevelt
    [("The order came from", "NEWS", T(3, 58.0)), ("@", "The order came from", NEWS_TAG), ("President Roosevelt agreed", "SW", T(38, 55.3)), ("@", "President Roosevelt agreed", SEA_TAG), ("a neutral Swedish ship", "CR", T(4, 53.9)), ("@", "a neutral Swedish ship", "Stand-in · ships at sea · United News newsreel, 1945"),
     ("#", "He asked that no story", "Some historians think", {"type": "LedgerQuote", "file": "FILE 11 — THE WHITE HOUSE", "head": "President Roosevelt's memorandum, 1943",
        "before": "I agree with your opinion that any publication of Japanese atrocities at this time might complicate the present and future missions of the GRIPSHOLM... ",
        "key": "I request, therefore, that you take effective measures to prevent the publication or circulation of any stories emanating from escaped prisoners", "after": " until I have authorized a release.",
        "who": "Franklin D. Roosevelt", "source": f"{LU}, p. 304"}),
     ("Some historians think", "CR", T(4, 14.7)), ("@", "Some historians think", CR_TAG)],
    # 20 the Tribune
    [("The Chicago Tribune wanted", "NEWS", T(1, 29.0)), ("@", "The Chicago Tribune wanted", NEWS_TAG), ("It offered Dice", "NEWS", T(1, 12.4)), ("The finished chapters", "NEWS", T(5, 20.8)),
     ("#", "Nothing was going to happen", None, {"type": "LedgerQuote", "file": "FILE 12 — SIX WEEKS", "head": "War Department public relations to the Chicago Tribune, September 9, 1943",
        "before": "", "key": "Nothing is going to happen on this thing for at least six weeks.", "after": "",
        "who": "Brig. Gen. Alexander Surles", "source": f"{LU}, p. 305"})],
    # 21 Texas steak
    [("Dice was allowed home", "NEWS", T(1, 53.8)), ("@", "Dice was allowed home", NEWS_TAG), ("The newspapers could not", "NEWS", T(6, 22.9)),
     ("#", "One headline read", None, {"type": "LedgerQuote", "file": "FILE 13 — ALBANY, TEXAS", "head": "The Dallas Morning News, autumn 1943",
        "before": "", "key": "One-Man Scourge of Japanese Turns Talents on Texas Steak", "after": "",
        "who": "Headline", "source": f"Dallas Morning News, 1943 · quoted in {LU}, p. 319"})],
    # 22 Burbank
    [("Then he went back", "P38", T(3, 16.6)), ("@", "Then he went back", P38_TAG),
     ("#", "On Wednesday", None, {"type": "Slug", "title": "December 22, 1943", "subtitle": "Grand Central Air Terminal · near Burbank, California"}),
     ("Just after takeoff", "P38", T(19, 17.8)), ("Below him were houses", "P38", T(30, 56.9))],
    # 23 the crash
    [("He stayed with", "P38", T(22, 12.6)), ("@", "He stayed with", P38_TAG), ("He brought it down", "P38", T(23, 40.0)), ("A wing clipped", "P38", T(28, 2.1))],
    # 24 the memorial
    [("Five days later", "BG", T(2, 8.4)), ("@", "Five days later", CHURCH_TAG),
     ("#", "A general told them", None, {"type": "LedgerTimeline", "file": "FILE 14 — THE GAG ORDER", "head": "Ed Dyess's story, August–December 1943",
        "rows": [{"date": "AUG. 9", "text": "Dyess lands in the United States; officially he is not there"},
                 {"date": "AUG.", "text": "Deposition to the War Department; sent to Ashford General Hospital, W.Va."},
                 {"date": "SEPT. 9", "text": "\"Nothing is going to happen on this thing for at least six weeks\""},
                 {"date": "DEC. 22", "text": "Dyess killed in a P-38, Burbank, California; the story still unpublished"}],
        "source": f"{LU}, pp. 18, 301–305, 324–328"})],
    # 25 January 28
    [("A month later", "NEWS", T(2, 35.2)), ("@", "A month later", NEWS_TAG),
     ("#", "At midnight on Friday", None, {"type": "Slug", "title": "January 28, 1944", "subtitle": "Washington · the Army and Navy release the story at midnight"}),
     ("#", "The New York Times headline", None, {"type": "LedgerQuote", "file": "FILE 15 — THE HEADLINE", "head": "The New York Times, January 28, 1944, front page",
        "before": "", "key": "5,200 AMERICANS, MANY MORE FILIPINOS DIE OF STARVATION, TORTURE AFTER BATAAN", "after": "",
        "who": "Banner headline", "source": f"The New York Times, January 28, 1944 · quoted in {LU}, p. 343"})],
    # 26 the Tribune series
    [("That Sunday", "NEWS", T(16, 2.4)), ("@", "That Sunday", NEWS_TAG),
     ("#", "There would be twenty-four", None, {"type": "LedgerTimeline", "file": "FILE 16 — THE STORY COMES OUT", "head": "January–February 1944",
        "rows": [{"date": "JAN. 28", "text": "Joint Army-Navy statement on Japanese atrocities against American prisoners"},
                 {"date": "JAN. 30", "text": "Chicago Tribune: the Dyess story, part 1 of 24, in about 100 newspapers"},
                 {"date": "FEB. 7", "text": "Life: McCoy and Mellnik, \"Death Was a Part of Our Life,\" 15 pages"}],
        "source": f"{LU}, pp. 343–347"})],
    # 27 the country
    [("The country was furious", "NEWS", T(7, 4.3)),
     ("#", "At the launching", "War bond sales", {"type": "LedgerQuote", "file": "FILE 17 — THE MISSOURI", "head": "Christening of the battleship Missouri, January 29, 1944",
        "before": "", "key": "May this great ship be an avenger to the barbarians who wantonly slaughtered the heroes of Bataan.", "after": "",
        "who": "Margaret Truman", "source": DMN}),
     ("War bond sales", "NEWS", T(10, 31.2)), ("@", "War bond sales", NEWS_TAG), ("From that day on", "NEWS", T(9, 49.8))],
    # 28 Shinyo Maru
    [("The men left behind", "RP", T(5, 0.0)), ("In nineteen forty-four", "SW", T(1, 38.7)), ("@", "In nineteen forty-four", SEA_TAG),
     ("#", "On the seventh of September", None, {"type": "Slug", "title": "September 7, 1944", "subtitle": "The Shinyo Maru, carrying the last Davao prisoners · off Mindanao"}),
     ("an American submarine", "SW", T(21, 36.5)), ("@", "an American submarine", SW_TAG), ("Fewer than a hundred", "SW", T(34, 32.2))],
    # 29 the ten after
    [("Of the ten", "P38", T(4, 0.3)), ("@", "Of the ten", P38_TAG), ("Years later he made", "P38", T(25, 51.1)), ("And in nineteen fifty-six", "P38", T(6, 55.1)),
     ("#", "Grash-ee-oh wrote that", None, {"type": "LedgerQuote", "file": "FILE 18 — DYESS AIR FORCE BASE", "head": "Abilene Air Force Base renamed for Ed Dyess, December 1, 1956",
        "before": "If Ed was watching in the Great Beyond he probably would have laughed, ", "key": "for it was a bomber base while he was a fighter pilot.", "after": "",
        "who": "Samuel Grashio", "source": f"{LU}, p. 372"})],
    # 30 your story
    [("If someone in your family", "CB", T(6, 7.0)),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Was your family there?", "subtitle": "A prisoner of the Japanese, or a Filipino who helped · tell us in the comments"})],
    # 31 the plaque
    [("The Dah-vow Penal Colony is still", "BG", T(3, 29.5)), ("@", "The Dah-vow Penal Colony is still", BG_TAG),
     ("When the historian", "EV", T(1, 44.0)), ("@", "When the historian", EV_TAG), ("The ten walked out", "SW", T(4, 52.5)), ("@", "The ten walked out", SEA_TAG),
     ("It took ten months", "SR", T(6, 20.7)), ("@", "It took ten months", "Stand-in · the coast of Mindanao, 1945 · U.S. Army film")],
]

PHOTOS = [
    (0, "while a Japanese guard", None, "dapecol_train.jpg", "00", "The Davao Penal Colony", "The colony's train, which ran the prisoners out to the fields · 1940s", f"Philippine Bureau of Corrections · public domain · {WC}", {}),
    (3, "Its men were marched", None, "bataan_prisoners.jpg", "03", "The Death March, April 1942", "American prisoners, hands tied behind their backs · captured Japanese photograph", f"National Archives 127-N-114541 · public domain · {WC}", {}),
    (4, "At the end of it", None, "litters_1942.jpg", "04", "Camp O'Donnell, May 1942", "Prisoners carry comrades on improvised litters · captured Japanese photograph", f"National Archives 535565 · public domain · {WC}", {}),
    (5, "Ed Dice was one", None, "dyess_portrait.jpg", "05", "Capt. William Edwin \"Ed\" Dyess", "Albany, Texas · photographed after his return, 1943", f"U.S. Air Force · public domain · {WC}", {}),
    (6, "Stephen Mel-nik was", None, "mellnik_cadet.jpg", "06", "Stephen M. Mellnik", "As a West Point cadet, about 1932", f"U.S. Military Academy · public domain · {WC}", {}),
    (6, "Austin Shofner Jack", None, "shofner_1941.jpg", "06", "Austin C. Shofner, USMC", "As a first lieutenant, 1941", f"U.S. Marine Corps · public domain · {WC}", {}),
    (13, "the submarine Trout", None, "uss_trout.jpg", "13", "USS Trout (SS-202)", "At Pearl Harbor, March 1942", f"U.S. Navy · public domain · {WC}", {}),
    (22, "from Grand Central", None, "grand_central_postcard.jpg", "22", "Grand Central Air Terminal", "Glendale, near Burbank, California · postcard, about 1930", f"public domain · {WC}", {}),
    (23, "Ed Dice was killed", None, "dyess_portrait.jpg", "23", "Maj. William Edwin Dyess", "1916–1943", f"U.S. Air Force · public domain · {WC}", {}),
    (28, "The men left behind", None, "davao_list_1945.jpg", "28", "\"List of American Prisoners ... in the Davao Concentration Camp\"", "U.S. Army report, February 1945", f"National Archives · public domain · {WC}", {}),
    (31, "Its historical marker", None, "dapecol_marker.jpg", "31", "Davao Penal Colony marker, 1956", "\"...used as concentration camp for American prisoners of war\" · photographed 2025", f"JasmineGoforth · CC BY 4.0 · {WC}", {}),
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
