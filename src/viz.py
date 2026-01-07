from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def line_chart(df: pd.DataFrame, x: str, y: str, title: str, xlabel: str = "", ylabel: str = "", path: str | None = None):
    plt.figure(figsize=(10, 5))
    plt.plot(df[x], df[y])
    plt.title(title)
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=200)
    plt.show()


def barh_top(df: pd.DataFrame, label: str, value: str, title: str, top_n: int = 10, path: str | None = None):
    top = df.sort_values(value, ascending=False).head(top_n).copy()
    plt.figure(figsize=(10, 6))
    plt.barh(top[label][::-1].astype(str), top[value][::-1])
    plt.title(title)
    plt.xlabel(value)
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=200)
    plt.show()
