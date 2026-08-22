# Retail Sales & Customer Insights — Complete Project Documentation

**Project Subtitle:** End-to-End Retail Analytics using PostgreSQL, Python, Pandas, Excel & Power BI  
**Author:** Senior Data Analyst & Analytics Engineer  
**Dataset Scale:** 61,926 Transactions | 19,021 Orders | 11,500 Customers | 1,220 SKUs | 12 Categories | 6 Regions  
**Financial Performance:** ₹45,828,146.55 (₹4.58 Cr) Total Revenue | ₹17,316,104.20 Profit | 37.78% Profit Margin | ₹2,409.34 AOV  

---

## 1. Executive Summary & Business Scenario

### 1.1 Business Context
The enterprise operates as a nationwide multi-category retail e-commerce platform in India, selling over 1,200 products across 12 distinct categories to 11,500 customers in 6 regional zones (West, North, South, East, Central, North-East). Management commissioned this analytics initiative to understand overall revenue drivers, customer lifetime value (CLV), repeat purchasing dynamics, regional profitability disparities, product margin contributions, and retention bottlenecks.

### 1.2 Core Business Objectives
1. **Sales Performance & Velocity:** Evaluate historical revenue trajectories, order growth, seasonal spikes (e.g., Diwali / Q4 surges), and payment channel adoption.
2. **Customer Segmentation & Retention:** Quantify repeat customer behavior, demographic spend drivers, and establish an 8-segment RFM (Recency, Frequency, Monetary) behavioral model.
3. **Merchandise & Category Profitability:** Identify high-margin vs high-volume product categories, uncover underperforming SKUs, and perform assortment rationalization.
4. **Geographic Distribution:** Assess regional revenue contribution and determine why the leading region contributes ~25% of total sales.
5. **Actionable Recommendations:** Provide data-driven executive strategies to maximize revenue, improve margins, and reactivate churn-risk customers.

---

## 2. Master Data Model & Schema Design

The project employs a Kimball star-schema model engineered for OLAP queries, scalable aggregation, and seamless multi-tool reconciliation.

### 2.1 Fact Table: `fact_sales` (61,926 rows)
Records each transaction line item with granular pricing, discount rates, and margin metrics.
- `transaction_id` (PK, VARCHAR): Unique line item identifier.
- `order_id` (FK, VARCHAR): Basket checkout session identifier.
- `order_date` (FK, DATE): Date of purchase (2024-01-01 to 2025-12-31).
- `customer_id` (FK, VARCHAR): Customer identifier.
- `product_id` (FK, VARCHAR): Product SKU identifier.
- `quantity` (INT): Units purchased (1 to 4 units).
- `unit_price` (NUMERIC): Catalog retail price in ₹.
- `discount` (NUMERIC): Promotional discount rate (0.00 to 0.20).
- `sales_amount` (NUMERIC): Net sales = `quantity * unit_price * (1 - discount)`.
- `cost_amount` (NUMERIC): COGS = `quantity * unit_cost`.
- `profit` (NUMERIC): Gross profit = `sales_amount - cost_amount`.
- `payment_method` (VARCHAR): UPI, Credit Card, Debit Card, Net Banking, COD, EMI.
- `region_id` (FK, VARCHAR): Delivery fulfillment territory.

### 2.2 Dimension Tables
- **`dim_customer` (11,500 rows):** Demographic attributes (`customer_name`, `gender`, `age`, `city`, `region_id`, `signup_date`, `customer_segment`).
- **`dim_product` (1,220 rows):** Catalog metadata (`product_name`, `category`, `subcategory`, `brand`, `unit_cost`, `unit_price`).
- **`dim_region` (6 rows):** Operational territories (`region_name`, `state`, `zone`).
- **`dim_date` (731 rows):** Date dimension with temporal hierarchy (`date`, `year`, `quarter`, `month`, `month_number`, `week`, `day`, `day_name`).

---

## 3. Data Cleaning, Validation & Anomaly Auditing

The Python data engineering pipeline (`01_data_validation.py` & `02_data_cleaning.py`) executed exhaustive audits before schema ingestion:

1. **Completeness:** 0 missing or null values across all 61,926 transaction records and 11,500 customer records.
2. **Uniqueness:** 0 duplicate primary keys detected in fact or dimension tables.
3. **Referential Integrity:** 100% foreign key match across `customer_id`, `product_id`, `region_id`, and `order_date`.
4. **Boundary Checks:** All quantities > 0, unit prices > 0, discounts strictly within `[0.00, 0.20]`.
5. **Mathematical Integrity:** Verified that `sales_amount` matches `quantity * unit_price * (1 - discount)` with zero discrepancy (`max diff = 0.00`), and `profit` matches `sales_amount - cost_amount` with zero discrepancy.
6. **Outlier Analysis (IQR Method):** 2,194 natural high-value basket transactions (3.54%) were verified as legitimate premium purchases.

