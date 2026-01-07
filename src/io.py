from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


REQUIRED_FILES = {
    "fact_sales": "fact_sales_sample.csv",
    "dim_customers": "dim_customers_sample.csv",
    "dim_products": "dim_products_sample.csv",
    "report_customers": "report_customers_sample.csv",
    "report_products": "report_products_sample.csv",
}


def project_root() -> Path:
    """Return the repository root (works regardless of current working directory).

    Assumes this file lives in: <repo>/src/io.py
    """
    return Path(__file__).resolve().parents[1]


def load_sample(data_dir: str | Path | None = None) -> Dict[str, pd.DataFrame]:
    """Load the local sample extracts used by this repository.

    By default, resolves `data/sample` relative to the repository root, not the notebook working directory.
    """
    root = project_root()
    data_dir = Path(data_dir) if data_dir is not None else (root / "data" / "sample")

    missing = [f for f in REQUIRED_FILES.values() if not (data_dir / f).exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing sample files in {data_dir}: {missing}. "
            "Ensure `data/sample/` exists, or regenerate using `sql/export_sample_sqlserver.sql`."
        )

    dfs = {k: pd.read_csv(data_dir / v) for k, v in REQUIRED_FILES.items()}

    # Type fixes
    if "order_date" in dfs["fact_sales"].columns:
        dfs["fact_sales"]["order_date"] = pd.to_datetime(dfs["fact_sales"]["order_date"], errors="coerce")
    for c in ["shipping_date", "due_date"]:
        if c in dfs["fact_sales"].columns:
            dfs["fact_sales"][c] = pd.to_datetime(dfs["fact_sales"][c], errors="coerce")

    return dfs
