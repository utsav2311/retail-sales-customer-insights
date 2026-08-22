-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: MASTER 27 ANALYTICAL SQL QUERIES
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Comprehensive Analytical Queries covering All 27 Business Questions
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Q1: What is total revenue?
-- Aggregation query calculating net revenue across all valid transactions
-- ----------------------------------------------------------------------------
SELECT ROUND(SUM(sales_amount), 2) AS total_revenue_inr
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q2: How many transactions exist?
-- Counts total transaction line items recorded in the fact table
-- ----------------------------------------------------------------------------
SELECT COUNT(transaction_id) AS total_transactions
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q3: How many orders exist?
-- Counts distinct checkout orders placed by customers
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q4: How many unique customers exist?
-- Counts distinct active transacting customers
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q5: How many unique products exist?
-- Counts total catalog products purchased
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT product_id) AS unique_products
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q6: How many categories exist?
-- Counts distinct merchandise categories
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT category) AS total_categories
FROM dim_product;

-- ----------------------------------------------------------------------------
-- Q7: How many regions exist?
-- Counts distinct geographic delivery operational regions
-- ----------------------------------------------------------------------------
SELECT COUNT(DISTINCT region_id) AS total_regions
FROM dim_region;

-- ----------------------------------------------------------------------------
-- Q8: What is the average order value (AOV)?
-- Total Net Revenue divided by Total Distinct Orders
-- ----------------------------------------------------------------------------
SELECT ROUND(SUM(sales_amount) / COUNT(DISTINCT order_id), 2) AS average_order_value_aov
FROM fact_sales;

-- ----------------------------------------------------------------------------
-- Q9: What is monthly revenue?
-- Time-series aggregation grouping sales by year and month
-- ----------------------------------------------------------------------------
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS year_month,
    ROUND(SUM(sales_amount), 2) AS monthly_revenue
FROM fact_sales
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY year_month;

-- ----------------------------------------------------------------------------
-- Q10: What is monthly order growth?
-- Uses LAG() window function to calculate percentage change in monthly order volume
-- ----------------------------------------------------------------------------
WITH monthly_orders AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS year_month,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_sales
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
)
SELECT 
    year_month,
    order_count,
    LAG(order_count, 1) OVER (ORDER BY year_month) AS prev_month_orders,
    ROUND(
        ((order_count - LAG(order_count, 1) OVER (ORDER BY year_month))::NUMERIC / 
        LAG(order_count, 1) OVER (ORDER BY year_month)) * 100, 2
    ) AS monthly_order_growth_pct
FROM monthly_orders
ORDER BY year_month;

-- ----------------------------------------------------------------------------
-- Q11: What is yearly revenue?
-- Aggregates sales revenue by calendar year
-- ----------------------------------------------------------------------------
SELECT 
    EXTRACT(YEAR FROM order_date) AS sales_year,
    ROUND(SUM(sales_amount), 2) AS yearly_revenue
FROM fact_sales
GROUP BY EXTRACT(YEAR FROM order_date)
ORDER BY sales_year;

-- ----------------------------------------------------------------------------
-- Q12: Which category generates the highest revenue?
-- Joins fact table with product dimension and ranks by total sales
-- ----------------------------------------------------------------------------
SELECT 
    dp.category,
    ROUND(SUM(fs.sales_amount), 2) AS category_revenue
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY category_revenue DESC
LIMIT 1;

-- ----------------------------------------------------------------------------
-- Q13: Which region generates the highest revenue?
-- Joins fact table with region dimension and ranks by total revenue
-- ----------------------------------------------------------------------------
SELECT 
    dr.region_name,
    ROUND(SUM(fs.sales_amount), 2) AS region_revenue
FROM fact_sales fs
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
GROUP BY dr.region_name
ORDER BY region_revenue DESC
LIMIT 1;

-- ----------------------------------------------------------------------------
-- Q14: Which region contributes approximately 25% of revenue?
-- Calculates percentage share of total revenue per region
-- ----------------------------------------------------------------------------
SELECT 
    dr.region_name,
    ROUND(SUM(fs.sales_amount), 2) AS region_revenue,
    ROUND((SUM(fs.sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct
FROM fact_sales fs
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
GROUP BY dr.region_name
ORDER BY region_revenue DESC;

-- ----------------------------------------------------------------------------
-- Q15: What is the repeat customer rate?
-- (Customers with > 1 Order / Total Unique Customers) * 100
-- ----------------------------------------------------------------------------
WITH customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS orders_count
    FROM fact_sales
    GROUP BY customer_id
)
SELECT 
    COUNT(customer_id) AS total_customers,
    COUNT(CASE WHEN orders_count > 1 THEN 1 END) AS repeat_customers,
    ROUND((COUNT(CASE WHEN orders_count > 1 THEN 1.0 END) / COUNT(customer_id)) * 100, 2) AS repeat_customer_rate_pct
FROM customer_orders;

-- ----------------------------------------------------------------------------
-- Q16: Who are the top 10 customers?
-- Ranked by total monetary expenditure
-- ----------------------------------------------------------------------------
SELECT 
    fs.customer_id,
    dc.customer_name,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    ROUND(SUM(fs.sales_amount), 2) AS total_spend
FROM fact_sales fs
INNER JOIN dim_customer dc ON fs.customer_id = dc.customer_id
GROUP BY fs.customer_id, dc.customer_name
ORDER BY total_spend DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q17: What are the top 10 products?
-- Ranked by total revenue generated
-- ----------------------------------------------------------------------------
SELECT 
    fs.product_id,
    dp.product_name,
    dp.category,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS product_revenue
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY fs.product_id, dp.product_name, dp.category
ORDER BY product_revenue DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q18: What are the bottom-performing products?
-- Ranked by lowest sales revenue
-- ----------------------------------------------------------------------------
SELECT 
    fs.product_id,
    dp.product_name,
    dp.category,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.sales_amount), 2) AS product_revenue
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY fs.product_id, dp.product_name, dp.category
ORDER BY product_revenue ASC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Q19: Which category generates the highest profit?
-- ----------------------------------------------------------------------------
SELECT 
    dp.category,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY total_profit DESC
