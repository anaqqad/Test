"""Assets for the 3D document-on-desk shot (doc-desk-3d skill, learned from Hoog's journal-paper shots).

  python tools/doc_desk.py desk <out.jpg> [--w 3840 --h 2400 --seed 2]
      Dark walnut desk: long wavy grain, darker pores, soft sheen. Procedural, no copyrighted texture.
  python tools/doc_desk.py page <scan.png> <out.png> [--width 1700] [--seed 1]
      Turns a document scan into a physical sheet: white-balanced to warm paper, faint fibre, very slight
      edge darkening and a few-pixel uneven edge so it reads as paper, not a flat image.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter, ImageOps


def desk(dst, w, h, seed):
    """Long fine streaks (very anisotropic noise) + a soft figure + board seams, low contrast, dark walnut."""
    rng = np.random.default_rng(seed)
    def streaks(rows, cols, amp):
        n = rng.normal(0, 1, (rows, cols)).astype(np.float32)
        return np.asarray(Image.fromarray(n).resize((w, h), Image.BICUBIC)) * amp
    v = streaks(h // 2, max(4, w // 240), 0.55) + streaks(h // 6, max(4, w // 600), 0.35) + streaks(h // 40, 6, 0.25)
    y = np.linspace(0, 1, h)[:, None]
    fig = np.sin((y * 34 + streaks(10, 3, 1.0) * 0.6) * np.pi) * 0.18      # soft cathedral figure, wavers
    v = v + fig
    v = (v - v.mean()) / (v.std() + 1e-6)
    board = np.floor(y * 4.0) % 2 * 0.25 - 0.12
    t = np.clip(0.5 + 0.16 * v + board * 0.3, 0, 1)
    base = np.array([34, 22, 15], np.float32); hi = np.array([92, 62, 40], np.float32)
    img = base + (hi - base) * t[..., None]
    seam = (np.abs((y * 4.0) % 1) < 0.0012)
    img[np.broadcast_to(seam, (h, w))] *= 0.4
    sheen = np.exp(-((np.linspace(-1, 1, w)[None, :] - 0.25) ** 2) / 0.35) * 10
    img += sheen[..., None]
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(dst, quality=92)
    print("desk", dst, (w, h))


def page(src, dst, width, seed):
    im = Image.open(src).convert("L")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=0.5)
    a = np.asarray(im, np.float32) / 255
    rng = np.random.default_rng(seed)
    paper = np.array([246, 243, 235], np.float32); ink = np.array([28, 26, 30], np.float32)
    rgb = ink + (paper - ink) * a[..., None]
    fib = np.asarray(Image.fromarray(rng.normal(0, 1, (im.height // 3, im.width // 3)).astype(np.float32)).resize(im.size, Image.BICUBIC))
    rgb += fib[..., None] * 2.5
    hh, ww = a.shape
    yy, xx = np.mgrid[0:hh, 0:ww]
    edge = np.minimum.reduce([xx, yy, ww - 1 - xx, hh - 1 - yy]).astype(np.float32)
    rgb *= (0.93 + 0.07 * np.clip(edge / 40, 0, 1))[..., None]
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", out.size, 0)
    jit = rng.normal(0, 1.2, 4)
    m.paste(255, (int(2 + abs(jit[0])), int(2 + abs(jit[1])), out.width - int(2 + abs(jit[2])), out.height - int(2 + abs(jit[3]))))
    out.putalpha(m.filter(ImageFilter.GaussianBlur(0.8)))
    out.save(dst)
    print("page", dst, out.size)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["desk", "page"]); ap.add_argument("paths", nargs="+")
    ap.add_argument("--w", type=int, default=3840); ap.add_argument("--h", type=int, default=2400)
    ap.add_argument("--width", type=int, default=1700); ap.add_argument("--seed", type=int, default=2)
    a = ap.parse_args()
    if a.mode == "desk":
        desk(a.paths[0], a.w, a.h, a.seed)
    else:
        page(a.paths[0], a.paths[1], a.width, a.seed)
