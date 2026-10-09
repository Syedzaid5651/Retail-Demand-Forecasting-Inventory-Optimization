import math
import streamlit as st
import pandas as pd
from google.cloud import bigquery

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

PROJECT_ID = "coherent-parity-509412-v6"
TABLE_ID = (
    "coherent-parity-509412-v6."
    "m5_retail.lightgbm_forecast"
)

# ==================================================
# 2. LOAD DATA FROM BIGQUERY
# ==================================================
@st.cache_data(ttl=300)
def load_forecast_data():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT *
        FROM {TABLE_ID}
        ORDER BY date
    """

    data = client.query(query).to_dataframe()

    required_columns = {
        "date",
        "actual_sales",
        "predicted_sales"
    }

    missing = required_columns - set(data.columns)

    if missing:
        raise ValueError(
            f"BigQuery table is missing columns: {sorted(missing)}"
        )

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    )

    for column in ["actual_sales", "predicted_sales"]:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    data = data.dropna(
        subset=["date", "predicted_sales"]
    )

    return data


# ==================================================
# 3. LOAD DATA AND HANDLE ERRORS
# ==================================================
st.title("📊 Retail Demand Forecasting & Inventory Optimization")

st.write(
    "Explore demand forecasts, compare model predictions, "
    "simulate pricing scenarios and estimate inventory needs."
)

if st.button("🔄 Refresh BigQuery Data"):
    load_forecast_data.clear()
    st.rerun()

try:
    df = load_forecast_data()

except Exception as error:
    st.error("Unable to load data from BigQuery.")
    st.code(str(error))
    st.info(
        "Check your Google Cloud authentication, table name "
        "and BigQuery permissions."
    )
    st.stop()

if df.empty:
    st.warning("The BigQuery table contains no usable forecast records.")
    st.stop()

st.success("Forecast data loaded successfully from BigQuery!")

# ==================================================
# 4. SIDEBAR FILTERS
# ==================================================
st.sidebar.header("Dashboard Filters")

filtered_df = df.copy()

# Date filter
st.sidebar.subheader("Date Range")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date)
            & (filtered_df["date"].dt.date <= end_date)
        ]

elif selected_dates:
    filtered_df = filtered_df[
        filtered_df["date"].dt.date == selected_dates
    ]

# Optional dimension filters.
# These appear only if the relevant columns exist.
dimension_options = [
    ("store_id", "Store"),
    ("dept_id", "Department"),
    ("cat_id", "Category"),
    ("item_id", "Product")
]

for column, label in dimension_options:
    if column in filtered_df.columns:
        values = sorted(
            filtered_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        if values:
            choice = st.sidebar.selectbox(
                f"Select {label}",
                ["All"] + values,
                key=f"filter_{column}"
            )

            if choice != "All":
                filtered_df = filtered_df[
                    filtered_df[column].astype(str) == choice
                ]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# Number of records to display
record_limit = st.sidebar.slider(
    "Number of records to display",
    min_value=1,
    max_value=min(100, len(filtered_df)),
    value=min(10, len(filtered_df))
)

# Use only numeric, valid sales records for calculations.
filtered_df = filtered_df.copy()

filtered_df["actual_sales"] = pd.to_numeric(
    filtered_df["actual_sales"], errors="coerce"
)

filtered_df["predicted_sales"] = pd.to_numeric(
    filtered_df["predicted_sales"], errors="coerce"
)

filtered_df = filtered_df.dropna(
    subset=["predicted_sales"]
)

if filtered_df.empty:
    st.warning("No valid predicted sales remain after filtering.")
    st.stop()

# ==================================================
# 5. SALES SUMMARY
# ==================================================
st.subheader("📌 Sales Summary")

actual_total = filtered_df["actual_sales"].sum()
predicted_total = filtered_df["predicted_sales"].sum()

evaluation_df = filtered_df.dropna(
    subset=["actual_sales", "predicted_sales"]
)

if not evaluation_df.empty:
    mae = (
        evaluation_df["actual_sales"]
        .sub(evaluation_df["predicted_sales"])
        .abs()
        .mean()
    )
else:
    mae = None

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Actual Sales",
    f"{actual_total:,.0f}"
)

col2.metric(
    "Total Predicted Sales",
    f"{predicted_total:,.2f}"
)

col3.metric(
    "Mean Absolute Error (MAE)",
    f"{mae:.4f}" if mae is not None else "Unavailable"
)

st.caption(
    "MAE is calculated only for records with both actual "
    "and predicted sales. Lower MAE generally indicates "
    "smaller prediction errors."
)

# ==================================================
# 6. FORECAST TABLE AND CHART
# ==================================================
st.subheader("📋 Demand Forecast")

display_df = (
    filtered_df
    .sort_values("date")
    .tail(record_limit)
    .copy()
)

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.subheader("📈 Actual vs Predicted Sales")

chart_data = display_df.set_index("date")[
    ["actual_sales", "predicted_sales"]
]

st.line_chart(chart_data, width="stretch")

# ==================================================
# 7. WHAT-IF PRICE SCENARIO
# ==================================================
st.divider()
st.header("💰 What-If Price Scenario")

st.write(
    "Estimate how a price reduction might affect demand. "
    "This is a scenario estimate using an assumed elasticity, "
    "not a price-response model trained on historical price changes."
)

price_drop = st.slider(
    "Simulated price reduction (%)",
    min_value=0,
    max_value=30,
    value=10,
    step=1
)

elasticity = st.slider(
    "Assumed demand elasticity",
    min_value=0.0,
    max_value=3.0,
    value=1.5,
    step=0.1,
    help=(
        "Illustrative assumption: 1.5 means a 1% price "
        "reduction is assumed to increase demand by about 1.5%."
    )
)

# Simplified linear scenario assumption.
demand_change_pct = price_drop * elasticity

scenario_df = filtered_df.copy()

scenario_df["scenario_predicted_sales"] = (
    scenario_df["predicted_sales"]
    * (1 + demand_change_pct / 100)
)

baseline_demand = filtered_df["predicted_sales"].sum()
scenario_demand = scenario_df["scenario_predicted_sales"].sum()

scenario_increase = scenario_demand - baseline_demand

c1, c2, c3 = st.columns(3)

c1.metric(
    "Baseline Predicted Demand",
    f"{baseline_demand:,.2f}"
)

c2.metric(
    "Scenario Demand",
    f"{scenario_demand:,.2f}",
    delta=f"{demand_change_pct:.1f}% assumed change"
)

c3.metric(
    "Estimated Additional Units",
    f"{scenario_increase:,.2f}"
)

st.caption(
    "The assumed demand increase is price reduction (%) × "
    "assumed elasticity. Actual customer response may differ."
)

# ==================================================
# 8. INVENTORY OPTIMIZATION
# ==================================================
st.divider()
st.header("📦 Inventory Optimization")

st.write(
    "Estimate target stock and reorder quantity using "
    "predicted demand, supplier lead time and safety stock."
)

inv1, inv2, inv3 = st.columns(3)

with inv1:
    current_stock = st.number_input(
        "Current inventory (units)",
        min_value=0,
        value=0,
        step=1
    )

with inv2:
    lead_time = st.number_input(
        "Supplier lead time (days)",
        min_value=1,
        max_value=365,
        value=7,
        step=1
    )

with inv3:
    safety_days = st.number_input(
        "Safety stock (days of demand)",
        min_value=0,
        max_value=365,
        value=3,
        step=1
    )

# This is an average of available prediction records.
# It is not automatically a genuine future forecast.
average_daily_demand = max(
    0.0,
    float(scenario_df["scenario_predicted_sales"].mean())
)

lead_time_demand = average_daily_demand * lead_time
safety_stock = average_daily_demand * safety_days

target_stock = math.ceil(
    lead_time_demand + safety_stock
)

reorder_quantity = max(
    0,
    target_stock - int(current_stock)
)

i1, i2, i3, i4 = st.columns(4)

i1.metric(
    "Average Daily Demand",
    f"{average_daily_demand:.2f}"
)

i2.metric(
    "Lead-Time Demand",
    f"{lead_time_demand:.2f}"
)

i3.metric(
    "Target Stock",
    f"{target_stock:,}"
)

i4.metric(
    "Suggested Reorder",
    f"{reorder_quantity:,} units"
)

if reorder_quantity > 0:
    st.warning(
        f"Estimated replenishment needed: {reorder_quantity:,} units."
    )
else:
    st.success(
        "Current stock meets or exceeds the estimated target stock."
    )

st.caption(
    "Planning estimate: target stock = average scenario demand "
    "per day × (lead time + safety-stock days). This calculation "
    "does not account for existing purchase orders, supplier "
    "constraints, expiry, minimum order quantities or costs."
)

# ==================================================
# 9. EXPORT RESULTS
# ==================================================
st.divider()
st.subheader("📥 Export Results")

export_df = scenario_df.sort_values("date").copy()

export_df["assumed_price_reduction_pct"] = price_drop
export_df["assumed_demand_elasticity"] = elasticity
export_df["current_inventory_units"] = int(current_stock)
export_df["supplier_lead_time_days"] = int(lead_time)
export_df["safety_stock_days"] = int(safety_days)
export_df["estimated_average_daily_demand"] = average_daily_demand
export_df["estimated_target_stock_units"] = target_stock
export_df["suggested_reorder_units"] = reorder_quantity

csv_data = export_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Forecast and Inventory CSV",
    data=csv_data,
    file_name="retail_forecast_inventory.csv",
    mime="text/csv"
)

# ==================================================
# 10. PROJECT NOTES
# ==================================================
st.info(
    "This dashboard reads forecasts from BigQuery. "
    "The date filter only selects records already stored in the table. "
    "Genuine future-demand forecasts must be generated and stored "
    "for future dates before the dashboard can display them."
)