LIMIT 1;

-- ----------------------------------------------------------------------------
-- Q20: Which region generates the highest profit?
-- ----------------------------------------------------------------------------
SELECT 
    dr.region_name,
    ROUND(SUM(fs.profit), 2) AS total_profit,
    ROUND((SUM(fs.profit) / SUM(fs.sales_amount)) * 100, 2) AS profit_margin_pct
FROM fact_sales fs
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
GROUP BY dr.region_name
ORDER BY total_profit DESC
LIMIT 1;

-- ----------------------------------------------------------------------------
-- Q21: What is each category's revenue contribution?
-- ----------------------------------------------------------------------------
SELECT 
    dp.category,
    ROUND(SUM(fs.sales_amount), 2) AS category_revenue,
    ROUND((SUM(fs.sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct
FROM fact_sales fs
INNER JOIN dim_product dp ON fs.product_id = dp.product_id
GROUP BY dp.category
ORDER BY category_revenue DESC;

-- ----------------------------------------------------------------------------
-- Q22: What is each region's revenue contribution?
-- ----------------------------------------------------------------------------
SELECT 
    dr.region_name,
    ROUND(SUM(fs.sales_amount), 2) AS region_revenue,
    ROUND((SUM(fs.sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_contribution_pct
FROM fact_sales fs
INNER JOIN dim_region dr ON fs.region_id = dr.region_id
GROUP BY dr.region_name
ORDER BY region_revenue DESC;

-- ----------------------------------------------------------------------------
-- Q23: What is the running total of revenue?
-- Window function SUM() OVER() ordered by month
-- ----------------------------------------------------------------------------
WITH monthly_rev AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS year_month,
        ROUND(SUM(sales_amount), 2) AS monthly_revenue
    FROM fact_sales
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
)
SELECT 
    year_month,
    monthly_revenue,
    SUM(monthly_revenue) OVER (ORDER BY year_month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue
FROM monthly_rev
ORDER BY year_month;

-- ----------------------------------------------------------------------------
-- Q24: What is month-over-month revenue growth?
-- LAG() window function calculating percentage change
-- ----------------------------------------------------------------------------
WITH monthly_rev AS (
    SELECT 
        TO_CHAR(order_date, 'YYYY-MM') AS year_month,
        ROUND(SUM(sales_amount), 2) AS monthly_revenue
    FROM fact_sales
    GROUP BY TO_CHAR(order_date, 'YYYY-MM')
)
SELECT 
    year_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) / 
        LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100, 2
    ) AS mom_growth_pct
FROM monthly_rev
ORDER BY year_month;

-- ----------------------------------------------------------------------------
-- Q25: What is the top product in every category?
-- Partitioned ranking using ROW_NUMBER() OVER (PARTITION BY category)
-- ----------------------------------------------------------------------------
WITH ranked_prods AS (
    SELECT 
        dp.category,
        fs.product_id,
        dp.product_name,
        ROUND(SUM(fs.sales_amount), 2) AS product_revenue,
        ROW_NUMBER() OVER (PARTITION BY dp.category ORDER BY SUM(fs.sales_amount) DESC) AS rank_in_cat
    FROM fact_sales fs
    INNER JOIN dim_product dp ON fs.product_id = dp.product_id
    GROUP BY dp.category, fs.product_id, dp.product_name
)
SELECT category, product_id, product_name, product_revenue
FROM ranked_prods
WHERE rank_in_cat = 1
ORDER BY product_revenue DESC;

-- ----------------------------------------------------------------------------
-- Q26: Which customers are repeat customers?
-- Identifies all customers who placed 2 or more orders with summary metrics
-- ----------------------------------------------------------------------------
SELECT 
    fs.customer_id,
    dc.customer_name,
    COUNT(DISTINCT fs.order_id) AS total_orders,
    ROUND(SUM(fs.sales_amount), 2) AS customer_total_spend
FROM fact_sales fs
INNER JOIN dim_customer dc ON fs.customer_id = dc.customer_id
GROUP BY fs.customer_id, dc.customer_name
HAVING COUNT(DISTINCT fs.order_id) > 1
ORDER BY total_orders DESC, customer_total_spend DESC;

-- ----------------------------------------------------------------------------
-- Q27: Which customers have not purchased recently? (At-Risk / Inactive)
-- Identifies customers whose last purchase was > 180 days ago relative to 2026-01-01
-- ----------------------------------------------------------------------------
SELECT 
    fs.customer_id,
    dc.customer_name,
    MAX(fs.order_date) AS last_purchase_date,
    (DATE '2026-01-01' - MAX(fs.order_date)) AS days_since_last_purchase,
    COUNT(DISTINCT fs.order_id) AS historical_orders,
    ROUND(SUM(fs.sales_amount), 2) AS historical_spend
FROM fact_sales fs
INNER JOIN dim_customer dc ON fs.customer_id = dc.customer_id
GROUP BY fs.customer_id, dc.customer_name
HAVING (DATE '2026-01-01' - MAX(fs.order_date)) > 180
ORDER BY days_since_last_purchase DESC, historical_spend DESC;
