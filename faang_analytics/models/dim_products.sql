{{ config(materialized='table') }}

WITH raw_data AS (
    -- We are querying the table directly for now.
    SELECT * FROM products_raw
),

transformed AS (
    SELECT
        id AS product_id,
        title AS product_title,
        price,
        stock,
        
        -- Business Logic 1: Categorize the pricing
        CASE
            WHEN price < 20.00 THEN 'Budget'
            WHEN price >= 20.00 AND price < 50.00 THEN 'Mid-Range'
            ELSE 'Premium'
        END AS price_category,
        
        -- Business Logic 2: Create a boolean flag for inventory management
        CASE
            WHEN stock > 0 THEN TRUE
            ELSE FALSE
        END AS is_in_stock

    FROM raw_data
)

SELECT * FROM transformed