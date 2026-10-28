"""Renders a Wojak Lives episode spec into a vertical 1080x1920 MP4.

    python3 wojak-lives/render/render.py wojak-lives/render/episodes/ep001_introvert.py
    python3 wojak-lives/render/render.py EPISODE.py --still 3      # PNG of scene 3's middle frame only

Needs: ffmpeg, Pillow, numpy, piper-tts (`pip install piper-tts`). The Piper voice is downloaded once into
render/.cache/ (free, offline TTS, no API key). Output: wojak-lives/render/out/<episode>.mp4

An episode file defines EPISODE = {"title": ..., "scenes": [...]}; see episodes/ep001_introvert.py for every
supported key. Times inside a scene are seconds from the scene start, or "vo+X" (X seconds after the
voice-over ends), or "N%" (fraction of the scene).
"""
import argparse
import hashlib
import importlib.util
import json
import math
import pathlib
import random
import subprocess
import urllib.request
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
BRAND = HERE.parent / "brand"
CACHE = HERE / ".cache"
W, H, FPS, SR = 1080, 1920, 30, 22050
INK, TAG, WHITE = (21, 21, 21), (255, 210, 63), (255, 255, 255)
VOICE = "en_US-ryan-medium"
VOICE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/ryan/medium/"


def font(name, size, _cache={}):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(str(BRAND / "fonts" / f"{name}.woff2"), size)
    return _cache[key]


# ------------------------------------------------------------------ characters
def black_and_grey(im):
    """Recolours the coral hoodie of the ChatGPT cut-outs to charcoal, keeping skin, lines and red rage face."""
    a = np.asarray(im.convert("RGBA")).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    hoodie = (b < 110) & (r - b > 50) & (r - g > 35)  # coral + its dark anti-aliased edges; rage-pink skin has b > 130
    lum = (0.3 * r + 0.59 * g + 0.11 * b)
    grey = np.clip(lum * 0.42, 0, 255)
    for c in range(3):
        a[..., c] = np.where(hoodie, grey, a[..., c])
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def npc_tint(im, level=170):
    """Grey 'NPC' version of a cut-out: everything flattened to grey tones, lines kept dark."""
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    lum = 0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]
    out = np.where(lum > 200, level, lum * level / 200)
    a[..., 0] = a[..., 1] = a[..., 2] = out
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def load_char(name, tint=None, _cache={}):
    key = (name, tint)
    if key not in _cache:
        drawn = HERE / "assets" / "chars" / f"{name}.png"
        if drawn.exists():  # characters from draw_niqabi.py are already black and grey
            im = Image.open(drawn).convert("RGBA")
        else:
            im = black_and_grey(Image.open(BRAND / "nobo" / f"{name}.png").convert("RGBA"))
        if tint == "npc":
            im = npc_tint(im)
        elif tint == "light":
            im = npc_tint(im, 215)
        _cache[key] = im
    return _cache[key]


# ------------------------------------------------------------------ backgrounds
def load_bg(name, tint=None, blur=3, _cache={}):
    key = (name, tint, blur)
    if key not in _cache:
        im = Image.open(HERE / "assets" / (name if "/" in name else f"bg/{name}")).convert("RGB")
        im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, 0.5))
        im = ImageEnhance.Color(im).enhance(0.75)
        im = ImageEnhance.Contrast(im).enhance(0.95)
        if tint == "night":
            im = ImageEnhance.Brightness(im).enhance(0.55)
            im = Image.blend(im, Image.new("RGB", im.size, (20, 30, 70)), 0.35)
        elif tint == "warm":
            im = Image.blend(im, Image.new("RGB", im.size, (255, 140, 60)), 0.12)
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        _cache[key] = im
    return _cache[key]


# ------------------------------------------------------------------ voice
def ensure_voice():
    CACHE.mkdir(exist_ok=True)
    for suffix in (".onnx", ".onnx.json"):
        f = CACHE / f"{VOICE}{suffix}"
        if not f.exists():
            print("downloading voice", f.name)
            urllib.request.urlretrieve(VOICE_URL + f.name, f)
    return CACHE / f"{VOICE}.onnx"


