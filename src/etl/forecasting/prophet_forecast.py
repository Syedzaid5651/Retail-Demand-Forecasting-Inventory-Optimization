import pandas as pd
from prophet import Prophet


# -----------------------------------
# Load M5 sales and calendar data
# -----------------------------------

sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")


# -----------------------------------
# Select the first product-store series
# -----------------------------------

row = sales.iloc[0]


# -----------------------------------
# Get daily sales columns
# -----------------------------------

day_columns = [col for col in sales.columns if col.startswith("d_")]


# -----------------------------------
# Create daily dataset
# -----------------------------------

df = pd.DataFrame({
    "d": day_columns,
    "y": row[day_columns].values
})


# -----------------------------------
# Map M5 day IDs to actual dates
# -----------------------------------

calendar_dates = calendar[["d", "date"]]

df = df.merge(calendar_dates, on="d", how="left")


# -----------------------------------
# Prepare Prophet columns
# -----------------------------------

df = df.rename(columns={
    "date": "ds"
})

df["ds"] = pd.to_datetime(df["ds"])
df["y"] = pd.to_numeric(df["y"])


# -----------------------------------
# Prepare M5 holiday/event data
# -----------------------------------

holidays_1 = calendar[["date", "event_name_1"]].dropna()

holidays_1 = holidays_1.rename(columns={
    "date": "ds",
    "event_name_1": "holiday"
})


holidays_2 = calendar[["date", "event_name_2"]].dropna()

holidays_2 = holidays_2.rename(columns={
    "date": "ds",
    "event_name_2": "holiday"
})


# Combine both event columns
holidays = pd.concat(
    [holidays_1, holidays_2],
    ignore_index=True
)

holidays["ds"] = pd.to_datetime(holidays["ds"])


# -----------------------------------
# Train Prophet with M5 holidays
# -----------------------------------

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    holidays=holidays
)


# -----------------------------------
# Fit the model
# -----------------------------------

model.fit(df[["ds", "y"]])


# -----------------------------------
# Create a 28-day forecast
# -----------------------------------

future = model.make_future_dataframe(periods=28)

forecast = model.predict(future)


# -----------------------------------
# Display forecast
# -----------------------------------

print("\nProphet model with M5 holidays trained successfully!")

print("\nForecast:")

print(
    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].tail(28)
)
import pandas as pd
from prophet import Prophet


# ==========================================
# Load M5 sales and calendar data
# ==========================================

sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")


# ==========================================
# Select the first product-store combination
# ==========================================

row = sales.iloc[0]


# ==========================================
# Get daily sales columns
# ==========================================

day_columns = [
    col for col in sales.columns
    if col.startswith("d_")
]


# ==========================================
# Create daily dataset
# ==========================================

df = pd.DataFrame({
    "d": day_columns,
    "y": row[day_columns].values
})


# ==========================================
# Map M5 day IDs to actual dates
# ==========================================

calendar_dates = calendar[["d", "date"]]

df = df.merge(
    calendar_dates,
    on="d",
    how="left"
)


# ==========================================
# Prepare data for Prophet
# ==========================================

df = df.rename(columns={"date": "ds"})

df["ds"] = pd.to_datetime(df["ds"])
df["y"] = pd.to_numeric(df["y"])


# ==========================================
# Create M5 holiday/event dataframe
# ==========================================

holidays = calendar[
    ["date", "event_name_1", "event_type_1"]
].dropna(
    subset=["event_name_1"]
).copy()

holidays = holidays.rename(
    columns={
        "date": "ds",
        "event_name_1": "holiday"
    }
)

holidays["ds"] = pd.to_datetime(holidays["ds"])


# ==========================================
# Train Prophet with M5 holidays
# ==========================================

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    holidays=holidays
)


# ==========================================
# Train the model
# ==========================================

model.fit(df[["ds", "y"]])


# ==========================================
# Create a 28-day forecast
# ==========================================

future = model.make_future_dataframe(
    periods=28
)

forecast = model.predict(future)


# ==========================================
# Display forecast
# ==========================================

print("\nProphet model with M5 holidays trained successfully!")

print("\nForecast:")

print(
    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].tail(28)
)


# ==========================================
# Evaluate Prophet model
# ==========================================

evaluation = forecast[
    ["ds", "yhat"]
].merge(
    df[["ds", "y"]],
    on="ds",
    how="inner"
)


# ==========================================
# Calculate Mean Absolute Error (MAE)
# ==========================================

mae = (
    evaluation["y"] -
    evaluation["yhat"]
).abs().mean()


print("\nProphet Model Evaluation:")

print(f"MAE: {mae:.4f}")