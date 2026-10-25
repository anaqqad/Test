"""Builds data/videos/korean-war.json from researched front lines.

Front lines come from the US Army CMH official histories (Appleman, "South to the Naktong, North to the Yalu";
Mossman, "Ebb and Flow") and the Natural Earth 10m line of control (the armistice line). Each keyframe is:
North everywhere, then the UN-held side of the front line, then pockets. A front line runs from the west coast
(start="west") or the south coast (start="south") to the east coast; the UN side is closed through the sea to the
south-east, so lines may bend back on themselves.
"""
import json, math, os

E, W, S = 131.5, 123.5, 32.5


def un_side(line, start="west"):
    end = line[-1]
    ring = list(line) + [[E, end[1]], [E, S]]
    ring += [[W, S], [W, line[0][1]]] if start == "west" else [[line[0][0], S]]
    ring.append(line[0])
    return {"type": "Polygon", "coordinates": [ring]}


def poly(points):
    return {"type": "Polygon", "coordinates": [list(points) + [points[0]]]}


def circle(c, km, n=20):
    lat = math.radians(c[1])
    return poly([[c[0] + km / (111.32 * math.cos(lat)) * math.cos(2 * math.pi * i / n),
                  c[1] + km / 110.57 * math.sin(2 * math.pi * i / n)] for i in range(n)])


def key(date, line, start="west", south_pockets=(), north_pockets=(), note=""):
    layers = [{"faction": "north", "everywhere": True}, {"faction": "south", "geometry": un_side(line, start)}]
    layers += [{"faction": "south", "geometry": g} for g in south_pockets]
    layers += [{"faction": "north", "geometry": g} for g in north_pockets]
    return {"date": date, "layers": layers, "note": note}


APP, EF, NE = "Appleman, South to the Naktong (CMH)", "Mossman, Ebb and Flow (CMH)", "Natural Earth 10m line of control"

# Armistice line (MDL), preceded by the Han estuary boundary.
estuary = [[126.10, 37.77], [126.20, 37.80], [126.30, 37.81], [126.40, 37.78], [126.50, 37.75], [126.58, 37.74]]
mdl = [[126.667, 37.828], [126.661, 37.914], [126.666, 37.938], [126.678, 37.945], [126.696, 37.946], [126.722, 37.954],
       [126.762, 37.979], [126.847, 38.082], [126.865, 38.096], [126.903, 38.120], [126.920, 38.135], [126.940, 38.174],
       [126.954, 38.201], [126.966, 38.213], [126.972, 38.219], [127.027, 38.254], [127.090, 38.286], [127.157, 38.307],
       [127.222, 38.313], [127.254, 38.310], [127.377, 38.319], [127.472, 38.296], [127.502, 38.298], [127.561, 38.312],
       [127.754, 38.325], [127.762, 38.321], [127.775, 38.306], [127.787, 38.297], [127.801, 38.294], [127.867, 38.305],
       [127.972, 38.300], [128.040, 38.304], [128.108, 38.324], [128.172, 38.356], [128.226, 38.400], [128.249, 38.426],
       [128.268, 38.454], [128.281, 38.484], [128.285, 38.520], [128.277, 38.554], [128.275, 38.571], [128.281, 38.584],
       [128.308, 38.601], [128.365, 38.624]]
armistice = estuary + mdl
salient = [[127.47, 38.30], [127.50, 38.33], [127.55, 38.38], [127.60, 38.40], [127.70, 38.41], [127.78, 38.40],
           [127.85, 38.36], [127.92, 38.32], [127.97, 38.30]]
with_salient = [p for p in armistice if p[0] < 127.47] + salient + [p for p in armistice if p[0] > 127.97]
islands = [poly([[124.55, 37.82], [124.95, 37.82], [124.95, 38.08], [124.55, 38.08]])]  # Baengnyeong group, UN-held

pusan_aug = [[128.43, 35.08], [128.38, 35.17], [128.37, 35.22], [128.38, 35.30], [128.35, 35.36], [128.47, 35.38],
             [128.42, 35.45], [128.37, 35.52], [128.42, 35.60], [128.45, 35.70], [128.38, 35.85], [128.40, 35.99],
             [128.37, 36.12], [128.30, 36.25], [128.28, 36.33], [128.45, 36.42], [128.70, 36.40], [129.00, 36.48],
             [129.30, 36.47], [129.40, 36.45]]
