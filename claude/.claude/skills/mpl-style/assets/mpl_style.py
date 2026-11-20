# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""
matplotlib の様式をそろえるためのモジュール．
図を作るスクリプトと同じディレクトリにコピーして import する．

    from mpl_style import use_style, color_map, save, C_REF

直接実行すると，各プリセットの見本を figures/ に出力する．

    uv run mpl_style.py
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap, Normalize

# Okabe-Ito．朱色は参照線用に取っておき，系列の色には使わない
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#000000", "#F0E442"]
C_REF = "#D55E00"  # 極限値・理論値の破線，注目点の丸

# 連続値のパラメータの系列は viridis の 0〜0.85 から取る (端の黄色は白背景で薄いため)
PARAM_RANGE = (0.0, 0.85)

OUT = Path("figures")

COMMON = {
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.alpha": 0.3,
    "axes.prop_cycle": cycler(color=OKABE_ITO),
    "image.cmap": "viridis",
    # Computer Modern．cmr10 は太字を持たない
    "font.family": "serif",
    "font.serif": ["cmr10"],
    "mathtext.fontset": "cm",
    "axes.formatter.use_mathtext": True,  # cmr10 はマイナス記号を持たないため数式で描く
    "axes.unicode_minus": False,
    "errorbar.capsize": 3,
    "legend.frameon": True,
    "figure.constrained_layout.use": True,
    "savefig.dpi": 300,
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
}

PRESETS = {
    # 論文の片段幅
    "paper": {
        "figure.figsize": (3.5, 2.6),
        "font.size": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
    },
    # 論文の全幅
    "paper-wide": {
        "figure.figsize": (7.0, 3.0),
        "font.size": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
    },
    # スライド (16:9)
    "slide": {
        "figure.figsize": (12.0, 6.75),
        "font.size": 18,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "legend.fontsize": 16,
        "lines.linewidth": 2.5,
        "lines.markersize": 7,
        "errorbar.capsize": 5,
    },
}

# 散布図の点 (中くらい，半透明，白の縁取り)．preset ごとに大きさを変える
SCATTER = {"alpha": 0.7, "edgecolors": "white", "linewidths": 0.5}
SCATTER_SIZE = {"paper": 12, "paper-wide": 16, "slide": 40}


def use_style(preset):
    """preset ("paper" / "paper-wide" / "slide") の様式を有効にする．"""
    plt.rcdefaults()
    plt.rcParams.update({**COMMON, **PRESETS[preset]})


def color_map(names):
    """系列名 -> 色 の対応を作る．同じ系列はどの図でも同じ色にするため，冒頭で 1 回だけ作る．"""
    return {n: OKABE_ITO[i % len(OKABE_ITO)] for i, n in enumerate(names)}


def _param_cmap(cmap):
    return ListedColormap(plt.get_cmap(cmap)(np.linspace(*PARAM_RANGE, 256)))


def param_colors(values, cmap="viridis"):
    """連続値のパラメータ -> 色．値の大きさに比例して色を取る．"""
    lo, hi = min(values), max(values)
    cm = _param_cmap(cmap)
    return {v: cm((v - lo) / (hi - lo) if hi > lo else 0.0) for v in values}


def param_colorbar(fig, ax, values, label, cmap="viridis"):
    """param_colors と対応するカラーバーを付ける．7 系列以上で凡例の代わりに使う．"""
    sm = ScalarMappable(norm=Normalize(min(values), max(values)), cmap=_param_cmap(cmap))
    return fig.colorbar(sm, ax=ax, label=label)


def scatter_kw(preset):
    """ax.scatter に渡す共通の引数．"""
    return {**SCATTER, "s": SCATTER_SIZE[preset]}


def save(fig, name, fmt):
    """figures/<name>.<fmt> に保存する．fmt は "png" か "pdf"．"""
    OUT.mkdir(exist_ok=True)
    path = OUT / f"{name}.{fmt}"
    fig.savefig(path)
    plt.close(fig)
    print(f"saved: {path}")


# ---- 見本 (直接実行したときだけ) ----

def _demo(preset):
    import numpy as np

    use_style(preset)
    rng = np.random.default_rng(0)
    colors = color_map(["Proposed", "Baseline"])

    fig, (a, b, c) = plt.subplots(1, 3, figsize=(plt.rcParams["figure.figsize"][0] * 2,
                                                  plt.rcParams["figure.figsize"][1]))
    n = np.arange(1, 11)
    for name, k in (("Proposed", 0.35), ("Baseline", 0.25)):
        a.errorbar(n, 1 - np.exp(-k * n), yerr=0.03 + 0.03 * rng.random(n.size),
                   marker="o", color=colors[name], label=name)
    a.axhline(1, color=C_REF, linestyle="--", linewidth=1)
    a.margins(x=0)  # 折れ線は x をデータの端ちょうどにする
    a.set_xlabel("Epoch $n$")
    a.set_ylabel("Score")
    a.legend(loc="lower right")

    p = rng.normal(0, 1, (100, 2))
    b.scatter(p[:, 0], p[:, 1], color=colors["Proposed"], **scatter_kw(preset))
    b.axhline(0, color="0.3", linewidth=0.8)
    b.set_xlabel("$x_1$")
    b.set_ylabel("$x_2$")

    bars = c.bar(["SGD", "Adam"], [0.82, 0.91], yerr=[0.03, 0.02])
    c.bar_label(bars, fmt="%.2f", padding=4)
    c.set_ylim(0, 1.1)
    c.grid(axis="x", visible=False)
    c.set_ylabel("Accuracy")
    if preset == "slide":
        fig.suptitle("Training score, samples, and accuracy")
    save(fig, f"demo_{preset}", "png")


if __name__ == "__main__":
    for p in PRESETS:
        _demo(p)
