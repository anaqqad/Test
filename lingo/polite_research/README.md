# Politeness-word database (research for "Ranking the World's Most Polite Languages")

Built 2026-10-24. Everything here is reproducible from the scripts; nothing was typed in by hand except the rules.

## Files (deliverables)

| | File | What it is |
|---|---|---|
| A | `out/master.csv` | One row per lemma per language: lemma, merged spelling variants, transliteration, part of speech, categories (1-12), English gloss, evidence (the label or definition that qualified it), sources, source URLs, confidence, date accessed, audio status |
| B | `out/language_summary.csv` | Per language: total, per-category counts, functional vs register words, formative-derived words, sources and how many lemmas each supplied, lemmas only one source has, coverage, known sources not used |
| C | `out/source_inventory.csv` | Every source used, consulted, or found but inaccessible, with licence and why |
| D | `out/exclusions.csv` | Every candidate that was rejected and the rule that rejected it (and whether the word still counts through another sense) |
| E | `out/ranking_audit_table.md` + the "Ranking audit" section below | Preliminary vs expanded ranking |
| F | `out/shortlist.csv` | 20 example words per top language with evidence URL and audio status on Wikimedia Commons |

Scripts: `extract_en.py` (English Wiktionary, per language), `scan_editions.py` (16 native Wiktionaries), `extract_dicts.py`
(JMdict, CC-CEDICT), `extract_javanese.py` (Poedjosoedarmo's Javanese list), `classify.py` (one rule set for all sources,
merging, deliverables A and D), `report.py` (B, C, E), `audio_check.py` (F). Raw downloads (`dicts/`) and first-pass
extraction (`data_en/`) are not committed.

## 1. Audit of the first (four-Wiktionary) method

The first count took every word labelled polite/honorific/humble/royal in four Wiktionary editions. Its blind spots:

1. **It only sees labels, not functions.** Wiktionary labels a word "polite" when it is a polite *variant* of another word.
   Languages with grammaticalised honorific vocabularies (Japanese, Korean, Thai, Javanese) get labelled thousands of
   times; languages that are polite with ordinary words get almost nothing. English came out with 44 words and was
   missing *please*, *sorry* and *thank*, while including capitalised pronouns for God.
2. **"Formal" was counted as "polite".** Khmer's 81 were mostly words labelled *formal* (75 of them), which the mission
   excludes as merely formal.
3. **Spelling variants were only partly merged** (Japanese by reading only, which can merge different words with the
   same reading; Korean Hanja spellings counted next to their Hangul spellings).
4. **Coverage = Wiktionary editors' interest.** Thai's 618 came almost entirely from the Thai Wiktionary's royal
   vocabulary category; Javanese's 149 was a fraction of what the scholarly literature documents.
5. **No specialist dictionaries or academic sources**, so no way to tell an undercount from a real difference.

## 2. Sources and passes

1. **English Wiktionary, ~110 languages** (kaikki.org extraction, streamed). A sense qualifies through a politeness tag
   (honorific, humble, polite, respectful, deferential), a royal/monastic register note ("of a royal person", "of monks"),
   a politeness category, or a definition that states the word's own politeness function (makes a request polite,
   thanks, apologises, is a respectful title/term of address, is a respectful pronoun, is the honorific/humble form of X).
2. **Specialist dictionaries:** JMdict (Japanese; `hon`/`hum`/`pol` tags), CC-CEDICT (Chinese; polite/honorific/humble labels).
3. **Academic source:** Poedjosoedarmo, *Wordlist of Javanese Non-Ngoko Vocabularies* (Cornell, *Indonesia*), the standard
   list of Javanese Krama and Krama Inggil/Andap stems. OCR'd; columns recovered from coordinates (confidence "medium").
   Searched but not available as open text: Thai Royal Institute rachasap lists, Korean NIKL dictionaries, the Tibetan
   zhesa dictionaries, Khmer royal-vocabulary books (Kbuon Reach Sap, Chuon Nath), Burmese MLC dictionary, KBBI/Kamus Dewan.
4. **16 native Wiktionary editions** (ja, ko, zh, th, vi, id, ms, it, pt, tr, pl, es, nl, ru, de, fr): senses whose labels or
   definitions put the word in a politeness register in the edition's own language (尊敬語/謙譲語/丁寧語, 높임말/겸양어,
   敬辭/謙辭, ราชาศัพท์/คำสุภาพ, kính ngữ, krama inggil/bahasa halus, formule de politesse, Höflichkeitsform, …).
