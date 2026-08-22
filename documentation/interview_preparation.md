# Data Analyst Interview Preparation Guide — Retail Sales & Customer Insights

An in-depth, interview-ready guide containing 30+ technical, behavioral, and business questions and answers referencing the exact empirical results of this project.

---

## 1. Project Overview & Elevator Pitch

### Q1: Can you walk me through your Retail Sales & Customer Insights project?
**Sample Answer:**
> "Certainly! In this project, I built an end-to-end analytics platform for a multi-category Indian retail e-commerce company operating across 6 geographic regions. The project spanned 61,926 transactions, 19,021 orders, 11,500 unique customers, and 1,220 products across 12 categories, generating ₹4.58 Crore (₹45.83M) in total revenue with a 37.78% gross margin.
>
> I followed a rigorous workflow: Raw Data Validation & Cleaning in Python -> Relational Star Schema modeling in PostgreSQL -> Advanced SQL Analytics with window functions -> Behavioral RFM Customer Segmentation -> Professional Multi-tab Excel Dashboarding with dynamic formulas -> Power BI Executive Dashboarding with DAX -> and 100% Multi-Tool KPI Reconciliation.
>
> Key business findings revealed that while Electronics was our largest revenue driver at ₹12.39M (27.04%), Fashion & Beauty delivered our highest profit margins (up to 49.8%). Additionally, our 35.19% repeat customer base drove 58.7% of total revenue. Based on these findings, I formulated data-backed strategies for automated churn win-back, cross-selling high-margin lines, and regional fulfillment replication."

### Q2: What was your specific role and tech stack?
**Sample Answer:**
> "I served as the Lead Data Analyst and Analytics Engineer. I designed the Kimball star schema, wrote Python validation and cleaning pipelines, developed 27 PostgreSQL queries using CTEs and window functions, built an 8-tier RFM segmentation engine in Pandas, developed an 8-sheet Excel workbook with `SUMIFS`/`XLOOKUP`, and designed 4 interactive Power BI dashboard pages with 15+ DAX measures."

---

## 2. PostgreSQL & SQL Technical Questions

### Q3: How did you design the database schema, and why did you choose a Star Schema?
**Sample Answer:**
> "I designed a Kimball Star Schema with one central fact table (`fact_sales` with 61,926 rows) and four dimension tables: `dim_customer` (11,500 rows), `dim_product` (1,220 rows), `dim_region` (6 rows), and `dim_date` (731 rows). 
> 
> A star schema was chosen because it de-normalizes dimensions to minimize complex multi-table joins during OLAP reporting, enables fast aggregations, simplifies DAX filtering in Power BI, and provides an intuitive structure for business queries."

### Q4: How did you calculate the Repeat Customer Rate in SQL?
**Sample Answer:**
> "In retail, a repeat customer is defined as a customer who has placed more than one distinct order. I used a Common Table Expression (CTE) to aggregate distinct orders per customer and then calculated the ratio:
> ```sql
> WITH customer_orders AS (
>     SELECT customer_id, COUNT(DISTINCT order_id) AS orders_count
>     FROM fact_sales
>     GROUP BY customer_id
> )
> SELECT 
>     COUNT(customer_id) AS total_customers,
>     COUNT(CASE WHEN orders_count > 1 THEN 1 END) AS repeat_customers,
>     ROUND(100.0 * COUNT(CASE WHEN orders_count > 1 THEN 1 END) / COUNT(customer_id), 2) AS repeat_customer_rate_pct
> FROM customer_orders;
> ```
> In our dataset, this produced exactly 4,047 repeat customers out of 11,500 total customers, representing a **35.19% repeat customer rate**."

### Q5: How did you calculate Month-over-Month (MoM) revenue growth using window functions?
**Sample Answer:**
> "I used the `LAG()` window function to retrieve the previous month's revenue and computed the percentage change:
> ```sql
> WITH monthly_rev AS (
>     SELECT 
>         TO_CHAR(order_date, 'YYYY-MM') AS year_month,
>         SUM(sales_amount) AS monthly_revenue
>     FROM fact_sales
>     GROUP BY TO_CHAR(order_date, 'YYYY-MM')
> )
> SELECT 
>     year_month,
>     monthly_revenue,
>     LAG(monthly_revenue, 1) OVER (ORDER BY year_month) AS prev_month_revenue,
>     ROUND(
>         ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) / 
>         LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100, 2
>     ) AS mom_growth_pct
> FROM monthly_rev
> ORDER BY year_month;
> ```
> This highlighted notable festive spikes in October (+20.0%) and November (+5.1%) during peak Diwali shopping."

### Q6: What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`, and where did you apply them?
**Sample Answer:**
> "`ROW_NUMBER()` assigns a unique sequential integer to every row regardless of ties. `RANK()` leaves gaps in rank numbering after ties (e.g., 1, 2, 2, 4), while `DENSE_RANK()` does not leave gaps (e.g., 1, 2, 2, 3).
> 
> In my project:
> - I used `DENSE_RANK()` to rank top customers and product revenues where identical sales totals should share ranks without skipping subsequent positions.
> - I used `ROW_NUMBER() OVER (PARTITION BY category ORDER BY sales_amount DESC)` to filter for `WHERE rank_in_cat = 1` to extract the single top-selling product for each of the 12 categories."

---

## 3. Python & Pandas Technical Questions

### Q7: How did you validate data quality and handle potential anomalies in Python?
**Sample Answer:**
> "I developed a dedicated audit suite (`01_data_validation.py`) checking:
> 1. Missing/Null values across all columns (`df.isnull().sum()`).
> 2. Duplicate transaction IDs and customer IDs (`df.duplicated().sum()`).
> 3. Referential integrity between transaction foreign keys and dimension primary keys.
> 4. Numerical validation: checked that quantities were strictly positive, discounts were within `[0.00, 0.20]`, and mathematically verified that `sales_amount == quantity * unit_price * (1 - discount)` with zero discrepancy.
> 5. Outlier detection using the IQR method (`Q3 + 1.5 * IQR`), identifying 2,194 natural high-value basket checkouts."

