# Lunchroom POWs: shots per paragraph and archive prints. exec()'d by tools/plan.py after plan_cards.py.
# Rules: no 3D; no film second or photo more than twice on screen (tools/reuse_check.py); stand-ins tagged.
# NS = 'The Negro Soldier' (avoid 230-290 flag, 1060-1080 enemy map); TW = 'Teamwork' (avoid 40-300 enemy staging);
# NP = WAC mail; TT = troop train; RS = restaurant (stand-in lunchroom); CG = POWs (faded, graded); PS = POWs shipped.

def S(t, sub):
    return SLUG(t, sub)

P = [
    # ── 1. Cold open
    # 0
    sh("It was a morning", "TT", 468.0) + card("It was a morning", S("1944 · a railroad station", "On the line from Louisiana to Arizona")) +
    sh("Nine American soldiers", "TT", 618.0, False) + sh("They were Black", "RS", 444.0),
    # 1
    sh("The only place", "RS", 285.0, False) + sh("But they were not allowed", "RS", 604.0, False) + sh("They had to eat in the kitchen", "RS", 272.0, False),
    # 2
    sh("Then, at eleven thirty", "PS", 324.0) + sh("The Germans sat down", "PS", 407.0) + sh("Their meals were served", "RS", 298.0) +
    sh("They talked, they smoked", "RS", 458.0, False) + sh("and one of the nine", "NS", 1324.0),
    # 3
    sh("His name was Rupert", "NP", 35.0) + sh("And when the Army's own", "NP", 62.0, False),
    # 4
    sh("This is the documented", "NS", 1576.0) + sh("It is told from the letters", "NP", 437.0) + sh("and from the words of a famous", "NS", 2333.0),
    # ── 2. Old Man Jim Crow
    # 5
    sh("To understand that morning", "NS", 1753.0) + card("About nine hundred thousand", SERVED) + sh("They served in a segregated", "NS", 1677.0, False),
    # 6
    sh("Off the base", "NS", 290.0),
    # 7
    sh("Trimmingham was not", "NS", 1578.0) + sh("He joined the Army", "TW", 411.0),
    # 8
    sh("He was stationed", "NS", 1601.0),
    # 9
    sh("He and eight other", "TT", 332.0) + card("He and eight other", TRIP, until="The letter never names"),
    # ── 3. The prisoners
    # 10
    sh("At the same time", "PS", 333.0) + card("More than three hundred", GERMANS),
    # 11
    sh("The United States treated", "PS", 346.0) + card("Its eleventh article", GENEVA),
    # 12
    sh("So the prisoners ate", "PS", 420.0) + sh("And when they travelled", "TT", 387.0),
    # 13
    sh("The Convention said nothing", "RS", 312.0) + sh("That was decided", "RS", 577.0, False) + sh("and in nineteen forty-four, in that town", "RS", 232.0, False),
    # ── 4. The letter
    # 14
    sh("Trimmingham went back", "NS", 1929.0) + card("Yank was written", COPIES),
    # 15
    sh("He began with a question", "NP", 48.0) + sh("On whose team", "NS", 592.0),
    # 16
    sh("He told them about", "RS", 590.0) + card("He wrote that the Germans", SWELL),
    # 17
    sh("Then he wrote the lines", "NS", 1349.0) + card("Are these men sworn", WHY),
    # 18
    sh("He ended with a bet", "NS", 1500.0) + card("He ended with a bet", BET),
    # 19
    sh("Yank printed it", "NP", 215.0),
    # ── 5. The answers
    # 20
    sh("The answers came", "NP", 270.0) + card("He wrote that he was a Southern", REBEL),
    # 21
    sh("A staff sergeant", "NP", 298.0) + sh("He asked whether", "PS", 424.0),
    # 22
    sh("A private at a port", "TT", 360.0),
    # 23
    sh("And from the jungle", "NS", 2181.0) + sh("They wrote that Black units", "TW", 546.0),
    # 24
    sh("They had read the letter", "NS", 2005.0) + card("They had read the letter", DOC_BURMA),
    # 25
    sh("Yank printed that letter", "NP", 312.0) + card("Then he told them what", DOC_LETTERS),
    # 26
    sh("Most of them", "NS", 1854.0) + card("Most of them", LETTERS),
    # 27
    sh("The editors added", "NP", 455.0) + sh("The incident had been", "NS", 1248.0),
    # 28
    sh("If you want more", "NS", 2358.0) + card("If you want more", SUB),
    # ── 6. Salina, Kansas
    # 29
    sh("Trimmingham's lunchroom", "NS", 1904.0) + sh("One of its men", "NS", 1803.0, False),
    # 30
    sh("German prisoners of war were in Salina", "PS", 455.0) + sh("One day at noon", "RS", 60.0) + sh("They had come to see", "RS", 617.0),
    # 31
    sh("Brown told the story", "RS", 240.0) + card("The owner hurried out", SERVE),
    # 32
    sh("They did not leave", "RS", 450.0) + sh("the German prisoners of war, having lunch", "PS", 411.0),
    # 33
    sh("Brown wrote that", "RS", 290.0) + card("And he finished", HEARTS),
    # ── 7. Not one town
    # 34
    sh("The historian Matthias", "NP", 104.0) + card("The historian Matthias", PLACES),
    # 35
    sh("In February nineteen forty-four", "NS", 1551.0) + sh("At least two camps", "PS", 360.0),
    # 36
    sh("In South Carolina", "TW", 351.0) + sh("German prisoners could walk", "RS", 610.0),
    # 37
    sh("The historian John Hope", "TT", 373.0) + sh("German prisoners on board", "TT", 505.0, False),
    # 38
    sh("And in January nineteen forty-five", "NP", 256.0) + card("The prisoners, the complaint", GLEE),
    # ── 8. Lena Horne
    # 39
    sh("By nineteen forty-four, Lena", "NS", 1299.0),
    # 40
    sh("That year, she came", "NS", 1650.0) + sh("Camp Robinson held", "PS", 395.0),
    # 41
    sh("She came out on stage", "NS", 2383.0) + sh("In the rows in front", "PS", 466.0),
    # 42
    sh("More than fifty years later", "NS", 315.0) + card("More than fifty years later", BACK),
    # 43
    sh("Her daughter", "NS", 1854.0),
    # 44
    sh("Then her tour was over", "TT", 631.0) + sh("So she paid her own way", "TT", 441.0),
    # 45
    sh("In January nineteen forty-five, a Black", "NP", 437.0) + sh("It told the story", "NS", 1626.0),
    # ── 9. What changed
    # 46
    sh("Some things were already", "NS", 1700.0) + sh("In April nineteen forty-four", "PS", 413.0),
    # 47
    sh("The story of the lunchroom", "NS", 1880.0) + card("The story of the lunchroom", AFTER),
    # 48
    sh("The last German prisoners", "PS", 440.0),
    # 49
    sh("Two years later", "NS", 1790.0) + card("Two years later", DOC_EO),
    # 50
    sh("It took years more", "NS", 1660.0) + sh("But the order was signed", "TW", 516.0),
    # ── 10. Afterwards
    # 51
    sh("Trimmingham was discharged", "NS", 1475.0) + sh("He became an American", "NS", 1324.0),
    # 52
    sh("He died there", "TT", 618.0),
    # 53
    sh("Lloyd Brown went on", "NS", 1349.0),
    # 54
    sh("Lena Horne kept singing", "NS", 1253.0),
    # ── 11. Your family
    # 55
    sh("If your father", "NS", 1720.0) + sh("And if he ever told", "TT", 292.0, False),
    # ── 12. Today
    # 56
    sh("Nobody knows the name", "TT", 625.0) + sh("The lunchroom has no plaque", "RS", 455.0),
    # 57
    sh("What is left is a letter", "NP", 40.0) + sh("And the question he asked", "NS", 1600.0),
]

