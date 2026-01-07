from __future__ import annotations

import pandas as pd

from src import quality


def dq_indicators(fact: pd.DataFrame, dim_customers: pd.DataFrame, dim_products: pd.DataFrame) -> dict:
    missing_customer_key = int(fact["customer_key"].isna().sum()) if "customer_key" in fact.columns else 0
    missing_product_key = int(fact["product_key"].isna().sum()) if "product_key" in fact.columns else 0
    neg_qty = int((fact["quantity"] < 0).sum()) if "quantity" in fact.columns else 0
    neg_sales = int((fact["sales_amount"] < 0).sum()) if "sales_amount" in fact.columns else 0
    zero_price = int((fact["price"] <= 0).sum()) if "price" in fact.columns else 0

    cust_viol = quality.referential_integrity_violations(fact, dim_customers, "customer_key", "customer_key")
    prod_viol = quality.referential_integrity_violations(fact, dim_products, "product_key", "product_key")

    return {
        "missing_customer_key_rows": missing_customer_key,
        "missing_product_key_rows": missing_product_key,
        "negative_quantity_rows": neg_qty,
        "negative_sales_rows": neg_sales,
        "zero_or_negative_price_rows": zero_price,
        "missing_customer_keys_in_dim": cust_viol,
        "missing_product_keys_in_dim": prod_viol,
    }
