# Infinite Language Generator (paused)

Started 2026-11-25, then paused by the owner ("stop new project, complete the Finnish video").
Brief: `lingo/ideas/infinite_language_generator.md`. To move into the owner's new repository when it exists.

Done so far:
- `data/concepts.json`: 19,539 English base concepts (lemma + main part of speech), ranked by frequency.
  Built by `tools/build_concepts.mjs <wordnet dict dir>` from wordfreq's English list (`data/freq_raw.txt`,
  wordfreq data CC BY-SA 4.0) and WordNet 3.1 index files (npm `wordnet-db`, WordNet licence), lemmatised with
  compromise. `data/closed_class.txt` = function words handled by grammar, `data/blocklist.txt` = slurs left out.
- Plan: seeded engine (phonology by aesthetic, POS-neutral roots, grammar parameters, generated script),
  compromise-based English parser -> structured clauses -> conlang, reverse by affix stripping; AES-256-GCM
  (Web Crypto) bytes -> language syllables; static website; AI test harness needs API keys + owner approval.
