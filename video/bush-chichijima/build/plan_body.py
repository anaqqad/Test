
# ── shots: sh() adds the film's source tag when the film changes; tag=False for a repeat, or a custom tag ──
TAG = {"RES": RES_TAG, "SJ": SJ_TAG, "SJA": SJA_TAG, "IND": IND_TAG, "INO": INO_TAG, "AVR": AVR_TAG, "TIG": TIG_TAG,
       "SUA": SU_TAG, "SUB": SU_TAG, "SUC": "Japanese envoys aboard USS Dunlap off Chichi Jima, 31 Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)",
       "B24A": B24_TAG, "B24B": "Chichi Jima from an AAF B-24, 22 March 1945 · AAF combat film (CS-3618)", "CJB": CJB_TAG,
       "FLA": FL_TAG, "FLB": FL_TAG, "KWA": KWA_TAG, "WOL": WOL_TAG, "K8": K8_TAG, "PH91": PH_TAG, "ST": ST_TAG, "PM": PM_TAG,
       "IV86": "Vice President George H.W. Bush, interview on his naval service, 19 June 1986 · White House Television (Reagan Library, NARA)",
       "STF": "President George H.W. Bush, White House interview on his war service, 2 June 1992 · White House Television (George Bush Library)"}
GENERIC = {"SJA", "IND", "INO", "AVR", "TIG", "FLA", "FLB", "KWA", "WOL", "B24A", "SUC"}  # not the event itself: marked as stand-ins


def sh(anchor, key, t, tag=True):
    film = "ST" if key == "STF" else key
    out = [(anchor, film, t)]
    if tag:
        txt = tag if isinstance(tag, str) else ((STAND if key in GENERIC else "") + TAG[key])
        out.append(("@", anchor, txt))
    return out


def card(anchor, c, until=None):
    return [("#", anchor, until, c)]


def LDOC(file, head, spans, source):
    return {"type": "LedgerDocument", "file": file, "head": head, "source": source, "spans": [{"doc": d, "say": s} for d, s in spans]}