pusan_sep = [[128.43, 35.08], [128.37, 35.17], [128.38, 35.30], [128.35, 35.36], [128.47, 35.38], [128.45, 35.45],
             [128.44, 35.50], [128.40, 35.57], [128.45, 35.70], [128.40, 35.85], [128.42, 35.95], [128.52, 35.98],
             [128.62, 35.99], [128.75, 36.00], [128.90, 36.02], [129.10, 36.02], [129.22, 36.01], [129.38, 35.99]]
inchon_landing = poly([[126.58, 37.44], [126.66, 37.49], [126.68, 37.45], [126.62, 37.41]])
inchon_beachhead = poly([[126.58, 37.52], [126.66, 37.55], [126.72, 37.52], [126.73, 37.46], [126.70, 37.41],
                         [126.63, 37.42], [126.58, 37.46]])
xcorps_0922 = poly([[126.58, 37.66], [126.70, 37.72], [126.80, 37.65], [126.88, 37.63], [126.94, 37.58], [126.96, 37.52],
                    [127.00, 37.42], [127.07, 37.30], [127.05, 37.22], [126.90, 37.18], [126.75, 37.25], [126.62, 37.40],
                    [126.58, 37.50]])
xcorps_0927 = poly([[126.55, 37.45], [126.60, 37.68], [126.75, 37.74], [127.02, 37.70], [127.18, 37.58], [127.22, 37.30],
                    [127.18, 37.10], [127.00, 37.08], [126.80, 37.18], [126.60, 37.30]])
hungnam_corridor = poly([[127.42, 39.74], [127.78, 39.78], [127.80, 39.98], [127.62, 40.06], [127.42, 40.18], [127.34, 40.43],
                         [127.19, 40.43], [127.22, 40.30], [127.33, 40.12], [127.42, 39.95]])
hungnam_perimeter = poly([[127.47, 39.72], [127.45, 39.80], [127.43, 39.90], [127.42, 40.03], [127.60, 40.05],
                          [127.75, 39.98], [127.82, 39.90], [127.95, 39.80], [127.60, 39.62]])
chosan_corridor = poly([[125.92, 40.08], [126.02, 40.08], [126.00, 40.56], [125.85, 40.84], [125.76, 40.83], [125.90, 40.55]])

