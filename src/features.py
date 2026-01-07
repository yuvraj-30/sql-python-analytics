from __future__ import annotations

import numpy as np
import pandas as pd


def ensure_display_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create stable display columns used across dashboards and notebooks.

    - customer_display: prefer customer_number; fallback customer_key, plus optional first/last name for readability.
    - product_name: fallback to product_key if missing.

    Adds:
      - customer_display
      - customer_name (compatibility alias)
      - product_name (if missing)
    """
    out = df.copy()

    # Product display
    if "product_name" not in out.columns:
        for c in ["prd_name", "product", "name"]:
            if c in out.columns:
                out["product_name"] = out[c].astype(str)
                break
        if "product_name" not in out.columns and "product_key" in out.columns:
            out["product_name"] = out["product_key"].astype(str)

    # Customer display
    if "customer_number" in out.columns:
        cust_id = out["customer_number"].astype(str)
    elif "customer_key" in out.columns:
        cust_id = out["customer_key"].astype(str)
    else:
        cust_id = pd.Series(["unknown"] * len(out))

    first = out["first_name"].astype(str).fillna("") if "first_name" in out.columns else pd.Series([""] * len(out))
    last = out["last_name"].astype(str).fillna("") if "last_name" in out.columns else pd.Series([""] * len(out))
    name = (first + " " + last).str.strip()

    out["customer_display"] = np.where(name != "", cust_id + " — " + name, cust_id)
    out["customer_name"] = out["customer_display"]  # legacy compatibility

    return out
