# BLUEPRINT 03 — DISCORD CHAT COMEDY

The third LingoDude production blueprint:
- **01 Normal Videos:** the `lingodude-video-method` skill.
- **02 Map Videos:** `MASTER_VIDEO_BLUEPRINT.md`, with the language layer in `LANGUAGE_VIDEO_BLUEPRINT.md`.
- **03 Discord Chat Comedy:** this file.

It turns a one-sentence premise into a **long-form 16:9 chat-screen comedy (1920×1080, about 1:30–3:00)**. That's the owner's default, matching the reference. A vertical Short is possible with `"width": 1080, "height": 1920`. The mechanics are reverse-engineered from a Beluga video. The characters, dialogue, jokes, avatars, sound effects and chat look are our own.

**Tools.** Renderer `lingo/chat.mjs`, mixer `lingo/chat_audio.py`, sound-effect generator `lingo/chat/make_sfx.py`. Episodes go in `lingo/chat/episodes/<key>.json`. The pilot episode is `roles`.

**Labels used in this document.**
- **[Measured]:** taken from the file with ffmpeg or numpy.
- **[Observed]:** seen in frames sampled every 0.25 s or 0.5 s.
- **[Estimated]:** judged by eye from frames.
- **[Unverified]:** can't be settled from the file.

---

## 1. Audit of the reference

**Reference:** `videoplayback_14.mp4`, a Beluga video about Netflix password sharing.
- **Format:** 640×360, 30 fps, H.264/AAC, 3:04.8 [Measured]. The story runs 0:00–2:53.8. A plushie advert follows from 2:53.8 to 3:04.8.
- **Cast:** skittle (a dog in a helmet), Beluga (a cat), a famous-scientist cameo, and a "Netflix CEO" character.

**How it was analysed.**
- **Frames:** every 2 s across the whole video, plus every 0.25–0.5 s for 0:00–0:20, 1:16–1:44 and 2:40–3:00.
- **Hard cuts:** ffmpeg scene score above 0.25.
- **Reveal events:** scene score above 0.004 on a 160×90 copy, merged within 0.3 s.
- **Audio:** RMS loudness every 50 ms, silences quieter than -50 dB, spectrograms of 0–20 s and 1:16–1:36, and Whisper speech recognition.

### 1.1 Measured rhythm
- **Hard cuts:** 21 before the advert [Measured]: 0.07, 18.9, 26.3, 51.1, 64.1, 71.2, 79.6, 82.4, 83.8, 88.3, 89.6, 90.9, 92.7, 95.9, 102.9, 103.6, 134.4, 172.1, 173.8, 176.2, 177.5 s. All other changes happen inside the same chat look: a line appears, or the frame changes size.
- **Reveal events:** 198 before the advert, about **59 per minute, one roughly every second** [Measured]. Gap between events:

  | Percentile | Gap |
  |---|---|
  | p10 | 0.53 s |
  | p25 | 0.77 s |
  | p50 (median) | 1.03 s |
  | p75 | 1.30 s |
  | p90 | 1.50 s |

- **Lines inside one message:** a new line every **0.5–1.0 s** [Observed at 0.25 s steps]. Example from 0:05–0:07.25: "but" at 5.0 s, "we sit" at 5.75 s, "next to each other" at 6.25 s, "in class" at 7.25 s.
- **Deadpan one-word replies** ("no", "and?", "idk", "sorry"): on screen for **0.75–1.25 s** [Observed].
- **Speech:** none during the story [Measured: Whisper hears only the advert line at 2:57–3:00]. All dialogue is text.
- **Loudness:** median about -20 dBFS (50 ms RMS). No peak above -6 dBFS [Measured].
- **Silences:** 48 stretches of at least 0.3 s, median 0.75 s, longest 1.25 s [Measured]. In the first 20 s, every silence sits under one of Beluga's flat replies: 4.45–5.1, 9.15–10.0, 13.95–15.0 and 19.2–19.8 s [Measured and Observed].

