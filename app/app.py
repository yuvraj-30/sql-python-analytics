from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dash_table, dcc, html

# Ensure repo root is on sys.path so `from src...` imports work when running `python app/app.py`
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from src.io import load_sample
from src.core import compute_monthly, dq_indicators, filter_df, kpis, pareto_curve, ensure_display_columns


# -----------------------------
# Load data (sample extract)
# -----------------------------
dfs = load_sample()
fact = dfs["fact_sales"]
dim_customers = dfs["report_customers"]
dim_products = dfs["report_products"]

# Ensure expected time grain exists for filtering
#fact = fact.copy()
if "year_month" not in fact.columns:
    # load_sample should already set order_date as datetime
    fact["year_month"] = pd.to_datetime(fact["order_date"]).dt.to_period("M").astype(str)

# Enrich with display columns (customer_display, product_name, etc.)
#fact_enriched = ensure_display_columns(fact)

fact_enriched = fact.merge(dim_customers, on="customer_key", how="left", suffixes=("", "_cust"))
fact_enriched = fact_enriched.merge(dim_products, on="product_key", how="left", suffixes=("", "_prd"))


# Precompute global DQ indicators for the sample (shown on DQ tab)
dq = dq_indicators(fact_enriched, dim_customers, dim_products)


# -----------------------------
# UI helpers
# -----------------------------
def money0(x):
    return f"${x:,.0f}" if pd.notna(x) else "—"


def card(title: str, value: str, subtitle: str | None = None):
    return html.Div(
        [
            html.Div(title, style={"fontSize": "12px", "color": "#555"}),
            html.Div(value, style={"fontSize": "22px", "fontWeight": 600}),
            html.Div(subtitle or "", style={"fontSize": "12px", "color": "#777"}) if subtitle else html.Div(),
        ],
        style={
            "border": "1px solid #e5e5e5",
            "borderRadius": "12px",
            "padding": "10px 14px",
            "minWidth": "210px",
        },
    )


# -----------------------------
# Controls
# -----------------------------
months = sorted(fact_enriched["year_month"].dropna().unique().tolist())
min_month = months[0] if months else "—"
max_month = months[-2] if months else "—"

segments = ["All"]
if "customer_segment" in fact_enriched.columns:
    segments += sorted([str(x) for x in fact_enriched["customer_segment"].dropna().unique().tolist()])

categories = ["All"]
if "category" in fact_enriched.columns:
    categories += sorted([str(x) for x in fact_enriched["category"].dropna().unique().tolist()])

subcategories = ["All"]
if "subcategory" in fact_enriched.columns:
    subcategories += sorted([str(x) for x in fact_enriched["subcategory"].dropna().unique().tolist()])

controls = html.Div(
    [
        html.Div(
            [
                html.Label("Start month"),
                dcc.Dropdown(id="start_month", options=months, value=min_month, clearable=False, persistence=False),
            ],
            style={"flex": 1},
        ),
        html.Div(
            [
                html.Label("End month"),
                dcc.Dropdown(id="end_month", options=months, value=max_month, clearable=False, persistence=False),
            ],
            style={"flex": 1},
        ),
        html.Div(
            [
                html.Label("Segment"),
                dcc.Dropdown(id="segment", options=segments, value="All", clearable=False, persistence=False),
            ],
            style={"flex": 1},
        ),
        html.Div(
            [
                html.Label("Category"),
                dcc.Dropdown(id="category", options=categories, value="All", clearable=False, persistence=False),
            ],
            style={"flex": 1},
        ),
        html.Div(
            [
                html.Label("Subcategory"),
                dcc.Dropdown(id="subcategory", options=subcategories, value="All", clearable=False, persistence=False),
            ],
            style={"flex": 1},
        ),
        html.Div(
            [
                html.Label("Top N"),
                dcc.Slider(id="topn", min=5, max=25, step=5, value=10, marks={5:"5",10:"10",15:"15",20:"20",25:"25"}, persistence=False),
            ],
            style={"flex": 2, "paddingTop": "24px"},
        ),
    ],
    style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
)