territories = [
    key("1950-06-25", [[W, 38.0], [E, 38.0]], note="38th parallel; Ongjin and Kaesong south-held. " + APP + " ch.3"),
    key("1950-06-26", [[W, 37.72], [126.1, 37.72], [126.5, 37.85], [126.8, 37.97], [127.2, 38.0], [E, 38.0]],
        north_pockets=[circle([128.95, 37.80], 7), circle([129.34, 37.23], 7)],
        note="Kaesong (25 Jun) and Ongjin (26 Jun) lost; KPA landings on the east coast. " + APP + " ch.3"),
    key("1950-06-28", [[126.55, 37.72], [126.85, 37.58], [126.98, 37.53], [127.20, 37.55], [127.35, 37.62], [127.55, 37.75],
                       [127.75, 37.83], [128.10, 37.80], [128.50, 37.75], [128.90, 37.72]], note="Seoul falls. " + APP + " ch.3, 5"),
    key("1950-07-04", [[126.72, 37.30], [127.01, 37.24], [127.25, 37.25], [127.45, 37.28], [127.70, 37.40], [127.95, 37.37],
                       [128.20, 37.40], [128.50, 37.35], [128.90, 37.33], [129.22, 37.30]], note="Inchon, Suwon fall. " + APP + " ch.5, 8"),
    key("1950-07-14", [[126.65, 36.05], [127.12, 36.46], [127.30, 36.48], [127.55, 36.55], [127.85, 36.70], [128.05, 36.78],
                       [128.25, 36.85], [128.37, 36.95], [128.47, 36.88], [128.80, 36.85], [129.45, 36.70]], note="Kum River line. " + APP + " ch.8, 10"),
    key("1950-07-20", [[126.65, 35.90], [127.10, 35.80], [127.35, 36.05], [127.57, 36.28], [127.78, 36.32], [127.90, 36.48],
                       [128.05, 36.65], [128.17, 36.70], [128.45, 36.78], [128.65, 36.78], [128.95, 36.65], [129.40, 36.42]],
        note="Taejon falls; KPA 6th Div sweeps the south-west. " + APP + " ch.11-13"),
    key("1950-07-31", [[128.22, 35.05], [128.20, 35.18], [128.05, 35.45], [127.98, 35.65], [128.05, 35.90], [128.11, 36.12],
                       [128.15, 36.30], [128.30, 36.45], [128.55, 36.55], [128.75, 36.60], [129.05, 36.50], [129.38, 36.37]],
        start="south", note="Chinju falls. " + APP + " ch.12, 13"),
    key("1950-08-05", pusan_aug, start="south", note="Pusan Perimeter. " + APP + " ch.15"),
    key("1950-09-14", pusan_sep, start="south", note="Perimeter after the August-September battles. " + APP + " ch.24, 27"),
    key("1950-09-15", pusan_sep, start="south", south_pockets=[inchon_landing], note="Inchon landing. " + APP + " ch.25"),
    key("1950-09-16", pusan_sep, start="south", south_pockets=[inchon_beachhead], note="Inchon beachhead. " + APP + " ch.25"),
    key("1950-09-22", [[128.30, 35.10], [128.25, 35.20], [128.33, 35.38], [128.38, 35.52], [128.38, 35.72], [128.35, 35.90],
                       [128.38, 36.02], [128.55, 36.08], [128.65, 36.10], [128.95, 36.12], [129.20, 36.10], [129.40, 36.10]],
        start="south", south_pockets=[xcorps_0922], note="Breakout; Marines in western Seoul. " + APP + " ch.26-27"),
    key("1950-09-27", [[127.75, 35.07], [127.80, 35.40], [128.00, 35.80], [128.11, 36.12], [127.78, 36.20], [127.55, 36.35],
                       [127.49, 36.64], [127.15, 36.81], [127.07, 37.15], [127.20, 37.18], [127.75, 36.50], [128.16, 36.41],
                       [128.73, 36.57], [129.20, 36.85], [129.42, 36.95]],
        start="south", south_pockets=[xcorps_0927], note="Link-up near Osan; KPA bypassed in Cholla. " + APP + " ch.28"),
    key("1950-09-30", [[126.60, 37.75], [126.80, 37.70], [127.05, 37.70], [127.30, 37.55], [127.60, 37.45], [127.95, 37.30],
                       [128.20, 37.15], [128.50, 37.40], [128.80, 37.93]], note="Nominal edge of UN control. " + APP + " ch.28"),
    key("1950-10-10", [[126.15, 37.90], [126.30, 38.00], [126.50, 38.05], [126.90, 38.15], [127.20, 38.35], [127.40, 38.70],
                       [127.44, 39.10], [127.50, 39.20]], note="Across the 38th; Wonsan taken. Centre approximate. " + APP + " ch.30"),
    key("1950-10-20", [[125.55, 39.45], [125.66, 39.41], [125.93, 39.43], [126.22, 39.30], [126.83, 39.22], [127.30, 39.60],
                       [127.53, 39.97], [128.00, 40.08]], note="Pyongyang taken. " + APP + " ch.31"),
    key("1950-10-26", [[125.45, 39.60], [125.60, 39.75], [125.82, 40.12], [125.97, 40.08], [126.28, 40.17], [126.60, 40.05],
                       [127.00, 40.10], [127.35, 40.15], [127.80, 40.15], [128.33, 40.25], [128.90, 40.45]],
        south_pockets=[chosan_corridor], note="ROK patrol at Chosan; PVA First Phase. " + APP + " ch.33, 38"),
    key("1950-11-06", [[125.40, 39.62], [125.58, 39.78], [125.72, 39.72], [125.95, 39.65], [126.30, 39.72], [126.6, 39.80],
                       [127.0, 40.0], [127.35, 40.13], [127.8, 40.4], [128.15, 40.85], [128.7, 40.95], [129.35, 40.98]],
        note="Chongchon bridgehead. " + APP + " ch.35, 38"),
    key("1950-11-24", [[125.30, 39.62], [125.55, 39.80], [125.80, 39.88], [126.10, 39.92], [126.32, 39.80], [126.55, 39.85],
                       [127.11, 40.48], [127.27, 40.50], [127.6, 40.7], [127.75, 41.38], [128.18, 41.40], [128.78, 41.15],
                       [129.70, 41.73]], note="Home-by-Christmas offensive; Hyesanjin, Chosin. " + APP + " ch.38; " + EF + " ch.4-5"),
    key("1950-12-06", [[125.30, 38.70], [125.62, 38.74], [126.00, 38.78], [126.40, 38.76], [126.53, 38.50], [127.3, 38.45],
                       [128.0, 38.45], [128.65, 38.45]],
        south_pockets=[hungnam_corridor, circle([127.44, 39.15], 8), circle([129.20, 40.67], 6)],
        note="Pyongyang abandoned; X Corps enclaves. East of Singye approximate. " + EF + " ch.6-8"),
    key("1950-12-15", [[126.68, 37.77], [126.79, 37.86], [126.87, 37.98], [127.06, 38.10], [127.40, 38.15], [127.71, 38.11],
                       [128.20, 38.08], [128.65, 38.08]], south_pockets=[hungnam_perimeter],
        note="Between Lines A and B; Hungnam perimeter. " + EF + " ch.8"),
    key("1950-12-24", [[126.68, 37.77], [126.79, 37.86], [126.87, 37.98], [127.06, 38.10], [127.40, 38.10], [127.71, 38.11],
                       [127.73, 38.00], [128.20, 38.05], [128.65, 38.05]], note="Line B; Hungnam evacuated. " + EF + " ch.8"),
    key("1950-12-31", [[126.68, 37.77], [126.79, 37.86], [126.87, 37.98], [127.06, 38.10], [127.40, 38.10], [127.71, 38.11],
                       [127.73, 38.00], [128.20, 38.05], [128.65, 38.05]], note="Line B at the start of the Third Phase."),
    key("1951-01-04", [[126.6, 37.45], [126.95, 37.50], [127.2, 37.50], [127.5, 37.50], [127.9, 37.55], [128.3, 37.55],
                       [128.9, 37.60], [129.1, 37.65]], note="Han River line as Seoul falls. Approximate. " + EF + " ch.11"),
    key("1951-01-08", [[126.85, 36.98], [127.09, 36.96], [127.28, 37.03], [127.64, 37.12], [127.78, 37.20], [127.95, 37.27],
                       [128.19, 37.20], [128.50, 37.22], [128.66, 37.38], [129.10, 37.48]],
        note="Line D. " + EF + " ch.11"),
    key("1951-01-25", [[126.85, 37.10], [127.07, 37.16], [127.20, 37.24], [127.44, 37.27], [127.64, 37.31], [127.95, 37.36],
                       [128.20, 37.38], [128.40, 37.40], [128.75, 37.55], [129.05, 37.62]],
        note="Operation Thunderbolt start. " + EF + " ch.12"),
    key("1951-02-15", [[126.55, 37.72], [126.75, 37.60], [126.90, 37.53], [127.10, 37.53], [127.35, 37.52], [127.55, 37.47],
                       [127.63, 37.50], [127.70, 37.42], [127.85, 37.38], [127.95, 37.37], [128.10, 37.25], [128.18, 37.22],
                       [128.40, 37.26], [128.65, 37.50], [128.95, 37.80]], note="Chipyong-ni; Inchon retaken 10 Feb. " + EF + " ch.13, 15"),
    key("1951-03-15", [[126.55, 37.73], [126.80, 37.60], [126.98, 37.62], [127.25, 37.65], [127.42, 37.73], [127.70, 37.75],
                       [127.90, 37.73], [128.10, 37.70], [128.45, 37.75], [128.70, 37.77], [128.83, 37.90]],
        note="Seoul retaken. " + EF + " ch.17"),
    key("1951-03-31", [[126.68, 37.77], [126.79, 37.86], [126.87, 37.98], [127.05, 37.97], [127.40, 37.93], [127.73, 37.93],
                       [128.00, 37.92], [128.30, 37.95], [128.64, 38.12]], note="End of Operation Ripper. " + EF + " ch.17-18"),
    key("1951-04-21", [[126.68, 37.77], [126.87, 37.98], [127.00, 38.08], [127.15, 38.15], [127.20, 38.18], [127.40, 38.20],
                       [127.60, 38.15], [127.78, 38.12], [127.95, 38.15], [128.17, 38.10], [128.35, 38.15], [128.63, 38.15]],
        note="Lines Utah/Wyoming, eve of the Spring Offensive. " + EF + " ch.19-20"),
    key("1951-04-30", [[126.60, 37.68], [126.85, 37.66], [127.00, 37.68], [127.15, 37.65], [127.33, 37.62], [127.55, 37.70],
                       [127.80, 37.75], [127.85, 37.88], [127.98, 38.05], [128.10, 37.95], [128.17, 38.02], [128.35, 38.05],
                       [128.63, 38.10]], note="No Name Line. " + EF + " ch.24"),
    key("1951-05-20", [[126.60, 37.68], [127.00, 37.68], [127.33, 37.62], [127.55, 37.70], [127.80, 37.75], [127.95, 37.80],
                       [128.08, 37.76], [128.20, 37.78], [128.40, 37.70], [128.47, 37.65], [128.56, 37.62], [128.63, 37.65],
                       [128.75, 37.85], [128.83, 37.93]], note="Fifth Phase, second step; ROK III Corps collapse. " + EF + " ch.25-26"),
    key("1951-06-15", [[126.68, 37.77], [126.87, 37.98], [127.00, 38.08], [127.12, 38.20], [127.15, 38.24], [127.22, 38.29],
                       [127.47, 38.30], [127.62, 38.20], [127.75, 38.15], [127.90, 38.18], [128.00, 38.17], [128.12, 38.25],
                       [128.25, 38.30], [128.40, 38.40], [128.46, 38.45]], south_pockets=islands,
        note="Lines Wyoming/Kansas. " + EF + " ch.26-27"),
    key("1951-10-25", with_salient, south_pockets=islands, note="After Heartbreak Ridge and Operation Commando; near the final line."),
    key("1953-07-12", with_salient, south_pockets=islands, note="Kumsong salient before the last Chinese offensive."),
    key("1953-07-20", armistice, south_pockets=islands, note="After the Kumsong offensive. " + NE),
    key("1953-07-27", armistice, south_pockets=islands, note="Armistice line (MDL). " + NE),
]

