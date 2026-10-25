"""Operation Bagration, 22 June - 19 August 1944 (blueprint 02 battle format).

Fronts: tools/battles/data/bagration_keyframes.json. Six dates (22.6., 28.6., 4.7., 17.7., 31.7., 29.8.) come from the
ZMSBw map "Operation Bagration" (vector PDF, sourced from OKH Lagekarten); the dates between are built forward
using capture dates from Wikipedia EN/RU, checked against 42 towns. Generalised lines, about 5-10 km.
"""
import json, os
from common import poly, keyframe, ramp, video, write

here = os.path.dirname(__file__)
K = {d: v for d, v in json.load(open(os.path.join(here, "data", "bagration_keyframes.json"))).items() if d.startswith("1944")}
S_ = json.load(open(os.path.join(here, "data", "bagration_static.json")))

territories = [keyframe(d, "soviet", [("germany", poly(g["ring"])) for g in v["german"] + v.get("pockets", [])],
                        "; ".join(g["name"] for g in v["german"] + v.get("pockets", []))) for d, v in K.items()]

arrows = [{"faction": "germany" if a.get("side") == "german" else "soviet", "from": a["from"], "to": a["to"], "path": a["path"],
           "width": 0.7 if a.get("side") == "german" else 1.0} for a in S_["arrows"] if a["id"] not in ("2BaltF", "DE-warsaw")]

E = [
    ("1944-06-22", "Bagration", "Three years to the day after Barbarossa, the Soviet offensive opens.", [30.6, 55.3], 1, True),
    ("1944-06-23", "Main assault", "Three Soviet fronts attack Army Group Centre.", [30.8, 54.6], 0, False),
    ("1944-06-24", "Bobruisk axis", "The 1st Belorussian Front joins the attack in the south.", [29.6, 52.8], 0, False),
    ("1944-06-25", "Vitebsk", "German LIII Corps is encircled.", [30.1, 55.15], 0, False),
    ("1944-06-27", "Bobruisk pocket", "Some 40,000 German troops are trapped (est.).", [29.22, 53.14], 1, False),
    ("1944-06-28", "Mogilev", "Taken after crossing the Dnieper. Model replaces Busch.", [30.34, 53.90], 0, False),
    ("1944-07-03", "Minsk", "Liberated. About 100,000 Germans are trapped to the east.", [27.56, 53.90], 1.5, True),
    ("1944-07-08", "Minsk pocket", "It collapses. Baranovichi falls; Vilnius is surrounded.", [28.3, 53.85], 0, False),
    ("1944-07-13", "Vilnius", "Falls after five days of street fighting.", [25.28, 54.69], 0, True),
    ("1944-07-17", "Moscow", "About 57,000 German prisoners are marched through the city.", [30.5, 55.6], 1, False),
    ("1944-07-18", "Lublin-Brest", "A new offensive opens west of Kovel.", [24.6, 51.3], 0, False),
    ("1944-07-23", "Majdanek", "The camp is found nearly intact. Lublin falls next day.", [22.6, 51.22], 0, False),
    ("1944-07-27", "Białystok", "Białystok, Šiauliai and Daugavpils are taken.", [23.16, 53.13], 0, False),
    ("1944-07-28", "Brest", "The fortress city falls.", [23.69, 52.10], 0, False),
    ("1944-07-31", "The Baltic", "Soviet tanks reach the Gulf of Riga. Army Group North is cut off.", [23.45, 57.03], 1, True),
    ("1944-08-01", "Warsaw", "The Uprising begins as Soviet tanks stall east of the Vistula.", [21.01, 52.23], 1, True),
    ("1944-08-02", "The Vistula", "Bridgeheads are seized at Magnuszew and Puławy.", [21.37, 51.77], 0, False),
    ("1944-08-17", "East Prussia", "Soviet troops reach the German border (approx.).", [22.86, 54.78], 0, False),
    ("1944-08-19", "Exhausted", "The front is now 500 km west of where it began.", [25.0, 53.5], 0, False),
    ("1944-08-20", "Doppelkopf", "A German counterattack reopens the link to Army Group North.", [23.15, 56.97], 1, True),
]
events = [{"date": d, "title": t, "text": x, "at": a, "holdSeconds": h, "captionSeconds": 3.5, "chapter": c} for d, t, x, a, h, c in E]

factions = [
    {"id": "germany", "name": "Germany", "color": "#5d6466", "flags": [{"flag": "germany"}]},
    {"id": "soviet", "name": "Soviet Union", "color": "#b8322a", "flags": [{"flag": "ussr"},
        {"flag": "poland", "weight": 0.25, "from": "1944-07-18", "region": [[20.5, 50.6], [23.6, 52.6]]}]},  # 1st Polish Army
]

