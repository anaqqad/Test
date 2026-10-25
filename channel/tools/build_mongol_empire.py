"""Builds data/videos/mongol-empire.json from tools/mongol/extents.geojson.

The extents were drawn region by region from Wikipedia's campaign articles (see tools/mongol/build_extents.py,
shapely) and cross-checked against Taagepera's area figures; raids that were not held (Poland, Hungary, Syria
after 1260, Japan) are not counted as territory. Borders of steppe empires are approximate: the video says so.
"""
import json, os

here = os.path.dirname(__file__)
ext = {f["properties"]["key"]: f["geometry"] for f in json.load(open(os.path.join(here, "mongol", "extents.geojson")))["features"]}


def unified(date, key, note="", cut=False):
    k = {"date": date, "layers": [{"faction": "mongol", "geometry": ext[key]}], "note": note}
    if cut:
        k["cut"] = True
    return k


def khanates(date, year, note="", cut=False):
    chag = "Chagatai" if year == "1264" else "Chagatai_Kaidu"
    layers = [{"faction": "yuan", "geometry": ext[f"{year}_Yuan"]},
              {"faction": "golden", "geometry": ext[f"{year}_GoldenHorde"]},
              {"faction": "chagatai", "geometry": ext[f"{year}_{chag}"]},
              {"faction": "ilkhanate", "geometry": ext[f"{year}_Ilkhanate"]}]
    if year != "1264":
        layers.append({"faction": "yuan", "geometry": ext["Hainan_Yuan_1279_1294"]} if "Hainan_Yuan_1279_1294" in ext else None)
        layers = [l for l in layers if l]
    k = {"date": date, "layers": layers, "note": note}
    if cut:
        k["cut"] = True
    return k


territories = [
    unified("1206-03-01", "1206", "Mongol plateau after the kurultai"),
    unified("1210-01-31", "1210", "Western Xia tributary (Jan 1210); Uighurs submit (1209)"),
    unified("1215-06-01", "1215", "Zhongdu taken; northern Jin"),
    unified("1218-12-31", "1218", "Qara Khitai absorbed"),
    unified("1221-12-31", "1221", "Khwarazm conquered"),
    unified("1227-09-30", "1227", "Western Xia destroyed; Chinggis Khan dies"),
    unified("1234-02-09", "1234", "Jin destroyed at Caizhou"),
    unified("1237-12-31", "1237", "Volga Bulgaria, Ryazan"),
    unified("1240-12-06", "1240", "Kiev falls; Rus' subjugated"),
    unified("1243-06-26", "1243", "Kose Dag: Seljuk Rum a vassal"),
    unified("1252-12-31", "1252", "Galicia tributary; Tibet nominal"),
    unified("1256-12-31", "1256", "Dali/Yunnan; Nizari castles taken"),
    unified("1258-02-10", "1258", "Baghdad falls"),
    unified("1259-08-11", "1259", "Goryeo vassal; Mongke dies"),
    unified("1260-03-01", "1260_JanSep_peak", "Aleppo and Damascus taken: peak of the united empire"),
    unified("1260-09-03", "1260", "Ain Jalut: Syria lost"),
    khanates("1264-08-21", "1264", "Ariq Boke surrenders; four khanates", cut=True),
    khanates("1268-01-01", "1264", "Song conquest resumes"),
    khanates("1279-03-19", "1279", "Battle of Yamen: Song destroyed"),
    khanates("1294-02-18", "1294", "Kublai Khan dies"),
]

events = [
    ("1206-03-01", "Chinggis Khan", "Temüjin unites the steppe tribes and takes a new name.", [109.5, 48.6], 1, True),
    ("1210-01-31", "Western Xia submits", "The first settled kingdom to bow.", [106.3, 38.5], 0, False),
    ("1215-06-01", "Zhongdu falls", "The Jin capital, today's Beijing, is taken.", [116.4, 39.9], 1, True),
    ("1219-09-01", "War on Khwarazm", "After envoys are killed, Chinggis turns west.", [68.3, 42.85], 1, True),
    ("1221-11-24", "Battle of the Indus", "Khwarazm's last army is destroyed.", [72.2, 33.9], 0, False),
    ("1227-08-18", "Chinggis Khan dies", "His empire already stretches from the Caspian to the Yellow Sea.", [105.0, 36.0], 1, True),
    ("1234-02-09", "Jin destroyed", "Northern China falls after twenty years of war.", [114.4, 33.0], 0, False),
    ("1240-12-06", "Kiev falls", "The Rus' principalities submit.", [30.52, 50.45], 1, True),
    ("1241-04-11", "Mohi", "Hungary's army is destroyed. Europe is raided, not held.", [20.95, 47.98], 0, False),
    ("1241-12-11", "Ögedei dies", "The armies in Europe turn back.", None, 0, False),
    ("1243-06-26", "Köse Dağ", "The Seljuks of Anatolia become vassals.", [38.7, 40.1], 0, False),
    ("1258-02-10", "Baghdad", "Five centuries of Abbasid rule in Baghdad end.", [44.4, 33.3], 1.5, True),
    ("1259-08-11", "Möngke dies", "The last khan of a united empire.", [106.28, 30.0], 0, False),
    ("1260-09-03", "Ain Jalut", "The Mamluks defeat a Mongol army in Palestine.", [35.36, 32.55], 1, True),
    ("1264-08-21", "Four khanates", "After a civil war, the empire splits in four.", None, 2, True),
    ("1271-12-18", "Yuan dynasty", "Kublai Khan declares himself emperor of China.", [116.4, 39.9], 0, False),
    ("1276-02-04", "Lin'an surrenders", "The Song capital opens its gates.", [120.15, 30.25], 0, False),
    ("1279-03-19", "Battle of Yamen", "The last Song emperor dies. All China is under Mongol rule.", [113.1, 22.2], 1.5, True),
    ("1281-08-15", "Kamikaze", "A typhoon wrecks the second invasion fleet off Japan.", [130.4, 33.6], 0, False),
    ("1294-02-18", "Kublai Khan dies", "It remains the largest contiguous land empire in history.", [116.4, 39.9], 2, True),
]

