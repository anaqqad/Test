#!/bin/bash
# worker for re-extraction; several can run at once (lock files in data_en2/.lock_*)
cd /home/user/Test/lingo/polite_research
for L in English Japanese Korean French Spanish German Italian Portuguese Arabic Chinese Russian Turkish Hindi Persian Dutch Swedish Polish Thai Vietnamese Indonesian Khmer Tibetan Javanese Burmese Malay Balinese Sundanese Tamil Lao Bengali Urdu Tagalog Marathi Nepali Sinhalese Mongolian Malayalam Telugu Kannada Dzongkha Gujarati Punjabi Cebuano Ilocano Samoan Tongan Hawaiian Maori Fijian Amharic Swahili Yoruba Hausa Igbo Zulu Xhosa Wolof Akan  Swahili Yoruba Hausa Igbo Zulu; do
  grep -qx "done $L" rerun_en.log && continue
  mkdir "data_en2/.lock_$L" 2>/dev/null || continue
  curl -s -f -A 'LingoDudeVideoBot/0.1' "https://kaikki.org/dictionary/$L/kaikki.org-dictionary-$L.jsonl" | python3 extract_en.py "$L" data_en2 2>>rerun_en.log || echo "FAILED $L" >> rerun_en.log
  echo "done $L" >> rerun_en.log
done
