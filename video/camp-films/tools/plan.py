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
    "CP": ("controlling_german_pows_1944", 1), "TC": ("tunisian_campaign_1943", 1), "ADC": ("prisoners_shipped_adc140", 1),
    "GH": ("general_hospital_1945", 1), "SR": ("sound_recording_1943", 1), "TIN": ("tuesday_in_november_1945", 1),
    "JS": ("just_a_spark_1937", 1), "AR": ("arteries_nyc_1941", 1), "NN": ("newport_news_1943", 0.8),
    "STK": ("pw_stockade_1945", 1), "RV": ("the_river_1938", 1), "THR": ("threading_projector_1950", 1),
    "BUR": ("movies_burma_1945", 1),
}


def T(m, s=0.0):
    return m * 60 + s

S = {"AR1": T(5, 8.0), "BUR1": T(7, 5.8), "BUR2": T(6, 34.8), "BUR3": T(3, 44.5), "BUR4": T(2, 42.6), "BUR5": T(5, 48.4),
     "THR1": T(2, 22.4), "THR2": T(1, 42.7), "THR3": T(0, 23.2), "THR4": T(1, 2.9), "STK2": T(2, 45.3),
     "NN1": T(2, 34.7), "NN2": T(1, 4.2), "NN3": T(3, 42.7),
     "RV1": T(3, 36.3), "RV2": T(12, 46.8), "RV3": T(2, 57.0), "RV4": T(1, 38.3), "RV5": T(7, 32.2), "RV6": T(0, 19.7),
     "RV7": T(21, 18.0), "RV8": T(2, 17.6), "RV9": T(22, 0.5), "RV10": T(3, 2.0), "RV11": T(6, 52.9)}

