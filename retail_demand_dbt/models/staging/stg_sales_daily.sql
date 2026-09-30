{{ config(materialized='view') }}

WITH sales_unpivoted AS (

    SELECT
        id,
        item_id,
        dept_id,
        cat_id,
        store_id,
        state_id,
        day,
        sales
    FROM {{ source('m5_retail', 'sales_train_validation_raw') }}
    UNPIVOT (
        sales FOR day IN (
            {% for i in range(1, 1914) %}
            d_{{ i }}{% if not loop.last %}, {% endif %}
            {% endfor %}
        )
    )

)

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
FROM sales_unpivoted s
LEFT JOIN {{ ref('stg_calendar') }} c
    ON s.day = c.d