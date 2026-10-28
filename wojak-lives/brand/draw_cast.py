"""Draws the Wojak Lives cast (our own Wojak drawings) as layered SVG and renders PNGs with the preinstalled Chromium.

    python3 wojak-lives/brand/draw_cast.py

Writes character_sheet.png, expressions.png, pfp.png (+ pfp_small_test.png), thumbnail_mock.png
and caption_style.png next to this file. Every character is a half-body Wojak (3/4 view, facing
right, cropped at the waist like the meme), built from the same parts: head + ear, heavy-lidded eyes
with bags, hooked nose line, torso, sleeves/hands, yellow name tag. The SVG groups double as a
cut-out rig: export each <g id=...> as its own layer for animation.
"""
import itertools
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

INK = "#151515"
PAPER = "#FFF8EC"
TAG = "#FFD23F"
BLUE = "#3D7BFF"
CORAL = "#FF6B4A"
NPC = "#A9AEB4"
WOJAK = "#FBF7F1"  # the classic near-white Wojak skin
SKIN = {"W": WOJAK, "S1": "#FBDCC4", "S2": "#EDBF98", "S3": "#D29E73", "S4": "#A86B45", "S5": "#6B4329"}
FLASH = {"red": "#F0625A", "pink": "#F7A8C4", "grey": "#B9BEC3", "green": "#B5D98A"}
LW = 6   # outline width
FW = 4.5  # facial feature width

_uid = itertools.count()


def uid(prefix):
    return f"{prefix}{next(_uid)}"


