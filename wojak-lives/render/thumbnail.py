"""Makes a reference-style YouTube cover: one big character, centred, on a real street photo, no text.

    python3 wojak-lives/render/thumbnail.py CHARACTER BACKGROUND OUT.png [--y 0.18] [--scale 1.9]
    e.g. python3 wojak-lives/render/thumbnail.py girl_tired bg169/small_store.jpg out/cover.png
"""
import argparse
import pathlib

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
W, H = 1280, 720

ap = argparse.ArgumentParser()
ap.add_argument("char")
ap.add_argument("bg")
ap.add_argument("out")
ap.add_argument("--y", type=float, default=0.10, help="top of the character as a fraction of the height")
ap.add_argument("--scale", type=float, default=1.55, help="character height / cover height")
ap.add_argument("--dx", type=float, default=0.0, help="horizontal nudge as a fraction of the width")
a = ap.parse_args()

bg = Image.open(HERE / "assets" / a.bg).convert("RGB")
bg = ImageOps.fit(bg, (W, H), Image.LANCZOS)
bg = ImageEnhance.Color(bg).enhance(0.85).filter(ImageFilter.GaussianBlur(1.2))
ch = Image.open(HERE / "assets" / "chars" / f"{a.char}.png").convert("RGBA")
ch = ch.crop(ch.getbbox())
th = int(H * a.scale)
ch = ch.resize((int(ch.width * th / ch.height), th), Image.LANCZOS)
bg = bg.convert("RGBA")
bg.alpha_composite(ch, (int(W / 2 - ch.width / 2 + a.dx * W), int(a.y * H)))
bg.convert("RGB").save(HERE / a.out, quality=95)
print(HERE / a.out)
