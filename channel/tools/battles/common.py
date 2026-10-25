"""Shared builder for the battle "every day" format (blueprint 02): war-room style, full-frame HUD, terrain,
rivers, round flag badges, arrows, force counters and a losses table. Each battle module supplies the data."""
import json, math, os

CHANNEL = "Borderclock"
TERRAIN_CREDIT = "Elevation: Terrain Tiles (Mapzen/Tilezen) on AWS Open Data, from SRTM, GMTED2010, ETOPO1 and EU-DEM (Copernicus)."


def ring(points):
    """Close a [lon, lat] ring."""
    pts = [list(p) for p in points]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


def poly(points):
    return {"type": "Polygon", "coordinates": [ring(points)]}


def multi(*polys):
    return {"type": "MultiPolygon", "coordinates": [[ring(p)] for p in polys]}


def circle(c, km, n=24):
    lat = math.radians(c[1])
    return poly([[c[0] + km / (111.32 * math.cos(lat)) * math.cos(2 * math.pi * i / n),
                  c[1] + km / 110.57 * math.sin(2 * math.pi * i / n)] for i in range(n)])


def keyframe(date, base, layers, note=""):
    """base: faction painted everywhere first; layers: [(faction, geometry), ...] painted in order."""
    out = [{"faction": base, "everywhere": True}]
    out += [{"faction": f, "geometry": g} for f, g in layers]
    return {"date": date, "layers": out, "note": note}


def ramp(start_date, end_date, total, points=None):
    """Cumulative series from 0 to total, optionally through sourced intermediate (date, value) points."""
    pts = [[start_date, 0]] + [list(p) for p in (points or [])] + [[end_date, total]]
    return pts


def video(*, id, title, subtitle, hook, outro, bounds, theatre, labels, factions, territories, timeline, events,
          arrows, forces, losses, camera, music, music_start, music_credit, sources, thumbnail, globe_to,
          footnote="Fronts simplified; losses interpolated between sourced totals.", spacing=(56, 15), density=0.5,
          relief_strength=1.0, borders="all", tags=(), summary=""):
    return {
        "id": id,
        "draft": False,
        "style": "warroom",
        "layout": "full",
        "header": {"title": title, "subtitle": subtitle, "hook": hook, "outro": outro, "footnote": footnote,
                   "watermark": CHANNEL, "globe": {"from": [globe_to[0] - 60, globe_to[1] - 12], "to": globe_to}},
        "map": {"projection": "conicEqualArea", "bounds": bounds, "theatre": theatre, "labels": labels,
                "relief": True, "reliefStrength": relief_strength, "rivers": True, "flagShape": "round",
                "markerSpacing": list(spacing), "markerDensity": density, "borders": borders, "edgeGlow": False},
        "factions": factions,
        "territories": territories,
        "timeline": {"introSeconds": 3, "outroSeconds": 6, **timeline},
        "camera": camera,
        "events": events,
        "arrows": arrows,
        "forces": forces,
        "counters": [losses],
        "audio": {"music": [{"src": f"music/{music}.mp3", "volume": 1, "startFrom": music_start}], "eventSfxVolume": 0.5},
        "youtube": {"title": f"{title}, Day by Day ({subtitle})", "summary": summary, "sources": sources,
                    "credits": [music_credit, TERRAIN_CREDIT], "tags": list(tags)},
        "thumbnail": thumbnail,
    }


def write(v):
    out = os.path.join(os.path.dirname(__file__), "..", "..", "data", "videos", f"{v['id']}.json")
    with open(out, "w") as f:
        json.dump(v, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote", os.path.normpath(out), len(v["territories"]), "keyframes,", len(v["events"]), "events,", len(v["arrows"]), "arrows")
