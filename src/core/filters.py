from __future__ import annotations

import pandas as pd


def filter_df(df: pd.DataFrame, start_month: str, end_month: str, segment: str, category: str, subcategory: str) -> pd.DataFrame:
    """Filter an enriched fact table by common dashboard slicers."""
    out = df[(df["year_month"] >= start_month) & (df["year_month"] <= end_month)].copy()

    if segment != "All" and "customer_segment" in out.columns:
        out = out[out["customer_segment"].astype(str) == str(segment)]

    if category != "All" and "category" in out.columns:
        out = out[out["category"].astype(str) == str(category)]

    if subcategory != "All" and "subcategory" in out.columns:
        out = out[out["subcategory"].astype(str) == str(subcategory)]

    return out
    
def money0(x):
    return f"${x:,.0f}" if pd.notna(x) else "—"