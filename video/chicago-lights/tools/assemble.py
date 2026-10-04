"""Footage track + overlays + audio -> out/<name>.mp4.

1. Each shot in build/storyboard.json is cut from its film, cropped of burned-in timecode, turned
   black-and-white, scaled into 1920x1080 (4:3 film is pillarboxed on black, as in the reference)
   and encoded to an exact frame count.
2. The shots are concatenated with hard cuts (dissolves happen on the cards' own fades).
3. Overlay cards (ProRes 4444 with alpha from remotion/render.mjs) are laid over at their times.
4. Narration + music bed (about 26 dB under the voice) are mixed and loudness-normalised.
Usage: python3 tools/assemble.py [--only-base] [--name chicago-lights]"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sb = json.load(open(ROOT / "build/storyboard.json"))
FPS = sb["fps"]
name = sys.argv[sys.argv.index("--name") + 1] if "--name" in sys.argv else "chicago-lights"
clips = ROOT / "build/clips"; clips.mkdir(parents=True, exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])

# 1. shots (frame-exact: cumulative rounding so the track never drifts from the narration)
lst = []
for i, s in enumerate(sb["shots"]):
    f0, f1 = round(s["start"] * FPS), round(s["end"] * FPS)
    n = f1 - f0
    if n <= 0: continue
    out = clips / f"{i:03d}.mp4"
    key = f"{s['file']}|{s['in']}|{n}|{s['keep']}"
    tag = out.with_suffix(".key")
    if not (out.exists() and tag.exists() and tag.read_text() == key):
        vf = (f"crop=iw:ih*{s['keep']}:0:0,hue=s=0,scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,"
              f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,eq=contrast=1.06:brightness=-0.01,noise=alls=4:allf=t,fps={FPS},format=yuv420p")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-i", str(ROOT / f"assets/footage/{s['file']}.mp4"),
             "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", str(FPS), str(out)])
        got = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(out)]).strip() or 0)
        if got < n:  # film ran out: hold the last frame
            run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf", f"tpad=stop_mode=clone:stop={n - got}", "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", str(out) + ".tmp.mp4"])
            Path(str(out) + ".tmp.mp4").replace(out)
        tag.write_text(key)
    lst.append(f"file '{out}'")
    print(f"\rshots {i + 1}/{len(sb['shots'])}", end="", flush=True)
print()
(ROOT / "build/clips.txt").write_text("\n".join(lst) + "\n")
base = ROOT / "build/base.mp4"
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(ROOT / "build/clips.txt"), "-c", "copy", str(base)])
if "--only-base" in sys.argv: raise SystemExit(0)

# 3 + 4. overlays and audio in one pass
ov = [o for o in sb["overlays"] if (ROOT / f"build/overlays/{o['id']}.mov").exists()]
missing = [o["id"] for o in sb["overlays"] if o not in ov]
if missing: print("WARNING: overlays not rendered:", missing)
cmd = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", str(base), "-i", str(ROOT / "audio/narration.wav"), "-i", str(ROOT / "assets/music/bed.wav")]
for o in ov:
    cmd += ["-itsoffset", f"{o['start']:.3f}", "-i", str(ROOT / f"build/overlays/{o['id']}.mov")]
fc, last = [], "[0:v]"
for k, o in enumerate(ov):
    nxt = f"[v{k}]"
    fc.append(f"{last}[{k + 3}:v]overlay=0:0:eof_action=pass:enable='between(t,{o['start']:.3f},{o['end'] + 0.05:.3f})'{nxt}")
    last = nxt
fc.append(f"{last}format=yuv420p[vout]")
fc.append("[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0[nar]")
fc.append("[2:a]volume=-27dB[mus]")
fc.append(f"[nar][mus]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[aout]")
(ROOT / "out").mkdir(exist_ok=True)
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]", "-t", f"{sb['duration']:.3f}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(ROOT / f"out/{name}.mp4")]
subprocess.run(cmd, check=True)
print("wrote", ROOT / f"out/{name}.mp4")
