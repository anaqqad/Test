"""Final assembly in time segments, for episodes with too many overlay cards to decode at once (assemble.py ran out of
memory with 76 VP9 layers at 1080p). Run `python tools/assemble.py --only-base --hd` first so build/clips/ is current.
Each segment ends on a shot boundary that no card spans; segments are encoded with the same settings, joined without
re-encoding and muxed with the narration + music mix (loudness-normalised to -16 LUFS).
Usage: python tools/assemble_parts.py [segments]"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sb = json.load(open(ROOT / "build/storyboard.json", encoding="utf-8"))
FPS, W, H = sb["fps"], 1920, 1080
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
name = ROOT.name
clips = sorted((ROOT / "build/clips").glob("[0-9][0-9][0-9].mp4"))
shots = [s for s in sb["shots"] if round(s["end"] * FPS) - round(s["start"] * FPS) > 0]
assert len(clips) == len(shots), (len(clips), len(shots))
ov = sb["overlays"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-3000:])


# segment boundaries: shot starts (frame-exact) that no overlay spans, nearest to k * total / N
starts = [(i, round(s["start"] * FPS) / FPS) for i, s in enumerate(shots)]
free = [(i, t) for i, t in starts if i > 0 and not any(o["start"] - 0.1 < t < o["end"] + 0.1 for o in ov)]
cuts = [0]
for k in range(1, N):
    target = sb["duration"] * k / N
    cuts.append(min(free, key=lambda it: abs(it[1] - target))[0])
cuts.append(len(shots))
parts = []
for k in range(N):
    a, b = cuts[k], cuts[k + 1]
    t0 = round(shots[a]["start"] * FPS) / FPS
    t1 = round(shots[b - 1]["end"] * FPS) / FPS if b == len(shots) else round(shots[b]["start"] * FPS) / FPS
    lst = ROOT / f"build/part{k}.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in clips[a:b]))
    mine = [o for o in ov if o["start"] >= t0 - 0.01 and o["start"] < t1]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst)]
    for o in mine:
        cmd += ["-itsoffset", f"{o['start'] - t0:.3f}", "-c:v", "libvpx-vp9", "-i", str(ROOT / f"build/overlays/{o['id']}.webm")]
    fc, last = [], "[0:v]"
    for j, o in enumerate(mine):
        fc.append(f"[{j + 1}:v]scale={W}:{H}[s{j}]")
        fc.append(f"{last}[s{j}]overlay=0:0:eof_action=pass:enable='between(t,{o['start'] - t0:.3f},{o['end'] - t0 + 0.05:.3f})'[v{j}]")
        last = f"[v{j}]"
    fc.append(f"{last}format=yuv420p[vout]")
    out = ROOT / f"build/part{k}.mp4"
    print(f"part {k}: {t0:.2f}-{t1:.2f} s, {b - a} shots, {len(mine)} cards", flush=True)
    run(cmd + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-t", f"{t1 - t0:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
               "-r", str(FPS), "-an", str(out)])
    parts.append(out)
(ROOT / "build/parts.txt").write_text("".join(f"file '{p}'\n" for p in parts))
(ROOT / "out").mkdir(exist_ok=True)
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(ROOT / "build/parts.txt"),
     "-i", str(ROOT / "audio/narration.wav"), "-i", str(ROOT / "assets/music/bed.wav"),
     "-filter_complex", "[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0[nar];[2:a]volume=-27dB[mus];"
     "[nar][mus]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]",
     "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{sb['duration']:.3f}",
     "-movflags", "+faststart", str(ROOT / f"out/{name}.mp4")])
for p in parts: p.unlink()
print("wrote", ROOT / f"out/{name}.mp4")
