---
name: lingodude-video-method
description: LingoDude Video Method. The established workflow, formats, rules and style for making scripted 1080p "X Languages be like…" / ranking / series videos with real recordings, Wojak characters, credits, thumbnails and YouTube metadata. Use when planning, building, rendering, checking or uploading a LingoDude video, or when reusing the method for another channel or niche.
---

# LingoDude Video Method

Code lives in `lingo/` (repo anaqqad/Test). Commit and push every finished step to the working branch.

## 1. Topic rules
- Meme-category titles in the reference style (youtube.com/@thatsquiteinteresting): "X Languages be like…", "Languages That…", rankings ("Ranking the Most Polite Languages"), "…Simulated by AI".
- Topics are language categories, never one country or region (owner rejected "Italy's languages", "Middle East").
- Series are real series: label every part, including Part 1, once Part 2 exists ("(Part 1)" in the title, PART 1 on the thumbnail, `part: "Part 1"` in the video). Add "Part 2" only when a Part 1 exists.
- Before a series: check that there are enough languages with real recordings for each part. Never repeat a language within the same series. Reusing a language from another video is fine.
- Keep the idea list in `lingo/ideas/TODO.md`. Saved ideas go in `lingo/ideas/<idea>.md`.

## 2. Audio rules (hard)
- Use only real recordings that were actually found: Wikimedia Commons (Wikitongues, Lingua Libre, other CC files), Creative Commons YouTube clips, or clips used with the uploader's or subscriber's permission. No synthesized speech or generated music.
- A language with no recording gets replaced or dropped, never faked.
- Only exception: the owner's AI-simulation series (`ancient*`). There, Piper voices read scholarly IPA reconstructions, every clip is labelled "AI SIMULATION", and YouTube's altered/synthetic box is ticked.
- Verify every clip:
  - Whisper language ID in windows (avoid English intros);
  - listen for music-only intros (skip to where the voice starts);
  - the clip must be speech, not instruments (e.g. Solresol must be spoken).
- **Let the recording run a little longer (owner, 2026-11-22).** In "can you understand" and listen-style videos, the
  first seconds often sound like any ordinary language (a greeting, a name, a place). Add a few seconds to what we used
  to do: about 20–25 s per clip (the Portuguese video used 14–22 s). Not long clips: the owner doesn't want them long.
  Pick the stretch with the most characteristic speech, not only the self-introduction.
- Run `python3 analyze_audio.py <key>` to get the voice gender. **The Wojak or avatar gender must match the voice.**
  Pitch alone is not enough between about 160 and 210 Hz: a high male voice read as female in the Portuguese video
  (Papiamento, 198 Hz, the speaker is Ricardo). Confirm the speaker from the transcript, the video or the file page first.
- Credit every recording (title, author, licence, link) in `out/<key>_credits.txt`, which goes into the description. Credit subscribers who send voices by name.

## 3. Finding recordings
- Commons API: `list=search` with `intitle:WIKITONGUES intitle:"speaking <Lang>"`. When the API returns 429, use the HTML search `commons.wikimedia.org/w/index.php?search=...&ns6=1&fulltext=1`, retry slowly and honour Retry-After.
- If Commons keeps answering 429 to scripts, fetch through headless Chromium (Playwright `page.request.get` on `Special:FilePath/<name>` or the API): it worked at once when plain HTTP was blocked for hours.
- Images: use standard thumbnail sizes only (`/thumb/h/hh/Name/1280px-Name`). Audio: `/transcoded/.../Name.mp3`.
- YouTube Creative Commons search: `results?search_query=...&sp=EgIwAQ%253D%253D`. YouTube blocks downloads from the cloud, so give the owner video IDs or links. The owner downloads the files and uploads them (to chat uploads or `lingo/incoming/`).
- Lingua Libre (via Wikidata P443) for single words.