# Losses: German (Frieser: 26,397 killed, 109,776 wounded, 262,929 missing/captured); Soviet (Krivosheev, 23 Jun -
# 29 Aug: 178,507 killed/missing, 587,308 wounded/sick). Intermediates: ~300,000 German losses by 4 Jul (EN WP),
# 57,000 prisoners paraded 17 Jul. Interpolated.
S, END = "1944-06-22", "1944-08-21"
losses = {"kind": "table", "label": "Losses", "columns": ["Killed", "Wounded", "Missing"], "source": "Frieser; Krivosheev",
          "rows": [
              {"factionId": "germany", "series": [ramp(S, END, 26397, [["1944-07-04", 17000]]), ramp(S, END, 109776, [["1944-07-04", 62000]]),
                                                  ramp(S, END, 262929, [["1944-06-29", 90000], ["1944-07-04", 170000], ["1944-07-13", 225000]])]},
              {"factionId": "soviet", "series": [ramp(S, END, 178507, [["1944-07-04", 60000]]), ramp(S, END, 587308, [["1944-07-04", 190000]]), None]},
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
    {"factionId": "germany", "flag": "germany", "at": [26.5, 55.3], "label": "Army Group Centre (est.)", "points": strength(849000, losses["rows"][0]["series"]),
     "moves": [["1944-06-21", [26.5, 55.3]], ["1944-07-08", [22.2, 54.0]]]},
    {"factionId": "soviet", "flag": "ussr", "at": [32.4, 54.0], "label": "Soviet forces", "points": strength(1670300, losses["rows"][1]["series"]),
     "moves": [["1944-06-21", [32.4, 54.0]], ["1944-07-08", [28.6, 53.3]], ["1944-07-28", [26.0, 53.6]]]},
]

labels = [{"text": n, "at": a, "kind": "city"} for n, a in S_["cities"]] + [
    {"text": "East Prussia", "at": [21.4, 54.35], "kind": "region", "size": 18}, {"text": "Byelorussia", "at": [28.2, 52.75], "kind": "region", "size": 20},
    {"text": "Lithuania", "at": [24.2, 55.45], "kind": "region", "size": 16}, {"text": "Latvia", "at": [25.6, 56.75], "kind": "region", "size": 16},
    {"text": "Baltic Sea", "at": [19.6, 56.0], "kind": "sea", "size": 18}, {"text": "Pripet Marshes", "at": [27.2, 51.75], "kind": "region", "size": 14}]

v = video(
    id="operation-bagration-1944", title="Operation Bagration", subtitle="1944",
    hook="In under two weeks, Army Group Centre lost some 300,000 men.",
    outro="Bagration tore open the road to Warsaw and East Prussia.",
    bounds=[[17.3, 50.6], [35.3, 57.7]], theatre=["Belarus", "Lithuania", "Latvia", "Estonia", "Poland", "Russia", "Ukraine", "Germany"],
    labels=labels, factions=factions, territories=territories,
    timeline={"start": "1944-06-21", "end": "1944-08-21", "daysPerSecond": 1.1,
              "pace": [{"from": "1944-06-22", "to": "1944-07-05", "daysPerSecond": 0.6}]},
    events=events, arrows=arrows, forces=forces, losses=losses,
    camera=[{"date": "1944-06-21", "center": [28.8, 54.1], "zoom": 1.7}, {"date": "1944-07-04", "center": [27.6, 54.0], "zoom": 1.45},
            {"date": "1944-07-20", "center": [25.3, 54.0], "zoom": 1.15}, {"date": "1944-08-21", "center": [25.6, 54.2], "zoom": 1.05}],
    music="Vanguard", music_start=130,
    music_credit="Vanguard by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au",
    sources=["ZMSBw map 'Operation Bagration, 22. Juni bis 29. August 1944' (from OKH Lagekarten), via bpb.de",
             "Wikipedia (EN/RU): Operation Bagration; Vitebsk-Orsha, Mogilev, Bobruysk, Minsk, Vilnius, Siauliai, Belostok, Lublin-Brest, Kaunas, Osovets offensives; Operation Doppelkopf",
             "K.-H. Frieser (German losses); G. F. Krivosheev (Soviet losses)", "Natural Earth (map data)"],
    thumbnail={"date": "1944-07-03", "text": "Destroyed", "textAt": "top-left", "highlight": [28.3, 53.88], "zoom": 1.6, "center": [28.2, 53.9]},
    globe_to=[27.5, 54.0], spacing=(56, 15), density=0.45, relief_strength=1.6,
    tags=["Operation Bagration", "1944", "WW2", "Eastern Front", "Army Group Centre", "WW2 map", "every day"],
    summary="Operation Bagration, day by day on one map: the Soviet summer offensive of 1944 that destroyed Germany's Army Group Centre, from Vitebsk and Bobruisk to Minsk, Vilnius, the Baltic and the Vistula.",
)
v["short"] = {"seconds": 45, "zoom": 1.4, "title": "Operation Bagration"}
write(v)
