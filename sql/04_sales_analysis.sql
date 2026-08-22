-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: SALES & TIME-SERIES ANALYSIS (SQL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Techniques: Aggregations, Date Functions, Window Functions (LAG, SUM OVER)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. EXECUTIVE REVENUE & OVERALL BUSINESS SCORECARD
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT transaction_id) AS total_transactions,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT product_id) AS unique_products,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales_amount), 2) AS total_revenue_inr,
    ROUND(SUM(cost_amount), 2) AS total_cost_inr,
    ROUND(SUM(profit), 2) AS total_profit_inr,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS overall_profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2) AS average_order_value_aov
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- 2. YEARLY SALES PERFORMANCE (2024 vs 2025)
-- ----------------------------------------------------------------------------
SELECT 
    EXTRACT(YEAR FROM order_date) AS sales_year,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct,
    ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2) AS aov
FROM fact_sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY sales_year;

-- ----------------------------------------------------------------------------
-- 3. MONTHLY REVENUE, MOM GROWTH & RUNNING TOTAL (WINDOW FUNCTIONS)
-- ----------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS year_month,
        COUNT(DISTINCT order_id) AS monthly_orders,
        SUM(quantity) AS monthly_units,
        ROUND(SUM(sales_amount), 2) AS monthly_revenue,
        ROUND(SUM(profit), 2) AS monthly_profit
    FROM fact_sales
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
)
SELECT 
    year_month,
    monthly_orders,
    monthly_units,
    monthly_revenue,
    monthly_profit,
    ROUND(monthly_revenue / monthly_orders, 2) AS monthly_aov,
    -- Window Function: LAG() to retrieve previous month revenue
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    -- Window Function: Calculate Month-over-Month (MoM) Growth %
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) / 
        LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100, 
        2
    ) AS mom_growth_pct,
    -- Window Function: Cumulative Running Total of Revenue
    SUM(monthly_revenue) OVER (ORDER BY year_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total_revenue
FROM monthly_metrics
ORDER BY year_month;

-- ----------------------------------------------------------------------------
-- 4. PAYMENT METHOD PERFORMANCE & ADOPTION
-- ----------------------------------------------------------------------------
SELECT 
    payment_method,
    COUNT(DISTINCT transaction_id) AS transaction_count,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS total_units,
    ROUND(SUM(sales_amount), 2) AS total_revenue,
    ROUND((SUM(sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales
GROUP BY payment_method
ORDER BY total_revenue DESC;