### Q8: How did you implement RFM Customer Segmentation in Python?
**Sample Answer:**
> "I set a snapshot reference date of `2026-01-01` (one day after the maximum transaction date in the 2-year dataset). For each customer:
> - **Recency:** `snapshot_date - max(order_date)` in days.
> - **Frequency:** `order_id.nunique()`.
> - **Monetary:** `sales_amount.sum()`.
> 
> I assigned 1–5 scores using `pd.qcut()` with rank ordering to handle ties. Then, I applied custom business logic mapping R, F, and M scores to 8 distinct behavioral segments: *Champions, Loyal Customers, Potential Loyalists, New Customers, At Risk, Can't Lose Them, Hibernating, and Lost Customers*.
> 
> The results showed that **Champions (17.5% of users)** generated **34.3% of total revenue**, while **At Risk (22.5% of users)** represented **₹9.30M** in endangered revenue."

---

## 4. Excel Analytics Technical Questions

### Q9: Which Excel formulas did you use and how was the workbook organized?
**Sample Answer:**
> "I built an 8-sheet corporate workbook (`retail_sales_analysis.xlsx`):
> - **Formulas Used:** `SUMIFS` and `COUNTIFS` for dynamic multi-criteria aggregations, `AVERAGEIFS` for segmented AOV, `XLOOKUP` for catalog metadata retrieval, and date calculations for MoM growth.
> - **Architecture:** Separate sheets for *Raw Data*, *Data Dictionary*, *Sales Analysis*, *Customer Analysis*, *Product Analysis*, *Regional Analysis*, *Pivot Analysis*, and an *Executive Summary* dashboard.
> - **Formatting:** Corporate navy/slate palette, freeze panes on all headers, structured borders, and explicit currency (`₹#,##0.00`) and percentage formatting."

---

## 5. Power BI & DAX Technical Questions

### Q10: How did you calculate Repeat Customer Rate in DAX?
**Sample Answer:**
> "I created a DAX measure leveraging `CALCULATE`, `FILTER`, and `VALUES`:
> ```dax
> Repeat Customers = 
> CALCULATE(
>     [Total Customers],
>     FILTER(
>         VALUES('fact_sales'[customer_id]),
>         CALCULATE(DISTINCTCOUNT('fact_sales'[order_id])) > 1
>     )
> )
> 
> Repeat Customer Rate % = 
> DIVIDE([Repeat Customers], [Total Customers], 0)
> ```
> This dynamically responds to all report slicers (such as Year, Region, or Category) while correctly evaluating order counts per customer."

### Q11: How did you implement Time Intelligence for Month-over-Month Growth?
**Sample Answer:**
> "I used `DATEADD` against our designated `dim_date` calendar table:
> ```dax
> Previous Month Revenue = 
> CALCULATE(
>     [Total Revenue],
>     DATEADD('dim_date'[date], -1, MONTH)
> )
> 
> MoM Revenue Growth % = 
> VAR PrevMonthRev = [Previous Month Revenue]
> RETURN
>     IF(
>         ISBLANK(PrevMonthRev),
>         BLANK(),
>         DIVIDE([Total Revenue] - PrevMonthRev, PrevMonthRev, 0)
>     )
> ```"

---

## 6. Business Strategy & Analytical Insights

### Q12: Why does the West region contribute approximately 25% of total revenue?
**Sample Answer:**
> "Our regional analysis shows that the **West Region generated ₹11,515,055.25**, accounting for **25.13% of total revenue**. This leadership is driven by higher customer density across major economic hubs (Mumbai, Pune, Ahmedabad, Surat) where average order value remained strong (₹2,400.97) and order fulfillment velocity was highest."

### Q13: If you were advising the VP of E-Commerce, what top 3 recommendations would you present?
**Sample Answer:**
> 1. **At-Risk Win-Back Automation:** Trigger automated marketing sequences with 10–15% discount incentives for the 2,593 'At Risk' customers at 90 days of inactivity to protect ₹9.30M in revenue.
> 2. **Cross-Selling High-Margin Categories:** Bundle high-demand Electronics (26.39% margin) with Beauty & Personal Care (49.82% margin) and Fashion (46.64% margin) to increase average basket margin.
> 3. **UPI Payment Prioritization:** UPI represents 42.0% of checkouts; providing seamless UPI 1-click checkout reduces payment gateway drop-offs and eliminates Cash-on-Delivery return costs."

---

## 7. Validated Resume Bullets (Ready to Copy-Paste)

- **Engineered an end-to-end Retail Analytics Suite** across PostgreSQL, Python, Excel, and Power BI analyzing 61,926 transactions, 19,021 orders, and 11,500 customers generating ₹4.58 Cr ($550K+) revenue.
- **Architected a Kimball Star Schema Database** in PostgreSQL with 27 analytical SQL queries utilizing window functions (`LAG`, `DENSE_RANK`, `PARTITION BY`) and CTEs to track MoM revenue velocity and customer lifetime value.
- **Developed an 8-Segment RFM Customer Model** in Python/Pandas across 11,500 users, discovering that Champions (17.5% of base) generate 34.3% of revenue, and designing win-back workflows for 2,593 at-risk customers.
- **Constructed an 8-Sheet Executive Excel Workbook** with dynamic `SUMIFS`, `XLOOKUP`, and Pivot Tables, alongside 4 Power BI report pages featuring 15+ custom DAX measures with 100% multi-tool mathematical reconciliation.
