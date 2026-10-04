# LingoDude: language videos, fully scripted

Six 1080p/30 fps videos in the style of "That's Quite Interesting" ("Nearly Extinct Languages be like…"), built
with code: no image generator, no paid API, no stock footage.

| key | title | languages |
|---|---|---|
| `extinct2` | Nearly Extinct Languages be like… Part 2 | 9 |
| `niche2` | Insanely Niche Languages be like… Part 2 | 11 |
| `hardest` | Ranking languages by how hard they are (for English speakers) | 18 |
| `sounds` | Languages with the weirdest sounds be like… | 12 |
| `conlangs` | Constructed Languages be like… | 6 |
| `revived` | Revived Languages be like… (back from the dead) | 6 |

## Rule: real sound only
Every language segment plays a **real recording found on Wikimedia Commons** (Wikitongues donations, Lingua Libre
word recordings, other CC0 / CC BY / CC BY-SA / public-domain files). No synthesized speech, no generated music.
A language with no recording found is dropped (`render.mjs` skips any item whose audio failed).
CC BY / BY-SA need attribution: paste `out/<video>_credits.txt` into the YouTube description.

## Run
    npm i                                  # playwright-core, flag-icons, fonts, d3-geo, world-atlas
    pip install faster-whisper             # only for picking the non-English stretch of a recording
    python3 fetch_audio.py [video ...]     # downloads + cuts clips -> cache/audio/<video>/ (polite: Commons rate-limits)
    node render.mjs <video> --still 3,12   # check frames -> out/<video>_<seg>_<t>s.png
    node render.mjs <video>                # full video -> out/<video>.mp4
    node brand.mjs                         # avatar, banner, thumbnails -> out/brand/

Chromium path: `CHROMIUM=/path/to/chrome` (defaults to the cloud container's Playwright Chromium). On Windows use
the installed Chrome, e.g. `set CHROMIUM=C:\Program Files\Google\Chrome\Application\chrome.exe`.

## Files
- `videos.mjs`: all scripts (names, speaker counts, 3 fact cards per language, character design, scene, map pin, audio source).
- `art.mjs`: procedural vector characters (skin, hair, headwear, traditional clothing, expressions) and 40 landscape presets.
- `render.mjs`: HTML/SVG page per segment, animated by `setT(t)`, screenshotted per frame by headless Chromium, piped to x264; then audio mix.
- `fetch_audio.py`: Commons API -> download (small transcodes for videos) -> Whisper language-ID to skip English intros -> loudness-normalised clip + credits.
- `brand.mjs`: channel avatar, banner, thumbnails.

## Status / handover
See the "LingoDude" section in the repo's `CLAUDE.md`.
