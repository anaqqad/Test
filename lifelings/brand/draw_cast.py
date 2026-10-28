"""Draws the Lifelings cast as layered SVG and renders PNGs with the preinstalled Chromium.

    python3 lifelings/brand/draw_cast.py

Writes character_sheet.png, expressions.png, pfp.png (+ pfp_small_test.png), thumbnail_mock.png
and caption_style.png next to this file. Every character is built from the same parts
(bean head, saucer eyes, sack body, noodle arms, mitten hands, yellow name tag), so the SVG
groups double as a cut-out rig: export each <g id=...> as its own layer for animation.
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
NPC = "#9AA0A6"
SKIN = {"S1": "#FFE0C7", "S2": "#F2C29B", "S3": "#D9A273", "S4": "#A86B45", "S5": "#6B4329"}
LW = 9  # outline width at character height ~470 units

_uid = itertools.count()


def uid(prefix):
    return f"{prefix}{next(_uid)}"


HEAD = ("M -104,-300 C -114,-420 -62,-462 0,-462 C 72,-462 118,-420 110,-310 "
        "C 104,-228 62,-205 0,-205 C -62,-205 -98,-228 -104,-300 Z")
BODY = "M -66,-222 C -84,-150 -96,-92 -90,-60 L 90,-60 C 96,-92 84,-150 66,-222 Z"
EYE_L, EYE_R = (-44, -342), (44, -342)


def eye(cx, cy, skin, gaze=(0, 0), pupil=8, lid=0.0, lid_tilt=0, rx=30, ry=37, empty=False, side=1):
    """One saucer eye. lid = fraction of the eye covered from the top (0..1)."""
    cid = uid("eye")
    out = [f'<clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath>',
           f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="white"/>']
    if not empty:
        out.append(f'<circle cx="{cx + gaze[0]}" cy="{cy + gaze[1]}" r="{pupil}" fill="{INK}"/>')
    if lid > 0:
        y = cy - ry + 2 * ry * lid
        t = lid_tilt * side
        out.append(f'<g clip-path="url(#{cid})"><path d="M {cx - rx - 5},{cy - ry - 5} L {cx + rx + 5},{cy - ry - 5} '
                   f'L {cx + rx + 5},{y - t} L {cx - rx - 5},{y + t} Z" fill="{skin}"/>'
                   f'<path d="M {cx - rx - 2},{y + t} L {cx + rx + 2},{y - t}" stroke="{INK}" stroke-width="{LW - 2}"/></g>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="{LW - 2}"/>')
    return "".join(out)


# expression -> eye params + brows + mouth (all in head coordinates)
EXPRESSIONS = {
    "deadpan":  dict(lid=0.42, mouth="M -18,-262 L 18,-262"),
    "happy":    dict(eyes="arc", mouth="M -30,-268 C -18,-240 18,-240 30,-268 Z", mouth_fill="#7A2E2E"),
    "panic":    dict(pupil=5, gaze=(0, 0), brows="M -70,-398 L -24,-388 M 70,-398 L 24,-388",
                     mouth="M -28,-258 C -28,-290 28,-290 28,-258 C 28,-236 -28,-236 -28,-258 Z", mouth_fill="#7A2E2E",
                     sweat=True),
    "side-eye": dict(lid=0.38, gaze=(16, 6), mouth="M -16,-262 C -6,-266 6,-258 18,-264", sweat=True),
    "sad":      dict(lid=0.25, lid_tilt=-9, gaze=(0, 8), brows="M -70,-388 L -26,-400 M 70,-388 L 26,-400",
                     mouth="M -20,-254 C -10,-270 10,-270 20,-254", tears=True),
    "shocked":  dict(pupil=4, rx=34, ry=42, mouth="M -10,-262 C -10,-280 10,-280 10,-262 C 10,-246 -10,-246 -10,-262 Z",
                     mouth_fill="#7A2E2E"),
    "smug":     dict(lid=0.5, lid_tilt=8, gaze=(-10, 4), mouth="M -24,-266 C -4,-258 14,-260 26,-276"),
    "dead inside": dict(empty=True, lid=0.3, mouth="M -22,-262 C -12,-256 -4,-268 6,-262 C 14,-256 20,-264 24,-262",
                        grey=True),
}


def face(skin, expr):
    e = EXPRESSIONS[expr]
    out = []
    if e.get("eyes") == "arc":
        for cx, cy in (EYE_L, EYE_R):
            out.append(f'<path d="M {cx - 26},{cy + 6} C {cx - 18},{cy - 26} {cx + 18},{cy - 26} {cx + 26},{cy + 6}" '
                       f'fill="none" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>')
        out.append(f'<ellipse cx="-66" cy="-292" rx="16" ry="9" fill="#FF8A8A" opacity=".55"/>'
                   f'<ellipse cx="66" cy="-292" rx="16" ry="9" fill="#FF8A8A" opacity=".55"/>')
    else:
        kw = {k: e[k] for k in ("gaze", "pupil", "lid", "lid_tilt", "rx", "ry", "empty") if k in e}
        out.append(eye(*EYE_L, skin, side=-1, **kw))
        out.append(eye(*EYE_R, skin, side=1, **kw))
    if "brows" in e:
        out.append(f'<path d="{e["brows"]}" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>')
    fill = e.get("mouth_fill", "none")
    out.append(f'<path d="{e["mouth"]}" fill="{fill}" stroke="{INK}" stroke-width="{LW - 1}" '
               f'stroke-linecap="round" stroke-linejoin="round"/>')
    if e.get("sweat"):
        out.append(f'<path d="M 92,-410 C 80,-386 80,-372 92,-370 C 104,-372 104,-386 92,-410 Z" fill="#8FD3FF" '
                   f'stroke="{INK}" stroke-width="5"/>')
    if e.get("tears"):
        out.append(f'<path d="M -44,-306 C -50,-280 -52,-262 -44,-258 C -36,-262 -38,-280 -44,-306 Z '
                   f'M 44,-306 C 38,-280 36,-262 44,-258 C 52,-262 50,-280 44,-306 Z" fill="#8FD3FF" '
                   f'stroke="{INK}" stroke-width="5"/>')
    if e.get("grey"):
        out.append(f'<path d="{HEAD}" fill="#6C7A89" opacity=".18"/>')
    return "".join(out)


def arm(sx, sy, ex, ey, hx, hy, sleeve, skin):
    d = f"M {sx},{sy} Q {ex},{ey} {hx},{hy}"
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{sleeve}" stroke-width="{34 - 2 * LW + 2}" stroke-linecap="round"/>'
            f'<circle cx="{hx}" cy="{hy}" r="21" fill="{skin}" stroke="{INK}" stroke-width="{LW - 1}"/>')


POSES = {  # (left arm elbow, left hand), (right arm elbow, right hand)
    "idle":   ((-108, -150), (-100, -86), (108, -150), (100, -86)),
    "wave":   ((-108, -150), (-100, -86), (150, -230), (150, -330)),
    "facepalm": ((-108, -150), (-100, -86), (110, -210), (40, -300)),
    "shrug":  ((-150, -190), (-150, -250), (150, -190), (150, -250)),
    "point":  ((-108, -150), (-100, -86), (150, -200), (200, -210)),
    "phone":  ((-108, -150), (-100, -86), (60, -130), (20, -190)),
}


def headwear(kind, color):
    if kind == "curl":
        return (f'<path d="M 4,-460 C -4,-498 32,-520 44,-500 C 54,-482 28,-470 22,-486" fill="none" '
                f'stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>')
    if kind == "hijab":  # drawn behind + around the face; face opening is the head shape scaled down
        return (f'<path d="M -128,-300 C -140,-440 -70,-490 0,-490 C 76,-490 142,-440 132,-300 '
                f'C 128,-230 110,-200 96,-190 L 112,-150 L -112,-150 L -96,-190 C -112,-205 -126,-240 -128,-300 Z" '
                f'fill="{color}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if kind == "bun":
        return (f'<circle cx="0" cy="-478" r="34" fill="{color}" stroke="{INK}" stroke-width="{LW}"/>'
                f'<path d="M -104,-330 C -112,-430 -60,-466 0,-466 C 72,-466 118,-430 110,-330 '
                f'C 80,-380 30,-400 0,-404 C -30,-400 -80,-380 -104,-330 Z" fill="{color}" stroke="{INK}" '
                f'stroke-width="{LW}" stroke-linejoin="round"/>')
    if kind == "bob":
        return (f'<path d="M -122,-236 C -138,-420 -74,-482 0,-482 C 76,-482 140,-420 124,-236 L 94,-236 '
                f'C 100,-320 92,-372 48,-396 C 20,-366 -40,-352 -94,-330 L -92,-236 Z" fill="{color}" '
                f'stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if kind == "dad":
        return (f'<path d="M -20,-462 C -24,-490 -8,-500 -6,-480 M 4,-462 C 4,-494 22,-500 20,-478 '
                f'M 24,-458 C 30,-486 46,-484 40,-466" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    if kind == "cap":
        return (f'<path d="M -106,-380 C -100,-470 100,-470 108,-380 Z" fill="{color}" stroke="{INK}" '
                f'stroke-width="{LW}" stroke-linejoin="round"/>'
                f'<path d="M 60,-384 C 120,-392 170,-386 180,-372 L 70,-372 Z" fill="{color}" stroke="{INK}" '
                f'stroke-width="{LW}" stroke-linejoin="round"/>')
    if kind == "combover":
        return (f'<path d="M -100,-380 C -60,-440 40,-450 104,-392 C 50,-418 -40,-414 -100,-380 Z" fill="{INK}"/>')
    return ""


def extras(kind):
    if kind == "mustache":
        return (f'<path d="M -40,-282 C -26,-300 -8,-296 0,-286 C 8,-296 26,-300 40,-282 C 26,-276 10,-278 0,-284 '
                f'C -10,-278 -26,-276 -40,-282 Z" fill="{INK}"/>')
    if kind == "glasses":
        return (f'<g fill="none" stroke="{INK}" stroke-width="6"><circle cx="-44" cy="-342" r="40"/>'
                f'<circle cx="44" cy="-342" r="40"/><path d="M -4,-346 L 4,-346"/></g>')
    if kind == "tie":
        return (f'<path d="M 0,-210 L 14,-196 L 8,-120 L 0,-108 L -8,-120 L -14,-196 Z" fill="#C0392B" '
                f'stroke="{INK}" stroke-width="5"/>')
    return ""


def character(x, y, scale=1.0, skin=SKIN["S2"], shirt=CORAL, pants="#2E3A59", hair="curl", hair_color=INK,
              expr="deadpan", pose="idle", tag="", face_extras=(), body_extras=(), npc=False, wobble=True, flip=False):
    gid = uid("char")
    if npc:
        skin = shirt = pants = hair_color = NPC
    la_e, la_h, ra_e, ra_h = POSES[pose]
    parts = [f'<g id="{gid}" transform="translate({x},{y}) scale({-scale if flip else scale},{scale})"'
             f'{" filter=\"url(#wobble)\"" if wobble else ""}>',
             f'<ellipse cx="0" cy="0" rx="120" ry="16" fill="{INK}" opacity=".18"/>']  # contact shadow
    if hair == "hijab":
        parts.append(headwear("hijab", hair_color))
    # legs + shoes
    parts.append(f'<path d="M -66,-64 L -70,-10 L -14,-10 L -12,-64 Z M 66,-64 L 70,-10 L 14,-10 L 12,-64 Z" '
                 f'fill="{pants}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    parts.append(f'<ellipse cx="-44" cy="-8" rx="36" ry="15" fill="{INK}"/><ellipse cx="44" cy="-8" rx="36" ry="15" '
                 f'fill="{INK}"/>')
    parts.append(f'<path d="{BODY}" fill="{shirt}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    parts.extend(extras(k) for k in body_extras)
    if tag and not npc:
        parts.append(f'<g transform="translate(0,-142) scale({-1 if flip else 1},1) rotate(-5)"><rect x="-56" y="-20" width="112" height="40" rx="5" '
                     f'fill="{TAG}" stroke="{INK}" stroke-width="5"/><text x="0" y="9" text-anchor="middle" '
                     f'font-family="Lilita" font-size="{26 if len(tag) < 6 else 20}" fill="{INK}">{tag}</text></g>')
    parts.append(arm(-62, -200, *la_e, *la_h, shirt, skin))
    face_skin = skin
    parts.append(f'<path d="{HEAD}" fill="{face_skin}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    if hair != "hijab":
        parts.append(headwear(hair, hair_color))
    if npc:
        parts.append(eye(*EYE_L, NPC, lid=0.42) + eye(*EYE_R, NPC, lid=0.42))
    else:
        parts.append(face(face_skin, expr))
    parts.extend(extras(k) for k in face_extras)
    parts.append(arm(62, -200, *ra_e, *ra_h, shirt, skin))
    parts.append("</g>")
    return "".join(parts)


DEFS = f"""<defs>
<filter id="wobble" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7"/>
  <feDisplacementMap in="SourceGraphic" scale="5"/>
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
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{rect}{body}</svg>'


