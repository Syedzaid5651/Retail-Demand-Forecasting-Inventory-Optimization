import pandas as pd
from prophet import Prophet

# Load M5 sales and calendar data
sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")

# Select the first product-store combination for the initial Prophet test
row = sales.iloc[0]

# Get daily sales columns
day_columns = [col for col in sales.columns if col.startswith("d_")]

# Create daily dataset
df = pd.DataFrame({
    "d": day_columns,
    "y": row[day_columns].values
})

# Map M5 day IDs to actual dates
calendar_dates = calendar[["d", "date"]]
df = df.merge(calendar_dates, on="d", how="left")

# Prophet requires columns named ds and y
df = df.rename(columns={"date": "ds"})

df["ds"] = pd.to_datetime(df["ds"])
df["y"] = pd.to_numeric(df["y"])

# Train Prophet
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(df[["ds", "y"]])

# Create a 28-day forecast
future = model.make_future_dataframe(periods=28)

forecast = model.predict(future)

print("\nProphet model trained successfully!")
print("\nForecast:")
print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(28))