5. **One rule set** (`classify.py`) applied to every candidate from every source (below).
6. **Merging:** Chinese traditional→simplified (OpenCC), Japanese kanji/kana spellings (JMdict spelling groups, then
   kana-only spellings joined to the single kanji spelling with that reading), Korean Hanja→Hangul, case and diacritics
   for Latin-script languages, old Javanese spelling (dj, tj, nj, j) → modern.
7. **Audio** checked only for the shortlist, after counting. It never changes a count or a rank.
8. **Saturation check:** for each language, the share of lemmas that only one source has (`language_summary.csv`). A high
   share means another source would still change the count.

### Rules

Counted: a single standalone word (not a phrase, idiom, proverb, affix, grammatical ending or counter) whose politeness
function or register is stated by a source. Each lemma once per language; inflected forms and alternative spellings are
not counted separately.

Not counted (each rejection is logged in `exclusions.csv`):
- merely *formal* words; words that only *describe* politeness (polite, courteous, humble, grateful);
- archaic, obsolete, historical senses; slang, Internet, humorous, baby-talk, sarcastic, proscribed senses;
- regional varieties outside the standard language (Philippine/Indian/Singapore English, Kansai Japanese, and for
  "Chinese" everything that is not Standard Mandarin: Cantonese, Hokkien, Hakka, Wu, Classical Chinese, …);
- courtesy interjections borrowed whole from another language (*merci* or *arigato* in English, *sorry* in German);
- general modal verbs whose polite request is one use (*would*, *may*); legal "pardon"; condolence and plain regret;
- a label that one language's Wiktionary puts on *another* language's word (e.g. the Korean edition calling English
  "teacher" honorific) unless another source confirms it;
- the Chinese Wiktionary's "honorific" tag on European words (it marks an elevated literary style there, not politeness);
- everyday greetings, farewells and toasts that are only labelled as courtesy formulas.

Categories follow the mission: 1 request, 2 apology, 3 gratitude, 4 courtesy/polite register vocabulary, 5 honorific
title/address, 6 respectful pronoun, 7 honorific vocabulary, 8 humble vocabulary, 9 deferential, 10 royal register,
11 polite particle/interjection/greeting, 12 other documented (a politeness label without a more specific type).

## 3. Results

5,457 qualifying lemmas in 85 languages (out of ~101 languages searched); 35,194 rejected candidates are logged with
their reason (the biggest groups: 22,330 senses labelled only *formal*; 4,465 native-edition hits where the keyword
was incidental; 1,193 multiword expressions; 1,126 inflected or alternative forms).

