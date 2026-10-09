import streamlit as st
from google.cloud import bigquery
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Retail Demand Forecasting & Inventory Optimization")

st.write(
    "View demand forecasts generated using the LightGBM model."
)

# Connect to BigQuery
client = bigquery.Client(
    project="coherent-parity-509412-v6"
)

# BigQuery table
table_id = "coherent-parity-509412-v6.m5_retail.lightgbm_forecast"

# Query forecast data
query = f"""
SELECT
    date,
    actual_sales,
    predicted_sales
FROM {table_id}
ORDER BY date
"""

# Load data
df = client.query(query).to_dataframe()

# Success message
st.success("Forecast data loaded successfully from BigQuery!")

# Show data
st.subheader("📈 Demand Forecast")

st.dataframe(
    df,
    use_container_width=True
)

# Chart
st.subheader("Actual vs Predicted Sales")

chart_data = df.set_index("date")[
    ["actual_sales", "predicted_sales"]
]

st.line_chart(chart_data)