def p(d, fill="none", w=FW, color=INK, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round"{extra}/>')


# ---------------------------------------------------------------- head (origin: under the jaw, face looks right)
HEAD = ("M -55,4 C -62,-30 -106,-62 -112,-122 C -124,-214 -84,-302 6,-306 C 92,-309 130,-256 127,-190 "
        "C 126,-160 133,-130 129,-102 C 124,-60 106,-26 70,-13 C 50,-6 30,-8 22,4 Z")
HEAD_LINE = HEAD[:-2]  # outline without the neck edge, so the collar line stays the only line there
EAR = ("M -86,-188 C -124,-200 -132,-118 -92,-116", "M -98,-172 C -112,-166 -112,-142 -99,-136")
NEAR, FAR = (26, -168), (98, -171)


def eye(cx, cy, s=1.0, open_=1.0, gaze=(0, 0), pupil=6.0, bags=True, lashes=False, closed_happy=False,
        tired=False):
    """Almond Wojak eye. open_ scales the eye height (heavy lids < 1 < wide)."""
    if closed_happy:
        return p(f"M {cx - 24 * s},{cy + 4} C {cx - 10 * s},{cy - 14} {cx + 12 * s},{cy - 14} {cx + 24 * s},{cy + 2}",
                 w=FW + 1)
    up, lo = 13 * open_, 9 * max(open_, 0.6)
    shape = (f"M {cx - 26 * s},{cy + 2} C {cx - 14 * s},{cy - up} {cx + 12 * s},{cy - up - 1} {cx + 26 * s},{cy - 3} "
             f"C {cx + 12 * s},{cy + lo} {cx - 10 * s},{cy + lo + 1} {cx - 26 * s},{cy + 2} Z")
    cid = uid("eye")
    out = [f'<clipPath id="{cid}"><path d="{shape}"/></clipPath>', f'<path d="{shape}" fill="white"/>',
           f'<g clip-path="url(#{cid})"><circle cx="{cx + gaze[0] * s}" cy="{cy + 1 + gaze[1]}" r="{pupil * s}" '
           f'fill="{INK}"/></g>',
           p(f"M {cx - 26 * s},{cy + 2} C {cx - 14 * s},{cy - up} {cx + 12 * s},{cy - up - 1} {cx + 26 * s},{cy - 3}",
             w=FW + 1.5),
           p(f"M {cx - 22 * s},{cy + 4} C {cx - 8 * s},{cy + lo + 1} {cx + 10 * s},{cy + lo} {cx + 22 * s},{cy + 1}",
             w=FW - 1.5)]
    if bags:
        out.append(p(f"M {cx - 20 * s},{cy + 17} C {cx - 6 * s},{cy + 24} {cx + 10 * s},{cy + 23} {cx + 20 * s},{cy + 14}",
                     w=FW + (1.5 if tired else -1.5), color="#6E6259" if tired else INK))
    if lashes:
        out.append(p(f"M {cx + 24 * s},{cy - 4} L {cx + 33 * s},{cy - 12} M {cx + 18 * s},{cy - 9} L {cx + 24 * s},{cy - 19}",
                     w=FW - 1))
    return "".join(out)


BROWS = {  # near brow, far brow
    "flat": ("M 6,-200 C 20,-206 40,-208 54,-205", "M 82,-206 C 96,-209 108,-206 118,-201"),
    "sad": ("M 6,-196 C 22,-200 40,-208 52,-214", "M 82,-214 C 94,-208 106,-202 118,-197"),
    "angry": ("M 6,-214 C 22,-210 40,-202 54,-194", "M 80,-194 C 94,-202 106,-210 118,-214"),
    "up": ("M 4,-214 C 20,-224 40,-224 54,-218", "M 82,-220 C 96,-226 108,-224 118,-216"),
}
NOSE = "M 66,-166 C 64,-146 60,-132 70,-124 C 80,-120 88,-126 84,-134"

# expression -> parts
EXPRESSIONS = {
    "feels":   dict(eye=dict(open_=0.85), brows="sad", mouth="M 46,-88 C 62,-93 82,-92 98,-86"),
    "bloomer": dict(eye=dict(closed_happy=True), brows="up", mouth="M 44,-96 C 58,-74 88,-72 102,-94",
                    blush=True),
    "crying":  dict(eye=dict(open_=0.8, gaze=(0, 2)), brows="sad", tears=True,
                    mouth="M 44,-84 C 52,-94 60,-80 68,-90 C 76,-98 86,-82 98,-90"),
    "rage":    dict(eye=dict(open_=1.1, pupil=4), brows="angry", flash="red",
                    mouth="M 40,-104 C 60,-112 92,-112 108,-102 C 104,-74 46,-72 40,-104 Z", teeth=True),
    "soy":     dict(eye=dict(open_=1.6, pupil=4.5), brows="up",
                    mouth="M 40,-108 C 50,-56 102,-54 110,-108 C 90,-116 58,-116 40,-108 Z", teeth=True),
    "smug":    dict(eye=dict(open_=0.55, gaze=(-8, 1)), brows="flat", mouth="M 46,-86 C 66,-86 86,-92 102,-104"),
    "side-eye": dict(eye=dict(open_=0.7, gaze=(-12, 1)), brows="flat", mouth="M 48,-88 C 64,-86 80,-92 96,-88",
                     sweat=True),
    "doomer":  dict(eye=dict(open_=0.5, pupil=5, tired=True), brows="flat", flash="grey",
                    mouth="M 48,-88 L 96,-88", stubble=True),
}


def face(expr, female=False, npc=False):
    if npc:  # the NPC meme face: dot eyes, triangle nose, flat mouth
        return (f'<circle cx="34" cy="-170" r="7" fill="{INK}"/><circle cx="100" cy="-172" r="6" fill="{INK}"/>'
                + p("M 68,-160 L 54,-120 L 80,-120 Z") + p("M 46,-88 L 98,-88") + p(BROWS["flat"][0]) +
                p(BROWS["flat"][1]))
    e = EXPRESSIONS[expr]
    kw = dict(e["eye"])
    out = [eye(*NEAR, 1.22, bags=not female, lashes=female, **kw),
           eye(*FAR, 0.95, bags=not female, lashes=female, **kw),
           p(BROWS[e["brows"]][0], w=FW), p(BROWS[e["brows"]][1], w=FW), p(NOSE)]
    if not female:  # the classic Wojak creases: forehead worry lines, cheek line, chin crease
        if e["brows"] in ("sad", "flat"):
            out.append(p("M 30,-238 C 50,-244 70,-244 90,-238 M 42,-254 C 56,-258 72,-258 84,-254", w=2.5))
        out.append(p("M 114,-130 C 120,-114 118,-100 112,-88 M 72,-50 C 82,-46 94,-48 102,-54", w=2.5))
    if e.get("stubble"):
        dots = [(x, y) for x in range(10, 118, 9) for y in range(-74, -20, 9)
                if (x * 7 + y * 3) % 5 and (x - 70) ** 2 / 55 ** 2 + (y + 48) ** 2 / 30 ** 2 < 1]
        out.append("".join(f'<circle cx="{x + (y % 4)}" cy="{y}" r="1.8" fill="#5A5A5A"/>' for x, y in dots))
    mouth = e["mouth"]
    if mouth.endswith("Z"):
        out.append(p(mouth, fill="#5C1E1E", w=FW))
        if e.get("teeth"):
            cid = uid("m")
            out.append(f'<clipPath id="{cid}"><path d="{mouth}"/></clipPath><g clip-path="url(#{cid})">'
                       f'<rect x="30" y="-120" width="90" height="16" fill="white"/></g>' + p(mouth, w=FW))
    else:
        out.append(p(mouth, w=FW + 0.5, color="#B5525B" if female else INK))
    if e.get("blush"):
        out.append('<ellipse cx="20" cy="-128" rx="20" ry="10" fill="#FF8A8A" opacity=".5"/>'
                   '<ellipse cx="112" cy="-130" rx="12" ry="8" fill="#FF8A8A" opacity=".5"/>')
    if e.get("tears"):
        out.append(p("M 16,-150 C 12,-124 20,-100 14,-62 M 92,-152 C 96,-126 88,-100 94,-70", w=9, color="#6EC3F5"))
    if e.get("sweat"):
        out.append(p("M 118,-236 C 108,-214 108,-202 118,-200 C 128,-202 128,-214 118,-236 Z", fill="#8FD3FF", w=3.5))
    return "".join(out)


def head_shading():
    """Soft grey on the back of the skull and under the jaw, like the original Wojak drawing."""
    cid = uid("hs")
    return (f'<clipPath id="{cid}"><path d="{HEAD}"/></clipPath><g clip-path="url(#{cid})" fill="{INK}">'
            f'<ellipse cx="-128" cy="-140" rx="58" ry="190" opacity=".07"/>'
            f'<ellipse cx="-10" cy="4" rx="80" ry="34" opacity=".10"/></g>')


# ---------------------------------------------------------------- headwear (behind = drawn before head)
def hair_behind(kind, color):
    if kind == "long":
        return p("M -120,-150 C -150,-300 -60,-350 20,-345 C 110,-342 160,-280 150,-170 C 146,-90 170,-10 150,60 "
                 "L -140,60 C -150,0 -116,-80 -120,-150 Z", fill=color, w=LW)
    if kind == "hijab":
        return p("M -140,-140 C -156,-300 -64,-352 14,-350 C 112,-348 166,-286 160,-170 C 156,-90 176,-20 196,40 "
                 "L -176,40 C -150,-20 -134,-70 -140,-140 Z", fill=color, w=LW)
    return ""


def hair_front(kind, color):
    if kind == "long":  # fringe + side lock that leaves the face open
        return (p("M -118,-150 C -126,-280 -50,-336 30,-330 C 104,-326 140,-276 134,-210 C 110,-250 80,-262 50,-246 "
                  "C 20,-270 -30,-262 -60,-230 C -80,-200 -90,-170 -92,-120 Z", fill=color, w=LW))
    if kind == "hijab":  # front wrap: everything but the face oval (even-odd hole)
        return (f'<path d="M -146,-150 C -160,-306 -64,-356 14,-354 C 116,-352 170,-290 164,-170 C 160,-90 178,-20 '
                f'198,40 L -178,40 C -152,-20 -140,-80 -146,-150 Z M 68,-246 C 120,-246 144,-200 142,-140 '
                f'C 140,-70 110,-30 66,-30 C 20,-30 -6,-74 -8,-140 C -10,-200 16,-246 68,-246 Z" fill="{color}" '
                f'fill-rule="evenodd" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if kind == "beanie":
        return (p("M -116,-200 C -120,-300 -40,-338 20,-336 C 90,-334 136,-290 132,-206 Z", fill=color, w=LW) +
                p("M -122,-206 C -40,-222 60,-226 136,-204 L 134,-176 C 60,-198 -40,-196 -120,-176 Z",
                  fill=color, w=LW))
    if kind == "headphones":
        return (hair_front("beanie", color) +
                p("M -112,-160 C -150,-330 150,-350 128,-150", w=16) +
                '<rect x="-128" y="-196" width="44" height="84" rx="18" fill="#222" stroke="#151515" stroke-width="6"/>')
    if kind == "combover":
        return p("M -104,-210 C -70,-290 60,-300 122,-236 C 60,-262 -30,-258 -104,-210 Z", fill=INK, w=3)
    if kind == "boomer":  # grey side hair + sunglasses + mustache
        return (p("M -112,-150 C -122,-190 -112,-220 -96,-232 C -98,-210 -96,-180 -88,-150 Z", fill="#9E9E9E", w=3) +
                p("M 0,-188 L 128,-190 L 124,-160 C 112,-142 82,-144 76,-164 L 64,-166 C 56,-144 18,-140 4,-160 Z",
                  fill=INK, w=3) +
                p("M 48,-106 C 60,-122 80,-122 104,-108 C 84,-100 64,-100 48,-106 Z", fill="#6B6B6B", w=3))
    if kind == "chad":
        return p("M -110,-180 C -130,-300 -20,-350 60,-330 C 120,-318 150,-280 140,-220 C 110,-270 40,-260 0,-250 "
                 "C -40,-240 -80,-220 -96,-150 Z", fill="#F1C24A", w=LW)
    return ""


# ---------------------------------------------------------------- body (origin: waist crop line)
TORSO = ("M -160,0 L -160,-190 C -160,-252 -120,-282 -64,-292 L 30,-292 C 100,-286 156,-254 160,-190 L 160,0 Z")
HAND = "M -18,-4 C -20,-26 16,-28 20,-6 C 22,14 -16,18 -18,-4 Z M -16,-10 C -30,-14 -32,-28 -20,-24"
GESTURES = {  # sleeve path (shoulder -> hand) and hand position, in body coords; None = arms down
    "idle": None,
    "point": ("M 130,-230 C 190,-200 230,-190 280,-196", (292, -196)),
    "phone": ("M 120,-230 C 150,-150 110,-110 60,-120", (52, -128)),
    "facepalm": ("M 120,-236 C 170,-260 160,-380 110,-430", (104, -440)),
    "raise": ("M 130,-236 C 190,-280 210,-360 210,-420", (210, -432)),
}


def character(x, y, scale=1.0, skin=WOJAK, shirt=CORAL, hair="", hair_color=INK, expr="feels", pose="idle",
              tag="", female=False, npc=False, body_extras=(), wobble=True, flip=False, flash=None):
    gid = uid("char")
    if npc:
        skin = shirt = NPC
    face_fill = FLASH.get(flash or EXPRESSIONS.get(expr, {}).get("flash"), skin) if not npc else NPC
    sx = -scale if flip else scale
    out = [f'<g id="{gid}" transform="translate({x},{y}) scale({sx},{scale})"'
           f'{" filter=\"url(#wobble)\"" if wobble else ""}>']
    out.append(p(TORSO, fill=shirt, w=LW))
    out.append(p("M -112,-214 C -116,-140 -112,-60 -108,0 M 116,-214 C 118,-140 116,-60 112,0", w=FW))
    if "tie" in body_extras:
        out.append(p("M -14,-290 L 10,-290 L 18,-160 L -2,-130 L -22,-160 Z", fill="#C0392B", w=4))
        out.append(p("M -60,-292 L -2,-200 L 40,-292", w=FW))
    if "polo" in body_extras:
        out.append(p("M -50,-292 L -4,-240 L 30,-292", fill="white", w=FW))
    if "hood" in body_extras:
        out.append(p("M -96,-288 C -70,-250 20,-250 56,-288", w=FW) + p("M -40,-262 L -44,-200 M 6,-262 L 8,-200", w=3.5))
    if tag and not npc:
        out.append(f'<g transform="translate(-60,-140) scale({-1 if flip else 1},1) rotate(-5)"><rect x="-62" y="-22" '
                   f'width="124" height="44" rx="5" fill="{TAG}" stroke="{INK}" stroke-width="5"/><text x="0" y="10" '
                   f'text-anchor="middle" font-family="Lilita" font-size="{28 if len(tag) < 6 else 21}" '
                   f'fill="{INK}">{tag}</text></g>')
    head = [f'<g transform="translate(-6,-300) scale(1.12)">', hair_behind(hair, hair_color),
            f'<path d="{HEAD}" fill="{face_fill}"/>', head_shading(), p(HEAD_LINE, w=LW), p(EAR[0], w=FW),
            p(EAR[1], w=FW - 1)]
    head.append(face(expr, female, npc))
    head.append(hair_front(hair, hair_color))
    head.append("</g>")
    out.extend(head)
    g = GESTURES[pose]
    if g:
        d, (hx, hy) = g
        out.append(p(d, w=46) + p(d, color=shirt, w=46 - 2 * LW))
        out.append(f'<g transform="translate({hx},{hy})">' + p(HAND, fill=skin, w=FW) + "</g>")
        if pose == "phone":
            out.append(f'<rect x="20" y="-196" width="44" height="78" rx="8" fill="#222" stroke="{INK}" '
                       f'stroke-width="4" transform="rotate(-12 42 -157)"/>')
    out.append("</g>")
    return "".join(out)


DEFS = f"""<defs>
<filter id="wobble" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7"/>
  <feDisplacementMap in="SourceGraphic" scale="3.5"/>
</filter></defs>"""

CSS = f"""<style>
@font-face {{ font-family: Lilita; src: url('{(HERE / "fonts/lilita.woff2").as_uri()}'); }}
@font-face {{ font-family: Baloo; src: url('{(HERE / "fonts/baloo.woff2").as_uri()}'); font-weight: 800; }}
html, body {{ margin: 0; background: transparent; }}
</style>"""


def label(x, y, text, size=34, color=INK, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Lilita" font-size="{size}" '
            f'fill="{color}">{text}</text>')


def tagbox(x, y, text, size=64, rot=-3, pad=22):
    w = len(text) * size * 0.56 + 2 * pad
    h = size * 1.35
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-w / 2 + 8}" y="{-h / 2 + 8}" width="{w}" '
            f'height="{h}" rx="10" fill="{INK}"/><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="10" '
            f'fill="{TAG}" stroke="{INK}" stroke-width="7"/><text x="0" y="{size * 0.36}" text-anchor="middle" '
            f'font-family="Lilita" font-size="{size}" fill="{INK}">{text}</text></g>')