| Rank | Language | Lemmas | What the count is made of | How complete |
|---|---|---|---|---|
| 1 | Japanese | 1,431 | 590 honorific (尊敬語), 260 humble (謙譲語), 294 polite (丁寧語/美化語), 75 pronouns, 122 thanks/sorry/please words. 419 of these are お-/ご-/御- forms | Strong: JMdict + English + Japanese Wiktionary agree on many; 36% come from one source only |
| 2 | Javanese | 916 | 610 Krama (polite register) stems + 289 Krama Inggil/Andap (honorific/humble) stems, almost all from Poedjosoedarmo's list | Depends on one academic list (86% single-source). Counting only honorific/humble words gives ~300 |
| 3 | Chinese (Mandarin) | 818 | 266 honorific (敬辞), 127 humble (谦辞), 124 polite, 81 thanks/sorry/please words | Strong: CC-CEDICT + English + Chinese Wiktionary; 27% single-source |
| 4 | Thai | 670 | 509 royal vocabulary (ราชาศัพท์), 98 polite words (คำสุภาพ) | One source: the Thai Wiktionary's royal-vocabulary category (89% single-source); the Royal Institute lists were not accessible |
| 5 | Korean | 192 | 102 honorific (높임말), 35 humble (겸양어) | Clearly undercounted: no open Korean dictionary with honorific labels; Korean politeness lives mostly in verb endings, which are not words |
| 6 | Burmese | 100 | 55 honorific, royal and monastic terms, titles (U, Daw, Ko) | One source (English Wiktionary) |
| 7 | English | 86 | 36 titles/terms of address (sir, madam, ma'am…), 11 thanks words, 9 apology words, please, kindly, polite euphemisms | Partial: definitions are searched for function; that is how *please*, *sorry*, *thank* now count |
| 8 | Tibetan | 52 | 45 honorific (zhesa) words | Undercounted: the zhesa dictionaries were not accessible |
| 9 | Indonesian | 50 | titles (Bapak, Ibu), royal words (bersantap, beradu), please/sorry/thanks | Partial |
| 10 | Malay | 49 | royal and polite words, titles | Partial |
| 11-25 | Polish 44, French 38, German 37, Tamil 35, Finnish 33, Portuguese 32, Spanish 32, Italian 30, Khmer 30, Persian 30, Russian 30, Swedish 30, … | mostly titles, the polite "you", please/sorry/thank words | These counts track Wiktionary coverage more than the languages |

Full per-language table: `out/language_summary.csv`; every word with its evidence: `out/master.csv`.

## 4. Ranking audit (preliminary → expanded)

See `out/ranking_audit_table.md` for the full table. What changed and why:

- **Japanese 848 → 1,431, still #1.** JMdict adds hundreds of tagged honorific/humble words; spelling merging is stricter.
- **Javanese 149 → 916, #5 → #2.** The scholarly list of non-Ngoko stems was added. This is the biggest single change and
  rests on one source; with Krama Inggil/Andap only, Javanese would be ~300 and rank #4.
- **Chinese 607 → 818, still #3.** CC-CEDICT added; Cantonese/Hokkien/Classical-only words removed.
- **Thai 618 → 670, #2 → #4.** Same royal-vocabulary source as before; nothing new was found to confirm or extend it.
- **Korean 262 → 192, still in the top 5.** Hanja spellings now merge with Hangul; labels that only the Japanese/Chinese
  Wiktionary put on Korean words need a second source. Korean is the language most likely undercounted.
- **Burmese 116 → 100**, proper names and archaic senses removed.
- **Vietnamese 90 → 18, out of the top 10.** Most of the 90 were chữ Hán/Nôm spellings or labels from other editions.
- **Khmer 81 → 30, out of the top 10.** 75 of the 81 were words labelled *formal*, not polite.
- **Tibetan 48 → 52, English 44 → 86, Indonesian 43 → 50, Malay 42 → 49.**

## 5. Can we name a defensible top 10?

**No, not as an exact order.** What the data supports:

1. **A clear top group: Japanese, Chinese, Javanese, Thai.** Each has hundreds of documented politeness-register words in
   at least one curated source. Japanese and Chinese are the best supported (several independent sources agree).
   The order inside this group depends on choices, not facts: Javanese moves from #2 to #4 depending on whether its
   Krama (polite-register) vocabulary counts, and Thai's number comes from a single list.
2. **Korean belongs with them by every description in the literature**, but no open source lets us count its honorific
   words, so its 192 is a floor.
3. **Places 6-10 are not defensible.** Burmese, Tibetan, Indonesian, Malay, English and the European languages are
   separated by a few dozen words, and those differences follow Wiktionary coverage. Tibetan and Khmer have
   full honorific/royal vocabularies described in the literature that we could not access as open text.

Recommendation for the video: present the top group as the result and be explicit that the count is "politeness words
we could verify in open dictionaries", or present tiers (honorific-system languages vs. the rest) instead of a strict
1-10. If a strict ranking is kept, the honest order from this data is Japanese, Javanese, Chinese, Thai, Korean, Burmese,
English, Tibetan, Indonesian, Malay, with the caveats above on screen or in the description.

## 6. Audio (reported separately, did not affect any count)

`out/shortlist.csv` lists 20 example words for each of the top 15 languages, plus the signature words already used in
the current cut. Audio status comes from Wikidata lexemes linked to Lingua Libre recordings, checked one language per
minute because Wikidata's query service was rate-limiting during an outage on 2026-10-24; the Commons search API was
also rate-limiting (HTTP 429). "Not found" therefore means "not linked on Wikidata", not "no recording exists".

## 7. Known gaps

- No open digital text was found for: Thai Royal Institute rachasap lists, Korean NIKL dictionaries, Tibetan zhesa
  dictionaries, Khmer royal-vocabulary books, the Burmese MLC dictionary, KBBI/Kamus Dewan, Bausastra Jawa (not parsed).
- The Javanese list is OCR'd; ~170 cells were rejected as OCR noise or multiword, and a few column misreads may remain
  (confidence "medium" on those rows).
- Wiktionary's coverage is uneven between languages; the per-language "lemmas only one source has" share in
  `language_summary.csv` shows where another source would still change the count (Thai, Burmese, Tibetan, Javanese).
- Lexicalised compounds formed with honorific formatives (Japanese お-/ご-, Thai พระ-/ทรง-, Korean -님) are counted
  as dictionary headwords; `language_summary.csv` also gives each count without them.
