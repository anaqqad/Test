"""Thumbnail for the Missouri episode, copied exactly from the reference series' layout (owner, 23 Nov 2026):
photo on the left fading into a black panel, a two-word question in big white caps, a small yellow place-and-date
line, and ONE straight thick red arrow to the face. Real archive photo (no AI).
python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "thumbnail"
W, H = 1280, 720
YELLOW = (255, 206, 38)
RED = (226, 30, 30)
DARK = 15


def font(name, size):
    return ImageFont.truetype(str(T / f"BarlowCondensed-{name}.ttf"), size)


def straight_arrow(img, p0, p1, width=22, head=62):
    """Straight red arrow from p0 to p1 (tip), with a black outline like the reference."""
    d = ImageDraw.Draw(img)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    base = (p1[0] - head * 0.85 * math.cos(ang), p1[1] - head * 0.85 * math.sin(ang))
    left = (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45))
    right = (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))
    d.line([p0, base], fill=(0, 0, 0), width=width + 8)
    d.polygon([p1, left, right], fill=(0, 0, 0))
    d.line([p0, base], fill=RED, width=width)
    shrink = lambda q: (q[0] + (base[0] - q[0]) * 0.12, q[1] + (base[1] - q[1]) * 0.12)
    tip = (p1[0] - 5 * math.cos(ang), p1[1] - 5 * math.sin(ang))
    d.polygon([tip, shrink(left), shrink(right)], fill=RED)


def panel_thumb(still, box, name, lines, small, arrow, photo_w=820, size=168, top=205, colour=True):
    im = Image.open(ROOT / "assets/stills" / still).convert("RGB").crop(box)
    r = max(photo_w / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = im.crop(((im.width - photo_w) // 2, 0, (im.width - photo_w) // 2 + photo_w, H))
    if not colour:
        im = im.convert("L").convert("RGB")
    im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=120, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(1.18)
    im = ImageEnhance.Color(im).enhance(1.1)
    a = np.zeros((H, W, 3), np.float32) + DARK
    a[:, :photo_w] = np.asarray(im, np.float32)
    fade = np.clip((photo_w - np.arange(W)) / 120, 0, 1)[None, :, None]
    a = a * fade + DARK * (1 - fade)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    cx = photo_w + (W - photo_w) // 2
    for k, line in enumerate(lines):
        f = font("Black", size)
        while d.textlength(line, font=f) > (W - photo_w) - 30:
            size -= 4; f = font("Black", size)
    for k, line in enumerate(lines):
        d.text((cx, top + k * size * 0.95), line, font=font("Black", size), fill=(255, 255, 255), anchor="ma",
               stroke_width=4, stroke_fill=(0, 0, 0))
    fs = font("Bold", 40)
    d.text((cx, top + len(lines) * size * 0.95 + 18), small, font=fs, fill=YELLOW, anchor="ma",
           stroke_width=3, stroke_fill=(0, 0, 0))
    straight_arrow(img, *arrow)
    img.save(T / f"{name}.jpg", quality=92)
    print("wrote", T / f"{name}.jpg", img.size)


if __name__ == "__main__":
    # Hajime Toyoshima's identification photographs, 9 Apr 1942 (AWM 068530, public domain): the front view.
    im = Image.open(ROOT / "assets/stills/toyoshima_id.jpg"); w, h = im.size
    box = (int(0.03 * w), int(0.05 * h), int(0.53 * w), int(0.05 * h) + int(0.50 * w * 720 / 820))
    panel_thumb("toyoshima_id.jpg", box, "thumbnail_A", ["CHARGE", "THE GUNS?"], "COWRA, AUSTRALIA, 1944",
                ((960, 660), (640, 470)), colour=False)
