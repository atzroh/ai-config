#!/bin/bash
set -uo pipefail

# The Desktop app sends its own notifications
[[ "${CLAUDE_CODE_ENTRYPOINT:-}" == "claude-desktop" ]] && exit 0

input=$(cat)
event=$(jq -r '.hook_event_name // empty' <<<"$input")
dir=$(basename "$(jq -r '.cwd // empty' <<<"$input")")

case "$event" in
  Notification) body=$(jq -r '.message // "入力を待っています"' <<<"$input") ;;
  Stop) body="応答が完了しました" ;;
  *) exit 0 ;;
esac

notify-send -a "Claude Code" "Claude Code: ${dir}" "$body" 2>/dev/null || true