def caption(x, y, text, highlight=(), size=72):
    words = []
    for i, w in enumerate(text.split()):
        col = TAG if w.strip(".,!?").upper() in highlight else "white"
        words.append(f'<tspan fill="{col}"{f' dx="{size * 0.28:.0f}"' if i else ""}>{w}</tspan>')
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Baloo" font-weight="800" font-size="{size}" '
            f'stroke="{INK}" stroke-width="16" stroke-linejoin="round" paint-order="stroke">{"".join(words)}</text>')


def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'{DEFS}{rect}{body}</svg>')


CAST = [
    ("NOBO (host)", dict(expr="feels", body_extras=("hood",))),
    ("LULU (lead)", dict(skin=SKIN["S3"], shirt="#1FB5A8", hair="long", hair_color="#2B1B12", female=True,
                         expr="smug")),
    ("MAMA", dict(skin=SKIN["S2"], shirt="#2BB673", hair="hijab", hair_color="#7B4FD6", female=True, expr="smug")),
    ("DAD (boomer)", dict(skin=SKIN["S4"], shirt="#F2F2F2", hair="boomer", expr="feels",
                          body_extras=("polo",))),
    ("BOSS", dict(shirt="#4A5568", hair="combover", expr="smug", body_extras=("tie",))),
    ("BRO (chad-ish)", dict(skin=SKIN["S1"], shirt="#FFB000", hair="chad", expr="bloomer",
                            pose="raise")),
    ("ZOOMER", dict(skin=SKIN["S5"], shirt="#6C5CE7", hair="headphones", hair_color="#333", expr="doomer", pose="phone")),
    ("NPC (extras)", dict(npc=True)),
]


