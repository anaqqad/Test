"""Ranked-list Wojak videos ("Every ___", "#1 … #N"): the format learned from the two reference clips.

    python3 wojak-lives/render/listvid.py wojak-lives/render/episodes/list_every_mom.py
    python3 wojak-lives/render/listvid.py LIST.py --still 3          # PNG of entry 3 with all cards shown

Measured from the references and reproduced here:
- 1920x1080, 30 fps, one entry every 7-8.5 s, hard cuts, no intro, no outro, no voice.
- Static, sharp real photo as the background; black title bar (11 % high): yellow "#N", the name in bold,
  details in brackets in a lighter colour, the flag on the right.
- A big Wojak bust bottom-left that sways gently (about +/-1.2 deg, 3.6 s period).
- Top-right: the photo in a black frame, tilted, with a red rubber-stamp verdict.
- Three white fact cards (black border, hard shadow, slight tilt) pop in at 5 %, 35 % and 64 % of the entry.
- Each entry has its own music piece, with a small "♫ track" credit bottom-right.
Entry keys: name, detail, flag, char, bg, photo, stamp, facts[3], music{track[, start]} (real Kevin MacLeod track,\nlike the references) or music{style, title} (procedural fallback).
"""
import argparse
import importlib.util
import json
import math
import pathlib
import subprocess
import urllib.parse
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

import render  # fonts, character loader, sfx/ music helpers

HERE = pathlib.Path(__file__).resolve().parent
LIST = HERE / "assets" / "list"
W, H, FPS, SR = 1920, 1080, 30, 44100
BAR = int(H * 0.11)
YELLOW, WHITE, INK, RED = (255, 205, 40), (255, 255, 255), (12, 12, 12), (214, 40, 40)
NOTE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(name, size):
    return render.font(name, size)


