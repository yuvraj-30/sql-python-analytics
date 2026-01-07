from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


class SchemaError(ValueError):
    """Raised when an input dataset does not match expected schema."""


def assert_required_columns(df: pd.DataFrame, required: Iterable[str], df_name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SchemaError(
            f"{df_name} is missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}"
        )


# Minimal, recruiter-friendly expectations for this project.
REQUIRED = {
    "fact_sales": ["order_number", "order_date", "customer_key", "product_key", "sales_amount"],
    "dim_customers": ["customer_key"],
    "dim_products": ["product_key"],
}
