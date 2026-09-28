# ai-config

Claude Code と Codex の設定を管理するリポジトリ。GNU stow で `$HOME` 配下にシンボリックリンクを張る。

## 構成

```txt
.
├── shared
│  └── AGENTS.md          # 共通指示の実体 (唯一の編集対象)
├── claude                # stow package -> ~/.claude
│  └── .claude
│     ├── CLAUDE.md -> ../../shared/AGENTS.md
│     └── settings.json
├── codex                 # stow package -> ~/.codex
│  └── .codex
│     └── AGENTS.md -> ../../shared/AGENTS.md
└── install.sh
```

```txt
~/.claude/CLAUDE.md --> claude/.claude/CLAUDE.md --+
                                                   +--> shared/AGENTS.md
~/.codex/AGENTS.md  --> codex/.codex/AGENTS.md  ---+
```

## インストール

```sh
cd ~
git clone <this repo> ai-config
~/ai-config/install.sh
```

リンク先に既存の通常ファイルがある場合は `<name>.bak.<日時>` に退避してから stow する。何度実行しても問題ない。

## 設定の追加

- 共通指示: `shared/AGENTS.md` を編集する (Claude / Codex の両方に反映される)
- Claude 専用: `claude/.claude/` 配下に置く (例: `agents/`, `commands/`, `skills/`, `hooks/`)
- Codex 専用: `codex/.codex/` 配下に置く (例: `config.toml`, `rules/`)

追加後は `./install.sh` を再実行する。新しいツールを追加する場合は `<tool>/.<tool>/...` のパッケージを作り、`install.sh` の `PACKAGES` と `.gitignore` に追記する。

`~/.claude` / `~/.codex` 自体は実ディレクトリのまま残り、ファイル単位でリンクされるため、セッション履歴や認証情報がリポジトリに入ることはない。
