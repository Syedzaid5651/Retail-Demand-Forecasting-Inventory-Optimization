-- Zaid's Project
-- Retail Demand Forecasting & Inventory Optimization
-- Week 1: Data Quality Checks
-- M5 Forecasting Dataset


-- ============================================================
-- 1. CHECK ROW COUNTS FOR ALL RAW TABLES
-- ============================================================

SELECT 'calendar_raw' AS table_name, COUNT(*) AS row_count
FROM 'coherent-parity-509412-v6.m5_retail.calendar_raw'

UNION ALL

SELECT 'sales_train_validation_raw', COUNT(*)
FROM 'coherent-parity-509412-v6.m5_retail.sales_train_validation_raw'

UNION ALL

SELECT 'sales_train_evaluation_raw', COUNT(*)
FROM 'coherent-parity-509412-v6.m5_retail.sales_train_evaluation_raw'

UNION ALL

SELECT 'sell_prices_raw', COUNT(*)
FROM 'coherent-parity-509412-v6.m5_retail.sell_prices_raw'

UNION ALL

SELECT 'sample_submission_raw', COUNT(*)
FROM 'coherent-parity-509412-v6.m5_retail.sample_submission_raw';


-- ============================================================
-- 2. CHECK FOR NULL VALUES IN CALENDAR DATA
-- ============================================================

SELECT
    COUNTIF(date IS NULL) AS null_dates,
    COUNTIF(wm_yr_wk IS NULL) AS null_week_numbers,
    COUNTIF(event_name_1 IS NULL) AS null_event_name_1,
    COUNTIF(event_type_1 IS NULL) AS null_event_type_1
FROM 'coherent-parity-509412-v6.m5_retail.calendar_raw';


-- ============================================================
-- 3. CHECK FOR INVALID NEGATIVE PRICES
-- ============================================================

SELECT
    COUNT(*) AS negative_price_rows
FROM 'coherent-parity-509412-v6.m5_retail.sell_prices_raw'
WHERE sell_price < 0;


-- ============================================================
-- 4. CHECK FOR DUPLICATE CALENDAR DATES
-- ============================================================

SELECT
    date,
    COUNT(*) AS duplicate_count
FROM 'coherent-parity-509412-v6.m5_retail.calendar_raw'
GROUP BY date
HAVING COUNT(*) > 1;