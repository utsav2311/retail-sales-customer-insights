# 📊 Retail Sales & Customer Insights
> **End-to-End Enterprise Retail Analytics using PostgreSQL, Python, Pandas, Excel & Power BI (5-Year Depth: 2021 – 2026 YTD)**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Interactive_Dashboard-GitHub_Pages-2563EB?style=for-the-badge)](https://utsav2311.github.io/retail-sales-customer-insights/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/utsav2311/retail-sales-customer-insights)
[![Download Master Excel](https://img.shields.io/badge/📥_Download-Master_Excel_(Raw_+_Clean)-10B981?style=for-the-badge)](https://raw.githubusercontent.com/utsav2311/retail-sales-customer-insights/main/data/retail_raw_and_cleaned_master.xlsx)

![Python](https://img.shields.io/badge/Python-3.13-blue.svg?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg?logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg?logo=pandas&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811.svg?logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-Advanced_Formulas-217346.svg?logo=microsoftexcel&logoColor=white)
![Status](https://img.shields.io/badge/Validation-100%25_PASS-success.svg)

---

### 🌐 Live Interactive Analytics Preview & Data Downloads
- 🚀 **[Click here to view the Live Interactive Dashboard](https://utsav2311.github.io/retail-sales-customer-insights/)** (Interactive charts, dynamic slicers, 5-year revenue trajectory, RFM matrix, and SQL runner directly in browser).
- 📥 **[Download Master Dataset Excel (Raw + Cleaned Data - 11 Sheets)](https://raw.githubusercontent.com/utsav2311/retail-sales-customer-insights/main/data/retail_raw_and_cleaned_master.xlsx)**
- 📥 **[Download Excel Analytics Workbook (retail_sales_analysis.xlsx)](https://raw.githubusercontent.com/utsav2311/retail-sales-customer-insights/main/excel/retail_sales_analysis.xlsx)**
- 📥 **[Download Multi-Tool KPI Reconciliation Matrix (kpi_reconciliation.xlsx)](https://raw.githubusercontent.com/utsav2311/retail-sales-customer-insights/main/documentation/kpi_reconciliation.xlsx)**

---

## 📈 5-Year Annual Revenue Trajectory (2021 – 2026 YTD)

Historical annual growth demonstrating organic revenue scaling from ₹16.4 Lakhs to ₹1.58 Crore (YTD 2026):

| Calendar Year | Total Revenue (₹) | Gross Profit (₹) | Profit Margin % | Total Orders | Transactions | Average Order Value (AOV) | YoY Growth % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2021** | ₹1,640,390.30 | ₹618,496.64 | 37.70% | 660 | 2,195 | ₹2,485.44 | Baseline |
| **2022** | ₹3,255,953.00 | ₹1,231,245.66 | 37.82% | 1,336 | 4,396 | ₹2,437.09 | **+98.5%** |
| **2023** | ₹5,219,348.30 | ₹1,971,698.61 | 37.78% | 2,174 | 7,084 | ₹2,400.80 | **+60.3%** |
| **2024** | ₹8,635,175.40 | ₹3,246,551.75 | 37.60% | 3,563 | 11,680 | ₹2,423.57 | **+65.4%** |
| **2025** | ₹14,250,158.95 | ₹5,396,007.05 | 37.87% | 5,827 | 19,290 | ₹2,445.54 | **+65.0%** |
| **2026 (YTD)** | ₹15,817,691.10 | ₹5,980,505.08 | 37.81% | 6,496 | 21,374 | ₹2,434.99 | **Peak Run-Rate** |
| **5-Year Total** | **₹48,818,717.05 (₹4.88 Cr)** | **₹18,444,504.22** | **37.78%** | **20,056** | **66,019** | **₹2,434.12** | — |

---

## 🌟 Executive Summary & Portfolio Metrics

| Core Metric | Actual Calculated Value | Project Target Range | Status |
| :--- | :--- | :--- | :--- |
| **Total Transactions** | **66,019** | 50,000+ | ✅ PASS |
| **Total Orders** | **20,056** | - | ✅ PASS |
| **Unique Customers** | **12,000** | 10,000+ | ✅ PASS |
| **Unique Products** | **1,220** | 1,000+ | ✅ PASS |
| **Product Categories** | **12** | 10+ | ✅ PASS |
| **Geographic Regions** | **6** | 5+ | ✅ PASS |
| **Total Net Revenue** | **₹48,818,717.05 (₹4.88 Cr)** | ₹2.00 Cr+ | ✅ PASS |
| **Total Gross Profit** | **₹18,444,504.22** | - | ✅ PASS |
| **Gross Profit Margin**| **37.78%** | 35% - 40% | ✅ PASS |
| **Average Order Value (AOV)** | **₹2,434.12** | ~₹2,200 | ✅ PASS |
| **Repeat Customer Rate** | **35.40% (4,248 users)** | ~35% | ✅ PASS |
| **Leading Category** | **Electronics (₹13.20M - 27.04%)** | Electronics #1 | ✅ PASS |
| **Leading Region** | **West (₹12.28M - 25.15%)** | ~25% contribution | ✅ PASS |

---

## 🏗️ Relational Star Schema Architecture

```
                  ┌──────────────────────┐
                  │      dim_date        │
                  ├──────────────────────┤
                  │ date (PK)            │
                  │ year, quarter, month │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ *
┌──────────────────────┐   ┌─┴────────────────────┐   ┌──────────────────────┐
│     dim_customer     │   │      fact_sales      │   │     dim_product      │
├──────────────────────┤   ├──────────────────────┤   ├──────────────────────┤
│ customer_id (PK)     ├───┤ customer_id (FK)     ├───┤ product_id (PK)      │
│ customer_name        │ 1*│ order_id             │* 1│ product_name         │
│ gender, age, city    │   │ order_date (FK)      │   │ category, subcat     │
│ customer_segment     │   │ product_id (FK)      │   │ brand, unit_cost/prc │
└──────────┬───────────┘   │ region_id (FK)       │   └──────────────────────┘
           │               │ quantity, discount   │
           │               │ sales_amount, profit │
           │               └─┬────────────────────┘
           │                 │ *
           │                 │
           │               1 │
           │      ┌──────────┴───────────┐
           └──────┤      dim_region      │
             *   1├──────────────────────┤
                  │ region_id (PK)       │
                  │ region_name, zone    │
                  └──────────────────────┘
```

---

## 📈 Power BI Interactive Dashboards

### 1. Executive Overview Dashboard
![Executive Dashboard](screenshots/executive_dashboard.png)

### 2. Sales Velocity & Monthly Performance Dashboard
![Sales Dashboard](screenshots/sales_dashboard.png)

### 3. Customer Retention & RFM Insights Dashboard
![Customer Dashboard](screenshots/customer_dashboard.png)

### 4. Product & Category Profitability Dashboard
![Product Dashboard](screenshots/product_dashboard.png)

---

## 👥 RFM Customer Segmentation (8 Segments)

| Segment | Customers | Cust % | Total Revenue (₹) | Rev % | Avg Spend (₹) | Avg Recency | Actionable Business Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Champions** | 2,096 | 17.5% | ₹16,886,511.10 | 34.6% | ₹8,056.54 | 90 days | VIP loyalty rewards & exclusive early access |
| **At Risk** | 2,678 | 22.3% | ₹9,891,536.80 | 20.3% | ₹3,693.63 | 844 days | Automated 10-15% win-back discount triggers |
| **Loyal Customers** | 1,618 | 13.5% | ₹8,483,309.70 | 17.4% | ₹5,243.08 | 253 days | Cross-sell premium bundles & accessories |
| **Potential Loyalists**| 1,922 | 16.0% | ₹4,504,826.70 | 9.2% | ₹2,343.82 | 99 days | Gamified 2nd-order loyalty points |
| **Hibernating** | 1,959 | 16.3% | ₹4,065,646.65 | 8.3% | ₹2,075.37 | 427 days | Category revival campaigns & seasonal push |
| **Can't Lose Them** | 748 | 6.2% | ₹3,449,255.05 | 7.1% | ₹4,611.30 | 1,196 days | High-touch personal account outreach |
| **Lost Customers** | 736 | 6.1% | ₹1,232,103.80 | 2.5% | ₹1,674.05 | 1,263 days | Low-cost re-engagement email blasts |
| **New Customers** | 243 | 2.0% | ₹305,527.25 | 0.6% | ₹1,257.31 | 101 days | Welcome onboarding sequence & review coupon |

---

## 🎯 100% Multi-Tool KPI Reconciliation

| KPI Metric | PostgreSQL | Python/Pandas | Excel Workbook | Power BI DAX | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Transactions** | 66,019 | 66,019 | 66,019 | 66,019 | **PASS** |
| **Total Orders** | 20,056 | 20,056 | 20,056 | 20,056 | **PASS** |
| **Unique Customers** | 12,000 | 12,000 | 12,000 | 12,000 | **PASS** |
| **Unique Products** | 1,220 | 1,220 | 1,220 | 1,220 | **PASS** |
| **Total Categories** | 12 | 12 | 12 | 12 | **PASS** |
| **Total Regions** | 6 | 6 | 6 | 6 | **PASS** |
| **Total Revenue** | ₹48,818,717.05 | ₹48,818,717.05 | ₹48,818,717.05 | ₹48,818,717.05 | **PASS** |
| **Average Order Value (AOV)** | ₹2,434.12 | ₹2,434.12 | ₹2,434.12 | ₹2,434.12 | **PASS** |
| **Repeat Customers** | 4,248 | 4,248 | 4,248 | 4,248 | **PASS** |
| **Repeat Customer Rate** | 35.40% | 35.40% | 35.40% | 35.40% | **PASS** |
| **Total Gross Profit** | ₹18,444,504.22 | ₹18,444,504.22 | ₹18,444,504.22 | ₹18,444,504.22 | **PASS** |
| **Overall Profit Margin**| 37.78% | 37.78% | 37.78% | 37.78% | **PASS** |
| **Top Category** | Electronics | Electronics | Electronics | Electronics | **PASS** |
| **Top Region** | West (25.15%) | West (25.15%) | West (25.15%) | West (25.15%) | **PASS** |

---

## 📂 Repository File Structure

```
retail-sales-customer-insights/
├── README.md                                # GitHub-ready portfolio documentation
├── index.html                               # Live Web Analytics Portal (GitHub Pages)
├── app.py                                   # Interactive Streamlit Web BI Dashboard
├── run_project.py                           # Master automated execution pipeline
│
├── data/
│   ├── raw/                                 # 4 Raw transaction & dimension CSVs
│   ├── cleaned/                             # 5 Cleaned Star Schema CSVs + RFM table
│   ├── retail_raw_and_cleaned_master.xlsx   # Combined Master Excel (11 Sheets)
│   └── data_dictionary.xlsx                 # 40-Field Data Dictionary
│
├── sql/
│   ├── 01_create_tables.sql                 # DDL with keys, constraints & indexes
│   ├── 02_load_data.sql                     # PostgreSQL COPY ingestion script
│   ├── 03_data_validation.sql               # SQL audit queries
│   ├── 04_sales_analysis.sql                # Time-series & MoM growth
│   ├── 05_customer_analysis.sql             # Repeat customer rate & CLV
│   ├── 06_product_analysis.sql              # Category & product profit margins
│   ├── 07_rfm_analysis.sql                  # Pure SQL NTILE(5) RFM pipeline
│   └── 08_advanced_analysis.sql             # Master 27 analytical queries
│
├── python/
│   ├── 01_data_validation.py                # Nulls, duplicates & IQR outlier audit
│   ├── 02_data_cleaning.py                  # Standardization & export pipeline
│   ├── 03_sales_analysis.py                 # Monthly trends & payment share
│   ├── 04_customer_analysis.py              # Cohort retention & demographics
│   ├── 05_product_analysis.py               # Pareto 80/20 & margin rankings
│   └── 06_rfm_segmentation.py               # 8-Tier RFM scoring pipeline
│
├── excel/
│   └── retail_sales_analysis.xlsx           # 9-sheet Excel workbook with 5-Year Trajectory
│
├── powerbi/
│   ├── dax_measures.dax                     # 15+ production DAX formulas
│   └── data_model_schema.md                 # Star schema visual architecture
│
├── documentation/
│   ├── project_documentation.md             # End-to-end technical report
│   ├── kpi_reconciliation.xlsx              # 100% PASS multi-tool matrix
│   └── interview_preparation.md             # 30+ Q&As & resume bullets
│
└── screenshots/
    ├── executive_dashboard.png              # Executive Overview
    ├── sales_dashboard.png                  # Sales Performance
    ├── customer_dashboard.png               # Customer Insights
    └── product_dashboard.png                # Product & Category
```

---

## 🚀 How to Run & Reproduce

```bash
# 1. Clone the repository
git clone https://github.com/utsav2311/retail-sales-customer-insights.git
cd retail-sales-customer-insights

# 2. Run the complete data pipeline locally
python3 run_project.py

# 3. Launch the interactive Streamlit Web Dashboard
streamlit run app.py
```
