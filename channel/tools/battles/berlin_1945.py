"""The Battle of Berlin, 16 April - 8 May 1945 (blueprint 02 battle format).

Fronts: tools/battles/data/berlin_keyframes.json, hand-digitised from Ziemke "Stalingrad to Berlin" (CMH) ch. XXI,
Wikipedia EN/DE/RU (Battle of Berlin, Seelow Heights, Halbe, Battle in Berlin, Bautzen, Elbe Day, 12th Army) and
DE town articles for capture dates. ~5 km around Seelow, the city pockets and Ketzin/Torgau; ~10-15 km elsewhere.
"""
import json, os
from common import poly, keyframe, ramp, video, write

here = os.path.dirname(__file__)
K = json.load(open(os.path.join(here, "data", "berlin_keyframes.json")))["dates"]
X = json.load(open(os.path.join(here, "data", "berlin_extras.json")))

territories = []
for date, k in K.items():
    wf = k["western_front_path"]
    west = poly(wf + [[7.0, wf[-1][1]], [7.0, wf[0][1]]])  # everything west of the Western Allies' line
    layers = [("western", west)]
    if k.get("mulde_elbe_gap"):
        layers.append(("western", poly(k["mulde_elbe_gap"])))  # no man's land between the Mulde and the Elbe
    layers += [("germany", poly(g["ring"])) for g in k["german"]]
    territories.append(keyframe(date, "soviet", layers, "; ".join(g["name"] for g in k["german"])))

side = {"soviet": "soviet", "german": "germany"}
arrows = [{"faction": side[a["side"]], "from": a["from"], "to": a["to"], "path": a["path"], "width": 1.0 if a["side"] == "soviet" else 0.75}
          for a in X["arrows"] if a["side"] in side]

E = [
    ("1945-04-16", "Seelow and the Neisse", "Zhukov attacks on the Oder; Konev crosses the Neisse.", [14.4, 52.55], 1, True),
    ("1945-04-19", "Seelow broken", "The last line before Berlin falls after four days.", [14.38, 52.53], 0, False),
    ("1945-04-20", "Hitler's birthday", "His last. Soviet long-range guns open fire on Berlin.", [13.381, 52.512], 0, False),
    ("1945-04-21", "Berlin's edge", "Soviet troops cross the city limits; Zossen is overrun.", [13.56, 52.545], 0, False),
    ("1945-04-22", "Sachsenhausen", "Soviet troops liberate the concentration camp.", [13.26, 52.77], 0, False),
    ("1945-04-24", "Halbe", "The German 9th Army is encircled south-east of Berlin.", [13.704, 52.11], 1, False),
    ("1945-04-25", "Berlin encircled", "The ring closes at Ketzin.", [12.85, 52.48], 1, True),
    ("1945-04-25", "Elbe Day", "US and Soviet troops meet at Torgau. Germany is cut in two.", [13.005, 51.561], 0, True),
    ("1945-04-26", "Stettin falls", "Rokossovsky breaks through in the north.", [14.553, 53.428], 0, False),
    ("1945-04-27", "Inside Berlin", "The defenders hold a strip about 16 km long.", [13.40, 52.51], 0, False),
    ("1945-04-28", "Wenck", "The 12th Army's relief attack stalls at Lake Schwielow.", [12.95, 52.33], 0, False),
    ("1945-04-29", "Moltke Bridge", "Soviet troops cross the Spree near the Reichstag.", [13.368, 52.522], 0, False),
    ("1945-04-30", "The bunker", "Hitler kills himself. A Soviet flag goes up on the Reichstag.", [13.376, 52.519], 1.5, True),
    ("1945-05-01", "Breakout", "9th Army survivors reach Wenck's lines near Beelitz.", [12.927, 52.238], 0, False),
    ("1945-05-02", "Berlin surrenders", "General Weidling surrenders the city.", [13.40, 52.51], 1.5, True),
    ("1945-05-08", "Surrender", "Germany's unconditional surrender takes effect.", [13.527, 52.481], 1, True),
]
events = [{"date": d, "title": t, "text": x, "at": a, "holdSeconds": h, "captionSeconds": 3.5, "chapter": c} for d, t, x, a, h, c in E]

factions = [
    {"id": "germany", "name": "Germany", "color": "#5d6466", "flags": [{"flag": "germany"}]},
    {"id": "soviet", "name": "Soviet Union", "color": "#b8322a", "flags": [{"flag": "ussr"},
        {"flag": "poland", "weight": 0.15, "region": [[13.5, 52.4], [15.5, 53.65]]},  # 1st Polish Army with Zhukov
        {"flag": "poland", "weight": 0.25, "region": [[13.6, 50.85], [15.5, 51.6]]}]},  # 2nd Polish Army at Bautzen
    {"id": "western", "name": "United States & Britain", "color": "#3b67a8", "flags": [{"flag": "usa"},
        {"flag": "uk", "weight": 1.5, "region": [[9.0, 52.9], [12.0, 54.6]]}]},
]

