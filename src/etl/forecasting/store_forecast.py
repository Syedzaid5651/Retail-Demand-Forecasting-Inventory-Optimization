import pandas as pd
import lightgbm as lgb
from google.cloud import bigquery

# Load data
sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")

# Select one product/store
row = sales.iloc[0]

day_columns = [
    col for col in sales.columns
    if col.startswith("d_")
]

# Create daily sales dataframe
df = pd.DataFrame({
    "d": day_columns,
    "sales": row[day_columns].values
})

# Add dates
df = df.merge(
    calendar[["d", "date"]],
    on="d",
    how="left"
)

df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"])

# Create features
df["lag_1"] = df["sales"].shift(1)
df["lag_7"] = df["sales"].shift(7)
df["rolling_7"] = df["sales"].shift(1).rolling(7).mean()
df["day_of_week"] = df["date"].dt.dayofweek

df = df.dropna()

features = [
    "lag_1",
    "lag_7",
    "rolling_7",
    "day_of_week"
]

X = df[features]
y = df["sales"]

# Train/test split
split = len(df) - 28

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]

# Train LightGBM
model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5,
    random_state=42,
    verbosity=-1
)

model.fit(X_train, y_train)

# Generate predictions
predictions = model.predict(X_test)

# Create forecast output
forecast = pd.DataFrame({
    "date": df.iloc[split:]["date"].values,
    "actual_sales": df.iloc[split:]["sales"].values,
    "predicted_sales": predictions
})

print("Forecast generated successfully!")
print(forecast.head())

# Connect to BigQuery
client = bigquery.Client(
    project="coherent-parity-509412-v6"
)

table_id = "coherent-parity-509412-v6.m5_retail.lightgbm_forecast"

# Upload forecast to BigQuery
job = client.load_table_from_dataframe(
    forecast,
    table_id,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )
)

job.result()

print("Forecast successfully stored in BigQuery!")
print("Table:", table_id)