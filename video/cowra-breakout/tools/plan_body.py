# Cowra breakout: shots per paragraph and archive prints. exec()'d by tools/plan.py after plan_cards.py.
# 3D rule (owner, 24 Nov 2026): no second of a 3D clip on screen more than twice (tools/reuse_check.py).
# Stand-in films: NA/NB = Japanese POWs in a U.S. camp at Noumea, 1943 (tagged); JN = Japanese 1942 newsreel.

def S(t, sub):
    return SLUG(t, sub)

P = [
    # ── 1. The bugle
    # 0
    sh("A few minutes", "R_NIGHT", 0.0) + card("it was freezing", S("5 August 1944 · before 2 a.m.", "No. 12 POW Compound, Cowra, New South Wales")) +
    sh("more than a thousand", "R_BUG", 0.0),
    # 1
    sh("Then a man ran", "NA", 88.0) + sh("A guard fired", "R_NIGHT", 9.0, False) + sh("And somewhere in the compound", "R_BUG", 2.5, False),
    # 2
    sh("Two guards came", "R_VK", 0.0) + sh("They pulled their army", "R_VK", 1.0, False),
    # 3
    sh("Behind them, hundreds", "R_CHG", 0.0),
    # 4
    sh("This is the documented", "R_DAY", 0.0) + sh("and from the recorded words", "NA", 415.0),
    # 5
    sh("The man who blew", "NB", 508.0) + sh("To understand why", "R_ZERO", 0.0),
    # ── 2. The rule
    # 6
    sh("In January nineteen forty-one", "JN", 123.0) + sh("One line in it", "JN", 498.0, False) + card("In the government's own", CODE),
    # 7
    sh("The code belonged", "JN", 140.0) + sh("A soldier who was captured", "JN", 513.0, False) + sh("He had shamed", "JN", 110.0, False) +
    sh("Many Japanese prisoners", "NB", 585.0),
    # 8
    sh("So Japanese prisoners", "NA", 401.0) + card("By August nineteen forty-four", PRISONERS),
    # 9
    sh("The Australian official history set", "NA", 510.0) + sh("The Japanese prisoners in Australian", "NA", 157.0, False),
    # ── 3. The first prisoner
    # 10
    sh("On the morning of February", "JR", 535.0) + card("On the morning of February", DARWIN, until="Bombs fell on"),
    # 11
    sh("One of the fighter pilots", "JR", 403.0, False) + sh("Over Darwin his plane", "JR", 229.0, False),
    # 12
    sh("He came down", "NB", 353.5) + card("He came down", MELVILLE, until="The crash landing") + sh("The crash landing", "R_ZERO", 5.0),
    # 13
    sh("He wandered through", "R_ZERO", 9.5, False) + card("he walked into a camp", S("Melville Island · February 1942", "Home of the Tiwi people")) + sh("he walked into a camp", "NB", 354.0, False) +
    sh("Not far away", "R_ZERO", 0.5, False),
    # ── 4. Stick 'em up
    # 14
    sh("The man who caught him", "NB", 431.0),
    # 15
    sh("I see him through", "NB", 353.0) + card("I see him through", STICK),
    # 16
    sh("kept watch over his prisoner", "NB", 380.0),
    # 17
    sh("The Zero lay", "NB", 357.0),
    # ── 5. A false name
    # 18
    sh("When the Australians questioned", "NB", 6.0) + sh("Even his story was invented", "NB", 32.0, False),
    # 19
    sh("He was not the only one", "NB", 520.0) + card("Many of us had", FALSE),
    # 20
    sh("A false name meant", "JN", 565.0) + sh("As far as his village", "NB", 590.0),
    # 21
    sh("Under the name", "NB", 444.0) + card("Under the name", JOURNEY),
    # ── 6. Cowra
    # 22
    sh("Cowra was the centre", "R_DAY", 0.0, False) + sh("It had been built", "NA", 105.5) + card("Cowra was the centre", S("Cowra, New South Wales", "No. 12 Prisoner of War Compound · built 1941")),
    # 23
    sh("Its official name", "R_DAY", 2.6, False) + sh("that crossed in the middle", "NA", 108.0),
    # 24
    sh("The prisoners and guards called", "NA", 101.0) + sh("At night, six", "R_TOWER", 0.0),
    # 25
    sh("Italians lived in one", "NA", 415.0) + card("By August nineteen forty-four", CAMPB),
    # ── 7. The guards
    # 26
    sh("The camp was guarded", "NA", 224.0),
    # 27
    sh("Charles Shepherd had been", "NA", 61.0),
    # 28
    sh("Ben Hardy was a motor", "NA", 75.0),
    # 29
    sh("Ralph Jones had been born", "NA", 230.0),
    # ── 8. Rifles and two Vickers guns
    # 30
    sh("A guard at Cowra", "NA", 433.0),
    # 31
    sh("On the edge of the Japanese", "R_VK", 9.5) + sh("each carrying a Vickers", "R_DAWN", 7.4),
    # 32
    sh("Most of the guards did not", "NA", 440.0) + card("We'd never ever", NEVER),
    # ── 9. Baseball
    # 33
    sh("Life in Camp B", "NA", 157.0),
    # 34
    sh("The official history says that the prisoners", "NA", 537.0) + card("The official history says that the prisoners", DOC_BASEBALL),
    # 35
    sh("Another survivor", "NA", 183.0),
    # 36
    sh("But comfort did not mean", "NA", 548.0) + card("A major of the garrison", FEAR),
    # ── 10. The warning
    # 37
    sh("In June nineteen forty-four", "NB", 45.0),
    # 38
    sh("According to a newspaper", "NB", 60.0),
    # 39
    sh("The official history says that early", "NA", 470.0) + sh("Extra precautions", "NA", 618.0, False),
    # 40
    sh("The camp was overcrowded", "NB", 455.0) + card("The camp was overcrowded", HAYMAP),
    # ── 11. Twenty-four hours
    # 41
    sh("The Geneva Convention", "NB", 482.0),
    # 42
    sh("To the Australians", "NA", 520.0) + sh("In the Japanese forces", "NA", 591.0, False),
    # 43
    sh("The Japanese leaders objected", "NB", 545.0) +
    card("Australian soldiers were to be attacked", HL("SGT MAJ. AKIRA KANAZAWA'S ORDER · AUSTRALIAN WAR MEMORIAL", "No prisoner was to harm", "a civilian", "a civilian", "AWM, 'The bugle and the breakout' (2019)")),
    # ── 12. The vote
    # 44
    sh("That night, the leaders", "NA", 604.0) + card("That night, the leaders", NIGHT),
    # 45
    sh("Then the men were asked", "NA", 496.0) +
    card("A circle meant yes", HL("THE VOTE · MIDNIGHT, 4-5 AUGUST 1944", "A circle meant", "yes", "A circle meant yes", "SBS News, 2019 · nippon.com, 2021", after=" · a cross meant no")),
    # 46
    sh("was twenty-three", "NA", 578.0) + card("Decades later he told", VOTE),
    # 47
    sh("said he had felt", "NB", 598.0) + card("I felt, okay", ALONG),
    # 48
    sh("The circles won", "R_TOWER", 0.0, False),
    # ── 13. Bats, knives and blankets
    # 49
    sh("The men had been preparing", "NA", 632.0),
    # 50
    sh("The official history lists", "NA", 20.0) + card("The official history lists", DOC_WEAPONS),
    # 51
    sh("carried a baseball bat", "NA", 347.0) + sh("He and a friend", "R_BUG", 9.0, False) + sh("If one of them was shot", "NA", 351.0, False),
    # 52
    sh("was told that the signal", "R_BDAY", 0.0) + sh("His task was", "NA", 14.0, False),
    # 53
    sh("said he joined believing", "NA", 374.0) + sh("Most of the men in Camp B", "NB", 525.0),
    # ── 14. Two o'clock
    # 54
    sh("At about two in the morning", "R_TOWER", 8.0, False) + card("At about two in the morning", S("5 August 1944 · about 2 a.m.", "B camp, No. 12 POW Compound")) + sh("The guard on Broadway", "NB", 389.0, False),
    # 55
    sh("Then the bugle sounded", "R_BUG", 6.5, False) + sh("by the prisoner the camp", "NB", 600.0),
    # 56
    sh("With a cry of", "R_CHG", 0.0, False) + sh("Many, a Memorial historian", "NA", 101.0, False),
    # 57
    sh("Behind them, men who stayed", "R_CHG", 11.5, False) + sh("Eighteen of the twenty", "NA", 105.0, False),
    # ── 15. The bastards have broken
    # 58
    sh("Sergeant Cooper woke", "R_BW", 0.0) + sh("flares going up", "R_SIDE", 0.0, False) + sh("I thought, oh", "NB", 376.0, False),
    # 59
    sh("He could see the huts", "R_BW", 5.8, False) + sh("The floodlights", "R_SIDE", 6.0),
    # 60
    sh("Most of the guards who were off", "NB", 380.0),
    # 61
    sh("Private Charles Shepherd came", "NB", 398.0),
    # ── 16. The gun
    # 62
    sh("The strongest group", "R_VK", 7.0) + sh("That was where Hardy", "NB", 386.5, False),
    # 63
    sh("The two men had pushed", "R_VK", 0.0, False) + sh("until they were overwhelmed", "R_BUG", 10.3, False),
    # 64
    sh("Hardy was clubbed", "R_DAWN", 9.0) + sh("The prisoners took the gun", "NB", 387.0, False) +
    card("The prisoners took the gun", HL("THE VICKERS GUN · NORTH-WEST WIRE", "It would", "not fire", "It would not fire", LONG + ", p. 624")),
    # 65
    sh("Accounts differ on why", "NB", 455.0) + card("The official history says only", LDOC("THE FINAL CAMPAIGNS · 1963", "The official history", [("long_jammed", "it jammed")], LONG + ", p. 624"),
                                                    until="Harry Gordon") +
    card("I think it was Hardy", QC("stills/hardy_gc.jpg", [("I think it was Hardy", "I think it was Hardy"), ("that took the bolt out of the gun", "took the bolt out")],
                                    "Sgt Ashley Cooper, 22nd Garrison Battalion · AWM S01027, p. 22", "took the bolt out"), until="The Australian War Memorial says"),
    # 66
    sh("At dawn, Cooper saw", "R_DAWN", 0.0, False) + card("Just like a pile", FIREWOOD),
    # ── 17. Broadway
    # 67
    sh("According to the official history, not one", "R_BDAY", 0.0) + sh("The fire there was so heavy", "R_BW", 0.0),
    # 68
    sh("reached Broadway with", "R_SIDE", 0.0, False),
    # 69
    sh("both ended up lying", "R_ASH", 0.0, False) + sh("an Australian came and spoke", "R_DAWN", 0.0, False) + card("We will not harm", DITCH),
    # 70
    sh("The shooting went on", "R_ASH", 0.0),
    # ── 18. Inside the wire
    # 71
    sh("When it was light", "NA", 265.0),
    # 72
    sh("The court of inquiry counted how", "NA", 251.0),
    # 73
    sh("remembered the fire", "NA", 129.0) +
    card("We had a big fire", QC("stills/burnt_huts.jpg", [("We had a big fire", "We had a big fire"), ("and put blankets in to make it big.", "put blankets in"),
                                                          ("We wanted to burn everything.", "burn everything")], "Teruo Murakami · SBS News, 2019", "burn everything")),
    # 74
    sh("Just outside the wire", "R_ASH", 9.0, False) + sh("The record of his grave", "NB", 392.0, False) +
    card("The record of his grave", HL("COWRA JAPANESE WAR CEMETERY DATABASE · GRAVE 510", "Cause of death:", "gunshot wound to chest", "gunshot wound to the chest",
                                       "cowrajapanesecemetery.org (Embassy of Japan, 2016-19)", after=" and self-inflicted wound")),
    # ── 19. Into the country
    # 75
    sh("Several hundred prisoners", "R_ASH", 11.8, False) + sh("Camp guards, soldiers", "NB", 462.0),
    # 76
    sh("The official history says that in this phase", "NB", 488.0),
    # 77
    sh("Many did not wait", "NA", 150.0),
    # ── 20. The rock
    # 78
    sh("That evening, a young", "NB", 468.0),
    # 79
    sh("At dusk they came", "NB", 492.0) + card("At dusk they came", S("Dusk, 5 August 1944", "The hills north of Cowra")),
    # 80
    sh("Doncaster was killed", "NA", 640.0),
    # ── 21. Halfway
    # 81
    sh("If you want more", "R_BDAY", 7.0, False) + card("If you want more", SUB),
    # 82
    sh("The people of Cowra heard", "NB", 470.0),
    # 83
    sh("Whether because of", "NB", 476.0),
    # ── 22. Tea and scones
    # 84
    sh("On a farm outside Cowra", "R_FARM", 0.0, False),
    # 85
    sh("The farm's mechanic", "R_VER", 0.0),
    # 86
    sh("just take them round", "NA", 170.0) + card("just take them round", SCONES),
    # 87
    sh("Margaret was sent", "NA", 213.0) +
    card("Then they got up", HL("THE WEIR FARM, NEAR COWRA · 5 AUGUST 1944", "They got up, and", "thanked her", "thanked her", "Margaret and Bruce Weir · AWM S00932, 1990")),
    # 88
    sh("One of those three men", "R_FARM", 5.2, False),
    # ── 23. Nine days
    # 89
    sh("The search went on", "NA", 453.0) + card("In the end", BROUGHT),
    # 90
    sh("The total was terrible", "NA", 460.0) + card("The court of inquiry counted", DEAD),
    # 91
    sh("Four Australians had been", "NA", 600.0),
    # 92
    sh("It was the largest prison", "R_BDAY", 9.5, False),
    # ── 24. The inquiry
    # 93
    sh("A military court of inquiry sat", "NB", 84.0),
    # 94
    sh("On September eighth", "NB", 66.0),
    # 95
    sh("The court found", "NB", 20.0) + card("The court found", SUICIDAL),
    # ── 25. Secrecy
    # 96
    sh("The government kept", "NA", 618.0) + card("In Australia the event", INCIDENT),
    # 97
    sh("The reason was the twenty-one", "NB", 96.0) + sh("Cooper said that he once", "NB", 110.0, False),
    # 98
    sh("The Australian government sent", "NB", 125.0) +
    card("Japan's own archives", HL("JAPAN CENTER FOR ASIAN HISTORICAL RECORDS · B02032491300", "The file heading:", "protest to Australia", "protest to Australia", "JACAR Newsletter no. 31 (2020)")),
    # ── 26. A medal six years late
    # 99
    sh("The secrecy lasted", "NB", 405.0),
    # 100
    sh("The citation reads", "NA", 236.0) + card("The citation reads", DOC_GAZETTE),
    # 101
    sh("Ben Hardy's widowed mother", "NA", 488.0),
    # 102
    sh("Because Cowra was not", "NA", 224.5),
    # ── 27. Going home
    # 103
    sh("The surviving prisoners", "NB", 446.0) + card("The surviving prisoners", HOME),
    # 104
    sh("They did not go home", "NB", 500.0),
    # 105
    sh("One survivor", "NB", 130.0),
    # 106
    sh("built a new life", "NB", 140.0) +
    card("he would joke", HL("MAREKUNI TAKAHARA · AWM ORAL HISTORY S03331", "A graduate of", "Cowra University", "Cowra University", "AWM S03331, 2004, p. 8")),
    # ── 28. The name on the grave
    # 107
    sh("The dead were buried", "NA", 401.5),
    # 108
    sh("One of the Japanese graves", "NA", 347.5),
    # 109
    sh("His bugle survived", "NA", 205.0) +
    card("How it reached", HL("THE BUGLE · AUSTRALIAN WAR MEMORIAL REL/04058", "How it reached Cowra is", "still a mystery", "still a mystery", "AWM, 'The bugle and the breakout' (2019)")),
    # ── 29. The graves
    # 110
    sh("In nineteen fifty-two", "NA", 3.0),
    # 111
    sh("In nineteen sixty-four", "NA", 55.0),
    # 112
    sh("In nineteen seventy-nine", "NA", 140.0),
    # ── 30. The jug
    # 113
    sh("In nineteen eighty-four", "R_VER", 2.0, False),
    # 114
    sh("He went back to the farm", "NA", 527.0) +
    card("It was the very same jug", HL("THE WEIR FARM · 1984", "It was", "the very same jug", "the very same jug", "Margaret Weir · AWM S00932, 1990, p. 6")),
    # 115
    sh("came back too", "NA", 379.0) + card("Everybody thought we would", ALIVE),
    # ── 31. The last survivor
    # 116
    sh("the man who drew a circle", "NA", 479.0),
    # 117
    sh("He said he had voted yes", "NA", 336.0) + card("I don't want any", MISERABLE, until="His message") + card("His message", NEVERAGAIN),
    # 118
    sh("He died in Japan", "NA", 566.0),
    # ── 32. Your family
    # 119
    sh("If your father", "NB", 426.0),
    # ── 33. Echo
    # 120
    sh("Today, almost nothing", "NA", 366.0),
    # 121
    sh("On the night of the eightieth", "R_TOWER", 8.0, False),
    # 122
    sh("Three kilometres away", "NB", 564.0),
]