# ------------------------------------------------------------------ flags (drawn, 3:2)
def flag(code, w=150):
    h = w * 2 // 3
    S = 4
    im = Image.new("RGB", (w * S, h * S), "white")
    d = ImageDraw.Draw(im)
    W_, H_ = im.size

    def hstripes(cols):
        n = len(cols)
        for i, c in enumerate(cols):
            d.rectangle((0, H_ * i / n, W_, H_ * (i + 1) / n), fill=c)

    def vstripes(cols, weights=None):
        weights = weights or [1] * len(cols)
        x = 0
        for c, wt in zip(cols, weights):
            x2 = x + W_ * wt / sum(weights)
            d.rectangle((x, 0, x2, H_), fill=c)
            x = x2

    def union_jack(x0, y0, x1, y1):
        cw, ch = x1 - x0, y1 - y0
        d.rectangle((x0, y0, x1, y1), fill=(1, 33, 105))
        t = ch * 0.2
        d.line((x0, y0, x1, y1), fill="white", width=int(t))
        d.line((x0, y1, x1, y0), fill="white", width=int(t))
        d.line((x0, y0, x1, y1), fill=(200, 16, 46), width=int(t / 3))
        d.line((x0, y1, x1, y0), fill=(200, 16, 46), width=int(t / 3))
        d.rectangle((x0 + cw / 2 - t * 0.8, y0, x0 + cw / 2 + t * 0.8, y1), fill="white")
        d.rectangle((x0, y0 + ch / 2 - t * 0.8, x1, y0 + ch / 2 + t * 0.8), fill="white")
        d.rectangle((x0 + cw / 2 - t * 0.45, y0, x0 + cw / 2 + t * 0.45, y1), fill=(200, 16, 46))
        d.rectangle((x0, y0 + ch / 2 - t * 0.45, x1, y0 + ch / 2 + t * 0.45), fill=(200, 16, 46))

    if code == "us":
        for i in range(13):
            d.rectangle((0, H_ * i / 13, W_, H_ * (i + 1) / 13), fill=(178, 34, 52) if i % 2 == 0 else "white")
        d.rectangle((0, 0, W_ * 0.4, H_ * 7 / 13), fill=(60, 59, 110))
        for r in range(5):
            for c in range(6):
                x, y = W_ * 0.4 * (c + 0.5) / 6, H_ * 7 / 13 * (r + 0.5) / 5
                d.ellipse((x - 5, y - 5, x + 5, y + 5), fill="white")
    elif code == "mx":
        vstripes([(0, 104, 71), "white", (206, 17, 38)])
        d.ellipse((W_ / 2 - H_ * 0.13, H_ / 2 - H_ * 0.13, W_ / 2 + H_ * 0.13, H_ / 2 + H_ * 0.13), fill=(140, 90, 40))
    elif code == "de":
        hstripes([(0, 0, 0), (221, 0, 0), (255, 206, 0)])
    elif code == "ca":
        vstripes([(216, 6, 33), "white", (216, 6, 33)], [1, 2, 1])
        cx, cy, r = W_ / 2, H_ / 2, H_ * 0.32
        pts = [(0, -1), (.12, -.7), (.32, -.78), (.26, -.45), (.62, -.6), (.52, -.32), (.72, -.2), (.4, .05),
               (.46, .28), (.08, .2), (.06, .65), (-.06, .65), (-.08, .2), (-.46, .28), (-.4, .05), (-.72, -.2),
               (-.52, -.32), (-.62, -.6), (-.26, -.45), (-.32, -.78), (-.12, -.7)]
        d.polygon([(cx + x * r, cy + y * r) for x, y in pts], fill=(216, 6, 33))
    elif code == "gb":
        union_jack(0, 0, W_, H_)
    elif code == "ie":
        vstripes([(22, 155, 98), "white", (255, 136, 62)])
    elif code == "au":
        d.rectangle((0, 0, W_, H_), fill=(1, 33, 105))
        union_jack(0, 0, W_ / 2, H_ / 2)
        for x, y, r in ((.25, .75, 22), (.75, .25, 12), (.65, .5, 12), (.85, .45, 12), (.75, .8, 12), (.8, .62, 7)):
            d.ellipse((W_ * x - r, H_ * y - r, W_ * x + r, H_ * y + r), fill="white")
    elif code == "kr":
        cx, cy, r = W_ / 2, H_ / 2, H_ * 0.25
        d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(205, 46, 58))
        d.pieslice((cx - r, cy - r, cx + r, cy + r), 0, 180, fill=(0, 71, 160))
        for sx, sy in ((-1, -1), (1, 1), (1, -1), (-1, 1)):
            for k in range(3):
                bx, by = cx + sx * W_ * 0.33, cy + sy * H_ * 0.3
                ang = math.atan2(sy, sx * 1.5)
                ox, oy = math.cos(ang) * (k - 1) * 22, math.sin(ang) * (k - 1) * 22
                px, py = -math.sin(ang) * 45, math.cos(ang) * 45
                d.line((bx + ox - px, by + oy - py, bx + ox + px, by + oy + py), fill="black", width=14)
    elif code == "fr":
        vstripes([(0, 85, 164), "white", (239, 65, 53)])
    elif code == "se":
        d.rectangle((0, 0, W_, H_), fill=(0, 106, 167))
        d.rectangle((W_ * 0.31, 0, W_ * 0.44, H_), fill=(254, 204, 0))
        d.rectangle((0, H_ * 0.4, W_, H_ * 0.6), fill=(254, 204, 0))
    elif code == "jp":
        r = H_ * 0.3
        d.ellipse((W_ / 2 - r, H_ / 2 - r, W_ / 2 + r, H_ / 2 + r), fill=(188, 0, 45))
    elif code == "it":
        vstripes([(0, 146, 70), "white", (206, 43, 55)])
    elif code == "cn":
        d.rectangle((0, 0, W_, H_), fill=(222, 41, 16))
        for x, y, r in ((.17, .27, 40), (.33, .12, 13), (.4, .22, 13), (.4, .37, 13), (.33, .47, 13)):
            d.regular_polygon((W_ * x, H_ * y, r), 5, rotation=0, fill=(255, 222, 0))
    elif code == "co":
        d.rectangle((0, 0, W_, H_ / 2), fill=(252, 209, 22))
        d.rectangle((0, H_ / 2, W_, H_ * 3 / 4), fill=(0, 56, 147))
        d.rectangle((0, H_ * 3 / 4, W_, H_), fill=(206, 17, 38))
    elif code == "br":
        d.rectangle((0, 0, W_, H_), fill=(0, 156, 59))
        d.polygon([(W_ * .08, H_ / 2), (W_ / 2, H_ * .1), (W_ * .92, H_ / 2), (W_ / 2, H_ * .9)], fill=(255, 223, 0))
        r = H_ * 0.24
        d.ellipse((W_ / 2 - r, H_ / 2 - r, W_ / 2 + r, H_ / 2 + r), fill=(0, 39, 118))
    elif code == "nl":
        hstripes([(174, 28, 40), "white", (33, 70, 139)])
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (w + 6, h + 6), "white")
    out.paste(im, (3, 3))
    return out