---

## 4. PostgreSQL & Advanced SQL Analytics

The SQL suite (`sql/01` to `sql/08`) demonstrates production SQL development:
- **Aggregations & Joins:** Multi-table inner/left joins calculating group-level metrics, revenue contributions, and profit margins.
- **Window Functions:**
  - `LAG()`: Evaluated month-over-month revenue and order volume velocity.
  - `SUM() OVER(ORDER BY ...)`: Calculated cumulative running totals of revenue across time.
  - `DENSE_RANK() / RANK()`: Ranked top 10 customers, top 10 products, and regional sales.
  - `ROW_NUMBER() OVER(PARTITION BY category ORDER BY revenue DESC)`: Extracted the top-selling product for all 12 categories.
- **Conditional Logic (CASE):** Categorized customer age brackets, spending tiers, and RFM segments.

---

## 5. RFM Customer Segmentation Methodology

Using Python/Pandas (`06_rfm_segmentation.py`) and PostgreSQL window functions (`07_rfm_analysis.sql`), customers were segmented relative to snapshot date `2026-01-01`:

1. **Recency (R):** Days since most recent purchase (1–5 quintiles, lower days = score 5).
2. **Frequency (F):** Total distinct checkout orders (1–5 quintiles, higher orders = score 5).
3. **Monetary (M):** Total net sales spend in ₹ (1–5 quintiles, higher spend = score 5).

### RFM Segment Distribution & Insights:
| Segment | Customers | Cust % | Total Revenue (₹) | Rev % | Avg Spend (₹) | Avg Recency | Avg Orders | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Champions** | 2,009 | 17.5% | ₹15,732,350.75 | 34.3% | ₹7,830.94 | 44.0 days | 3.14 | VIP loyalty program, early product access |
| **At Risk** | 2,593 | 22.5% | ₹9,301,426.60 | 20.3% | ₹3,587.13 | 367.2 days | 1.42 | Win-back discount triggers, personalized SMS |
| **Loyal Customers** | 1,532 | 13.3% | ₹7,981,005.90 | 17.4% | ₹5,209.53 | 119.8 days | 2.11 | Cross-sell premium categories & bundles |
| **Potential Loyalists**| 1,886 | 16.4% | ₹4,421,375.40 | 9.6% | ₹2,344.31 | 50.7 days | 1.02 | Gamified second-purchase incentives |
| **Hibernating** | 1,847 | 16.1% | ₹3,771,899.50 | 8.2% | ₹2,042.18 | 197.5 days | 1.01 | Re-engagement email series, category promotions |
| **Can't Lose Them** | 709 | 6.2% | ₹3,135,176.80 | 6.8% | ₹4,421.97 | 508.8 days | 1.53 | Dedicated relationship outreach & high-value perks |
| **Lost Customers** | 727 | 6.3% | ₹1,241,388.80 | 2.7% | ₹1,707.55 | 525.5 days | 1.00 | Broad brand revival campaigns |
| **New Customers** | 197 | 1.7% | ₹243,522.80 | 0.5% | ₹1,236.16 | 47.7 days | 1.00 | Onboarding drip sequence & first-review reward |

---

## 6. Multi-Tab Excel Analytics Workbook

