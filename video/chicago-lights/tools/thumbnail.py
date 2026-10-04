"""YouTube thumbnail (1280x720) in the channel's thumbnail format: one archive photo, a big caps
question, a red grease-pencil arrow at the detail that answers it, a small caps tag line.
Base photo: Jack Delano, Chicago at night, May 1943 (LoC LC-USW36-606, public domain).
Usage: python3 tools/thumbnail.py   (needs thumbnail/freight_master.tif and Barlow Condensed TTFs)"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "thumbnail"
RED = (224, 68, 46)
W, H = 1280, 720

def base():
    im = Image.open(T / "freight_master.tif").convert("RGB")
    # crop to 16:9 inside the scan border, centred on the lit towers and the street lamps
    w = im.width * 0.90; h = w * 9 / 16
    x0 = im.width * 0.05; y0 = im.height * 0.12
    im = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114])
    gray = np.repeat(lum[..., None], 3, 2)
    # keep colour only in the lights, warm them; everything else black-and-white
    m = np.clip((lum - 0.16) / 0.18, 0, 1)[..., None]
    warm = np.clip(np.repeat(lum[..., None], 3, 2) * np.array([1.55, 1.2, 0.62]) * 1.5, 0, 1)
    out = gray * (1 - m) + warm * m
    out = np.clip((out - 0.02) * 1.4, 0, 1) ** 0.75  # lift the dark city a little
    img = Image.fromarray((out * 255).astype(np.uint8))
    glow = img.filter(ImageFilter.GaussianBlur(14))
    img = Image.blend(img, Image.fromarray(np.maximum(np.asarray(img), np.asarray(glow))), 0.6)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = 1 - 0.45 * (((xx - W * 0.6) / W) ** 2 + ((yy - H * 0.5) / H) ** 2) * 2.2
    return Image.fromarray((np.asarray(img) * np.clip(v, 0.35, 1)[..., None]).astype(np.uint8))

def text(d, xy, s, size, font="Black", stroke=9, fill=(255, 255, 255), anchor="la"):
    f = ImageFont.truetype(str(T / f"BarlowCondensed-{font}.ttf"), size)
    x, y = xy
    d.text((x + 5, y + 7), s, font=f, fill=(0, 0, 0), stroke_width=stroke, stroke_fill=(0, 0, 0), anchor=anchor)
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0), anchor=anchor)

def arrow(img, pts, width=15):
    """Hand-drawn curved arrow (quadratic Bezier) ending in an open head; black outline under red."""
    (x0, y0), (cx, cy), (x1, y1) = pts
    path = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1)
            for t in np.linspace(0, 1, 60)]
    ang = math.atan2(y1 - path[-6][1], x1 - path[-6][0])
    head = [(x1 + 46 * math.cos(ang + s * 2.6), y1 + 46 * math.sin(ang + s * 2.6)) for s in (-1, 1)]
    d = ImageDraw.Draw(img)
    for col, w in (((0, 0, 0), width + 8), (RED, width)):
        d.line(path, fill=col, width=w, joint="curve")
        for h in head:
            d.line([h, (x1, y1)], fill=col, width=w)
        for p in [path[0], path[-1], *head]:
            d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)

def tag(d, xy, s, size=40):
    """House slug: black tab with a red square."""
    f = ImageFont.truetype(str(T / "BarlowCondensed-Bold.ttf"), size)
    x, y = xy
    tw = d.textlength(s, font=f)
    d.rectangle([x, y, x + tw + 62, y + size + 18], fill=(11, 11, 11))
    d.rectangle([x + 16, y + (size + 18) / 2 - 8, x + 32, y + (size + 18) / 2 + 8], fill=RED)
    d.text((x + 44, y + 7), s, font=f, fill=(236, 233, 225))

def make(name, line1, line2, small, arrow_pts):
    img = base()
    d = ImageDraw.Draw(img)
    text(d, (52, 34), line1, 150)
    if line2:
        text(d, (52, 176), line2, 150)
    arrow(img, arrow_pts)
    tag(ImageDraw.Draw(img), (52, H - 98), small)
    img.save(T / f"{name}.jpg", quality=92)
    img.save(T / f"{name}.png")
    print("wrote", T / f"{name}.jpg")

if __name__ == "__main__":
    # A: the question the title raises
    make("thumbnail_A", "NO", "BLACKOUT?", "ESCAPED POW · CHICAGO 1945", [(700, 120), (980, 90), (1075, 255)])
    # B: what he wrote in his memoir
    make("thumbnail_B", "A MILLION", "LIGHTS?!", "HE ESCAPED TO SEE THIS", [(720, 120), (985, 90), (1075, 255)])