# ------------------------------------------------------------------ static layers
def text_w(t, f):
    b = f.getbbox(t)
    return b[2] - b[0]


def title_bar(n, name, detail, code):
    bar = Image.new("RGBA", (W, BAR), (10, 10, 10, 255))
    d = ImageDraw.Draw(bar)
    fn = font("baloo", int(BAR * 0.52))
    fd = font("baloo", int(BAR * 0.40))
    d.text((int(W * 0.025), BAR * 0.2), f"#{n}", font=fn, fill=YELLOW)
    detail = f" ({detail})" if detail else ""
    tw = text_w(name, fn) + text_w(detail, fd)
    x = (W - tw) // 2
    d.text((x, BAR * 0.2), name, font=fn, fill=WHITE)
    d.text((x + text_w(name, fn) + 6, BAR * 0.29), detail, font=fd, fill=(205, 205, 205))
    if code:
        f = flag(code, int(BAR * 0.92))
        bar.paste(f, (W - f.width - int(W * 0.022), (BAR - f.height) // 2))
    return bar


def stamp(text):
    f = font("lilita", 46)
    tw = text_w(text, f)
    im = Image.new("RGBA", (tw + 44, 78), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((3, 3, tw + 40, 74), fill=(255, 255, 255, 215), outline=RED, width=6)
    d.text((22, 11), text, font=f, fill=RED)
    return im.rotate(8, expand=True, resample=Image.BICUBIC)


def photo_frame(path, verdict):
    w, h = int(W * 0.155), int(H * 0.34)
    ph = ImageOps.fit(Image.open(path).convert("RGB"), (w, h), Image.LANCZOS)
    frame = Image.new("RGBA", (w + 16, h + 16), (12, 12, 12, 255))
    frame.paste(ph, (8, 8))
    st = stamp(verdict)
    canvas = Image.new("RGBA", (frame.width + 140, frame.height + 140), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 120), (70 + 10, 50 + 12, 70 + 10 + frame.width, 50 + 12 + frame.height))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    canvas.alpha_composite(frame, (70, 50))
    canvas = canvas.rotate(-3, expand=False, resample=Image.BICUBIC)
    canvas.alpha_composite(st, (40, 50 + frame.height - st.height // 2 - 10))
    return canvas


def fact_card(text, rot):
    f = font("baloo", int(H * 0.036))
    lines = render.wrap(text, f, int(W * 0.29))
    lh = int(f.size * 1.12)
    tw = max(text_w(l, f) for l in lines)
    w, h = tw + 46, lh * len(lines) + 28
    im = Image.new("RGBA", (w + 14, h + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((9, 9, w + 9, h + 9), fill=(0, 0, 0, 170))
    d.rectangle((0, 0, w, h), fill=WHITE, outline=INK, width=3)
    y = 12
    for l in lines:
        d.text((22, y), l, font=f, fill=INK)
        y += lh
    return im.rotate(rot, expand=True, resample=Image.BICUBIC)


def credit(title, artist="Wojak Lives"):
    fn = ImageFont.truetype(NOTE_FONT, 24)
    ft = font("baloo", 26)
    t = f"{title} — {artist}"
    w = text_w(t, ft) + 64
    im = Image.new("RGBA", (w, 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 43), 10, fill=(0, 0, 0, 150))
    d.text((14, 8), "♫", font=fn, fill=WHITE)
    d.text((44, 5), t, font=ft, fill=WHITE)
    return im


def bg_image(name):
    p = LIST / "bg" / name if (LIST / "bg" / name).exists() else HERE / "assets" / name
    im = ImageOps.fit(Image.open(p).convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.45))
    return ImageEnhance.Color(im).enhance(1.05).convert("RGBA")


def wojak(name, height):
    im = render.load_char(name)
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * height / im.height), int(height)), Image.LANCZOS)


# ------------------------------------------------------------------ music: one piece per entry
SCALES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10], "penta": [0, 2, 4, 7, 9],
          "inscale": [0, 1, 5, 7, 8], "dorian": [0, 2, 3, 5, 7, 9, 10]}