WCPD = "public domain · " + WC
PHOTOS = [
    (3, "What he saw that morning", None, "colored_waiting.jpg", "3", "", "", "Esther Bubley, OWI, 1943 · " + WCPD, {"style": "print", "label": "Bus station, Rome, Georgia, 1943"}),
    (4, "This is the documented story", None, "yank_0728_cover.jpg", "4", "", "", "Yank, the Army Weekly, 28 July 1944 · public domain", {"style": "print", "label": "Yank, the Army Weekly, 28 July 1944"}),
    (6, "In the South it was written", None, "durham_bus.jpg", "6", "", "", "Jack Delano, FSA, 1940 · " + WCPD, {"style": "print", "label": "Bus station, Durham, North Carolina, May 1940"}),
    (6, "The signs said", None, "durham_hitler.jpg", "6", "", "", "Jack Delano, FSA, 1940 · " + WCPD, {"style": "print", "label": "Durham, North Carolina, 1940"}),
    (8, "At the height of the war", None, "huachuca_patrol.jpg", "8", "", "", "Signal Corps SC131141, 1942 · " + WCPD, {"style": "print", "label": "Patrol on the border, Huachuca Mountains, Arizona, 1942"}),
    (8, "The ninety-third Infantry", None, "huachuca_93rd.jpg", "8", "", "", "NARA 531142 · " + WCPD, {"style": "print", "label": "93rd Infantry Division in training, Fort Huachuca"}),
    (10, "two thirds of them", None, "pows_debarking_b.jpg", "10", "", "", "Army Service Forces · NARA via DPLA · " + WCPD, {"style": "print", "label": "German prisoners land at Hampton Roads, Virginia"}),
    (12, "And when they travelled", None, "pows_dadecity.jpg", "12", "", "", "NARA 23936579 · " + WCPD, {"style": "print", "label": "German prisoner of war camp, Dade City, Florida, Dec 1944"}),
    (38, "Black Army nurses", None, "huachuca_waac.jpg", "38", "", "", "NARA 531154 · " + WCPD, {"style": "print", "label": "Black WAAC officers at Fort Huachuca, 1942"}),
    (39, "By nineteen forty-four, Lena", None, "horne_fuel.jpg", "39", "", "", "NARA 535820 · " + WCPD, {"style": "print", "label": "Lena Horne, war-time poster photograph"}),
    (39, "She toured Army camps", None, "horne_tuskegee.png", "39", "", "", WCPD, {"style": "print", "label": "Lena Horne with Tuskegee Airmen"}),
    (40, "That year, she came", None, "robinson_pano.jpg", "40", "", "", "Wikib101hermann · CC BY-SA 4.0 · " + WC, {"style": "print", "label": "Camp Robinson, Arkansas, February 1943"}),
    (43, "Her daughter", None, "horne_gottlieb.jpg", "43", "", "", "William P. Gottlieb · Library of Congress · " + WCPD, {"style": "print", "label": "Lena Horne, New York, 1946-48"}),
    (54, "Lena Horne kept singing", None, "horne_gottlieb.jpg", "54", "", "", "William P. Gottlieb · Library of Congress · " + WCPD, {"style": "print", "label": "Lena Horne, New York, 1946-48"}),
    (55, "If your father", None, "huachuca_kitchen.jpg", "55", "", "", "NARA 531152 · " + WCPD, {"style": "print", "label": "A new kitchen at Fort Huachuca, December 1942"}),
]
