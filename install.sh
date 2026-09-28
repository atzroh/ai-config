#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
packages=(claude codex)

# --adopt overwrites package files with conflicting ones, so refuse to run on uncommitted changes
if ! git diff --quiet -- "${packages[@]}"; then
  echo "error: uncommitted changes in ${packages[*]}" >&2
  exit 1
fi

# Adopt conflicting files, show what they contained, then restore the repo versions
stow --adopt --no-folding -R "${packages[@]}"
git --no-pager diff -- "${packages[@]}"
git checkout -- "${packages[@]}"
