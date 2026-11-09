import sys
from pathlib import Path
P = Path(__file__).resolve().parent / "thumbnail.py"
src = P.read_text(encoding="utf-8"); src = src[:src.index('if __name__ == "__main__":')]
g = {"__file__": str(P)}; exec(src, g)
ROOT, T, from_image = g["ROOT"], g["T"], g["from_image"]
from PIL import Image, ImageEnhance
im = Image.open(ROOT / "assets/stills/jefferson_2013.jpg").convert("RGB").crop((400, 0, 1920, 855))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.3)).enhance(0.74).save(T / "jeff_base.jpg", quality=95)
from_image(T / "jeff_base.jpg", "thumbnail_A", "MY SCHOOL", "GRADES?!", "TUSKEGEE AIRMAN · GERMAN POW 1944", [(700, 330), (640, 230), (590, 140)], text_x=720, size=118)
im = Image.open(ROOT / "assets/stills/pilots_frissell.jpg").convert("RGB").crop((0, 150, 1920, 1230))
ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.2)).enhance(0.82).save(T / "pilots_base.jpg", quality=95)
from_image(T / "pilots_base.jpg", "thumbnail_B", "THEY HAD", "MY FILE?!", "332ND FIGHTER GROUP · ITALY 1945", [(600, 250), (480, 200), (330, 160)], text_x=690, size=118)
