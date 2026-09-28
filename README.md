# AI Config

Claude Code と Codex の設定を管理するリポジトリ。GNU stow で `$HOME` 配下にシンボリックリンクを張る。

## 構成

```txt
.
├── shared
│  └── AGENTS.md          # 共通指示の実体 (唯一の編集対象)
├── claude                # stow package -> ~/.claude
│  └── .claude
│     ├── CLAUDE.md -> ../../shared/AGENTS.md
│     ├── settings.json
│     ├── statusline.sh   # statusLine の表示
│     └── hooks
│        └── notify.sh    # CLI 用のデスクトップ通知
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

何度実行しても問題ない。`~` 直下に clone すること (stow のターゲットはリポジトリの親ディレクトリになる)。

リンク先に既存の通常ファイル (例: `~/.claude/settings.json`) がある場合は `stow --adopt` でリポジトリ側に取り込み、その差分を表示してから `git checkout` でリポジトリの版に戻す。既存ファイルの内容は破棄されるので、必要なら表示された差分から拾う。`claude/` / `codex/` に未コミットの変更があると、上書きを防ぐためエラーで止まる。

## 設定の追加

- 共通指示: `shared/AGENTS.md` を編集する (Claude / Codex の両方に反映される)
- Claude 専用: `claude/.claude/` 配下に置く (例: `agents/`, `commands/`, `skills/`, `hooks/`)
- Codex 専用: `codex/.codex/` 配下に置く (例: `config.toml`, `rules/`)

追加後は `./install.sh` を再実行する。新しいツールを追加する場合は `<tool>/.<tool>/...` のパッケージを作り、`install.sh` の `stow` の引数と `.gitignore` に追記する。

`~/.claude` / `~/.codex` 自体は実ディレクトリのまま残り、ファイル単位でリンクされるため、セッション履歴や認証情報がリポジトリに入ることはない。
