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

# ---- v2: split frame, so the thumbnail reads as WWII at a glance ----
# Left: German soldiers surrendering, 1944 (LoC LOT 8754, "Fifty-six German prisoners of war come out
# with their hands in the air", public domain). Right: Chicago at night, 1943. Red grease-pencil divider.

def surrender_panel(w, h):
    im = Image.open(T / "surrender_master.tif").convert("L")
    s = im.width / 1024  # crop chosen on the 1024 px preview
    x0, y0, y1 = 70 * s, 255 * s, 700 * s  # the surrendering soldiers, hands up
    hh = y1 - y0; ww = hh * w / h
    im = im.crop((int(x0), int(y0), int(x0 + ww), int(y1))).resize((w, h), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    a = np.clip((a - 0.08) * 1.25, 0, 1) ** 1.15
    return Image.fromarray((a * 255).astype(np.uint8)).convert("RGB")

def make_split(name, line1, line2, left_tag, right_tag, arrow_pts):
    img = base()
    left = surrender_panel(640, H)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (650, 0), (590, H), (0, H)], fill=255)
    canvas = img.copy()
    canvas.paste(left, (0, 0))
    img = Image.composite(canvas, img, mask)
    d = ImageDraw.Draw(img)
    for col, w in (((0, 0, 0), 22), (RED, 12)):
        d.line([(652, -10), (590, H + 10)], fill=col, width=w)
    text(d, (690, 22), line1, 118)
    text(d, (690, 132), line2, 118)
    arrow(img, arrow_pts)
    d = ImageDraw.Draw(img)
    tag(d, (40, H - 92), left_tag, 38)
    tag(d, (700, H - 92), right_tag, 38)
    img.save(T / f"{name}.jpg", quality=92)
    print("wrote", T / f"{name}.jpg")


def from_image(src, name, line1, line2, small, arrow_pts, text_x=None, size=None):
    """Thumbnail from a generated/supplied image (e.g. made in ChatGPT): fit to 1280x720, B&W except the
    warm lights, caps question on the window side, red grease arrow, house tag."""
    im = Image.open(src).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
    a = np.asarray(im).astype(np.float32) / 255
    lum = a @ np.array([0.299, 0.587, 0.114])
    m = np.clip((lum - 0.78) / 0.15, 0, 1)[..., None]  # only the brightest lights keep a warm tint
    warm = np.clip(np.repeat(lum[..., None], 3, 2) * np.array([1.25, 1.05, 0.7]), 0, 1)
    out = np.repeat(lum[..., None], 3, 2) * (1 - m) + warm * m
    img = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    x = text_x if text_x is not None else 700
    size = size or (128 if max(len(line1), len(line2)) <= 9 else 108)
    text(d, (x, 26), line1, size)
    text(d, (x, 26 + size * 0.94), line2, size)
    arrow(img, arrow_pts)
    tag(ImageDraw.Draw(img), (52, H - 98), small)
    img.save(T / f"{name}.jpg", quality=92)
    print("wrote", T / f"{name}.jpg")


def shifted_base(src, out, dx=200):
    """Frame moved right by dx px over a dark gradient, leaving room for text on the left."""
    im = Image.open(src).convert("RGB").resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    canvas = np.zeros_like(a) + 18
    canvas[:, dx:] = a[:, :W - dx]
    ramp = np.clip((np.arange(W) - dx) / 260, 0, 1)[None, :, None]  # the frame's left edge fades into the dark
    Image.fromarray(np.clip(canvas * ramp + 18 * (1 - ramp), 0, 255).astype(np.uint8)).save(out, quality=95)


if __name__ == "__main__":
    from PIL import ImageFilter, ImageEnhance
    # A: the guard tower at Camp Salina today (CC BY 2.0)
    im = Image.open(ROOT / "assets/stills/camp_salina_site.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((300, int(h * 0.12), 300 + int(h * 0.80 * 16 / 9), int(h * 0.92)))
    a = np.asarray(ImageEnhance.Contrast(im.convert("L").convert("RGB")).enhance(1.35)).astype(np.float32)
    vramp = np.clip(np.linspace(0.55, 1.0, a.shape[0]), 0, 1.0)[:, None, None]
    hramp = np.clip(np.linspace(0.45, 1.05, a.shape[1]), 0, 1.0)[None, :, None]
    Image.fromarray(np.clip(a * vramp * hramp, 0, 255).astype(np.uint8)).save(T / "tower_base.jpg", quality=95)
    from_image(T / "tower_base.jpg", "thumbnail_B", "THE WAR", "WAS OVER.", "GERMAN POWS · UTAH, JULY 1945", [(640, 540), (740, 500), (835, 430)], text_x=50, size=132)
    # B: the Salina Sun, July 13, 1945 (Utah Digital Newspapers, no copyright)
    im = Image.open(ROOT / "assets/stills/salina_sun_1945.jpg").convert("RGB")
    w, h = im.size
    im = im.crop((0, int(h * 0.0), w, int(w * 9 / 16)))
    a = np.asarray(im).astype(np.float32)
    Image.fromarray(np.clip(a * 0.92, 0, 255).astype(np.uint8)).save(T / "sun_base.jpg", quality=95)
    from_image(T / "sun_base.jpg", "thumbnail_A", "TWO MONTHS", "AFTER V-E DAY", "GERMAN POWS · UTAH, JULY 1945", [(300, 560), (420, 470), (520, 360)], text_x=40, size=110)
