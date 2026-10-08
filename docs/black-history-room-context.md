# Context: Facebook Reels for "The Black History Room"

Saved 2026-10-05 from the chat so the next session can pick up without the conversation.

## Where the work is
- **All reel code, specs, images and finished MP4s are on branch `claude/funny-bohr-xrel88`** (anaqqad/Test),
  not on this branch. Read its `README.md` ("Reels" section) and `CLAUDE.md` first.
- The pipeline was copied from `anaqqad/Youtube-Automation` (MathDoc, branch `claude/ecstatic-turing-j7jqd8`)
  into this repo at the same paths (`src/`, `scripts/`, `data/`, `public/`). The owner chose "copy into Test".
- Branch `claude/black-history-reels-4pk8ts` (this one) only holds the Blender globe shot plus this note.

## Reels made so far (on `claude/funny-bohr-xrel88`)
| Reel | Spec | MP4 | Post text |
| --- | --- | --- | --- |
| Robert Smalls (pilot) | `data/reel-robert-smalls.json` (18 beats) | `publish/video/Robert-Smalls-reel.mp4` | `publish/reels/robert-smalls.md` |
| Bessie Coleman | `data/reel-bessie-coleman.json` (16 beats) | `publish/video/Bessie-Coleman-reel.mp4` | `publish/reels/bessie-coleman.md` |
| Black Boston, Then and Now | `data/reel-boston-then-now.json` | `publish/video/Black-Boston-Then-and-Now-reel.mp4` | - |
| Boston Then and Now (Boston Before Us page) | `data/reel-boston-before-us-then-now.json` | `publish/video/Boston-Then-and-Now-BostonBeforeUs.mp4` | - |
| Matthew Henson | `data/reel-matthew-henson.json` (14 beats) | `publish/video/Matthew-Henson-reel.mp4` | below (not yet in a file) |

Measured on the cloud VM: Smalls narration 904 ElevenLabs characters, Coleman 914, Henson 923; Henson reel
61.5 s with 12 different photos, passes every QC check. Final render ~174 s for 58.5 s of video (4 CPU, no GPU).
The last request was "stop at one reel" (Henson); nothing is in progress.

### Matthew Henson post text (delivered in chat)
Title: The Explorer History Almost Forgot: Matthew Henson

Description:
> In 1909, he stood near the top of the world, and history almost forgot him.
>
> Matthew Henson was born in Maryland in 1866 and went to sea as a cabin boy. In 1887 he met the explorer
> Robert Peary, and together they made seven expeditions to the Arctic. Henson learned the Inuit language and
> became an expert dog-sled driver. On April 6, 1909, Peary's team said they had reached the North Pole, and
> Henson was there. Whether they reached the exact Pole is still debated.
>
> Peary got the fame. Henson spent decades as a clerk in New York. In 1937 the Explorers Club finally made him
> a member, and in 1988 he was reburied at Arlington National Cemetery, near Peary.
>
> Had you heard of Matthew Henson before today?
>
> Sources: Bowdoin College Peary-MacMillan Arctic Museum; National Geographic; BlackPast; National Archives.
>
> #BlackHistory #MatthewHenson #NorthPole #Explorers #HiddenHistory

Tags: Matthew Henson, Black history, North Pole, Arctic explorer, Robert Peary, 1909 expedition, Explorers Club,
Arlington National Cemetery, hidden history, African American history, history shorts

## The original brief (summary)
- Page: The Black History Room, "Sharing powerful people, moments, struggles, achievements from Black history".
- Format: 1080x1920, 30 fps, 45-75 s, `"format": "reel"` specs voiced by `scripts/tts_mathdoc.py`, composition
  `Reel` in `src/Root.tsx`.
- Captions from `timeline.json`: 2-4 words at a time, large serif, cream, spoken word in gold (most watch muted).
- Photo-led: Ken Burns on archival photos, warm sepia; palette black, cream, gold.
- Blocks: lower third (name, year), map pin, year counter, newspaper-clipping card, bold hook text, end card
  "Follow The Black History Room for one story a day."
- Safe zones: nothing important in the bottom 20 % or right 15 % (QC: `scripts/qc_reel.py`). Frame 0 = cover still.
- Audio: music quieter than YouTube videos, master at -14 LUFS.
- 60 s structure: hook 0-1.5 s over a tight face crop; who/when/where to 8 s; story 8-40 s (8-12 beats, one
  fact each, new picture every 1.5-3 s); twist or cost 40-52 s; legacy line 52-58 s; follow request 58-60 s,
  cut to loop. Script 140-170 words.
- Deliverables per reel: `out/reel-<slug>.mp4`, a <30 MB copy for chat, hook and caption stills,
  `publish/reels/<slug>.md` (hook line, 2-3 sentences, easy question, sources, 3-5 hashtags, cover suggestion),
  short report (render time, what was verified and how, open questions).