### 1.2 Beat table

Columns: C = comedy, T = chat timing, E = editing, S = sound.

| Time | Beat | C | T | E | S |
|---|---|---|---|---|---|
| 0:00.0–0:01.25 | skittle: "@Beluga" | **Hook.** A ping summons the straight man. There's a conflict before any context. | One line, 1.25 s [Observed] | Message highlighted yellow with a left bar (mention style) | Music bed plus a message pop [Measured/Observed] |
| 0:01.25–0:01.75 | Beluga: "sup" | Straight man, low energy | 0.5 s | New frame | — |
| 0:01.75–0:04.25 | skittle: "can i use your netflix? / mine expired 😭" | **Premise stated by 0:04** | Lines at 1.75 and 2.75 s | Frame changes size | Music continues |
| 0:04.25–0:05.0 | Beluga: "no" | **First rejection**, deadpan | 0.75 s | Tight frame | **Silence 4.45–5.1** [Measured]. The music cut is the laugh. |
| 0:05.0–0:08.75 | skittle: "but / we sit / next to each other / in class" | Pleading builds one line at a time | Lines 0.5–1.0 s apart | A small reframe on each line [Estimated] | Music back, plus a pop on each line [Observed in spectrogram] |
| 0:08.75–0:10.0 | Beluga: "and?" | Rejection 2 | 1.25 s | — | Silence 9.15–10.0 [Measured] |
| 0:10–0:13 / 0:13–0:15 | "i always let you / copy / my homework" / "idk / what ur talking about" | Leverage, then denial (rule of three) | Lines about 0.75 s apart | — | Music, then silence 13.95–15.0 [Measured] |
| 0:15–0:19 / 0:19–0:26 | "please / help a brother out / gimme / your netflix password" / "sorry / but / i cant share that / password sharing is against the rules" | The stakes are named: rules | 4 lines each | **Hard cut at 26.3: full-width zoom on "against the rules" alone** [Measured cut] | — |
| 0:26–0:51 | "who cares lol" / "netflix does" / "they will find out / they always do / trust me" / "ive heard stories…" / "that's how they kidnap you" | Escalation: the straight man's claims get absurd | 1–4 lines | "they will" at 0:34 is framed larger [Observed] | Music under skittle, silence under Beluga |
| 0:56–1:11 | "rules are meant to be broken – albert einstein" → Einstein: "I never said that." → "'i never said that' – albert einstein" → Einstein: "I said that." → "see?? @Beluga @Beluga @Beluga" | **Absurd cameo**: a new character appears in the chat to settle a quote. Then **ping spam**. | — | Hard cuts at 64.1 and 71.2 [Measured] | Cameo entrance on its own cut |
| 1:12–1:21 | "fine i will give u" / "YESSS" / "just promise you wont share it with anyone else ok?" / "i promise 🤞" | **Reversal**: he gives in. The 🤞 emoji plants the betrayal. | "YESSS" framed large | — | — |
| 1:21–1:25 | Credentials (blurred) → **phone notification** insert: "A new device is using your account" | First consequence | — | **Insert at 82.4** [Measured cut] | **Notification chime**: decaying tone at about 82.6–83.6 s [Observed in spectrogram] |
| 1:26–1:30 | "@everyone FREE NETFLIX 👇👇👇 email: … password: …" | **Betrayal and callback** to the promise | — | Mention highlight | — |
| 1:30–1:36 | Notification again → inbox flooded with alerts → member list scrolls past "Online — 3" to reveal **"Netflix CEO — 1"** | **Escalation by consequence** | — | Inserts: hard cuts at 89.6, 90.9 and 92.7. Member-list scroll, then zoom. | A busy new music bed, 88.4–92.7 [Observed in spectrogram] |
| 1:36–2:13 | The CEO character interrogates Beluga: "147 households" / "i own 147 homes", "23 languages" / "i speak multiple languages… 24 actually" | **Call and response**: each piece of evidence gets a worse excuse | Short lines, about 1–1.5 s each | Avatar close-up insert at 102.9 | Music returns under the accuser |
| 2:14–2:16 | "Did you share your password?" | The question, isolated | — | **Full-width zoom, hard cut at 134.4** [Measured] | — |
| 2:16–2:50 | "definetely not" / "Ok. I believe you 😊" / "Btw- how did you react when Gerald died?" … "Gerald was my favorite character" / "i was so sad when he died / RIP gerald" | **Trap**: a fake show tests whether he really watched it | — | — | — |
| 2:48.5–2:51.5 | "Gerald never died." / "But you will 😊" | **Final punchline at about 92% of the story** | Held about 1.5 s [Observed] | — | — |
| 2:51.5–2:53.8 | "WAIT / I CAN EXPLAIN-" → profile card. The status icon turns to offline. | Tag gag: he's gone | — | Hard cut at 172.1, profile card zoomed in [Measured cut] | — |
| 2:53.8–3:04.8 | Plushie advert | (not part of the format) | — | — | The only spoken voice [Measured] |

