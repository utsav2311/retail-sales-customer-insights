-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: RFM CUSTOMER SEGMENTATION (SQL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Techniques: CTEs, NTILE(5) Window Functions, Complex CASE Business Logic
-- ============================================================================

-- ----------------------------------------------------------------------------
-- RFM SEGMENTATION PIPELINE IN PURE SQL
-- ----------------------------------------------------------------------------
WITH customer_rfm_raw AS (
    SELECT 
        customer_id,
        -- Recency: Days since last order relative to 2026-01-01
        DATE '2026-01-01' - MAX(order_date) AS recency_days,
        -- Frequency: Distinct orders count
        COUNT(DISTINCT order_id) AS frequency_orders,
        -- Monetary: Total sales amount
        ROUND(SUM(sales_amount), 2) AS monetary_spend,
        ROUND(SUM(profit), 2) AS total_profit
    FROM fact_sales
    GROUP BY customer_id
),
customer_rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        frequency_orders,
        monetary_spend,
        total_profit,
        -- Score 1-5 for Recency (Lower days = higher score 5)
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Score 1-5 for Frequency (Higher orders = higher score 5)
        NTILE(5) OVER (ORDER BY frequency_orders ASC) AS f_score,
        -- Score 1-5 for Monetary (Higher spend = higher score 5)
        NTILE(5) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM customer_rfm_raw
),
customer_segments AS (
    SELECT 
        customer_id,
        recency_days,
        frequency_orders,
        monetary_spend,
        total_profit,
        r_score,
        f_score,
        m_score,
        (r_score || f_score || m_score) AS rfm_score,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
            WHEN r_score = 1 AND (f_score >= 4 OR m_score >= 4) THEN 'Can''t Lose Them'
            WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
            WHEN r_score <= 2 AND (f_score >= 3 OR m_score >= 3) THEN 'At Risk'
            WHEN r_score >= 4 AND (f_score >= 2 OR m_score >= 2) THEN 'Potential Loyalists'
            WHEN r_score >= 4 AND f_score = 1 THEN 'New Customers'
            WHEN (r_score IN (2, 3)) AND f_score <= 2 THEN 'Hibernating'
            WHEN r_score = 1 AND f_score <= 2 THEN 'Lost Customers'
            ELSE 'Hibernating'
        END AS rfm_segment
    FROM customer_rfm_scores
)
-- Segment Executive Summary
SELECT 
    rfm_segment,
    COUNT(customer_id) AS total_customers,
    ROUND((COUNT(customer_id)::NUMERIC / (SELECT COUNT(*) FROM customer_segments)) * 100, 2) AS customer_share_pct,
    ROUND(SUM(monetary_spend), 2) AS total_segment_revenue,
    ROUND((SUM(monetary_spend) / (SELECT SUM(sales_amount) FROM fact_sales)) * 100, 2) AS revenue_share_pct,
    ROUND(AVG(monetary_spend), 2) AS avg_spend_per_customer,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency_orders), 2) AS avg_order_frequency
FROM customer_segments
GROUP BY rfm_segment
ORDER BY total_segment_revenue DESC;
