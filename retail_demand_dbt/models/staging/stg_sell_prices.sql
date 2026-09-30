{{ config(materialized='view') }}

SELECT
    store_id,
    item_id,
    wm_yr_wk,
    sell_price
FROM {{ source('m5_retail', 'sell_prices_raw') }}