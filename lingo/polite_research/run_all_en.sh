#!/bin/bash
cd /home/user/Test/lingo/polite_research
for L in English Japanese Korean French Spanish German Italian Portuguese Arabic Chinese Russian Turkish Hindi Persian Dutch Swedish Polish Thai Vietnamese Indonesian Khmer Tibetan Javanese Burmese Malay Balinese Sundanese Tamil Lao Bengali Urdu Tagalog Marathi Nepali Sinhalese Mongolian Malayalam Telugu Kannada Dzongkha Gujarati Punjabi Cebuano Ilocano Samoan Tongan Hawaiian Maori Fijian Amharic Swahili Yoruba Hausa Igbo Zulu Xhosa Wolof Akan Somali Greek Czech Hungarian Finnish Romanian Ukrainian Bulgarian Serbo-Croatian Danish Norwegian\ Bokmål Catalan Hebrew Georgian Armenian Azerbaijani Kazakh Uzbek Uyghur Pashto Kurdish Sanskrit Pali Okinawan Ainu Manchu Yakut Tatar Bashkir Chuvash Hmong Shan Mon Karen Acehnese Minangkabau Madurese Buginese Makasar Sasak Tetum Chamorro Malagasy; do
  [ -s "data_en/$L.cand.jsonl" ] && [ "$L" != "Japanese" ] && continue
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$L")
  code=$(curl -s -o /dev/null -w '%{http_code}' -A 'LingoDudeVideoBot/0.1' "https://kaikki.org/dictionary/$enc/kaikki.org-dictionary-$(echo $enc | sed 's/%20//g').jsonl" --head)
  url="https://kaikki.org/dictionary/$enc/kaikki.org-dictionary-$(echo $L | tr -d ' ').jsonl"
  curl -s -f -A 'LingoDudeVideoBot/0.1' "$url" | python3 extract_en.py "$L" data_en 2>>run_all_en.log || echo "FAILED $L" >> run_all_en.log
  echo "done $L $(wc -l < data_en/$L.cand.jsonl 2>/dev/null)" >> run_all_en.log
done
echo ALLDONE >> run_all_en.log
