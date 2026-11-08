#!/bin/bash
IFS=$'\t' read -r name ref prompt <<< "$1"
args=(--skip-git-repo-check -s workspace-write)
[ "$ref" = ref ] && args+=(-i ref_wojaks.png)
args+=(-o "last_$name.txt")   # -i takes several files: it must not come right before the prompt
timeout 900 codex exec "${args[@]}" "$prompt" < /dev/null > "log_$name.txt" 2>&1; echo "$name exit $?"