### 1.3 What makes it work
1. **One message per shot, shown big.** There's no scrolling history. The viewer reads exactly one thing at a time, and the frame size changes with every message.
2. **Lines appear one at a time.** A long message is a drumroll, and the last line is the punchline.
3. **Music under the needy character, dead silence under the deadpan one.** The silence *is* the rimshot, measured at 0.6–1.15 s.
4. **Every 15–25 s the situation changes:** ask → refusal → leverage → reversal → betrayal → authority arrives → trap → doom.
5. **Plants and callbacks:** 🤞 → "@everyone FREE NETFLIX". The promise → the betrayal. The "Online" list → "Netflix CEO — 1".
6. **Inserts as consequences:** a phone notification, a flooded inbox, the member list, a profile card. Each is a hard cut. Everything else is chat.
7. **A recurring structure:** a request, a run of excuses each worse than the last, a bigger authority, a trap, a final threat.

### 1.4 What still needs checking
- **Exact sound effects:** which files they used, and whether the message pop is 1 or 2 tones. The spectrogram shows short paired tonal blips at about 1.0–1.3 kHz, so the pop is likely 2 tones. Listening by ear would confirm. [Unverified]
- **Music:** the titles and any per-character theme. The first-20 s spectrogram shows a plucked pattern from 0 to 4.4 s and held chords from 5.1 s, so tracks may change per turn. [Unverified]
- **Zoom amounts:** about 1.0–1.35× per message, judged from avatar size [Estimated]. The source is 640×360, so sub-pixel motion and ease curves can't be measured.
- **Typing indicators:** none seen in the sampled frames. Frames between samples weren't checked.
- **Do not copy:**
  - the reference uses a real executive's photo and a real company's brand;
  - **we never use real people's faces or real company logos.**

---

## 2. Inputs and defaults

| Input | Default | Notes |
|---|---|---|
| Premise | (required) | One sentence. A character misunderstands something about the chat, or wants something they shouldn't get. |
| Key | a short slug from the premise | Becomes `chat/episodes/<key>.json` and `out/chat_<key>.mp4` |
| Target duration | **1:30–3:00** (long-form) | The reference story is 2:53.8 (3:04.8 with its ad). A Short is 30–40 s with one loop per act. |
| Aspect ratio | **1920×1080** horizontal, 30 fps (owner, 2026-11-17: "long form size, not short size") | Vertical Short: `"width": 1080, "height": 1920` |
| Cast | 3–4 | A chaos character (music), a straight man (silence), an authority who arrives late, an optional bot as narrator of consequences |
| Avatars | Calm Wojaks from `lingo/wojaks/`, or our own SVGs (`chat/assets/avatars/`) | Never real people's photos, never brand logos |
| Tone | Friendly absurd, PG-13 at most | Laugh at misunderstandings, never at nationalities or groups |
| Ending | A callback punchline from the chaos character, held 1.5–2 s | Optional tag gag (panel, profile, goes offline) placed *before* the last line |
| Music | One real, credited CC track (Kevin MacLeod on Commons) | Channel rule: no generated music. It plays only under music beats. |
| Sound effects | `chat/assets/sfx/*.wav` | Made by `chat/make_sfx.py`: our own synthesised UI sounds, no speech, no music |
| Language | English | For language episodes, real words that need pronouncing use real recordings, as in Blueprint 02 |

