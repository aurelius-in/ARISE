#!/usr/bin/env bash
MINUTES=${1:-5}
BRANCH="develop"

if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git checkout -B "$BRANCH"
else
  git checkout "$BRANCH"
fi

human_msg() {
  files=$(git diff --cached --name-only)
  [ -z "$files" ] && echo "small updates" && return
  labels=()
  while IFS= read -r f; do
    case "$f" in
      src/ui/*) labels+=(UI) ;;
      src/core/*) labels+=(pipeline) ;;
      tests/*) labels+=(tests) ;;
      data/*) labels+=(data) ;;
      reports/*) labels+=(reports) ;;
      architecture_RM-ODP/*) labels+=("architecture docs") ;;
      ai_approaches/*) labels+=("ai approaches") ;;
      ai_research/*) labels+=("ai research") ;;
      knowledge_exchange/*) labels+=(comms) ;;
      market/*) labels+=(market) ;;
      software/*|.streamlit/*) labels+=(dev/deploy) ;;
      .gitignore|.gitattributes) labels+=("repo setup") ;;
      README.md) labels+=(readme) ;;
      dev/*) labels+=("dev tooling") ;;
    esac
  done <<< "$files"
  # unique labels
  uniq=()
  for l in "${labels[@]}"; do
    skip=false
    for u in "${uniq[@]}"; do [ "$u" = "$l" ] && skip=true && break; done
    $skip || uniq+=("$l")
  done
  if [ ${#uniq[@]} -eq 0 ]; then echo "small updates"; else echo "update ${uniq[*]// /, }"; fi
}

while true; do
  echo "Working for $MINUTES minutes..."
  sleep $(( MINUTES * 60 ))

  git add -A
  if git diff --cached --quiet; then
    git push -u origin "$BRANCH" >/dev/null 2>&1 || true
  else
    msg=$(human_msg)
    git commit -m "$msg"
    git push -u origin "$BRANCH"
  fi

  read -rp "Type 'c' to continue another $MINUTES min; anything else to stop: " answer
  if [[ "$answer" != "c" ]]; then
    break
  fi
done