The workbook `excel/retail_sales_analysis.xlsx` contains 8 structured sheets:
1. **Raw Data:** 61,926 cleaned transaction rows with freeze panes and currency formatting.
2. **Data Dictionary:** Schema definitions, keys, and descriptions for all 40 table columns.
3. **Sales Analysis:** Time-series tables using `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, and MoM growth formulas.
4. **Customer Analysis:** Customer RFM profiling, demographic breakdown, and lifetime value matrix.
5. **Product Analysis:** Catalog performance, volume vs margin ranking, and top/bottom 10 tables.
6. **Regional Analysis:** Multi-zone regional revenue, orders, AOV, and contribution shares.
7. **Pivot Analysis:** Pivot tables comparing Category vs Region revenue matrices.
8. **Executive Summary:** KPI Scorecards, formatted summary cards, and executive findings.

---

## 7. Power BI Data Model, DAX & Dashboards

The Power BI implementation features a 1-to-many single-direction star schema model with 15+ production DAX measures and 4 report pages:
1. **Page 1: Executive Overview:** High-level scorecard, 24-month revenue trajectory, category bar charts, and regional share donut.
2. **Page 2: Sales Performance:** MoM growth analysis, quarterly seasonality waterfall, payment channel preferences (UPI 42%, Credit Card 28%).
3. **Page 3: Customer Insights:** Repeat customer dynamics (35.19% repeat rate driving 58.7% revenue), RFM segment treemaps, demographic breakdown (Millennials driving 49.3% spend).
4. **Page 4: Product & Category:** Category margin scatter plot, top 10 products by revenue, bottom 10 underperforming products for rationalization.

---

## 8. Multi-Tool KPI Reconciliation Table (100% Reconciled)

| KPI | PostgreSQL | Python / Pandas | Excel Workbook | Power BI DAX | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Transactions** | 61,926 | 61,926 | 61,926 | 61,926 | **PASS** |
| **Total Orders** | 19,021 | 19,021 | 19,021 | 19,021 | **PASS** |
| **Unique Customers** | 11,500 | 11,500 | 11,500 | 11,500 | **PASS** |
| **Unique Products** | 1,220 | 1,220 | 1,220 | 1,220 | **PASS** |
| **Categories** | 12 | 12 | 12 | 12 | **PASS** |
| **Regions** | 6 | 6 | 6 | 6 | **PASS** |
| **Total Revenue** | ₹45,828,146.55 | ₹45,828,146.55 | ₹45,828,146.55 | ₹45,828,146.55 | **PASS** |
| **Total Quantity Sold** | 77,567 | 77,567 | 77,567 | 77,567 | **PASS** |
| **Average Order Value (AOV)** | ₹2,409.34 | ₹2,409.34 | ₹2,409.34 | ₹2,409.34 | **PASS** |
| **Repeat Customers** | 4,047 | 4,047 | 4,047 | 4,047 | **PASS** |
| **Repeat Customer Rate** | 35.19% | 35.19% | 35.19% | 35.19% | **PASS** |
| **Total Profit** | ₹17,316,104.20 | ₹17,316,104.20 | ₹17,316,104.20 | ₹17,316,104.20 | **PASS** |
| **Profit Margin** | 37.78% | 37.78% | 37.78% | 37.78% | **PASS** |
| **Top Category** | Electronics | Electronics | Electronics | Electronics | **PASS** |
| **Top Category Revenue** | ₹12,389,744.40 | ₹12,389,744.40 | ₹12,389,744.40 | ₹12,389,744.40 | **PASS** |
| **Top Region** | West | West | West | West | **PASS** |
| **Top Region Revenue** | ₹11,515,055.25 | ₹11,515,055.25 | ₹11,515,055.25 | ₹11,515,055.25 | **PASS** |
| **Top Region Revenue %** | 25.13% | 25.13% | 25.13% | 25.13% | **PASS** |

---

## 9. Key Findings & Strategic Business Recommendations

### 9.1 Key Analytical Findings
1. **Electronics is the Primary Revenue Anchor:** Electronics generates ₹12.39M (27.04% of total revenue) with 15,338 units sold, but operates at a moderate profit margin of 26.39%.
2. **Fashion & Beauty are the Profit Engines:** Fashion & Apparel delivers the highest absolute profit (₹3.74M with 46.64% margin), while Beauty & Personal Care achieves the highest individual margin (49.82%).
3. **High Repeat Customer Leverage:** Although repeat customers represent only 35.19% (4,047 users) of the base, they generate 58.7% (₹26.90M) of total company revenue. Repeat buyers spend an average of ₹6,647 compared to ₹2,540 for one-time buyers.
4. **Western & Northern Dominance:** The West (25.13%) and North (22.50%) regions account for nearly half (47.63%) of all sales, driven by strong fulfillment in metro clusters like Mumbai, Pune, Delhi NCR, and Lucknow.
5. **High At-Risk Capital:** 2,593 customers (22.5% of the customer base) are classified as "At Risk", representing ₹9.30M in historical revenue that is currently at danger of churning.

### 9.2 Data-Driven Strategic Recommendations
1. **Electronics & High-Margin Cross-Selling:** Bundle high-demand Electronics items (e.g., smartwatches, headphones) with high-margin Beauty or Fashion accessories to increase average basket margin by an estimated 3.5–5.0%.
2. **Automated Churn Win-Back Triggers:** Implement an automated marketing workflow targeting the 2,593 "At Risk" customers using dynamic discount coupons (10–15%) timed at 90 days of inactivity, potentially recovering ₹1.8M–₹2.5M in recurring revenue.
3. **Replication of Western Region Logistics in Central & East:** Benchmark West region's delivery speed and courier partnerships to improve fulfillment velocity in East (14.99%) and Central (10.75%) zones.
4. **Assortment Rationalization for Bottom SKUs:** Discontinue or re-bundle the bottom 10 SKUs (such as slow-moving stationery and niche gourmet chocolates) to reduce inventory holding costs and free working capital.
5. **UPI & Instant Checkout Promotion:** With UPI accounting for 42.0% of checkouts, incentivize UPI payments with small cashback offers to decrease payment gateway processing fees and eliminate Cash-on-Delivery return risks.