def tts(text, length_scale=1.05):
    model = ensure_voice()
    out = CACHE / "vo" / (hashlib.md5(f"{VOICE}|{length_scale}|{text}".encode()).hexdigest()[:16] + ".wav")
    out.parent.mkdir(exist_ok=True)
    if not out.exists():
        subprocess.run(["python3", "-m", "piper", "-m", str(model), "-f", str(out), "--length-scale",
                        str(length_scale)], input=text.encode(), check=True, capture_output=True)
    with wave.open(str(out)) as w:
        assert w.getframerate() == SR
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


# ------------------------------------------------------------------ sound effects (synthesised, no licences)
def env(n, attack=0.005, decay=None):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(attack, 1e-4))
    if decay:
        e = e * np.exp(-t / decay)
    return e


def sfx(name, rng=np.random.default_rng(3)):
    t = lambda dur: np.arange(int(dur * SR)) / SR
    if name == "thwack":
        x = t(0.25)
        return 0.9 * (np.sin(2 * np.pi * 70 * x) * np.exp(-x / 0.06) + 0.6 * rng.normal(0, 1, x.size) *
                      np.exp(-x / 0.02))
    if name == "boing":
        x = t(0.6)
        f = 180 + 120 * np.exp(-x / 0.25) * np.sin(2 * np.pi * 14 * x) + 60 * x
        return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.3)
    if name == "pop":
        x = t(0.08)
        return 0.5 * np.sin(2 * np.pi * (900 - 4000 * x) * x) * np.exp(-x / 0.02)
    if name == "whoosh":
        x = t(0.4)
        n = np.convolve(rng.normal(0, 1, x.size), np.ones(12) / 12, "same")
        return 0.6 * n * np.sin(np.pi * x / 0.4) ** 2
    if name == "scratch":
        x = t(0.35)
        f = 900 * np.exp(-x / 0.12) + 150
        return 0.45 * (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + rng.normal(0, 0.5, x.size)) * \
            np.exp(-x / 0.15)
    if name == "slide_down":
        x = t(0.6)
        f = 1100 * np.exp(-x / 0.3) + 220
        return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum(1, (0.6 - x) / 0.1)
    if name == "buzz":
        x = t(0.7)
        gate = ((x % 0.35) < 0.22).astype(float)
        return 0.35 * np.sign(np.sin(2 * np.pi * 160 * x)) * gate * 0.6
    if name == "tick":
        x = t(0.03)
        return 0.4 * rng.normal(0, 1, x.size) * np.exp(-x / 0.004)
    if name == "sting":
        out = []
        for f in (523, 659, 784):
            x = t(0.22)
            out.append(0.3 * np.sin(2 * np.pi * f * x) * np.exp(-x / 0.12))
        return np.concatenate(out)
    if name == "impact":  # deep cinematic hit (title card)
        x = t(1.2)
        return 0.9 * np.sin(2 * np.pi * (45 + 30 * np.exp(-x / 0.1)) * x) * np.exp(-x / 0.45) + \
            0.25 * rng.normal(0, 1, x.size) * np.exp(-x / 0.05)
    if name == "horn":
        x = t(0.5)
        return 0.3 * (np.sign(np.sin(2 * np.pi * 330 * x)) + np.sign(np.sin(2 * np.pi * 415 * x))) * \
            np.minimum(1, (0.5 - x) / 0.05)
    if name == "ding":
        x = t(0.8)
        return 0.35 * (np.sin(2 * np.pi * 1320 * x) + 0.5 * np.sin(2 * np.pi * 1980 * x)) * np.exp(-x / 0.25)
    if name == "door":
        x = t(0.3)
        return 0.8 * np.sin(2 * np.pi * 55 * x) * np.exp(-x / 0.08) + 0.3 * rng.normal(0, 1, x.size) * \
            np.exp(-x / 0.03)
    if name.startswith("talk"):  # gibberish blips for non-narrator speech
        dur = float(name[4:] or 1.2)
        out = np.zeros(int(dur * SR))
        pos = 0
        while pos < out.size - 2000:
            n = int(rng.uniform(0.06, 0.11) * SR)
            x = np.arange(n) / SR
            f = rng.uniform(260, 420)
            blip = 0.25 * np.sign(np.sin(2 * np.pi * f * x)) * 0.5 * np.sin(np.pi * x / x[-1])
            out[pos:pos + n] += blip[: out.size - pos]
            pos += n + int(rng.uniform(0.01, 0.04) * SR)
        return out
    raise ValueError(name)


