-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: DATA INGESTION SCRIPT
-- Database Engine: PostgreSQL 14+ / psql
-- Ingests cleaned star schema CSV files into database tables
-- ============================================================================

-- Ensure working directory or absolute paths match your environment:
-- If running via psql CLI, execute: \i sql/02_load_data.sql

BEGIN;

-- 1. Load Dimension Tables First (Parent tables)
\copy dim_region (region_id, region_name, state, zone) FROM 'data/cleaned/dim_region.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy dim_customer (customer_id, customer_name, gender, age, city, region_id, signup_date, customer_segment) FROM 'data/cleaned/dim_customer.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy dim_product (product_id, product_name, category, subcategory, brand, unit_cost, unit_price) FROM 'data/cleaned/dim_product.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy dim_date (date, year, quarter, month, month_number, week, day, day_name) FROM 'data/cleaned/dim_date.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

-- 2. Load Fact Table (Child table referencing parent dimensions)
\copy fact_sales (transaction_id, order_id, order_date, customer_id, product_id, quantity, unit_price, discount, sales_amount, cost_amount, profit, payment_method, region_id) FROM 'data/cleaned/fact_sales.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

COMMIT;

-- Verify row counts after ingestion
SELECT 'dim_region' AS table_name, COUNT(*) AS row_count FROM dim_region
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_date', COUNT(*) FROM dim_date
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;
