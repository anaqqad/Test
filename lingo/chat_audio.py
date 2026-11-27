# Sound mix for chat.mjs (Blueprint 03): python3 chat_audio.py <timeline.json> <out.wav>
# Music beds (real, credited CC tracks) play only under beats with "music": true (or a track name) and cuts to silence on deadpan
# beats; the music keeps its place between windows (it does not restart). Sound effects: chat/assets/sfx/*.wav.
import json, os, subprocess, sys, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 44100
tl = json.load(open(sys.argv[1]))
dur = tl["dur"]
out = np.zeros(int(SR * (dur + 1)), np.float32)

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

m = tl.get("music")
tracks = {}
if m:
    tracks = {"default": m} if "file" in m else m      # one track, or {"default": {...}, "sad": {...}, ...}
MUSIC_DB = tl.get("musicDb", -21.0)                    # reference: music bed about -21 dB RMS (owner: "music so loud it hurts")
def rmsdb0(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
loaded, cursors = {}, {}
beats = tl["beats"]
for k, b in enumerate(beats):
    name = b["music"]
    if not name or name not in tracks:
        continue
    tr = tracks[name]
    if name not in loaded:
        x = load(os.path.join(HERE, tr["file"]))
        x = x[int(SR * tr.get("start", 0)):]
        loud = x[np.abs(x) > 1e-4]
        loaded[name] = x * 10 ** ((MUSIC_DB + tr.get("trim", 0) - rmsdb0(loud)) / 20)   # every track at the same level
        cursors[name] = 0
    mus = loaded[name]
    a = b["start"]; e = beats[k + 1]["start"] if k + 1 < len(beats) else dur
    i0, i1 = int(SR * a), int(SR * e); n = i1 - i0
    c = cursors[name] % len(mus)
    seg = np.resize(np.concatenate([mus[c:], mus[:c]]), n)
    f = min(int(SR * 0.025), n // 2)
    seg[:f] *= np.linspace(0, 1, f); seg[n - f:] *= np.linspace(1, 0, f)
    out[i0:i1] += seg; cursors[name] += n

# sound effects, balanced to the reference: the message pop's RMS sits about 3.5 dB above the music bed's RMS
# (reference: pop -16.5 dB, music about -20 dB); other effects are set relative to that
def rmsdb(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
# absolute levels taken from the reference (owner: "the music is so loud it hurts"): music bed about -21 dB RMS,
# message pop about -16.5 dB RMS. The music is scaled to its target first; effects are set relative to it.
music_db = MUSIC_DB
REL = {"discord_pop": 4.5, "pop": 4.5, "ping": 3.5, "join": 3.0, "role": 3.0, "boom": 5.0, "scratch": 1.0, "typing": -14.0, "crickets": -2.0, "discord_call": 0.0, "sad_trombone": 1.0, "dun_dun_dun": 2.0}
cache = {}
for b in tl["beats"]:
    for s in b["sfx"]:
        name = s["name"]
        if name not in cache:
            f = os.path.join(HERE, "chat", "assets", "sfx", name + ".wav")
            if not os.path.exists(f):
                f = os.path.join(HERE, "chat", "assets", "sfx", "meme", name + ".wav")
            x = load(f)
            core = x[np.abs(x) > np.abs(x).max() * 0.05]
            cache[name] = x * 10 ** ((music_db + REL.get(name, 3.0) - rmsdb(core[: int(SR * 0.16)])) / 20)
        x = cache[name]; i0 = int(SR * s["at"])
        out[i0:i0 + len(x)] += x[: len(out) - i0]
out = out[: int(SR * dur)]
out = out / max(1.0, np.abs(out).max() / 0.95)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("audio ->", sys.argv[2])
