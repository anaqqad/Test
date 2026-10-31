#!/bin/bash
cd /home/user/Test/lingo/polite_research
for ed in jawiktionary kowiktionary idwiktionary mswiktionary viwiktionary thwiktionary zhwiktionary itwiktionary ptwiktionary trwiktionary plwiktionary eswiktionary nlwiktionary ruwiktionary dewiktionary frwiktionary; do
  [ -s data_ed/$ed.jsonl ] && continue
  curl -s -f -A 'LingoDudeVideoBot/0.1' "https://kaikki.org/$ed/All%20languages%20combined/kaikki.org-dictionary-all.jsonl" | python3 scan_editions.py $ed data_ed 2>>run_editions.log || echo "FAILED $ed" >> run_editions.log
done
echo ALLDONE >> run_editions.log
