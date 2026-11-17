"""Thumbnails for this episode: python tools/thumbs_episode.py -> thumbnail/thumbnail_A.jpg, thumbnail_B.jpg"""
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image, W, H = g["ROOT"], g["T"], g["from_image"], g["W"], g["H"]
import numpy as np
from PIL import Image, ImageEnhance


def right_portrait(src, out, crop, x0=560):
    """Portrait on the right half over a dark left side that fades into it, leaving room for the question."""
    im = Image.open(ROOT / "assets/stills" / src).convert("RGB").crop(crop)
    im = im.resize((round(im.width * H / im.height), H), Image.LANCZOS)
    im = ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.15)).enhance(0.78)
    canvas = np.zeros((H, W, 3), np.float32) + 14
    a = np.asarray(im).astype(np.float32)[:, : W - x0]
    canvas[:, x0:x0 + a.shape[1]] = a
    ramp = np.clip((np.arange(W) - x0) / 220, 0, 1)[None, :, None]
    Image.fromarray(np.clip(canvas * ramp + 14 * (1 - ramp), 0, 255).astype(np.uint8)).save(out, quality=95)


# A: Maj. William Edwin "Ed" Dyess after his return, 1943 (U.S. Air Force photo, public domain)
right_portrait("dyess_portrait.jpg", T / "dyess_base.jpg", (40, 80, 1280, 1320), x0=560)
from_image(T / "dyess_base.jpg", "thumbnail_A", "ESCAPED...", "THEN SILENCED?", "BATAAN SURVIVOR · 1943", [(620, 560), (720, 450), (800, 370)], text_x=36, size=112)
# B: American prisoners on the Bataan Death March, hands tied behind their backs, May 1942 (NARA 127-N-114541, public domain)
right_portrait("bataan_prisoners.jpg", T / "bataan_base.jpg", (0, 0, 330, 396), x0=680)
from_image(T / "bataan_base.jpg", "thumbnail_B", "10 ESCAPED.", "WHY HIDE IT?", "BATAAN · 1942", [(560, 560), (700, 470), (820, 400)], text_x=36, size=112)
