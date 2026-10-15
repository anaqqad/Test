# OPTION 2 (saved): "Same Language, Different Countries" (map-tour format)

Status: idea saved, not built yet. Owner liked this format (2026-10-13) and saved it as **option 2** (2026-10-15).
Owner's words: the original language says something first (e.g. France in French), then every other country that
speaks it says the same thing with its own word; same for Arabic (Saudi Arabia first, then all Arabic-speaking
countries), and so on, one language after another.

## Format
One video, several **chapters**, one per language. In each chapter:
1. **Start with the language's reference version.** The camera zooms to its "home" country (or Standard Arabic as a
   floating label), and the character says the phrase. A real native recording plays and the word card appears.
2. **Hop to the next country** that speaks the same language (the camera flies along a dotted line, no fake cloud).
   That country's character says **the same thing in its own version**, with a real recording and a word card.
3. Repeat for every country, keeping the funniest or most different version for **last**.
4. **Zoom out**: all versions stay on the map as cards (a visual comparison), then move to **the next language**.

Rules (from blueprints/LANGUAGE_VIDEO_BLUEPRINT.md and the owner's notes):
- Real native recordings only for the words (Wikimedia Commons / Lingua Libre / Wikitongues). If a version has no
  recording, swap that country, never fake it.
- Clouds fade on zoom (no fake cloud wipe), counter or word card on the country, big readable text.
- Music bed per country: public-domain anthem recordings, credited (as in the official-languages video).
- Each fact in the description, with sources for regional words.

## Chapters (draft order)
| # | Chapter | Countries / versions | Phrase or word |
|---|---|---|---|
| 1 | Arabic Isn't One Language | Standard Arabic, Morocco, Egypt, Lebanon, Iraq, Saudi Arabia | "How are you?": kayf halak (Standard) / labas (Morocco) / izzayak (Egypt) / kifak (Lebanon) / shlonak (Iraq) |
| 2 | Spanish Has Many Words for "Bus" | Spain, Mexico, Argentina, Chile, Cuba | autobús / camión / colectivo / micro / guagua |
| 3 | English Is Different Everywhere | UK, USA, Australia, India, South Africa | "traffic light" is "robot" in South Africa; "trousers" vs "pants" |
| 4 | French Can't Agree on Numbers | France, Belgium, Switzerland, Quebec, Senegal | 70 / 80 / 90: soixante-dix, septante, huitante (Switzerland, some cantons)… |
| 5 | Portuguese: Portugal vs Brazil vs Angola | Portugal, Brazil, Angola, Mozambique | "bus": autocarro / ônibus / machimbombo |
| 6 | German Says Hello 5 Ways | Germany (north and south), Austria, Switzerland | Moin / Servus / Grüß Gott / Grüezi |

Possible later chapters or standalone episodes: Chinese varieties ("thank you"), Malay vs Indonesian false friends,
Persian in 3 countries / 2 alphabets, and the "mother language and its children" journeys (Latin → Romance,
Turkic numbers 1–3, Germanic "night", Slavic "water", Bantu "person").

## To do before building
- Verify every regional word with a dictionary or source (e.g. Swiss huitante is regional; Mexican camión for bus).
- Find a real recording for each version; the Arabic dialects and the Swiss/Quebec French numbers are the hardest.
- Renderer: extend maptour.mjs with (a) word cards + recording per country instead of the counter,
  (b) a dotted flight path between countries, (c) chapter titles between languages.
- Length: about 6 chapters × 4–6 countries × ~8 s ≈ 4–5 minutes, or split into one Short per chapter.