---

## 3. Script structure: premise to beats

Write in this order. Each step is 1–3 messages. **Long-form: 55–75 beats in 3 acts for 1:30–2:30.** Each act has its own escalation loop of three, its own deadpan foil and a new insert (panel, timeout, boost). Act 3 brings the authority with its own music bed and a trap question. Short: 18–22 beats for 30–40 s.

| Step | Share of runtime | Purpose | Rule |
|---|---|---|---|
| 1. Ping hook | 0–1.5 s | Someone is summoned, welcomed or mentioned. Highlighted message plus ping. | The weird line must land **by 2 s** |
| 2. Premise line | to about 4 s | The chaos character says the misunderstanding out loud | One message, 2 lines, with the punchline on line 2 |
| 3. Deadpan | about 1 s | The straight man answers in 1–4 words | Silence under it |
| 4. Escalation loop × 3 | 60–70% | Each loop: **a new fact arrives** (bot action, notification, a new character) → chaos overreacts → straight man deflates it | Every loop must change the situation (rule of three). The third loop is the biggest. |
| 5. Reversal | about 10% | The straight man reveals the truth, or the chaos character's plan backfires | Use a typing indicator (0.6–1 s) before it, and 0.6–0.8 s between its lines |
| 6. Authority / consequence | about 10% | Someone higher appears (owner, CEO, "everyone"): a ping, a sound effect, a record scratch | A new character, or a new insert (panel, notification) |
| 7. Callback punchline | last 2–3 s | The chaos character turns the consequence into the premise's logic | Held **1.5–2 s**. Nothing after it except the 0.5 s tail. |

**Character voices.**
- **Chaos character:** lowercase, typos allowed, all caps for panic, emojis.
- **Straight man:** lowercase, 1–4 words, no emojis.
- **Bot:** title case, system wording, role pills.
- **Authority:** proper punctuation and capital letters ("Ok. I believe you 😊" is scarier than "ok").

**Joke checks.**
- Every message is either a setup or a payoff. Cut anything that's neither.
- Plant something for the ending in the first third: a word, an emoji or a role.

---

## 4. Production format: the episode file

`lingo/chat/episodes/<key>.json`. The renderer computes all times. You only write beats.

```jsonc
{
  "title": "…", "premise": "…", "clock": "12:01",             // the timestamp starts here and goes up 1 minute every 4 beats
  "music": { "file": "chat/assets/music/fluffing_a_duck.ogg", "gain": -17, "start": 2.0,
             "credit": "\"Fluffing a Duck\" by Kevin MacLeod (incompetech.com), CC BY 3.0, via Wikimedia Commons" },
  "timing": { "lineGap": 0.42, "holdBase": 0.55, "holdPerChar": 0.03, "readPerChar": 0.045, "minHold": 0.7 },  // optional overrides
  "cast": {
    "trevor": { "name": "trevor", "role": "New Member", "roleColor": "#99aab5", "color": "#f2f3f5",
                "avatar": "wojaks/s_eng_calm.png", "avatarBg": "#e0b04a", "music": true },   // music: true marks the chaos character
    "bot":    { "name": "RoleBot", "bot": true, "avatar": "chat/assets/avatars/rolebot.svg" }
  },
  "beats": [
    { "who": "bot", "lines": ["Welcome @trevor! 🎉", "Your role: [[Member|#99aab5]]"], "ping": true, "firstSfx": "join" },
    { "who": "trevor", "lines": ["OMG I GOT THE JOB", "when do i get paid"] },
    { "who": "maya", "lines": ["what job"] },
    { "who": "trevor", "big": "TIME OF DEATH: 12:04", "shake": true, "sfx": ["boom"], "hold": 1.1 },
    { "who": "maya", "lines": ["trevor", "nobody gets paid"], "typing": 0.8, "lineGap": 0.7, "zoom": 1.06 },
    { "who": "trevor", "panel": { "header": "UNEMPLOYED — 1", "rows": [{ "who": "trevor" }] }, "hold": 1.1, "music": false }
  ]
}
```

