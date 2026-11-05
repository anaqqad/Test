"""3-photo Facebook collage: tall photo left, two stacked right, small brand tag.
Usage: python collage.py <pd dir> <left> <top right> <bottom right> <out.jpg>"""
import sys
from PIL import Image, ImageDraw, ImageFont

pd, left, top, bottom, out = sys.argv[1:6]
W, H, G = 1500, 1500, 8
LW = int(W * .56)


def fit(n, w, h, fy=.3):
    i = Image.open(f'{pd}/{n}.jpg').convert('RGB')
    W0, H0 = i.size
    i = i.crop((int(.04 * W0), int(.05 * H0), int(.97 * W0), int(.93 * H0)))  # drop LOC borders
    iw, ih = i.size
    r = w / h
    if iw / ih > r:
        nw = int(ih * r)
        l = (iw - nw) // 2
        i = i.crop((l, 0, l + nw, ih))
    else:
        nh = int(iw / r)
        t = int((ih - nh) * fy)
        i = i.crop((0, t, iw, t + nh))
    return i.resize((w, h), Image.LANCZOS)


c = Image.new('RGB', (W, H), 'white')
c.paste(fit(left, LW, H, .1), (0, 0))
rw = W - LW - G
rh = (H - G) // 2
c.paste(fit(top, rw, rh, .5), (LW + G, 0))
c.paste(fit(bottom, rw, H - rh - G, .6), (LW + G, rh + G))
d = ImageDraw.Draw(c, 'RGBA')
f = ImageFont.truetype('C:/Windows/Fonts/georgiab.ttf', 30)
t = 'The Black History Room'
b = d.textbbox((0, 0), t, font=f)
tw, th = b[2] - b[0], b[3] - b[1]
x, y = W - tw - 28, H - th - 30
d.rectangle((x - 14, y - 12, x + tw + 14, y + th + 18), fill=(0, 0, 0, 150))
d.text((x, y - b[1]), t, font=f, fill=(255, 255, 255, 235))
c.save(out, quality=92)
print(out, c.size)
