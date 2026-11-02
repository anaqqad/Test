"""Import ChatGPT-drawn Wojaks (the real meme look) into the pipeline.

    python3 import_gpt.py sheet.png g_yakuza g_camorra g_triad g_sicily
    python3 import_gpt.py one_guy.png g_peaky

The image may hold one character or a sheet of several (any grid, reading order: left to right, then top to
bottom). It may have a transparent or a plain white/light background. Each character is cut out, trimmed and
saved as assets/gpt/<name>.png. render.load_char() prefers assets/gpt/, so "g_yakuza_smug", "g_yakuza_rage", ...
all use the ChatGPT drawing; delete the file to fall back to the vector rig.
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "assets" / "gpt"


def cutout(im):
    """RGBA with the background removed (flood fill from the border through light pixels)."""
    im = im.convert("RGBA")
    a = np.asarray(im)
    if (a[..., 3] < 200).mean() > 0.05:  # already transparent
        return im
    rgb = a[..., :3].astype(int)
    light = (rgb.min(axis=2) > 225) & (rgb.max(axis=2) - rgb.min(axis=2) < 25)
    m = Image.fromarray(np.where(light, 255, 0).astype(np.uint8)).copy()  # floodfill ignores array-backed images
    h, w = light.shape
    seeds = [(x, 0) for x in range(0, w, 8)] + [(x, h - 1) for x in range(0, w, 8)] + \
            [(0, y) for y in range(0, h, 8)] + [(w - 1, y) for y in range(0, h, 8)]
    for s in seeds:
        if m.getpixel(s) == 255:
            ImageDraw.floodfill(m, s, 128)
    bg = np.asarray(m) == 128
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))  # eat the white halo
    im.putalpha(ImageChops.multiply(alpha, im.split()[3]))
    return im


def runs(mask1d, min_len):
    out, start = [], None
    for i, v in enumerate(list(mask1d) + [False]):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_len:
                out.append((start, i))
            start = None
    return out


def split(im, n):
    """Reading-order bounding boxes of the n biggest characters, separated by empty rows/columns."""
    fg = np.asarray(im.split()[3]) > 40
    h, w = fg.shape
    boxes = []
    for y0, y1 in runs(fg.any(axis=1), h // 20):
        band = fg[y0:y1]
        for x0, x1 in runs(band.any(axis=0), w // 30):
            sub = band[:, x0:x1]
            ys = np.where(sub.any(axis=1))[0]
            boxes.append((x0, y0 + ys[0], x1, y0 + ys[-1] + 1, sub.sum()))
    boxes = sorted(boxes, key=lambda b: -b[4])[:n]
    if len(boxes) < n:
        sys.exit(f"found {len(boxes)} characters, expected {n}: leave more white space between them")
    rows = sorted(boxes, key=lambda b: b[1])
    rows_grouped, cur = [], [rows[0]]
    for b in rows[1:]:
        if b[1] < cur[0][3] - (cur[0][3] - cur[0][1]) * 0.4:  # same row if it starts within the first row's box
            cur.append(b)
        else:
            rows_grouped.append(cur)
            cur = [b]
    rows_grouped.append(cur)
    return [b[:4] for r in rows_grouped for b in sorted(r, key=lambda b: b[0])]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, names = sys.argv[1], sys.argv[2:]
    im = cutout(Image.open(src))
    OUT.mkdir(parents=True, exist_ok=True)
    for name, box in zip(names, split(im, len(names))):
        c = im.crop(box)
        c = c.crop(c.getbbox())
        if c.height > 1400:
            c = c.resize((int(c.width * 1400 / c.height), 1400), Image.LANCZOS)
        c.save(OUT / f"{name}.png")
        print(OUT / f"{name}.png", c.size)


if __name__ == "__main__":
    main()