def character_sheet():
    W, H = 2700, 1260
    b = [label(60, 90, "LIFELINGS: CAST SHEET v1", 64, anchor="start"),
         label(60, 140, "Bean head, saucer eyes, sack body, noodle arms, mitten hands, yellow name tag. "
               "Max 3 colours per character + tag yellow. 9px ink outline.", 28, "#555", "start")]
    cast = [
        ("NOBO (host)", dict(tag="ME", expr="deadpan")),
        ("LULU (lead)", dict(skin=SKIN["S3"], shirt="#1FB5A8", hair="bob", hair_color="#2B1B12", expr="happy",
                             tag="ME", pose="wave")),
        ("MAMA", dict(skin=SKIN["S3"], shirt="#2BB673", hair="hijab", hair_color="#7B4FD6", expr="smug", tag="MAMA")),
        ("MOM (alt)", dict(skin=SKIN["S1"], shirt="#E84393", hair="bun", hair_color="#5A3A22", expr="side-eye",
                           tag="MOM")),
        ("DAD", dict(skin=SKIN["S4"], shirt="#F2F2F2", hair="dad", face_extras=("mustache", "glasses"),
                     expr="deadpan", tag="DAD", pose="shrug")),
        ("BOSS", dict(skin=SKIN["S2"], shirt="#4A5568", hair="combover", body_extras=("tie",), expr="smug",
                      tag="BOSS")),
        ("BESTIE", dict(skin=SKIN["S5"], shirt="#FFB000", hair="cap", hair_color=BLUE, expr="happy",
                        tag="BRO", pose="phone")),
        ("NPC (extras)", dict(npc=True, hair="")),
    ]
    for i, (name, kw) in enumerate(cast):
        x = 190 + i * 330
        b.append(character(x, 820, 1.15, **kw))
        b.append(label(x, 900, name, 38))
    # skin swatches + palette
    b.append(label(60, 1020, "SKIN", 34, anchor="start"))
    for i, (k, c) in enumerate(SKIN.items()):
        b.append(f'<rect x="{180 + i * 110}" y="985" width="90" height="56" rx="8" fill="{c}" stroke="{INK}" '
                 f'stroke-width="5"/>' + label(225 + i * 110, 1080, k, 26))
    b.append(label(800, 1020, "BRAND", 34, anchor="start"))
    for i, (k, c) in enumerate((("INK", INK), ("PAPER", PAPER), ("TAG", TAG), ("SIGNAL", BLUE),
                                ("NOBO", CORAL), ("NPC", NPC))):
        b.append(f'<rect x="{950 + i * 130}" y="985" width="110" height="56" rx="8" fill="{c}" stroke="{INK}" '
                 f'stroke-width="5"/>' + label(1005 + i * 130, 1080, k, 24))
    b.append(label(1780, 1022, "Nobo is 2.2 heads tall. Head = 55% of height.", 30, "#555", "start"))
    b.append(label(1780, 1065, "Headwear swaps per identity; body never changes.", 30, "#555", "start"))
    return svg(W, H, "".join(b), PAPER)


