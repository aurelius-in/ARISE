#!/usr/bin/env bash
MINUTES=${1:-5}
BRANCH="develop"

if ! git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  git checkout -B "$BRANCH"
else
  git checkout "$BRANCH"
fi

while true; do
  echo "Working for $MINUTES minutes..."
  sleep $(( MINUTES * 60 ))

  git add -A
  if git diff --cached --quiet; then
    git push -u origin "$BRANCH" >/dev/null 2>&1 || true
  else
    msg="chore: checkpoint $(date +%Y-%m-%d_%H-%M)"
    git commit -m "$msg"
    git push -u origin "$BRANCH"
  fi

  read -rp "Type 'c' to continue another $MINUTES min; anything else to stop: " answer
  if [[ "$answer" != "c" ]]; then
    break
  fi
done

