{{ config(materialized='view') }}

SELECT
    day,
    date,
    wm_yr_wk,
    store_id,
    dept_id,
    cat_id,
    state_id,
    SUM(sales) AS total_sales
FROM {{ ref('int_sales_daily') }}
GROUP BY
    day,
    date,
    wm_yr_wk,
    store_id,
    dept_id,
    cat_id,
    state_id