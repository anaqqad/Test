"""The Battle of the Bulge, 16 December 1944 - 25 January 1945 (blueprint 02 battle format).

Fronts: tools/battles/data/bulge.json. December lines from Cole, "The Ardennes: Battle of the Bulge" (US Army CMH,
maps I-X, georeferenced to <1 km) and the West Point atlas (16, 20, 25 Dec); 3, 16 and 28 Jan lines digitised from
MacDonald, "The Last Offensive", Map II. 8, 12 and 20 Jan interpolated from MacDonald's text.
"""
import json, os
from common import poly, circle, keyframe, ramp, video, write

here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "data", "bulge.json")))
P = D["pockets"]

territories = []
for date, ring in D["german"].items():
    layers = [("germany", poly(ring))]
    for name, p in P.items():
        if date not in p["dates"] or name == "st_vith_salient":
            continue
        if name == "peiper_la_gleize" and date in ("1944-12-22", "1944-12-23"):
            layers.append(("germany", circle([5.846, 50.411], 1.6)))  # only La Gleize still held
        elif p["side"] == "German":
            layers.append(("germany", poly(p["ring"])))
    for name, p in P.items():
        if date in p["dates"] and p["side"] == "Allied" and name != "st_vith_salient":
            layers.append(("allies", poly(p["ring"])))
    territories.append(keyframe(date, "allies", layers))

arrows = [{"faction": "germany" if a["side"] == "German" else "allies", "from": a["start"], "to": a["end"], "path": a["path"],
           "width": 0.9 if a["side"] == "German" else 0.8} for a in D["arrows"]]

E = [
    ("1944-12-16", "The attack", "At 05:30 the Germans open fire. Fog grounds Allied aircraft.", [6.37, 50.36], 1, True),
    ("1944-12-16", "Lanzerath", "18 US soldiers hold up the SS spearhead all day.", [6.334, 50.357], 0, False),
    ("1944-12-17", "Malmedy", "SS troops kill at least 84 captured Americans.", [6.067, 50.403], 0, False),
    ("1944-12-17", "Schnee Eifel", "Two US regiments are cut off.", [6.264, 50.289], 0, False),
    ("1944-12-18", "Stavelot", "Peiper takes the town; US engineers blow the Trois-Ponts bridges.", [5.931, 50.394], 0, False),
    ("1944-12-19", "Surrender", "About 7,000 men of the 106th Division surrender.", [6.33, 50.27], 1, False),
    ("1944-12-19", "Elsenborn Ridge", "The northern shoulder holds.", [6.22, 50.44], 0, False),
    ("1944-12-21", "Bastogne", "The town is surrounded. St. Vith falls.", [5.717, 50.002], 1, True),
    ("1944-12-22", "\"Nuts!\"", "General McAuliffe's reply to a German surrender demand.", [5.717, 50.002], 1, False),
    ("1944-12-22", "Patton", "III Corps attacks north from Arlon toward Bastogne.", [5.817, 49.684], 0, False),
    ("1944-12-23", "Clear skies", "Allied aircraft strike; supplies are dropped on Bastogne.", [5.717, 50.002], 0, False),
    ("1944-12-24", "High-water mark", "German tanks stop about 6 km from the Meuse.", [4.99, 50.247], 1.5, True),
    ("1944-12-25", "Celles", "US and British tanks smash the 2nd Panzer Division.", [5.006, 50.231], 0, False),
    ("1944-12-26", "Bastogne relieved", "4th Armored breaks through at 16:50.", [5.682, 49.966], 1.5, True),
    ("1945-01-01", "Bodenplatte", "A Luftwaffe raid on Allied airfields; heavy losses on both sides.", None, 0, False),
    ("1945-01-03", "Counteroffensive", "The US First Army attacks from the north.", [5.676, 50.293], 0, True),
    ("1945-01-08", "Withdrawal", "Hitler authorises a pullback from the western tip.", [5.576, 50.182], 0, False),
    ("1945-01-16", "Houffalize", "The First and Third Armies link up.", [5.789, 50.132], 1, True),
    ("1945-01-23", "St. Vith", "The 7th Armored Division retakes the town.", [6.126, 50.28], 0, False),
    ("1945-01-25", "The bulge is gone", "The front is nearly back where it started.", [6.20, 50.10], 1, True),
]
events = [{"date": d, "title": t, "text": x, **({"at": a} if a else {}), "holdSeconds": h, "captionSeconds": 3.5, "chapter": c} for d, t, x, a, h, c in E]

factions = [
    {"id": "germany", "name": "Germany", "color": "#5d6466", "flags": [{"flag": "germany"}]},
    {"id": "allies", "name": "United States & Britain", "color": "#3b67a8", "flags": [{"flag": "usa"},
        {"flag": "uk", "weight": 0.8, "from": "1944-12-20", "region": [[4.6, 50.05], [5.35, 50.6]]}]},  # XXX Corps at the Meuse
]

