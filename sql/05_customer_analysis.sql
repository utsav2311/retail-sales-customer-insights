-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: CUSTOMER ANALYTICS (SQL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Techniques: CTEs, Subqueries, CASE statements, Window Functions (DENSE_RANK)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. REPEAT CUSTOMER RATE & RETENTION SUMMARY
-- ----------------------------------------------------------------------------
WITH customer_order_counts AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(sales_amount) AS customer_revenue,
        SUM(profit) AS customer_profit
    FROM fact_sales
    GROUP BY customer_id
)
SELECT 
    COUNT(customer_id) AS total_unique_customers,
    COUNT(CASE WHEN total_orders > 1 THEN 1 END) AS repeat_customers_count,
    COUNT(CASE WHEN total_orders = 1 THEN 1 END) AS onetime_customers_count,
    ROUND((COUNT(CASE WHEN total_orders > 1 THEN 1.0 END) / COUNT(customer_id)) * 100, 2) AS repeat_customer_rate_pct,
    ROUND(SUM(CASE WHEN total_orders > 1 THEN customer_revenue ELSE 0 END), 2) AS repeat_customer_revenue,
    ROUND(SUM(CASE WHEN total_orders = 1 THEN customer_revenue ELSE 0 END), 2) AS onetime_customer_revenue,
    ROUND((SUM(CASE WHEN total_orders > 1 THEN customer_revenue ELSE 0 END) / SUM(customer_revenue)) * 100, 2) AS repeat_revenue_contribution_pct
FROM customer_order_counts;

-- ----------------------------------------------------------------------------
-- 2. TOP 10 HIGHEST-VALUE CUSTOMERS (WITH WINDOW RANKING)
-- ----------------------------------------------------------------------------
WITH customer_summary AS (
    SELECT 
        fs.customer_id,
        dc.customer_name,
        dc.city,
        dr.region_name,
        dc.customer_segment,
        COUNT(DISTINCT fs.order_id) AS total_orders,
        SUM(fs.quantity) AS total_units_bought,
        ROUND(SUM(fs.sales_amount), 2) AS total_spend_inr,
        ROUND(SUM(fs.profit), 2) AS total_profit_inr
    FROM fact_sales fs
    INNER JOIN dim_customer dc ON fs.customer_id = dc.customer_id
    INNER JOIN dim_region dr ON fs.region_id = dr.region_id
    GROUP BY fs.customer_id, dc.customer_name, dc.city, dr.region_name, dc.customer_segment
)
SELECT 
    DENSE_RANK() OVER (ORDER BY total_spend_inr DESC) AS customer_rank,
    customer_id,
    customer_name,
    city,
    region_name,
    customer_segment,
    total_orders,
    total_units_bought,
    total_spend_inr,
    total_profit_inr,
    ROUND(total_spend_inr / total_orders, 2) AS customer_aov
FROM customer_summary
ORDER BY total_spend_inr DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- 3. CUSTOMER DEMOGRAPHICS ANALYSIS (AGE GROUP CLASSIFICATION VIA CASE)
-- ----------------------------------------------------------------------------
WITH customer_sales AS (
    SELECT 
        fs.customer_id,
        dc.gender,
        dc.age,
        CASE 
            WHEN dc.age BETWEEN 18 AND 25 THEN '18-25 (Gen Z)'
            WHEN dc.age BETWEEN 26 AND 35 THEN '26-35 (Millennials)'
            WHEN dc.age BETWEEN 36 AND 50 THEN '36-50 (Gen X)'
            ELSE '51+ (Seniors)'
        END AS age_group,
        dc.customer_segment,
        fs.sales_amount,
        fs.profit
    FROM fact_sales fs
    INNER JOIN dim_customer dc ON fs.customer_id = dc.customer_id
)
SELECT 
    age_group,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales_amount), 2) AS group_revenue,
    ROUND((SUM(sales_amount) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_share_pct,
    ROUND(SUM(profit), 2) AS group_profit,
    ROUND((SUM(profit) / SUM(sales_amount)) * 100, 2) AS profit_margin_pct
FROM customer_sales
GROUP BY age_group
ORDER BY group_revenue DESC;

-- ----------------------------------------------------------------------------
-- 4. CUSTOMER SPENDING TIER CLASSIFICATION (CASE STATEMENT)
-- ----------------------------------------------------------------------------
WITH customer_totals AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(sales_amount) AS total_spent
    FROM fact_sales
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN total_spent >= 15000 THEN 'Tier 1: High Value (₹15,000+)'
        WHEN total_spent >= 7500 THEN 'Tier 2: Mid-High Value (₹7,500 - ₹14,999)'
        WHEN total_spent >= 3000 THEN 'Tier 3: Moderate Value (₹3,000 - ₹7,499)'
        ELSE 'Tier 4: Low Value (< ₹3,000)'
    END AS spending_tier,
    COUNT(customer_id) AS customer_count,
    ROUND((COUNT(customer_id)::NUMERIC / (SELECT COUNT(*) FROM customer_totals)) * 100, 2) AS customer_pct,
    ROUND(SUM(total_spent), 2) AS tier_revenue,
    ROUND((SUM(total_spent) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_pct,
    ROUND(AVG(total_spent), 2) AS avg_spend_per_customer
FROM customer_totals
GROUP BY 
    CASE 
        WHEN total_spent >= 15000 THEN 'Tier 1: High Value (₹15,000+)'
        WHEN total_spent >= 7500 THEN 'Tier 2: Mid-High Value (₹7,500 - ₹14,999)'
        WHEN total_spent >= 3000 THEN 'Tier 3: Moderate Value (₹3,000 - ₹7,499)'
        ELSE 'Tier 4: Low Value (< ₹3,000)'
    END
ORDER BY tier_revenue DESC;
