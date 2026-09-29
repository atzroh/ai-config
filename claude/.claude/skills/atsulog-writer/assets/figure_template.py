"""
<記事のテーマ> の記事用の図を生成するスクリプト．
実行すると figures/ 以下に PNG と SVG を出力する．

    python <script_name>.py

必要なライブラリ: numpy, matplotlib
ラベルは環境依存のフォント問題を避けるため英語 + 数式にしている．
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

OUT = Path("figures")
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "mathtext.fontset": "cm",
})

C_MAIN = "#1f77b4"   # 主役
C_SUB = "#ff7f0e"    # 比較対象
C_ALT = "green"      # 2 つ目の比較対象
C_ACCENT = "#d62728" # 極限値・強調（破線で使う）


def save(fig, name):
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {name}")


# 01. <節名>: <この図で分かること>
def fig_01_example():
    x = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, x ** 2, color=C_MAIN, label="$y=x^2$")
    ax.set_xlabel("$x$")
    ax.set_title("Short message of this figure")
    ax.legend()
    save(fig, "01_example")


if __name__ == "__main__":
    fig_01_example()
