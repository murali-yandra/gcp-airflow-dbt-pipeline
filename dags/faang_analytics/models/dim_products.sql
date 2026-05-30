{{ config(materialized='table') }}

WITH raw_data AS (
    -- We are no longer hardcoding! We are using the contact book.
    SELECT * FROM {{ source('cloud_landing_zone', 'sample_products') }}
),

transformed AS (
    SELECT
        product_id,
        product_name AS product_title,
        price_usd AS price,
        
        -- Business Logic 1: Categorize the pricing
        CASE
            WHEN price_usd < 50.00 THEN 'Budget'
            WHEN price_usd >= 50.00 AND price_usd < 200.00 THEN 'Mid-Range'
            ELSE 'Premium'
        END AS price_category

    FROM raw_data
)

SELECT * FROM transformed