static = json.load(open(os.path.join(here, "mongol", "static.json")))

video = {
    "id": "mongol-empire",
    "draft": False,
    "header": {
        "title": "The Mongol Empire",
        "subtitle": "Year by year, 1206 - 1294",
        "hook": "In seventy years, one steppe confederation built an empire from Korea to the Danube.",
        "globe": {"from": [25, 40], "to": [100, 45], "showDate": "1279-03-19"},
        "footnote": "Borders approximate; raids not counted as territory.",
        "outro": "Within 75 years of Kublai's death, the Ilkhanate had collapsed and the Yuan had fallen.",
        "watermark": "Borderclock",
    },
    "map": {
        "projection": "conicEqualArea",
        "bounds": [[12, 14], [146, 63]],
        "landDetail": "50m",
        "markers": False,
        "labels": static["labels"],
    },
    "factions": [
        {"id": "mongol", "name": "Mongol Empire", "color": "#b8322a"},
        {"id": "yuan", "name": "Yuan dynasty", "color": "#b8322a"},
        {"id": "golden", "name": "Golden Horde", "color": "#c99a2e"},
        {"id": "chagatai", "name": "Chagatai Khanate", "color": "#5f8a4a"},
        {"id": "ilkhanate", "name": "Ilkhanate", "color": "#3f6f9a"},
    ],
    "territories": territories,
    "timeline": {
        "start": "1206-03-01", "end": "1294-02-18", "clock": "year", "introSeconds": 7, "outroSeconds": 12,
        "daysPerSecond": 200,
        "pace": [
            {"from": "1219-06-01", "to": "1222-01-01", "daysPerSecond": 110},
            {"from": "1236-01-01", "to": "1243-07-01", "daysPerSecond": 140},
            {"from": "1256-06-01", "to": "1260-10-01", "daysPerSecond": 110},
            {"from": "1264-09-01", "to": "1271-06-01", "daysPerSecond": 420},
            {"from": "1283-01-01", "to": "1294-01-01", "daysPerSecond": 420},
        ],
    },
    "camera": [
        {"date": "1206-03-01", "center": [100, 45], "zoom": 1.9},
        {"date": "1215-06-01", "center": [102, 43], "zoom": 1.6},
        {"date": "1219-06-01", "center": [88, 42], "zoom": 1.25},
        {"date": "1227-06-01", "center": [80, 42], "zoom": 1.05},
        {"date": "1236-01-01", "center": [70, 44], "zoom": 1.05},
        {"date": "1243-01-01", "center": [65, 44], "zoom": 1.1},
        {"date": "1252-01-01", "center": [78, 40], "zoom": 1},
        {"date": "1258-01-01", "center": [60, 38], "zoom": 1.15},
        {"date": "1261-01-01", "center": [75, 40], "zoom": 1},
        {"date": "1294-02-18", "center": [79, 40], "zoom": 1},
    ],
    "events": [
        {"date": d, "title": t, "text": x, **({"at": a} if a else {}), "holdSeconds": h, "chapter": c,
         **({"captionSeconds": 6} if d == "1294-02-18" else {})}
        for d, t, x, a, h, c in events
    ],
    "counters": [{"kind": "area", "label": "Land under Mongol rule", "mode": "total"}],
    "leaders": static["leaders"],
    "audio": {"music": [{"src": "music/RideTheWind.mp3", "volume": 1, "startFrom": 20}], "eventSfxVolume": 0.5},
    "youtube": {
        "title": "The Mongol Empire, Year by Year (1206-1294)",
        "summary": "Every year of the Mongol Empire on one map: from Chinggis Khan's steppe confederation in 1206 to the largest contiguous land empire in history, its split into four khanates, and the death of Kublai Khan in 1294.",
        "sources": [
            "Wikipedia: Mongol Empire; Division of the Mongol Empire; Mongol conquests of Western Xia, the Jin dynasty and the Khwarazmian Empire; Siege of Kiev (1240); Battle of Kose Dag; Siege of Baghdad (1258); Battle of Ain Jalut; Battle of Yamen; Kublai Khan",
            "Rein Taagepera, 'Expansion and Contraction Patterns of Large Polities' (International Studies Quarterly, 1997), for area estimates",
        ],
        "credits": ["Ride The Wind by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au"],
        "tags": ["Mongol Empire", "Mongol Empire map", "Genghis Khan", "Chinggis Khan", "Kublai Khan", "Golden Horde", "Yuan dynasty", "history map"],
    },
    "thumbnail": {"date": "1260-03-01", "text": "It started here", "textAt": "bottom-left", "highlight": [102.83, 47.2],
                  "zoom": 1.1, "center": [80, 42]},
}

out = os.path.join(here, "..", "data", "videos", "mongol-empire.json")
with open(out, "w") as f:
    json.dump(video, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(out), len(territories), "keyframes,", len(events), "events")
