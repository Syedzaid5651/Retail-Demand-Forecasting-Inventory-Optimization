{{ config(materialized='view') }}

SELECT
    store_id,
    item_id,
    wm_yr_wk,
    sell_price

FROM {{ ref('stg_sell_prices') }}