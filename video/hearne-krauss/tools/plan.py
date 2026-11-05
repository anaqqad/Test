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
    "NYW": ("around_the_world_in_new_york_1940", 1), "ART": ("arteries_of_new_york_1941", 1), "TT": ("troop_train_1943", 1),
    "CML": ("children_must_learn_1940", 1), "RIV": ("the_river_1937", 1), "COT": ("cotton_cultivation_1937", 1),
    "BAL": ("cotton_bales_1937", 1), "TUN": ("tunisian_campaign_1943", 1), "ADC": ("prisoners_shipped_adc140", 1),
    "CP": ("controlling_german_pows_1944", 1), "HOS": ("general_hospital_1945", 1), "MEM": ("memorial_day_1945", 1),
    "GAS": ("modern_gasoline_1946", 1),
}


def T(m, s=0.0):
    return m * 60 + s

WAT = "Michael R. Waters et al., Lone Star Stalag (Texas A&M University Press, 2004)"
GER = "William Geroux, The Fifteen (Random House, 2026)"
WPH = "Wikipedia, “Camp Hearne”"
ETH = "Rachael Larkin, “Hearne Prisoner of War Camp,” East Texas History"
WPG = "Wikipedia, “German prisoners of war in the United States”"
KBTX = "KBTX News, Dec. 10, 2024"
NYW_TAG = "New York, 1940 · from Around the World in New York"
ART_TAG = "New York, 1941 · from Arteries of New York City"
ARTS_TAG = "Stand-in · from Arteries of New York City (1941)"
TT_TAG = "Stand-in · from Troop Train (OWI, 1943)"
CML_TAG = "Stand-in · from The Children Must Learn (1940)"
RIV_TAG = "Stand-in · cotton country · from The River (FSA, 1937)"
RIVS_TAG = "Stand-in · from The River (FSA, 1937)"
WH_TAG = "The White House, 1945 · Universal Newsreel"
SHIP_TAG = "Stand-in · a transport ship · U.S. Army film, c. 1943"
NIGHT_TAG = "Stand-in · sleeping berths at night · from Troop Train (OWI, 1943)"
TUNS_TAG = "Stand-in · German prisoners in Tunisia, May 1943 · U.S. Army film"
WAR_TAG = "Stand-in · war damage, Tunisia, 1943 · U.S. Army film"
COT_TAG = "Stand-in · a cotton field, 1937"
BAL_TAG = "Stand-in · cotton bales, 1937"
TUN_TAG = "Tunisia, May 1943 · German prisoners after the surrender · U.S. Army film"
ADC_TAG = "German prisoners from North Africa board ships · U.S. Army film, c. 1943"
ADCD_TAG = "Stand-in · North Africa · U.S. Army film, c. 1943"
CP_TAG = "Stand-in · from Controlling German Prisoners of War (U.S. Army, 1944)"
HOS_TAG = "Stand-in · an Army hospital · from The General Hospital (1945)"
MEM_TAG = "Stand-in · a national cemetery, Memorial Day 1945"
GAS_TAG = "Stand-in · a country road · from Modern Gasoline (1946)"
P = [
    # 0 the visit
    [("In", "TT", T(10, 18.2)), ("@", "In nineteen forty-three", TT_TAG),
     ("#", "In nineteen forty-three", None, {"type": "Slug", "title": "1943", "subtitle": "A prisoner of war camp in Texas · visitors from New York"}),
     ("a prison camp in the cotton country", "COT", T(0, 3.0)), ("@", "a prison camp in the cotton country", COT_TAG),
     ("They had come to see", "ART", T(4, 2.4)), ("@", "They had come to see", ARTS_TAG), ("He was a corporal", "TUN", T(13, 1.7)), ("@", "He was a corporal", TUN_TAG)],
    # 1 the presents
    [("They brought him presents", "ART", T(2, 51.5)), ("@", "They brought him presents", ARTS_TAG), ("A sewing machine", "NYW", T(1, 13.2)),
     ("And a radio", "CML", T(5, 14.0)), ("@", "And a radio", CML_TAG), ("In the barracks around him", "TUN", T(13, 8.3)), ("@", "In the barracks around him", TUNS_TAG),
     ("Most of them did not like", "TUN", T(16, 12.8))],
    # 2 the night
    [("On the night of December", "TT", T(9, 5.8)), ("@", "On the night of December", NIGHT_TAG),
     ("#", "On the night of December", None, {"type": "Slug", "title": "December 17, 1943", "subtitle": "Camp Hearne, Texas · about 11:45 p.m."}),
     ("men with clubs walked", "TT", T(9, 22.2)), ("The attack lasted", "TT", T(9, 8.2)), ("Nobody in the room", "TT", T(9, 12.8))],
    # 3 documented story
    [("This is the documented story", "ART", T(0, 41.4)), ("@", "This is the documented story", ART_TAG), ("who came back to America", "ADC", T(5, 16.5)),
     ("@", "who came back to America", ADC_TAG), ("of the men who killed him", "TUN", T(13, 21.7)), ("and of a stranger on a Texas road", "GAS", T(14, 24.8)),
     ("@", "and of a stranger on a Texas road", GAS_TAG)],
    # 4 Yorkville
    [("Hugo Krauss was born", "NYW", T(0, 8.1)), ("When he was nine", "ART", T(5, 13.4)), ("@", "When he was nine", ART_TAG),
     ("in Yorkville", "NYW", T(7, 43.9)), ("@", "in Yorkville", NYW_TAG),
     ("#", "Hugo Krauss was born", "He went to school there", {"type": "LedgerTimeline", "file": "FILE 01 — HUGO KRAUSS", "head": "From Yorkville to Texas",
        "rows": [{"date": "1919", "text": "Born in Germany"},
                 {"date": "AGE 9", "text": "To New York with his family; Yorkville, Manhattan"},
                 {"date": "1939", "text": "Sails back to Germany, at nineteen"},
                 {"date": "1943", "text": "Captured in Tunisia; a prisoner of war in Texas"}],
        "source": WAT + "; " + GER}),
     ("He went to school there", "ART", T(6, 0.7)), ("He grew up speaking English", "NYW", T(6, 6.2))],
    # 5 1939
    [("In nineteen thirty-nine", "ART", T(5, 13.4)), ("@", "In nineteen thirty-nine", ART_TAG), ("A pro-Nazi group", "ART", T(0, 53.2)),
     ("One history says", "NYW", T(5, 33.7)),
     ("#", "Why he went", None, {"type": "LedgerQuote", "file": "FILE 02 — 1939", "head": "Why did he go?",
        "before": "", "key": "It's unclear what was going on in the young man's head at that point.", "after": "",
        "who": "William Geroux, historian", "source": GER})],
    # 6 the war
    [("Then the war began", "TUN", T(19, 52.1)), ("@", "Then the war began", WAR_TAG), ("At first he got out of it", "TUN", T(20, 19.5)),
     ("He fought in Russia", "TUN", T(7, 59.6)), ("and then in North Africa", "ADC", T(4, 21.0)), ("@", "and then in North Africa", ADCD_TAG)],
    # 7 captured
    [("In the spring of", "TUN", T(0, 13.7)), ("@", "In the spring of", TUN_TAG), ("Krauss was captured", "TUN", T(12, 6.2)),
     ("Less than four years", "ADC", T(5, 16.5)), ("@", "Less than four years", ADC_TAG), ("this time as a prisoner of war", "ADC", T(7, 40.9))],
    # 8 Hearne
    [("He was sent to a town", "TT", T(10, 31.8)), ("@", "He was sent to a town", TT_TAG), ("sixty-five miles", "RIV", T(3, 38.8)), ("@", "sixty-five miles", RIV_TAG),
     ("About three thousand five hundred", "BAL", T(0, 15.1)), ("@", "About three thousand five hundred", BAL_TAG),
     ("#", "About three thousand five hundred", None, {"type": "LedgerTimeline", "file": "FILE 03 — HEARNE, TEXAS", "head": "The town, 1943",
        "rows": [{"date": "65 MILES", "text": "Southeast of Waco, on the Brazos River bottomland"},
                 {"date": "3,500", "text": "People"},
                 {"date": "2 + 2", "text": "Cotton gins and railroad lines"}],
        "source": GER})],
    # 9 the camp
    [("On the edge of town", "TUN", T(16, 12.8)), ("@", "On the edge of town", TUNS_TAG), ("The first men", "TUN", T(13, 25.0)), ("@", "The first men", TUN_TAG),
     ("At its peak", "TUN", T(13, 35.0)),
     ("#", "At its peak", None, {"type": "LedgerTimeline", "file": "FILE 04 — CAMP HEARNE", "head": "One of the largest camps in America",
        "rows": [{"date": "JUNE 3, 1943", "text": "The first Afrika Korps prisoners arrive"},
                 {"date": "ABOUT 4,800", "text": "Prisoners at its peak"},
                 {"date": "3", "text": "Compounds, and a hospital, on 711 acres"}],
        "source": ETH + "; Tex Appeal (2023)"})],
    # 10 the Fritz Ritz
    [("Life there was not hard", "TUN", T(6, 33.5)), ("@", "Life there was not hard", TUNS_TAG), ("They built small castles", "TUN", T(13, 50.0)),
     ("They picked cotton", "RIV", T(22, 52.4)), ("@", "They picked cotton", RIV_TAG), ("Some people in town", "BAL", T(0, 28.0))],
    # 11 the Nazis
    [("But inside the compounds", "TUN", T(16, 12.8)), ("@", "But inside the compounds", TUNS_TAG), ("Prisoners who doubted", "TUN", T(13, 41.7)),
     ("#", "Those who did not", None, {"type": "LedgerQuote", "file": "FILE 05 — THE HOLY GHOST", "head": "Inside the compounds",
        "before": "Afrika Korps members held ", "key": "secret kangaroo courts for those accused of disloyalty", "after": ".",
        "who": "On the hard Nazis in American camps", "source": WPG}),
     ("Those who did not", "TT", T(9, 24.5)), ("@", "Those who did not", NIGHT_TAG)],
    # 12 the interpreter
    [("Hugo Krauss did not keep quiet", "TUN", T(14, 11.7)), ("@", "Hugo Krauss did not keep quiet", TUNS_TAG), ("He spoke perfect English", "TUN", T(14, 8.3)), ("@", "He spoke perfect English", TUNS_TAG),
     ("He told the other prisoners", "TUN", T(13, 5.0)),
     ("#", "He told the other prisoners", None, {"type": "LedgerQuote", "file": "FILE 06 — THE INTERPRETER", "head": "What Krauss told the others",
        "before": "He told them he ", "key": "had no intention of going back to Germany", "after": ", which he said was certain to lose the war.",
        "who": "William Geroux, historian", "source": GER})],
    # 13 Christmas
    [("He said he would get leave", "TT", T(6, 27.2)), ("@", "He said he would get leave", TT_TAG),
     ("#", "He said he would get leave", "When his company sang", {"type": "LedgerQuote", "file": "FILE 07 — CHRISTMAS", "head": "From the Army's report",
        "before": "He told his fellow prisoners ", "key": "he was going to get a Christmas furlough to visit his parents in New York", "after": " …",
        "who": "U.S. Army report, 1945, as quoted by Michael R. Waters", "source": WAT}),
     ("When his company sang", "TUN", T(13, 45.0)), ("@", "When his company sang", TUNS_TAG)],
    # 14 sewing machine, radio
    [("He had a sewing machine", "NYW", T(1, 29.5)), ("@", "He had a sewing machine", NYW_TAG), ("And he had his radio", "CML", T(5, 14.0)), ("@", "And he had his radio", CML_TAG),
     ("He listened to American news", "ART", T(3, 3.3)), ("@", "He listened to American news", ARTS_TAG)],
    # 15 Erichsen
    [("A man in his barracks", "TT", T(9, 15.2)), ("@", "A man in his barracks", NIGHT_TAG),
     ("#", "A man in his barracks", None, {"type": "LedgerQuote", "file": "FILE 08 — THE VISITORS", "head": "A prisoner in the same barracks",
        "before": "I knew there was antagonism because ", "key": "he had American relatives who visited him in camp", "after": ".",
        "who": "Heino Erichsen, interpreter, Camp Hearne", "source": WAT}),
     ("and some of the prisoners said", "TUN", T(13, 11.7))],
    # 16 the army's verdict
    [("The army later put it simply", "CP", T(8, 52.0)), ("@", "The army later put it simply", CP_TAG),
     ("#", "Krauss was very much disliked", None, {"type": "LedgerQuote", "file": "FILE 09 — THE ARMY'S VIEW", "head": "U.S. Army, 1944",
        "before": "", "key": "He was very much disliked and was considered a traitor to Germany,", "after": " especially by the younger prisoners of war who were devout Hitlerites.",
        "who": "Letter of the assistant provost marshal general", "source": WAT + "; " + GER})],
    # 17 the slowdown
    [("By December", "TUN", T(16, 12.8)), ("@", "By December", TUNS_TAG), ("Some German sergeants", "CP", T(6, 17.2)), ("The Nazis believed", "TUN", T(13, 15.0)),
     ("#", "Some German sergeants", None, {"type": "LedgerTimeline", "file": "FILE 10 — DECEMBER 1943", "head": "What the Nazis held against him",
        "rows": [{"date": "THE SLOWDOWN", "text": "Sergeants behind work slowdowns are moved out; Krauss is blamed"},
                 {"date": "THE RADIO", "text": "Guards seize a hidden shortwave set; Krauss is blamed"}],
        "source": WAT + "; " + GER})],
    # 18 the radio
    [("Then the guards found", "TT", T(9, 19.8)), ("@", "Then the guards found", NIGHT_TAG), ("The Americans took it away", "TUN", T(14, 11.7)), ("The prisoners blamed", "TUN", T(13, 28.3))],
    # 19 Boehmer
    [("On December seventeenth", "TUN", T(13, 31.7)), ("@", "On December seventeenth", TUNS_TAG), ("stood in front of the men", "TUN", T(13, 38.3)),
     ("#", "stood in front of the men", None, {"type": "LedgerQuote", "file": "FILE 11 — THE ANNOUNCEMENT", "head": "December 17, 1943",
        "before": "", "key": "We have a man in our ranks who is disloyal to the cause", "after": " …",
        "who": "The company's ranking sergeant, as recalled by prisoner Hans Schiller (affidavit, 1945)", "source": WAT})],
    # 20 let them come
    [("Krauss heard", "TT", T(9, 12.8)), ("@", "Krauss heard", NIGHT_TAG),
     ("#", "Let them come", None, {"type": "LedgerQuote", "file": "FILE 12 — HIS ANSWER", "head": "Overheard in Barracks 1",
        "before": "", "key": "Let them come. I am not afraid.", "after": "",
        "who": "Hugo Krauss, as heard by Guenther Meisel (affidavit, 1945)", "source": WAT})],
    # 21 the plan
    [("That evening", "TT", T(9, 15.2)), ("@", "That evening", NIGHT_TAG), ("They had sticks", "TT", T(9, 17.5)),
     ("#", "They had sticks", None, {"type": "LedgerTimeline", "file": "FILE 13 — THE PLAN", "head": "Barracks 4, by candlelight",
        "rows": [{"date": "WEAPONS", "text": "Sticks, some with spikes driven through; a piece of pipe"},
                 {"date": "LOOKOUTS", "text": "Posted to watch the guard towers"},
                 {"date": "THE LIGHTS", "text": "One man to turn them off"},
                 {"date": "AFTER", "text": "Bury the sticks"}],
        "source": WAT + "; " + GER}),
     ("Lookouts went out", "TT", T(9, 22.2))],
    # 22 a quarter to midnight
    [("At about a quarter to midnight", "TT", T(9, 5.8)), ("@", "At about a quarter to midnight", NIGHT_TAG), ("The lights went out", "TT", T(9, 29.2)),
     ("Krauss was in his bunk", "TT", T(9, 22.2))],
    # 23 Erichsen remembers
    [("was in the same barracks", "TT", T(9, 12.8)), ("@", "was in the same barracks", NIGHT_TAG),
     ("#", "He remembered the noise", None, {"type": "LedgerQuote", "file": "FILE 14 — THAT NIGHT", "head": "A prisoner in Barracks 1",
        "before": "", "key": "There was a lot of noise and the lights went out", "after": " and there was a scuffle and screaming and beating, and it didn't take that long.",
        "who": "Heino Erichsen, interpreter, Camp Hearne", "source": WAT}),
     ("Krauss cried out", "TT", T(9, 8.2))],
    # 24 the wounds
    [("His skull was broken", "HOS", T(4, 58.3)), ("@", "His skull was broken", HOS_TAG),
     ("#", "His skull was broken", None, {"type": "LedgerTimeline", "file": "FILE 15 — THE MEDICAL RECORD", "head": "Cpl. Hugo Krauss, December 1943",
        "rows": [{"date": "SKULL", "text": "Fractured in three places"},
                 {"date": "ARMS", "text": "Left forearm snapped; right arm broken at the elbow"},
                 {"date": "DEC. 18", "text": "Moved to McCloskey General Hospital, Temple, Texas"},
                 {"date": "DEC. 23", "text": "Dies, a month short of his 25th birthday"}],
        "source": WAT}),
     ("and the next day", "HOS", T(6, 21.6)), ("He died there", "HOS", T(7, 58.7))],
    # 25 rumors
    [("Years later", "TUN", T(16, 12.8)), ("@", "Years later", TUNS_TAG),
     ("#", "The historians who studied", None, {"type": "LedgerQuote", "file": "FILE 16 — THE RUMORS", "head": "On the guards' stories",
        "before": "", "key": "the medical report and autopsy photographs show that this did not actually happen", "after": "",
        "who": "Michael R. Waters and his co-authors", "source": WAT})],
    # 26 the silence
    [("The Army investigated", "TT", T(2, 9.1)), ("@", "The Army investigated", TT_TAG), ("Almost fifty prisoners", "TUN", T(13, 1.7)),
     ("#", "Almost fifty prisoners", None, {"type": "Slug", "title": "December 1943 – mid-1945", "subtitle": "Almost fifty prisoners questioned · no one is named"}),
     ("Nobody named anyone", "TUN", T(13, 48.3)), ("asked to be transferred", "TT", T(6, 27.2)), ("@", "asked to be transferred", TT_TAG)],
    # 27 the father
    [("In New York", "ART", T(0, 41.4)), ("@", "In New York", ART_TAG),
     ("#", "He was a citizen", None, {"type": "LedgerQuote", "file": "FILE 17 — THE FATHER", "head": "Henry Krauss to the Army, New York, 1943",
        "before": "", "key": "As a citizen of the United States, I would like a further investigation made", "after": " and all details sent to me.",
        "who": "Henry Krauss, Hugo's father", "source": WAT})],
    # 28 the answer
    [("The answer came", "TT", T(1, 41.9)), ("@", "The answer came", TT_TAG),
     ("#", "His son's attitude", "The men who attacked him", {"type": "LedgerQuote", "file": "FILE 18 — THE ANSWER", "head": "The Army to Henry Krauss, 1944",
        "before": "Your son's attitude and conduct, ", "key": "praiseworthy from an American viewpoint", "after": ", incurred for him the enmity of other German prisoners of war …",
        "who": "U.S. Army letter", "source": WAT}),
     ("The men who attacked him", "TUN", T(13, 18.3)), ("@", "The men who attacked him", TUNS_TAG)],
    # 29 1945
    [("In January", "ART", T(3, 3.3)), ("@", "In January", ARTS_TAG),
     ("#", "In January", None, {"type": "Slug", "title": "January 16, 1945", "subtitle": "The New York Times: “Ex-Yorkville Man Slain as Prisoner”"}),
     ("The war in Europe ended", "MEM", T(1, 22.0)), ("The case was still open", "CP", T(8, 52.0)), ("@", "The case was still open", CP_TAG)],
    # 30 Meisel
    [("One of the attackers", "TUN", T(11, 11.4)), ("@", "One of the attackers", TUNS_TAG), ("he worked in the truck workshop", "TUN", T(17, 7.6)),
     ("and the Army trusted him", "GAS", T(11, 34.7)), ("@", "and the Army trusted him", GAS_TAG)],
    # 31 the road
    [("One afternoon", "GAS", T(14, 24.8)), ("@", "One afternoon", GAS_TAG),
     ("#", "he saw a young woman", "Before they drove off", {"type": "LedgerQuote", "file": "FILE 19 — THE ROAD", "head": "Guenther Meisel, as told to a fellow prisoner",
        "before": "I noticed a young girl on the side of the road; ", "key": "the bonnet [hood] of her car was open and she was obviously in trouble", "after": ".",
        "who": "Recalled by Fritz Haus", "source": WAT}),
     ("He stopped and fixed", "GAS", T(19, 8.4)), ("Before they drove off", "GAS", T(11, 34.7))],
    # 32 the letters
    [("At first he told her", "GAS", T(11, 34.7)), ("@", "At first he told her", GAS_TAG), ("In his first letter", "CP", T(8, 52.0)), ("@", "In his first letter", CP_TAG),
     ("She wrote back anyway", "CP", T(8, 55.0)), ("She was a Christian", "CML", T(10, 3.9)), ("@", "She was a Christian", CML_TAG)],
    # 33 the cotton field
    [("He arranged to be sent out", "RIV", T(22, 52.4)), ("@", "He arranged to be sent out", RIV_TAG), ("And one day", "COT", T(0, 11.3)), ("@", "And one day", COT_TAG)],
    # 34 the confession
    [("She told him he had to confess", "RIV", T(22, 58.0)), ("He fought it", "TT", T(9, 15.2)), ("@", "He fought it", NIGHT_TAG),
     ("Then, near the end of", "TUN", T(14, 23.2)), ("@", "Then, near the end of", TUNS_TAG),
     ("#", "The officer asked him", None, {"type": "LedgerQuote", "file": "FILE 20 — THE CONFESSION", "head": "Guenther Meisel, 1945",
        "before": "He asked, did I realize what I was saying and doing to myself? ", "key": "Yes, I knew.", "after": "",
        "who": "Meisel's own account, as told to Fritz Haus", "source": WAT})],
    # 35 the trial
    [("named the others", "CP", T(8, 52.0)), ("@", "named the others", CP_TAG), ("In January", "TT", T(2, 9.1)), ("@", "In January", TT_TAG), ("before an American military court", "ART", T(8, 34.4)),
     ("#", "In January", None, {"type": "Slug", "title": "January 22–30, 1946", "subtitle": "Court-martial of seven German prisoners · Camp Swift, near Bastrop, Texas"}),
     ("for the murder of", "TT", T(1, 28.3))],
    # 36 the prosecutor
    [("The prosecutor told the court", "TT", T(2, 9.1)), ("@", "The prosecutor told the court", TT_TAG),
     ("#", "The prosecutor told the court", None, {"type": "LedgerQuote", "file": "FILE 21 — THE PROSECUTION", "head": "Closing argument, 1946",
        "before": "", "key": "There are two of the accused who have been of assistance to me in the breaking of this case.", "after": "",
        "who": "The prosecutor, Camp Swift court-martial", "source": WAT})],
    # 37 the verdict
    [("After more than two hours", "TT", T(1, 28.3)), ("@", "After more than two hours", TT_TAG),
     ("#", "After more than two hours", None, {"type": "LedgerTimeline", "file": "FILE 22 — THE VERDICT", "head": "Camp Swift, January 30, 1946",
        "rows": [{"date": "7", "text": "German prisoners on trial"},
                 {"date": "2+ HOURS", "text": "Of deliberation"},
                 {"date": "ALL 7", "text": "Guilty of murder"},
                 {"date": "LIFE", "text": "In prison, at hard labor"}],
        "source": WAT}),
     ("They were sent to", "TT", T(6, 27.2))],
    # 38 shrinking sentences
    [("Then the sentences began", "TT", T(1, 41.9)), ("@", "Then the sentences began", TT_TAG),
     ("#", "Then the sentences began", None, {"type": "LedgerTimeline", "file": "FILE 23 — THE SENTENCES", "head": "Leavenworth, 1946-1949",
        "rows": [{"date": "DEC. 1946", "text": "Two convictions thrown out; Meisel cut to 15 years, four others to 10"},
                 {"date": "1948", "text": "President Truman cuts Meisel's sentence to 10 years"},
                 {"date": "1949", "text": "All five paroled and sent home to Germany"}],
        "source": WAT + "; " + WPH}),
     ("In nineteen forty-eight", "MEM", T(4, 58.3)), ("@", "In nineteen forty-eight", WH_TAG)],
    # 39 home
    [("In nineteen forty-nine", "ADC", T(5, 16.5)), ("@", "In nineteen forty-nine", SHIP_TAG), ("They had spent about", "TT", T(10, 25.0)), ("@", "They had spent about", TT_TAG),
     ("#", "Fourteen German prisoners", None, {"type": "LedgerQuote", "file": "FILE 24 — THE OTHERS", "head": "Other camp murders",
        "before": "The U.S. military ", "key": "executed 14 Germans after the war for murdering three fellow prisoners", "after": ".",
        "who": "German prisoners of war in the United States", "source": WPG}),
     ("The men who killed", "TT", T(10, 18.2))],
    # 40 the grave
    [("Hugo Krauss was buried", "MEM", T(1, 58.4)), ("@", "Hugo Krauss was buried", MEM_TAG), ("After the war", "MEM", T(0, 27.3)), ("to a section with", "MEM", T(0, 29.0))],
    # 41 the camp today
    [("closed in nineteen forty-six", "RIV", T(21, 32.9)), ("@", "closed in nineteen forty-six", RIVS_TAG), ("The buildings were sold off", "RIV", T(7, 37.5))],
    # 42 scene of the crime
    [("There is also a trail", "RIV", T(1, 39.5)), ("@", "There is also a trail", RIVS_TAG),
     ("#", "Its program director", None, {"type": "LedgerQuote", "file": "FILE 25 — HIS SIDE", "head": "Camp Hearne museum",
        "before": "", "key": "He was done with Nazi Germany.", "after": "",
        "who": "Melissa Freeman, program director, Camp Hearne", "source": KBTX})],
    # 43 comment ask
    [("If your family", "RIV", T(3, 38.8)), ("@", "If your family", RIVS_TAG),
     ("#", "If your family", None, {"type": "Slug", "title": "Texas camps, 1943–46, in your family's story?", "subtitle": "Tell us in the comments"})],
    # 44 echo
    [("In San Antonio", "MEM", T(0, 27.3)), ("@", "In San Antonio", MEM_TAG), ("One visitor who found it", "MEM", T(1, 58.4))],
]

