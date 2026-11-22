# Film log: Bush / Chichi Jima episode

Logged 22 Nov 2026 from contact sheets in `build/sheets/` (`<film>_ov.jpg` = 60-frame overview, other files = dense
checks at 0.1-2 s). All times are seconds (or m:ss) in the files in `assets/footage/`, as labelled by `tools/sheet.py`
(label = exact seek time). Ranges are inclusive; trim ~0.2 s inside each edge when cutting.

Skipped on purpose: `bush_kilo8_1991`, `bush_pearl_1991` (audio cards, already known).

## Global warnings (read first)

1. **Burned-in timecode on whole files** (no clean frame anywhere):
   - `san_jacinto_1944`, `kwajalein_strike_1944`: "00:xx:xx:xx RTC" box at x 9-48 %, y 80-88 % of frame.
     Usable only with a crop that keeps the top ~78 % (1.28x push-in) or a mask.
   - `fighting_lady_out_a`, `fighting_lady_out_b`: big timecode at x 22-69 %, y 88-97 %. Crop to the top ~86 %.
   - `wolverine_training_1943`: big timecode at x 23-72 %, y 73-83 %. Crop to the top ~70 % (2:1 strip) or skip.
   - `tang_lifeguard_1944`: RTC timecode throughout (and wrong content, see below).
2. **`tang_lifeguard_1944.mp4` is the wrong film.** It is not the Tang/Truk lifeguard rescue. Content is a USS Franklin
   practice-firing roll (slate "FRANKLIN Roll 51 2/18/45 Op No III Practice Firing") and Marines of the 3rd Division
   boarding landing craft for Iwo Jima (slates 2/19/45, 2/20/45, 2/21/45). No raft, no submarine. Treat as useless for
   the rescue; re-download the real 428-NPC-4369 if the Tang shots are wanted.
3. **`chichi_surrender_c` is the 31 Aug 1945 negotiation**, not the 3 Sept surrender: its own slate at 2:22-2:29 reads
   "U.S.S. DUNLAP / JAP Negotiations / CHICHI / 31 Aug / MARK photog". Use reel A for the 3 Sept ceremony.
4. **Tachibana and the salute.** In reel A a senior Army officer with glasses and four rows of ribbons climbs the ladder
   (2:22.9-2:35.0), walks aft (5:18-5:25) and signs (5:59-6:30). This is almost certainly Lt Gen Tachibana (compare with
   photo P36 before captioning). **He is not seen saluting at the top of the ladder.** The visible salutes are by other,
   younger officers (A 2:38.0-2:40.0; B 1:37.5-1:45.0). Suggest the narration in act 21 says "filmed him climbing
   aboard" rather than "saluting", or cut the salute from reel B under a neutral line.
5. Many "carrier" planes are Hellcats (F6F), not Avengers. Avenger (TBF/TBM) shots are listed explicitly as such.
6. No film shows a submarine interior. No film shows Midway or Pearl Harbor; Tigrone at Guam (July 1945) is the only
   "submarine arrives in port" footage.

---

## 1. `finback_rescue_1944.mp4` (THE REAL RESCUE FILM)

- 960x706 file (490x360 source upscaled, 4:3 image with black side bars), 54.75 s, B&W, 8 mm, soft, dirt specks and
  vertical scratches throughout, exposure drifts. Shot from Finback's conning tower by Ens. Bill Edwards, 2 Sept 1944.

Shot by shot:

| Time (s) | Shot |
|---|---|
| 0.00-5.00 | Bush Library / NARA title card. **RISKY** |
| 5.00-11.4 | Shot 1: hazy sea and horizon from the boat, heavily overexposed, slight pan. No raft identifiable (dark dot at ~9.2 s is dirt). Marginal; at most a 2-3 s "searching the sea" insert (6-9 s). |
| 11.4-16.55 | Almost pure white, blank overexposed frames. **RISKY (unreadable)** |
| 16.55-22.75 | Shot 2: forward deck seen from the conning tower. A sailor stands at the bow looking out (16.6-18.0); shirtless sailors hurry forward along the deck (17.5-21.0); a group lines the bow edge peering into the water (21.0-22.7). Faint land on the horizon at 16.6-17.0. |
| 22.75-27.0 | Shot 3: bow, closer. **The raft first appears at 22.8 s**: a light, round raft floating alongside the starboard bow (clearest 25.0-26.5) with sailors at the edge reaching down to it. |
| 27.0-34.8 | Shot 4: tighter on the bow edge. Sailors kneel and haul the pilot up from the raft (27.0-31.0); the emptied raft drifts along the hull (30.3-31.2); **the pilot comes up onto the deck among the sailors at ~31.3-34.7** (figures small, Bush's face not distinguishable). |
| 34.85-37.6 | Shot 5: from the deck, the group walks aft toward the camera carrying the raft and gear. |
| 37.65-41.5 | Shot 6: **Bush (dark, wet flight clothes, right) walks aft toward the camera beside a sailor in a white T-shirt (left)**. This is the shot NARA still P5 comes from. Clearest 38.0-41.0. |
| 41.55-42.5 | Shot 7: close-up, Bush climbs up past the camera at the rail/ladder, face visible 41.6-42.4 (motion blur). |
| 42.5-43.6 | Shot 8: two young crewmen at a gun mount by the conning tower, handheld, flare. |
| 43.6-44.6 | Shot 9: deck gun with the US flag flying behind it. |
| 44.65-~51.0 | Shot 10: sea and horizon from the boat; a small white spout on the horizon 44.7-46.8 (unexplained splash). Heavy dirt specks. |
| ~51.0-53.9 | Shot 11: horizon, different angle; small spout ~52-53. |
| 53.95-54.75 | Shot 12: island coastline under cumulus on the horizon (0.8 s, possibly Chichi Jima). |

USABLE RANGES
- 16.6-22.7: sailors run forward along the deck to the bow (act 13, the boat closes in).
- 22.8-27.0: raft alongside the bow, sailors reach down (act 13, "four minutes to noon").
- 27.0-34.7: sailors haul the pilot aboard from the raft (act 13; also cold open act 1).
- 34.9-37.6: group walks aft with the raft (act 13).
- 37.7-41.5: Bush walks aft beside a sailor (act 13 payoff; act 15).
- 41.6-42.4: Bush close-up climbing (act 13; hold/freeze-frame candidate).
- 43.6-44.6: deck gun and flag (act 15, life aboard).
- 44.7-50.9: empty sea from the boat (act 13 "she commenced a search", act 14).
- 53.95-54.75: island on horizon (very short; act 13, freeze-frame only).
- Keep at native size inside a frame, as planned; do not upscale beyond ~2x.

RISKY RANGES: 0.00-5.00 title card; 11.4-16.55 blank white; 5.0-11.4 near-blank (only if needed).

---

## 2. `chichi_surrender_a.mp4` (428-NPC-17059, surrender of Chichi Jima, 3 Sept 1945)

- 720x480 (4:3, SAR 10:11), 8:10, colour (Kodachrome, blue cast), fair sharpness, handheld.

Tachibana (probable, see warning 4): **2:22.9-2:35.0** climbs the boarding ladder and steps over the rail (face clear
2:33.9-2:35.0, rows of ribbons); **4:27-4:34** close two-shot of two Japanese officers, he is on the left (glasses);
**5:18-5:25** walks along Dunlap's deck toward camera beside a US officer in whites and gold-braided cap (Commodore
Magruder?), face clear 5:22.5-5:24.8; **5:59-6:30** signs the surrender document (close-ups of glove and pen 6:11-6:30).
Chichi Jima coastline: **1:01-1:22**.

