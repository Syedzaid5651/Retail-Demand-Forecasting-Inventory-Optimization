{{ config(materialized='view') }}

SELECT
    wm_yr_wk,
    store_id,
    dept_id,
    cat_id,
    state_id,
    SUM(total_sales) AS weekly_sales
FROM {{ ref('mart_daily_sales') }}
GROUP BY
    wm_yr_wk,
    store_id,
    dept_id,
    cat_id,
    state_id