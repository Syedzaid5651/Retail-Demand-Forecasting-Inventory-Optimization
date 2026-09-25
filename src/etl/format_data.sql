 -- Zaid's Project
-- Retail Demand Forecasting & Inventory Optimization
-- Week 1: Data Formatting
-- M5 Forecasting Dataset


-- ============================================================
-- 1. FORMAT CALENDAR DATA
-- ============================================================

CREATE OR REPLACE VIEW
  coherent-parity-509412-v6.m5_retail.calendar_clean
AS
SELECT
  SAFE_CAST(date AS DATE) AS date,
  wm_yr_wk,
  weekday,
  wday,
  month,
  year,
  event_name_1,
  event_type_1,
  event_name_2,
  event_type_2,
  snap_CA,
  snap_TX,
  snap_WI
FROM
  coherent-parity-509412-v6.m5_retail.calendar_raw;


-- ============================================================
-- 2. FORMAT SALES VOLUME DATA
-- ============================================================

CREATE OR REPLACE VIEW
  coherent-parity-509412-v6.m5_retail.sales_clean
AS
SELECT
  *
FROM
  coherent-parity-509412-v6.m5_retail.sales_train_validation_raw;


-- ============================================================
-- 3. FORMAT PRICING DATA
-- ============================================================

CREATE OR REPLACE VIEW
  coherent-parity-509412-v6.m5_retail.prices_clean
AS
SELECT
  store_id,
  item_id,
  wm_yr_wk,
  SAFE_CAST(sell_price AS NUMERIC) AS sell_price
FROM
  coherent-parity-509412-v6.m5_retail.sell_prices_raw;


-- ============================================================
-- 4. VERIFY FORMATTED DATA
-- ============================================================

SELECT
  'calendar_clean' AS object_name,
  COUNT(*) AS row_count
FROM
  coherent-parity-509412-v6.m5_retail.calendar_clean

UNION ALL

SELECT
  'sales_clean' AS object_name,
  COUNT(*) AS row_count
FROM
  coherent-parity-509412-v6.m5_retail.sales_clean

UNION ALL

SELECT
  'prices_clean' AS object_name,
  COUNT(*) AS row_count
FROM
  coherent-parity-509412-v6.m5_retail.prices_clean;