#!/bin/bash
set -uo pipefail

# Prints: <model> (<effort>) | <dir> <branch>[*] | ctx N% | 5h N% 7d N%
input=$(cat)

IFS=$'\t' read -r model effort dir ctx five seven < <(jq -r '
  def pct: if type == "number" then (. | round | tostring) else "" end;
  [
    (.model.display_name // ""),
    (.effort.level // ""),
    (.workspace.current_dir // .cwd // ""),
    (.context_window.used_percentage | pct),
    (.rate_limits.five_hour.used_percentage | pct),
    (.rate_limits.seven_day.used_percentage | pct)
  ] | map(if . == "" then "-" else . end) | @tsv
' <<<"$input")

parts=()

if [[ "$model" != "-" ]]; then
  [[ "$effort" != "-" ]] && model+=" (${effort})"
  parts+=("$model")
fi

if [[ "$dir" != "-" ]]; then
  loc=$(basename "$dir")
  branch=$(git -C "$dir" --no-optional-locks branch --show-current 2>/dev/null)
  if [[ -n "$branch" ]]; then
    [[ -n "$(git -C "$dir" --no-optional-locks status --porcelain 2>/dev/null)" ]] && branch+="*"
    loc+=" ${branch}"
  fi
  parts+=("$loc")
fi

[[ "$ctx" != "-" ]] && parts+=("ctx ${ctx}%")

limits=""
[[ "$five" != "-" ]] && limits="5h ${five}%"
[[ "$seven" != "-" ]] && limits+="${limits:+ }7d ${seven}%"
[[ -n "$limits" ]] && parts+=("$limits")

out=""
for p in "${parts[@]}"; do
  out+="${out:+ | }${p}"
done
printf '%s\n' "$out"
