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
    "BB": ("battle_of_britain_1943", 1), "BD": ("bus_driver_1946", 1), "BC": ("boy_in_court_1940", 1),
    "DE": ("detroit_edison_1946", 1), "BL": ("bright_lights_1935", 1), "FT": ("presidents_tour_1942", 1),
    "CP": ("controlling_german_pows_1944", 1), "TT": ("troop_train_1943", 1),
}


def T(m, s=0.0):
    return m * 60 + s

CA6 = "Stephan v. United States, 133 F.2d 87 (6th Cir. 1943)"
DC = "United States v. Stephan, 50 F. Supp. 738 (E.D. Mich. 1943)"
WP = "Wikipedia, “Max Stephan” (after the Detroit Free Press and the Windsor Star, 1942-43)"
SASE = "J. Sase & G. J. Senick, “Treason in Detroit,” Detroit Legal News, Mar. 17, 2021"
BB_TAG = "Battle of Britain, 1940 · from The Battle of Britain (U.S. Army, 1943)"
BD_TAG = "Stand-in · from The Bus Driver (1946)"
BC_TAG = "Stand-in · from Boy in Court (1940)"
DE_TAG = "Stand-in · from My Dad's Company (Detroit Edison, 1946)"
BL_TAG = "Stand-in · city lights, 1935 · from Behind the Bright Lights"
CP_TAG = "Stand-in · from Controlling German Prisoners of War (U.S. Army, 1944)"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
FT_TAG = "President Roosevelt, 1942 · FDR Library film"
P = [
    # 0 the birthday
    [("On", "BD", T(1, 46.6)), ("@", "a restaurant owner", BD_TAG),
     ("#", "On the afternoon", None, {"type": "Slug", "title": "April 18, 1942", "subtitle": "Detroit, Michigan · a Saturday"}),
     ("He gave him a necktie", "BD", T(0, 56.5)), ("and drove him from bar to bar", "BL", T(6, 48.2)), ("@", "and drove him from bar to bar", BL_TAG),
     ("At each stop", "BL", T(0, 50.1))],
    # 1 the guest
    [("The guest was not", "CP", T(12, 5.5)), ("@", "The guest was not", CP_TAG), ("A few days earlier", "CP", T(12, 14.0)), ("in a prisoner of war camp", "CP", T(12, 5.5))],
    # 2 the restaurant owner
    [("The restaurant owner was", "DE", T(16, 1.1)), ("Within four months", "BC", T(6, 50.3)), ("@", "Within four months", BC_TAG),
     ("This is the documented story", "BD", T(2, 49.4)), ("@", "This is the documented story", BD_TAG)],
    # 3 the pilot
    [("Kroog testified", "BB", T(22, 19.0)), ("@", "Kroog testified", BB_TAG),
     ("#", "in August nineteen forty", None, {"type": "Slug", "title": "August 28, 1940", "subtitle": "Krug's bomber is shot down over England · his sworn testimony"}),
     ("he was shot down", "BB", T(16, 15.0)), ("while flying a bomber", "BB", T(1, 57.0)), ("In January nineteen forty-one", "BB", T(12, 21.0)), ("across the Atlantic", "TT", T(6, 29.5)), ("@", "across the Atlantic", TT_TAG), ("and later to a camp", "CP", T(4, 40.5)), ("@", "and later to a camp", CP_TAG)],
    # 4 Bowmanville
    [("Bowmanville had been", "CP", T(12, 20.0)), ("The Canadians ringed", "CP", T(12, 5.5)), ("@", "The Canadians ringed", CP_TAG),
     ("For an officer", "CP", T(12, 12.0)), ("The year before", "TT", T(7, 41.9)), ("@", "The year before", TT_TAG),
     ("crossed the frozen", "TT", T(6, 47.6)), ("and made it all the way", "TT", T(6, 29.5))],
    # 5 the escape
    [("In the middle of April", "CP", T(7, 54.0)), ("@", "In the middle of April", CP_TAG),
     ("#", "In the middle of April", None, {"type": "Slug", "title": "Mid-April 1942", "subtitle": "Krug walks out of Camp 30, Bowmanville, Ontario"}),
     ("In Toronto", "BD", T(5, 32.5)), ("He showed them forged", "BC", T(1, 51.9)), ("@", "He showed them forged", BC_TAG),
     ("A Catholic priest", "BD", T(0, 18.8)), ("@", "A Catholic priest", BD_TAG)],
    # 6 the river
    [("In Windsor", "DE", T(4, 8.4)), ("@", "In Windsor", DE_TAG), ("He was now inside", "BL", T(6, 48.2)), ("@", "He was now inside", BL_TAG),
     ("He spent the night", "BL", T(6, 33.9))],
    # 7 the address
    [("Other prisoners had given", "CP", T(7, 34.6)), ("@", "Other prisoners had given", CP_TAG), ("Margareta", "DE", T(16, 22.7)), ("@", "Margareta", DE_TAG),
     ("She knitted", "DE", T(17, 27.5))],
    # 8 the knock
    [("At about half past nine", "BC", T(3, 21.4)), ("@", "At about half past nine", BC_TAG),
     ("#", "At about half past nine", None, {"type": "Slug", "title": "Saturday, 9:30 a.m.", "subtitle": "259 Phillip Avenue, Detroit"}),
     ("He showed her", "BC", T(4, 51.0)), ("She let him in", "TT", T(1, 39.6)), ("@", "She let him in", TT_TAG)],
    # 9 Stephan
    [("Stephan was born", "DE", T(9, 10.8)), ("@", "Stephan was born", DE_TAG), ("In nineteen twenty-eight", "DE", T(4, 8.4)),
     ("#", "In nineteen thirty-five", "His restaurant", {"type": "LedgerQuote", "file": "FILE 01 — THE OATH", "head": "Sworn by Max Stephan, June 28, 1935",
        "before": "I absolutely and entirely renounce and abjure all allegiance and fidelity to any foreign prince, potentate, state or sovereignty, and ",
        "key": "particularly to Germany", "after": ".", "who": "Oath of allegiance, naturalization of Max Stephan", "source": CA6}),
     ("His restaurant", "BL", T(6, 48.2)), ("@", "His restaurant", BL_TAG), ("Stephan denied", "DE", T(16, 1.1))],
    # 10 the kitchen
    [("Stephan arrived", "BC", T(4, 36.0)), ("@", "Stephan arrived", BC_TAG),
     ("#", "She testified that", "Kroog remembered", {"type": "LedgerQuote", "file": "FILE 02 — THE KITCHEN", "head": "Mrs. Bertelmann's testimony",
        "before": "What are you shaking for? ", "key": "You're crazy.", "after": "",
        "who": "Max Stephan to Margareta Bertelmann, April 18, 1942, as she testified", "source": CA6}),
     ("Kroog remembered", "BC", T(4, 51.0)), ("She heard Stephan ask", "DE", T(10, 58.7)), ("@", "She heard Stephan ask", DE_TAG)],
    # 11 the help
    [("Then the help began", "DE", T(17, 27.5)), ("@", "Then the help began", DE_TAG), ("One of Kroog's shoes", "BD", T(0, 56.5)), ("@", "One of Kroog's shoes", BD_TAG),
     ("Twenty dollars of hers", "DE", T(10, 58.7)), ("When the men left", "BD", T(1, 46.6)), ("Stephan walked the pilot", "DE", T(14, 13.1))],
    # 12 the restaurant
    [("At the restaurant", "BL", T(6, 48.2)), ("@", "At the restaurant", BL_TAG), ("Kroog ate", "BL", T(6, 33.9)), ("Then the escaped enemy officer", "DE", T(4, 8.4)), ("When he came back", "BL", T(0, 50.1)),
     ("#", "When he came back", None, {"type": "LedgerQuote", "file": "FILE 03 — THE BIRTHDAY", "head": "Saturday afternoon",
        "before": "Now, I have nothing to do and ", "key": "it is your birthday today", "after": " and we will take a pleasure trip.",
        "who": "Max Stephan to Hans Peter Krug, as Krug testified", "source": CA6})],
    # 13 the trip
    [("At Haller's Cafe", "BL", T(6, 33.9)), ("@", "At Haller's Cafe", BL_TAG), ("At the Progressive Club", "BL", T(6, 48.2)),
     ("Then they went to the shop", "DE", T(12, 46.7)), ("@", "Then they went to the shop", DE_TAG), ("Here Kroog gave", "DE", T(16, 1.1)),
     ("Stephan bought him candy", "DE", T(16, 44.3)), ("A clerk named", "DE", T(18, 10.7))],
    # 14 the night
    [("Back at the restaurant", "BL", T(0, 50.1)), ("When a young couple", "BL", T(6, 33.9)), ("A waitress offered", "DE", T(10, 58.7)), ("Stephan said no", "BL", T(6, 48.2)),
     ("#", "Back at the restaurant", None, {"type": "LedgerTimeline", "file": "FILE 04 — ONE SATURDAY", "head": "Krug's day in Detroit, April 18, 1942",
        "rows": [{"date": "9:30 A.M.", "text": "Mrs. Bertelmann's kitchen: shoes, socks, $20"},
                 {"date": "NOON", "text": "Stephan's restaurant, Jefferson Avenue"},
                 {"date": "AFTERNOON", "text": "Haller's Cafe: “one of the Meyers boys”"},
                 {"date": "AFTERNOON", "text": "Donay's shop: candy, another $20"},
                 {"date": "EVENING", "text": "Dinner: “a friend from Milwaukee”"},
                 {"date": "9 P.M.", "text": "Out the back door, to the Field Hotel"}],
        "source": CA6})],
    # 15 the bus
    [("At eight the next morning", "BD", T(0, 6.3)), ("@", "At eight the next morning", BD_TAG), ("Stephan had looked up", "BD", T(0, 31.4)),
     ("They had breakfast", "BD", T(1, 21.6)), ("Then Stephan bought him", "BD", T(0, 18.8)), ("and Kroog was gone", "BD", T(2, 49.4))],
    # 16 the arrest
    [("The next day", "DE", T(18, 10.7)), ("@", "The next day", DE_TAG), ("He went to the", "TT", T(1, 57.7)),
     ("#", "On Monday morning", None, {"type": "Slug", "title": "April 20, 1942", "subtitle": "The FBI arrests Max Stephan in Detroit"}),
     ("On Monday morning", "BC", T(1, 37.0)), ("That same day", "BC", T(2, 21.8)), ("@", "That same day", BC_TAG)],
    # 17 the run
    [("Kroog was heading", "BD", T(3, 39.6)), ("@", "Kroog was heading", BD_TAG),
     ("#", "According to one later account", None, {"type": "LedgerMap", "file": "FILE 05 — THE RUN", "head": "Twelve days, by bus and train",
        "stops": ["Detroit", "Chicago", "New York", "Pittsburgh", "Nashville", "Dallas", "San Antonio"],
        "legs": ["April 19, bus", "via Philadelphia", "no ship", "via Cincinnati", "", "May 1"], "extra": ["Laredo"],
        "source": "Route after Chicago as told by " + SASE})],
    # 18 San Antonio
    [("On May first", "BD", T(7, 25.4)), ("@", "On May first", BD_TAG),
     ("#", "On May first", None, {"type": "Slug", "title": "May 1, 1942", "subtitle": "San Antonio, Texas · Krug is arrested"}),
     ("One account says", "BC", T(1, 51.9)), ("@", "One account says", BC_TAG),
     ("#", "On him", None, {"type": "LedgerTimeline", "file": "FILE 06 — EXHIBITS", "head": "Taken from Krug in San Antonio",
        "rows": [{"date": "EXHIBIT", "text": "A revolver and cartridges"},
                 {"date": "EXHIBIT", "text": "A Greyhound bus map"},
                 {"date": "EXHIBIT", "text": "Matthews Atlas of the World at War"},
                 {"date": "CARD", "text": "A note in his own hand. In court: “I won't read it.”"}],
        "source": CA6})],
    # 19 the charge
    [("Hiding an escaped", "BC", T(10, 4.3)), ("@", "Hiding an escaped", BC_TAG), ("In June, a grand jury", "BC", T(9, 19.5)),
     ("#", "The Constitution defines", "And it adds", {"type": "LedgerQuote", "file": "FILE 07 — THE CONSTITUTION", "head": "Article III, Section 3",
        "before": "Treason against the United States, shall consist only in levying War against them, or in ",
        "key": "adhering to their Enemies, giving them Aid and Comfort", "after": ".", "who": "Constitution of the United States, 1787", "source": "Art. III, Sec. 3, Cl. 1"}),
     ("#", "And it adds", "The indictment listed", {"type": "LedgerQuote", "file": "FILE 08 — THE RULE", "head": "Article III, Section 3",
        "before": "No Person shall be convicted of Treason unless on the ", "key": "Testimony of two Witnesses to the same overt Act",
        "after": ", or on Confession in open Court.", "who": "Constitution of the United States, 1787", "source": "Art. III, Sec. 3, Cl. 1"}),
     ("The indictment listed", "BC", T(6, 20.5))],
    # 20 the trial
    [("The trial opened", "BC", T(10, 4.3)), ("@", "The trial opened", BC_TAG), ("The government's main witness", "BC", T(5, 50.6)), ("Under the rules of war", "BC", T(6, 35.4))],
    # 21 the witness
    [("Then, in the afternoon", "BC", T(6, 50.3)), ("@", "Then, in the afternoon", BC_TAG),
     ("#", "I don't intend", None, {"type": "LedgerQuote", "file": "FILE 09 — THE WITNESS", "head": "Krug, on the stand, July 1942",
        "before": "I asked the FBI agents that ", "key": "I never can testify against a man who helped me", "after": ".",
        "who": "Lt. Hans Peter Krug, testimony in U.S. v. Stephan", "source": CA6})],
    # 22 the closing
    [("Stephan never took", "BC", T(6, 20.5)), ("His lawyer", "BC", T(9, 34.5)),
     ("#", "The prosecutor told", None, {"type": "LedgerQuote", "file": "FILE 10 — THE CLOSING", "head": "The government's closing argument",
        "before": "…to get Lieutenant Krug back to Germany so he could ", "key": "get up in a bomber and come over here and bomb the United States", "after": ".",
        "who": "U.S. Attorney John C. Lehr, to the jury", "source": CA6})],
    # 23 the verdict
    [("Judge Tuttle told the jury", "BC", T(6, 50.3)), ("@", "Judge Tuttle told the jury", BC_TAG), ("They could convict", "BC", T(7, 5.3)),
     ("By most accounts", "BC", T(9, 34.5))],
    # 24 the sentence
    [("On August sixth", "BC", T(6, 35.4)),
     ("#", "On August sixth", None, {"type": "LedgerQuote", "file": "FILE 11 — THE SENTENCE", "head": "Detroit, August 6, 1942",
        "before": "The life of the traitor Max Stephan is ", "key": "less valuable than the lives of our loyal sons", "after": ".",
        "who": "Judge Arthur J. Tuttle, sentencing Stephan to hang", "source": WP})],
    # 25 the appeal
    [("Appeals pushed", "BC", T(9, 19.5)), ("@", "Appeals pushed", BC_TAG),
     ("#", "In February", None, {"type": "LedgerTimeline", "file": "FILE 12 — THE TWELVE ACTS", "head": "As sorted by the Court of Appeals, February 1943",
        "rows": [{"date": "NOT PROVED", "text": "The drive to Mrs. Bertelmann's house"},
                 {"date": "NOT PROVED", "text": "The $20 from her table"},
                 {"date": "NOT PROVED", "text": "Candy and money at Donay's shop"},
                 {"date": "PROVED", "text": "The walk to the car"},
                 {"date": "PROVED", "text": "Drinks at Haller's Cafe"},
                 {"date": "PROVED", "text": "The dinner, and the Field Hotel"}],
        "source": CA6}),
     ("The conviction stood", "BC", T(10, 4.3))],
    # 26 the gallows
    [("Some people told", "FT", T(9, 22.1)), ("@", "Some people told", FT_TAG),
     ("#", "Judge Tuttle answered", "A scaffold", {"type": "LedgerQuote", "file": "FILE 13 — THE ANSWER", "head": "From the bench, June 5, 1943",
        "before": "", "key": "There should be no trifling with traitors.", "after": "", "who": "Judge Arthur J. Tuttle, setting the new date", "source": DC}),
     ("A scaffold was built", "BC", T(2, 36.7)), ("@", "A scaffold was built", BC_TAG)],
    # 27 nine hours
    [("At four fifty-five", "TT", T(1, 57.7)), ("@", "At four fifty-five", TT_TAG), ("on July first", "TT", T(1, 39.6)), ("word reached the prison", "BC", T(2, 36.7)),
     ("#", "At four fifty-five", None, {"type": "Slug", "title": "July 1, 1943 · 4:55 p.m.", "subtitle": "About nine hours before the hanging"}),
     ("He believed", "FT", T(2, 52.4)), ("@", "He believed", FT_TAG)],
    # 28 the statement
    [("The White House", "FT", T(4, 7.3)), ("@", "The White House", FT_TAG),
     ("#", "The man was properly", None, {"type": "LedgerQuote", "file": "FILE 14 — THE COMMUTATION", "head": "White House statement, July 1, 1943",
        "before": "The man was properly convicted of treason. ", "key": "He was guilty.", "after": "",
        "who": "Statement on President Roosevelt's commutation", "source": WP})],
    # 29 what happened to Stephan
    [("Max Stephan spent", "BC", T(2, 21.8)), ("and was moved", "TT", T(9, 12.5)), ("He died there", "CP", T(12, 5.5)), ("@", "He died there", CP_TAG),
     ("His wife Agnes", "BD", T(4, 54.8)), ("@", "His wife Agnes", BD_TAG), ("Theodore Donay", "DE", T(12, 46.7))],
    # 30 Krug
    [("Hans Peter Kroog was sent", "CP", T(7, 54.0)), ("@", "Hans Peter Kroog was sent", CP_TAG), ("In August", "CP", T(12, 5.5)),
     ("After the war", "TT", T(6, 29.5)), ("@", "After the war", TT_TAG)],
    # 31 comment ask
    [("If your family", "DE", T(4, 8.4)),
     ("#", "If your family", None, {"type": "Slug", "title": "Detroit, 1942, in your family's story?", "subtitle": "Tell us in the comments"})],
    # 32 echo
    [("The old boys' school", "CP", T(12, 20.0)), ("In 2013", "CP", T(12, 5.5)), ("And in the federal law books", "BC", T(9, 34.5)), ("@", "And in the federal law books", BC_TAG),
     ("A necktie", "BD", T(0, 56.5)), ("and a bus ticket", "BD", T(2, 49.4)), ("Twelve acts", "BD", T(9, 5.8))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (1, "He was Lieutenant", None, "krug_1942.jpg", "01", "Lt. Hans Peter Krug", "Escorted into the Detroit courtroom, July 1942 (insignia blurred)", f"Detroit Times, July 1, 1942 · public domain · {WC}", {"crop": [0.43, 0.04, 0.55, 0.42]}),
    (2, "The restaurant owner was", None, "stephan_1943.png", "02", "Max Stephan", "Detroit restaurant owner, U.S. citizen since 1935", f"Detroit Evening News, July 2, 1943 · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (3, "at Bowmanville", None, "camp30_admin_1941.jpg", "03", "Camp 30, Bowmanville", "The school building, October 1941, as the camp opened", f"Toronto Public Library · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (4, "Bowmanville had been", None, "bowmanville_1941.jpg", "04", "Bowmanville, Ontario", "The boys' training school, readied for German officer prisoners, September 1941", f"Toronto Public Library · public domain · {WC}", {"crop": [0.0, 0.15, 1.0, 0.75]}),
    (6, "he landed on Belle Isle", None, "belle_isle.jpg", "06", "Belle Isle, Detroit", "The island park in the Detroit River (postcard, 1930s)", f"Tichnor Brothers · Boston Public Library · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (9, "he crossed to Detroit", None, "woodward_1942.jpg", "09", "Detroit, 1942", "Woodward Avenue and the skyline, July 1942", f"Arthur S. Siegel, OWI · Library of Congress · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (12, "Then the escaped enemy officer", None, "detroit_skyline_1942.jpg", "12", "Downtown Detroit", "Looking south to the skyline, July 1942", f"Arthur S. Siegel, OWI · Library of Congress · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (17, "toward the border crossing", None, "pittsburgh_greyhound_1943.jpg", "17", "Greyhound, Pittsburgh", "The waiting room of the Greyhound terminal, September 1943", f"Esther Bubley, OWI · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.7]}),
    (20, "Judge Arthur Tuttle", None, "tuttle.jpg", "20", "Judge Arthur J. Tuttle", "U.S. District Court, Eastern District of Michigan", f"U.S. Court of Appeals for the Sixth Circuit · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (20, "in the uniform", None, "krug_1942.jpg", "20", "The witness", "Krug, under Canadian guard, arrives at court, July 1942 (insignia blurred)", f"Detroit Times, July 1, 1942 · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 0.5]}),
    (23, "On July second", None, "jury_1942.jpg", "23", "The jury", "The Stephan jury, Detroit, July 2, 1942", f"Detroit Times, July 3, 1942 · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (27, "President Roosevelt", None, "fdr_1942.jpg", "27", "Franklin D. Roosevelt", "The President, January 1942", f"U.S. National Archives · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (29, "Max Stephan spent", None, "atlanta_pen.jpg", "29", "U.S. Penitentiary, Atlanta", "Where Stephan served eight years (postcard, 1930s-40s)", f"Boston Public Library · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (32, "The old boys' school", None, "camp30_admin_1941.jpg", "32", "Bowmanville", "Camp 30 is a National Historic Site of Canada since 2013", f"Toronto Public Library · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
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