USABLE RANGES
- 0:19-0:30: a destroyer ahead on a sunlit sea, our wake in foreground (act 21 approach).
- 0:31-0:40: destroyer broadside on the horizon (act 21).
- 0:41-0:59: Dunlap's US flag and commodore's pennant flying, sailor at the rail (act 21).
- 1:01-1:12: Chichi Jima's coastline along the horizon, long lens (act 8, act 21, act 25).
- 1:13-1:22: high cliffs of Chichi Jima close (act 8 "the island was a fortress").
- 1:24-1:41: Japanese boats coming out across the sea (act 21).
- 1:43-1:52: two Japanese boats under a cloud bank (act 21).
- 1:53-2:15: Japanese officers in the boat alongside, seen from Dunlap's deck (act 21).
- 2:22.9-2:35.0: senior officer (Tachibana, probable) climbs the ladder (act 21 key shot).
- 2:35.6-2:37.5: he walks aft toward US officers in khaki (act 21).
- 3:09-3:16: officers grouped by the surrender table, silhouettes against sky (act 21).
- 3:17-3:33: green-covered surrender table, Japanese party facing US officers (act 21).
- 3:53-4:01: US officer in white cap signs at the table (act 21).
- 4:27-4:34: two Japanese officers close, Tachibana (probable) left (act 21, act 20 trial set-up).
- 4:35-4:55: Japanese officers walk past ranks of sailors in whites (act 21).
- 5:18-5:25: Tachibana (probable) walks the deck with a US officer (act 21).
- 5:43-5:57: Japanese party at the table among sailors (act 21).
- 5:59-6:30: Japanese general signs, close on hand and pen 6:11-6:30 (act 21 "surrendered the Bonin Islands").
- 6:41-6:48: high angle, crowd of sailors around the table, gun barrel (act 21).
- 7:00-7:22: close on hand signing (US side) (act 21).

RISKY RANGES: 0:00-0:18 slate "428 NPC 017059" and black; 7:38.5-8:10 grey, "B" leader frame (~7:41), black and
"END OF RECORDING"; 5:03-5:09 and 5:15-5:17 orange light-struck flash frames; 2:38-2:51 close faces of junior Japanese
officers (not our named men; avoid lingering).

---

## 3. `chichi_surrender_b.mp4` (428-NPC-17060, Dunlap off Chichi Jima)

- 720x480 (4:3), 6:15, colour (Kodachrome, blue), fair; very dark handheld deck shots 1:12-1:33 and 4:07-4:16.

Tachibana (probable): **4:17.5-4:22.5** walks on deck beside a US officer in whites (glasses, Army cap). No ladder salute.
Other officers salute at the rail **1:37.5-1:39.5** (white-gloved salute) and **1:43.5-1:45.0** (officer with aiguillette).
Chichi Jima coastline: **0:37-0:44**, **3:27-3:39**, **5:17-5:45**.

USABLE RANGES
- 0:19-0:36: Japanese wooden boat lying off, cumulus behind (act 21).
- 0:37-0:44: large four-engine plane flies low past Chichi Jima's coast (act 21; act 17 B-24 era only as generic).
- 0:47-0:52: Japanese boat close, crew on the cabin roof (act 21).
- 0:53-1:11: boat with white flag comes toward Dunlap, island behind (act 21).
- 1:33-1:45: Japanese officers at the rail; salutes 1:37.5-1:39.5 and 1:43.5-1:45.0 (act 21).
- 2:13-2:22: officers in the boat seen from above, waiting (act 21).
- 2:31-2:59: boat with white flag pulls away toward a warship on the horizon (act 21).
- 3:07-3:12: US officers in whites seated at a green table on deck, coast behind (act 21).
- 3:27-3:39: Chichi Jima's mountains on the horizon, planes passing (act 8, act 25).
- 3:53-4:01: four-engine aircraft and fighters flying past low (act 21 flyover).
- 4:17.5-4:22.5: Tachibana (probable) with US officer (act 21).
- 4:25-4:31: Japanese naval officer with ribbons beside US officers (act 21; do not name him).
- 4:33-4:45: Japanese boat with white flag, close (act 21).
- 5:17-5:45: boats returning toward Chichi Jima under cumulus, the island's whole profile behind (act 21 end, act 25).

