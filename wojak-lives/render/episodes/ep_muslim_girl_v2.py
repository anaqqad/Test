"""Life as a Muslim girl (part 2): remake of the reference format with new points, 16:9, ~80 s.

Reference style: one veiled Wojak girl over real photos, a sentence caption top-left, no voice, a sad music
loop, impact hits under the title, literal visual gags (flames, sweat, "?!"). Characters come from
draw_niqabi.py (girl_*, mom_*, aunty_red_*, aunty_green_*); men are the black-and-grey Nobo cut-outs.
Scene keys are documented in ep001_introvert.py; extra keys here: text (top-left caption), lines (title
text), fx [{t, kind: flames|sweat|question|exclaim|hearts|steam, x, y, size}].
"""
B = "bg169/"
BRO = dict(img="face_smug", size=0.78, pos=(0.83, 1.02), flip=True, enter=0.4)
MOM = dict(img="mom_angry", size=1.0, pos=(0.2, 1.14), enter=-0.4)

EPISODE = {
    "title": "LIFE AS A MUSLIM GIRL",
    "size": (1920, 1080),
    "no_title": True,
    "music": "sad",
    "scenes": [
        # ---- title card
        dict(bg=B + "alley_people.jpg", dur=4.6, char="girl_tired", pos=(0.5, 1.45),
             lines=[dict(t=0.0, text="Life as a Muslim girl", size=150, y=0.13),
                    dict(t=1.3, text="growing up in an Arab family", size=64, y=0.27)],
             labels=[dict(t=2.6, text="NOT ALL FAMILIES", x=0.5, y=0.38, size=72, rot=-6)],
             beats=[dict(t=2.6, char="girl_side", shake=0.3)],
             sfx=[dict(t=0.0, name="impact", gain=0.8), dict(t=1.3, name="impact", gain=0.6),
                  dict(t=2.6, name="thwack", gain=0.8)]),
        # ---- 1
        dict(bg=B + "small_store.jpg", char="girl_tired", pos=(0.4, 1.16),
             text="Your brother can go out at midnight. You need a permission slip to buy bread.",
             keywords=["MIDNIGHT", "PERMISSION", "SLIP"],
             extras=[dict(t=0.0, t1="55%", **BRO)],
             labels=[dict(t="55%", text="PERMISSION SLIP", x=0.72, y=0.45, size=64)],
             beats=[dict(t="55%", char="girl_angry", punch=1.12)],
             sfx=[dict(t="55%", name="thwack")]),
        # ---- 2
        dict(bg=B + "beach.jpg", char="girl_dead",
             text="Beach day: everyone goes swimming. You guard the bags.", keywords=["BAGS"],
             labels=[dict(t="45%", text="BAG SECURITY", x=0.78, y=0.55, size=64)],
             fx=[dict(t=0.4, kind="sweat", x=0.62, y=0.2, size=0.6)], sfx=[dict(t="45%", name="ding")]),
        # ---- 3
        dict(bg=B + "wedding_hall.jpg", char="girl_tired",
             text="Every wedding. Every aunty. \"Inshallah you're next!\"", keywords=["NEXT!"],
             extras=[dict(t=0.4, img="aunty_red_happy", size=0.95, pos=(0.17, 1.14), enter=-0.4),
                     dict(t=1.2, img="aunty_green_happy", size=0.95, pos=(0.84, 1.14), flip=True, enter=0.4)],
             bubbles=[dict(t=0.6, text="Inshallah you're next!", x=0.2, y=0.33, tail="down", talk=True,
                           talk_dur=0.9),
                      dict(t=1.4, text="When is YOUR turn?", x=0.8, y=0.33, tail="down", talk=True, talk_dur=0.9)],
             beats=[dict(t="70%", char="girl_roll")]),
        # ---- 4
        dict(bg=B + "wedding_hall.jpg", char="girl_side",
             text="You turn 20 and suddenly every aunty has a son who is \"a doctor\".",
             keywords=["20", "DOCTOR\"."],
             extras=[dict(t=0.6, img="aunty_red_happy", size=0.95, pos=(0.82, 1.14), flip=True, enter=0.4)],
             bubbles=[dict(t=0.9, text="My son is a doctor!", x=0.8, y=0.33, tail="down", talk=True,
                           talk_dur=0.8)],
             labels=[dict(t=2.4, text="(he is not)", x=0.8, y=0.5, size=48)],
             beats=[dict(t=2.4, char="girl_roll")]),
        # ---- 5
        dict(bg=B + "moroccan_room.jpg", char="girl_tired", pos=(0.55, 1.16),
             text="Mom: \"Cover your hair, the neighbour's son is here!\" The neighbour's son is 6.",
             keywords=["6."],
             extras=[dict(t=0.0, **MOM), dict(t="62%", img="face_shocked", size=0.45, pos=(0.85, 1.02), flip=True,
                                               enter=0.3)],
             labels=[dict(t="62%", text="AGE: 6", x=0.85, y=0.42, size=56)],
             beats=[dict(t="62%", char="girl_roll", punch=1.1)], sfx=[dict(t="62%", name="boing")]),
        # ---- 6
        dict(bg=B + "street.jpg", char="girl_happy",
             text="Laughing too loud in public = family scandal.", keywords=["SCANDAL."],
             labels=[dict(t="50%", text="SCANDAL", x=0.76, y=0.42, size=80, rot=-8)],
             beats=[dict(t="50%", char="girl_wide", punch=1.15, shake=0.35)],
             fx=[dict(t="50%", kind="exclaim", x=0.5, y=0.12, size=0.9)],
             sfx=[dict(t="50%", name="scratch", gain=0.7)]),
        # ---- 7
        dict(bg=B + "moroccan_room.jpg", char="girl_angry",
             text="Your hijab pins disappear exactly when you're already late.", keywords=["PINS", "LATE."],
             labels=[dict(t=1.2, text="PINS FOUND: 0", x=0.78, y=0.5, size=60)],
             fx=[dict(t=0.6, kind="question", x=0.5, y=0.12, size=0.8)]),
        # ---- 8
        dict(bg="bg/kitchen.jpg", char="girl_dead",
             text="Ramadan: you fast all day, then cook iftar for 12 people.", keywords=["12"],
             labels=[dict(t="55%", text="x12", x=0.78, y=0.45, size=110)],
             fx=[dict(t=0.6, kind="sweat", x=0.62, y=0.2, size=0.6), dict(t=0.3, kind="steam", x=0.15, y=0.75)]),
        # ---- 9
        dict(bg="bg/kitchen.jpg", char="girl_tired", pos=(0.4, 1.16),
             text="And your brother still asks: \"Is the food ready?\"", keywords=["READY?\""],
             extras=[dict(t=0.2, **BRO)],
             bubbles=[dict(t=0.5, text="Is the food ready?", x=0.8, y=0.4, tail="down", talk=True, talk_dur=0.9)],
             beats=[dict(t="55%", char="girl_angry", shake=0.4)],
             fx=[dict(t="55%", kind="flames", x=0.4, y=0.2, size=1.0)], sfx=[dict(t="55%", name="impact", gain=0.5)]),
        # ---- 10
        dict(bg=B + "university.jpg", char="girl_tired", pos=(0.6, 1.16),
             text="Want to study abroad? \"And who is going to watch you there?\"",
             keywords=["ABROAD?", "WATCH"],
             extras=[dict(t=0.6, **dict(MOM, img="mom_side"))],
             bubbles=[dict(t=0.9, text="Who will watch you?!", x=0.22, y=0.36, tail="down", talk=True,
                           talk_dur=0.9)],
             beats=[dict(t="60%", char="girl_sad")]),
        # ---- 11
        dict(bg=B + "university.jpg", char="girl_dead",
             text="So you pick the university 400 metres from your dad's house.", keywords=["400"],
             labels=[dict(t="50%", text="DISTANCE: 400 m", x=0.78, y=0.5, size=64)], sfx=[dict(t="50%", name="ding")]),
        # ---- 12
        dict(bg=B + "alley.jpg", char="girl_tired", pos=(0.38, 1.16),
             text="The taxi driver asks why you're not married before asking where you're going.",
             keywords=["MARRIED", "WHERE"],
             extras=[dict(t=0.2, img="face_stare", size=0.78, pos=(0.84, 1.02), flip=True, enter=0.4)],
             bubbles=[dict(t=0.6, text="Why not married yet?", x=0.8, y=0.4, tail="down", talk=True, talk_dur=0.9)],
             beats=[dict(t="65%", char="girl_roll")], sfx=[dict(t=0.1, name="horn", gain=0.4)]),
        # ---- 13
        dict(bg=B + "mall2.jpg", char="girl_tired_phone",
             text="Family group chat: your cousin saw you at the mall. ALONE.", keywords=["ALONE."],
             bubbles=[dict(t=1.2, text="Aunty: I saw her at the mall. ALONE.", style="phone", x=0.78, y=0.35,
                           tail="none")],
             beats=[dict(t=1.9, char="girl_wide_phone", punch=1.12, shake=0.3)],
             fx=[dict(t=1.9, kind="exclaim", x=0.5, y=0.12, size=0.8)],
             sfx=[dict(t=1.2, name="buzz"), dict(t=1.9, name="boing")]),
        # ---- 14
        dict(bg="bg/cafe.jpg", char="girl_happy_phone",
             text="Your Instagram: 300 photos of coffee. Zero photos of you.", keywords=["300", "ZERO"],
             labels=[dict(t="55%", text="FACE REVEAL: never", x=0.76, y=0.5, size=56)]),
        # ---- 15
        dict(bg=B + "street.jpg", char="girl_wide", pos=(0.5, 1.16),
             text="Learning to drive is a family debate. Parking is a family emergency.",
             keywords=["DEBATE.", "EMERGENCY."],
             extras=[dict(t=0.8, **MOM), dict(t=1.4, img="aunty_green_angry", size=0.95, pos=(0.84, 1.14),
                                               flip=True, enter=0.4)],
             bubbles=[dict(t=1.0, text="LEFT! LEFT!", x=0.2, y=0.36, tail="down", talk=True, talk_dur=0.7),
                      dict(t=1.7, text="NO, YOUR OTHER LEFT!", x=0.8, y=0.36, tail="down", talk=True,
                           talk_dur=0.9)],
             fx=[dict(t="60%", kind="sweat", x=0.62, y=0.2, size=0.6)],
             sfx=[dict(t=0.4, name="horn", gain=0.4), dict(t="60%", name="horn", gain=0.5)]),
        # ---- 16
        dict(bg=B + "wedding_hall.jpg", char="girl_dead",
             text="Cousin's wedding: 4 days, 9 outfits, and getting ready starts at 6 a.m.",
             keywords=["4", "9", "6"],
             labels=[dict(t=1.0, text="DAY 4", x=0.2, y=0.45, size=64), dict(t=1.8, text="OUTFIT 9", x=0.8, y=0.45,
                                                                            size=64),
                     dict(t=2.6, text="06:00", x=0.5, y=0.62, size=72)],
             sfx=[dict(t=1.0, name="pop"), dict(t=1.8, name="pop"), dict(t=2.6, name="pop")]),
        # ---- 17
        dict(bg="bg/cafe.jpg", char="girl_tired",
             text="Strangers assume you can't speak English. Then you correct their grammar.",
             keywords=["ENGLISH.", "GRAMMAR."],
             bubbles=[dict(t="60%", text="*whom, actually.", x=0.78, y=0.4, tail="down-left")],
             beats=[dict(t="60%", char="girl_side", punch=1.12)], sfx=[dict(t="60%", name="ding")]),
        # ---- 18 warm ending
        dict(bg=B + "moroccan_room.jpg", char="girl_happy", pos=(0.6, 1.16),
             text="But nobody, NOBODY, makes Friday couscous like Mom.", keywords=["NOBODY,", "COUSCOUS"],
             extras=[dict(t=0.0, **dict(MOM, img="mom_happy"))],
             fx=[dict(t=0.8, kind="hearts", x=0.42, y=0.45, size=0.8)], hold=1.0),
        # ---- end
        dict(bg=B + "moroccan_room.jpg", blur=12, char="girl_happy", pos=(0.5, 1.4), dur=2.6,
             labels=[dict(t=0.2, text="PART 3?", x=0.5, y=0.3, size=110)], sfx=[dict(t=0.2, name="thwack")]),
    ],
}
