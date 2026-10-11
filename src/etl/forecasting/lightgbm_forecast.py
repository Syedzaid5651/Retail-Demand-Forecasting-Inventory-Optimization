import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error

# Load dataset
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

# Remove missing values
df = df.dropna()

features = [
    "lag_1",
    "lag_7",
    "rolling_7",
    "day_of_week"
]

X = df[features]
y = df["sales"]

# Use the last 28 days for testing
split = len(df) - 28

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# Create LightGBM model
model = lgb.LGBMRegressor(
    objective="regression",
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5,
    random_state=42,
    verbosity=-1
)

# Train model
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

# Calculate MAE
mae = mean_absolute_error(y_test, predictions)

print("LightGBM model trained successfully!")
print("Features used:", features)
print(f"LightGBM MAE: {mae:.4f}")