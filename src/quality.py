from __future__ import annotations

import pandas as pd


def null_rate(df: pd.DataFrame) -> pd.Series:
    return df.isna().mean().sort_values(ascending=False)


def duplicate_key_count(df: pd.DataFrame, key_cols: list[str]) -> int:
    return int(df.duplicated(subset=key_cols).sum())


def referential_integrity_violations(fact: pd.DataFrame, dim: pd.DataFrame, fact_key: str, dim_key: str) -> int:
    fact_keys = set(fact[fact_key].dropna().unique())
    dim_keys = set(dim[dim_key].dropna().unique())
    return int(len(fact_keys - dim_keys))
