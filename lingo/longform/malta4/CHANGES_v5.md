# Malta v5: what changed from v4 (`out/malta4_v5.mp4`, 9:23)

Render: `node longform4.mjs malta4 --voice am_fenrir --out malta4_v5`. Sources for every board string: `sources_v5.md`.

## Owner's notes on v4
| Note | Fix | Where in v5 |
|---|---|---|
| "6:27 a scene shows quickly and disappears" | A photo faded out while the map behind it was still at its previous framing (Malta in red), so the old map showed for about 0.3 s before the next map shot. The renderer now hard-cuts any layer that ends where a map shot starts. QA has a new "flashes" check (anything on screen under 0.5 s between cuts). | 7:10 (the street sign → Italy map cut; it was 6:27 in v4) |
| "First scene shows face of woman 1 sec, then her hands. Delete face" | The opening now starts on the over-the-shoulder page turn (source 12.4–14.3 s, slowed to 0.85×), cropped so the burned-in subtitles and logo stay out. The second shot is the decorated carpet page. The closing callback uses the same page turn. Checked frame by frame: no face. | 0:00–0:05, 9:12 |
| "Make passing documents smooth so readers can read" | Desk shots: camera angles lowered from up to 68° to at most 40°, blur cut from 6–8 px to 2.5–3 px, moves made much smaller (the line glide in m2 is split into two slow halves along the same line). Board: cards read close up, then the camera glides to the next one instead of jumping; the caption strip stays on screen across cuts. | 4:20–5:03, 9:05 |
| "Make evidence logical and hover from one to the other" | Board rebuilt (below). Consecutive board shots glide from card to card with an eased move and a small zoom-out arc. | throughout |
| "Check everything" | Full render, QA (loudness, phone speaker, five-second rule, flashes), contact sheets. See the QA section. | |

## The board, rebuilt
**Structure:** shared clue at the top (ktieb ≈ kitāb, K·T·B, THE LINK, then the Phoenician claim beside the test that
checks it), the question under it, MALTA on the left and SICILY on the right with the oldest evidence at the top, and a
PROVISIONAL ANSWER band at the bottom.

**Each step:** close on the active card with its key phrase highlighted, then a cut wide as a labelled string draws
(RECORDS, SHOWS, SUGGESTS, CHALLENGES, SUPPORTS, NOT SHOWN). Older branches dim while the current one is explained.

| Time | Step |
|---|---|
| 0:36 | The clue: ktieb ≈ kitāb (highlight "book"), then K·T·B (glide) |
| 0:42 | THE LINK pinned; two SHOWS strings |
| 0:46 | "Why did this link survive in Malta, and not in Sicily?" (RAISES), then how to read the board |
| 1:30 | al-Himyari's claim (Malta empty 870–1048) |
| 1:40 | Test card "who else says so?" → CHALLENGES → claim rewritten "Emptied after 870? Uncertain: one late source" |
| 2:04 | Malaterra's chronicle (1091) → RECORDS → "In 1091, Malta was under Muslim rule"; Roger I's coin pinned as a VISUAL ANCHOR with no string |
| 2:23 | Palermo 1142 inscription → SHOWS → "Arabic still used at the royal court in 1142" |
| 2:30 | Lucera → RECORDS → "Muslim communities were deported" |
| 2:38 | Abbate report c. 1241 → RECORDS → "Muslim and Christian families are recorded" |
| 3:12 | OPEN card "Did Malta's Christians already speak the dialect in 1241?" with a dashed NOT SHOWN string (the report counts faith, not language) |
| 3:29 | 15th-century surnames → SHOWS → "Arabic origins in some recorded surnames" |
| 3:36 | Gallo-Italic dialects (Nicosia, San Fratello) → RECORDS → "New settlers arrived from northern Italy" (new source card) |
| 3:48 | zàgara ← zahra → SHOWS → "Arabic survives only as loanwords" |
| 3:55 | Sicily's steps joined: SUGGESTS ×2 + SHOWS → "Arabic's speakers were removed and replaced; the language faded" |
| 4:53 | Il-Kantilena (register dated 1533–1536) → CHALLENGES → "Maltese was never written down" rewritten "Written Maltese is attested by the 1530s" |
| 5:51 | Back to K·T·B |
| 6:28 | Phoenician claim (1750) placed beside THE LINK |
| 6:39 | Test: Maltese il- = Arabic al-, Phoenician ha- → CHALLENGES; claim rewritten "Its grammar points to Arabic, not Phoenician"; SUPPORTS string to THE LINK |
| 8:25 | Full board, then a trace down the Sicily column |
| 8:38 | Trace down the Malta column; joins into the Malta answer (SUGGESTS ×3) |
| 8:48 | Provisional answer: both halves, then the open question, then the full board |

## Narration changed to match the evidence
- b0/b0b/b1 (new): the clue, the link, the question, how to read the board.
- t3c: "rests on his account alone… the empty century stays uncertain" (was "not every historian believes him… by the eleventh century Malta spoke Arabic").
- t6: Malaterra's record of the 1091 landing.
- p1/p2: the 1241 report counts faith, not language, so that step stays open (was "they had been speaking the same dialect all along").
- p4/p4b/p4c: the settlers' dialects named; loanword example zàgara; Sicily's steps joined. "A few hundred words" dropped (count not confirmed).
- m2/m5/m6: the attribution to Pietru Caxaro is the copyist's; the register is dated 1533–1536; "written by the 1530s, and decades earlier if the copyist is right" (was "by the fourteen hundreds").
- w10: the article test (il- / al- / ha-) instead of "almost nothing pointed to Phoenician".
- r1/r2/r2b: trace both columns; strongest supported conclusion; the open question said out loud.

## Also fixed
- Fraunces draws the macron of ā on the next letter, so "kitāb" read as "kitab" (in v4 too). The page now draws the macron itself.
- Head cards dim by fading the text (no dark box).

## Found by "check everything" on the first v5 render, then fixed
- The film opened on 0.3 s of map before the first shot, then a few frames of the woman's shirt (the source cut is at about 12.45 s). The first shot now covers the lead-in and starts at 12.52 s.
- When the board cut in from footage, it showed empty for 0.15–0.3 s before the card popped in (2:06, 2:40, 3:30, 3:39, 4:53, 6:27). On a cut-in, a card due in the first half second is already landing on the first frame. Same for objects dropped on the table (2:22).
- QA's flash check also lists motion inside a shot (candle flicker, boats, fire); each candidate was checked by eye on a frame sheet.

## Could not do
- No specific counterevidence to the empty-island claim met the bar: the archaeology claim on Wikipedia (Blouet 2007 p. 41) carries a "verify source" tag. The board challenges the claim on its sourcing instead and says the gap is uncertain.
