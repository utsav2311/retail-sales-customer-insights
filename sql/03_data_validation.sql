-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: DATA INTEGRITY & VALIDATION (SQL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Performs full automated audit of database constraints, logic, and integrity
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. NULL VALUES & MISSING DATA AUDIT
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) - COUNT(transaction_id) AS null_txns,
    COUNT(*) - COUNT(order_id) AS null_orders,
    COUNT(*) - COUNT(customer_id) AS null_customers,
    COUNT(*) - COUNT(product_id) AS null_products,
    COUNT(*) - COUNT(sales_amount) AS null_sales,
    COUNT(*) - COUNT(profit) AS null_profits
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- 2. PRIMARY KEY UNIQUENESS AUDIT
-- ----------------------------------------------------------------------------
SELECT transaction_id, COUNT(*) AS duplicate_count
FROM fact_sales
GROUP BY transaction_id
HAVING COUNT(*) > 1;

SELECT customer_id, COUNT(*) AS duplicate_count
FROM dim_customer
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS duplicate_count
FROM dim_product
GROUP BY product_id
HAVING COUNT(*) > 1;

-- ----------------------------------------------------------------------------
-- 3. REFERENTIAL INTEGRITY / ORPHAN RECORDS AUDIT
-- ----------------------------------------------------------------------------
-- Check for orphan customer records in fact_sales
SELECT COUNT(*) AS orphan_sales_customers
FROM fact_sales fs
LEFT JOIN dim_customer dc ON fs.customer_id = dc.customer_id
WHERE dc.customer_id IS NULL;

-- Check for orphan product records in fact_sales
SELECT COUNT(*) AS orphan_sales_products
FROM fact_sales fs
LEFT JOIN dim_product dp ON fs.product_id = dp.product_id
WHERE dp.product_id IS NULL;

-- Check for orphan region records in fact_sales
SELECT COUNT(*) AS orphan_sales_regions
FROM fact_sales fs
LEFT JOIN dim_region dr ON fs.region_id = dr.region_id
WHERE dr.region_id IS NULL;

-- ----------------------------------------------------------------------------
-- 4. MATHEMATICAL FORMULA CONSISTENCY AUDIT
-- ----------------------------------------------------------------------------
-- Verify Sales Amount = Quantity * Unit Price * (1 - Discount)
SELECT 
    COUNT(*) AS invalid_sales_calculation_count,
    MAX(ABS(sales_amount - ROUND(quantity * unit_price * (1 - discount), 2))) AS max_sales_discrepancy
FROM fact_sales
WHERE ABS(sales_amount - ROUND(quantity * unit_price * (1 - discount), 2)) > 0.01;

-- Verify Profit = Sales Amount - Cost Amount
SELECT 
    COUNT(*) AS invalid_profit_calculation_count,
    MAX(ABS(profit - ROUND(sales_amount - cost_amount, 2))) AS max_profit_discrepancy
FROM fact_sales
WHERE ABS(profit - ROUND(sales_amount - cost_amount, 2)) > 0.01;

-- ----------------------------------------------------------------------------
-- 5. NUMERICAL & DOMAIN BOUNDARY AUDIT
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(CASE WHEN quantity <= 0 THEN 1 END) AS invalid_quantity_count,
    COUNT(CASE WHEN unit_price <= 0 THEN 1 END) AS invalid_unit_price_count,
    COUNT(CASE WHEN discount < 0.00 OR discount > 1.00 THEN 1 END) AS invalid_discount_count,
    COUNT(CASE WHEN sales_amount < 0 THEN 1 END) AS negative_sales_count
FROM fact_sales;