def expression_sheet():
    W, H = 2600, 820
    b = [label(60, 90, "NOBO: EXPRESSION SET (8 faces, swap only eyes / brows / mouth)", 56, anchor="start")]
    for i, ex in enumerate(EXPRESSIONS):
        x = 175 + i * 320
        b.append(f'<g transform="translate({x},880) scale(1.15)" filter="url(#wobble)">'
                 f'<path d="{HEAD}" fill="{SKIN["S2"]}" stroke="{INK}" stroke-width="{LW}"/>{headwear("curl", INK)}'
                 f'{face(SKIN["S2"], ex)}</g>')
        b.append(label(x, 720, ex.upper(), 40))
    return svg(W, H, "".join(b), PAPER)


def pfp():
    W = H = 1024
    body = (f'<circle cx="512" cy="512" r="512" fill="{BLUE}"/>'
            f'<g transform="translate(512,1180) scale(2.05)">'
            + character(0, 0, 1.0, tag="?", expr="side-eye", wobble=False).split('>', 1)[1].rsplit('</g>', 1)[0]
            + '</g>')
    return svg(W, H, f'<g filter="url(#wobble)">{body}</g>')


def thumbnail_mock():
    W, H = 1280, 720
    b = [f'<rect width="{W}" height="{H}" fill="#CFE3F7"/>',
         '<rect y="470" width="1280" height="250" fill="#B9C4CF"/>',
         character(380, 690, 1.25, tag="NEW", expr="panic", pose="facepalm"),
         character(1160, 640, 0.75, npc=True, hair=""),
         character(960, 700, 1.05, shirt="#4A5568", hair="combover", body_extras=("tie",), expr="smug",
                   pose="point", tag="BOSS", flip=True),
         tagbox(900, 105, "FIRST JOB", 100, rot=-4)]
    return svg(W, H, "".join(b))


def caption_style():
    W, H = 1080, 1920
    b = [f'<rect width="{W}" height="{H}" fill="#C8D6E5"/>',
         '<rect y="1300" width="1080" height="620" fill="#A9B4C0"/>',
         label(540, 60, "9:16 STYLE FRAME (photo goes here)", 34, "#5B6B7B"),
         tagbox(540, 250, "LIFE AS AN INTROVERT", 72, rot=-3),
         caption(540, 560, "Someone said “we should", size=74),
         caption(540, 650, "hang out” and MEANT it.", highlight=("MEANT",), size=74),
         character(500, 1480, 1.55, tag="ME", expr="side-eye", pose="phone"),
         '<path d="M 0,1540 L 1080,1540 M 920,700 L 920,1540" stroke="#E53935" stroke-width="4" '
         'stroke-dasharray="14 10"/>', label(540, 1600, "below this line + right strip: Shorts UI covers it", 30,
         "#E53935"), label(540, 1650, "(title, channel name, like/comment buttons)", 26, "#E53935")]
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