def character_sheet():
    W, H = 3000, 1220
    b = [label(60, 90, "WOJAK LIVES: CAST v3", 64, anchor="start"),
         label(60, 140, "Our own Wojak drawings, faces only: 3/4 view facing right, half-body, cropped at the waist. "
               "Near-white Wojak skin by default, flat colours, thin MS-Paint line, classic creases.", 28, "#555",
               "start")]
    for i, (name, kw) in enumerate(CAST):
        x = 210 + i * 365
        b.append(f'<g>{character(x, 860, 0.95, **kw)}</g>')
        b.append(label(x + 10, 920, name, 38))
    b.append(label(60, 1010, "SKIN", 34, anchor="start"))
    for i, (k, c) in enumerate(SKIN.items()):
        b.append(f'<rect x="{180 + i * 110}" y="975" width="90" height="56" rx="8" fill="{c}" stroke="{INK}" '
                 f'stroke-width="5"/>' + label(225 + i * 110, 1070, k, 26))
    b.append(label(900, 1010, "FACE FLASH", 34, anchor="start"))
    for i, (k, c) in enumerate(FLASH.items()):
        b.append(f'<rect x="{1110 + i * 120}" y="975" width="100" height="56" rx="8" fill="{c}" stroke="{INK}" '
                 f'stroke-width="5"/>' + label(1160 + i * 120, 1070, k.upper(), 24))
    b.append(label(1640, 1010, "BRAND", 34, anchor="start"))
    for i, (k, c) in enumerate((("INK", INK), ("TAG", TAG), ("SIGNAL", BLUE), ("NOBO", CORAL))):
        b.append(f'<rect x="{1780 + i * 120}" y="975" width="100" height="56" rx="8" fill="{c}" stroke="{INK}" '
                 f'stroke-width="5"/>' + label(1830 + i * 120, 1070, k, 24))
    b.append(label(2290, 1000, "Face flash = whole face recoloured", 28, "#555", "start"))
    b.append(label(2290, 1040, "for one beat: red rage, pink cringe,", 28, "#555", "start"))
    b.append(label(2290, 1080, "grey dead inside, green jealous/sick.", 28, "#555", "start"))
    return svg(W, H, "".join(b), PAPER)


