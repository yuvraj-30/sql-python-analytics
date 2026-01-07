from __future__ import annotations

import numpy as np
import pandas as pd


def pareto_curve(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    s = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    t = s.reset_index()
    t["rank"] = range(1, len(t) + 1)
    t["cum_value"] = t[value_col].cumsum()
    t["cum_share"] = t["cum_value"] / t[value_col].sum()
    return t


def compute_monthly(df: pd.DataFrame) -> pd.DataFrame:
    m = (
        df.groupby("year_month", as_index=False)
        .agg(
            revenue=("sales_amount", "sum"),
            orders=("order_number", "nunique"),
            units=("quantity", "sum"),
        )
        .sort_values("year_month")
    )
    m["aov"] = m["revenue"] / m["orders"].replace(0, np.nan)
    m["asp"] = m["revenue"] / m["units"].replace(0, np.nan)
    m["upo"] = m["units"] / m["orders"].replace(0, np.nan)
    m["mom_revenue_pct"] = m["revenue"].pct_change() * 100
    m["mom_orders_pct"] = m["orders"].pct_change() * 100
    m["rolling_3m_revenue"] = m["revenue"].rolling(3).mean()
    return m


def kpis(df: pd.DataFrame) -> dict:
    revenue = float(df["sales_amount"].sum())
    orders = int(df["order_number"].nunique())
    units = float(df["quantity"].sum())
    customers = int(df["customer_key"].nunique()) if "customer_key" in df.columns else int(df["customer_name"].nunique())

    aov = revenue / orders if orders else np.nan
    asp = revenue / units if units else np.nan
    upo = units / orders if orders else np.nan

    top10_cust_share = np.nan
    if "customer_name" in df.columns and len(df):
        s = df.groupby("customer_name")["sales_amount"].sum().sort_values(ascending=False)
        top10_cust_share = float(s.head(10).sum() / s.sum() * 100) if len(s) else np.nan

    top10_prod_share = np.nan
    if "product_name" in df.columns and len(df):
        s = df.groupby("product_name")["sales_amount"].sum().sort_values(ascending=False)
        top10_prod_share = float(s.head(10).sum() / s.sum() * 100) if len(s) else np.nan

    latest_mom_rev = np.nan
    latest_mom_ord = np.nan
    if "year_month" in df.columns:
        m = df.groupby("year_month").agg(revenue=("sales_amount","sum"), orders=("order_number","nunique")).sort_index()
        if len(m) >= 2:
            prev = m.iloc[-2]
            last = m.iloc[-1]
            if prev["revenue"] != 0:
                latest_mom_rev = (last["revenue"] / prev["revenue"] - 1) * 100
            if prev["orders"] != 0:
                latest_mom_ord = (last["orders"] / prev["orders"] - 1) * 100

    return {
        "revenue": revenue,
        "orders": orders,
        "units": units,
        "customers": customers,
        "aov": aov,
        "asp": asp,
        "upo": upo,
        "top10_customer_share_pct": top10_cust_share,
        "top10_product_share_pct": top10_prod_share,
        "latest_mom_revenue_pct": latest_mom_rev,
        "latest_mom_orders_pct": latest_mom_ord,
    }
