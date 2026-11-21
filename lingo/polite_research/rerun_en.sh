#!/bin/bash
# re-extract languages processed before etymology and royal/clerical raw tags were saved (runs alongside run_all_en.sh)
cd /home/user/Test/lingo/polite_research
mkdir -p data_en2
for L in English Japanese Korean French Spanish German Italian Portuguese Arabic Chinese Russian Turkish Hindi Persian Dutch Swedish Polish Thai Vietnamese Indonesian Khmer Tibetan Javanese Burmese Malay Balinese Sundanese Tamil Lao Bengali Urdu Tagalog Marathi Nepali Sinhalese Mongolian Malayalam Telugu Kannada Dzongkha Gujarati Punjabi Cebuano Ilocano Samoan Tongan Hawaiian Maori Fijian Amharic Swahili Yoruba Hausa Igbo Zulu Xhosa Wolof Akan  Swahili Yoruba Hausa Igbo Zulu; do
  url="https://kaikki.org/dictionary/$L/kaikki.org-dictionary-$L.jsonl"
  curl -s -f -A 'LingoDudeVideoBot/0.1' "$url" | python3 extract_en.py "$L" data_en2 2>>rerun_en.log || echo "FAILED $L" >> rerun_en.log
  echo "done $L" >> rerun_en.log
done
echo ALLDONE >> rerun_en.log