AWMPD = "Australian War Memorial {} · public domain"
def A(n):
    return AWMPD.format(n)
CCBY = "Commons · CC BY 3.0"
PHOTOS = [
    # (para, anchor, until, file, frameNo, title, caption, source, extra)
    (1, "Then a man ran", None, "jap_section_view.jpg", "01", "", "", A("067172"), {"style": "print", "label": "The Japanese section, No. 12 POW Compound, 1 Jul 1944"}),
    (2, "Ben Hardy was", None, "hardy_gc.jpg", "02", "", "", A("081385"), {"style": "print", "label": "Pte Benjamin Gower Hardy, 22nd Garrison Battalion"}),
    (2, "Ralph Jones was", None, "jones_gc.jpg", "02", "", "", A("081386"), {"style": "print", "label": "Pte Ralph Jones, 22nd Garrison Battalion"}),
    (3, "They carried knives", None, "knives.jpg", "03", "", "", A("073486"), {"style": "print", "label": "Knives recovered in and around B camp, Aug 1944"}),
    (4, "told from the Australian", None, "aerial_b_after.jpg", "04", "", "", A("P03160.003"), {"style": "print", "label": "B compound from the air, the day after the breakout"}),
    (4, "and from the recorded words", None, "parade_1115.jpg", "04", "", "", A("067205"), {"style": "print", "label": "Japanese prisoners fall in for the 11:15 parade, Cowra, 1 Jul 1944"}),
    (5, "under a name", None, "toyoshima_id.jpg", "05", "", "", A("068530"), {"style": "print", "label": "The first Japanese prisoner taken in Australia: identification photographs, 9 Apr 1942"}),
    (7, "Many Japanese prisoners", None, "jpow_newguinea.jpg", "07", "", "", A("072471") + " · " + WC, {"style": "print", "label": "A Japanese prisoner, New Guinea, April 1944"}),
    (9, "Most of the twenty-one", None, "aus_pows_changi.jpg", "09", "", "", "Leslie Cole, 1945 · Imperial War Museum ARTLD5618 · public domain · " + WC, {"style": "print", "label": "Painting: Allied prisoners with beriberi, Changi Gaol, Singapore, 1945"}),
    (9, "The Japanese prisoners in Australian", None, "veg_garden.jpg", "09", "", "", A("067190"), {"style": "print", "label": "Vegetable garden outside the Japanese mess, Cowra, 1 Jul 1944"}),
    (10, "Bombs fell on", None, "darwin_neptuna_big.jpg", "10", "", "", A("128108") + " · " + WC, {"style": "print", "label": "The Neptuna explodes in Darwin harbour, 19 Feb 1942"}),
    (11, "He flew a Zero", None, "zero_hiryu_crash.jpg", "11", "", "", "U.S. Navy · 80-G-22163 · public domain · " + WC, {"style": "print", "label": "A Zero from the carrier Hiryu, downed at Pearl Harbor, Dec 1941 (same carrier, same type)"}),
    (14, "The man who caught him", None, "jpows_nov44.jpg", "14", "", "", A("083404") + " · " + WC, {"style": "print", "label": "Japanese prisoners with an Australian soldier, Nov 1944 (not Toyoshima)"}),
    (15, "When the pilot walked", None, "jpows_singorkai.jpg", "15", "", "", "Keith Rainsford · public domain · Wikimedia Commons", {"style": "print", "label": "Stand-in · Japanese prisoners with Papuan soldiers, New Guinea, 1944"}),
    (16, "handed him over", None, "toyoshima_captors.jpg", "16", "", "", A("P00022.001"), {"style": "print", "label": "Sgt Hajime Toyoshima with Sgt Leslie J. Powell, Feb 1942"}),
    (17, "The Zero lay", None, "zero_melville.jpg", "17", "", "", A("P00022.002"), {"style": "print", "label": "Toyoshima's Zero on Melville Island, 27 Feb 1942"}),
    (17, "And its pilot was", None, "toyoshima_id.jpg", "17", "", "", A("068530"), {"style": "print", "label": "'P.O.W. J. 910.1': Toyoshima's identification photographs, 9 Apr 1942"}),
    (18, "He said he was", None, "toyoshima_id_strip.jpg", "18", "", "", A("100524"), {"style": "print", "label": "Identification photographs, April 1942"}),
    (20, "A false name meant", None, "jpows_brisbane.jpg", "20", "", "", "State Library of Queensland · public domain · " + WC, {"style": "print", "label": "Japanese prisoners of war arriving at Brisbane, c. 1944"}),
    (22, "It had been built", None, "a_compound.jpg", "22", "", "", A("064283"), {"style": "print", "label": "A compound (Italian prisoners), Cowra, 4 Feb 1944"}),
    (23, "Each camp was fenced", None, "camp_plan.jpg", "23", "", "", A("P02567.002"), {"style": "print", "label": "Hand-drawn plan of the camp: headquarters and the four compounds"}),
    (24, "The prisoners and guards called", None, "compounds_west.jpg", "24", "", "", A("064284"), {"style": "print", "label": "The compounds looking west, headquarters in front, 4 Feb 1944"}),
    (25, "Camp B, one quarter", None, "bowing_sun.jpg", "25", "", "", A("067196"), {"style": "print", "label": "Japanese prisoners at the 12th POW camp, 2 Jul 1944 (photographed for propaganda)"}),
    (26, "The camp was guarded", None, "gb22_parade.jpg", "26", "", "", A("P07758.010"), {"style": "print", "label": "Men of the 22nd Garrison Battalion, later at Cowra"}),
    (26, "Many had fought", None, "officers_22gb.jpg", "26", "", "", A("064287"), {"style": "print", "label": "Officers of the 22nd Garrison Battalion, Cowra, 5 Feb 1944"}),
    (27, "Charles Shepherd had been", None, "shepherd.jpg", "27", "", "", A("P04966.001"), {"style": "print", "label": "Pte Charles Henry Shepherd, 22nd Garrison Battalion"}),
    (28, "Ben Hardy was a motor", None, "hardy_1942.jpg", "28", "", "", A("P01451.001"), {"style": "print", "label": "Pte Ben Hardy, 1942"}),
    (29, "Ralph Jones had been born", None, "jones_gc.jpg", "29", "", "", A("081386"), {"style": "print", "label": "Pte Ralph Jones, 22nd Garrison Battalion"}),
    (30, "A guard at Cowra", None, "guard_tower.jpg", "30", "", "", A("064350"), {"style": "print", "label": "Pte O. O. Treacy, 22nd Garrison Battalion, on a guard tower at Cowra, 7 Feb 1944"}),
    (30, "They had been shown", None, "gb22_personnel.jpg", "30", "", "", A("064288"), {"style": "print", "label": "Men of the 22nd Garrison Battalion, Cowra, 4 Feb 1944"}),
    (33, "Life in Camp B", None, "clothing_parade.jpg", "33", "", "", A("067198"), {"style": "print", "label": "Clothing parade, Japanese section, Cowra, 1 Jul 1944"}),
    (34, "They made their own", None, "baseball.jpg", "34", "", "", A("067192"), {"style": "print", "label": "Japanese prisoners playing baseball outside their huts, Cowra, 1 Jul 1944"}),
    (35, "Another survivor", None, "sportsground.jpg", "35", "", "", A("067176"), {"style": "print", "label": "Sports ground and huts of the Japanese section, 1 Jul 1944"}),
    (37, "In June nineteen forty-four", None, "guard_tower_b.jpg", "37", "", "", A("064351"), {"style": "print", "label": "A guard tower, Cowra, 7 Feb 1944"}),
    (38, "According to a newspaper", None, "officers_a.jpg", "38", "", "", A("064344"), {"style": "print", "label": "Officers of the 22nd Garrison Battalion, A compound, 4 Feb 1944"}),
    (41, "So on Friday", None, "barmera_internees.jpg", "41", "", "", A("064888"), {"style": "print", "label": "Japanese internees moved from Hay by train, March 1943"}),
    (42, "To the Australians", None, "parade_sports.jpg", "42", "", "", A("067180"), {"style": "print", "label": "Japanese prisoners assembled on the sports area, Cowra, 1 Jul 1944"}),
    (49, "The men had been preparing", None, "knives.jpg", "49", "", "", A("073486"), {"style": "print", "label": "Weapons recovered after the breakout: knives, Aug 1944"}),
    (50, "The blankets were for", None, "blankets_wire.jpg", "50", "", "", A("073485"), {"style": "print", "label": "Blankets thrown over the wire of B camp, Aug 1944"}),
    (52, "His task was", None, "camp_plan.jpg", "52", "", "", A("P02567.002"), {"style": "print", "label": "The camp plan: B compound's huts in black"}),
    (54, "The guard on Broadway", None, "guard_tower_b.jpg", "54", "", "", A("064351"), {"style": "print", "label": "A guard tower, Cowra, 7 Feb 1944"}),
    (55, "It was blown", None, "toyoshima_id.jpg", "55", "", "", A("068530"), {"style": "print", "label": "Hajime Toyoshima, known at Cowra as Tadao Minami"}),
    (56, "Many, a Memorial historian", None, "blankets_wire.jpg", "56", "", "", A("073485"), {"style": "print", "label": "Blankets on the wire of B camp, Aug 1944"}),
    (57, "Eighteen of the twenty", None, "burnt_huts.jpg", "57", "", "", A("073484"), {"style": "print", "label": "Huts burned in B camp, Aug 1944"}),
    (58, "I thought, oh", None, "gb22_personnel.jpg", "58", "", "", A("064288"), {"style": "print", "label": "22nd Garrison Battalion, Cowra, 1944"}),
    (60, "Most of the guards who were off", None, "officers_22gb.jpg", "60", "", "", A("064287"), {"style": "print", "label": "22nd Garrison Battalion, Cowra, 1944"}),
    (61, "Private Charles Shepherd came", None, "shepherd.jpg", "61", "", "", A("P04966.001"), {"style": "print", "label": "Pte Charles Henry Shepherd, killed 5 Aug 1944"}),
    (62, "That was where Hardy", None, "hardy_gc.jpg", "62", "", "", A("081385"), {"style": "print", "label": "Pte Ben Hardy, 22nd Garrison Battalion"}),
    (63, "Hardy fired", None, "hardy_1942.jpg", "63", "", "", A("P01451.001"), {"style": "print", "label": "Pte Ben Hardy, 1942"}),
    (63, "Jones fed the", None, "jones_gc.jpg", "63", "", "", A("081386"), {"style": "print", "label": "Pte Ralph Jones"}),
    (65, "The Australian War Memorial says", None, "hardy_gc.jpg", "65", "", "", A("081385"), {"style": "print", "label": "Pte Ben Hardy GC"}),
    (68, "reached Broadway with", None, "aerial_b_after.jpg", "68", "", "", A("P03160.003"), {"style": "print", "label": "B compound and the road beside it, the day after the breakout"}),
    (71, "Almost every hut", None, "burnt_huts.jpg", "71", "", "", A("073484"), {"style": "print", "label": "Burnt huts, B camp, Aug 1944"}),
    (72, "The court of inquiry counted how", None, "burial_japanese.jpg", "72", "", "", A("073487"), {"style": "print", "label": "Burial of the Japanese dead, Cowra, Aug 1944"}),
    (75, "Camp guards, soldiers", None, "gb22_parade.jpg", "75", "", "", A("P07758.010"), {"style": "print", "label": "Men of the 22nd Garrison Battalion"}),
    (76, "A police constable", None, "daily_mirror.jpg", "76", "", "", A("044178"), {"style": "print", "label": "'Camp escapes accounted for': the Daily Mirror, Aug 1944"}),
    (77, "Many did not wait", None, "camp_site_after.jpg", "77", "", "", A("044176"), {"style": "print", "label": "The country north of Cowra: the camp site after the war"}),
    (78, "That evening, a young", None, "veg_garden.jpg", "78", "", "", A("067190"), {"style": "print", "label": "Cowra camp and the hills beyond, 1944"}),
    (80, "Doncaster was killed", None, "grave_doncaster.jpg", "80", "", "", "Commons · CC BY 3.0", {"style": "print", "label": "Lt Harry Doncaster's grave, Cowra War Cemetery"}),
    (82, "The people of Cowra heard", None, "cowra_guardian.jpg", "82", "", "", A("044175"), {"style": "print", "label": "The Cowra Guardian, 8 Aug 1944"}),
    (83, "Whether because of", None, "headlines.jpg", "83", "", "", A("044570"), {"style": "print", "label": "Headlines on the Cowra outbreak, Aug 1944"}),
    (87, "Margaret was sent", None, "clothing_parade.jpg", "87", "", "", A("067198"), {"style": "print", "label": "Japanese prisoners in camp clothing, Cowra, 1944"}),
    (91, "Four Australians had been", None, "funeral_procession.jpg", "91", "", "", A("P01451.002"), {"style": "print", "label": "The funeral of Ptes Shepherd, Jones and Hardy, Cowra, Aug 1944"}),
    (91, "A fifth, Sergeant", None, "coffins.jpg", "91", "", "", A("P01451.004"), {"style": "print", "label": "Their coffins carried to the grave"}),
    (93, "A military court of inquiry sat", None, "officers_a.jpg", "93", "", "", A("064344"), {"style": "print", "label": "Officers of the 22nd Garrison Battalion, 1944"}),
    (94, "On September eighth", None, "curtin.jpg", "94", "", "", "Antonio Dattilo Rubbo · public domain · " + WC, {"style": "print", "label": "Prime Minister John Curtin (official portrait)"}),
    (96, "The government kept", None, "headlines.jpg", "96", "", "", A("044570"), {"style": "print", "label": "What the papers were allowed to print, Aug 1944"}),
    (97, "The reason was the twenty-one", None, "aus_pows_changi.jpg", "97", "", "", "Leslie Cole, 1945 · IWM ARTLD5618 · public domain · " + WC, {"style": "print", "label": "Painting: Allied prisoners, Changi Gaol, Singapore, 1945"}),
    (99, "two posthumous awards", None, "mourners.jpg", "99", "", "", A("P01451.003"), {"style": "print", "label": "Mourners beside the coffins of Shepherd, Jones and Hardy, 1944"}),
    (101, "Ben Hardy's widowed mother", None, "grave_hardy.jpg", "101", "", "", "Commons · CC BY 3.0", {"style": "print", "label": "Ben Hardy GC, Cowra War Cemetery"}),
    (101, "Ralph Jones's brother", None, "grave_jones.jpg", "101", "", "", "Commons · CC BY 3.0", {"style": "print", "label": "Ralph Jones GC, Cowra War Cemetery"}),
    (102, "Because Cowra was not", None, "shepherd.jpg", "102", "", "", A("P04966.001"), {"style": "print", "label": "Pte Charles Shepherd"}),
    (104, "They did not go home", None, "pows_balmain.jpg", "104", "", "", A("126121"), {"style": "print", "label": "Japanese prisoners from Hay at Balmain wharf, Sydney, 2 Mar 1946"}),
    (104, "According to a New South Wales", None, "guard_balmain.jpg", "104", "", "", A("126109"), {"style": "print", "label": "Going aboard for Japan, No. 1 wharf, Balmain, 2 Mar 1946"}),
    (105, "One survivor", None, "pow_ambulance_1946.jpg", "105", "", "", A("126291"), {"style": "print", "label": "A prisoner wounded in the breakout is carried to the ship, Sydney, 6 Mar 1946"}),
    (107, "The dead were buried", None, "burial_australians.jpg", "107", "", "", A("044119"), {"style": "print", "label": "Burial of the Australian soldiers killed in the breakout, Aug 1944"}),
    (108, "One of the Japanese graves", None, "jcem_graves2020.jpg", "108", "", "", "Commons · CC BY-SA 4.0", {"style": "print", "label": "Graves in the Cowra Japanese War Cemetery, 2020"}),
    (108, "who he really was", None, "toyoshima_id_strip.jpg", "108", "", "", A("100524"), {"style": "print", "label": "Hajime Toyoshima, identification photographs, April 1942"}),
    (110, "In nineteen fifty-two", None, "jcem_entry.jpg", "110", "", "", CCBY, {"style": "print", "label": "Cowra Japanese War Cemetery"}),
    (111, "In nineteen sixty-four", None, "jcem_wide.jpg", "111", "", "", CCBY, {"style": "print", "label": "Cowra Japanese War Cemetery"}),
    (111, "The Japanese who died", None, "jcem_004.jpg", "111", "", "", CCBY, {"style": "print", "label": "The cemetery's memorial stone"}),
    (112, "In nineteen seventy-nine", None, "garden_pano.jpg", "112", "", "", "Commons · CC BY-SA 3.0", {"style": "print", "label": "Cowra Japanese Garden, 2006"}),
    (112, "Its designer", None, "garden_001.jpg", "112", "", "", CCBY, {"style": "print", "label": "Cowra Japanese Garden, 2011"}),
    (113, "One of them was one", None, "takezawa_oliver.jpg", "113", "", "", "Commons · CC BY 4.0", {"style": "print", "label": "Albert Oliver, who cared for the Japanese graves, with Japan's first exchange student at Cowra, 1970"}),
    (114, "He went back to the farm", None, "garden_02.jpg", "114", "", "", "Commons · public domain", {"style": "print", "label": "Cowra, 2006"}),
    (115, "came back too", None, "site_monument.jpg", "115", "", "", CCBY, {"style": "print", "label": "The breakout memorial at the camp site"}),
    (116, "the man who drew a circle", None, "site_sign.jpg", "116", "", "", CCBY, {"style": "print", "label": "The camp site today"}),
    (118, "He died in Japan", None, "jcem_rows.jpg", "118", "", "", CCBY, {"style": "print", "label": "Graves dated 5 August 1944, Cowra Japanese War Cemetery"}),
    (119, "If your father", None, "gb22_parade.jpg", "119", "", "", A("P07758.010"), {"style": "print", "label": "Men of the 22nd Garrison Battalion"}),
    (120, "Today, almost nothing", None, "site_pan.jpg", "120", "", "", "Commons · CC BY-SA 3.0", {"style": "print", "label": "The camp site today"}),
    (120, "After the war", None, "site_ruins.jpg", "120", "", "", CCBY, {"style": "print", "label": "Hut foundations at the camp site"}),
    (121, "On the night of the eightieth", None, "site_tower.jpg", "121", "", "", CCBY, {"style": "print", "label": "The rebuilt guard tower at the camp site"}),
    (122, "Three kilometres away", None, "jcem_entry.jpg", "122", "", "", CCBY, {"style": "print", "label": "Cowra Japanese War Cemetery"}),
    (122, "Beside it", None, "toyoshima_captors.jpg", "122", "", "", A("P00022.001"), {"style": "print", "label": "Hajime Toyoshima, 1942"}),
]
