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
