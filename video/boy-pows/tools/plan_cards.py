# Boy POWs: films, tags and cards. exec()'d by tools/plan.py. No 3D (owner, 25 Nov 2026); nothing on screen more than twice.
F = {
    "PS": ("prisoners_shipped_adc140", 1), "TT": ("troop_train_1943", 1), "CH": ("prisoners_cherbourg_1944", 1),
    "NA": ("prisoners_naples_1943", 1), "IT": ("prisoners_italy_1945", 1), "LG": ("logging_1950", 1),
}
WC = "Wikimedia Commons"
STAND = "Stand-in · "
TAG = {
    "PS": "German prisoners shipped to the U.S. from North Africa · Signal Corps film (NARA 111-ADC-140)",
    "TT": STAND + "'Troop Train', U.S. government film, 1943",
    "CH": "German prisoners, Cherbourg, Normandy, 28 June 1944 · Signal Corps film (NARA ADC-1395)",
    "NA": "German prisoners taken to Naples, Italy, Dec 1943 · U.S. Navy film (NARA NPC-1533)",
    "IT": "German prisoners, Italy, April 1945 · Signal Corps film (NARA ADC-4101)",
    "LG": STAND + "logging in the woods, c. 1950 (archive.org, public domain)",
}
NPR = "Hank Welzel, NPR All Things Considered, 11 Nov 2010"
STRIPES = "Stars and Stripes / Bangor Daily News, 27 Jul 2021"
AMERICA = "America magazine, 11 Dec 2006"

FLO = [11.26, 43.85]; ALA = [-85.72, 31.36]; NOR = [-1.3, 49.3]; HOU = [-67.84, 46.13]
ROUTES = {"type": "GlobeMap", "theme": "history",
          "cam": [{"t": 0, "center": [-30, 42], "scale": 1.6}, {"t": 0.55, "center": [-40, 44], "scale": 1.7}],
          "pins": [{"ll": FLO, "label": "Florence, Italy", "at": 0.1, "color": "amber"},
                   {"ll": ALA, "label": "Alabama", "at": "shipped across the Atlantic", "color": "red", "below": True},
                   {"ll": NOR, "label": "Normandy", "at": 0.6, "color": "amber", "below": True},
                   {"ll": HOU, "label": "Houlton, Maine", "at": 0.6, "color": "red"}],
          "arcs": [{"from": FLO, "to": ALA, "at": "shipped across the Atlantic", "style": "dashed", "color": "amber", "loft": 0.12, "draw": 50},
                   {"from": NOR, "to": HOU, "at": 0.6, "style": "dashed", "color": "red", "loft": 0.10, "draw": 45}],
          "footer": "Routes generalised · " + NPR + " · " + AMERICA, "year": {"at": 0.1, "year": "1944", "sub": "Two boys"}}

GRAVE = QC("stills/aroostook_after.jpg", [("One soldier, just 15, broke out in tears", "started to cry"),
                                         ("when asked to dig a latrine pit.", "When the guard asked"),
                                         ("He said he had believed he was digging his own grave.", "digging his own grave")],
           STRIPES, "digging his own grave")
GERMAN = QC("stills/boy_pow_crying.jpg", [("You had to consider yourself a German", "You had to consider"),
                                          ("if you wanted to stay alive.", "wanted to stay alive")], NPR, "wanted to stay alive")
SECRET = QC("stills/pows_dadecity.jpg", [("I never told anybody", "He never told anybody"), ("that I was an American citizen by birth.", "It was his highest secret"),
                                         ("That was my secret.", "It was his highest secret")], NPR, "It was his highest secret")
BEST = QC("stills/aroostook_farm2.jpg", [("The best years of my life were spent", "The best years of my life"),
                                         ("in a prison camp behind barbed wire.", "in a prison camp"),
                                         ("It was the consequence of a senseless war that Germany had started,", "senseless war"),
                                         ("for which we were shamelessly misused.", "shamelessly misused")],
          "Gerhard Kleindt, former prisoner at Camp Houlton · " + AMERICA, "shamelessly misused")
HOULTON = BIG(3500, "German prisoners held at Camp Houlton, Maine, 1944-1946", STRIPES)
SLUG_H = SLUG("Camp Houlton · Aroostook County, Maine", "German prisoners of war, 1944-1946")
