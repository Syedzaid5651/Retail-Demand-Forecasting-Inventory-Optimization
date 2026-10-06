import pandas as pd
import lightgbm as lgb

# Load dataset
sales = pd.read_csv("data/raw/sales_train_validation.csv")
calendar = pd.read_csv("data/raw/calendar.csv")

# Select one product/store
row = sales.iloc[0]

# Get all daily sales columns
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

# Convert columns to correct data types
df["date"] = pd.to_datetime(df["date"])
df["sales"] = pd.to_numeric(df["sales"])

# Create forecasting features
df["lag_1"] = df["sales"].shift(1)
df["lag_7"] = df["sales"].shift(7)
df["rolling_7"] = df["sales"].shift(1).rolling(7).mean()
df["day_of_week"] = df["date"].dt.dayofweek

# Convert features to numeric
df["lag_1"] = pd.to_numeric(df["lag_1"])
df["lag_7"] = pd.to_numeric(df["lag_7"])
df["rolling_7"] = pd.to_numeric(df["rolling_7"])
df["day_of_week"] = pd.to_numeric(df["day_of_week"])

# Remove missing values
df = df.dropna()

# Define features and target
features = [
    "lag_1",
    "lag_7",
    "rolling_7",
    "day_of_week"
]

X = df[features]
y = df["sales"]

# Create LightGBM model
model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)

# Train model
model.fit(X, y)

print("LightGBM model trained successfully!")
print("Features used:", features)