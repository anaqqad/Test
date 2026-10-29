"""Draws family Wojak characters (Mexican-mom and Asian-parents episodes) as transparent PNG cut-outs.

    python3 wojak-lives/render/draw_family.py

Reuses the Wojak rig in brand/draw_cast.py (same face for everyone, only skin tone, hair and clothes
change; no ethnic caricature) and adds hair styles and props: bun, perm, side part, messy kid hair,
mustache, glasses, apron, chancla, wooden spoon, report card. Writes render/assets/chars/<who>_<expr>.png.
"""
import importlib.util
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "assets" / "chars"
spec = importlib.util.spec_from_file_location("dc", HERE.parent / "brand" / "draw_cast.py")
dc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dc)
p, INK, LW = dc.p, dc.INK, dc.LW

_hair_front, _hair_behind = dc.hair_front, dc.hair_behind


def hair_behind(kind, color):
    if kind == "bun":
        return f'<circle cx="-70" cy="-300" r="52" fill="{color}" stroke="{INK}" stroke-width="{LW}"/>'
    return _hair_behind(kind, color)


def curls(cx, cy, r, n, spread, color):
    return "".join(f'<circle cx="{cx + (i - (n - 1) / 2) * spread}" cy="{cy}" r="{r}" fill="{color}" '
                   f'stroke="{INK}" stroke-width="4"/>' for i in range(n))


def hair_front(kind, color):
    if kind == "bun":  # pulled back with a centre part
        return (p("M -112,-170 C -126,-280 -50,-322 18,-320 C 96,-318 136,-272 130,-212 C 96,-252 50,-262 20,-258 "
                  "C -20,-256 -70,-236 -100,-160 Z", fill=color, w=LW) + p("M 22,-318 C 30,-290 34,-270 30,-256",
                                                                        w=3, color="#555"))
    if kind == "perm":  # short tight curls
        return (p("M -116,-170 C -128,-286 -40,-330 20,-326 C 100,-322 140,-270 132,-206 C 90,-236 40,-246 0,-240 "
                  "C -50,-232 -90,-206 -104,-150 Z", fill=color, w=LW) +
                curls(-10, -322, 26, 6, 34, color) + curls(-96, -250, 24, 1, 0, color) +
                curls(-108, -196, 22, 1, 0, color) + curls(118, -252, 22, 1, 0, color))
    if kind == "sidepart":
        return p("M -112,-196 C -122,-290 -40,-332 28,-326 C 104,-320 138,-272 130,-212 C 110,-240 70,-252 40,-246 "
                 "L 46,-282 C 10,-262 -50,-240 -100,-180 Z", fill=color, w=LW)
    if kind == "messy":
        return p("M -116,-190 L -134,-250 L -96,-246 L -100,-300 L -56,-280 L -40,-330 L 0,-298 L 30,-340 L 56,-298 "
                 "L 104,-318 L 100,-276 L 140,-262 L 120,-228 C 90,-252 40,-262 0,-252 C -50,-240 -90,-220 -100,-170 Z",
                 fill=color, w=LW)
    if kind == "dadstache":  # short hair + thick mustache
        return (p("M -112,-196 C -120,-284 -40,-326 26,-322 C 104,-318 138,-270 130,-212 C 96,-244 40,-254 0,-248 "
                  "C -50,-240 -90,-220 -100,-176 Z", fill=color, w=LW) +
                p("M 40,-104 C 52,-126 80,-128 108,-108 C 88,-96 62,-96 40,-104 Z", fill=color, w=3))
    if kind == "sidepart_glasses":
        return hair_front("sidepart", color) + (
            f'<g fill="none" stroke="{INK}" stroke-width="5"><circle cx="26" cy="-168" r="38"/>'
            f'<circle cx="100" cy="-170" r="32"/><path d="M 64,-170 L 68,-170 M -12,-172 L -60,-180"/></g>')
    return _hair_front(kind, color)


dc.hair_front, dc.hair_behind = hair_front, hair_behind

PROPS = {  # drawn in body coordinates after the arm; pose "raise" puts the hand at (210,-432), "phone" at (52,-128)
    "apron": ('<path d="M -90,-250 L 90,-250 L 120,0 L -120,0 Z" fill="#F4F1EA" stroke="#151515" stroke-width="6"/>'
              '<path d="M -70,-250 C -60,-290 60,-290 70,-250" fill="none" stroke="#151515" stroke-width="5"/>'
              '<rect x="-50" y="-160" width="100" height="56" rx="8" fill="#E9E3D6" stroke="#151515" stroke-width="4"/>',
              False),
    "chancla": ('<g transform="translate(222,-500) rotate(-20)"><path d="M -34,-70 C -46,-20 -40,60 -14,80 C 10,96 '
                '34,80 36,40 C 40,-10 30,-60 6,-80 C -10,-92 -28,-86 -34,-70 Z" fill="#2F7DE1" stroke="#151515" '
                'stroke-width="6"/><path d="M -24,-30 L 2,-6 L 24,-34" fill="none" stroke="#F4D03F" '
                'stroke-width="9" stroke-linecap="round"/></g>', True),
    "spoon": ('<g transform="translate(214,-470) rotate(-14)"><rect x="-8" y="-20" width="16" height="150" rx="8" '
              'fill="#B07A45" stroke="#151515" stroke-width="5"/><ellipse cx="0" cy="-48" rx="26" ry="38" '
              'fill="#B07A45" stroke="#151515" stroke-width="5"/></g>', True),
    "report": ('<g transform="translate(60,-190) rotate(-8)"><rect x="-70" y="-90" width="140" height="180" rx="6" '
               'fill="white" stroke="#151515" stroke-width="5"/><text x="0" y="20" text-anchor="middle" '
               'font-family="Lilita" font-size="64" fill="#D63031">{grade}</text>'
               '<path d="M -50,-60 L 50,-60 M -50,-40 L 30,-40" stroke="#999" stroke-width="5"/></g>', True),
}