**Beat fields.**

| Field | Meaning |
|---|---|
| `who` | Who speaks. |
| `lines` | One line appears per `lineGap`. Inline markup: `@name` (mention chip), `#channel` (channel chip), `[[Label\|#hex]]` (role pill), emojis. |
| `big` | One phrase, full width. The reference's "against the rules" shot. |
| `panel` | A member-list insert, e.g. "UNEMPLOYED — 1". |
| `ping` | Yellow highlight plus a ping sound. |
| `typing` | Seconds of "X is typing…" shown before the beat, over the previous message. |
| `pause` | Extra silence before the beat. |
| `hold` | Fixed hold after the last line. |
| `zoom` | 1.0–1.08. |
| `shake` | Shakes the frame for 0.4 s. |
| `music` | Overrides the speaker's default. |
| `sfx` | Extra sounds: `boom`, `scratch`, `ping`, `role`, `join`, `typing`. |
| `firstSfx` | Replaces the first line's pop. |

**Automatic timing rule:**
```
end = max(lastLineTime + max(minHold, holdBase + holdPerChar * len(lastLine)),
          start + 0.3 + readPerChar * len(allText))
```
Long-form defaults (`lineGap` 0.6, `holdBase` 0.7) sit inside the reference's 0.5–1.0 s per line and 1.03 s median between events. For a Short, use `lineGap` 0.42 and `holdBase` 0.55.

**Sample timeline: the pilot.** Output of `node chat.mjs roles --timeline`. ♪ means the music bed plays.

```
0.10-1.30   bot       Welcome @trevor! 🎉 / Your role: @Member
  1.30-3.22   trevor  ♪ OMG I GOT THE JOB / when do i get paid
  3.82-4.76   maya      what job
  4.76-6.57   trevor  ♪ it says MEMBER / do i get dental??
  6.57-8.47   maya      trevor / this is a group chat
  8.47-10.01  bot       @trevor is now: / @Chef 🍳
 10.01-12.51  trevor  ♪ WAIT / i can't cook / i burned cereal once
 12.86-14.07  maya      it's just a color
 14.07-16.27  trevor  ♪ so i'm a chef / who can't cook / in a color
 16.27-17.36  maya      basically yes
 17.36-18.96  bot       @trevor is now: / @Doctor 🩺
 18.96-21.20  trevor  ♪ someone in #general is dying / do i operate??
 21.80-23.09  maya      he lost a video game
 23.09-24.39  trevor  ♪ [BIG] TIME OF DEATH: 1:31
   … (64 beats in total: act 2 = meeting, timeout, HR, boost; act 3 = Greg, trap question, firing)
 95.67-97.00  trevor  ♪ I DON'T EVEN GET PAID
 97.00-98.03  greg    ♪ Exactly. 😊
 98.03-99.66  bot       @trevor is now: / @Unemployed
 99.66-100.86 trevor    [PANEL] UNEMPLOYED — 1
100.86-103.56 trevor  ♪ finally / a job i'm qualified for
duration 104.16 s, 64 beats
```

---

## 5. Rendering workflow

There are no Remotion components in this project. The renderer uses the same Playwright frame capture plus ffmpeg as `render.mjs`.

1. **Sound effects:** only once, or after editing the generator.
   ```
   cd lingo && python3 chat/make_sfx.py
   ```
