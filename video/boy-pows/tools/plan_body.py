# Boy POWs: shots per paragraph and archive prints. exec()'d by tools/plan.py after plan_cards.py.
# CH: avoid 0-6 slate, 20-40 / 92-106 close-ups with cap eagles, 70-82 chalk slate, 128+ end. IT: avoid 0-45 / 128-205 haze,
# 113-126 officer with breast eagle. LG: colour film shown grey; woods only. Naples reel not used (burned-in timecode).

P = [
    # 0
    sh("In the woods of northern Maine", "LG", 312.0) + sh("The prisoner was fifteen", "LG", 387.0, False),
    # 1
    sh("He started to dig", "LG", 262.0) + card("He started to dig", GRAVE),
    # 2
    sh("It was a latrine pit", "LG", 112.0),
    # 3
    sh("This is the documented story", "IT", 52.0) + sh("what they had been told", "IT", 62.0, False),
    # 4
    sh("By nineteen forty-four", "IT", 210.0) + sh("At the camp in Houlton", "IT", 218.0, False),
    # 5
    sh("One of them was Gerhard", "CH", 56.0) + sh("Before he was captured", "CH", 44.0),
    # 6
    sh("One night his convoy", "CH", 110.0) + sh("Instead, American soldiers", "CH", 120.0) + sh("They took him in", "CH", 50.0) +
    sh("The Americans, he said", "CH", 63.0),
    # 7
    sh("Another boy was Hank", "IT", 84.0) + sh("He was trained as a medic", "IT", 236.0, False),
    # 8
    sh("Welzel had a secret", "IT", 245.0) + card("You had to consider", GERMAN),
    # 9
    sh("On October the tenth", "IT", 225.0) + sh("Now he faced", "IT", 255.0, False),
    # 10
    sh("He did not", "IT", 262.0) + card("He never told anybody", SECRET),
    # 11
    sh("He was shipped across", "PS", 330.0) + card("He was shipped across", ROUTES),
    # 12
    sh("Kleindt was sent to Maine", "PS", 342.0) + card("About three thousand", HOULTON),
    # 13
    sh("One of the American guards", "PS", 407.0) + sh("They were really just boys", "PS", 420.0, False),
    # 14
    sh("Maine needed them", "PS", 455.0) + sh("cut wood for the paper mills", "LG", 287.0) + sh("One of them, Rudi Richter", "PS", 466.0),
    # 15
    sh("They were paid in credit", "PS", 440.0) + sh("The University of Maine", "IT", 66.0, False) + sh("Kleindt cooked", "TT", 428.0),
    # 16
    sh("If you want more", "IT", 268.0) + card("If you want more", SUB),
    # 17
    sh("The boys had been raised", "CH", 115.0) + sh("One day a young prisoner", "TT", 434.0),
    # 18
    sh("Nobody hit him", "TT", 441.0) + sh("He went back to the barracks", "TT", 360.0, False),
    # 19
    sh("At Christmas, a farmer", "LG", 337.0) + sh("His family brought", "LG", 345.0, False),
    # 20
    sh("That night, the prisoners", "PS", 412.0),
    # 21
    sh("Not everyone in Houlton", "IT", 230.0) + sh("But a museum curator", "CH", 60.0) + sh("Many were young", "IT", 240.0),
    # 22
    sh("When the war ended", "TT", 618.0),
    # 23
    sh("Rudi Richter could not", "TT", 625.0) + sh("He stopped an old man", "TT", 373.0),
    # 24
    sh("Sixty years later, telling", "LG", 120.0),
    # 25
    sh("Hank Welzel worked in France", "PS", 350.0) + sh("In nineteen forty-nine", "TT", 387.0),
    # 26
    sh("A year later", "TT", 292.0),
    # 27
    sh("In 2003, the town", "LG", 293.0) + sh("Veterans gave them", "LG", 300.0, False),
    # 28
    sh("Not everyone was comfortable", "LG", 318.0),
    # 29
    sh("Rudi Richter did something more", "LG", 324.0) + sh("Sixty years later, Richter went", "LG", 23.0),
    # 30
    sh("Gerhard Kleindt looked back", "LG", 330.0) + card("Gerhard Kleindt looked back", BEST),
    # 31
    sh("If your family farmed", "PS", 426.0),
    # 32
    sh("The prisoners at Houlton", "LG", 280.0),
    # 33
    sh("Their paintings still hang", "LG", 395.0),
]

WCPD = "public domain · Wikimedia Commons"
FSA = "Jack Delano, FSA/OWI, Library of Congress · " + WCPD
PHOTOS = [
    (3, "This is the documented story", None, "boy_pow_crying.jpg", "3", "", "", "John Florea, 1945 · " + WCPD, {"style": "print", "label": "A 15-year-old German prisoner, Germany, April 1945"}),
    (12, "Camp Houlton sat", None, "aroostook_farm1.jpg", "12", "", "", FSA, {"style": "print", "label": "Potato farms, Aroostook County, Maine, 1940s"}),
    (14, "Maine needed them", None, "aroostook_children.jpg", "14", "", "", FSA, {"style": "print", "label": "Potato harvest near Caribou, Aroostook County"}),
    (14, "One of them, Rudi Richter", None, "aroostook_layout.jpg", "14", "", "", FSA, {"style": "print", "label": "Farms near Caribou, Aroostook County"}),
    (15, "Kleindt cooked", None, "pows_dadecity.jpg", "15", "", "", "NARA 23936579 · " + WCPD, {"style": "print", "label": "A German prisoner of war camp in the U.S. (Dade City, Florida, Dec 1944)"}),
    (26, "He went to Korea", None, "korea_mash.jpg", "26", "", "", WCPD, {"style": "print", "label": "Wounded soldier arriving at the 8063rd MASH, Korea"}),
    (26, "Purple Heart", None, "korea_medic.jpg", "26", "", "", "Signal Corps SC 361229 · National Museum of Health and Medicine · CC BY 2.0", {"style": "print", "label": "An American medic near the front line, Korea"}),
    (29, "During the war, a potato", None, "aroostook_after.jpg", "29", "", "", FSA, {"style": "print", "label": "Aroostook County after the harvest"}),
    (31, "If your family farmed", None, "pows_debarking_b.jpg", "31", "", "", "Army Service Forces · NARA via DPLA · " + WCPD, {"style": "print", "label": "German prisoners land in the U.S. (Hampton Roads, Virginia)"}),
]
