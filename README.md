# CRM & ERP Analytics Project  
**Customer, Product, and Sales Performance Analysis**

---

## Executive Summary

This project demonstrates end-to-end analytics using **CRM and ERP data** to support customer, product, and sales decision-making.  
It focuses on validating data quality, analysing performance, and producing trusted tables and visual outputs suitable for operational and commercial reporting.

The project is designed to reflect how data analysts work with enterprise systems rather than isolated datasets.

---

## Business Questions Addressed

This project answers practical business questions such as:

- What is the **data quality** of CRM and ERP datasets used for reporting?
- Which **customers** contribute most to revenue and sales volume?
- Which **products** are high-performing versus underperforming?
- How does **sales performance change over time**?
- Are there **missing or inconsistent keys** between CRM and ERP systems that could affect reporting accuracy?

---

## Data Sources

The analysis uses structured CRM and ERP-style datasets located in the `data/` folder:

- `dim_customers_sample.csv` – customer master data  
- `dim_products_sample.csv` – product master data  
- `fact_sales_sample.csv` – transactional sales data  
- `report_customers_sample.csv` – customer-level reporting output  
- `report_products_sample.csv` – product-level reporting output  

Detailed schema definitions are documented in  
[`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## Analytical Approach

The project follows a structured analytics workflow:

1. **Data exploration**
   - Row counts, date ranges, key dimensions, and measures
2. **Data quality validation**
   - Null-rate analysis
   - Schema checks
   - Detection of missing customer and product keys
3. **Performance analysis**
   - Customer and product ranking
   - Revenue and quantity trends
4. **Segmentation and contribution analysis**
   - Part-to-whole analysis by customer, product, and region
5. **Visualisation and reporting**
   - Reproducible tables and figures generated from notebooks

Reusable logic is implemented in the `src/` directory.

---

## Key Outputs

### Tables

Generated tables are stored in `outputs/tables/`, including:

- `dq_summary.csv`
- `customer_performance.csv`
- `product_performance.csv`
- `sales_trends_over_time.csv`

These tables are produced directly from notebooks and SQL-style transformations.

### Figures

Visual outputs are stored in `outputs/figures/`, including:

- Customer revenue contribution
- Product sales distribution
- Sales trends over time
- Data quality summaries

All figures are reproducible and traceable to source notebooks.

---

## Business Impact & Decision Support

This project demonstrates how CRM and ERP data can be transformed into **decision-ready insights**:

- **Improved data reliability** through explicit data quality checks  
- **Customer-focused insights** to support prioritisation of high-value accounts  
- **Product performance visibility** to inform pricing, promotion, and inventory decisions  
- **Trend awareness** to identify growth patterns and seasonality  

Although the datasets are anonymised and sample-based, the workflow mirrors how real organisations use CRM and ERP data to support operational and commercial decisions.

---

## Project Structure

```text
├── data/           # CRM and ERP source datasets
├── notebooks/      # Exploration, quality, and performance analysis
├── src/            # Reusable validation, metrics, and visualisation logic
├── outputs/
│   ├── tables/     # Generated analytical tables
│   └── figures/    # Generated figures used in reporting
├── app/            # Dash application
├── docs/           # Data dictionary and documentation
└── README.md
```

---

## Dashboard (Optional)

An interactive Dash dashboard is available in the `app/` directory and consumes the curated outputs to present key metrics and insights.

---

## Relationship to the Data Warehouse Project

This project complements the **Data Warehouse project** in the portfolio:

- The warehouse project focuses on **data modelling and quality at the platform level**
- This project focuses on **consuming curated data for analysis and insight generation**

Together, they demonstrate the full lifecycle from **data foundations to business insights**.

---

## How to Run

1. Open notebooks from the `notebooks/` directory.
2. Run notebooks top-to-bottom to reproduce tables and figures.
3. Launch the dashboard using `python app/app.py` if required.

---

## Notes

This README is the single source of truth for the project and is intentionally aligned with the actual data, folders, and outputs in the repository.