{{ config(materialized='view') }}

SELECT
    s.id,
    s.item_id,
    s.dept_id,
    s.cat_id,
    s.store_id,
    s.state_id,
    s.day,
    s.sales,
    c.date,
    c.wm_yr_wk,
    c.weekday,
    c.wday,
    c.month,
    c.year,
    c.event_name_1,
    c.event_type_1,
    c.event_name_2,
    c.event_type_2,
    c.snap_CA,
    c.snap_TX,
    c.snap_WI

FROM {{ ref('stg_sales_daily') }} s

LEFT JOIN {{ ref('stg_calendar') }} c
    ON s.day = c.d