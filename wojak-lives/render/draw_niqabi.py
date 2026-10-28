"""Draws the veiled Wojak characters (niqab, Wojak heavy-lidded eyes) as transparent PNG cut-outs.

    python3 wojak-lives/render/draw_niqabi.py

Writes render/assets/chars/<who>_<expression>[_<hands>].png for who in girl, mom, aunty_red, aunty_green.
Drawn at 2x and downsampled for smooth MS-Paint-style lines.
"""
import pathlib

from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent / "assets" / "chars"
S = 2  # supersampling
W, H = 1000, 1400
INK = (12, 12, 12, 255)
SKIN = (233, 212, 190, 255)
BAG = (120, 104, 92, 255)
TEAR = (110, 195, 245, 255)

WHO = {  # garment colour, fold colour, eye-band offset, body width, extra bags (age)
    "girl": dict(cloth=(22, 22, 22), fold=(48, 48, 48), dx=0, width=1.0, age=0),
    "mom": dict(cloth=(30, 28, 30), fold=(58, 56, 58), dx=0, width=1.12, age=1),
    "aunty_red": dict(cloth=(86, 24, 36), fold=(120, 44, 58), dx=0, width=1.08, age=1),
    "aunty_green": dict(cloth=(26, 64, 50), fold=(44, 96, 76), dx=0, width=1.05, age=1),
}

EXPR = {  # lid (0 open .. 1 closed), lid tilt (+ = angry, inner side lower), pupil (dx, dy, r), eye height scale
    "tired": dict(lid=0.42, tilt=0, pupil=(0, 2, 12), hs=1.0),
    "wide": dict(lid=0.0, tilt=0, pupil=(0, 0, 7), hs=1.45),
    "angry": dict(lid=0.38, tilt=1, pupil=(0, 4, 11), hs=1.0),
    "side": dict(lid=0.4, tilt=0, pupil=(-26, 3, 12), hs=1.0),
    "sad": dict(lid=0.3, tilt=-1, pupil=(0, 8, 12), hs=1.0),
    "cry": dict(lid=0.3, tilt=-1, pupil=(0, 8, 12), hs=1.0, tears=True),
    "happy": dict(closed=True),
    "roll": dict(lid=0.18, tilt=0, pupil=(4, -16, 12), hs=1.05),
    "dead": dict(lid=0.5, tilt=0, pupil=None, hs=1.0, grey=True),
}


def bez(p0, p1, p2, p3, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def sc(pts):
    return [(x * S, y * S) for x, y in pts]


def line(d, pts, w, col=INK):
    d.line(sc(pts), fill=col, width=int(w * S), joint="curve")
    for x, y in (pts[0], pts[-1]):
        r = w * S / 2
        d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=col)


def eye(img, cx, cy, k, e, near):
    """One Wojak eye. k = size factor; near = the bigger eye on the left (inner side is its right)."""
    d = ImageDraw.Draw(img)
    if e.get("closed"):
        line(d, bez((cx - 48 * k, cy + 6), (cx - 20 * k, cy - 26), (cx + 22 * k, cy - 26), (cx + 48 * k, cy + 4)), 8)
        return
    hs = e["hs"]
    top = bez((cx - 54 * k, cy + 4), (cx - 22 * k, cy - 30 * k * hs), (cx + 24 * k, cy - 32 * k * hs),
              (cx + 54 * k, cy - 6))
    bot = bez((cx + 54 * k, cy - 6), (cx + 26 * k, cy + 20 * k * hs), (cx - 24 * k, cy + 22 * k * hs),
              (cx - 54 * k, cy + 4))
    shape = top + bot
    white = (205, 205, 205, 255) if e.get("grey") else (255, 255, 255, 255)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon(sc(shape), fill=255)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon(sc(shape), fill=white)
    if e["pupil"]:
        px, py, r = e["pupil"]
        r *= k
        ld.ellipse(sc([(cx + px * k - r, cy + py - r), (cx + px * k + r, cy + py + r)]), fill=INK)
    # eyelid: skin polygon over the top part of the eye, tilted for anger/sadness
    lid = e["lid"]
    if lid > 0:
        y0 = cy - 32 * k * hs
        ly = y0 + (cy + 22 * k * hs - y0) * lid
        inner = 1 if near else -1  # +x side is the inner corner for the near eye
        tilt = e["tilt"] * 14 * k
        yl, yr = ly - tilt * inner * -1, ly + tilt * inner * -1
        yl, yr = (ly + tilt, ly - tilt) if (e["tilt"] and not near) else (yl, yr)
        if e["tilt"] and near:
            yl, yr = ly - tilt, ly + tilt
        ld.polygon(sc([(cx - 70 * k, y0 - 40), (cx + 70 * k, y0 - 40), (cx + 70 * k, yr), (cx - 70 * k, yl)]),
                   fill=SKIN)
        lidline = [(cx - 56 * k, yl + (yr - yl) * (-2 / 140)), (cx + 56 * k, yr - (yr - yl) * (-2 / 140))]
    img.paste(layer, (0, 0), Image.composite(layer, Image.new("RGBA", img.size), mask).split()[3])
    d = ImageDraw.Draw(img)
    if lid > 0:
        line(d, lidline, 8)
        line(d, bot, 4)
    else:
        line(d, top, 8)
        line(d, bot, 4)


