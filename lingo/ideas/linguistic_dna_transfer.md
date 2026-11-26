# Video concept: Linguistic DNA Transfer (saved 2026-11-26, not started)

Status: concept only. The owner said: "Do not start production yet."

## Titles
- Working title: **What If You Could Learn a Language Without Studying It?**
- I Tried Learning a Language by Slowly Replacing English
- Can You Learn Spanish Without Studying Spanish?
- I Created a Book That Changes Its Language as You Read

The final title must match what the experiment actually shows. We did not invent the method (see the references
below). Say so on screen and in the description: "an old idea, tested our way". "I Created a Book" refers only to
our own book or implementation, never to the technique.

## Concept
A text starts as 100% English and changes, page by page, into 100% Spanish. First single words switch (the most
frequent and the most guessable ones), then short phrases, then Spanish word order and grammar (adjective after the
noun, object pronouns before the verb, verb endings), until the last pages are plain Spanish. The reader never sits
down to "study": the meaning comes from the context of a story they can already follow.

The video is an experiment, not a tutorial: explain the idea with visuals, show where it comes from, build our own
version, test it on real people against a normal method, and report what actually happened.

## Research references (check each one before it goes on screen)
Background and prior art:
- **Diglot reading / diglot weave.** Robbins Burling proposed reading material that shifts gradually from the
  learner's language into the target language: "Some outlandish proposals for the teaching of foreign languages",
  Language Learning 18 (1968). (Verify the page numbers.)
- **"Diglot Weave"** is the name used by the Power-Glide language courses (Robert W. Blair, Brigham Young
  University, 1980s–90s). Verify who coined the term and whether it was a trademark before naming it on screen.
