"""The Battle of France, 10 May - 25 June 1940 (blueprint 02 battle format).

Fronts: tools/battles/data/france1940.json, researched from Wikipedia (EN/FR: Battle of France, invasions of the
Netherlands and Belgium, Sedan, Dunkirk, Fall Rot, Ligne de demarcation...) and checked against ~30 cities.
Accuracy ~10 km on the documented lines (Dyle, Escaut, Lys, Dunkirk perimeter, Weygand line, demarcation line),
~20-30 km for the fast June fronts.
"""
import json, os
from common import poly, keyframe, ramp, video, write

here = os.path.dirname(__file__)
D = json.load(open(os.path.join(here, "data", "france1940.json")))
side = {"german": "germany", "allied": "allies", "italian": "germany"}

territories = []
for date, k in D["keyframes"].items():
    if date == "1940-06-04":
        continue  # identical to 06-05
    territories.append(keyframe(date, "allies", [(side[l["side"]], poly(l["ring"])) for l in k["layers"]], f"{k['src']} | conf: {k['conf']}"))

# Then the armistice zones: Germans pull back from Auvergne/Lyon and take the Atlantic coast to Spain.
k = keyframe("1940-06-30", "allies", [("germany", poly(D["occupied"]))], "Demarcation line (FR Wikipedia, commune-by-commune route)")
k["layers"].append({"faction": "germany", "countries": ["Germany"]})  # the zone polygon covers France and the Low Countries only
territories.append(k)

arrow_side = {"German": "germany", "Allied": "allies"}
arrows = [{"faction": arrow_side[a["side"]], "from": a["start"], "to": a["end"], "path": a["path"], "width": 1.0 if a["side"] == "German" else 0.7}
          for a in D["arrows"] if a["side"] in arrow_side]

E = [  # date, title, text, at
    ("1940-05-10", "Invasion", "Germany invades the Netherlands, Belgium and Luxembourg.", [5.9, 50.8]),
    ("1940-05-11", "Eben-Emael", "Glider troops take Belgium's strongest fort.", [5.68, 50.80]),
    ("1940-05-13", "Sedan", "German armour crosses the Meuse at Sedan and Dinant.", [4.94, 49.70]),
    ("1940-05-14", "Rotterdam", "The Luftwaffe bombs Rotterdam; 711 killed.", [4.48, 51.92]),
    ("1940-05-15", "The Netherlands", "The Dutch army capitulates.", [4.57, 51.85]),
    ("1940-05-17", "Brussels", "German troops enter Brussels.", [4.35, 50.85]),
    ("1940-05-20", "The Channel", "Panzers reach the sea at Abbeville. The Allies are cut in two.", [1.71, 50.18]),
    ("1940-05-21", "Arras", "A British-French counterattack briefly checks Rommel.", [2.78, 50.29]),
    ("1940-05-24", "Halt order", "Hitler stops the panzers on the Aa canal.", [2.25, 50.80]),
    ("1940-05-26", "Dunkirk", "Calais falls. The evacuation begins.", [2.38, 51.03]),
    ("1940-05-28", "Belgium", "The Belgian army capitulates.", [3.22, 51.21]),
    ("1940-06-04", "Dunkirk ends", "338,226 Allied soldiers reach Britain.", [2.38, 51.03]),
    ("1940-06-05", "Fall Rot", "Germany attacks across the Somme.", [2.30, 49.85]),
    ("1940-06-10", "Italy", "Italy declares war. The French government leaves Paris.", [7.50, 43.78]),
    ("1940-06-12", "Saint-Valery", "The British 51st Highland Division surrenders.", [0.71, 49.87]),
    ("1940-06-14", "Paris", "German troops enter Paris unopposed.", [2.35, 48.86]),
    ("1940-06-17", "Cut off", "Guderian reaches the Swiss border. Pétain asks for terms.", [6.35, 46.90]),
    ("1940-06-18", "De Gaulle", "From London, de Gaulle calls on France to fight on.", None),
    ("1940-06-19", "Cherbourg", "Rommel takes Cherbourg.", [-1.62, 49.64]),
    ("1940-06-22", "Armistice", "Signed at Compiègne, in the same railway carriage as 1918.", [2.906, 49.427]),
    ("1940-06-25", "Ceasefire", "The fighting stops at 00:35.", [1.5, 46.8]),
    ("1940-06-30", "France divided", "Germany occupies the north and the Atlantic coast.", [0.7, 46.9]),
]
chapters = {"1940-05-10", "1940-05-20", "1940-06-04", "1940-06-14", "1940-06-22"}
holds = {"1940-05-13": 1, "1940-05-20": 1.5, "1940-06-04": 1, "1940-06-14": 1.5, "1940-06-22": 1.5}
events = [{"date": d, "title": t, "text": x, **({"at": a} if a else {}), "holdSeconds": holds.get(d, 0), "captionSeconds": 3.5,
           "chapter": d in chapters} for d, t, x, a in E]