def expression_sheet():
    W, H = 2900, 760
    b = [label(60, 90, "NOBO: 8 WOJAK FACES (swap eyes / brows / mouth, flash the face colour)", 52, anchor="start")]
    for i, ex in enumerate(EXPRESSIONS):
        x = 190 + i * 350
        e = EXPRESSIONS[ex]
        fill = FLASH.get(e.get("flash"), WOJAK)
        b.append(f'<g transform="translate({x - 20},560) scale(1.05)" filter="url(#wobble)">'
                 f'{p(HEAD, fill=fill, w=LW)}{p(EAR[0])}{p(EAR[1], w=FW - 1)}{face(ex)}</g>')
        b.append(label(x + 10, 660, ex.upper(), 40))
    return svg(W, H, "".join(b), PAPER)


def pfp():
    W = H = 1024
    inner = character(0, 0, 1.0, expr="feels", body_extras=("hood",), wobble=False)
    inner = inner.split(">", 1)[1].rsplit("</g>", 1)[0]
    body = (f'<circle cx="512" cy="512" r="512" fill="{BLUE}"/>'
            f'<g transform="translate(470,1120) scale(1.62)">{inner}</g>')
    cid = uid("pfp")
    return svg(W, H, f'<clipPath id="{cid}"><circle cx="512" cy="512" r="512"/></clipPath>'
                     f'<g clip-path="url(#{cid})" filter="url(#wobble)">{body}</g>')


