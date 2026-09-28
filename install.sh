#!/bin/bash
set -euo pipefail

# ==============================================================================
# ai-config installer
#   Links the packages in this repository into $HOME with GNU stow.
# ==============================================================================

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES=(claude codex)

# Back up regular files that would conflict with stow links
for pkg in "${PACKAGES[@]}"; do
  while IFS= read -r -d '' src; do
    rel="${src#"$REPO_DIR/$pkg/"}"
    dest="$HOME/$rel"
    if [[ -e "$dest" && ! -L "$dest" ]]; then
      backup="$dest.bak.$(date +%Y%m%d%H%M%S)"
      echo "[*] Backing up $dest -> $backup"
      mv "$dest" "$backup"
    fi
  done < <(find "$REPO_DIR/$pkg" \( -type f -o -type l \) -print0)
done

echo "[*] Stowing: ${PACKAGES[*]}"
stow -d "$REPO_DIR" -t "$HOME" -R "${PACKAGES[@]}"

echo "[*] Done"
