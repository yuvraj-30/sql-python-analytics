from __future__ import annotations

import pandas as pd


def monthly_kpis(fact: pd.DataFrame) -> pd.DataFrame:
    f = fact.copy()
    f["year_month"] = f["order_date"].dt.to_period("M").astype(str)

    out = (
        f.groupby("year_month", as_index=False)
        .agg(
            revenue=("sales_amount", "sum"),
            orders=("order_number", "nunique"),
            units=("quantity", "sum"),
            avg_price=("price", "mean"),
        )
        .sort_values("year_month")
    )
    out["aov"] = out["revenue"] / out["orders"]
    out["mom_revenue_pct"] = out["revenue"].pct_change() * 100
    out["mom_orders_pct"] = out["orders"].pct_change() * 100
    return out
