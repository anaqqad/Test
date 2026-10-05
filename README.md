# Test repo

Two things live here:

- `blender/`: scripted Blender shots for history documentaries (see `CLAUDE.md` and `blender/README.md`).
- Root (`src/`, `scripts/`, `data/`, `public/`): **Reels for The Black History Room**, a vertical
  1080x1920 / 30 fps format for Facebook Reels (also Instagram Reels and YouTube Shorts).

## Reels

The Reel pipeline is a copy of the MathDoc pipeline from `anaqqad/Youtube-Automation`
(branch `claude/ecstatic-turing-j7jqd8`), cut down to what reels need, with the same file names so
fixes can move between the two repos:

| File | From MathDoc | What it does here |
| --- | --- | --- |
| `scripts/tts_mathdoc.py`, `tts_elevenlabs.py`, `tts_kokoro.py` | unchanged | voice the spec -> `public/generated/<id>/narration.wav` + `timeline.json` (word timings, beat starts) |
| `scripts/fetch_pd_images.py` | + records pixel size | public-domain / CC0 images from Wikimedia Commons, licence checked, `credits.json` |
| `scripts/make_music.py` | unchanged | original ambient bed |
| `scripts/mix_mathdoc.py` | + `"mix"` options in the spec | voice leveller, music bed, master; reels use -14 LUFS, -1.5 dBTP, music 21 dB under the voice |
| `scripts/retime_mathdoc.py`, `check_blank.py`, `qc_mathdoc.py` | unchanged | re-cut without re-voicing; blank-frame check; 16:9 contact sheet |
| `scripts/qc_reel.py` | new | safe zones, cover frame, caption sizes, length, word count, loudness, vertical contact sheet |
| `src/reel/*` | new | the `Reel` composition (registered in `src/Root.tsx`) |

### Spec (`data/reel-<slug>.json`)

Same shape as a MathDoc spec, with `"format": "reel"`, so `tts_mathdoc.py` voices it unchanged.

- `voice`: ElevenLabs "Andrew" (same block as the Sand video). Beats with `"section"` start a new request.
- `assets`: Commons file titles; `faces`: face boxes per image (0..1), used by the safe-zone QC.
- `beats[]`: `text` (one fact per beat), `visual`, optional `overlays`, `captions: false` for beats that
  show their own text (hook, end card).
- `facts[]` / `sources`: the fact sheet. Every claim lists at least two independent sources.

Visual kinds: `photo` (Ken Burns with sepia grade: `image`, `focus`, `anchor`, `zoom`, `motion`),
`card` (cropped image on a blurred copy: `crop`, `caption`, `clipping: true` for a newspaper clipping),
`map` (illustrative Charleston harbor map: `step` = `wharf | forts | sumter | fleet`), `endcard`.

Overlays: `hook` (bold opening line, complete on frame 0), `lowerThird {name, sub}`, `year {from, to}`
(counter), `pin {label, sub}` (map-pin location chip), `stamp` (gold label, e.g. a date).

Captions are word by word from `timeline.json`: 2-4 words at a time, Playfair Display 88 px, cream, the
spoken word in gold. Without a timeline (before voicing) the words are spread at an estimated pace.

### Safe zones

Facebook covers the bottom 20 % and the right 15 % of a Reel. All text sits in the column
x 60-918, y 150-1536 (`SAFE` in `src/reel/style.ts`). `scripts/qc_reel.py` renders the reel in QC
mode, where every caption, title and label is solid magenta and every face box cyan, and fails if any of
them reach those zones in any frame, or if text touches the left or top edge. It also checks that frame
0 has the hook text and a face (cover still).

### Run

```bash
npm install
pip install numpy soundfile pyloudnorm scipy pillow opencv-python-headless kokoro-onnx
S=data/reel-robert-smalls.json
python3 scripts/fetch_pd_images.py $S
python3 scripts/tts_mathdoc.py $S        # ElevenLabs: paid, needs ELEVENLABS_API_KEY; ask first
python3 scripts/make_music.py $S
python3 scripts/mix_mathdoc.py $S
npx remotion render Reel out/reel-robert-smalls.mp4 --props=$S
python3 scripts/qc_reel.py $S out/reel-robert-smalls.mp4
```

Free timing preview: copy the spec with a new `id` ending in `-scratch` and
`"voice": {"engine": "kokoro", "voice": "am_michael", "speed": 1.1}`; symlink
`public/pd/<id>-scratch` to the real image folder. Both are git-ignored.