def music(dur, mood="lofi"):
    """Soft pluck loop (procedural, so no licence issues). "sad" = slower minor piano-like loop, louder (no voice)."""
    x = np.zeros(int(dur * SR))
    chords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7), (164.8, 207.7, 246.9)]
    if mood == "sad":
        chords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (130.8, 196.0, 261.6), (146.8, 196.0, 246.9)]
    beat = 60 / (88 if mood == "sad" else 84)
    i = 0
    while i * beat < dur:
        chord = chords[(i // 4) % 4]
        f = chord[[0, 1, 2, 1][i % 4]]
        n = int(beat * 0.95 * SR)
        s = int(i * beat * SR)
        tt = np.arange(n) / SR
        note = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt / 0.35)
        if i % 4 == 0:
            note += 0.5 * np.sin(2 * np.pi * chord[0] / 2 * tt) * np.exp(-tt / 0.6)
        x[s:s + n] += note[: max(0, min(n, x.size - s))]
        i += 1
    return (0.11 if mood == "sad" else 0.05) * x


# ------------------------------------------------------------------ drawing helpers
def text_size(txt, fnt):
    b = fnt.getbbox(txt)
    return b[2] - b[0], b[3] - b[1]


def wrap(txt, fnt, maxw):
    lines, cur = [], ""
    for word in txt.split():
        trial = (cur + " " + word).strip()
        if text_size(trial, fnt)[0] <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def tag_image(text, size=70, rot=-3):
    fnt = font("lilita", size)
    tw, th = text_size(text, fnt)
    pad = 28
    im = Image.new("RGBA", (tw + 2 * pad + 14, int(size * 1.45) + 14), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, tw + 2 * pad + 10, int(size * 1.45) + 10), 12, fill=INK)
    d.rounded_rectangle((0, 0, tw + 2 * pad, int(size * 1.45)), 12, fill=TAG, outline=INK, width=7)
    d.text((pad, size * 0.18), text, font=fnt, fill=INK)
    return im.rotate(-rot, expand=True, resample=Image.BICUBIC)