- **Patent application US20160019816A1, "Language Learning Tool"** (https://patents.google.com/patent/US20160019816A1/en).
  - Filed 2015-07-16 by Nimble Knowledge LLC; inventors Kent Parry and Dan Masterson; published 2016-01-21.
  - Status on Google Patents: Abandoned.
  - Abstract: a user profile records which target-language words the user knows. Those words replace the
    source-language words in a text, and clicking a word switches it between the two languages, with the result
    saved back to the profile.
  - The video can show it as one modern attempt to automate the idea: an abandoned application, not a granted
    patent. This note is not legal advice.
- **Products that already do partial versions:** for example the Toucan browser extension, which swaps some words
  on web pages into a target language. Survey the current ones before production; there are probably more.
- **Macaronic texts:** writing that mixes two languages on purpose, a centuries-old literary practice.

Learning science to ground the experiment:
- **A Clockwork Orange study:** Saragi, Nation & Meister, "Vocabulary learning and reading", System 6 (1978).
  Readers picked up many of the novel's invented Nadsat words just by reading, without being told to learn them.
  This is the closest classic evidence for incidental learning from a "mixed" text.
- **How many words a reader must know:** Hu & Nation, "Unknown vocabulary density and reading comprehension",
  Reading in a Foreign Language 13 (2000). Readers need about 98% of the words to read comfortably; Laufer (1989)
  gives about 95% as a minimum. This sets the maximum amount of new Spanish per page.
- **How often a word must be met:** Waring & Takaki, "At what rate do learners learn and retain new vocabulary
  from reading a graded reader?", Reading in a Foreign Language 15 (2003). Words met only a few times were mostly
  forgotten; many more encounters were needed for retention. This sets the repetition schedule.
- **Comprehensible input:** Krashen's input hypothesis (1980s); graded readers and extensive reading.
- **Possible limits to test:** grammar may be harder to pick up than vocabulary this way; English-like Spanish
  word order in the middle stages could teach wrong patterns; spelling, pronunciation and speaking are not trained.

## Our experimental implementation (to build later)
1. **Source text:** a public-domain English story (Project Gutenberg), about 10,000–20,000 words.
   - The Spanish version is ours. A native Spanish speaker checks it; no unchecked machine translation goes into
     the final book.
2. **Replacement schedule**, in stages, from 0% to 100% Spanish:
   - Stage A, single words: cognates and near-cognates first (*animal*, *chocolate*, *hospital*), then frequent
     nouns, adjectives and verbs (*casa*, *perro*, *grande*, *come*).
   - Stage B, function words: *el/la*, *y*, *de*, *en*, *que*, *no*.
   - Stage C, short phrases: *por favor*, *tengo hambre*, *¿qué pasa?*.
   - Stage D, grammar: Spanish word order (noun before adjective), gender agreement, object pronouns before the
     verb, verb endings.
   - Stage E: full Spanish.
3. **Rules for each page:**
   - At most about 2–5% of the words are new to the reader (Hu & Nation; Laufer).
   - Each new word is shown in bold the first time.
   - Each word comes back many times, spaced across later pages (Waring & Takaki).
   - Never two new things in the same sentence.
4. **Reader tool:**
   - A web page or e-book where tapping a word shows the other language. This tap-to-switch idea is close to
     the patent application above.
   - It logs which words were tapped, so the results can show which words needed help.
   - Free, runs in the browser, no paid APIs.
5. **Whole books:** the same pipeline on a full novel, to see whether a book-length version is feasible. Things to
   measure:
   - translation-checking time per chapter;
   - how many unique Spanish words the book introduces;
   - how many encounters each word gets.

## Experiment design
- **Question:** after the same reading time, do beginners who read the progressive text remember more Spanish
  words, and understand a plain-Spanish passage better, than beginners who studied the same words in a
  conventional way?
- **Participants:**
  - Absolute Spanish beginners who know English well, for example volunteers from the audience or friends.
  - Exclude anyone who studied Spanish or a close language such as Portuguese, Italian or French.
  - Get consent. Publish only first names or no names.
  - Aim for at least 20 per group. If it ends up smaller, say on screen that it is a small demonstration, not a
    study.
- **Groups**, same total time (for example 4 × 30 min over one week) and the same list of target words:
  - A, progressive text: reads our English-to-Spanish book.
  - B, flashcards: learns the same words with a spaced-repetition app, plus a short grammar sheet.
  - C, parallel text: reads the same story with the Spanish and the English side by side.
  - Optional: a control group with no study, for the effect of the tests themselves.
- **Tests:**
  - Pre-test: a check on the target words, plus made-up "pseudo-words" to catch guessing.
  - Immediate post-test and delayed post-test (7 days later). Each contains:
    - meaning recall (Spanish word → write the English);
    - form recall (English → write the Spanish);
    - a short, unseen, 100% Spanish passage made only of the target words, with 10 comprehension questions.
- **Scores:** percent correct per test. Report the average per group, the spread, and how much was forgotten
  between the immediate and delayed tests.
  - Decide the scoring rules before testing; save the raw answers; never edit results.
- **Honesty rules:**
  - Same instructions and same time for every group.
  - Show the results that came out, including if the progressive text does not win.
  - Explain any limits: small groups, one language pair, a short time.

## Possible visual sequences
- **The DNA helix:** an English sentence twists like a double helix, and on every turn one more word flips into
  Spanish, until the strand is fully Spanish (the "Linguistic DNA Transfer" title shot).
- **The page that changes:** one page shown at 0%, 25%, 50%, 75% and 100% Spanish, with Spanish words highlighted
  as they arrive and a progress bar ("Book: 37% Spanish").
- **Word-order morph:** "the black cat" → "the cat black" → "el gato negro", with the words physically sliding into
  place.
- **Timeline of prior art:**
  - Burling's 1968 proposal;
  - Power-Glide's "diglot weave";
  - the 2015 patent application zooming in to an "ABANDONED" status stamp;
  - today's browser extensions;
  - then "our version".
- **Clockwork Orange callback:** a few Nadsat words on screen ("droog", "moloko") and the 1978 study result.
- **Book heat-map:** a whole novel drawn as a strip of pages, coloured from English blue to Spanish red, showing
  where each stage starts.
- **Experiment scenes:** three Wojak groups (book, flashcards, parallel text) with a clock and equal time bars.
- **Results:** test scores rising bar by bar, immediate vs one week later; the moment someone reads a 100% Spanish
  paragraph out loud.
- **Real recordings:**
  - A native speaker reading the final Spanish paragraph. The channel rule is real recordings only, so use our
    own recorded volunteer or a free-licence recording, never synthetic speech, unless the owner decides
    otherwise.
  - Learners reading it after the week.

## Open decisions for the owner (before production)
- Format: a normal 16:9 video (channel style, 3–5 min) or a Short? Narrated or text cards only?
- Target language: Spanish (many English cognates, a large audience), or let viewers vote.
- Who the participants are, and how many we can realistically recruit.
- Which public-domain story to use, and who checks the Spanish.
- Whether the reader tool and the book are published for viewers (free website), and where.