RISKY RANGES: 0:00-0:18.5 slate "428 NPC 017060" and black; 4:57-5:08 dark blurred frames; 5:46-6:15 "R" leader,
**Kodak colour-reference girl (~5:47)**, black, "END OF RECORDING"; 3:21-3:26 close faces of sailors (fine, but generic).

---

## 4. `chichi_surrender_c.mp4` (428-NPC-17062, negotiations aboard Dunlap, 31 Aug 1945 per slate)

- 720x480 (4:3), 8:40, colour (blue cast), fair.
- Tachibana: **not identifiable** in this reel. The envoys are staff officers (one with aiguillette). Chichi Jima
  coastline: faint on horizon 2:47-2:52 and 3:15-3:20.

USABLE RANGES
- 0:17-0:20: signalmen at the flag bags (act 21).
- 0:21-0:28: signal flags streaming from the halyards (act 21).
- 1:13-1:14, 1:19-1:22, 1:29-1:32: Hellcats very low over the water past the ship (act 21 flyover; act 9 cover).
- 1:41-1:46: officers in whites walk the deck (act 21).
- 2:29-2:40: officers on the bridge wing with binoculars (act 21; act 13 lookouts as generic).
- 2:47-2:59: lookouts with binoculars, island on horizon (act 21).
- 3:15-3:27: Japanese boat with white flag approaches (act 21).
- 3:29-3:41: boat comes alongside, seen from directly above (act 21).
- 4:15-4:27: envoys climb Dunlap's ladder (act 21, label as 31 Aug).
- 4:29-4:37: envoys received on deck by US officers (act 21).
- 5:43-5:59: envoys stand on deck among US sailors (act 21).
- 6:29-6:34: officer with aiguillette and envoys on deck (act 21).
- 7:27-7:41: envoys back in their boat, seen from above (act 21).
- 7:43-8:05: boat with white flag pulls away (act 21).

RISKY RANGES: 0:00-0:17 slate and black; **2:22-2:29 handwritten slate card** ("JAP Negotiations", ethnic slur, never
show); 1:39 dark frame; 1:47-2:03 close-up of a bearded sailor (fine, but generic); 4:49-4:52 and 5:05-5:08 dark blurs;
8:06-8:40 flare, grey, Kodak reference face (~8:09), black, end card.

---

## 5. `chichi_bombing_1944.mp4` (111-ADC-1817, Signal Corps, 27 Sept 1944)

- 720x480 (4:3), 9:08, B&W, good and sharp (the best aerial of the real island).
- First 3:30 = **Chichi Jima, 27 Sept 1944, 25 days after Bush**. From 3:37 the film is bomb loading and B-25s for
  another target (Celebes), not relevant.

USABLE RANGES
- 0:13-0:18: vertical view, bomb splashes in the sea off the coast (act 11 dive, act 12).
- 0:19-0:30: vertical pan along Chichi Jima's rugged north coast (act 8, act 11).
- 0:31-0:41: vertical over hills and harbour installations, cloud below (act 8).
- 0:43-0:54: oblique view of the island's coast and a deep bay (act 8 "the harbor of Futami", act 25).
- 0:55-0:57: wide oblique of the island with offshore islets (act 8).
- 1:13-1:30: **bombs burst on the island, flash at 1:21-1:25, smoke cloud rising** (act 11, "releasing his bombs").
- 1:31-1:47: smoke over the island, wing of the bomber in frame (act 11-12).
- 1:49-1:57: Bonin islands under a cloud layer, oblique (act 9-10 approach).
- 2:13-2:20: B-24 Liberator alongside above clouds (B-24s over the Bonins).
- 2:27-2:32: formation of B-24s (B-24s over the Bonins).
- 2:33-2:40: B-24 close, seen past a waist window (B-24s).
- 2:49-2:58: B-24s seen past the wing (B-24s).

RISKY RANGES: 0:00-0:12 "111.ADC.1817" card and handwritten slate "CHICHI JIMA 9-27 1944"; 1:59-2:12 black;
2:21-2:25 white flash; 2:58-3:00 slate roll 2; 3:01-3:25 crew close-ups (AAF faces, not our story); 3:26-3:36 "END OF
ROLL", mirror slate, white; 5:52-6:10 white; 7:50-7:53 black; 8:58 reversed lettering leader; 9:02-end black and card.

---

## 6. `chichi_b24_1944.mp4` (CS-2599, 7th AAF, Oct-Nov 1944)

