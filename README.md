# Retail-Demand-Forecasting-Inventory-Optimization

Retail demand forecasting and inventory optimization system using machine learning to predict product-level demand and recommend optimal stock levels, reducing overstock and stockouts.

## Dataset

This project uses the *M5 Forecasting – Accuracy* dataset from Kaggle, which contains daily unit sales data for thousands of products across multiple stores and states, along with calendar and pricing information.

Files used:
- calendar.csv — dates, events, and holidays
- sales_train_validation.csv — historical daily unit sales
- sell_prices.csv — product pricing by store and week

## Tech Stack

- *Python* — Pandas, PyArrow, python-dotenv
- *Google BigQuery* — data warehousing and querying
- *Machine Learning* (upcoming) — Prophet, LightGBM
- *Version Control* — Git & GitHub

## Project Plan

- *Week 1* — Set up local environment, load and explore the dataset
- *Week 2* — Clean and transform data (ETL pipeline)
- *Week 3* — Build and evaluate forecasting models
- *Week 4* — Inventory optimization logic and final reporting

## Folder Structure 

data/         -> raw and processed datasets
src/etl/      -> ETL scripts
src/utils/    -> helper/utility functions
sql/          -> SQL queries
notebooks/    -> exploration and analysis notebooks
outputs/      -> results, reports, and visualizations

## Project Progress

### BigQuery Setup
- Created Google Cloud project: Retail Demand Forecasting
- Created BigQuery dataset: m5_retail
- Loaded all M5 source files into BigQuery
- Created raw tables:
  - calendar_raw
  - sales_train_validation_raw
  - sales_train_evaluation_raw
  - sell_prices_raw
  - sample_submission_raw
- Verified all five tables successfully.

### Week 3 Day 1
Implemented Prophet-based time-series forecasting with a 28-day forecast for the M5 sales dataset.

### Week 3 Day 2
- Added a LightGBM forecasting model (src/etl/forecasting/lightgbm_forecast.py)
- Engineered features: lag features (7, 14, 28 days), rolling mean/std, calendar features (day of week, month, events, holidays), and price features from sell_prices
- Used a time-based train/validation split to avoid data leakage

### Week 3 Day 3
- Evaluated Prophet vs LightGBM on the 28-day validation window
- Metrics: RMSE, MAE, and WRMSSE (the M5 competition metric)
- Results: Prophet RMSE = [x], LightGBM RMSE = [y]
- Selected [model] as the primary model based on validation error

### Week 3 Day 4
- Saved forecasts to BigQuery (m5_retail.forecast_results)
- Added forecast vs actual visualizations in outputs/
- Connected forecast output to app.py for viewing predictions

How to Run the Dashboard

1. Activate the Python virtual environment.
2. Install the required dependencies using "pip install -r requirements.txt".
3. Start the Streamlit application using "streamlit run app.py".
4. Open the local URL displayed in the terminal.
5. Ensure Google Cloud authentication is configured to access BigQuery.

Project Validation

- Verify the dashboard loads forecast data from BigQuery.
- Check sales summary metrics and charts.
- Test price scenario calculations and inventory reorder suggestions.
- Confirm CSV export works correctly.
- Review Git status before sharing the project.