# Losses: US Army preliminary report (8,407 killed, 46,170 wounded, 20,905 missing; MacDonald: 41,315 casualties to
# 2 Jan) and the OKW figure for Germany (12,652 killed, 38,600 wounded, 30,582 missing). Interpolated.
S, END = "1944-12-16", "1945-01-25"
losses = {"kind": "table", "label": "Losses", "columns": ["Killed", "Wounded", "Missing"], "source": "US Army preliminary report; OKW",
          "rows": [
              {"factionId": "germany", "series": [ramp(S, END, 12652, [["1945-01-02", 6500]]), ramp(S, END, 38600, [["1945-01-02", 20000]]), ramp(S, END, 30582, [["1945-01-02", 12000]])]},
              {"factionId": "allies", "flag": "usa", "series": [ramp(S, END, 8407, [["1945-01-02", 4300]]), ramp(S, END, 46170, [["1945-01-02", 23000]]),
                                                              ramp(S, END, 20905, [["1944-12-19", 9500], ["1945-01-02", 14500]])]},
          ]}
forces = [
    {"factionId": "germany", "flag": "germany", "at": [7.0, 50.55], "label": "German forces", "points": [[S, 406342], ["1944-12-24", 449000], [END, 367000]]},
    {"factionId": "allies", "flag": "usa", "at": [4.6, 49.75], "label": "Allied forces", "points": [[S, 228741], ["1945-01-02", 705000], [END, 630000]]},
]

labels = [{"text": n, "at": a, "kind": "city", "size": 19 if n in ("Bastogne", "St. Vith", "Liège", "Luxembourg") else 15} for n, a in D["cities"]
          if n not in ("Foy-Notre-Dame", "Martelange", "Givet", "Trois-Ponts", "La Gleize", "Hotton", "Diekirch")]
labels += [{"text": "Meuse", "at": [4.86, 50.36], "kind": "sea", "size": 14}, {"text": "Ardennes", "at": [5.55, 49.85], "kind": "region", "size": 20},
           {"text": "Germany", "at": [7.05, 50.2], "kind": "country", "size": 22}, {"text": "Belgium", "at": [4.6, 50.6], "kind": "country", "size": 20},
           {"text": "Luxembourg", "at": [6.05, 49.68], "kind": "country", "size": 15}]

v = video(
    id="battle-of-the-bulge-1944", title="The Battle of the Bulge", subtitle="1944-45",
    hook="Hitler's last gamble in the West, launched in fog and snow.",
    outro="Germany never mounted another major offensive in the West.",
    bounds=[[3.9, 49.5], [7.7, 50.9]], theatre=["Belgium", "Luxembourg", "Germany", "France", "Netherlands"],
    labels=labels, factions=factions, territories=territories,
    timeline={"start": "1944-12-15", "end": "1945-01-25", "daysPerSecond": 1.0,
              "pace": [{"from": "1944-12-16", "to": "1944-12-27", "daysPerSecond": 0.4}]},
    events=events, arrows=arrows, forces=forces, losses=losses,
    camera=[{"date": "1944-12-15", "center": [5.9, 50.2], "zoom": 1.45}, {"date": "1944-12-24", "center": [5.55, 50.15], "zoom": 1.5},
            {"date": "1945-01-25", "center": [5.85, 50.15], "zoom": 1.4}],
    music="Juggernaut", music_start=75,
    music_credit="Juggernaut by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au",
    sources=["Hugh M. Cole, The Ardennes: Battle of the Bulge (US Army CMH), text and maps I-X",
             "Charles B. MacDonald, The Last Offensive (US Army CMH), ch. II and Map II",
             "West Point Atlas, Ardennes 16-25 Dec 1944", "Wikipedia: Battle of the Bulge; Siege of Bastogne; Battle of St. Vith; Battle of Elsenborn Ridge",
             "Natural Earth (map data)"],
    thumbnail={"date": "1944-12-24", "text": "Surrounded", "textAt": "bottom-left", "highlight": [5.717, 50.002], "zoom": 1.6, "center": [5.55, 50.15]},
    globe_to=[5.7, 50.1], spacing=(56, 15), density=0.45, relief_strength=1.2,
    tags=["Battle of the Bulge", "1944", "WW2", "Bastogne", "Ardennes", "WW2 map", "every day"],
    summary="The Battle of the Bulge, day by day on one map: the German offensive through the Ardennes, the siege of Bastogne, the high-water mark near the Meuse and the Allied counteroffensive.",
)
v["short"] = {"seconds": 45, "zoom": 1.1, "title": "The Battle of the Bulge"}
write(v)