STYLES = {  # scale, tempo, beats per bar, timbre, root
    "bluegrass": ("major", 132, 4, "pluck", 196.0), "waltz": ("major", 150, 3, "music_box", 261.6),
    "mariachi": ("major", 168, 3, "pluck", 220.0), "polka": ("major", 120, 2, "accordion", 233.1),
    "tarantella": ("minor", 160, 3, "pluck", 220.0), "lullaby": ("major", 80, 3, "music_box", 293.7),
    "minuet": ("major", 108, 3, "harpsichord", 246.9), "jig": ("major", 160, 3, "pluck", 293.7),
    "swing": ("dorian", 118, 4, "piano", 174.6), "march": ("major", 112, 4, "accordion", 196.0),
    "folk": ("major", 100, 4, "pluck", 220.0), "pentatonic": ("penta", 92, 4, "music_box", 329.6),
    "musette": ("minor", 140, 3, "accordion", 261.6), "nordic": ("minor", 90, 3, "harpsichord", 220.0),
    "koto": ("inscale", 84, 4, "pluck", 293.7), "street_organ": ("major", 124, 3, "accordion", 261.6),
}


def tone(f, dur, timbre):
    t = np.arange(int(dur * SR)) / SR
    if timbre == "pluck":
        s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.3 for k in range(1, 6)) * np.exp(-t / 0.28)
    elif timbre == "music_box":
        s = (np.sin(2 * np.pi * f * 2 * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t)) * np.exp(-t / 0.5)
    elif timbre == "accordion":
        s = (np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * 1.004 * t)) * \
            np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.05)
    elif timbre == "harpsichord":
        s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9)) * np.exp(-t / 0.35)
    else:  # piano
        s = sum(np.sin(2 * np.pi * f * k * t) / k ** 2 for k in range(1, 6)) * np.exp(-t / 0.6)
    return s * np.minimum(1, t / 0.004)