CAST = {  # who: (rig kwargs, props, pose)
    "mxmom": (dict(skin=dc.SKIN["S3"], shirt="#C0392B", hair="bun", hair_color="#2B1B12", female=True), ["apron"],
              "idle"),
    "mxmom_chancla": (dict(skin=dc.SKIN["S3"], shirt="#C0392B", hair="bun", hair_color="#2B1B12", female=True),
                      ["apron", "chancla"], "raise"),
    "mxmom_spoon": (dict(skin=dc.SKIN["S3"], shirt="#C0392B", hair="bun", hair_color="#2B1B12", female=True),
                    ["apron", "spoon"], "raise"),
    "mxdad": (dict(skin=dc.SKIN["S4"], shirt="#ECECEC", hair="dadstache", hair_color="#1E1A18"), ["polo"], "idle"),
    "mxkid": (dict(skin=dc.SKIN["S3"], shirt="#2E86DE", hair="messy", hair_color="#2B1B12"), [], "idle"),
    "tia": (dict(skin=dc.SKIN["S2"], shirt="#8E44AD", hair="long", hair_color="#5A2D0C", female=True), [], "idle"),
    "asmom": (dict(skin=dc.SKIN["S1"], shirt="#16A085", hair="perm", hair_color="#141414", female=True), [], "idle"),
    "asmom_spoon": (dict(skin=dc.SKIN["S1"], shirt="#16A085", hair="perm", hair_color="#141414", female=True),
                    ["spoon"], "raise"),
    "asdad": (dict(skin=dc.SKIN["S1"], shirt="#7F8C8D", hair="sidepart_glasses", hair_color="#141414"), ["polo"],
              "idle"),
    "asdad_report": (dict(skin=dc.SKIN["S1"], shirt="#7F8C8D", hair="sidepart_glasses", hair_color="#141414"),
                     ["polo", "report:B+"], "phone"),
    "askid": (dict(skin=dc.SKIN["S1"], shirt="#F39C12", hair="sidepart", hair_color="#141414"), [], "idle"),
    "askid_report": (dict(skin=dc.SKIN["S1"], shirt="#F39C12", hair="sidepart", hair_color="#141414"),
                     ["report:98%"], "phone"),
    # oldest-daughter episode
    "oldsis": (dict(skin=dc.SKIN["S2"], shirt="#1FB5A8", hair="long", hair_color="#3B2314", female=True), [], "idle"),
    "oldsis_phone": (dict(skin=dc.SKIN["S2"], shirt="#1FB5A8", hair="long", hair_color="#3B2314", female=True), [],
                     "phone"),
    "omom": (dict(skin=dc.SKIN["S1"], shirt="#3D7BFF", hair="bun", hair_color="#7A4B2A", female=True), [], "idle"),
    "odad": (dict(skin=dc.SKIN["S1"], shirt="#ECECEC", hair="dadstache", hair_color="#4A3426"), ["polo"], "idle"),
    "lilbro": (dict(skin=dc.SKIN["S2"], shirt="#E74C3C", hair="messy", hair_color="#3B2314"), [], "idle"),
    "lilsis": (dict(skin=dc.SKIN["S2"], shirt="#FF8FB1", hair="long", hair_color="#8A5A36", female=True), [], "idle"),
}


def build(who, expr):
    kw, props, pose = CAST[who]
    extras = tuple(x for x in props if x == "polo")
    svg = dc.character(0, 0, 1.0, expr=expr, pose=pose, body_extras=extras, wobble=False, **kw)
    under, over = [], []
    for prop in props:
        if prop == "polo":
            continue
        name, _, arg = prop.partition(":")
        markup, on_top = PROPS[name]
        markup = markup.replace("{grade}", arg)
        (over if on_top else under).append(markup)
    # apron sits on the torso (under the head/arms), hand props sit on top of everything
    torso_end = svg.index("</path>") if "</path>" in svg else None
    head_at = svg.index('<g transform="translate(-6,-300)')
    svg = svg[:head_at] + "".join(under) + svg[head_at:]
    svg = svg[: svg.rindex("</g>")] + "".join(over) + "</g>"
    return svg


RENDER_JS = """
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [html, png] of JSON.parse(process.argv[1])) {
    await page.goto('file://' + html);
    await page.evaluate(() => document.fonts.ready);
    await page.locator('svg').first().screenshot({ path: png, omitBackground: true });
  }
  await browser.close();
})();
"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = HERE / ".cache" / "family_svg"
    tmp.mkdir(parents=True, exist_ok=True)
    jobs = []
    for who in CAST:
        for expr in dc.EXPRESSIONS:
            body = build(who, expr)
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1300" height="1400" viewBox="-360 -780 720 776">'
                   f'{dc.DEFS}{body}</svg>')
            html = tmp / f"{who}_{expr}.html"
            html.write_text(f"<!doctype html><html><head>{dc.CSS}</head><body>{svg}</body></html>")
            jobs.append([str(html), str(OUT / f"{who}_{expr}.png")])
    subprocess.run(["node", "-e", RENDER_JS, json.dumps(jobs)], check=True)
    print(len(jobs), "characters")
