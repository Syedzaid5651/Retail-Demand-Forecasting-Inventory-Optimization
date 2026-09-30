{{ config(materialized='view') }}

SELECT
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    store_id,
    dept_id,
    cat_id,
    state_id,
    SUM(total_sales) AS monthly_sales
FROM {{ ref('mart_daily_sales') }}
GROUP BY
    year,
    month,
    store_id,
    dept_id,
    cat_id,
    state_id