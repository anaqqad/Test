"""EP001: Life as an Introvert (draft render). Script: wojak-lives/episodes/01-introvert.md

Scene keys (all optional except bg):
  bg, tint ("night"|"warm"), blur        background photo in render/assets/bg/
  vo                                     narrator line (Piper TTS) and the auto captions
  keywords                               caption words drawn in yellow
  lead, hold, dur                        seconds before the VO / after it / fixed scene length
  char, pos, size, flip, char_tint       lead character cut-out from brand/nobo/ (face_*, bust_*)
  beats   [{t, char, punch, shake, pos, size, flip, tint, unpunch}]
  bubbles [{t, t1, text, x, y, style: speech|phone, tail: down-left|down-right|down|none, talk, talk_dur}]
  labels  [{t, t1, text, x, y, size, rot}]     yellow sticker tags
  extras  [{t, t1, img, pos, size, flip, tint: npc|light, enter}]   other characters
  sfx     [{t, name, gain}]  names: thwack boing pop whoosh scratch slide_down buzz tick sting door talkN
  push, exit {t, dx, d}, cap_y, no_title
"""
NIGHT = dict(bg="bedroom.jpg", tint="night")

EPISODE = {
    "title": "LIFE AS AN INTROVERT",
    "voice_speed": 1.08,
    "scenes": [
        dict(**NIGHT, char="face_stare", lead=0.9,
             vo="Every introvert's horror movie starts with one text.", keywords=["HORROR", "TEXT"],
             bubbles=[dict(t=0.15, text="party at mine tonight. you're coming :)", style="phone", x=0.5, y=0.43,
                           tail="none")],
             beats=[dict(t=0.9, char="face_shocked", punch=1.18, shake=0.25)],
             sfx=[dict(t=0.15, name="buzz"), dict(t=0.9, name="boing")]),
        dict(**NIGHT, char="face_forced_smile",
             vo="And my thumbs said sure, before my brain could stop them.", keywords=["SURE"],
             bubbles=[dict(t="45%", text="haha sure!!", style="phone", x=0.62, y=0.43, tail="none")],
             sfx=[dict(t="45%", name="whoosh")]),
        dict(**NIGHT, char="face_stare", char_tint="light",
             vo="Now I have six hours to prepare. Emotionally. Like an astronaut.", keywords=["SIX", "ASTRONAUT"],
             labels=[dict(t=0.3, text="T-MINUS 6:00:00", x=0.5, y=0.43)],
             sfx=[dict(t=0.3, name="tick"), dict(t=0.8, name="tick"), dict(t=1.3, name="tick")]),
        dict(bg="bathroom.jpg", char="face_stare",
             vo="I practised saying hey in the mirror. Forty times. Version thirty-seven was too excited.",
             keywords=["HEY", "FORTY", "THIRTY-SEVEN"],
             labels=[dict(t=0.6, t1=1.6, text="hey.", x=0.3, y=0.43), dict(t=1.6, t1=2.6, text="hey!", x=0.7, y=0.43),
                     dict(t=2.6, text="HEY!!!", x=0.5, y=0.43, size=90), dict(t="vo-1.4", text="#37", x=0.82, y=0.42)],
             beats=[dict(t=1.6, char="face_forced_smile"), dict(t=2.6, char="face_shocked", punch=1.15),
                    dict(t="vo-1.2", char="face_stare", unpunch=True)],
             sfx=[dict(t=0.6, name="pop"), dict(t=1.6, name="pop"), dict(t=2.6, name="boing")]),
        dict(bg="hallway.jpg", tint="night", char="face_stare", size=0.42,
             vo="I arrive. And I stand outside the door for eleven minutes, listening to people having fun.",
             keywords=["ELEVEN", "FUN"], push=1.09,
             labels=[dict(t=1.0, text="11:00", x=0.5, y=0.5)]),
        dict(bg="hallway.jpg", tint="warm", char="face_shocked", size=0.42, pos=(0.38, 1.03), lead=1.4,
             vo="Then the door opens, and someone yells my name. Out loud. In front of witnesses.",
             keywords=["YELLS", "WITNESSES"],
             extras=[dict(t=0.0, img="face_forced_smile", tint="light", pos=(0.78, 1.0), size=0.44, flip=True,
                          enter=0.5)],
             bubbles=[dict(t=0.15, text="YOU CAME!!!", x=0.7, y=0.44, tail="down-right", talk=True, talk_dur=0.9)],
             beats=[dict(t=0.2, shake=0.4)],
             sfx=[dict(t=0.0, name="door")]),
        dict(bg="party_kitchen.jpg", blur=6, char="face_stare",
             vo="I find my spot. Next to the snacks. Strategic. If anyone talks to me, I'm chewing.",
             keywords=["SNACKS", "STRATEGIC", "CHEWING"],
             labels=[dict(t=0.5, text="SAFE ZONE", x=0.5, y=0.43)], beats=[dict(t="vo-2.0", char="face_smug")],
             sfx=[dict(t=0.5, name="pop")]),
        dict(bg="party_kitchen.jpg", blur=6, char="face_stare", pos=(0.34, 1.03), size=0.42, lead=3.9,
             vo="You too. He told me his name. Why did I say you too.", keywords=["YOU", "TOO", "NAME"],
             extras=[dict(t=0.0, img="face_stare", tint="npc", pos=(0.8, 1.0), size=0.42, flip=True, enter=0.6)],
             labels=[dict(t=0.4, text="ALEX", x=0.82, y=0.43, size=56)],
             bubbles=[dict(t=0.5, t1=2.2, text="Hi! I'm Alex!", x=0.66, y=0.38, tail="down-right", talk=True,
                           talk_dur=0.8),
                      dict(t=2.2, t1=3.6, text="Thanks, you too!", x=0.36, y=0.38, tail="down-left", talk=True,
                           talk_dur=0.8)],
             beats=[dict(t=2.2, char="face_forced_smile"), dict(t=3.5, char="face_stare", tint="light", punch=1.3)],
             sfx=[dict(t=0.4, name="pop"), dict(t=3.5, name="scratch", gain=0.7)]),
        dict(bg="cat_bed.jpg", blur=2, char="face_smug", pos=(0.28, 1.03), size=0.45,
             vo="So I did what any mature adult would do. I found the cat. Best conversation of the night.",
             keywords=["CAT", "BEST"],
             bubbles=[dict(t="vo-2.6", text="...", x=0.72, y=0.40, tail="down"),
                      dict(t="vo-1.2", text="same.", x=0.3, y=0.42, tail="down-left")]),
        dict(bg="party_kitchen.jpg", blur=6, char="face_stare", size=0.44,
             vo="At ten oh four, I left without saying goodbye to anyone.", keywords=["10:04", "GOODBYE"],
             labels=[dict(t=0.2, text="STEALTH MODE", x=0.5, y=0.43)], exit=dict(t="45%", dx=-0.9, d=1.4),
             sfx=[dict(t="45%", name="whoosh")]),
        dict(**NIGHT, char="face_smug", vo="Home. Pyjamas. Silence. Perfect.", keywords=["PERFECT"], hold=0.8),
        dict(**NIGHT, char="face_shocked", lead=1.6,
             vo="They liked me. Being likeable is a trap.", keywords=["TRAP"],
             bubbles=[dict(t=0.1, text="ur so fun!!! same time next week??", style="phone", x=0.5, y=0.43,
                           tail="none")],
             beats=[dict(t=0.6, punch=1.2, shake=0.3), dict(t="vo-1.5", char="face_tear", unpunch=True)],
             sfx=[dict(t=0.1, name="buzz"), dict(t=0.6, name="boing"), dict(t="vo-1.5", name="slide_down")]),
        dict(**NIGHT, char="face_forced_smile", vo="And my thumbs said sure.", keywords=["SURE"], hold=0.9,
             bubbles=[dict(t="vo-0.4", text="haha sure!!", style="phone", x=0.62, y=0.43, tail="none")],
             sfx=[dict(t="vo-0.4", name="whoosh")]),
        dict(bg="bedroom.jpg", tint="night", blur=12, char="face_stare", no_title=True, dur=2.4,
             labels=[dict(t=0.1, text="WHO'S NEXT?", x=0.5, y=0.36, size=96)], sfx=[dict(t=0.1, name="sting")]),
    ],
}