# -----------------------------
# Dash app
# -----------------------------
app = Dash(__name__)
app.title = "Commercial Analytics Dashboard"

app.layout = html.Div(
    [
        html.H1("Commercial Analytics Dashboard"),
        html.Div("Dash and the notebook dashboard are designed to show the same KPIs and views."),
        html.Hr(),
        controls,
        html.Br(),
        dcc.Tabs(
            id="tabs",
            value="exec",
            children=[
                dcc.Tab(label="Executive", value="exec"),
                dcc.Tab(label="Trends", value="trends"),
                dcc.Tab(label="Customers", value="customers"),
                dcc.Tab(label="Products", value="products"),
                dcc.Tab(label="Data Quality", value="dq"),
            ],
            persistence=False,
        ),
        html.Div(id="tab_content"),
        html.Br(),
        html.Hr(),
        html.Div(
            [
                html.H3("Data quality indicators (sample extract)"),
                html.Ul([html.Li(f"{k}: {v}") for k, v in dq.items()]),
            ]
        ),
    ],
    style={"maxWidth": "1200px", "margin": "0 auto", "padding": "18px"},
)


@app.callback(
    Output("tab_content", "children"),
    Input("tabs", "value"),
    Input("start_month", "value"),
    Input("end_month", "value"),
    Input("segment", "value"),
    Input("category", "value"),
    Input("subcategory", "value"),
    Input("topn", "value"),
)
def render_tab(tab, s, e, seg, cat, subcat, topn):
    if s > e:
        return html.Div("Start month must be <= End month.", style={"color": "crimson"})

    df = filter_df(fact_enriched, s, e, seg, cat, subcat)
    k = kpis(df)
    monthly = compute_monthly(df)

    if tab == "exec":
        cards = html.Div(
            [
                card("Revenue", money0(k["revenue"])),
                card("Orders", f"{k['orders']:,}"),
                card("Units", f"{k['units']:,.0f}"),
                card("Active Customers", f"{k['customers']:,}"),
                card("AOV", money0(k["aov"]), "Revenue / Orders"),
                card("ASP", f"${k['asp']:,.2f}" if pd.notna(k["asp"]) else "—", "Revenue / Units"),
                card("Units per Order", f"{k['upo']:,.2f}" if pd.notna(k["upo"]) else "—"),
                card("MoM Revenue", f"{k['latest_mom_revenue_pct']:+.1f}%" if pd.notna(k["latest_mom_revenue_pct"]) else "—"),
                card("MoM Orders", f"{k['latest_mom_orders_pct']:+.1f}%" if pd.notna(k["latest_mom_orders_pct"]) else "—"),
                card("Top 10 Customer Share", f"{k['top10_customer_share_pct']:.1f}%" if pd.notna(k["top10_customer_share_pct"]) else "—"),
                card("Top 10 Product Share", f"{k['top10_product_share_pct']:.1f}%" if pd.notna(k["top10_product_share_pct"]) else "—"),
            ],
            style={"display": "flex", "gap": "12px", "flexWrap": "wrap"},
        )

        fig = px.line(monthly, x="year_month", y="revenue", title="Monthly Revenue")
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))

        return html.Div([cards, html.Br(), dcc.Graph(figure=fig)])

    if tab == "trends":
        fig1 = px.line(monthly, x="year_month", y="revenue", title="Monthly Revenue")
        fig2 = px.line(monthly, x="year_month", y="orders", title="Monthly Orders")
        fig3 = px.line(monthly, x="year_month", y="rolling_3m_revenue", title="Rolling 3M Revenue (Avg)")
        return html.Div([dcc.Graph(figure=fig1), dcc.Graph(figure=fig2), dcc.Graph(figure=fig3)])

    if tab == "customers":
        top = (
            df.groupby("customer_name")["sales_amount"]
            .sum()
            .sort_values(ascending=False)
            .head(int(topn))
            .reset_index()
        )
        fig = px.bar(top, x="sales_amount", y="customer_name", orientation="h", title=f"Top {int(topn)} Customers by Revenue")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=20, r=20, t=50, b=20))

        pareto = pareto_curve(df, "customer_name", "sales_amount")
        pareto_fig = px.line(pareto, x="rank", y="cum_share", title="Customer Pareto Curve (Cumulative Revenue Share)")
        pareto_fig.update_yaxes(tickformat=".0%")

        #seg_table = None
        if "customer_segment" in df.columns:
            seg_df = df.groupby("customer_segment")["sales_amount"].sum().sort_values(ascending=False).reset_index()
            seg_df["share_pct"] = (seg_df["sales_amount"] / seg_df["sales_amount"].sum() * 100).round(1)
            seg_table = dash_table.DataTable(
                data=seg_df.to_dict("records"),
                columns=[
                    {"name": "customer_segment", "id": "customer_segment"},
                    {"name": "revenue", "id": "sales_amount", "type": "numeric", "format": {"specifier": ",.0f"}},
                    {"name": "share_pct", "id": "share_pct"},
                ],
                page_size=10,
                style_table={"overflowX": "auto"},
            )
            
       # print(seg_table)
            return html.Div([dcc.Graph(figure=fig), dcc.Graph(figure=pareto_fig),html.H4("Segment contribution"), seg_table])
       # parts = html.Div.([dcc.Graph(figure=fig), dcc.Graph(figure=pareto_fig),html.H4("Segment contribution"), seg_table])
        #if seg_table:
         #   parts += [html.H4("Segment contribution"), seg_table]
        #print(parts)
        #return html.Div(parts)
        return html.Div([dcc.Graph(figure=fig), dcc.Graph(figure=pareto_fig)])

    if tab == "products":
        top = df.groupby("product_name")["sales_amount"].sum().sort_values(ascending=False).head(int(topn)).reset_index()
        fig = px.bar(top, x="sales_amount", y="product_name", orientation="h", title=f"Top {int(topn)} Products by Revenue")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, margin=dict(l=20, r=20, t=50, b=20))

        pareto = pareto_curve(df, "product_name", "sales_amount")
        pareto_fig = px.line(pareto, x="rank", y="cum_share", title="Product Pareto Curve (Cumulative Revenue Share)")
        pareto_fig.update_yaxes(tickformat=".0%")

        if "category" in df.columns:
            cols = ["category"] + (["subcategory"] if "subcategory" in df.columns else [])
            cat_df = df.groupby(cols)["sales_amount"].sum().sort_values(ascending=False).reset_index().rename(columns={"sales_amount":"revenue"})
            table = dash_table.DataTable(
                data=cat_df.head(20).to_dict("records"),
                columns=[{"name": c, "id": c} for c in cat_df.columns],
                page_size=20,
                style_table={"overflowX": "auto"},
            )
            return html.Div([dcc.Graph(figure=fig), dcc.Graph(figure=pareto_fig), html.H4("Top categories/subcategories"), table])

        return html.Div([dcc.Graph(figure=fig), dcc.Graph(figure=pareto_fig)])

    if tab == "dq":
        nulls = df.isna().mean().sort_values(ascending=False).head(12).reset_index()
        nulls.columns = ["field", "null_rate"]
        table = dash_table.DataTable(
            data=nulls.to_dict("records"),
            columns=[{"name":"field","id":"field"},{"name":"null_rate","id":"null_rate"}],
            page_size=12,
            style_table={"overflowX":"auto"},
        )
        return html.Div(
            [
                html.H3("Data Quality — Selected Slice"),
                html.Ul([
                    html.Li(f"Rows: {len(df):,}"),
                    html.Li(f"Missing customer keys in dim (sample-wide): {dq['missing_customer_keys_in_dim']}"),
                    html.Li(f"Missing product keys in dim (sample-wide): {dq['missing_product_keys_in_dim']}"),
                ]),
                html.H4("Top null rates (selected slice)"),
                table,
            ]
        )

    return html.Div("Unknown tab")


if __name__ == "__main__":
    app.run(debug=True)