def character(who, expr, hands="none"):
    cfg, e = WHO[who], EXPR[expr]
    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cloth = cfg["cloth"] + (255,)
    fold = cfg["fold"] + (255,)
    wf = cfg["width"]
    # body / abaya: bell from the shoulders down past the frame
    left = bez((330, 560), (250, 700), (140 * wf if wf < 1 else 140 - 60 * (wf - 1), 900), (100 - 80 * (wf - 1), 1420))
    right = bez((900 + 80 * (wf - 1), 1420), (870 + 60 * (wf - 1), 900), (760, 700), (690, 560))
    body = left + right
    d.polygon(sc(body), fill=cloth)
    line(d, left, 7)
    line(d, right, 7)
    # head / hood
    d.ellipse(sc([(225, 110), (785, 700)]), fill=cloth, outline=INK, width=7 * S)
    # hood edge + folds
    line(d, bez((300, 600), (360, 690), (600, 700), (720, 610)), 4, fold)
    line(d, bez((420, 720), (400, 900), (380, 1100), (360, 1420)), 5, fold)
    line(d, bez((640, 720), (680, 920), (700, 1150), (720, 1420)), 5, fold)
    line(d, bez((520, 760), (515, 1000), (525, 1200), (530, 1420)), 3, fold)
    # eye band (niqab opening), slightly to the right for a 3/4 view
    band = bez((318, 330), (420, 296), (630, 292), (758, 322)) + bez((758, 322), (776, 380), (768, 440), (748, 466)) + \
        bez((748, 466), (630, 484), (430, 488), (322, 470)) + bez((322, 470), (300, 430), (300, 370), (318, 330))
    d.polygon(sc(band), fill=SKIN)
    line(d, band, 6)
    eye(img, 448, 392, 1.3, e, True)
    eye(img, 662, 388, 1.06, e, False)
    d = ImageDraw.Draw(img)
    if not e.get("closed"):
        for cx, k in ((448, 1.3), (662, 1.06)):
            line(d, bez((cx - 40 * k, 440), (cx - 15 * k, 452), (cx + 15 * k, 452), (cx + 40 * k, 438)), 3.5, BAG)
            if cfg["age"]:
                line(d, bez((cx - 30 * k, 456), (cx - 10 * k, 463), (cx + 10 * k, 463), (cx + 30 * k, 455)), 3, BAG)
    if e.get("tears"):
        for cx in (430, 650):
            line(d, bez((cx, 446), (cx - 8, 520), (cx + 6, 600), (cx - 4, 700)), 11, TEAR)
    if hands in ("down", "phone"):
        for hx in (300, 700):
            d.ellipse(sc([(hx - 48, 990), (hx + 48, 1100)]), fill=SKIN, outline=INK, width=6 * S)
            line(d, bez((hx - 40, 1020), (hx - 70, 1000), (hx - 66, 970), (hx - 44, 980)), 6)
    if hands == "phone":
        d.rounded_rectangle(sc([(580, 820), (710, 1030)]), radius=18 * S, fill=(30, 30, 34, 255), outline=INK,
                            width=6 * S)
        d.rounded_rectangle(sc([(598, 840), (692, 1000)]), radius=10 * S, fill=(120, 170, 255, 255))
    return img.resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for who in WHO:
        for expr in EXPR:
            character(who, expr).save(OUT / f"{who}_{expr}.png")
    for expr in ("tired", "side", "wide", "happy"):
        character("girl", expr, "phone").save(OUT / f"girl_{expr}_phone.png")
    print("ok")