WC = "Wikimedia Commons"
PHOTOS = [
    (4, "in Yorkville", None, "yorkville_view.jpg", "04", "Yorkville, Manhattan", "The German neighborhood of New York, seen from 86th Street, today", f"CC BY-SA 3.0 · {WC}", {"crop": [0.0, 0.1, 1.0, 0.75]}),
    (7, "this time as a prisoner of war", None, "pows_jervis_1943.jpg", "07", "Off Tunisia, May 1943", "German prisoners aboard HMS Jervis (badges blurred)", f"Imperial War Museum A16824 · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (8, "He was sent to a town", None, "hearne_station.jpg", "08", "Hearne, Texas", "The railroad station", f"no known restrictions · {WC}", {"crop": [0.0, 0.15, 1.0, 0.7]}),
    (10, "They built small castles", None, "camp_wallace_a.jpg", "10", "Another Texas camp, 1943", "Stand-in: German prisoners at Camp Wallace, Texas, on a mowing detail", f"U.S. Army Signal Corps · NARA · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (14, "He had a sewing machine", None, "camp_wallace_c.jpg", "14", "Prisoners at work, Texas, 1943", "Stand-in: two German prisoners repair typewriters at Camp Wallace", f"U.S. Army Signal Corps · NARA · public domain · {WC}", {"crop": [0.0, 0.05, 1.0, 0.85]}),
    (35, "for the murder of", None, "camp_swift_1944.jpg", "35", "Camp Swift, Texas", "The main entrance, August 6, 1944. The court-martial met here in January 1946.", f"U.S. Army · public domain · {WC}", {"crop": [0.0, 0.0, 1.0, 1.0]}),
    (37, "They were sent to", None, "leavenworth.jpg", "37", "Leavenworth, Kansas", "The U.S. Penitentiary", f"public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.75]}),
    (40, "After the war", None, "fort_sam_cemetery.jpg", "40", "Fort Sam Houston National Cemetery", "San Antonio, Texas, where Krauss lies among other German prisoners of war", f"public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
    (41, "Today there is a museum", None, "camp_hearne_museum.png", "41", "Camp Hearne today", "The rebuilt barracks that houses the museum", f"CC BY-SA 4.0 · {WC}", {"crop": [0.0, 0.3, 1.0, 0.32]}),
    (44, "One visitor who found it", None, "fort_sam_volkstrauertag_2023.jpg", "44", "Fort Sam Houston, November 2023", "German Memorial Day among the German prisoners' graves", f"U.S. Army · public domain · {WC}", {"crop": [0.0, 0.1, 1.0, 0.8]}),
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
