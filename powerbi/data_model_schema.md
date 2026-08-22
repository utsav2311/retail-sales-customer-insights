# Power BI Star Schema Data Model & Visual Architecture

## 1. Relational Architecture (Star Schema)

The Power BI data model is engineered following Kimball star-schema best practices. It comprises 1 central fact table (`fact_sales`) and 4 surrounding dimension tables (`dim_customer`, `dim_product`, `dim_region`, `dim_date`), plus a dedicated `_Measures` table for centralized DAX logic.

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

## 2. Table Relationships & Cardinality

| From Table (Fact) | Foreign Key | To Table (Dimension) | Primary Key | Cardinality | Cross Filter Direction | Security / Inactive |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fact_sales` | `order_date` | `dim_date` | `date` | Many to One (`*:1`) | Single (`dim_date` filters `fact_sales`) | Active |
| `fact_sales` | `customer_id` | `dim_customer` | `customer_id` | Many to One (`*:1`) | Single (`dim_customer` filters `fact_sales`) | Active |
| `fact_sales` | `product_id` | `dim_product` | `product_id` | Many to One (`*:1`) | Single (`dim_product` filters `fact_sales`) | Active |
| `fact_sales` | `region_id` | `dim_region` | `region_id` | Many to One (`*:1`) | Single (`dim_region` filters `fact_sales`) | Active |
| `dim_customer` | `region_id` | `dim_region` | `region_id` | Many to One (`*:1`) | Single (`dim_region` filters `dim_customer`) | Inactive / Secondary |

---

## 3. Power BI Report Pages & Visual Matrix

### Page 1: Executive Overview
- **Top Header**: Project Title, Corporate Slicers (Year, Quarter, Region).
- **KPI Card Row**:
  - Total Revenue (`₹45.83M` / `₹4.58 Cr`)
  - Total Gross Profit (`₹17.32M` / `₹1.73 Cr`)
  - Profit Margin (`37.78%`)
  - Total Orders (`19,021`)
  - Unique Customers (`11,500`)
  - Average Order Value (`₹2,409.34`)
  - Repeat Customer Rate (`35.19%`)
- **Visuals**:
  - *Monthly Revenue & Profit Area Chart* (24 Months 2024–2025).
  - *Category Revenue vs Margin Horizontal Bar Chart* (12 categories ranked).
  - *Regional Revenue Contribution Donut Chart* (West leading with 25.13%).

### Page 2: Sales Performance
- **Visuals**:
  - *Monthly Revenue vs Previous Month Column & Line Combo Chart* (with MoM % line).
  - *Quarterly Performance Waterfall Chart* (Q1–Q4 revenue build-up).
  - *Payment Method Share Treemap* (UPI 42.0%, Credit Card 28.0%, Debit Card 14.0%, etc.).
  - *Average Order Value by Category & Region Matrix*.

### Page 3: Customer Insights
- **Visuals**:
  - *Repeat vs One-Time Customer Revenue Donut Chart* (Repeat customers drive 58.7% of total revenue).
  - *RFM Segment Distribution Treemap* (Champions, Loyal, At Risk, Potential Loyalists, etc.).
  - *Age Group & Gender Revenue Breakdown Clustered Column Chart* (Millennials 26-35 driving 49.3%).
  - *Top 10 High-Value Customers Table* with Sparklines.

### Page 4: Product & Category Performance
- **Visuals**:
  - *Category Profit Margin vs Total Revenue Scatter Plot* (Quadrant analysis).
  - *Top 10 Products by Revenue Bar Chart* (Electronics models leading).
  - *Bottom 10 Underperforming Products Table* (Assortment optimization candidates).
  - *Subcategory Revenue & Profit Matrix Table* with Conditional Color Formatting.

---

## 4. How to Import in Power BI Desktop
1. Open Power BI Desktop.
2. Click **Get Data** -> **Text/CSV** and select the 5 files in `data/cleaned/`:
   - `fact_sales.csv`
   - `dim_customer.csv`
   - `dim_product.csv`
   - `dim_region.csv`
   - `dim_date.csv`
   - `customer_rfm_segments.csv`
3. Click **Transform Data**, verify data types, and click **Close & Apply**.
4. Go to **Model View** and ensure relationships match the Star Schema table above.
5. Create a new table `_Measures` and copy all formulas from `powerbi/dax_measures.dax`.
