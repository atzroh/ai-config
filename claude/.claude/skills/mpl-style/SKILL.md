---
name: mpl-style
description: The user's house style for every graph or plot made with Python (matplotlib, including seaborn or pandas .plot, which draw through matplotlib) - Okabe-Ito colors, Computer Modern fonts, size presets for paper (3.5in), paper-wide (7.0in) and slide (16:9), English labels with units like `Time $t$ [s]`, error bars, colormaps, reference lines, and saving to figures/ as PNG (300dpi) or PDF (asks which each time). Comes with a helper module (use_style, color_map, save). Use this skill whenever Python code is about to draw a chart, graph, plot, figure, heatmap, histogram, or any data visualization (e.g. 「グラフにして」「プロットして」「図を作って」「論文用の図」「スライド用のグラフ」「可視化して」), for reports, papers, slides, notebooks, or blog figures, even if the user does not mention style or matplotlib. Do not use it for Mermaid or other structural diagrams, or for charts built in HTML/JS.
---

# Python のグラフ様式

Python (matplotlib) で作るグラフの様式をそろえるためのスキル。
ユーザーは論文・レポート、スライド、手元での分析にグラフを使う。どの図も同じ見た目になるよう、規則は `assets/mpl_style.py` にまとめてある。
各規則は、ユーザーが比較用の図を見比べて選んだもの。理由が分かれば例外の判断もしやすいので、主な規則には理由を添えている。

```
依頼
 └─ 1. 用途 (プリセット) と保存形式を確認する   <- 分からなければ質問する
 └─ 2. mpl_style.py をコピーし、スクリプトを書く
 └─ 3. 実行して、画像を目で確認する             <- 4 節のチェック
 └─ 4. 渡す (スクリプトと図のパス)
```

## 1. 始める前に確認すること

- **用途 -> プリセット**: 図をどこに載せるかでサイズと文字の大きさが決まる。
  | プリセット | 大きさ | 文字 | 用途 |
  |---|---|---|---|
  | `paper` | 3.5 x 2.6 in | 8 pt (目盛り・凡例 7 pt) | 論文・レポートの片段幅 (2 段組の 1 段) |
  | `paper-wide` | 7.0 x 3.0 in | 8 pt (目盛り・凡例 7 pt) | 論文・レポートの全幅 |
  | `slide` | 12.0 x 6.75 in | 18 pt (目盛り・凡例 16 pt)、太線 | 発表スライド |

  Jupyter などで手元確認する図も、最終的に載せる先のプリセットで描く (あとで描き直さずに済むため)。載せる先が依頼から読み取れなければ質問する。
- **保存形式**: PNG か PDF かは毎回ユーザーに聞く。保存しない (ノートブックで表示するだけの) 場合は聞かなくてよい。
  - PNG: 300 dpi、白背景
  - PDF: フォントを Type 42 で埋め込む (投稿先のチェックで Type 3 フォントが不可とされることがあるため)
- 用途と保存形式は、まとめて 1 回で聞く。
- ブログ記事の図 (md-writer スキル) は、`slide` プリセット・PNG 固定・タイトルあり・番号付きのファイル名にする。詳細は md-writer の `references/figures.md` 3 節。

## 2. スクリプトの書き方

`assets/mpl_style.py` をスクリプトと同じディレクトリにコピーし、import して使う。コピーにするのは、スキルがない環境でもスクリプト単体で再実行できるようにするため。

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""
<テーマ> の図を生成する．figures/ 以下に出力する．

    uv run <script_name>.py