lowlands = [[2.4, 49.4], [7.3, 53.7]]
factions = [
    {"id": "germany", "name": "Germany", "color": "#5d6466", "flags": [{"flag": "germany"}]},
    {"id": "allies", "name": "France & Allies", "color": "#3b67a8", "flags": [
        {"flag": "france", "weight": 1},
        {"flag": "netherlands", "weight": 3, "to": "1940-05-15", "region": [[3.3, 51.25], [7.3, 53.7]]},
        {"flag": "belgium", "weight": 2, "to": "1940-05-28", "region": [[2.5, 49.5], [6.5, 51.5]]},
        {"flag": "uk", "weight": 1.2, "to": "1940-06-05", "region": [[1.5, 49.9], [4.6, 51.3]]},
        {"flag": "uk", "weight": 0.25, "from": "1940-06-05", "to": "1940-06-13", "region": [[0.3, 49.5], [1.8, 50.2]]},
    ]},
]

# Losses (Frieser via Wikipedia; Allied infobox). Intermediate: OKW 10 May-4 Jun for Germany; Belgian capitulation,
# Lille and Dunkirk rearguard prisoners; ~1.2M French prisoners 16-25 June. Interpolated between these.
S, END = "1940-05-10", "1940-06-25"
losses = {"kind": "table", "label": "Losses", "columns": ["Killed", "Wounded", "Captured"], "source": "Frieser; Wikipedia infobox",
          "rows": [
              {"factionId": "germany", "series": [ramp(S, END, 27074, [["1940-06-04", 10232]]), ramp(S, END, 111034, [["1940-06-04", 42523]]),
                                                  ramp(S, END, 18384, [["1940-06-04", 8463]])]},
              {"factionId": "allies", "flag": "france", "series": [ramp(S, END, 73000, [["1940-06-04", 30000]]), ramp(S, END, 240000, [["1940-06-04", 100000]]),
                                                                   ramp(S, END, 1756000, [["1940-05-28", 240000], ["1940-06-04", 330000], ["1940-06-15", 560000]])]},
          ]}


def strength(start, rows):
    """Start strength minus cumulative losses, sampled on the dates where the loss series change."""
    dates = sorted({d for series in rows for d, _ in series})
    def at(series, d):
        from datetime import date
        pts = [(date.fromisoformat(a), v) for a, v in series]
        x = date.fromisoformat(d)
        for (d0, v0), (d1, v1) in zip(pts, pts[1:]):
            if d0 <= x <= d1:
                return v0 + (v1 - v0) * (x - d0).days / max(1, (d1 - d0).days)
        return pts[-1][1]
    return [[d, round(start - sum(at(s, d) for s in rows))] for d in dates]


forces = [
    {"factionId": "germany", "flag": "germany", "at": [7.3, 50.9], "label": "German forces", "points": strength(3300000, losses["rows"][0]["series"]),
     "moves": [["1940-05-10", [7.3, 50.9]], ["1940-06-05", [7.3, 49.9]], ["1940-06-20", [5.5, 48.6]]]},
    {"factionId": "allies", "flag": "france", "at": [2.6, 49.3], "label": "Allied forces", "points": strength(3300000, losses["rows"][1]["series"]),
     "moves": [["1940-05-10", [2.6, 49.3]], ["1940-06-05", [1.5, 47.6]], ["1940-06-20", [1.2, 45.3]]]},
]

