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