- 1280x720 (4:3 image, upscale), 5:20, B&W, fair (haze, film scratches).
- Mixed islands: 0:18-1:12 and 2:30-3:09 are **Iwo Jima** (airfield, "X" runways; slate "Iwo Jima 10-25"), 3:46-4:15
  a reef island (probably Yap). The Chichi Jima section is 1:30-2:26 (after/before the slate "Shipping Strike Chichi
  Jima 11/2"). 4:16-5:05 is a harbour shipping strike whose island is **not confirmed** (Chichi Jima or Yap): check
  against the GSI aerial (P47) before labelling.

USABLE RANGES
- 0:08-0:14: B-24 flying past a small volcanic islet (B-24s over the Bonins, as generic).
- 1:17-1:29: B-24 Liberator air-to-air, close (B-24s).
- 1:45-1:58: harbour and town on a rugged coast from high altitude (likely Chichi Jima; act 8, verify).
- 2:18-2:26: B-24 formation over clouds, Chichi Jima strike (B-24s over the Bonins).
- 2:30-2:34: Japanese phosphorus air burst with falling streamers (Iwo; heavy flak, label generic).
- 2:47-3:09: Iwo Jima's airfield under smoke (act 17 Iwo Jima only).
- 3:14-3:20: B-24 formation over the sea (B-24s).
- 4:22-4:49: harbour with ships, wakes and bomb splashes from altitude (shipping strike, island unconfirmed).
- 4:50-5:05: flak puffs over a rugged island coast (heavy flak; island unconfirmed).

RISKY RANGES: 0:00-0:05 slate "Shipping Strike 11-4"; 2:12-2:17 slate "Shipping Strike Chichi Jima"; 2:27-2:29 slate
"Iwo Jima 10-25"; 1:21 cloud blur; 5:19-end white leader with lettering.

---

## 7. `chichi_b24_1945.mp4` (CS-3618, 11th BG, Marcus and Chichi Jima, Mar-Apr 1945)

- 1280x720 (4:3 image), 4:51, B&W, good.
- Mostly **Marcus Island** (triangular atoll, slates "MARCUS 4-2" and "MARCUS 3-30"). The **Chichi Jima** part is
  2:41-3:05 (slate "CHICHI JIMA 3-22", i.e. 22 Mar 1945).

USABLE RANGES
- 1:58-2:06: B-24 Liberator alongside in cloud (B-24s, as generic).
- 2:41.5-2:48: **Chichi Jima's coastline from a B-24, oblique, clouds above** (Chichi Jima from the air; act 8, act 17).
- 2:50.5-2:55: vertical over the bombed town (Omura) with craters (act 17-18, the island in 1945).
- 2:55.5-2:59: **harbour waterfront and quays under smoke** (Chichi Jima harbour; act 17, act 25).
- 2:59.5-3:04: hills and roads of the island through cloud (act 8).
- 3:06-3:14: view from the B-24 past an engine nacelle over clouds and sea (B-24s).
- 4:33-4:46: B-24s in formation, close (B-24s).

RISKY RANGES: 1:29-1:31 slate "MARCUS"; 2:38-2:41 slate "CHICHI JIMA 3-22"; 2:48.5-2:50 black; 4:48-end slate
"MARCUS 3-30". Marcus shots (0:00-1:28, 2:08-2:38, 3:19-4:30) must not be labelled Chichi Jima.

---

## 8. `san_jacinto_1944.mp4` (NPC-1521, USS San Jacinto shakedown, Feb 1944)

- 1280x720, 4:05, B&W, sharp. **Burned-in RTC timecode on every frame** (crop, see warning 1).
- Bush's own carrier. Planes are VF-51 **Hellcats** (side code 51-F-xx), not Avengers.

USABLE RANGES (all need the crop)
- 0:02-0:36: Marine firing party fires volleys at a burial at sea (act 6 "Wykes never returned", memorial tone).
- 0:39-0:52: men fall in and march on the flight deck (act 5).
- 0:55-1:05: coastline and sea from the carrier (act 5 shakedown).
- 1:07-1:20: Hellcats land and taxi past the island (act 5).
- 1:21-1:34: deck crew and pilots climb up from the catwalk onto the deck (act 10 "the four planes left").
- 1:35-1:46: pilot in flight gear runs to his plane and climbs on the wing (act 10).
- 1:47-1:58: Hellcat engine starts, propeller spinning, close (act 10).
- 1:59-2:12: launch officer by a turning propeller, waits (act 10 take-off).
- 2:09-2:16: launch officer signals, plane rolls (act 10).
- 2:15-2:20: Hellcat 51-F-15 takes off down the deck (act 10).
- 2:23-2:33: launch officer whirls his arm and points down the deck (act 10).
- 2:35-2:45: Hellcat 51-F-16 rolls and lifts off (act 10).
- 2:49-2:56: Hellcat 51-F-8 takes off (act 10).
- 3:01-3:30: destroyer alongside fuelling, men handle lines (act 5).
- 3:30-3:57: hoses and seas between the ships (act 5).

RISKY RANGES: whole file (timecode); 3:38-3:45 white flare frames; 0:00-0:01 head.

---

## 9. `san_jacinto_attack_1945.mp4` (428-NPC-7784, Japanese attack on San Jacinto, 1945)

- 720x480 (4:3), 3:59, B&W, good and sharp. Several white flash frames.

USABLE RANGES
- 0:13-0:20: shell splashes on the horizon near ships (act 11 flak, generic).
- 0:21-0:28: destroyer firing, AA bursts above it (heavy flak).
- 0:33-0:46: **battleship surrounded by black AA bursts and splashes** (heavy flak).
- 0:49-0:59: scattered flak bursts in the sky (heavy flak).
- 1:05-1:18: **dense black flak bursts filling the sky** (best heavy-flak shot; act 11 "very intense, heavy and medium").
- 1:21-1:45: drifting flak smoke over the fleet, splash near a battleship 1:39-1:44 (act 11).
- 1:49-2:06: gun crews on the carrier deck handling ammunition (act 6 combat).
- 2:48.5-2:57: Hellcat approaches and lands over the stern of a carrier (training/returning landings).
- 2:58-3:04: US fighter (white star at 3:03.8) flies across the sky (generic air).
- 3:06-3:13: flak bursts over ships on the horizon, splash at 3:11 (heavy flak).
- 3:15-3:19: dye/marker in the water (act 12-13 man in the water, as generic).
- 3:20.5-3:22: plane on a carrier deck ready to launch (act 10).
- 3:22-3:34: destroyer alongside in heavy seas, crew on deck (act 5).

RISKY RANGES: 0:00-0:08 NARA logo and "428.NPC.7784" card; 0:09-0:12 out-of-focus frame; white flashes at ~0:29,
~1:01, ~1:27, ~1:47, 2:08-2:11, 2:23-2:24, 3:55; black 2:06.5-2:08 and 2:46-2:48; **2:24-2:46 wrapped casualty in a
Stokes litter transferred by highline (body/wounded man, do not show)**; 3:35-3:54 man/object dragged through waves on
highline (ambiguous, avoid); 3:56-end white and "End of Recording".

---

## 10. `independence_tbf_1943.mp4` (NPC-800, USS Independence CVL-22, 19 Apr 1943)

- 1280x720, 5:31, B&W, soft and low-contrast (duplicate generation), no timecode.
- Sister ship of San Jacinto (same class). Genuine **TBF Avengers**.

USABLE RANGES
- 0:00-0:11: **TBF Avenger takes off down the CVL deck away from camera**, grey morning sky (launch of an Avenger, act 10).
- 0:12-0:30: TBF with wings folded, engine close, crewman beneath (act 5 "the Avenger carried three men").
- 0:35-0:40: plane handlers and Avenger tail on deck (act 5).
- 0:42-0:50: battleship on the horizon from the carrier (act 9).
- 0:51-0:56: aircraft low over the water (act 7).
- 0:56.2-0:59.5: **an aircraft down in the sea, afloat with spray** (act 7 first ditching, soft; label generic).
- 1:06-1:30: TBFs pass overhead and turn against a grey sky (Avenger in flight).
- 1:31-1:36: TBF close fly-past (Avenger in flight).
- 1:39-1:55: TBFs pass close, one after another (Avenger in flight).
- 1:56-2:08: formation of seven TBFs at altitude (Avenger in flight, act 10 "four Avengers").
- 2:17-2:32: crew work on an Avenger's engine on deck, silhouette (act 5).
- 2:37-2:45: carrier island with signal flags, backlit (act 10 dawn).
- 2:47-2:50: Avengers parked on deck, backlit (act 10 dawn).
- 2:52-3:01: **TBF taxies past camera and takes off down the deck** (launch of an Avenger, act 10).
- 4:24-4:29: crew roll a torpedo on a cart across the deck (act 5).
- 4:30-4:37: torpedo/ordnance close on a dolly (act 5).
- 4:38-4:50: ordnancemen wheel and fit a weapon (act 10 "four 500-lb bombs", as generic).

RISKY RANGES: 1:05 white frame; 1:37-1:38 black frame; 2:09-2:16 white then black; 2:33-2:36 grey blank;
**3:02-3:06 slate "PHOTOGRAPHIC OFFICER Lt(jg) W. Burlingame / WEBSTER"**; 3:17-3:38 big close-ups of a bald head
(haircut gag, unreadable); 3:40-4:20 a cake-cutting ceremony with faces (off-topic).

---

## 11. `independence_ops_1944.mp4` (NPC-6523, USS Independence, 14 Oct 1944)

- 1280x720, 9:49, colour (faded, blue cast, often washed out), soft. Burned-in "Number 1 / 10 / 12 / 13" reel cards.
- Mostly Hellcats. Flak is distant and small.

USABLE RANGES
- 0:06-0:10: Hellcat on the catapult, deck crew (act 10).
- 0:11-0:17: Hellcat climbs away over the bow (act 10).
- 0:21-0:27: Hellcat launches from the catapult, close (act 10).
- 0:31-0:36: Hellcat on catapult and away (act 10).
- 1:01-1:25: plane lands and taxies forward on the CVL deck, seen from the island (landings).
- 1:31-2:12: tiny dark AA bursts above the horizon (heavy flak at distance; soft).
- 2:23-2:37: ships on the horizon under AA bursts (heavy flak, distant).
- 4:16-4:32: Hellcat on deck against a bright morning sky, close (deck at dawn).
- 4:48-4:52: plane takes off into a low sun (deck at dawn / launch).
- 5:01-5:16: planes take off past the island in low light (deck at dawn).
- 5:38-6:05: island and planes warming up, propellers turning, backlit (carrier deck at dawn).
- 6:16-6:30: deck crew in yellow shirts around planes with folded wings (act 10).
- 6:36-6:44: pilot cleans his canopy in the cockpit (act 10 pre-flight).
- 6:46-6:52: pilot in flight gear walks across the deck (act 10).
- 8:26-8:34: Avenger-type plane on deck in sunlight (act 5).

RISKY RANGES: 0:00-0:05 grey and "Number 1" card; 0:18-0:20, 1:26-1:30 white/green flare; 0:41-0:59 light-struck
frames; 2:51-4:12 night deck, almost black and unreadable; ~4:13-4:15 "Number 10" card; ~7:00-7:03 "Number 12" card
over deck; 7:47-7:55 dark; ~8:25 "Number 13" card; 9:15-9:49 washed-out white.

---

## 12. `fighting_lady_out_a.mp4` (NPC-2658, Fighting Lady trims, 1944)

- 1280x720, 6:55, colour (faded green/yellow), soft. **Burned-in timecode throughout** (crop bottom ~14 %).

USABLE RANGES (crop)
- 0:00-0:16: formation of carrier bombers (TBMs/SB2Cs) in blue sky (Avenger in flight, act 10).
- 0:17-1:23: dive view from a plane over sea and cloud (act 11 the dive, as POV; long, cut 4-6 s).
- 1:46-1:51: plane crashes into the deck barrier, propeller smashing (act 7 lost a plane; generic).
- 1:53-2:01: thick black smoke rolling (act 12 burning engine, act 11 hits).
- 2:07-2:12: formation of dark carrier planes (Avenger in flight).
- 2:21-2:43: Avengers with wings folded, deck crew at the island (act 5, act 10).
- 2:44-3:00: diving through clouds, gun barrel in frame (act 11).
- 3:03-3:25: **attack on a ship by a rocky island shore, bomb rings in the water** (glide-bombing, act 11).
- 3:31-3:42: ship below trailing smoke, seen from a diving plane (act 11).
- 4:40-4:46: large air group in formation over clouds (act 10).
- **4:48-4:56: an unidentified plane falls trailing smoke and splashes into the sea at 4:52.8** (smoking plane going
  down, act 12; nationality unknown, show only very briefly).
- 5:48-5:51: planes in formation (act 10).
- 6:11-6:23: **Avengers in formation over cloud tops** (Avenger in flight).
- 6:33-6:41: carrier gun crew, sea and stern wake (act 6).
- 6:42-6:46: gun firing, smoke (act 11 flak from below).

RISKY RANGES: whole file (timecode); **4:01-4:14 surgery in a ship's operating room (open wound, never show)**;
4:15-4:21 cross in chapel (only if appropriate); **4:24-4:30 well-known ace posing by his kill flags (Japanese flags,
named person)**; **5:05-5:20 close-ups of a young aviator's face (could be read as Bush or his crew)**; 4:31-4:33,
4:56-4:57, 5:53 yellow blank frames; 6:53-end "R" leader.

---

## 13. `fighting_lady_out_b.mp4` (NPC-2661, Fighting Lady out-takes)

- 1280x720, 5:13, colour (faded), soft. **Burned-in timecode throughout** (crop bottom ~14 %).

USABLE RANGES (crop)
- 0:05-0:12: dive over a coastline, gun-camera style (act 11).
- 0:36-0:48: target vessel in the sea from above, strafing splashes (act 11).
- 0:52-0:58: **sunset/dawn sky, ship's guns and men in silhouette** (carrier deck at dawn).
- 0:59-1:19: **TBM Avengers in formation, close** (Avenger in flight, act 10).
- 1:20-1:25: crewman climbs into a plane (act 10).
- 1:27-1:44: deck crew by a big radial engine and propeller (act 10).
- 1:46-1:56: large air group formation (act 10).
- 2:09-2:17: ship in heavy seas (act 5).
- 2:30-2:36: battleship on the horizon (act 9).
- 2:49-2:56: SB2C dive bombers on deck being armed with bombs (act 10 "eight Helldivers").
- 2:58-3:05: **rows of bombs on the flight deck** (act 10 "four 500-lb bombs").
- 3:16-3:22: plane approaches and lands on a carrier (landings).
- 4:08-4:22: **a plane crashes into the water off a forested shore, splash at 4:19-4:22** (plane down near an island,
  act 12; unidentified).
- 4:28-4:34: deck crew run across the flight deck in low sun (carrier deck at dawn).
- 4:37-4:46: officers plotting at a chart table (act 9-10 briefing).
- 5:05-5:10: plane takes off past the island (launch).

RISKY RANGES: whole file (timecode); 0:00-0:04 black; 2:04-2:08 dark; 2:38 crash on deck (fine, generic);
3:31 Hellcat nosed over; 5:11-end "G" leader.

---

## 14. `kwajalein_strike_1944.mp4` (NPC-1469, SBD and TBF strike on Kwajalein, 27 Jan 1944)

- 1280x720, 7:29, B&W, sharp. **Burned-in RTC timecode throughout** (crop to the top ~78 %).

USABLE RANGES (crop)
- 0:06-0:14: carrier seen from the air, turning, wake behind (act 10 "left San Jacinto").
- 0:16-0:19: TBF banks over the sea (Avenger in flight).
- 0:20-0:31: **TBF Avenger close air-to-air, number 18** (best Avenger in flight; act 10-11).
- 0:34-0:41: atoll island from the air (act 8, generic island).
- 0:42-0:50: ships in a lagoon from the air (act 11).
- 1:08-1:14: island beach and smoke from low altitude (act 11).
- 1:30-1:40: **bombs burst on the island, black smoke rises** (bombs on an island, act 11).
- 1:40-1:47: blast and smoke, dive bomber pulls out across frame (act 11).
- 3:27-3:32: three SBD dive bombers in formation (act 10 "Helldivers", generic).
- 3:33-3:42: SBD rear gunner at his twin guns, close (act 5 "the gunner"; it is an SBD, not a TBM).
- 3:49-3:52: bomb explosion column on the island (act 11).
- 4:05-4:17: atoll lagoon and beach from above (act 8).
- 4:27-4:31: line of bomb bursts across the island (act 11).
- 4:33-4:57: island burning, smoke columns (act 11).
- 4:59-5:05: **three bombs explode on the island** (bombs on an island, act 11).
- 5:35-6:01: battleship firing, smoke trailing (act 9).
- 6:04-6:20: carrier on the horizon seen through rigging (act 5).

RISKY RANGES: whole file (timecode); 0:00-0:05 slate "Marshalls Campaign 1-27-44"; 1:03-1:05 white; 3:00-3:20 blank
white sky; 4:19-4:20 white; 5:07-5:23 black; 5:24-5:33 white; 6:47-6:50 black.

---

## 15. `aviator_rescue_1945.mp4` (NPC-8646, rescue of aviator at sea, 13 Feb 1945)

- 1280x720, 2:45, colour (faded Kodachrome), moderately soft.

USABLE RANGES
- 0:03-0:11: a man in the water, tiny in a wide sea (man in the water, act 12-13).
- 0:12-0:22: **downed aviator in a yellow life vest swimming** (man in the water, act 12 "he came down in the sea").
- 0:34-0:52: aviator in yellow vest swims toward the ship, closer (act 12-13).
- 0:53-1:01: rescuer swims to him and grabs him, close (act 13).
- 1:02-1:17: sailors at the ship's side haul him aboard (act 13; act 7 "picked up by destroyer Bronson").
- 1:35-1:54: wake/spray streak on the sea surface (act 13 search).
- 1:57-2:25: **empty sea to the horizon** (act 13-14 "she found nothing"; act 23).

RISKY RANGES: 0:00-0:02 grey leader; 0:23 black blur; 1:18-1:34 dark, out-of-focus close crowd; 1:55 frame edge;
**2:27-2:46 close-ups of the rescued airman's face (young, dark-haired; could be read as Bush)**.

---

## 16. `tigrone_guam_1945.mp4` (428-NPC-14153, B-29 survivors leave USS Tigrone at Guam, 3 Jul 1945)

- 1024x576, 4:06, B&W, soft and contrasty (backlit, many underexposed frames).

USABLE RANGES
- 0:47-1:00: submarine conning tower silhouetted as she comes in (Midway/Pearl arrival proxy, act 15).
- 1:03-1:10: conning tower and deck gun, crew on deck (act 15).
- 1:11-1:16: crowd on the pier, harbour behind (Guam 1945; act 15 proxy).
- 1:28-1:50: men handle lines on the deck, hills behind (act 15 "tied up at Midway" proxy).
- **1:53-2:05: submarine alongside, hull and conning tower, men lined up on deck** (submarine on the surface; act 15).
- 2:08-2:26: crew and passengers lined along the deck, waving (act 15).
- 2:27-2:38: line of men on deck, low angle against sky (act 15).
- 2:49-3:02: rescued airmen and crew group on the deck in front of the conning tower (act 15 group photo echo;
  wide only).
- 3:35-4:00: view over the bow, men on deck, harbour shore and ships ahead (Guam 1945; act 16 "by Guam").

RISKY RANGES: 0:00-0:45 very dark, hard to read; 1:19-1:22 blurred close faces; **2:39-2:47 and 3:03-3:33 close faces
of rescued airmen (could be read as Bush and the Finback group; label Tigrone 1945 if used)**; 4:02-end dark.

---

## 17. `wolverine_training_1943.mp4` (NPC-5074, USS Wolverine, Lake Michigan, 14 Jul 1943)

- 1280x720, 4:03, B&W, very soft and dark. **Huge burned-in timecode at mid-height** (x 23-72 %, y 73-83 %). Poor.

USABLE RANGES (only with a crop to the top ~70 %)
- 0:06-0:11: trainer takes off over the deck (training carrier, act 4).
- 0:14-0:30: plane low over the deck, approach (training landings, act 4).
- 0:54-1:00: plane on deck, signal officer silhouette (act 4).
- 1:14-1:28: the training carrier on the lake, long shot (act 4 "first carrier landings").
- 2:35-2:40: plane on final approach (act 4).
- 2:47-2:50: plane low over the deck (act 4).
- 3:00-3:13: carrier side profile, plane landing (act 4).
- 3:20-3:25: **paddle-wheel churning at the side** (identifies a Lake Michigan training carrier; act 4).
- 3:30-3:40: carrier with funnel smoke on the lake (act 4).
- 3:52-4:01: plane takes off over the carrier (act 4).

RISKY RANGES: whole file (timecode); 1:31 and 2:19 white frames; 2:03 black; 2:27-2:28 white; 1:02-1:11 confusing
close-ups.

---

## 18. `tang_lifeguard_1944.mp4` (file labelled 428-NPC-4369)

- 720x480 (4:3), 2:30, B&W. **Wrong content, burned-in RTC timecode throughout. Useless for this episode.**
- Content: 0:00-0:05 "428.NPC 004369" card; 0:06 slate "FRANKLIN Roll 51 2/18/45"; 0:08-1:12 gun crews firing AA
  aboard a carrier; 1:13-1:17 slates "2/19/45 Iwo Jima Southern Tip", "2/20/45 Iwo Jima 3rd Div goes ashore";
  1:18-1:57 Marines climb down nets into landing craft; 1:58 slate "2/21/45"; 2:01-2:22 landing craft circling;
  2:24-end grey/black.
- Only conceivable use: act 17 (Feb 1945, fleet back for Iwo Jima) 2:01-2:22 landing craft, with a crop. Prefer to skip.

---

## 19. Bush interviews (face ranges only)

### `bush_interview_1986.mp4` (Reagan Library, 19 Jun 1986)
- 720x480 (4:3), 16:09, colour video, sharp. One camera, in-camera zooms, **no cutaways, no other people**.
- 0:00-4.8: text card (date, Master Tape #667, credit). RISKY.
- Bush's face clean from **0:05 to 16:09** throughout. Framing (approximate, zooms are gradual):
  wide (seated, Barbara's photo at left) 0:05-~1:20, ~3:05-~5:20, ~9:50-~10:40, ~11:30-~13:00, ~15:15-16:09;
  medium close-up ~1:25-~2:55, ~5:25-~9:45, ~10:50-~11:20, ~13:10-~15:05.

### `bush_stinnett_1992.mp4` (MT3897, White House, 2 Jun 1992)
- 960x706 (4:3 inside), 15:43, colour video, good. One camera, **no cutaways**; Stinnett's questions are off camera.
- 0:00-5.0: Bush Library title card. RISKY.
- Bush's face clean from **0:05 to 15:43**. Wide (US flag at left) 0:05-~0:36; medium close-up ~0:37-15:43, slightly
  tighter at times (e.g. ~8:40-~10:40). He gestures out of frame at ~5:24, ~7:02, ~9:59 (brief).
- Transcript with timings: `assets/footage/bush_stinnett_1992.mp4.txt`.

### `bush_powmia_1992.mp4` (MT3192, POW-MIA families, 24 Jul 1992)
- 960x706 (4:3 inside), 2:58, colour video, good. One camera, zooms, **no cutaways**.
- 0:00-5.1: Bush Library title card. RISKY.
- Medium shot of Bush at the presidential lectern, face clear: **0:05-0:30** and **1:45-2:56**.
- Zoom-out 0:30-0:37; wide shot with POW-MIA flag and two panel members at the table 0:37-1:36 (Bush small);
  zoom-in 1:36-1:45. A photographer crosses the foreground 0:41-0:44 and 0:53-0:56.
- 2:56.5-end: a woman in red stands up (applause), end of tape.
- Transcript: `assets/footage/bush_powmia_1992.mp4.txt`.

---

## Best shots for key beats

| Beat | Film and range | Notes |
|---|---|---|
| Carrier deck at dawn | `fighting_lady_out_b` 0:52-0:58 (sunset/dawn silhouettes, crop TC); `independence_ops_1944` 5:38-6:05 (planes warming up, backlit) | `independence_tbf_1943` 2:37-2:50 for B&W |
| Launch of an Avenger | `independence_tbf_1943` 0:00-0:11 and 2:52-3:01 (real TBFs, CVL deck, no TC) | `san_jacinto_1944` 2:09-2:45 for Bush's own deck (Hellcats, crop TC) |
| Avenger in flight | `kwajalein_strike_1944` 0:20-0:31 (TBF "18" close, crop TC); `fighting_lady_out_b` 0:59-1:19 (TBM formation, colour) | no-TC option: `independence_tbf_1943` 1:31-1:55 |
| Glide-bombing dive / bombs on an island | `chichi_bombing_1944` 1:13-1:30 (**bombs on Chichi Jima itself**, 27 Sept 1944); `kwajalein_strike_1944` 4:59-5:05 and 1:30-1:47; `fighting_lady_out_a` 3:03-3:25 (dive on ship by island) | |
| Heavy flak bursts | `san_jacinto_attack_1945` 1:05-1:18 (sky full of black bursts); 0:33-0:46 (battleship in bursts) | `chichi_b24_1944` 4:50-5:05 flak over an island (island unconfirmed) |
| Damaged or smoking plane | `fighting_lady_out_a` 4:48-4:56 (plane falls trailing smoke, splash at 4:52.8; crop TC, unidentified) | `fighting_lady_out_a` 1:53-2:01 black smoke as abstract "engine on fire"; nothing shows a burning Avenger |
| Parachute / man in the water | `aviator_rescue_1945` 0:12-0:22 and 0:34-0:52 (aviator in yellow vest) | no parachute descent in any film |
| Life raft | `finback_rescue_1944` 22.8-27.0 (**Bush's actual raft**) | only raft in the set (Tang film is the wrong reel) |
| Submarine surfacing / on the surface | `tigrone_guam_1945` 1:53-2:05 (sub alongside, men on deck); `finback_rescue_1944` 16.6-22.7 (Finback's own deck) | no surfacing shot exists in the set |
| Airmen climbing onto a submarine | `finback_rescue_1944` 27.0-34.7 (pilot hauled aboard) then 37.7-41.5 (Bush walks aft) | |
| Submarine interior or crew | `finback_rescue_1944` 42.5-44.6 (crewmen, deck gun, flag); `tigrone_guam_1945` 2:08-2:38 (crew on deck) | **no interior footage anywhere** |
| Chichi Jima seen from the air | `chichi_b24_1945` 2:41.5-2:48 (oblique, 22 Mar 1945); `chichi_bombing_1944` 0:43-0:57 (oblique, 1944) | `chichi_bombing_1944` 0:19-0:30 vertical |
| Chichi Jima harbour | `chichi_b24_1945` 2:55.5-2:59 (waterfront under smoke) | from sea level: `chichi_surrender_a` 1:01-1:22, `chichi_surrender_b` 5:17-5:45 (coast) |
| B-24s over the Bonins | `chichi_bombing_1944` 2:13-2:20 and 2:27-2:58 (B-24s on the 27 Sept 1944 Chichi Jima mission) | `chichi_b24_1944` 2:18-2:26 (Chichi Jima strike, Nov 1944) |
| Surrender aboard Dunlap | `chichi_surrender_a` 2:22.9-2:35.0 (Tachibana, probable, climbs aboard), 5:18-5:25 (walks deck), 5:59-6:30 (signs) | no ladder salute by him; `chichi_surrender_b` 1:37.5-1:45 other officers salute |
| Training carrier landings | `san_jacinto_attack_1945` 2:48.5-2:57 (Hellcat lands over the stern, sharp); `wolverine_training_1943` 3:00-3:25 (Lake Michigan paddle-wheel carrier, poor, crop TC) | `fighting_lady_out_b` 3:16-3:22 |
| Midway or Pearl arrival | `tigrone_guam_1945` 1:53-2:05 and 3:35-4:00 (sub arrives in port, Guam 1945, label honestly) | no Midway/Pearl footage |
| Guam 1945 | `tigrone_guam_1945` 1:11-1:16, 1:53-2:26, 3:35-4:00 | |
