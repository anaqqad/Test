"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg
Layout adapted from the reference channel's current series (photo on the left, dark panel on the right with a two-word
question and a yellow place-and-date line, a big red arrow to the face), drawn in our own house type, arrow and red tag."""
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, W, H, text, arrow, RED = g["ROOT"], g["T"], g["W"], g["H"], g["text"], g["arrow"], g["RED"]
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

YELLOW = (255, 206, 38)
DARK = 15


def panel_thumb(still, box, name, lines, small, arrow_pts, photo_w=800, size=150, top=150):
    """box: (x0, y0, x1, y1) of the still to show; it is scaled to fill photo_w x 720 on the left."""
    im = Image.open(ROOT / "assets/stills" / still).convert("L").crop(box)
    r = max(photo_w / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im = im.crop(((im.width - photo_w) // 2, 0, (im.width - photo_w) // 2 + photo_w, H))
    im = ImageEnhance.Contrast(im).enhance(1.25)
    a = np.zeros((H, W, 3), np.float32) + DARK
    a[:, :photo_w] = np.repeat(np.asarray(im, np.float32)[..., None], 3, 2)
    fade = np.clip((photo_w - np.arange(W)) / 140, 0, 1)[None, :, None]  # the photo's right edge fades into the panel
    a = a * fade + DARK * (1 - fade)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    cx = photo_w + (W - photo_w) // 2 - 10
    for k, line in enumerate(lines):
        text(d, (cx, top + k * size * 0.92), line, size, anchor="ma")
    f = ImageFont.truetype(str(T / "BarlowCondensed-Bold.ttf"), 50)
    y = top + len(lines) * size * 0.92 + 26
    tw = d.textlength(small, font=f)
    x0 = cx - (tw + 34) / 2
    d.rectangle([x0, y + 17, x0 + 18, y + 35], fill=RED)
    d.text((x0 + 34, y), small, font=f, fill=YELLOW, stroke_width=4, stroke_fill=(0, 0, 0))
    arrow(img, arrow_pts, width=18)
    img.save(T / f"{name}.jpg", quality=92)
    print("wrote", T / f"{name}.jpg")


if __name__ == "__main__":
    # Gen. Masaharu Homma on the stand in his own defense, Manila, 6 Feb 1946 (Signal Corps album 111-SCA-2919, public domain)
    panel_thumb("homma_stand_c.jpg", (350, 250, 1750, 1510), "thumbnail_A", ["HIS", "FAULT?"], "MANILA, FEB 1946",
                [(880, 600), (680, 520), (450, 300)])