"""
import numpy as np
import matplotlib.pyplot as plt

from mpl_style import use_style, color_map, scatter_kw, save, C_REF

PRESET = "paper"
FMT = "pdf"
COLORS = color_map(["Proposed", "Baseline"])  # 系列名 -> 色．全図で共通


# 計算・読み込み (描画とは分ける)
def load_results():
    rng = np.random.default_rng(0)
    ...


# 1 図 1 関数．関数名は fig_<内容名>
def fig_loss_curve(res):
    fig, ax = plt.subplots()
    ...
    save(fig, "loss_curve", FMT)


if __name__ == "__main__":
    use_style(PRESET)
    res = load_results()
    fig_loss_curve(res)
```

- **PEP 723 の依存関係**を冒頭に書き、`uv run <script>.py` だけで動くようにする。pandas や scipy を使うなら `dependencies` に足す
- **1 図 1 関数**にして、`main` ですべての図を生成する。1 つの図だけ直したいときに、その関数だけ見ればよいため
- **計算と描画を分ける**。データの読み込みや重い計算は別の関数にする。計算に時間がかかるなら、結果を `.npz` や `.csv` に保存し、描画側はそれを読むだけにする。見た目の調整のたびに計算をやり直さずに済むため
- **乱数の seed を固定する** (`np.random.default_rng(0)`)。何度実行しても同じ図にするため
- **ファイル名**は `figures/<内容名>.<ext>` (例: `figures/loss_curve.pdf`)。番号は付けない。論文側で図の順番が変わっても、名前を変えずに済むため
- ノートブックでは、最初のセルで `use_style(...)` を呼び、`save` は保存を頼まれたときだけ使う
- スクリプトの冒頭の docstring には、実行方法を書く。コメントは日本語でよい

## 3. 様式の規則

規則は 2 段に分かれている。

- **必ず守る** (全体・軸): 図をまたいだ見た目の統一に直結する。ユーザーが指示したときだけ変える
- **既定値** (色・要素): まずこの通りに描き、図に合わなければ変えてよい (点が多くてエラーバーが潰れる、凡例を置く場所がない、など)。変えたときは、渡すときに何をなぜ変えたかを一言添える

### 全体

| 項目 | 規則 |
|---|---|
| 枠・グリッド | 上と右の枠なし、薄いグリッド (`use_style` で設定済み) |
| フォント | 文字・数式とも Computer Modern (`cmr10` + mathtext `cm`)。LaTeX の本文と見た目をそろえるため |
| ラベル | 英語 + 数式。変数は `$t$` のように数式にする |
| 単位 | `名前 記号 [単位]` (例: `Time $t$ [s]`、`Voltage $V$ [mV]`) |
| タイトル | `paper` / `paper-wide` では付けない (説明は論文のキャプションで行うため)。`slide` では、何のデータのグラフかを短く付ける (例: `Top-1 accuracy by model`)。結論や解釈 (`... converges faster` など) は書かない |
| パネルラベル | (a)(b) を付けるか、どこに置くかは図に応じて判断する。付けるなら、データに重ならない位置にする |

### 色 (既定値)

図に合わなければ変えてよい。変えてよい例:

- 強調したい系列が 1 つある -> 主役だけ色を付け、ほかはグレーにする
- 白黒で印刷される -> 黒とグレーの濃淡に、線種・マーカー・ハッチを組み合わせる
- 投稿先やスライドのテンプレートに配色の指定がある -> それに合わせる

変える場合も、同じ系列はどの図でも同じ色にする (その図のセットの中でそろえる)。

- **系列の色**は Okabe-Ito (色覚の多様性に配慮した配色)。`color_map` で「系列名 -> 色」の対応を冒頭で 1 回作り、どの図でも同じ系列は同じ色にする。図ごとに描いた順で色を割り当てると、図をまたいで比べるときに混乱するため
- 系列の色は 7 色。8 系列以上になると色が重複するので、重複した系列には線種 (`--`、`:`) かマーカーを足して区別できるようにする
- **連続値のパラメータごとの系列** (例: 減衰比 ζ = 0.1, 0.3, …、温度、学習率) は、Okabe-Ito ではなく `param_colors(values)` で viridis の 0〜0.85 から値に比例して色を取る。色の明るさで値の大小が読み取れるため。端の明るい黄色は白背景で線が薄くなるので使わない。6 本までは凡例で示し、7 本以上は凡例の代わりに `param_colorbar(fig, ax, values, label)` でカラーバーを付ける。手法名などのカテゴリには使わない
- 朱色 (`C_REF`) は参照線と強調用に取っておき、系列の色には使わない
- **参照線**: 極限値・理論値は `C_REF` の破線 (`linestyle="--", linewidth=1`)。凡例に入れるか、線の近くにラベルを書く。y=0 などの基準線は細い実線 (`color="0.3", linewidth=0.8`)
- **カラーマップ**: 0 以上の値 (密度、強度など) は `viridis`。正負がある値は `RdBu_r` で、`norm=TwoSlopeNorm(0)` で 0 を中央の白に固定する。カラーバーには量と単位のラベルを付ける

### 軸

- **範囲**: 折れ線 (エラーバー付きも含む) は `ax.margins(x=0)` で x をデータの端ちょうどにする。散布図と棒は既定の余白を残す (端の点や棒が軸で切れるため)。y は既定の余白のまま
- **桁の大きい値・小さい値**は、データを $10^k$ で割り、倍率を軸ラベルに入れる (例: `Samples [$\times 10^{6}$]`、`Loss [$\times 10^{-4}$]`)。軸の端に `1e6` や `×10^6` が浮かないようにするため。単位と一緒に書くときは `Power [$\times 10^{3}$ W]` とする
- **対数軸**: 主目盛りは `10^n` 表記にし、補助目盛りも出す (matplotlib の既定のままでよい)
- **2 軸 (twinx) は使わない**。単位の違う量を重ねたいときは、上下 2 段のパネルに分けて x 軸を共有する (`plt.subplots(2, 1, sharex=True)`)。どの線がどちらの軸か迷わずに済むため

### 要素 (既定値)

| 要素 | 既定 | 変えてよい例 |
|---|---|---|
| 凡例 | 図の中に枠付きで置く。線や棒、エラーバーに重なるときは `loc` を変えるか、`set_ylim` で余白を作る | 図の中に空きがない → 図の外に置く、線の端に直接ラベルを書く |
| 誤差 | エラーバー (キャップあり。`errorbar.capsize` で設定済み)。折れ線でも棒でも同じ | 点が多くてバーが潰れる (目安 20 点超) → `errorevery` で数点おきにする、`fill_between` (alpha 0.2) の帯にする |
| 散布図 | 中くらいの点、半透明、白の縁取り。`ax.scatter(x, y, **scatter_kw(PRESET))` | 点が数千以上 → 小さくして透明度を上げる。点が少ない → 不透明にする |
| 棒 | グリッドは値の方向だけにする (縦棒なら `ax.grid(axis="x", visible=False)`)。棒の上に値を書く (`ax.bar_label(bars, fmt="%.2f")`)。ラベルが長くて斜めにしないと読めないときは横棒 (`barh`) にし、上から順に並ぶよう `ax.invert_yaxis()` を使う | 棒が多くて値が詰まる → 値を省く |
| 注目点 | `C_REF` の丸で囲み (`marker="o", mfc="none", mec=C_REF`)、同じ色の文字を点の横に添える。矢印は使わない | 点から離れた位置にしか文字を置けない → 細い引き出し線を使う |

## 4. よくある問題

- **matplotlib の mathtext は LaTeX の一部しか使えない**。`\textstyle`、`\displaystyle`、`\dfrac`、`\operatorname` などはエラーになる。`\frac` を使うか、書き下す
- **Computer Modern (cmr10) には太字がない**。`fontweight="bold"` は効かず、警告が出る。強調したいときは数式の `$\mathbf{...}$` を使う
- **cmr10 にはマイナス記号がない**。`use_style` で数式描画にしてあるので、目盛りは正しく出る。ラベルの文字列に負の数を書くときは数式にする (`"$-1$"`)
- **凡例や注釈が線・点に重なる**。生成した画像で必ず確認する
- **浮動小数点の限界が図に出る**。誤差を対数軸で描くと、約 $10^{-16}$ で頭打ちになる。そこに達する手前で打ち切る
- **`bbox_inches="tight"` を使わない**。図の大きさがプリセットからずれ、論文に貼ったときに文字の大きさがそろわなくなる。はみ出しは constrained layout (`use_style` で有効) で防ぐ

## 5. 出力前のチェック

- スクリプトを `uv run` で最初から最後まで実行できたか (途中で直したら、最初から再実行する)
- 生成した図をすべて開いて確認したか。PDF は Read で開ける
  - 文字・凡例・注釈がはみ出したり、重なったりしていないか
  - 端の点や棒が軸で切れていないか
  - 色の対応が、ほかの図と同じか
- 単位の書き方 (`[単位]`)、倍率の書き方、タイトルの有無がプリセットと合っているか
- 渡すときは、スクリプトと図のパスを伝える。既定値から変えた要素があれば、何をなぜ変えたかも書く
