# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""
<記事のテーマ> の記事用の図を生成するスクリプト．
実行すると figures/ 以下に PNG を出力する．

    uv run <script_name>.py

様式は mpl-style スキルに従う．同じディレクトリに mpl_style.py を置く．
"""
import numpy as np
import matplotlib.pyplot as plt

from mpl_style import use_style, color_map, save, C_REF

PRESET = "slide"  # ブログ用
FMT = "png"
COLORS = color_map(["main", "sub"])  # 系列名 -> 色．全図で共通


# 01. <節名>: <この図で分かること>
def fig_01_example():
    x = np.linspace(0, 1, 200)
    fig, ax = plt.subplots()
    ax.plot(x, x ** 2, color=COLORS["main"], label="$y=x^2$")
    ax.axhline(1, color=C_REF, linestyle="--", linewidth=1, label="$y=1$")
    ax.margins(x=0)
    ax.set_xlabel("$x$")
    ax.set_title("What this figure plots")
    ax.legend()
    save(fig, "01_example", FMT)


if __name__ == "__main__":
    use_style(PRESET)
    fig_01_example()
