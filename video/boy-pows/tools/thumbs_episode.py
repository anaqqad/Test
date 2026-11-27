"""Thumbnail in Captive Witness's layout on a real photo (no AI): a crying 15-year-old German POW (John Florea, 1945,
public domain per Commons), dark left panel, huge yellow "MY GRAVE?", small line, one red arrow.
python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "thumbnail"
W, H = 1280, 720
YELLOW = (255, 196, 20)
RED = (226, 30, 30)


def font(name, size):
    return ImageFont.truetype(str(T / f"BarlowCondensed-{name}.ttf"), size)


def cover(im, w, h, focus=(0.5, 0.5)):
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = round((im.width - w) * focus[0]); y = round((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


def bw(im, contrast=1.2):
    return ImageEnhance.Contrast(ImageOps.grayscale(im).convert("RGB")).enhance(contrast)


def arrow(d, p0, p1, width=20, head=58):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    base = (p1[0] - head * 0.85 * math.cos(ang), p1[1] - head * 0.85 * math.sin(ang))
    left = (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45))
    right = (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))
    d.line([p0, base], fill=(0, 0, 0), width=width + 8); d.polygon([p1, left, right], fill=(0, 0, 0))
    d.line([p0, base], fill=RED, width=width)
    s = lambda q: (q[0] + (base[0] - q[0]) * 0.14, q[1] + (base[1] - q[1]) * 0.14)
    d.polygon([(p1[0] - 6 * math.cos(ang), p1[1] - 6 * math.sin(ang)), s(left), s(right)], fill=RED)


def main():
    boy = Image.open(ROOT / "assets/stills/boy_pow_crying.jpg").convert("RGB")
    img = ImageEnhance.Brightness(bw(cover(boy, W, H, (0.5, 0.3)), 1.0).filter(ImageFilter.GaussianBlur(18))).enhance(0.35)
    p = bw(cover(boy, 760, H, (0.55, 0.25)))
    ramp = Image.new("L", (760, H))
    ramp.putdata([min(255, int(x / 160 * 255)) for y in range(H) for x in range(760)])  # soft left edge
    img.paste(p, (W - 760, 0), ramp)
    d = ImageDraw.Draw(img)
    f = font("Black", 200)
    for i, line in enumerate(["MY", "GRAVE?"]):
        d.text((40, 90 + i * 190), line, font=f, fill=YELLOW, stroke_width=12, stroke_fill=(0, 0, 0))
    d.text((46, 520), "15 YEARS OLD · POW IN MAINE", font=font("Bold", 54), fill=(255, 255, 255), stroke_width=5, stroke_fill=(0, 0, 0))
    arrow(d, (560, 330), (770, 330))
    img.save(T / "thumbnail_A.jpg", quality=92)
    print("thumbnail/thumbnail_A.jpg")


main()
