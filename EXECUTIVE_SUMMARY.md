# Executive Summary — Commercial Sales Analytics (Python)

## What this project is
This repository demonstrates how Python can be used to analyse the same **Gold-layer warehouse outputs** produced by a SQL Server data warehouse
(CRM + ERP → Bronze/Silver/Gold). It is intentionally scoped to commercial analytics tasks commonly found in wholesale/distribution environments.

## Business problem
Even with strong SQL reporting, stakeholders often lack visibility into:
- revenue concentration across customers/products (dependency risk),
- early performance changes over time (growth or decline),
- data integrity issues that reduce trust in analytics outputs.

## Goals
- Validate Gold-layer extracts through lightweight data quality checks  
- Produce monthly KPIs and trend signals (MoM movement)  
- Identify customer and product contribution and concentration  
- Create A/B/C contribution tiers to support commercial prioritisation

## Snapshot (from the included sample extract)
- Total revenue: **$15,631,069**
- Total orders: **21,715**
- Active customers: **17,612**
- Products sold: **102**
- Top 10 customers revenue share: **0.5%**
- Top 10 products revenue share: **51.5%**
- Best month: **2013-12** ($1,874,128)


## How to read the repo
- Start with `notebooks/01_data_quality_profile.ipynb` to validate data readiness.
- Use `notebooks/02_sales_kpis_trends.ipynb` for KPI trends and MoM movement.
- Use `notebooks/03_customer_analysis.ipynb` and `notebooks/04_product_analysis.ipynb` for contribution analysis.
- Use `notebooks/05_pareto_segmentation.ipynb` for Pareto curves and A/B/C tiers.

## Business value
This workflow complements dashboards by enabling deeper, repeatable analysis on top of trusted warehouse data, supporting:
- account management and customer prioritisation,
- product portfolio performance reviews,
- early detection of performance changes,
- stronger data trust through validation.