def bubble_image(text, style="speech", tail="down-left", maxw=760):
    fnt = font("baloo", 54 if style != "phone" else 50)
    lines = wrap(text, fnt, maxw)
    lh = int(fnt.size * 1.15)
    tw = max(text_size(l, fnt)[0] for l in lines)
    bw, bh = tw + 70, lh * len(lines) + 46
    im = Image.new("RGBA", (bw + 20, bh + 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fill = (235, 235, 238) if style == "phone" else WHITE
    if style == "phone":
        fill, txtcol = (58, 120, 255), WHITE
    else:
        txtcol = INK
    d.rounded_rectangle((6, 6, bw + 6, bh + 6), 34, fill=fill, outline=INK, width=6)
    tx = {"down-left": 70, "down-right": bw - 70, "down": bw // 2}.get(tail)
    if tx:
        d.polygon([(tx - 26, bh), (tx + 26, bh), (tx - 10 if "left" in tail else tx + 10, bh + 58)], fill=fill,
                  outline=INK)
        d.line([(tx - 26, bh + 1), (tx + 26, bh + 1)], fill=fill, width=8)
        d.line([(tx - 26, bh), (tx - 10 if "left" in tail else tx + 10, bh + 58), (tx + 26, bh)], fill=INK,
               width=6)
    y = 26
    for line in lines:
        d.text((40, y), line, font=fnt, fill=txtcol)
        y += lh
    return im


def caption_image(words, keywords):
    fnt = font("baloo", 78)
    lines = wrap(" ".join(words), fnt, 940)
    lh = int(fnt.size * 1.12)
    im = Image.new("RGBA", (W, lh * len(lines) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 10
    for line in lines:
        lw = text_size(line, fnt)[0] + 40
        x = (W - lw) // 2
        for word in line.split():
            col = TAG if word.strip(".,!?\"'…").upper() in keywords else WHITE
            d.text((x, y), word, font=fnt, fill=col, stroke_width=12, stroke_fill=INK)
            x += text_size(word + " ", fnt)[0] + 14
        y += lh
    return im


def text_caption(txt, keywords):
    """Reference-style sentence caption: top-left, white with a black outline, one or two lines."""
    fnt = font("baloo", int(H * 0.052))
    lines = wrap(txt, fnt, int(W * 0.62))
    lh = int(fnt.size * 1.12)
    im = Image.new("RGBA", (int(W * 0.7), lh * len(lines) + 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y = 6
    for line in lines:
        x = 6
        for word in line.split():
            col = TAG if word.strip(".,!?\"'…:").upper() in keywords else WHITE
            d.text((x, y), word, font=fnt, fill=col, stroke_width=max(4, fnt.size // 9), stroke_fill=INK)
            x += text_size(word + " ", fnt)[0] + fnt.size // 5
        y += lh
    return im


def big_text(txt, size, color):
    fnt = font("baloo", size)
    tw, th = text_size(txt, fnt)
    im = Image.new("RGBA", (tw + size, int(size * 1.6)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((size // 2, size // 6), txt, font=fnt, fill=color, stroke_width=max(6, size // 12),
                            stroke_fill=INK)
    return im


def draw_fx(frame, f, age):
    """Literal visual gags drawn on top: flames, sweat, question marks, exclamation, hearts, steam."""
    d = ImageDraw.Draw(frame)
    kind, cx, cy, size = f["kind"], f["x"] * W, f["y"] * H, f.get("size", 1.0) * H * 0.12
    rnd = random.Random(int(age * 12) + int(cx))
    if kind == "flames":
        for i, dx in enumerate((-1.2, -0.4, 0.4, 1.2)):
            h = size * (1.0 + 0.25 * rnd.random()) * (1.25 if i in (1, 2) else 0.85)
            x0, y0 = cx + dx * size * 0.55, cy
            for col, k in (((236, 80, 20), 1.0), ((255, 170, 30), 0.68), ((255, 235, 120), 0.36)):
                w, hh = size * 0.42 * k, h * k
                sway = (rnd.random() - 0.5) * size * 0.25
                d.polygon([(x0 - w, y0), (x0 - w * 0.6, y0 - hh * 0.5), (x0 + sway, y0 - hh), (x0 + w * 0.6, y0 - hh * 0.5),
                           (x0 + w, y0), (x0, y0 + w * 0.5)], fill=col)
    elif kind == "sweat":
        for i in range(f.get("n", 3)):
            x0 = cx + (i - 1) * size * 0.7
            y0 = cy + ((age * 0.9 + i * 0.3) % 1.0) * size * 1.5
            d.polygon([(x0, y0 - size * 0.35), (x0 - size * 0.16, y0), (x0, y0 + size * 0.14), (x0 + size * 0.16, y0)],
                      fill=(130, 205, 250), outline=INK)
    elif kind in ("question", "exclaim"):
        fnt = font("lilita", int(size * 1.3))
        for i, dx in enumerate((-0.8, 0.0, 0.8)):
            bob = math.sin(age * 6 + i) * size * 0.08
            d.text((cx + dx * size, cy + bob), "?" if kind == "question" else "!", font=fnt, fill=TAG,
                   stroke_width=6, stroke_fill=INK, anchor="mm")
    elif kind == "hearts":
        for i in range(4):
            a = age * 0.8 + i * 0.25
            x0 = cx + math.sin(i * 2.1 + age) * size
            y0 = cy - (a % 1.0) * size * 2.2
            r = size * 0.22
            d.ellipse((x0 - r, y0 - r, x0, y0), fill=(235, 70, 90), outline=INK, width=3)
            d.ellipse((x0, y0 - r, x0 + r, y0), fill=(235, 70, 90), outline=INK, width=3)
            d.polygon([(x0 - r, y0 - r * 0.45), (x0 + r, y0 - r * 0.45), (x0, y0 + r * 0.9)], fill=(235, 70, 90))
    elif kind == "steam":
        for i in range(3):
            x0 = cx + (i - 1) * size * 0.6
            pts = [(x0 + math.sin(age * 5 + k * 0.9 + i) * size * 0.15, cy - k * size * 0.18) for k in range(8)]
            d.line(pts, fill=(235, 235, 235), width=int(size * 0.12), joint="curve")


def ease_out(p):
    return 1 - (1 - min(max(p, 0), 1)) ** 3


def pop_scale(age, dur=0.2):
    if age >= dur:
        return 1.0
    p = age / dur
    return 1.12 * ease_out(p / 0.7) if p < 0.7 else 1.12 - 0.12 * (p - 0.7) / 0.3


# ------------------------------------------------------------------ episode timing
def resolve_time(t, scene_dur, vo_end):
    if isinstance(t, (int, float)):
        return float(t)
    t = str(t)
    if t.endswith("%"):
        return scene_dur * float(t[:-1]) / 100
    if t.startswith("vo"):
        return vo_end + float(t[2:] or 0)
    return float(t)


def caption_chunks(text, start, dur, max_words=4):
    words = text.replace("—", " ").split()
    chunks, cur = [], []
    for w_ in words:
        cur.append(w_)
        if len(cur) >= max_words or w_[-1] in ".?!,…" and len(cur) >= 2:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    total = sum(len(" ".join(c)) + 4 for c in chunks)
    out, t = [], start
    for c in chunks:
        d = dur * (len(" ".join(c)) + 4) / total
        out.append((t, t + d, c))
        t += d
    return out


def build(ep):
    """Turns the spec into absolute timings + the mixed audio track."""
    scenes, t0 = [], 0.0
    ls = ep.get("voice_speed", 1.05)
    for sc in ep["scenes"]:
        vo = tts(sc["vo"], ls) if sc.get("vo") else np.zeros(0, np.float32)
        lead = sc.get("lead", 0.25)
        vo_dur = vo.size / SR
        if not sc.get("vo") and sc.get("text") and not sc.get("dur"):
            lead = 0.0
            dur = max(3.2, 1.0 + 0.25 * len(sc["text"].split()))  # reading time for on-screen text
        else:
            dur = sc.get("dur") or (lead + vo_dur + sc.get("hold", 0.45))
        vo_end = lead + vo_dur
        s = dict(sc, start=t0, dur=dur, vo_audio=vo, vo_start=lead, vo_end=vo_end)
        s["caps"] = caption_chunks(sc["vo"], lead, vo_dur) if sc.get("vo") else []
        for key in ("beats", "bubbles", "labels", "extras", "sfx", "fx", "lines"):
            s[key] = [dict(item, t=resolve_time(item.get("t", 0), dur, vo_end),
                           **({"t1": resolve_time(item["t1"], dur, vo_end)} if "t1" in item else {}))
                      for item in sc.get(key, [])]
        scenes.append(s)
        t0 += dur
    total = t0
    audio = np.zeros(int((total + 0.5) * SR), np.float32)

    def add(sig, at, gain=1.0):
        i = int(at * SR)
        n = min(sig.size, audio.size - i)
        if n > 0:
            audio[i:i + n] += gain * sig[:n]

    voice = np.zeros_like(audio)
    for s in scenes:
        i = int((s["start"] + s["vo_start"]) * SR)
        n = min(s["vo_audio"].size, voice.size - i)
        voice[i:i + n] += s["vo_audio"][:n]
        for fx in s["sfx"]:
            add(sfx(fx["name"]), s["start"] + fx["t"], fx.get("gain", 0.6))
        for b in s["bubbles"]:
            if b.get("talk"):
                add(sfx(f"talk{b.get('talk_dur', 1.1)}"), s["start"] + b["t"], 0.55)
        if s is scenes[0]:
            add(sfx("thwack"), 0.0, 0.7)
    bed = music(audio.size / SR, ep.get("music", "lofi"))[: audio.size]
    duck = np.convolve((np.abs(voice) > 0.02).astype(np.float32), np.ones(4000) / 4000, "same")
    audio[: bed.size] += bed * (1 - 0.6 * np.clip(duck[: bed.size] * 3, 0, 1))
    audio += voice
    audio = audio / max(1.0, np.abs(audio).max() / 0.95)
    return scenes, total, audio


# ------------------------------------------------------------------ frame rendering
def place_char(world, img, pos, size, flip, breath, slide=0.0):
    th = int(H * size * (1 + breath))
    tw = int(img.width * (H * size) / img.height)
    im = img.transpose(Image.FLIP_LEFT_RIGHT) if flip else img
    im = im.resize((tw, th), Image.LANCZOS)
    x = int(pos[0] * W - tw / 2 + slide * W)
    y = int(pos[1] * H - th)
    paste_clipped(world, im, x, y)


def paste_clipped(world, im, x, y):
    box = (max(0, -x), max(0, -y), min(im.width, W - x), min(im.height, H - y))
    if box[2] > box[0] and box[3] > box[1]:
        world.alpha_composite(im.crop(box), (max(0, x), max(0, y)))


def render_frame(s, lt, gt, ep, title_img):
    world = load_bg(s["bg"], s.get("tint"), s.get("blur", 3)).convert("RGBA").copy()
    # extras (other characters) behind the lead
    for ex in s["extras"]:
        if lt < ex["t"] or ("t1" in ex and lt >= ex["t1"]):
            continue
        age = lt - ex["t"]
        slide = (1 - ease_out(age / 0.3)) * ex.get("enter", 0)
        img = load_char(ex["img"], ex.get("tint"))
        place_char(world, img, ex["pos"], ex.get("size", 0.4), ex.get("flip", False),
                   0.008 * math.sin(gt * 2.2 + 1), slide)
    # lead character: latest beat wins
    wide = W > H
    state = {"char": s.get("char"), "pos": tuple(s.get("pos", (0.5, 1.16) if wide else (0.5, 1.03))),
             "size": s.get("size", 1.05 if wide else 0.45),
             "flip": s.get("flip", False), "tint": s.get("char_tint")}
    zoom, shake = 1.0, 0.0
    for b in s["beats"]:
        if lt >= b["t"]:
            for k in ("char", "pos", "size", "flip", "tint"):
                if k in b:
                    state[k] = b[k]
            age = lt - b["t"]
            if "punch" in b:
                zoom = b["punch"]
            if "shake" in b and age < b["shake"]:
                shake = 14 * (1 - age / b["shake"])
            if b.get("unpunch"):
                zoom = 1.0
    exit_ = s.get("exit")
    slide = 0.0
    if exit_ and lt > resolve_time(exit_["t"], s["dur"], s["vo_end"]):
        slide = exit_["dx"] * ease_out((lt - resolve_time(exit_["t"], s["dur"], s["vo_end"])) / exit_.get("d", 1.2))
    if state["char"]:
        place_char(world, load_char(state["char"], state["tint"]), state["pos"], state["size"], state["flip"],
                   0.01 * math.sin(gt * 2.4), slide)
    # camera: slow push across the scene * punch-ins, around the character's face
    push = 1 + (s.get("push", 1.05) - 1) * (lt / s["dur"])
    z = push * zoom
    cx, cy = W * state["pos"][0], H * (state["pos"][1] - state["size"] * 0.62)
    if shake:
        z = max(z, 1.03)  # zoom in a touch so the shaken crop never leaves the photo
        cx += random.uniform(-shake, shake)
        cy += random.uniform(-shake, shake)
    cx, cy = min(max(cx, W / (2 * z)), W - W / (2 * z)), min(max(cy, H / (2 * z)), H - H / (2 * z))
    if z != 1 or shake:
        bw, bh = W / z, H / z
        world = world.resize((W, H), Image.BILINEAR, box=(cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2))
    frame = world
    # UI layer: bubbles, labels, captions, title tag
    for b in s["bubbles"]:
        if lt < b["t"] or ("t1" in b and lt >= b["t1"]):
            continue
        im = bubble_image(b["text"], b.get("style", "speech"), b.get("tail", "down-left"))
        sc = pop_scale(lt - b["t"])
        if sc != 1:
            im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
        paste_clipped(frame, im, int(b["x"] * W - im.width / 2), int(b["y"] * H - im.height / 2))
    for lb in s["labels"]:
        if lt < lb["t"] or ("t1" in lb and lt >= lb["t1"]):
            continue
        im = tag_image(lb["text"], lb.get("size", 64), lb.get("rot", -4))
        sc = pop_scale(lt - lb["t"])
        if sc != 1:
            im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
        paste_clipped(frame, im, int(lb["x"] * W - im.width / 2), int(lb["y"] * H - im.height / 2))
    for f in s["fx"]:
        if lt >= f["t"] and not ("t1" in f and lt >= f["t1"]):
            draw_fx(frame, f, lt - f["t"])
    for ln in s["lines"]:
        if lt >= ln["t"]:
            im = big_text(ln["text"], ln.get("size", 120), ln.get("color", WHITE))
            sc = pop_scale(lt - ln["t"], 0.18)
            if sc != 1:
                im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
            paste_clipped(frame, im, int(W / 2 - im.width / 2), int(ln["y"] * H - im.height / 2))
    if s.get("text"):
        im = text_caption(s["text"], set(k.upper() for k in s.get("keywords", [])))
        paste_clipped(frame, im, int(0.03 * W), int(0.035 * H))
    for c0, c1, words in s["caps"]:
        if c0 <= lt < c1:
            cap = caption_image(words, set(k.upper() for k in s.get("keywords", [])))
            sc = pop_scale(lt - c0, 0.12)
            if sc != 1:
                cap = cap.resize((max(1, int(cap.width * sc)), max(1, int(cap.height * sc))), Image.BILINEAR)
            paste_clipped(frame, cap, int(W / 2 - cap.width / 2), int(s.get("cap_y", 0.17) * H))
    if not s.get("no_title") and not ep.get("no_title"):
        im = title_img
        if gt < 0.25:  # tag slap
            p = ease_out(gt / 0.25)
            sc = 1.6 - 0.6 * p
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR).rotate(
                12 * (1 - p), expand=True, resample=Image.BILINEAR)
        paste_clipped(frame, im, int(W / 2 - im.width / 2), int(0.115 * H - im.height / 2))
    return frame.convert("RGB")


def load_episode(path):
    spec = importlib.util.spec_from_file_location("ep", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EPISODE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--still", type=int, help="render only the middle frame of this scene (1-based) as PNG")
    ap.add_argument("--out")
    args = ap.parse_args()
    ep = load_episode(args.episode)
    global W, H
    W, H = ep.get("size", (W, H))
    name = pathlib.Path(args.episode).stem
    outdir = HERE / "out"
    outdir.mkdir(exist_ok=True)
    scenes, total, audio = build(ep)
    title_img = tag_image(ep["title"], 66, -3)
    random.seed(1)
    if args.still:
        s = scenes[args.still - 1]
        lt = s.get("still_t", s["dur"] * 0.6)
        render_frame(s, lt, s["start"] + lt, ep, title_img).save(outdir / f"{name}_scene{args.still}.png")
        print(outdir / f"{name}_scene{args.still}.png")
        return
    wav = outdir / f"{name}.wav"
    with wave.open(str(wav), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes())
    out = pathlib.Path(args.out) if args.out else outdir / f"{name}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                           f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset",
                           "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-ar", "44100", "-b:a", "160k",
                           "-shortest", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = int(total * FPS)
    si = 0
    for f in range(n):
        gt = f / FPS
        while si < len(scenes) - 1 and gt >= scenes[si]["start"] + scenes[si]["dur"]:
            si += 1
        s = scenes[si]
        ff.stdin.write(render_frame(s, gt - s["start"], gt, ep, title_img).tobytes())
        if f % 150 == 0:
            print(f"frame {f}/{n}", flush=True)
    ff.stdin.close()
    ff.wait()
    print(out, f"{total:.1f}s")
    (outdir / f"{name}.json").write_text(json.dumps({"duration": total, "scenes": [
        {"start": round(s["start"], 2), "dur": round(s["dur"], 2), "vo": s.get("vo", "")} for s in scenes]},
        indent=1))


if __name__ == "__main__":
    main()