2. **Music:** a CC track from Commons, downloaded into `chat/assets/music/`. Commons rate-limits scripts (HTTP 429), so fetch `Special:FilePath/<name>` through headless Chromium if needed. Put its credit in `music.credit`.
3. **Timeline check:**
   ```
   node chat.mjs <key> --timeline
   ```
   Check the total length, when the hook lands (2 s or less), and that ♪ alternates with silence.
4. **Stills at phone size:**
   ```
   node chat.mjs <key> --still 1.5,10,30,60,90
   ```
   Then view them at 270–360 px wide.
5. **Full render:**
   ```
   node chat.mjs <key>
   ```
   - It renders the episode size (default 1920×1080) at 30 fps. A 104 s episode takes about 3 minutes.
   - It writes `out/chat_<key>_timeline.json`.
   - `chat_audio.py` mixes music windows (with 25 ms fades; the music keeps its place between windows) and sound effects.
   - ffmpeg muxes AAC 192k. Loudness is two-pass: the mix is measured with `ebur128`, then one fixed gain and a limiter are applied (the pilot measures -15.4 LUFS).
   - A 32 s episode takes about 55 s to render.
6. **How the effects work:**
   - **Line reveals:** CSS visibility per line.
   - **New message:** a 0.12 s scale pop from 0.965 to 1, plus a 1.2% re-pop on every new line.
   - **Slow push:** +3% across each beat.
   - **Vertical offset:** each beat sits up to ±70 px from centre (deterministic random).
   - **Shake:** ±11 px for 0.4 s.
   - **One message per shot**, like the reference.
   - **Discord look (owner, 2026-11-17: "match the style"):**
     - one grey message band (#36383e) across the full width on near-black;
     - round avatar, bold name in the role colour, small grey timestamp ("1:28 PM"), no role pills in the header;
     - a blue **BOT** tag for bots;
     - mentions as blue-purple chips; roles as coloured `@Role` mentions (`[[Doctor|#e91e63]]`);
     - a mentioned message gets a yellow tint and a gold left bar;
     - **camera re-fit:** each message is scaled so it fills the frame (short replies up to 3.1×, panels and big text up to 4×). It eases to a new fit over 0.15 s whenever a line arrives, like the reference re-framing on every line;
     - **typing row (owner's screenshot, 2026-11-17):** a darker strip *inside the bottom of the current message box*, scaled with it. Three dots (grey, grey, white, with the white one cycling) and "**name** is typing...". It shows over the previous message for 0.5–1 s before key replies.
     - **timestamps** read "Today at 8:02 AM" (`dayLabel`, `ampm` and `clock` in the episode file).
7. **Deliver:**
   - Copy to `lingo/videos/chat_<key>.mp4`.
   - The description credits the music, says "Characters drawn for LingoDude", and has no AI voice.
   - Settings: not made for kids; altered/synthetic content: No.

---

## 6. Sound rules
- **Music** plays only under music beats: `true` uses the default track, and a name such as `"boss"` uses that track. Normally the default plays under the chaos character, and the authority gets their own track when they take over (the reference switches the music bed when the CEO appears). Deadpan beats get **silence**, the reference's main trick. Keep music about 15–17 dB below the sound effects.
- **Message pop = the Discord notification sound (owner, 2026-11-17: "use the Beluga one").**
  - The owner supplied it from myinstants.com ("discord-notification.mp3"). It's the same sound the reference uses: 393/587 Hz, then 781/522 Hz, about 165 ms.
  - Trimmed to start on the line (the file has 130 ms of silence before the sound) and saved as `chat/assets/sfx/discord_pop.wav`. It's the default line sound (`popSound` in the episode file; `"pop"` is our own synthesised look-alike).
  - It's third-party audio (Discord's), used at the owner's request. If YouTube ever claims it, set `"popSound": "pop"`.
- **Balance as in the reference:**
  - The reference's pop RMS is -16.5 dB against music around -20 dB, so the pop is about 3.5 dB above the bed, and the story plays at -14.8 LUFS.
  - `chat_audio.py` sets each effect relative to the measured music RMS: pop and ping +3.5 dB, role and join +3 dB, boom +5 dB, typing -14 dB.
  - `chat.mjs` then applies one gain to reach -14.8 LUFS.
  - In the class episode: the pop is +2.6 dB over the music, typing sits at -38 dB, and the whole mix is -14.3 LUFS.
- **Sound kit like Beluga's (owner, 2026-11-17):**
  - 16 meme sound effects in `chat/assets/sfx/meme/`: vine_boom, bruh, crickets, huh, discord_join/leave/call, record_scratch, sad_trombone, dun_dun_dun, metal_pipe, ding, boing, wait_what, anime_wow, bong. Sources are in `chat/assets/sfx/SOURCES.md`.
  - Use one on most punchlines: `"sfx": ["vine_boom"]`.
- **Music by mood, not one track:**
  - `"music": {"silly": …, "awkward": …, "sad": …}` in the episode file.
  - Any beat can set `"mood": "sad"`, which switches the track for the following music beats.
  - Every track is levelled to -21 dB RMS. The pop sits about 4 dB above that, and there's no loudness boost afterwards (owner: "the music is so loud it hurts").
  - The class episode measures music -19.3 dB, pop -17.0 dB, overall -19.3 LUFS.
- **Typing sound (owner: "less noisy"):** three soft, low-passed taps, far under the dialogue.
- **Pop on every line.** Ping for mentions. Chime when a bot gives a role. Join chime for arrivals.
  - **Boom:** only on the biggest escalations (2–3 per long-form video).
  - **Record scratch:** only on the authority's entrance or the reversal.
  - **Typing clicks:** only under a typing indicator.
- No speech and no AI voices in this format. If a language episode needs a word pronounced, use a real credited recording (Blueprint 02 rules).

## 7. Quality check (watch at phone size with sound)
1. **Hook by 2 s:** the first weird line is on screen at 2.0 s or earlier.
2. **Readable on a phone:**
   - message text at least 70 px at 1080 width;
   - no line that leaves a single word alone;
   - every message stays up at least `0.3 s + 0.045 s × characters`.
3. **Every beat changes the situation.** Point to each beat in turn. If removing it changes nothing, cut it or rewrite it into a new fact.
4. **Rhythm:** a new event about every 1 s (the reference's median is 1.03 s), and no single frame held longer than 2.5 s except the punchline.
5. **Sound:**
   - silence under every deadpan line;
   - music returns on the chaos character;
   - no clipping;
   - integrated loudness -14 to -16 LUFS.
6. **The punchline gets room:** held 1.5–2 s, a callback to something planted in the first third, nothing after it.
7. **Safe and original:**
   - no real people's photos, no app logos, our own chat look;
   - jokes about misunderstandings, not about groups;
   - music credited.
8. **Name the weakest beat**, rewrite it, and re-render before final export.

**How to watch "at phone size with sound" in a cloud session:**
- **Frames:** sample at 2 fps, scale to 270 px wide, and tile them into one image.
- **Audio:** look at a spectrogram (`showspectrumpic`) to see the music and silence pattern, and run `ebur128` for loudness.
- **On a real phone, the owner checks:** the timing of the jokes by ear.

## 8a. Language episode: `class`, "English Teacher vs Her Foreign Students (Group Chat)" (owner, 2026-11-17)
- **Topic (owner):** learning languages. A teacher and her foreign students; every joke is a real false friend:
  - German "bekommen" = get (not "become"), German "Gift" = poison;
  - Spanish "constipado" = having a cold, "embarazada" = pregnant;
  - Japanese "manshon" = an apartment building;
  - French "assister" = attend.
- **Cast and sound:** the teacher is the straight man (silence). The students are chaos (default music). Principal Weber gets the "boss" track and makes the same "become" mistake (a twist callback).
- **Ending:** "OFFLINE — 1" panel, then "she is very constipated" (callback).
- **Final:** 1:31, 48 beats, 1920×1080, -16.5 LUFS. File: `lingo/videos/teaching_foreign_students_english_be_like.mp4` (title: "Teaching Foreign Students English be like…").
- **Fixes from the review:**
  - long single lines were shrunk tiny, so they're now split into short lines, as in the reference;
  - a line ran off the frame during re-fit, so the zoom is now clamped to the frame width.
- **Weakest beat:** "Rude!" after Pierre's "i will not assist your presentation". It became "I didn't ASK for your help, Pierre." (the misunderstanding sets up his correction).
- **Writing rule learned:** keep each line to about 28 characters or less. Longer lines force the camera to zoom out until the text is small.

## 8. Pilot record: `roles`, "New Member Thinks Server Roles Are Real Jobs"

- **First render:** 34.3 s. Problems found at phone size:
  1. Text too small for a vertical screen (58 px) → raised to 76 px, and avatars cropped to the face.
  2. "TIME OF DEATH" overflowed the left edge while shaking → the big font went from 150 to 124 px, with smaller shake.
  3. "@trevor got a new role:" left "role:" alone on a line → changed to "@trevor is now:".
  4. The hook joke landed at 2.06 s → the welcome is faster, and the joke now lands at 1.2 s.
- **Weakest beat:** "MEMBER / it says it right there". It repeated the premise and nothing changed. Rewritten as "it says MEMBER / do i get dental??", which escalates the job fantasy into benefits.
- **Version 1 (vertical Short), final:** 32.06 s, 20 beats, 1080×1920, -16.3 LUFS. The deadpan silences show in the spectrogram at each Maya line.
- **Version 2, long-form (owner, 2026-11-17):** the owner asked for long-form size and a closer Discord style.
  - Re-rendered at 1920×1080 and expanded to 3 acts: 1:44, 64 beats, -15.4 LUFS.
  - Added: camera re-fit, a Discord typing bar, role mentions, a "boss" music track under Greg, and the trap question "What is the name of this server?" → "Dental Plans Incorporated" (a callback).
  - Fixes from the phone-size review:
    - emoji moved out of role mentions;
    - member-list panels shown big;
    - a bigger typing bar;
    - two-pass loudness (-22.4 → -15.4 LUFS).
  - **Weakest beat:** "a group chat / with dental" → "no". It repeated the dental joke and delayed the first role gag, so it was cut.
- **Files:**
  - `lingo/videos/chat_roles.mp4` (long-form; replaces the vertical pilot)
  - episode `lingo/chat/episodes/roles.json`
  - credits `lingo/out/chat_roles_credits.txt`

## 9. Reusable command (paste into a fresh session)

```
Make a new LingoDude chat comedy with Blueprint 03.
Premise: "<one sentence>".
Read lingo/blueprints/DISCORD_CHAT_COMEDY_BLUEPRINT.md (sections 2–7) and lingo/chat/episodes/roles.json as the example.
Write lingo/chat/episodes/<key>.json in English: long-form 1920x1080, 55–75 beats in 3 acts (1:30–2:30), hook by 2 s, three escalation loops,
a reversal with a typing indicator, an authority entrance, and a callback punchline held 1.5–2 s.
Use calm Wojaks from lingo/wojaks/ (or our own SVGs), our own chat look, no real people or logos,
and a credited CC music track only under the chaos character.
Then run, from lingo/:
  node chat.mjs <key> --timeline
  node chat.mjs <key> --still 1.5,10,30,60,90
  node chat.mjs <key>
Do the section 7 quality check at phone size, name and rewrite the weakest beat, re-render,
copy out/chat_<key>.mp4 to lingo/videos/chat_<key>.mp4, write out/chat_<key>_credits.txt,
commit and push, and send me the video.
```

**Command for the owner** (after an episode file exists): `cd lingo && node chat.mjs <key>`.