KR = "Arnold Krammer, Nazi Prisoners of War in America (1979), p. 228"
NYT = "The New York Times, June 27, 1945, p. 5 · quoted in Arnold Krammer, Nazi Prisoners of War in America (1979)"
GA = "Judith M. Gansberg, Stalag: U.S.A. (1977), p. 127"
RO = "Ron Robin, The Barbed-Wire College (1995)"
HE = "Gerhard H. Hennes, The Barbed Wire: POW in the U.S.A. (2004)"
HN = "Ronald H. Bailey, \"The Secret and Controversial Attempt to Teach German POWs About Freedom,\" HistoryNet (2008)"
DMR = "Des Moines Register, 1945 · reprinted in the Camp Algona POW papers Drahtpost and Lagerzeitung"
GEN = "Convention relative to the Treatment of Prisoners of War, Geneva, July 27, 1929, Art. 17"
CP_TAG = "Stand-in · German prisoners in U.S. Army hands · from Controlling German Prisoners of War (War Dept., 1944)"
TC_TAG = "German prisoners after the surrender in Tunisia, May 1943 · U.S. Army film"
ADC_TAG = "German prisoners board a ship in North Africa, 1943 · U.S. Army film"
GH_TAG = "Stand-in · an Army general hospital · from The General Hospital (War Dept., 1945)"
SR_TAG = "Stand-in · sound film, 1940s · from Sound Recording and Reproduction (Erpi, 1943)"
TIN_TAG = "Stand-in · an American election · from Tuesday in November (OWI, 1945)"
JS_TAG = "Stand-in · fire · from Just a Spark (1937)"
AR_TAG = "Stand-in · a New York ferry, 1941 · from Arteries of New York City"
NN_TAG = "Stand-in · troopships, Newport News, Virginia, 1943 · U.S. Navy film"
STK_TAG = "Stand-in · German prisoners in a U.S. Army enclosure, Austria, 1945 · U.S. Army film"
RV_TAG = "Stand-in · the American South, 1930s · from The River (Farm Security Administration, 1938)"
THR_TAG = "Stand-in · a 16 mm projector · from Threading the 16mm Projector (1950)"
BUR_TAG = "Stand-in · an Army film show (American soldiers), Burma, August 1945 · U.S. Army film"
WC = "Wikimedia Commons"
P = [
    # 0 Halloran
    [("On", "AR", S["AR1"]), ("@", "On the twenty-sixth", AR_TAG),
     ("#", "On the twenty-sixth", None, {"type": "Slug", "title": "June 26, 1945", "subtitle": "Halloran General Hospital · Staten Island, New York"}),
     ("Halloran General Hospital", "GH", T(1, 16.3)), ("@", "Halloran General Hospital", GH_TAG),
     ("The lights went down", "BUR", S["BUR1"]), ("@", "The lights went down", BUR_TAG),
     ("The New York Times", "GH", T(4, 58.3)),
     ("#", "A few men held", None, {"type": "LedgerQuote", "file": "FILE 01 — HALLORAN", "head": "Screening for 150 German prisoners, June 26, 1945",
        "before": "", "key": "a few men held handkerchiefs over their eyes, and one sat with bowed head and with hands tightly covering his ears for most of the film.", "after": "",
        "who": "The New York Times, June 27, 1945", "source": NYT})],
    # 1 headline
    [("The next day's headline", "CP", T(7, 38.0)),
     ("#", "The next day's headline", "Yet that same summer", {"type": "LedgerQuote", "file": "FILE 02 — THE HEADLINE", "head": "The New York Times, June 27, 1945, page 5",
        "before": "", "key": "Germans Are Unmoved by Atrocity Film", "after": ": Prisoners Lay War Crimes to 'Higher-Ups'",
        "who": "Headline, The New York Times", "source": NYT}),
     ("Yet that same summer", "JS", T(5, 21.5)), ("@", "Yet that same summer", JS_TAG), ("They burned their own", "JS", T(4, 55.5))],
    # 2 this is the story
    [("This is the documented", "CP", T(12, 34.5)), ("@", "This is the documented", CP_TAG), ("a father and son", "RV", S["RV1"]), ("@", "a father and son", RV_TAG),
     ("and the survey", "TIN", T(15, 46.1)), ("@", "and the survey", TIN_TAG)],
    # 3 380,000
    [("By the spring", "TC", T(13, 28.4)), ("@", "By the spring", TC_TAG), ("Many had been captured", "TC", T(17, 7.6)),
     ("They picked cotton", "CP", T(11, 33.9)), ("@", "In the evenings", CP_TAG), ("In the evenings", "CP", T(7, 54.0)), ("In some camps", "CP", T(12, 8.7))],
    # 4 Hennes
    [("Gerhard Hennis was one", "TC", T(1, 35.9)), ("@", "Gerhard Hennis was one", TC_TAG),
     ("#", "He was captured in May", None, {"type": "Slug", "title": "May 13, 1943", "subtitle": "Tunisia · the last pocket to surrender"}),
     ("He was captured in May", "TC", T(18, 57.3)), ("and was sent to", "RV", S["RV2"]), ("@", "and was sent to", RV_TAG), ("Years later he admitted", "TC", T(13, 32.0))],
    # 5 father
    [("In nineteen forty-four a prisoner", "CP", T(9, 11.3)), ("@", "In nineteen forty-four a prisoner", CP_TAG),
     ("#", "It was from Major", None, {"type": "LedgerTimeline", "file": "FILE 03 — FATHER AND SON", "head": "Gerhard and Friedrich Hennes",
        "rows": [{"date": "MAY 1943", "text": "Gerhard captured in Tunisia, sent to Crossville, Tennessee"},
                 {"date": "AUG. 1944", "text": "Major Friedrich Hennes captured near Falaise, France; sent to Trinidad, Colorado"},
                 {"date": "1944", "text": "His POW postcard reaches his son"},
                 {"date": "DEC. 1944", "text": "Father reaches Crossville, paying his own fare and his guard's"}],
        "source": f"{HE}, pp. 87–97"}),
     ("They were the only father", "RV", S["RV3"])],
    # 6 the program
    [("In Washington", "TIN", T(8, 40.9)), ("@", "In Washington", TIN_TAG), ("Teaching politics", "CP", T(9, 30.7)), ("@", "Teaching politics", CP_TAG),
     ("#", "so the program borrowed", None, {"type": "LedgerQuote", "file": "FILE 04 — ARTICLE 17", "head": "The Geneva Convention of 1929",
        "before": "", "key": "So far as possible, belligerents shall encourage intellectual diversions and sports organized by prisoners of war.", "after": "",
        "who": "Article 17", "source": f"{GEN} · {HN}"})],
    # 7 the Idea Factory
    [("Its headquarters", "CP", T(9, 11.3)),
     ("#", "Its headquarters", None, {"type": "LedgerTimeline", "file": "FILE 05 — THE IDEA FACTORY", "head": "The secret program",
        "rows": [{"date": "SEPT. 1944", "text": "The War Department approves the program"},
                 {"date": "OCT. 1944", "text": "The Idea Factory opens at Camp Van Etten, New York; later Fort Kearney, R.I."},
                 {"date": "85", "text": "German prisoners on its staff, chosen as anti-Nazis"},
                 {"date": "MAR. 1, 1945", "text": "First issue of Der Ruf (The Call), the camps' paper"}],
        "source": f"{HN}; Krammer (1979), p. 206"}),
     ("Hard-line Nazis called it", "JS", T(5, 4.6)), ("@", "Hard-line Nazis called it", JS_TAG)],
    # 8 the films
    [("Films were part", "THR", S["THR1"]), ("@", "Films were part", THR_TAG), ("and prisoners paid", "THR", S["THR2"]),
     ("#", "and prisoners paid", None, {"type": "Slug", "title": "15 cents a seat", "subtitle": "115 American features approved · no gangsters, no cowboys"}),
     ("The Idea Factory approved", "SR", T(0, 20.0)), ("@", "The Idea Factory approved", SR_TAG), ("Gangster films", "SR", T(0, 33.3))],
    # 9 the footage
    [("Then in the spring", "THR", T(1, 29.4)), ("@", "Then in the spring", THR_TAG),
     ("After Germany surrendered", "THR", S["THR3"]), ("@", "After Germany surrendered", THR_TAG),
     ("#", "On the twelfth of May", None, {"type": "LedgerQuote", "file": "FILE 06 — MAY 1945", "head": "Des Moines Register, May 12, 1945",
        "before": "", "key": "343,000 German prisoners in America watch films", "after": "",
        "who": "Des Moines Register, as reported in the Camp Algona POW paper Drahtpost, June 3, 1945", "source": DMR})],
    # 10 compulsory
    [("Attendance was compulsory", "CP", T(9, 11.3)), ("@", "Attendance was compulsory", CP_TAG), ("and American officers wrote", "GH", T(2, 25.7)), ("@", "and American officers wrote", GH_TAG),
     ("#", "With the films came", None, {"type": "LedgerQuote", "file": "FILE 07 — THE BOOKLET", "head": "Issued with the films, in German (title translated)",
        "before": "", "key": "German Concentration and Prisoner-of-War Camps as the American and British Armies Found Them, April 1945", "after": "",
        "who": "Deutsche Konzentrations- und Gefangenenlager…", "source": GA})],
    # 11 not shown
    [("The footage is still", "SR", T(9, 38.8)), ("What matters in this", "BUR", S["BUR2"]), ("@", "What matters in this", BUR_TAG), ("among men who had fought", "CP", T(12, 5.5)), ("@", "among men who had fought", CP_TAG)],
    # 12 Crossville
    [("At Crossville", "RV", S["RV4"]), ("@", "At Crossville", RV_TAG),
     ("#", "At Crossville", None, {"type": "Slug", "title": "Spring 1945", "subtitle": "Crossville, Tennessee · the movie house outside the wire"}),
     ("Gerhard Hennis described", "BUR", S["BUR3"]), ("@", "Gerhard Hennis described", BUR_TAG),
     ("#", "We saw he wrote", None, {"type": "LedgerQuote", "file": "FILE 08 — CROSSVILLE", "head": "Gerhard Hennes, prisoner at Crossville",
        "before": "", "key": "We saw and stared in silence, struggling but unable to believe what we Germans had done to Jews, gypsies, prisoners of war, and many others deemed inferior or expendable.", "after": "",
        "who": "Gerhard Hennes, The Barbed Wire (2004)", "source": f"{HE}, p. 100"})],
    # 13 hero to villain
    [("He remembered the theater", "BUR", T(7, 9.0)), ("@", "He remembered the theater", BUR_TAG), ("He admitted", "RV", S["RV5"]), ("@", "He admitted", RV_TAG),
     ("#", "That spring day", None, {"type": "LedgerQuote", "file": "FILE 09 — THAT DAY", "head": "Gerhard Hennes, prisoner at Crossville",
        "before": "That day, when spring was at its most beautiful around Crossville, was also the day when I turned in one profound transformation ", "key": "from being a hero to being a villain.", "after": "",
        "who": "Gerhard Hennes, The Barbed Wire (2004)", "source": f"{HE}, p. 101"})],
    # 14 subscribe (midpoint)
    [("If you want more", "RV", S["RV6"]), ("@", "If you want more", RV_TAG),
     ("#", "If you want more", None, {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented", "dur": 6.5})],
    # 15 Butner
    [("At Camp Butner", "CP", T(12, 5.5)), ("@", "the Army showed a film", CP_TAG), ("the Army showed a film", "BUR", S["BUR4"]),
     ("#", "Afterwards according to", None, {"type": "LedgerQuote", "file": "FILE 10 — CAMP BUTNER", "head": "Camp Butner, North Carolina, 1945",
        "before": "", "key": "A thousand men at Camp Butner voluntarily burned their German uniforms.", "after": "",
        "who": "Judith M. Gansberg, Stalag: U.S.A. (1977)", "source": f"{GA}; Krammer (1979), p. 228"}),
     ("The historian Judith", "JS", T(5, 24.5)), ("@", "The historian Judith", JS_TAG)],
    # 16 Eglin, Shelby
    [("It is the most dramatic", "CP", T(11, 42.9)), ("@", "It is the most dramatic", CP_TAG),
     ("#", "At Eglin Field", None, {"type": "Slug", "title": "$2,371", "subtitle": "Eglin Field, Florida · given by prisoners to American war charities"}),
     ("In other camps", "TC", T(6, 10.0)), ("@", "In other camps", TC_TAG),
     ("#", "At Camp Shelby", None, {"type": "LedgerQuote", "file": "FILE 11 — CAMP SHELBY", "head": "Josef K., prisoner at Camp Shelby, Mississippi",
        "before": "We were forced to watch the movies about the concentration camps. This was the first knowledge we had of these things happening. ", "key": "It was hard for the Americans to believe, but we really didn't know.", "after": "",
        "who": "Josef K., as quoted by Judith M. Gansberg", "source": GA})],
    # 17 Clarinda
    [("In Iowa", "TC", T(1, 50.0)), ("@", "In Iowa", TC_TAG), ("They were veterans", "TC", T(11, 11.4)),
     ("#", "The camp spokesman signed", None, {"type": "LedgerTimeline", "file": "FILE 12 — CAMP CLARINDA", "head": "Camp Clarinda, Iowa, summer 1945",
        "rows": [{"date": "225", "text": "prisoners see the film"},
                 {"date": "FIRST", "text": "the camp spokesman signs a letter to Lt. Col. George Ball"},
                 {"date": "THEN", "text": "every man who saw the film signs: the crimes are \"deplorable\""},
                 {"date": "OMAHA", "text": "the letter goes to the 7th Service Command"}],
        "source": "Des Moines Register, July 4, 1945, reprinted in Lagerzeitung (Camp Algona), July 21, 1945"})],
    # 18 Algona
    [("At Camp Algona", "CP", T(9, 30.7)), ("@", "At Camp Algona", CP_TAG),
     ("#", "They wrote that they", None, {"type": "LedgerQuote", "file": "FILE 13 — CAMP ALGONA", "head": "Lagerzeitung, Camp Algona, Iowa, July 21, 1945",
        "before": "", "key": "complete and total solidarity", "after": "",
        "who": "The prisoners of Camp Algona, on the Clarinda letter", "source": DMR})],
    # 19 unmoved
    [("But many audiences", "GH", T(10, 17.4)), ("@", "But many audiences", GH_TAG), ("At Fort Doo-pont", "THR", S["THR4"]), ("@", "At Fort Doo-pont", THR_TAG),
     ("#", "Some of the men think", None, {"type": "LedgerQuote", "file": "FILE 14 — FORT DUPONT", "head": "The projectionist at Fort DuPont, Delaware",
        "before": "", "key": "Some of the men think the bodies in the movie are Germans whom the Russians tortured.", "after": "",
        "who": "A German prisoner, to a reporter, 1945", "source": KR})],
    # 20 propaganda
    [("The Army had expected", "TC", T(11, 38.8)), ("@", "The Army had expected", TC_TAG), ("Gans-berg noted", "BUR", S["BUR5"]), ("@", "Gans-berg noted", BUR_TAG), ("scenes that could not", "CP", T(7, 54.0))],
    # 21 95 percent
    [("By the autumn", "NN", S["NN1"]), ("@", "By the autumn", NN_TAG), ("Suddenly democracy", "TIN", T(1, 35.7)), ("@", "Suddenly democracy", TIN_TAG), ("At Camp Butner the camp", "TIN", T(9, 44.7)),
     ("#", "the prisoners voted ninety-five", None, {"type": "LedgerBars", "file": "FILE 15 — THE VOTE", "head": "Camp Butner, autumn 1945", "max": 100,
        "bars": [{"label": "Prisoners voting in favor of democracy", "value": 95, "figure": "95 %", "note": ""}],
        "source": f"{RO}, p. 102"})],
    # 22 Der Ruf
    [("The prisoner editors", "TIN", T(15, 3.6)),
     ("#", "In an article written", None, {"type": "LedgerQuote", "file": "FILE 16 — DER RUF", "head": "Der Ruf (The Call), article for Nov. 15, 1945, cut before printing",
        "before": "So Camp Butner, North Carolina voted ninety-five percent in favor of democracy, thereby obediently falling into the ranks of a new ideology. ", "key": "Ninety-five percent—it sounds like an old well-known fairy tale. As you know, Goebbels never allowed lower figures.", "after": "",
        "who": "The prisoner editors of Der Ruf", "source": f"{RO}, p. 102"})],
    # 23 the poll
    [("The Army wanted to know", "NN", S["NN2"]), ("@", "The Army wanted to know", NN_TAG), ("it gave an anonymous", "TIN", T(15, 46.1)), ("@", "it gave an anonymous", TIN_TAG),
     ("#", "But only thirty percent", None, {"type": "LedgerBars", "file": "FILE 17 — THE EXIT POLL", "head": "Over 22,000 departing prisoners, 1945–46", "max": 100,
        "bars": [{"label": "Accepted the camp reports as true", "value": 30, "figure": "30 %", "note": ""},
                 {"label": "Placed at least part of the blame on the Jews", "value": 57, "figure": "57 %", "note": ""}],
        "source": f"{RO}, pp. 178–179"})],
    # 24 going home
    [("Many of the prisoners", "ADC", T(5, 16.5)), ("@", "Many of the prisoners", ADC_TAG), ("Gerhard Hennis and his father", "NN", S["NN3"]), ("@", "Gerhard Hennis and his father", NN_TAG),
     ("Before he went", "RV", S["RV7"]), ("@", "Before he went", RV_TAG)],
    # 25 Attichy
    [("They were taken", "STK", S["STK2"]), ("@", "They were taken", STK_TAG), ("In nineteen forty-eight the French", "RV", T(13, 26.1)),
     ("#", "Each of them fell", None, {"type": "LedgerTimeline", "file": "FILE 18 — GOING HOME", "head": "Gerhard and Friedrich Hennes",
        "rows": [{"date": "DEC. 1945", "text": "Leave Crossville"},
                 {"date": "WINTER", "text": "Attichy, France: each falls to about 110 pounds"},
                 {"date": "JAN. 30, 1946", "text": "Released, 13 years to the day after Hitler took power"},
                 {"date": "1948", "text": "Father removed from his pulpit in Koblenz"}],
        "source": f"{HE}, pp. 106–125"})],
    # 26 never recovered
    [("Gerhard went to work", "RV", S["RV8"]), ("@", "Gerhard went to work", RV_TAG),
     ("#", "He wrote that he had", None, {"type": "LedgerQuote", "file": "FILE 19 — AFTER", "head": "Gerhard Hennes, U.S. citizen from 1958",
        "before": "", "key": "I have never totally recovered from the shock sustained in that dark and suddenly uncomfortably hot movie theater in Crossville", "after": "",
        "who": "Gerhard Hennes, The Barbed Wire (2004)", "source": f"{HE}, p. 101"})],
    # 27 comment ask
    [("If someone in your family", "RV", S["RV9"]), ("@", "If someone in your family", RV_TAG),
     ("#", "If someone in your family", None, {"type": "Slug", "title": "Was your family there?", "subtitle": "A prisoner in America, or a camp worker · tell us in the comments"})],
    # 28 the medals
    [("In nineteen sixty-four", "RV", S["RV10"]), ("@", "The guards' barracks", RV_TAG), ("The prisoners' barracks were gone", "RV", S["RV11"]),
     ("#", "For a few minutes", None, {"type": "LedgerQuote", "file": "FILE 20 — CROSSVILLE, 1964", "head": "Gerhard Hennes, back at the camp with his daughters",
        "before": "", "key": "we could not find the medals that I had hidden on that day in Crossville in December 1945.", "after": "",
        "who": "Gerhard Hennes, The Barbed Wire (2004)", "source": f"{HE}, p. 125"})],
]

PHOTOS = [
    (0, "were brought into", None, "halloran_b.jpg", "00", "Halloran General Hospital", "Staten Island, New York · wartime postcard", f"New York Public Library · public domain · {WC}", {}),
    (3, "They picked cotton", None, "wallace_warehouse.jpg", "03", "German prisoners in America", "Camp Wallace, Texas, 1943", f"U.S. Army Signal Corps SC 184881 · public domain · {WC}", {}),
    (4, "Gerhard Hennis was one", None, "wallace_watchmaker.jpg", "04", "Stand-in · a German prisoner", "Camp Wallace, Texas, 1943 (not Hennes)", f"U.S. Army Signal Corps SC 184883 · public domain · {WC}", {}),
    (9, "Army cameramen had filmed", None, "dachau_liberation.jpg", "09", "Dachau, April 29, 1945", "Survivors cheer approaching U.S. troops", f"USHMM photograph 45075 · public domain · {WC}", {}),
    (15, "At Camp Butner", None, "butner_postcard.jpg", "15", "Camp Butner, North Carolina", "Wartime Signal Corps postcard of the camp's Army hospital", f"State Archives of North Carolina · no known restrictions · {WC}", {}),
    (19, "At Halloran the Times", None, "halloran_c.jpg", "19", "Halloran General Hospital", "Staten Island · wartime postcard", f"New York Public Library · public domain · {WC}", {}),
    (24, "They were handed over", None, "pows_normandy_farm.jpg", "24", "Prisoners as laborers in France", "German prisoners farming in Normandy, May 1945", f"U.S. Army · National Archives · public domain · {WC}", {}),
    (28, "In nineteen sixty-four", None, "crossville_main.jpg", "28", "Crossville, Tennessee, today", "South Main Street, 2016", f"Brian Stansberry · CC BY 4.0 · {WC}", {}),
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