## Voice
- **Owner, 2026-10-08:** the published reels (Box Brown, Ellen Craft, Tubman) use the free Kokoro voice (`am_michael`, speed 1.1). Kokoro is the default final voice; do not ask about ElevenLabs unless the owner asks for Andrew.
ElevenLabs "Andrew" (same block as the Sand video). This page uses Andrew; the Ink & Infinity YouTube channel
uses the owner's cloned CosyVoice voice and never ElevenLabs.
```json
"voice": { "engine": "elevenlabs", "voiceId": "gUABw7pXQjhjt0kNFBTF",
  "voiceName": "Andrew - Smooth audio books", "model": "eleven_multilingual_v2",
  "stability": 0.6, "similarity": 0.75, "style": 0.0, "speed": 1.05, "seed": 1234,
  "leadInSeconds": 0.3, "sectionGapSeconds": 0.5 }
```
Free timing previews: Kokoro scratch (`am_michael`, speed 1.1), spec id ending in `-scratch` (git-ignored).

## Rules (must follow)
- Facebook post text: the story part is long (about 250-350 words, several short paragraphs: background, the event step by step, the aftermath), built only from facts in the reel's fact sheet (two sources each). Owner, 2026-10-07.
- Every Facebook post description includes this support line (after the question, before the sources):
  "Researching and editing these videos takes real time and effort. If you value these stories, please support our page so we can keep bringing them to light. Thank you! https://ko-fi.com/theblackhistoryroom"
- Every Facebook post description ends (before the sources) with:
  "Researching and making these videos takes a lot of time. If you value these stories, please consider supporting our page so we can keep bringing them to light. Thank you!"
- ElevenLabs is paid: ask before every call and give the character count (~1,000 per 60 s reel).
- Every fact needs two independent sources (LoC, National Archives, NMAAHC, US House history, NPS, scholarly
  biography...). Sources go in the post text, not the video.
- No unverified quotes (many Tubman/MLK/Douglass quotes are fake). Label legends as legends.
- Real archival photos only, public domain or CC0, credit recorded in `public/pd/<id>/credits.json`.
  Never AI-generated faces of real people.
- No graphic violence: tell those stories with documents, places and faces.
- In reports label claims [M] measured, [V] visually checked, [E] estimate.
- Never print or commit API keys. Never commit `voices/`.
- Push only to the session's assigned branch; no PR unless asked.

## Lessons from the pilot
- **Hook rules (owner, 2026-10-06, from comparing two Story Room reels):** the reel that failed opened with low
  sound on a shot of a hand; the one that worked opened on a crying face with a line spoken at once. So:
  1. The hook is *heard* from the first instant: `voice.leadInSeconds: 0`, `mix.hookBoostDb: 2` (the hook beat
     2 dB above the rest of the voice). QC `audibleHook`: voice by 0.15 s, first 3 s >= whole reel - 1 LU.
  2. Frame 0 is a tight crop on the most striking thing: the face and its expression, never a hand, a wide
     shot or empty sky. (QC `coverFrame` checks a face is on frame 0.)
  3. The first spoken line is the crazy part, short and direct, stated or asked as a question to the viewer.
     No invented dialogue: only real, verified quotes may be spoken as quotes.
- End card and title cards are centred on the frame (CENTER_COL, x 162-918), not on the caption safe column,
  which looked off-centre on YouTube (owner, 2026-10-06). Captions, pins and stamps stay in the safe column.
- **Hook = views.** Owner, 2026-10-05: the Robert Smalls reel got by far the most views because its first
  seconds say something shocking ("In 1862, an enslaved man stole a Confederate warship."). Bessie Coleman
  ("She learned French to learn to fly") did worse because nothing shocking is said in the first 5 s.
  Every reel must open with a jaw-drop line in the first 1-2 s: who + an unbelievable act, stated plainly.
- Tight hook crops can push the face into the right 15 %; group engravings put faces in the bottom/right zones;
  overshoot animations (date stamp) can poke into the right edge. The safe-zone QC catches these.
- The greedy caption chunker stranded one-word chunks ("Smalls."); it was replaced by a balanced chunker that
  splits at punctuation/pauses (TS and Python versions kept identical).
- QC can pass while the contact sheet still shows problems (cut-off map label, low label contrast on beige land,
  pin colliding with captions, an empty-sky shot): always look at the contact sheet too.

## Ideas for later reels
Series: Forgotten First, Before Rosa Parks, One Photo One Story, Invented By, Myth vs Fact.
Candidates not yet done: Claudette Colvin (2 March 1955), Garrett Morgan (1916 Lake Erie tunnel rescue),
Henrietta Lacks (handle consent carefully), Major Taylor (1899 world cycling champion), Katherine Johnson,
Lewis Latimer, Madam C. J. Walker (word the "first" claim carefully).
Done: Robert Smalls, Bessie Coleman, Matthew Henson. Waiting for Andrew voice: Henry "Box" Brown, Ellen and William Craft, Harriet Tubman (Combahee raid), Mansa Musa (branch claude/black-history-reels-4pk8ts).