events = [
    ("1950-06-25", "The invasion", "North Korean forces cross the 38th parallel before dawn.", [127.0, 37.95], 0, True),
    ("1950-06-28", "Seoul falls", "Day 4. South Korea's capital is lost.", [126.98, 37.57], 0, False),
    ("1950-07-05", "Battle of Osan", "The first American troops to fight are overrun.", [127.07, 37.15], 0, False),
    ("1950-07-20", "Taejon falls", "The US 24th Division is driven out.", [127.38, 36.35], 0, False),
    ("1950-08-04", "The Pusan Perimeter", "UN forces hold the last corner of Korea behind the Naktong River.", [128.45, 35.75], 1.5, True),
    ("1950-09-15", "Inchon", "An amphibious landing far behind North Korean lines.", [126.62, 37.47], 2, True),
    ("1950-09-27", "Seoul retaken", "Forces from Inchon and Pusan link up. North Korea's army collapses.", [126.98, 37.57], 0, False),
    ("1950-10-01", "Across the 38th", "South Korean troops push into the North.", [128.6, 38.1], 0, False),
    ("1950-10-19", "Pyongyang taken", "That night, Chinese troops begin crossing the Yalu.", [125.75, 39.03], 1.5, True),
    ("1950-10-25", "China enters the war", "Its first offensive strikes as a patrol reaches the Yalu.", [125.9, 40.1], 1.5, False),
    ("1950-11-24", "Home by Christmas", "The UN offensive meant to end the war begins.", [126.1, 39.9], 0, True),
    ("1950-11-27", "Chosin Reservoir", "Chinese forces surround US Marines in sub-zero cold.", [127.25, 40.45], 1, False),
    ("1950-12-05", "Pyongyang abandoned", "The UN retreat from the North.", [125.75, 39.03], 0, False),
    ("1950-12-24", "Hungnam evacuated", "About 100,000 troops and 98,000 civilians leave by sea.", [127.62, 39.83], 0, False),
    ("1951-01-04", "Seoul falls again", "The capital changes hands for the third time.", [126.98, 37.57], 0, True),
    ("1951-02-13", "Chipyong-ni", "A surrounded US regiment holds. China's advance stalls.", [127.63, 37.47], 0, False),
    ("1951-03-15", "Seoul retaken again", "Fourth change of hands. The city lies in ruins.", [126.98, 37.57], 0, False),
    ("1951-04-11", "MacArthur relieved", "Truman removes the UN commander.", None, 0, False),
    ("1951-04-22", "Spring Offensive", "China's largest attack of the war.", [127.2, 38.0], 1, True),
    ("1951-07-10", "Talks begin", "Negotiations open at Kaesong. Two more years of fighting follow.", [126.55, 37.97], 2, True),
    ("1951-10-13", "Heartbreak Ridge", "Weeks of fighting for a few hills. This is the war now.", [128.03, 38.28], 1.5, False),
    ("1953-07-13", "The last offensive", "China pushes the line back one final time at Kumsong.", [127.60, 38.40], 1, False),
    ("1953-07-27", "Armistice", "Signed at Panmunjom. No peace treaty has ever followed.", [126.68, 37.96], 2, True),
]

