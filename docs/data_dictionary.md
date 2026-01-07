# Data Dictionary (Sample Extracts)

This repo uses Gold-layer extracts from a SQL Server warehouse project.

## fact_sales_sample.csv
- order_number: order identifier
- product_key: product surrogate key
- customer_key: customer surrogate key
- order_date / shipping_date / due_date: dates
- sales_amount: revenue amount
- quantity: units
- price: unit price (as provided)

## dim_customers_sample.csv
Contains customer attributes used for slicing and segmentation (e.g., segment, demographics, geography).

## dim_products_sample.csv
Contains product attributes such as category, subcategory, and product-level descriptors.

## report_customers_sample.csv / report_products_sample.csv
Pre-aggregated reporting marts with customer and product KPIs.