def piece(style, dur, seed):
    scale_name, bpm, meter, timbre, root = STYLES[style]
    sc = SCALES[scale_name]
    rng = np.random.default_rng(seed)
    beat = 60 / bpm
    out = np.zeros(int(dur * SR) + SR)
    deg = 0
    t, i = 0.0, 0
    prog = [0, 3, 4, 0] if scale_name != "inscale" else [0, 3, 0, 4]
    while t < dur:
        bar = int(i / meter)
        chord = prog[bar % 4]
        if i % meter == 0:  # bass
            f = root / 2 * 2 ** (sc[chord % len(sc)] / 12)
            b = tone(f, beat * meter * 0.9, timbre if timbre != "music_box" else "piano") * 0.5
            s0 = int(t * SR)
            out[s0:s0 + b.size] += b[: max(0, out.size - s0)]
        elif timbre in ("accordion", "pluck") and meter >= 3:  # oom-pah chord
            for k in (2, 4):
                f = root * 2 ** (sc[(chord + k) % len(sc)] / 12)
                c = tone(f, beat * 0.6, timbre) * 0.18
                s0 = int(t * SR)
                out[s0:s0 + c.size] += c[: max(0, out.size - s0)]
        steps = 2 if rng.random() < 0.35 else 1  # melody: random walk on the scale, eighths sometimes
        for k in range(steps):
            deg = int(np.clip(deg + rng.choice([-2, -1, -1, 0, 1, 1, 2]), -3, 9))
            if i % meter == 0 and k == 0:
                deg = chord + rng.choice([0, 2, 4])
            octave, idx = divmod(deg, len(sc))
            f = root * 2 ** (octave + sc[idx] / 12)
            m = tone(f, beat / steps * 0.95, timbre) * 0.42
            s0 = int((t + k * beat / steps) * SR)
            out[s0:s0 + m.size] += m[: max(0, out.size - s0)]
        t += beat
        i += 1
    out = out[: int(dur * SR)]
    fade = int(0.04 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out / max(1e-6, np.abs(out).max()) * 0.6


# ------------------------------------------------------------------ real music: Kevin MacLeod (incompetech.com)
# Same source as the reference channels. CC-BY 4.0: credit "Kevin MacLeod (incompetech.com)" + the track titles in
# the description. Tracks are downloaded once into .cache/music/ (git-ignored).
MUSIC_CACHE = HERE / ".cache" / "music"


def track_audio(title):
    MUSIC_CACHE.mkdir(parents=True, exist_ok=True)
    mp3 = MUSIC_CACHE / f"{title}.mp3"
    if not mp3.exists():
        url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + urllib.parse.quote(title) + ".mp3"
        subprocess.run(["curl", "-sSfL", "-o", str(mp3), url], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def track_clip(title, dur, start=None):
    """dur seconds of a real track. start=None skips a quiet intro: first second whose loudness reaches 60 % of
    the track's loud parts."""
    a = track_audio(title)
    if start is None:
        cs = np.concatenate([[0.0], np.cumsum(a ** 2)])
        idx = np.arange(0, max(1, a.size - SR), SR // 4)
        rms = np.sqrt((cs[idx + SR] - cs[idx]) / SR) if a.size > SR else np.array([1.0])
        loud = np.percentile(rms, 80)
        start = (np.argmax(rms >= 0.6 * loud) / 4) if loud > 0 else 0.0
    s0 = int(start * SR)
    if s0 + int(dur * SR) > a.size:
        s0 = max(0, a.size - int(dur * SR))
    out = np.zeros(int(dur * SR))
    seg = a[s0:s0 + out.size]
    out[:seg.size] = seg
    fi, fo = int(0.03 * SR), int(0.25 * SR)
    out[:fi] *= np.linspace(0, 1, fi)
    out[-fo:] *= np.linspace(1, 0, fo)
    return out / max(1e-6, np.sqrt(np.mean(out ** 2))) * 0.12  # equal loudness across entries


def entry_music(m, dur, seed):
    if "track" in m:
        return track_clip(m["track"], dur, m.get("start"))
    return piece(m["style"], dur, seed)  # synthesised at SR directly


def pop():
    p = render.sfx("pop")
    return np.interp(np.arange(int(p.size * SR / 22050)) / SR, np.arange(p.size) / 22050, p)


# ------------------------------------------------------------------ build + render
def load(path):
    spec = importlib.util.spec_from_file_location("lst", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LIST


def prepare(lst):
    render.W, render.H = W, H
    dur = lst.get("entry_dur", 8.0)
    entries = []
    for n, e in enumerate(lst["entries"], 1):
        base = bg_image(e["bg"])
        base.alpha_composite(title_bar(n, e["name"], e.get("detail"), e.get("flag")), (0, 0))
        pf = photo_frame(LIST / "photo" / e["photo"], e["stamp"])
        base.alpha_composite(pf, (W - pf.width - 6, int(H * 0.06)))
        m = e["music"]
        cr = credit(m["track"], "Kevin MacLeod") if "track" in m else credit(m["title"])
        base.alpha_composite(cr, (W - cr.width - 24, H - cr.height - 20))
        cards = [fact_card(t, r) for t, r in zip(e["facts"], (-2.2, -1.0, -1.6))]
        entries.append(dict(base=base, cards=cards, woj=wojak(e["char"], H * 0.8), start=(n - 1) * dur, dur=dur))
    return entries, dur


CARD_AT = (0.05, 0.35, 0.64)
CARD_POS = [(0.415, 0.24), (0.43, 0.45), (0.415, 0.66)]  # top-left corner, fractions of W/H


def frame(e, lt):
    im = e["base"].copy()
    ang = 1.2 * math.sin(2 * math.pi * lt / 3.6)  # gentle sway around the bottom centre
    wj = e["woj"]
    pad = Image.new("RGBA", (wj.width + 200, wj.height * 2), (0, 0, 0, 0))
    pad.alpha_composite(wj, (100, 0))
    rot = pad.rotate(ang, center=(pad.width / 2, wj.height), resample=Image.BICUBIC)
    rot = rot.crop((0, 0, rot.width, wj.height + 40))
    render.paste_clipped(im, rot, int(W * 0.2 - rot.width / 2), int(H - wj.height + 40))
    for k, c in enumerate(e["cards"]):
        t0 = CARD_AT[k] * e["dur"]
        if lt < t0:
            continue
        age = lt - t0
        sc = 0.86 + 0.14 * min(1, age / 0.16) if age < 0.16 else 1.0
        cc = c if sc == 1 else c.resize((int(c.width * sc), int(c.height * sc)), Image.BILINEAR)
        x, y = CARD_POS[k]
        render.paste_clipped(im, cc, int(W * x + (c.width - cc.width) / 2), int(H * y + (c.height - cc.height) / 2))
    return im.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("listfile")
    ap.add_argument("--still", type=int)
    a = ap.parse_args()
    lst = load(a.listfile)
    name = pathlib.Path(a.listfile).stem
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    entries, dur = prepare(lst)
    if a.still:
        frame(entries[a.still - 1], dur * 0.9).save(out / f"{name}_entry{a.still}.png")
        print(out / f"{name}_entry{a.still}.png")
        return
    total = dur * len(entries)
    audio = np.concatenate([entry_music(e["music"], dur, 100 + i) for i, e in enumerate(lst["entries"])])
    for i, e in enumerate(entries):  # soft card "pop" on every card
        for k in range(3):
            s0 = int((e["start"] + CARD_AT[k] * dur) * SR)
            p = pop() * 0.25
            audio[s0:s0 + p.size] += p[: max(0, audio.size - s0)]
    audio = audio / max(1.0, np.abs(audio).max() / 0.95)
    wav = out / f"{name}.wav"
    with wave.open(str(wav), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    mp4 = out / f"{name}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                           f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset",
                           "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                           "-c:a", "aac", "-ar", "44100", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                           str(mp4)], stdin=subprocess.PIPE)
    n = int(total * FPS)
    for f in range(n):
        gt = f / FPS
        e = entries[min(int(gt // dur), len(entries) - 1)]
        ff.stdin.write(frame(e, gt - e["start"]).tobytes())
        if f % 300 == 0:
            print(f"frame {f}/{n}", flush=True)
    ff.stdin.close()
    ff.wait()
    print(mp4, f"{total:.1f}s")
    (out / f"{name}.json").write_text(json.dumps({"duration": total, "entries": len(entries)}))


if __name__ == "__main__":
    main()
