"""Thumbnail in Captive Witness's layout (owner, 25 Nov 2026: "what works for this channel are the thumbnails"):
B&W split image, a huge yellow condensed question in caps top-left, one red arrow. Real archive images only (no AI):
left German POWs landing in the U.S. (Army Service Forces photo, insignia blurred), right a decorated Black veteran
from 'The Negro Soldier' (U.S. War Department, 1944). python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg"""
from pathlib import Path
import math, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

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


def bw(im, contrast=1.25):
    im = ImageOps.grayscale(im).convert("RGB")
    return ImageEnhance.Contrast(im).enhance(contrast)


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
    pows = Image.open(ROOT / "assets/stills/pows_debarking_b.jpg").convert("RGB").crop((330, 330, 1420, 1300))
    vet_png = ROOT / "build/vet.png"
    if not vet_png.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "assets/footage/negro_soldier_1944.mp4"), "-ss", "744",
                        "-frames:v", "1", str(vet_png)], check=True)
    vet = Image.open(vet_png).convert("RGB")
    img = Image.new("RGB", (W, H))
    img.paste(bw(cover(pows, 700, H, (0.5, 0.25))), (0, 0))
    img.paste(bw(cover(vet, 576, H, (0.5, 0.2)), 1.15), (704, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([700, 0, 704, H], fill=(0, 0, 0))
    f = font("Black", 172)
    for i, line in enumerate(["THE", "KITCHEN?"]):
        x, y = 34, 18 + i * 150
        d.text((x, y), line, font=f, fill=YELLOW, stroke_width=10, stroke_fill=(0, 0, 0))
    arrow(d, (560, 470), (690, 560))
    img.save(T / "thumbnail_A.jpg", quality=92)
    print("thumbnail/thumbnail_A.jpg")


main()
