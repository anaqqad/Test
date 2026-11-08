"""High-CTR YouTube covers (1280x720): big sticker-outlined characters, emotion/conflict, a 1-3 word yellow tag.

    python3 wojak-lives/render/cover.py            # every cover in COVERS
    python3 wojak-lives/render/cover.py german     # only covers whose key starts with "german"

Rules: faces fill ~60 % of the height, white sticker outline + shadow, darker/softer background so the
characters pop, max 3 words of text (never repeating the title), conflict = kid on the left, parent on the right.
Output: render/out/covers/<key>.png
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render  # noqa: E402  (font + tag_image + character loader)

W, H = 1280, 720
OUT = HERE / "out" / "covers"


def char_img(name):
    im = render.load_char(name)
    return im.crop(im.getbbox())


def sticker(im, border=12):
    """White sticker outline + soft shadow around a cut-out."""
    a = im.split()[3]
    grow = a.filter(ImageFilter.MaxFilter(border * 2 + 1))
    out = Image.new("RGBA", (im.width + 40, im.height + 40), (0, 0, 0, 0))
    shadow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (26, 30), grow)
    out.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    out.paste(white, (20, 20), grow)
    out.alpha_composite(im, (20, 20))
    return out


def place(canvas, name, x, top, height, flip=False):
    im = char_img(name)
    if flip:
        im = ImageOps.mirror(im)
    im = im.resize((int(im.width * height / im.height), int(height)), Image.LANCZOS)
    st = sticker(im)
    canvas.alpha_composite(st, (int(x * W - st.width / 2), int(top * H) - 20))


def cover(key, bg, chars, text=None, text_pos=(0.5, 0.14), text_size=96, rot=-4):
    render.W, render.H = W, H
    base = Image.open(HERE / "assets" / bg).convert("RGB")
    base = ImageOps.fit(base, (W, H), Image.LANCZOS)
    base = ImageEnhance.Brightness(ImageEnhance.Color(base).enhance(1.15)).enhance(0.72)
    base = base.filter(ImageFilter.GaussianBlur(4)).convert("RGBA")
    vign = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vign).ellipse((-W * 0.2, -H * 0.3, W * 1.2, H * 1.3), fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(120))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 170))
    base = Image.composite(base, Image.alpha_composite(base, dark), vign)
    for c in chars:
        place(base, **c)
    if text:
        tag = render.tag_image(text, text_size, rot)
        x = min(max(int(text_pos[0] * W - tag.width / 2), 16), W - tag.width - 16)
        base.alpha_composite(tag, (x, int(text_pos[1] * H - tag.height / 2)))
    OUT.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT / f"{key}.png", quality=95)
    print(OUT / f"{key}.png")


def duo(kid, parent):  # kid left facing right, parent right facing left, faces large
    return [dict(name=kid, x=0.3, top=0.26, height=H * 1.05),
            dict(name=parent, x=0.72, top=0.2, height=H * 1.12, flip=True)]


def row(*names):  # list videos: a line-up of characters
    n = len(names)
    return [dict(name=nm, x=0.08 + 0.84 * (i + 0.5) / n, top=0.3 + 0.04 * (i % 2), height=H * (0.82 if n <= 3 else 0.72),
                 flip=i >= n / 2)
            for i, nm in enumerate(names)]


def solo(name, x=0.5):
    return [dict(name=name, x=x, top=0.24, height=H * 1.15)]


def cover_list(key, bg, char, header, flag_code, lines):
    """Reference list-channel look (LingoDude-style): white header band with the entry name + flag, a big
    ChatGPT Wojak bottom-left on a sharp photo, huge red words with a white outline on the right."""
    import listvid
    render.W, render.H = W, H
    band = int(H * 0.16)
    base = Image.new("RGBA", (W, H), "white")
    ph = ImageOps.fit(Image.open(HERE / "assets" / bg).convert("RGB"), (W, H - band), Image.LANCZOS)
    base.paste(ImageEnhance.Color(ph).enhance(1.15), (0, band))
    d = ImageDraw.Draw(base)
    fh = render.font("baloo", int(band * 0.62))
    fl = listvid.flag(flag_code, int(band * 0.78)).convert("RGBA") if flag_code else None
    tw = d.textlength(header, font=fh) + (fl.width + 24 if fl else 0)
    x = (W - tw) / 2
    d.text((x, band * 0.12), header, font=fh, fill=(0, 0, 0))
    if fl:
        base.alpha_composite(fl, (int(x + d.textlength(header, font=fh) + 24), (band - fl.height) // 2))
    im = char_img(char)
    hgt = (H - band) * 1.02
    im = im.resize((int(im.width * hgt / im.height), int(hgt)), Image.LANCZOS)
    if im.width > W * 0.52:
        im = im.resize((int(W * 0.52), int(im.height * W * 0.52 / im.width)), Image.LANCZOS)
    base.alpha_composite(im, (-int(im.width * 0.04), H - im.height))
    fr = render.font("lilita", 10)
    size = min(int(H * 0.26), *(int(10 * W * 0.44 / max(1, d.textlength(l, font=fr))) for l in lines))
    fr = render.font("lilita", size)
    total = len(lines) * size * 1.08
    y = band + (H - band - total) / 2
    cx = W * 0.73
    for l in lines:
        lw = d.textlength(l, font=fr)
        d.text((cx - lw / 2 + 6, y + 8), l, font=fr, fill=(0, 0, 0, 120), stroke_width=int(size * 0.09),
               stroke_fill=(0, 0, 0, 120))
        d.text((cx - lw / 2, y), l, font=fr, fill=(232, 32, 42), stroke_width=int(size * 0.09),
               stroke_fill="white")
        y += size * 1.08
    OUT.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT / f"{key}.png", quality=95)
    print(OUT / f"{key}.png")


LIST_COVERS = {
    "languages_A": ("list/bg/lang_island.jpg", "l_sentinel", "Sentinelese", "in", ["NOBODY", "KNOWS IT"]),
    "languages_B": ("list/bg/lang_iran.jpg", "l_kusunda", "Sumerian", "iq", ["NO", "RELATIVES"]),
    "nnn_A": ("list/bg/nnn_night.jpg", "n_doomer", "NNN: Day 25", None, ["SEND", "HELP"]),
    "nnn_B": ("list/bg/nnn_bathroom.jpg", "n_cold", "NNN: Day 9", None, ["3 COLD", "SHOWERS"]),
    "last_speakers_A": ("list/bg/ls_amazon.jpg", "s_taushiro", "Taushiro", "pe", ["1 SPEAKER", "LEFT"]),
    "last_speakers_B": ("list/bg/ls_tabasco.jpg", "s_ayapaneco", "Ayapaneco", "mx", ["THEY DON'T", "TALK"]),
}

B = "bg169/"
COVERS = {
    # key: (background, characters, tag text)
    "muslim_girl_A": (B + "wedding_hall.jpg", duo("girl_sad", "aunty_red_happy"), "WHEN'S YOUR TURN?"),
    "muslim_girl_B": (B + "small_store.jpg", solo("girl_cry"), "18 RULES"),
    "mexican_mom_A": (B + "us_kitchen2.jpg", duo("mxkid_crying", "mxmom_chancla_smug"), "SHE NEVER MISSES"),
    "mexican_mom_B": (B + "us_kitchen2.jpg", solo("mxmom_chancla_rage"), "THE CHANCLA"),
    "asian_parents_A": (B + "us_living_tv.jpg", duo("askid_report_crying", "asdad_side-eye"), "98%?!"),
    "asian_parents_B": (B + "us_living_tv.jpg", solo("asdad_report_rage", 0.55), "B+ = F"),
    "oldest_daughter_A": (B + "us_living.jpg", duo("oldsis_crying", "omom_smug"), "YOU'RE THE OLDEST"),
    "oldest_daughter_B": (B + "us_living.jpg", solo("oldsis_crying"), "UNPAID SINCE BIRTH"),
    "immigrant_parents_A": (B + "us_kitchen.jpg", duo("ikid_crying", "mxmom_side-eye"), "DID YOU EAT?"),
    "immigrant_parents_B": (B + "us_porch.jpg", duo("ikid_side-eye", "asdad_side-eye"), "CANDY: DENIED"),
    "german_mom_A": (B + "us_kitchen2.jpg", duo("dekid_crying", "demom_point_smug"), "6:01 = LATE"),
    "german_mom_B": (B + "us_living.jpg", solo("demom_rage"), "NO ICE."),
    "southern_mom_A": (B + "us_porch.jpg", duo("sokid_crying", "somom_spoon_smug"), "BLESS YOUR HEART"),
    "southern_mom_B": (B + "us_porch.jpg", solo("somom_spoon_rage"), "FULL NAME = RUN"),
    "every_mom_A": (B + "us_porch.jpg", row("somom_smug", "mxmom_chancla_smug", "krmom_smug",
                                            "ukmom_smug"), "WHICH ONE IS YOURS?"),
    "every_mom_B": (B + "us_kitchen2.jpg", row("mxmom_chancla_rage", "itmom_spoon_smug", "somom_spoon_rage"),
                    "EVERY TYPE OF MOM"),
    "midwest_mom_A": (B + "us_porch.jpg", duo("mwkid_crying", "mwmom_bloomer"), "45 MIN GOODBYE"),
    "midwest_mom_B": (B + "us_living.jpg", solo("mwmom_side-eye"), "\"THAT'S DIFFERENT\""),
    "gangs_A": ("list/bg/nyc.jpg", row("g_sicily_smug", "g_yakuza_side-eye", "g_peaky_smug", "g_hells_rage"),
                "WHO RUNS THE STREETS?"),
    "gangs_B": ("list/bg/la2.jpg", row("g_crips_side-eye", "g_usmafia_smug", "g_bloods_side-eye"),
                "MOST NOTORIOUS"),
}

if __name__ == "__main__":
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    for key, (bg, chars, text) in COVERS.items():
        if key.startswith(want):
            cover(key, bg, chars, text)
    for key, args in LIST_COVERS.items():
        if key.startswith(want):
            cover_list(key, *args)