def thumbnail_mock():
    W, H = 1280, 720
    b = [f'<rect width="{W}" height="{H}" fill="#CFE3F7"/>',
         '<rect y="470" width="1280" height="250" fill="#B9C4CF"/>',
         character(1130, 760, 0.8, npc=True),
         character(930, 790, 1.0, shirt="#4A5568", hair="combover", expr="smug", pose="point",
                   body_extras=("tie",), flip=True),
         character(330, 780, 1.25, skin=SKIN["S5"], shirt="#6C5CE7", hair="headphones", hair_color="#333",
                   expr="soy"),
         tagbox(900, 100, "FIRST JOB", 100, rot=-4)]
    return svg(W, H, "".join(b))


def caption_style():
    W, H = 1080, 1920
    b = [f'<rect width="{W}" height="{H}" fill="#C8D6E5"/>',
         '<rect y="1300" width="1080" height="620" fill="#A9B4C0"/>',
         label(540, 60, "9:16 STYLE FRAME (photo goes here)", 34, "#5B6B7B"),
         tagbox(540, 250, "LIFE AS AN INTROVERT", 72, rot=-3),
         caption(540, 520, "Someone said “we should", size=74),
         caption(540, 610, "hang out” and MEANT it.", highlight=("MEANT",), size=74),
         character(470, 1545, 1.45, expr="side-eye", pose="phone", body_extras=("hood",)),
         '<path d="M 0,1540 L 1080,1540 M 920,700 L 920,1540" stroke="#E53935" stroke-width="4" '
         'stroke-dasharray="14 10"/>',
         label(540, 1600, "below this line + right strip: Shorts UI covers it", 30, "#E53935"),
         label(540, 1650, "(title, channel name, like/comment buttons)", 26, "#E53935")]
    return svg(W, H, "".join(b))


RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  for (const [html, png] of JSON.parse(process.argv[1])) {
    const page = await browser.newPage();
    await page.goto('file://' + html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.locator('svg').first().screenshot({ path: png, omitBackground: true });
    await page.close();
  }
  await browser.close();
})();
"""


def render(pages):
    """Writes <name>.svg and renders <name>.png with the preinstalled Playwright (Node)."""
    jobs = []
    for name, markup in pages.items():
        (HERE / f"{name}.svg").write_text(markup)
        html = HERE / f".{name}.html"
        html.write_text(f"<!doctype html><html><head>{CSS}</head><body>{markup}</body></html>")
        jobs.append([str(html), str(HERE / f"{name}.png")])
    try:
        subprocess.run(["node", "-e", RENDER_JS, json.dumps(jobs)], check=True)
    finally:
        for html, _ in jobs:
            pathlib.Path(html).unlink()


if __name__ == "__main__":
    render({"character_sheet": character_sheet(), "expressions": expression_sheet(), "pfp": pfp(),
            "thumbnail_mock": thumbnail_mock(), "caption_style": caption_style()})
    from PIL import Image
    im = Image.open(HERE / "pfp.png")
    sheet = Image.new("RGBA", (98 + 48 + 30 + 40, 110), "white")
    sheet.paste(im.resize((98, 98), Image.LANCZOS), (10, 6))
    sheet.paste(im.resize((48, 48), Image.LANCZOS), (128, 31))
    sheet.paste(im.resize((30, 30), Image.LANCZOS), (186, 40))
    sheet.save(HERE / "pfp_small_test.png")
    print("ok")