# Losses: Soviet (Krivosheev, incl. Polish dead); German (Mueller: 92,000-100,000 dead, ~220,000 wounded,
# ~480,000 prisoners by Soviet count). Interpolated; the city's surrender on 2 May adds ~134,000 prisoners.
S, END = "1945-04-16", "1945-05-08"
losses = {"kind": "table", "label": "Losses", "columns": ["Killed", "Wounded", "Captured"], "source": "Krivosheev; Mueller; Wikipedia",
          "rows": [
              {"factionId": "germany", "series": [ramp(S, END, 92000, [["1945-05-02", 85000]]), ramp(S, END, 220000, [["1945-05-02", 200000]]),
                                                  ramp(S, END, 480000, [["1945-04-30", 220000], ["1945-05-02", 380000]])]},
              {"factionId": "soviet", "series": [ramp(S, END, 81116, [["1945-04-19", 22000], ["1945-05-02", 78000]]), ramp(S, END, 280251, [["1945-05-02", 270000]]), None]},
          ]}


def strength(start, rows):
    from datetime import date
    rows = [r for r in rows if r]
    dates = sorted({d for s in rows for d, _ in s})
    def at(series, d):
        pts = [(date.fromisoformat(a), v) for a, v in series]
        x = date.fromisoformat(d)
        for (d0, v0), (d1, v1) in zip(pts, pts[1:]):
            if d0 <= x <= d1:
                return v0 + (v1 - v0) * (x - d0).days / max(1, (d1 - d0).days)
        return pts[-1][1]
    return [[d, round(start - sum(at(s, d) for s in rows))] for d in dates]


forces = [
    {"factionId": "germany", "flag": "germany", "at": [12.3, 52.75], "label": "German forces (est.)", "points": strength(850000, losses["rows"][0]["series"]),
     "moves": [["1945-04-15", [12.3, 52.75]], ["1945-04-26", [12.6, 52.9]]], "to": "1945-05-03"},
    {"factionId": "soviet", "flag": "ussr", "at": [15.0, 52.95], "label": "Soviet & Polish forces", "points": strength(2500000, losses["rows"][1]["series"]),
     "moves": [["1945-04-15", [15.0, 52.95]], ["1945-04-26", [13.9, 52.25]], ["1945-05-03", [14.6, 52.6]]]},
]

city_kinds = {"capital": 22, "city": 17, "town": 15}
labels = [{"text": l["text"], "at": l["at"], "kind": "city", "size": city_kinds.get(l.get("kind"), 15)} for l in X["map"]["labels"]
          if l.get("kind") in city_kinds]
labels += [{"text": t, "at": a, "kind": "city", "size": 13, "from": "1945-04-26"} for t, a in [
    ("Reichstag", [13.376, 52.519]), ("Tiergarten", [13.35, 52.514]), ("Tempelhof", [13.403, 52.473]), ("Charlottenburg", [13.296, 52.521])]]
labels += [{"text": "Oder", "at": [14.45, 52.85], "kind": "sea", "size": 15}, {"text": "Elbe", "at": [12.2, 52.75], "kind": "sea", "size": 15},
           {"text": "Poland", "at": [15.3, 52.05], "kind": "country", "size": 20}, {"text": "Czechoslovakia", "at": [14.2, 50.75], "kind": "country", "size": 16}]

v = video(
    id="battle-of-berlin-1945", title="The Battle of Berlin", subtitle="1945",
    hook="Three weeks, two and a half million Soviet soldiers, one city.",
    outro="Six days after Berlin fell, the war in Europe was over.",
    bounds=[[11.2, 50.85], [15.5, 53.65]], theatre=["Germany", "Poland", "Czechia"],
    labels=labels, factions=factions, territories=territories,
    timeline={"start": "1945-04-15", "end": "1945-05-08", "daysPerSecond": 0.32,
              "pace": [{"from": "1945-05-02", "to": "1945-05-08", "daysPerSecond": 2}]},
    events=events, arrows=arrows, forces=forces, losses=losses,
    camera=[{"date": "1945-04-15", "center": [13.4, 52.3], "zoom": 1.0}, {"date": "1945-04-22", "center": [13.5, 52.35], "zoom": 1.25},
            {"date": "1945-04-25", "center": [13.3, 52.4], "zoom": 1.6}, {"date": "1945-04-28", "center": [13.33, 52.5], "zoom": 3.2},
            {"date": "1945-05-02", "center": [13.33, 52.5], "zoom": 3.4}, {"date": "1945-05-05", "center": [13.4, 52.3], "zoom": 1.1},
            {"date": "1945-05-08", "center": [13.4, 52.3], "zoom": 1.0}],
    music="PassageOfTime", music_start=150,
    music_credit="Passage of Time by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au",
    sources=["Earl F. Ziemke, Stalingrad to Berlin: The German Defeat in the East (US Army CMH), ch. XXI",
             "Wikipedia (EN/DE/RU): Battle of Berlin; Battle of the Seelow Heights; Battle of Halbe; Battle in Berlin; Battle of Bautzen (1945); Elbe Day; 12th Army",
             "G. F. Krivosheev (Soviet losses); R.-D. Mueller (German losses)", "Natural Earth (map data)"],
    thumbnail={"date": "1945-04-25", "text": "Encircled", "textAt": "bottom-left", "highlight": [13.35, 52.5], "zoom": 1.7, "center": [13.5, 52.35]},
    globe_to=[13.4, 52.5], spacing=(56, 15), density=0.45,
    tags=["Battle of Berlin", "1945", "WW2", "Seelow Heights", "Reichstag", "WW2 map", "every day"],
    summary="The Battle of Berlin, day by day on one map: Seelow Heights, the encirclement of Berlin and the Halbe pocket, Elbe Day at Torgau, the fight for the Reichstag and the surrender.",
)
v["short"] = {"seconds": 45, "zoom": 1.4, "title": "The Fall of Berlin"}
write(v)