## 4. Formats and builders
- **Story layout** (`videos.mjs`, `node render.mjs <key>`): per language:
  - flag, speakers, scene, map `loc`, `wojak`;
  - 2 short fact `cards` (one claim each, highlighted words in quotes; use ’ instead of ' inside names);
  - `audio: { file, start: "auto"|seconds, voice: "m"|"f" }`;
  - optional `like` + `verdict` [text, colour] for the "sounds like" series.
  - About 12 languages and about 2:40 long. Intro card with title, PART label and all flags; outro at the end.
- **Countdown/ranking** (`node vulgar.mjs --set <set>`, JSON set with an explicit `rank`). Rank by a stated, reproducible method (e.g. FSI weeks + Swadesh %, corpus counts), never by feel. Fix card claims to what was actually counted ("We counted over 900").
- **Similar pairs** (`similar.mjs`): score on the same 41 Swadesh words (vocabulary root, spelling edit distance, 6-point grammar checklist) and play 10 real Lingua Libre words.
- **Map tour** (`maptour.mjs` + `maptour_episodes.mjs`).
- **Custom builders** for YouTube or uploaded sources (`build_<key>.py`): a CLIPS list of (source, start, title, author, licence) that writes `cache/audio/<key>/manifest.json` and the credits.
- Audio fetch for Commons-based sets: `python3 fetch_audio.py <key>` (resumable).

## 5. Characters (Wojaks)
- Use Wojaks for every language, not the plain drawn avatars (owner correction). Use a `wojak: "<id>"` field per item, with the PNG in `lingo/wojaks/`.
- Generate them with ChatGPT through the Codex CLI (`gen.sh name "description"` + a job loop that passes `</dev/null`):
  - classic Wojak line style, head and shoulders, transparent background, no text;
  - describe age, skin, hair and local clothing, plus "calm, friendly, gentle smile".
- If ChatGPT fails to save an image, retry the job; it is not a content problem.
- Gender must match the voice. No shouting Wojaks, except in the curse/vulgar video.
- Stay signed in to Codex between batches. Log out only when the owner says "logout".

## 6. Thumbnails (`node thumb_photo.mjs <key>`)
- Always the channel look:
  - white name strip with the language name;
  - real landscape photo (free licence from Commons, credited in the description);
  - Wojak on the left, touching the bottom edge (transparent margin trimmed, no gap), flag top right;
  - red PART label for series;
  - hook of 2 short lines in **red text with a white outline**, never another hook colour.
- Hook examples: "This Isn't / Japanese?!", "No Relatives / At All?!", "Too / Polite?!".
- Send the thumbnail to the owner for approval before publishing.

## 7. Check, render, deliver
1. Render stills first: `node render.mjs <key> --still 2,8`. Check the text fits, the facts, the flags, the Wojak gender and the in-video branding (big LingoDude logo plus part label).
2. Run the full render, then spot-check frames and any timestamp the owner flags. Look for silence, music-only parts and wrong languages.
3. Run `node make_meta.mjs <key>`, then fix the title (add "(Part N)").
4. Write `meta/<key>.md` (Title, Description, Tags, Settings) plus plain-text `<key>_title.txt`, `_description.txt` and `_tags.txt` for copy-paste. Give the owner the metadata in copyable text boxes in chat too.
5. Description:
   - hook paragraph and a "which language next?" question;
   - chapters with speaker counts;
   - all recording credits, licence links and the thumbnail photo credit;
   - hashtags.
   - No `<` or `>` (YouTube rejects them).
6. Settings: Education, not made for kids, synthetic content No (Yes only for AI simulation). Ad suitability: "None of the above", except tick "Inappropriate language" for the vulgar video.
7. Copy the MP4 and thumbnail to `lingo/videos/`, commit, push, and send the MP4, the thumbnail and the description to the owner.
8. If the owner says "do not rerender", stop immediately and say if it was too late.

## 8. Upload
- `python lingo/upload_youtube.py <key> lingo/videos/<file>.mp4` reads `meta/<key>.md` and uploads as **private** (`--dry-run` to check, `--public` only with the owner's OK).
- `client_secret.json` and `youtube_token.json` are gitignored. Never print or commit them.
- Ask before publishing anything public. Quota is about 10,000 units a day (an upload costs about 1,600).

## 9. General rules
- Never print, log or commit API keys; secrets come from environment variables.
- Ask before any paid API usage.
- Don't touch unrelated projects or folders.
- Fact-check every card. Use speaker counts with "~" and note in the description that estimates vary.
- Don't commit generated MP4s from `out/`. The deliverable copy goes in `videos/`, and ignored cache sources need `git add -f`.

## Reusing for another channel or niche
Keep the pipeline and swap these:
- the topic category list;
- the source rules (only real, licensed material, credited);
- the character style;
- the thumbnail template (name strip, photo, character, flag, part label, red hook);
- the brand logo.

## Long-form techniques (Malta v3)
Reusable scene techniques for long-form map explainers (`lingo/longform3.mjs`), each with origin, when to use, how to build
and where it appears in Malta v3: `.claude/skills/lingodude-video-method/techniques/`
(The Word Arrives Before the Place, The Consonants Lock In, Two Islands One Clock, The Cut Starts in the Soundtrack,
Read the Ink, The Claim Revises Itself, Footage With Its Own Air). QA: `python3 lingo/longform_qa.py <key> <tag>`.

## Long-form v4: shot-based edit (Malta v4)
`lingo/longform4.mjs` cuts every line into `shots` and refuses shots over 5 s (The Five-Second Rule). New shot types:
`table` (3D Mediterranean Table), `board` (Investigation Board, with The Claim Rewrites Itself on cards), `desk`
(Document Pullback), `plate` (cards on a clean background, never over the map), `words` (Typography Follows the Voice),
and pillarboxed vertical footage. Location beds per sequence (`EP.beds`) and Foley on every event. Techniques:
`.claude/skills/lingodude-video-method/techniques/` (investigation-board, mediterranean-table, document-pullback,
live-action-match-cuts, typography-follows-the-voice, five-second-rule). QA adds a scene-cut check on the MP4.
