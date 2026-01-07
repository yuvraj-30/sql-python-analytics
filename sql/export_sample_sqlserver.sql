/*
SQL Server sample export script (optional)

Purpose:
- Regenerate the sample CSVs used in this Python repo from your SQL Server Gold layer.

How to use:
1) Update database name/schema if needed
2) Run in SSMS
3) Export results to CSV (SSMS grid export) OR use sqlcmd/bcp for automated export

Default sample window: last 12 months based on max(order_date) in gold.fact_sales.
*/

DECLARE @max_date DATE = (SELECT MAX(order_date) FROM gold.fact_sales);
DECLARE @cutoff  DATE = DATEADD(MONTH, -12, @max_date);

-- fact_sales sample
SELECT *
FROM gold.fact_sales
WHERE order_date >= @cutoff;

-- dim_customers sample (only customers in window)
SELECT c.*
FROM gold.dim_customers c
WHERE EXISTS (
    SELECT 1 FROM gold.fact_sales f
    WHERE f.customer_key = c.customer_key
      AND f.order_date >= @cutoff
);

-- dim_products sample (only products in window)
SELECT p.*
FROM gold.dim_products p
WHERE EXISTS (
    SELECT 1 FROM gold.fact_sales f
    WHERE f.product_key = p.product_key
      AND f.order_date >= @cutoff
);

-- report marts (optional)
SELECT rc.*
FROM gold.report_customers rc
WHERE EXISTS (SELECT 1 FROM gold.fact_sales f WHERE f.customer_key = rc.customer_key AND f.order_date >= @cutoff);

SELECT rp.*
FROM gold.report_products rp
WHERE EXISTS (SELECT 1 FROM gold.fact_sales f WHERE f.product_key = rp.product_key AND f.order_date >= @cutoff);