labels = [{"text": t, "at": a, "kind": "city"} for t, a in [
    ("Paris", [2.35, 48.86]), ("Sedan", [4.94, 49.70]), ("Dunkirk", [2.38, 51.03]), ("Brussels", [4.35, 50.85]),
    ("Amsterdam", [4.90, 52.37]), ("Rotterdam", [4.48, 51.92]), ("Lille", [3.06, 50.63]), ("Abbeville", [1.83, 50.11]),
    ("Calais", [1.86, 50.95]), ("Amiens", [2.30, 49.89]), ("Reims", [4.03, 49.26]), ("Verdun", [5.38, 49.16]),
    ("Metz", [6.18, 49.12]), ("Strasbourg", [7.75, 48.58]), ("Lyon", [4.84, 45.76]), ("Bordeaux", [-0.58, 44.84]),
    ("Tours", [0.69, 47.39]), ("Brest", [-4.49, 48.39]), ("Cherbourg", [-1.62, 49.64]), ("Dijon", [5.04, 47.32]),
    ("Antwerp", [4.40, 51.22]), ("Liège", [5.57, 50.63]), ("Rouen", [1.10, 49.44]), ("Vichy", [3.43, 46.13]),
    ("Compiègne", [2.83, 49.42]), ("Orléans", [1.91, 47.90])]] + [
    {"text": "Germany", "at": [7.9, 51.9], "kind": "country", "size": 22}, {"text": "Switzerland", "at": [7.8, 46.75], "kind": "country", "size": 16},
    {"text": "United Kingdom", "at": [-1.2, 51.6], "kind": "country", "size": 18}, {"text": "Spain", "at": [-2.5, 42.6], "kind": "country", "size": 18},
    {"text": "English Channel", "at": [-1.8, 50.1], "kind": "sea", "size": 16}, {"text": "North Sea", "at": [3.2, 52.9], "kind": "sea", "size": 18},
    {"text": "Bay of Biscay", "at": [-3.6, 45.4], "kind": "sea", "size": 16}]

v = video(
    id="battle-of-france-1940", title="The Battle of France", subtitle="1940",
    hook="Six weeks. One of Europe's great armies, defeated.",
    outro="France would stay divided until the liberation of 1944.",
    bounds=[[-5.3, 42.6], [8.4, 53.65]], theatre=["France", "Belgium", "Netherlands", "Luxembourg", "Germany"],
    labels=labels, factions=factions, territories=territories,
    timeline={"start": "1940-05-10", "end": "1940-06-30", "daysPerSecond": 0.75,
              "pace": [{"from": "1940-05-12", "to": "1940-05-21", "daysPerSecond": 0.6}, {"from": "1940-06-25", "to": "1940-06-30", "daysPerSecond": 3}]},
    events=events, arrows=arrows, forces=forces, losses=losses,
    camera=[{"date": "1940-05-10", "center": [4.4, 51.0], "zoom": 1.9}, {"date": "1940-05-21", "center": [3.3, 50.5], "zoom": 2.0},
            {"date": "1940-06-04", "center": [2.8, 50.2], "zoom": 1.9}, {"date": "1940-06-09", "center": [2.3, 48.9], "zoom": 1.35},
            {"date": "1940-06-19", "center": [1.6, 47.3], "zoom": 1.05}, {"date": "1940-06-30", "center": [1.6, 47.3], "zoom": 1.05}],
    music="Legionnaire", music_start=25,
    music_credit="Legionnaire by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au",
    sources=["Wikipedia (EN/FR): Battle of France; German invasion of the Netherlands; German invasion of Belgium (1940); Battle of Sedan (1940); Dunkirk evacuation; Fall Rot; Armistice of 22 June 1940; Ligne de démarcation",
             "Karl-Heinz Frieser, The Blitzkrieg Legend (losses)", "Natural Earth (map data)"],
    thumbnail={"date": "1940-05-26", "text": "Trapped", "textAt": "bottom-left", "highlight": [2.38, 51.03], "zoom": 2.2, "center": [2.6, 50.4]},
    globe_to=[2.5, 49.0], spacing=(56, 15), density=0.5,
    tags=["Battle of France", "1940", "WW2", "Dunkirk", "Blitzkrieg", "WW2 map", "every day"],
    summary="The fall of France in 1940, day by day on one map: the invasion of the Low Countries, the breakthrough at Sedan, Dunkirk, the fall of Paris and the armistice.",
)
v["short"] = {"seconds": 45, "zoom": 1.15, "title": "The Fall of France"}
write(v)