P = [
    # 0 the raft
    sh("The Pacific Ocean", "RES", 44.8) + card("The Pacific Ocean", SLUG("2 September 1944 · late morning", "Off Chichi Jima, Bonin Islands")) +
    sh("A few miles off", "CJB", 43.5) + sh("Minutes earlier", "FLA", 113.5, STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("He paddles as hard", "AVR", 12.5),
    # 1 the periscope
    sh("Above him", "SUC", 79.3, STAND + "Hellcats low over the sea off Chichi Jima, Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)") + sh("Then, a little before noon", "RES", 16.8) +
    sh("First a periscope", "TIG", 113.5) + sh("Sailors run out", "RES", 17.6) + sh("and up on the conning", "RES", 42.6, False),
    # 2 the patrol report (LedgerDocument)
    sh("The submarine's captain", "RES", 27.2) + sh("It gives the time", "AVR", T(1, 58.0)) + card("The submarine's captain", LDOC("FROM THE FILE · USS FINBACK", "Patrol report, 2 Sept 1944, 1156",
        [("fin_rescue", "he failed to see his crew's parachutes and believed they had jumped when plane was still over")], FINR)),
    # 3 two young men
    sh("Two young men", "IND", 12.5) + sh("And on the island", "CJB", 19.5) + sh("What happened to those", "B24B", T(2, 51.0)),
    # 4 documented story
    sh("This is the documented", "RES", 38.0) + sh("the squadron's secret", "SJ", T(1, 22.0)) + sh("Where the papers agree", "IV86", T(6, 0.0)),
    # 5 three claims
    sh("You will often read", "FLA", 114.0, STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("that he sat in the raft", "RES", 23.2) +
    sh("and that his crew", "IND", 13.5) + sh("The file backs one", "IV86", T(6, 20.0)),
    # 6 the file
    sh("A man who later became", "IV86", T(7, 0.0)) + sh("To them he was one pilot", "SJ", T(1, 36.0)),
    # 7 the documents
    sh("The first is Form", "IND", T(2, 38.0)) + card("The first is Form", DESK("stills/doc_aar_s1_paper.png", 1.3306, [(0, "wide", [0.5, 0.3]), ("stamped secret", "heading", [0.78, 0.04]),
        ("five sheets", "glide", [0.12, 0.2, 0.7])], AAR)) + sh("The second is the war patrol", "TIG", 63.5) + sh("The third is a small", "IND", T(2, 47.5)),
    # 8 the fourth file
    sh("The fourth file", "SUA", T(1, 13.5)) + sh("Bush never appears", "CJB", 31.5) + sh("But it describes", "CJB", 43.8, False),
    # 9 7 Dec 1941
    sh("The story starts", "IV86", T(1, 30.0)) + card("The story starts", SLUG("7 December 1941", "Phillips Academy, Andover, Massachusetts")) + sh("He heard the news", "IV86", T(2, 10.0), False),
    # 10 CLIP Kilo 8
    sh("Like all American", "K8", 8.5),
    # 11 seaman second class
    sh("Seaman second class", "WOL", 6.5) + sh("He had signed up", "WOL", 74.5, False),
    # 12 preflight
    sh("The Navy turned schoolboys", "WOL", 14.5) + sh("Bush started at", "WOL", 54.5, False) + sh("Then came primary", "WOL", T(2, 35.0), False) + sh("His logbook shows", "WOL", T(2, 47.0), False),
    # 13 commissioned
    sh("From there he went", "WOL", T(3, 30.0)) + sh("He was one of the youngest", "IND", 66.5),
    # 14 Avenger, Sable
    sh("He was sent to fly", "IND", 0.5) + sh("He learned it", "IND", 99.5, False) + sh("In August", "WOL", T(3, 0.5), STAND + "USS Wolverine, a Lake Michigan training carrier like Sable, 1943 · U.S. Navy film (NARA NPC-5074)") +
    sh("A stamp in his logbook", "WOL", T(3, 20.5), False),
    # 15 VT-51
    sh("That September", "IND", T(2, 17.5)) + sh("Ensign Bush became", "IND", 12.5, False),
    # 16 San Jacinto
    sh("The squadron's ship", "SJ", T(0, 55.5)) + sh("She was a light carrier", "SJ", T(1, 7.5), False) + sh("fast, narrow", "SJ", T(1, 47.5), False),
    # 17 three men
    sh("The Avenger carried", "IND", 13.0) + sh("Behind him", "FLB", 80.5) + sh("Down in the belly", "IND", T(2, 18.0)) + sh("He talked to them", "FLB", 87.5),
    # 18 crew
    sh("Bush's regular crew", "FLB", 60.0) + sh("The three of them", "FLB", 66.0, False),
    # 19 Barbara
    sh("In December", "IND", T(2, 38.5)) + sh("He named his planes", "FLA", T(2, 22.0)),
    # 20 Wake
    sh("reached the war", "INO", T(5, 38.5)) + card("reached the war", WAR44) + sh("Bush's logbook marks", "INO", T(5, 2.0), False),
    # 21 roommate
    sh("The same operation", "SJ", 3.0, "Burial at sea aboard USS San Jacinto, Feb 1944 (not Wykes) · U.S. Navy film (NARA NPC-1521)") + sh("Forty-seven years later", "SJ", 20.0, False),
    # 22 CLIP Pearl 1991
    sh("My roommate", "PH91", 10.1),
    # 23 Marianas
    sh("In June the carriers", "SJA", 13.5) + sh("On the fifteenth of June", "FLB", T(2, 30.5)),
    # 24 Philippine Sea
    sh("Four days later", "SJA", 21.5) + sh("American fighter pilots", "SJA", T(2, 58.2), False) + sh("For Bush it was", "IND", 56.3),
    # 25 red ink
    sh("His logbook entry", "IND", 51.0) + sh("Emergency crash landing", "AVR", 62.5),
    # 26 Bronson
    sh("He set the crippled", "AVR", 66.0) + sh("For the next four days", "SJ", T(3, 2.0)),
    # 27 back to work
    sh("Then it was back", "KWA", 20.5) + sh("On the twenty-fifth", "FLB", 36.5) + sh("On the first of August", "KWA", 6.5) + sh("He had already been lucky", "KWA", 16.0, False),
    # 28 the Bonins
    sh("At the end of August", "CJB", T(1, 49.5)) + card("At the end of August", BONINS) + sh("The Japanese called", "SUA", T(1, 1.5)) + sh("and it mattered", "CJB", 44.0, False),
    # 29 fortress
    sh("The island was a fortress", "SUA", T(1, 13.5)) + sh("The Navy had a base", "SUA", T(1, 2.0), False) + sh("The prosecutor's opening", "CJB", 31.5),
    # 30 Woellhof (DocDesk on the trial page)
    sh("The same record shows", "CJB", 19.6) + card("On or about the fourth", DESK("stills/doc_trial_p2_paper.png", 1.7076, [(0, "wide", [0.5, 0.6]),
        ("He was Lloyd", "glide", [0.6, 0.15, 0.75])], TRIAL + ", prosecution opening, p. F-2")),
    # 31 garage, Aug 1944
    sh("The record says", "SUB", T(3, 28.0)) + sh("Then, on or about", "CJB", T(1, 32.0)) + sh("Nobody in Bush's squadron", "SJA", T(1, 5.5)) + sh("To the pilots", "SJA", T(1, 9.5), False),
    # 32 lifeguard idea
    sh("The Navy did know", "AVR", 3.5) + sh("So when the carriers struck", "TIG", 114.0),
    # 33 Finback sails
    sh("On the sixteenth of August", "TIG", 47.5) + card("On the sixteenth of August", FINBACK),
    # 34 1 Sept
    sh("On the first of September", "TIG", 103.0) + sh("The same day", "IND", 67.0) + sh("His logbook says", "KWA", 16.3),
    # 35 Strike Baker
    sh("On the morning", "INO", T(5, 39.0)) + card("On the morning", SLUG("2 September 1944 · Strike Baker", "VT-51, USS San Jacinto · target: radio station, Chichi Jima")) +
    sh("The target was", "CJB", 31.8) + sh("Four Avengers would", "FLB", T(2, 58.5)) + sh("escorted by twelve", "INO", 21.5),
    # 36 Ted White
    sh("That morning Bush's crew", "FLB", 81.0) + sh("In his place", "IND", 14.0) + sh("He was twenty-six", "IND", T(2, 19.0), False) + sh("took his usual seat", "FLB", 90.0),
    # 37 take-off
    sh("According to the action report", "IND", 1.0) + sh("In the lead", "IND", 99.5, False) + sh("The weather was good", "FLA", 1.0),
    # 38 push-over
    sh("At about twenty-five", "KWA", 21.0) + sh("and pushed over", "FLA", 20.0) + sh("The report describes", "SJA", T(1, 5.5)),
    # 39 the line (LedgerDocument)
    sh("and the second pilot", "CJB", T(1, 13.5), "Bombs on Chichi Jima, 27 Sept 1944, three weeks after Bush's strike · Signal Corps film (111-ADC-1817)") +
    card("Then the report turns", LDOC("FROM THE FILE · VT-51 ACTION REPORT", "Sheet 4: the dive",
        [("aar_fire", "In spite of this hit which caused his engine to smoke and catch on fire Lieutenant junior grade Bush continued in his dive releasing his bombs on the radio station")], AAR)),
    # 40 1992 intro
    sh("Forty-eight years later", "STF", 540.5),
    # 41 CLIP dive
    sh("About halfway", "ST", 553.7),
    # 42 the DFC
    sh("In other words", "FLA", T(2, 45.0)) + sh("He held a diving plane", "FLA", T(3, 4.0), False) +
    card("That is what his", LQ("FILE 03 — THE CITATION", "DISTINGUISHED FLYING CROSS · LT.(JG) G.H.W. BUSH", "in spite of smoke and flames from the fire in his plane, he continued in his dive",
        "Commander, Second Carrier Task Force, Pacific, December 1944", DFC, after=" …")),
    # 43 turn east
    sh("After the bombs fell", "FLA", T(1, 54.0), STAND + "Smoke over a carrier strike, 1944 · U.S. Navy film (NARA NPC-2658)") + sh("He told his skipper", "KWA", T(1, 40.5), False) + sh("He also ordered", "KWA", T(1, 44.5)),
    # 44 the bail-out (LedgerDocument, two spans)
    sh("Then the report says", "AVR", T(1, 58.0)) + card("Then the report says", LDOC("FROM THE FILE · VT-51 ACTION REPORT", "Sheet 4: the bail-out",
        [("aar_bail", "Bush and one other person were seen to bail out"), ("aar_chute", "The chute of the other person either Lieutenant junior grade White or J L")], AAR)),
    # 45 incomplete
    sh("The report adds", "AVR", T(2, 3.0)) + sh("And it closes", "AVR", T(2, 12.0), False),
    # 46 1992 intro 2
    sh("In the same", "STF", 598.0),
    # 47 CLIP bail
    sh("Told them to bail", "ST", 609.7),
    # 48 the tail
    sh("Bush himself had hit", "AVR", 12.8) + sh("He came down", "AVR", 35.0, False),
    # 49 fighters overhead
    sh("From the air", "SUC", 79.5, STAND + "Hellcats low over the sea off Chichi Jima, Aug 1945 · U.S. Navy film (NARA 428-NPC-17062)") + sh("Somewhere off the island", "TIG", 115.0),
    # 50 reconstruction chart
    sh("Her patrol report", "TIG", 116.0, False) + card("Her patrol report", STRIKE),
    # 51 the film
    sh("At four minutes", "RES", 22.9) + sh("A sailor named", "RES", 27.1, False) + sh("This is that film", "RES", 31.3, False) + sh("It runs less", "RES", 37.8, False),
    # 52 how long
    sh("How long was Bush", "RES", 41.6) + sh("Popular accounts", "RES", 44.8, False) + sh("Either way", "AVR", T(1, 58.0)),
    # 53 CLIP raft
    sh("I remember being sick", "ST", 748.95),
    # 54 search
    sh("The submarine did not leave", "RES", 45.0) + sh("Her report says", "AVR", T(1, 36.0)) + sh("She found nothing", "AVR", T(2, 6.0)),
    # 55 what does the file say
    sh("So, what does the file", "IV86", T(13, 15.0)),
    # 56 two reports (desk)
    sh("The squadron report", "IND", 99.5) + card("The squadron report", DESK("stills/doc_aar_s4_paper.png", 1.3235, [(0, "wide", [0.5, 0.45]), ("says Bush and one", "glide", [0.5, 0.3, 0.8])], AAR)),
    # 57 Beckman (desk)
    sh("And there is a third", "AVR", 53.5) + card("Once aboard", DESK("stills/doc_finback_beckman_paper.png", 1.3594, [(0, "wide", [0.5, 0.15]), ("The report says it", "glide", [0.11, 0.3, 0.8])], FINR)),
    # 58 the logbook (desk)
    sh("Bush's own logbook", "INO", T(4, 16.5)) + card("On the line", DESK("stills/doc_logbook_paper.png", 0.7915, [(0, "wide", [0.5, 0.2]),
        ("the plane's number", "glide", [0.08, 0.1, 0.5]), ("and then", "heading", [0.78, 0.07])], LOG)),
    # 59 on patrol
    sh("Finback could not", "RES", 43.7) + sh("So for about a month", "TIG", T(2, 9.0)),
    # 60 watches
    sh("He stood watches", "TIG", 63.0) + sh("He was there when", "TIG", 103.5, False) + card("Forty-eight years later", WATCH),
    # 61 the letter
    sh("From the submarine", "RES", 45.5) + card("From the submarine", LETTER) + sh("He wrote that there", "TIG", 63.5),
    # 62 Midway
    sh("On the thirtieth", "TIG", 88.5, STAND + "A lifeguard submarine ties up with rescued airmen, Guam, July 1945 · U.S. Navy film (NARA 428-NPC-14153)") + sh("A Navy photographer", "TIG", T(2, 8.5), False),
    # 63 back
    sh("From Midway", "INO", T(5, 2.0)) + card("From Midway", HOMEBACK),
    # 64 eight more
    sh("He flew eight more", "FLB", 61.0) + sh("including strikes", "FLA", T(3, 32.0)) + sh("By the end of its tour", "FLB", T(1, 47.0)),
    # 65 decorations
    sh("In all, his file", "IND", 67.5) + card("In all, his file", MISSIONS, "He was awarded") + sh("He was awarded", "SJ", T(2, 16.0)) + sh("On the sixth of January", "IV86", T(0, 20.0)),
    # 66 VT-153, totals
    sh("He spent the rest", "IND", T(1, 57.0)) + sh("The last page", "IND", 67.0, False),
    # 67 subscribe
    sh("If you want more", "INO", T(5, 3.0)) + card("If you want more", {"type": "SubscribeButton", "channel": "WWII Frontlines", "tagline": "Prisoner of war stories, documented"}) +
    sh("And now, back", "SUA", T(1, 2.5)),
    # 68 Feb 1945
    sh("In February", "B24B", T(2, 41.8)) + sh("this time to cover", "B24B", T(2, 50.6), False) + sh("On the eighteenth", "B24B", T(2, 55.6), False),
    # 69 Randolph
    sh("An Avenger from the carrier", "FLB", T(4, 9.0)) + sh("Their gunner", "CJB", 31.5),
    # 70 Bennington
    sh("Another Avenger", "FLA", 2.0) + sh("Its pilot ditched", "AVR", 4.0) + sh("His two crewmen", "CJB", 20.5),
    # 71 Vaughn
    sh("Then, on the twenty-third", "B24A", 82.6) + sh("On the island he was", "B24B", T(2, 51.0)) + sh("The two became friends", "CJB", 44.5),
    # 72 the record
    sh("The trial record describes", "CJB", T(1, 32.0)) + sh("These are the facts", "CJB", T(1, 40.0), False),
    # 73 shelter (LedgerDocument)
    sh("were taken to General", "SUB", T(3, 28.0)) + card("were taken to General", LDOC("FROM THE FILE · THE TRIAL RECORD", "Prosecution opening, p. F-3",
        [("trial_shelter", "ordered not to give the prisoners shelter food nor water")], TRIAL)),
    # 74 executions
    sh("On or about the twenty-third", "SUA", T(1, 14.0)) + sh("York was put", "CJB", 21.5) + sh("Dye was kept alive", "CJB", 34.0, False) + sh("Hall was executed", "SUB", T(5, 20.0)),
    # 75 cannibalism
    sh("The trial record also", "SUB", T(5, 30.0)) + sh("The prosecution said", "CJB", T(1, 44.0)),
    # 76 the eight
    sh("In all, eight", "AVR", T(1, 57.0)) + card("In all, eight", EIGHT),
    # 77 cover story
    sh("When the war ended", "SUA", 42.0) + sh("American investigators", "SUC", T(4, 29.5)) + sh("or sent away", "SUC", T(5, 43.5), False),
    # 78 Savory, Rixey
    sh("The story did not hold", "SUB", T(3, 30.0)) + sh("On the twenty-first", "SUC", T(2, 29.5)),
    # 79 Matoba testifies
    sh("On the seventh of January", "SUA", T(4, 35.5)) + card("He admitted ordering", MATOBA),
    # 80 Guam
    sh("The cases were tried", "TIG", T(3, 35.5), STAND + "Guam, July 1945 · U.S. Navy film (NARA 428-NPC-14153)") + card("The cases were tried", GUAMTRIAL),
    # 81 the charges
    sh("The charges were murder", "TIG", T(3, 36.0)) + sh("One problem had", "SUA", T(4, 28.0), "Japanese officers aboard USS Dunlap, 3 Sept 1945 · U.S. Navy film (NARA 428-NPC-17059)"),
    # 82 Flynn (LedgerDocument)
    sh("The prosecutor", "SUA", T(4, 36.0), False) + card("The prosecutor", LDOC("FROM THE FILE · THE TRIAL RECORD", "Opening argument for the prosecution",
        [("trial_revolting", "so revolting to the human mind that man long ago decided it unnecessary to legislate directly against their commission")], TRIAL)),
    # 83 never again
    sh("He went on", "SUA", T(5, 44.0), False) + card("He went on", FLYNN),
    # 84 Time
    sh("It was not a secret", "TIG", T(3, 40.0)) + sh("But the Navy did not", "AVR", T(2, 0.0)),
    # 85 verdicts
    sh("Of the fourteen", "SUA", T(5, 46.0)) + sh("received a life sentence", "SUA", T(4, 40.0), False),
    # 86 hanged
    sh("On the twenty-fourth", "SUB", T(5, 18.0)) + sh("The Navy's own", "SUB", T(5, 33.0), False),
    # 87 surrender, 1945
    sh("Two years before", "SUA", T(1, 25.0)) + sh("A Navy cameraman", "SUA", T(2, 23.2), "Surrender of the Bonin Islands aboard USS Dunlap, 3 Sept 1945 · the senior officer is probably Lt. Gen. Tachibana · U.S. Navy film (NARA 428-NPC-17059)") +
    sh("and signing", "SUA", T(5, 59.5), False) + sh("It was one day after", "SUA", T(6, 12.0), False),
    # 88 the gunner
    sh("when Bush was running", "IV86", T(11, 35.0)) + sh("A former Torpedo", "FLB", 62.0) + card("He said the plane", GUNNER),
    # 89 absurd
    sh("Bush's campaign", "STF", 525.0) + card("In 2003", BURNING),
    # 90 what the file shows
    sh("So what does the file show", "IND", 100.0) + sh("comes from one man", "FLB", 64.0),
    # 91 parachutes
    sh("On the parachutes", "AVR", T(1, 35.5)) + sh("Whether Ted White", "AVR", T(2, 8.0)) + sh("That is the honest", "AVR", T(2, 16.0), False),
    # 92 verdict
    sh("So here are the three", "SJ", T(1, 7.5)) + sh("The four hours in", "SJ", T(3, 2.0), False) + card("So here are the three", VERDICT),
    # 93 declared dead
    sh("were officially declared", "AVR", T(1, 58.5)) + sh("the gunner who stayed", "IND", T(2, 48.0)),
    # 94 scrapped
    sh("Finback was decommissioned", "TIG", 64.0) + sh("was scrapped in", "SJ", T(2, 49.5)) + sh("guard and friend", "CJB", 45.5),
    # 95 1984
    sh("On the second of September", "IV86", T(3, 10.0)),
    # 96 2002
    sh("In June 2002", "SUB", T(3, 32.0)) + card("He dropped wreaths", BOYS),
    # 97 died
    sh("George Herbert Walker Bush died", "STF", 900.0),
    # 98 your family
    sh("Torpedo Squadron Fifty-One, the", "FLB", 66.5) + sh("If your father", "IND", 104.0),
    # 99 today
    sh("went back to Japan", "SUB", T(5, 17.5)) + sh("Boats come and go", "SUA", T(1, 2.0)) + sh("and in a bay", "AVR", T(1, 59.0)),
    # 100 the place
    sh("Somewhere off the north-east", "AVR", T(1, 57.5)) + sh("There is no marker", "AVR", T(1, 36.5), False) + card("There is only the line", DESK("stills/doc_logbook_paper.png", 0.7915, [(0, "heading", [0.75, 0.07]), ("crash landing", "glide", [0.07, 0.62, 0.95])], LOG)),
]

PC = f"U.S. Navy · public domain · {WC}"
BL = "George Bush Presidential Library and Museum · NARA · public domain"
PHOTOS = [
    (3, "Two young men", None, "bl_H080-01.jpg", "03", "", "", BL, {"style": "print", "label": "John Delaney, Leo Nadeau and George Bush"}),
    (4, "the pilot's own logbook", None, "doc_logbook_cover.png", "04", "", "", LOG, {"style": "print", "label": "Bush's Aviator's Flight Log Book"}),
    (4, "and the record of", None, "trial_folder_tab.jpg", "04", "", "", TRIAL, {"style": "print", "label": "U.S. v. Tachibana et al., case file"}),
    (6, "But the papers", None, "bush_flight_gear.jpg", "06", "", "", f"U.S. Navy · NARA 186380 · public domain · {WC}", {"style": "print", "label": "Lt.(jg) George H.W. Bush, Navy pilot, 1944"}),
    (7, "The third is a small", None, "doc_logbook_cover.png", "07", "", "", LOG, {"style": "print", "label": "Aviator's Flight Log Book, 'Bush G.H.W.'"}),
    (8, "a case called", None, "trial_folder_tab.jpg", "08", "", "", TRIAL, {"style": "print", "label": "'Tachibana, Yoshio et al.' · Navy JAG, Pacific war crimes trials"}),
    (11, "He had signed up", None, "bl_H077.jpg", "11", "", "", BL, {"style": "print", "label": "George Bush as a naval aviation cadet"}),
    (12, "Bush started at", None, "corpus_christi_cadets.jpg", "12", "", "", f"U.S. Navy · NARA 520975 · public domain · {WC}", {"style": "print", "label": "Aviation cadets check the flight boards, NATC Corpus Christi"}),
    (13, "On the ninth of June", None, "bush_flight_gear.jpg", "13", "", "", f"U.S. Navy · NARA 186380 · public domain · {WC}", {"style": "print", "label": "George Bush, naval aviator"}),
    (15, "That September", None, "bl_H048.jpg", "15", "", "", BL, {"style": "print", "label": "Torpedo Squadron 51 (VT-51)"}),
    (16, "commissioned at Philadelphia", None, "sanjac_philly.jpg", "16", "", "", f"U.S. Navy · NH 43506 · public domain · {WC}", {"style": "print", "label": "USS San Jacinto (CVL-30), Philadelphia, January 1944"}),
    (17, "The pilot sat up front", None, "bush_cockpit_wide.jpg", "17", "", "", f"U.S. Navy · NARA 186383 · public domain · {WC}", {"style": "print", "label": "Bush in the cockpit of his TBM Avenger"}),
    (18, "His radioman was", None, "bl_H080-01.jpg", "18", "", "", BL, {"style": "print", "label": "John 'Del' Delaney (left), Leo Nadeau and George Bush"}),
    (19, "He named his planes", None, "bush_cockpit_wide.jpg", "19", "", "", f"U.S. Navy · NARA 186383 · public domain · {WC}", {"style": "print", "label": "'Barbara' painted on the side of a Bush Avenger"}),
    (23, "Marines invaded", None, "doc_logbook_jun44.png", "23", "", "", LOG, {"style": "print", "label": "Logbook, June 1944: 'Marines invaded Saipan'"}),
    (25, "is written in red ink", None, "doc_logbook_jun44.png", "25", "", "", LOG, {"style": "print", "label": "Logbook, 19 June 1944, in red: 'Emergency crash landing in sea near Guam'"}),
    (27, "Bush and another pilot", None, "vt51_majuro.jpg", "27", "", "", PC, {"style": "print", "label": "A VT-51 Avenger over Majuro, May 1944"}),
    (29, "An Army brigade", None, "chichi_fortress_hq.jpg", "29", "", "", f"Public domain · {WC}", {"style": "print", "label": "Japanese brigade headquarters, Chichi Jima"}),
    (29, "The prosecutor's opening", None, "ams_chichi_map.jpg", "29", "", "", f"U.S. Army Map Service, 1943-44 · public domain · {WC}", {"style": "print", "label": "U.S. Army map of Chichi Jima"}),
    (32, "could be saved", None, "kingfisher_truk.jpg", "32", "", "", f"U.S. Navy · 80-G-227991 · public domain · {WC}", {"style": "print", "label": "Downed airmen await a lifeguard submarine, Truk, May 1944"}),
    (33, "She had a new captain", None, "bl_H062.jpg", "33", "", "", BL, {"style": "print", "label": "USS Finback (SS-230)"}),
    (34, "Finback picked up", None, "harder_rescue.jpg", "34", "", "", PC, {"style": "print", "label": "A submarine picks up a downed pilot (USS Harder, Woleai, 1944)"}),
    (35, "Four Avengers would", None, "vt51_takeoff_jun44.jpg", "35", "", "", f"U.S. Navy · 80-G-238783 · public domain · {WC}", {"style": "print", "label": "A VT-51 TBM-1C takes off from San Jacinto, June 1944"}),
    (36, "In his place", None, "vt51_launch_may44.jpg", "36", "", "", PC, {"style": "print", "label": "VT-51 Avenger launch, USS San Jacinto, May 1944"}),
    (37, "In the lead", None, "tbm_saipan.jpg", "37", "", "", f"U.S. Navy · 80-G-428459 · public domain · {WC}", {"style": "print", "label": "TBM-1C Avenger, the model Bush flew, June 1944"}),
    (43, "smoke and flames", None, "tbm_flak_damage.jpg", "43", "", "", f"U.S. Navy · NH 89380 · public domain · {WC}", {"style": "print", "label": "Stand-in · a flak-damaged Avenger, 1945 (not Bush's)"}),
    (45, "the words every family", None, "doc_casualty_list.jpg", "45", "", "", f"NARA 305178 · public domain · {WC}", {"style": "print", "label": "Casualty list by aircraft type, TBM-1C, 2 Sept 1944"}),
    (51, "This is that film", None, "bush_rescue_400dpi.jpg", "51", "", "", BL, {"style": "print", "label": "Frame from the rescue film: Bush pulled aboard Finback"}),
    (59, "with five rescued", None, "finback_officers_aviators.jpg", "59", "", "", BL, {"style": "print", "label": "The rescued airmen with Finback's officers"}),
    (62, "A Navy photographer", None, "finback_officers_aviators.jpg", "62", "", "", BL, {"style": "print", "label": "Midway, 30 Sept 1944: Bush kneels second from left"}),
    (65, "received the Presidential", None, "bl_H079-02.jpg", "65", "", "", BL, {"style": "print", "label": "USS San Jacinto"}),
    (66, "The last page", None, "doc_logbook_totals.png", "66", "", "", LOG, {"style": "print", "label": "Logbook totals: 1,228.3 hours, 126 carrier landings"}),
    (68, "this time to cover", None, "b24_chichi_harbour.jpg", "68", "", "", f"U.S. Army Air Forces · NARA 204981413 · public domain", {"style": "print", "label": "B-24s over Chichi Jima harbour, Nov 1944"}),
    (75, "The trial record also", None, "marines_search_1946.jpg", "75", "", "", f"U.S. Marine Corps · public domain · {WC}", {"style": "print", "label": "Marines search for the remains of murdered airmen, Chichi Jima, 1946"}),
    (78, "Among the people", None, "futami_1920s.jpg", "78", "", "", f"Public domain · {WC}", {"style": "print", "label": "Futami harbour, Chichi Jima, 1920s"}),
    (80, "The main case opened", None, "guam_trial_building.jpg", "80", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "The war crimes trial building, Guam"}),
    (81, "There were thirty-eight", None, "trial_folder_tab.jpg", "81", "", "", TRIAL, {"style": "print", "label": "Case file: 'Tachibana, Yoshio et al.'"}),
    (81, "So the Navy lawyers", None, "koso_abe_guam.jpg", "81", "", "", f"NARA · public domain · {WC}", {"style": "print", "label": "A defendant before the Navy commission, Guam, 1947 (another case)"}),
    (85, "was sentenced to death", None, "guam_sentence.jpg", "85", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "A sentence is read, Navy war crimes commission, Guam"}),
    (87, "It was one day after", None, "tachibana_surrender.jpg", "87", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Lt. Gen. Tachibana signs the surrender of the Bonins, USS Dunlap, 3 Sept 1945"}),
    (93, "Their names are carved", None, "bl_H080-01.jpg", "93", "", "", BL, {"style": "print", "label": "John Delaney (left), Leo Nadeau and George Bush"}),
    (94, "Finback was decommissioned", None, "finback_launch.jpg", "94", "", "", f"U.S. Navy · NARA · public domain · {WC}", {"style": "print", "label": "USS Finback launched, Portsmouth, 1941"}),
    (94, "was scrapped in", None, "sanjac_underway.jpg", "94", "", "", f"U.S. Navy · 80-G-212798 · public domain · {WC}", {"style": "print", "label": "USS San Jacinto, January 1944"}),
    (95, "forty years to the day", None, "bush_1984_anniv.jpg", "95", "", "", "White House photo · George Bush Library · NARA · public domain", {"style": "print", "label": "Vice President Bush, 2 Sept 1984, forty years after"}),
    (95, "The signatures are still", None, "doc_logbook_sig1984.png", "95", "", "", LOG, {"style": "print", "label": "Logbook: 'Sept 2, 1984 · 40 years later'"}),
    (96, "In June 2002", None, "bush_2002_japan.jpg", "96", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Former President Bush in Japan, June 2002"}),
    (97, "George Herbert Walker Bush died", None, "bush_1994_tbm.jpg", "97", "", "", f"U.S. Navy · public domain · {WC}", {"style": "print", "label": "Bush in an Avenger cockpit again, 1994"}),
    (98, "If your father", None, "bl_H048.jpg", "98", "", "", BL, {"style": "print", "label": "Torpedo Squadron 51"}),
    (99, "Today it belongs", None, "futami_pano.jpg", "99", "", "", f"CC BY-SA 3.0 · {WC}", {"style": "print", "label": "Futami Bay, Chichi Jima, today"}),
    (99, "and in a bay", None, "hinko_maru_wreck.jpg", "99", "", "", f"CC0 · {WC}", {"style": "print", "label": "Wreck of the Hinko Maru, Chichi Jima"}),
]