video = {
    "id": "korean-war",
    "draft": False,
    "header": {
        "title": "The Korean War",
        "subtitle": "25 Jun 1950 - 27 Jul 1953",
        "hook": "The front swept the length of Korea twice. Then it froze for two years.",
        "globe": {"from": [70, 22], "to": [127.6, 37.8]},
        "footnote": "Front lines simplified from US Army official histories.",
        "outro": "The line where the fighting stopped still divides Korea today.",
        "watermark": "Borderclock",
    },
    "map": {
        "projection": "conicEqualArea",
        "bounds": [[124.0, 33.0], [131.0, 43.0]],
        "theatre": ["South Korea", "North Korea"],
        "labels": [
            {"text": "China", "at": [125.2, 42.3], "kind": "country"},
            {"text": "Japan", "at": [130.6, 33.6], "kind": "country", "size": 20},
            {"text": "Yellow Sea", "at": [124.6, 36.3], "kind": "sea"},
            {"text": "Sea of Japan", "at": [130.4, 39.0], "kind": "sea", "size": 17},
            {"text": "Yalu", "at": [125.9, 41.15], "kind": "sea", "size": 15},
            {"text": "Seoul", "at": [126.98, 37.57], "kind": "city"},
            {"text": "Pyongyang", "at": [125.75, 39.03], "kind": "city"},
            {"text": "Pusan", "at": [129.04, 35.18], "kind": "city"},
            {"text": "Taegu", "at": [128.60, 35.87], "kind": "city"},
            {"text": "Taejon", "at": [127.38, 36.35], "kind": "city"},
            {"text": "Inchon", "at": [126.63, 37.46], "kind": "city", "size": 15},
            {"text": "Kaesong", "at": [126.55, 37.97], "kind": "city", "size": 15},
            {"text": "Wonsan", "at": [127.44, 39.15], "kind": "city"},
            {"text": "Hungnam", "at": [127.62, 39.83], "kind": "city"},
            {"text": "Chosin Res.", "at": [127.25, 40.45], "kind": "city", "size": 15},
        ],
    },
    "factions": [
        {"id": "north", "name": "North Korea & China", "color": "#c0473b", "ink": "#7a1f17", "marker": "diamond"},
        {"id": "south", "name": "South Korea & UN", "color": "#3f6f9a", "ink": "#1d3d5c", "marker": "square"},
    ],
    "territories": territories,
    "timeline": {
        "start": "1950-06-25", "end": "1953-07-27", "introSeconds": 5, "outroSeconds": 12, "daysPerSecond": 2.9,
        "pace": [
            {"from": "1950-09-13", "to": "1950-09-18", "daysPerSecond": 1},
            {"from": "1950-11-22", "to": "1950-12-26", "daysPerSecond": 1.5},
            {"from": "1951-07-11", "to": "1953-07-05", "daysPerSecond": 45},
            {"from": "1953-07-05", "to": "1953-07-27", "daysPerSecond": 2},
        ],
    },
    "camera": [
        {"date": "1950-06-25", "center": [127.6, 38.0], "zoom": 1},
        {"date": "1950-07-04", "center": [127.6, 37.6], "zoom": 1.1},
        {"date": "1950-07-25", "center": [128.0, 36.4], "zoom": 1.35},
        {"date": "1950-08-06", "center": [128.4, 35.9], "zoom": 1.65},
        {"date": "1950-09-12", "center": [128.3, 36.0], "zoom": 1.6},
        {"date": "1950-09-15", "center": [127.6, 36.6], "zoom": 1.35},
        {"date": "1950-09-28", "center": [127.5, 37.6], "zoom": 1.15},
        {"date": "1950-10-26", "center": [127.0, 39.6], "zoom": 1.1},
        {"date": "1950-11-26", "center": [127.3, 40.0], "zoom": 1.15},
        {"date": "1950-12-24", "center": [127.4, 38.6], "zoom": 1.05},
        {"date": "1951-01-08", "center": [127.7, 37.5], "zoom": 1.3},
        {"date": "1951-07-10", "center": [127.6, 37.9], "zoom": 1.35},
        {"date": "1953-07-08", "center": [127.5, 38.1], "zoom": 1.6},
        {"date": "1953-07-27", "center": [127.5, 38.1], "zoom": 1.6},
    ],
    "events": [
        {"date": d, "title": t, "text": x, **({"at": a} if a else {}), "holdSeconds": h, "chapter": c,
         **({"captionSeconds": 6} if d == "1953-07-27" else {})}
        for d, t, x, a, h, c in events
    ],
    "counters": [{"kind": "area", "label": "Territory held"}],
    "leaders": [
        {"factionId": "north", "name": "Kim Il Sung", "role": "North Korea"},
        {"factionId": "north", "name": "Mao Zedong", "role": "China", "from": "1950-10-19"},
        {"factionId": "south", "name": "Syngman Rhee", "role": "South Korea"},
        {"factionId": "south", "name": "Harry S. Truman", "role": "United States", "to": "1953-01-20"},
        {"factionId": "south", "name": "Dwight D. Eisenhower", "role": "United States", "from": "1953-01-20"},
        {"factionId": "south", "name": "Douglas MacArthur", "role": "UN Command", "from": "1950-07-08", "to": "1951-04-11"},
        {"factionId": "south", "name": "Matthew Ridgway", "role": "UN Command", "from": "1951-04-11", "to": "1952-05-12"},
        {"factionId": "south", "name": "Mark W. Clark", "role": "UN Command", "from": "1952-05-12"},
    ],
    "audio": {"music": [{"src": "music/Uprising.mp3", "volume": 1}], "eventSfxVolume": 0.5},
    "youtube": {
        "title": "The Korean War, Day by Day (1950-1953)",
        "summary": "Every day of the Korean War on one map: the invasion, the Pusan Perimeter, Inchon, China's entry, the retreat from the North, and two years of stalemate that drew the line still dividing Korea.",
        "sources": [
            "Roy E. Appleman, South to the Naktong, North to the Yalu (US Army Center of Military History, 1961)",
            "Billy C. Mossman, Ebb and Flow: November 1950 - July 1951 (US Army Center of Military History, 1990)",
            "Armistice line: Natural Earth 10m boundary lines (line of control)",
            "Hungnam evacuation and Kumsong offensive figures: Wikipedia, 'Hungnam evacuation' and 'Battle of Kumsong'",
        ],
        "credits": ["Uprising by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au"],
        "tags": ["Korean War", "Korean War map", "Korean War every day", "Korean War day by day", "Inchon", "Pusan Perimeter", "DMZ"],
    },
    "thumbnail": {"date": "1950-09-14", "text": "One corner left", "textAt": "top-left", "highlight": [128.85, 35.5],
                  "zoom": 1.25, "center": [127.8, 37.0]},
}

out = os.path.join(os.path.dirname(__file__), "..", "data", "videos", "korean-war.json")
with open(out, "w") as f:
    json.dump(video, f, indent=1)
    f.write("\n")
print("wrote", os.path.normpath(out), len(territories), "keyframes,", len(events), "events")
