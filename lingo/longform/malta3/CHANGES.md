# Malta v3: change list (v2 → v3)

Film: `out/malta3_v3.mp4` (8:18, 1080p30). Project: `longform/malta3/episode.mjs` + `longform3.mjs`; the soundtrack in five stems,
`cache/longform/malta3/stems_malta3_v3/{vo,words,amb,sfx,score}.wav`; timeline and mix: `project_malta3_v3.json`.

| v3 time | What changed | Why / technique |
|---|---|---|
| 0:00 | Cold open on Vassalli's 1796 dictionary, tight on "KTŶB". A page turn, then a native speaker says **ktieb**. No narrator, no music. | The Word Arrives Before the Place; the page-turn Foley starts 0.3 s before the picture (The Cut Starts in the Soundtrack) |
| 0:03 | ktieb, then Arabic kitāb; the words appear one at a time and K-T-B lock into red columns | The Consonants Lock In; score muted for the comparison |
| 0:07 | Reveal: Grand Harbour footage with its own sound, then Marsaxlokk. "That was Maltese… why did this language survive on Malta, while the Arabic once spoken in Sicily disappeared?" | Footage With Its Own Air; first music cue enters here |
| 0:17 | Malta and Sicily on one map: ≈90 km, both Arab-ruled; 1091 and the coin of Roger I as first evidence | |
| 0:28 | "Today, Sicily speaks a Latin language. Malta still says ktieb." Title card. | |
| 0:35–0:54 | Was v2's static 0:36–0:48 close-up. Now three camera moves: Malta and Gozo, then Sicily and Tunisia with distance lines, then the whole Mediterranean | |
| 0:54–2:48 | New sequence: **two islands at the same scale on one clock** (800 → 1300). Each step recolours a side; the clock pauses for evidence (coin, 1142 trilingual inscription, Lucera, the Abbate dots). Silence at 2:42 when the clocks disagree. | Two Islands, One Clock |
| 1:11 | al-Himyari's "empty island" claim is struck through and revised to "Disputed" | The Claim Revises Itself |
| 2:48 | The people who stayed: Mdina footage (carriage, Pjazza San Pawl), surnames 42.5 % | |
| 3:36 | Mid-roll teaser line, then a 1.3 s gap: mid-roll at **3:42** | |
| 3:43–4:18 | The Kantilena as an investigation: tight on line 1, a highlight tracks across the ink, the camera holds on *gireni*, then pulls back to the whole page and the attribution (who wrote it, who copied it, when it was found). Score gap on the line read aloud. | Read the Ink (after WWII Frontlines' LedgerDocument) |
| 4:09 | "Never written down" struck through: "Rarely written: the oldest known text is from before 1485" | The Claim Revises Itself |
| 4:18–4:40 | Was v2's static 4:24–5:12. Now the cathedral interior (door pre-lap), the siege fresco, Valletta balconies, Italian loanwords heard | |
| 4:40–5:13 | A word travelling: Mdina street, then a street sign (triq ← ṭarīq, bir ← biʾr, ljun ← Italian), the bakery (ħobża heard, khubz), then a listening demo: ktieb/kitāb and kittieb/kātib lock on K-T-B | |
| 5:13–6:02 | K-T-B word family, the dictionary bar over the National Library, the 1565 callback, and the Soldanis monument under the Phoenician claim. That claim is then revised over a real Phoenician inscription. | |
| 6:24–6:48 | Was v2's static 6:24–6:48. Now the 1934 stamp, then Marsaxlokk harbour footage; speakers counter | |
| 6:44–7:39 | Alive today: Keith (Wikitongues) over Tritons' Fountain; numbers heard (ħamsa u sittin); "IS MALTESE SAFE?" census gauge; door pre-lap into the cathedral; Alla / Alla jbierek heard; "CAN ARABIC SPEAKERS FOLLOW IT?" ≈40 %; a real proverb recording with bird, hand and hundred traced to Arabic | statistics are asked as questions |
| 7:39–8:18 | The answer: the twin clock returns in its final state ("The religion changed. The language stayed."), then Vassalli's title page pulls in to Ktieb il-Kliem Malti. ktieb is heard again, then the harbour and a fade. | resolves the cold open |

**Sound:** stems for narration, native words, ambience (each clip's own location sound), Foley (page, door) and score. Ten
score textures, one per sequence. The score is muted for every word comparison and for the music gaps. Mix: −16.2 LUFS, −1.6 dBTP.

**Palette and type:** honey limestone, Mediterranean blue, warm paper, restrained red; Fraunces and Inter; Noto Naskh for Arabic. ċ ġ għ ħ ż checked on screen.

**QA** (`python3 longform_qa.py malta3 malta3_v3` → `out/qa_malta3_v3.txt`):
- headphones;
- phone-speaker simulation: Whisper recovers 92 % of the narration, and every native word is at least 6 dB over the bed;
- muted contact sheet;
- audio-only list.

The muted sheet caught a cat: the "ferry harbour" Commons clip is a cat for its whole length. It is replaced.

**Missing dependency:** no native recording of *ktieb* inside a natural sentence exists on Commons or Lingua Libre (see `sources_v3.md`).
