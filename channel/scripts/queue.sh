#!/usr/bin/env bash
# Render jobs one after another, once any running render has finished. Detach it so it outlives the shell:
#   nohup bash scripts/queue.sh "battle-of-france-1940" "battle-of-france-1940 --short" > out/queue.log 2>&1 &
cd "$(dirname "$0")/.."
while pgrep -f "node scripts/render.mjs" >/dev/null; do sleep 30; done
for job in "$@"; do
  echo "== $job $(date +%H:%M)"
  node scripts/render.mjs $job --concurrency=4 2>&1 | grep -E "rendered in|wrote|Error|error"
done
echo "== done $(date +%H:%M)"
