-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: PRODUCT, CATEGORY & REGIONAL ANALYSIS (SQL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Techniques: Multi-Table Joins, PARTITION BY, DENSE_RANK, Window Functions
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CATEGORY PERFORMANCE RANKINGS & REVENUE CONTRIBUTION
-- ----------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(fs.sales_amount) DESC) AS category_rank,
    dp.category,
    COUNT(DISTINCT fs.product_id) AS active_products,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS total_revenue,
    ROUND((SUM(fs.sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 2. REGIONAL PERFORMANCE & LEADING REGION CONTRIBUTION
-- ----------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(fs.sales_amount) DESC) AS regional_rank,
    dr.region_name,
    dr.zone,
    COUNT(DISTINCT fs.customer_id) AS unique_customers,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS total_revenue,
    ROUND((SUM(fs.sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(fs.sales_amount) / COUNT(DISTINCT fs.order_id), 2) AS regional_aov
FROM fact_sales fs
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
GROUP BY dr.region_name, dr.zone
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- 3. TOP 10 PRODUCTS BY REVENUE
-- ----------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(fs.sales_amount) DESC) AS product_rank,
    fs.product_id,
    dp.product_name,
    dp.category,
    dp.brand,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS total_revenue,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY fs.product_id, dp.product_name, dp.category, dp.brand
ORDER BY total_revenue DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 4. BOTTOM 10 PRODUCTS BY REVENUE (UNDERPERFORMING)
-- ----------------------------------------------------------------------------
SELECT 
    DENSE_RANK() OVER (ORDER BY SUM(fs.sales_amount) ASC) AS bottom_rank,
    fs.product_id,
    dp.product_name,
    dp.category,
    dp.brand,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS total_revenue,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY fs.product_id, dp.product_name, dp.category, dp.brand
ORDER BY total_revenue ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 5. TOP PRODUCT IN EVERY CATEGORY (PARTITION BY WINDOW FUNCTION)
-- ----------------------------------------------------------------------------
WITH category_product_ranks AS (
    SELECT 
        dp.category,
        fs.product_id,
        dp.product_name,
        dp.brand,
        SUM(fs.quantity) AS units_sold,
        ROUND(SUM(fs.sales_amount), 2) AS product_revenue,
        ROUND(SUM(fs.profit), 2) AS product_profit,
        ROW_NUMBER() OVER (PARTITION BY dp.category ORDER BY SUM(fs.sales_amount) DESC) AS rank_in_category
    FROM fact_sales fs
    INNER JOIN dim_product dp ON fs.product_id = dp.product_id
    GROUP BY dp.category, fs.product_id, dp.product_name, dp.brand
)
SELECT 
    category,
    product_id,
    product_name,
    brand,
    units_sold,
    product_revenue,
    product_profit
FROM category_product_ranks
WHERE rank_in_category = 1
ORDER BY product_revenue DESC;
