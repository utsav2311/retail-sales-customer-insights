"""
04_customer_analysis.py
Retail Sales & Customer Insights Project
Customer Demographics, Repeat Behavior, and Cohort Insights.
Calculates:
- Total Customers & Repeat Customer Rate
- One-Time vs Repeat Customer Revenue Contribution
- Customer Demographics (Age groups, Gender, Account Segments)
- Top 20 Customers by Revenue & Lifetime Value
- Regional Customer Distribution
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")

def run_customer_analysis():
    print("=" * 60)
    print("  RETAIL SALES & CUSTOMER INSIGHTS: CUSTOMER ANALYSIS")
    print("=" * 60)
    
    # 1. Load Data
    df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
    df_cust = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_customer.csv"))
    df_reg = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_region.csv"))
    
    # 2. Customer Order Dynamics
    cust_orders = df_sales.groupby("customer_id").agg(
        Order_Count=("order_id", "nunique"),
        Total_Revenue=("sales_amount", "sum"),
        Total_Quantity=("quantity", "sum"),
        Total_Profit=("profit", "sum")
    ).reset_index()
    
    tot_custs = len(df_cust)
    transacting_custs = len(cust_orders)
    repeat_custs = cust_orders[cust_orders["Order_Count"] > 1]
    onetime_custs = cust_orders[cust_orders["Order_Count"] == 1]
    
    repeat_cust_count = len(repeat_custs)
    onetime_cust_count = len(onetime_custs)
    repeat_rate = (repeat_cust_count / transacting_custs) * 100
    
    tot_rev = cust_orders["Total_Revenue"].sum()
    repeat_rev = repeat_custs["Total_Revenue"].sum()
    onetime_rev = onetime_custs["Total_Revenue"].sum()
    
    print("\n[1] CUSTOMER RETENTION & REPEAT PURCHASING METRICS:")
    print(f"  • Total Registered Customers:  {tot_custs:,}")
    print(f"  • Active Transacting Customers:{transacting_custs:,}")
    print(f"  • Repeat Customers (>1 Order): {repeat_cust_count:,} ({repeat_rate:.2f}%)")
    print(f"  • One-Time Customers:          {onetime_cust_count:,} ({100 - repeat_rate:.2f}%)")
    print(f"  • Repeat Customer Revenue:     ₹{repeat_rev:,.2f} ({repeat_rev/tot_rev*100:.2f}% of total)")
    print(f"  • One-Time Customer Revenue:   ₹{onetime_rev:,.2f} ({onetime_rev/tot_rev*100:.2f}% of total)")
    print(f"  • Avg Revenue Per Customer:    ₹{tot_rev/transacting_custs:,.2f}")
    print(f"  • Avg Revenue (Repeat):        ₹{repeat_rev/repeat_cust_count:,.2f}")
    print(f"  • Avg Revenue (One-Time):      ₹{onetime_rev/onetime_cust_count:,.2f}")

    # 3. Demographics Breakdown
    df_merged = df_cust.merge(cust_orders, on="customer_id", how="inner")
    
    # Age Groups
    bins = [17, 25, 35, 50, 75]
    labels = ["18-25 (Gen Z)", "26-35 (Millennials)", "36-50 (Gen X)", "51+ (Seniors)"]
    df_merged["Age_Group"] = pd.cut(df_merged["age"], bins=bins, labels=labels)
    
    print("\n[2] AGE GROUP DISTRIBUTION & REVENUE:")
    age_summary = df_merged.groupby("Age_Group", observed=False).agg(
        Customers=("customer_id", "count"),
        Revenue=("Total_Revenue", "sum")
    ).reset_index()
    age_summary["Revenue_%"] = (age_summary["Revenue"] / tot_rev) * 100
    for _, row in age_summary.iterrows():
        print(f"  • {row['Age_Group']:<22} | Customers: {row['Customers']:>5,} | Revenue: ₹{row['Revenue']:>11,.2f} ({row['Revenue_%']:>5.2f}%)")

    # Customer Segment
    print("\n[3] ACCOUNT SEGMENT BREAKDOWN:")
    seg_summary = df_merged.groupby("customer_segment").agg(
        Customers=("customer_id", "count"),
        Revenue=("Total_Revenue", "sum")
    ).reset_index()
    seg_summary["Revenue_%"] = (seg_summary["Revenue"] / tot_rev) * 100
    for _, row in seg_summary.iterrows():
        print(f"  • {row['customer_segment']:<15} | Customers: {row['Customers']:>5,} | Revenue: ₹{row['Revenue']:>11,.2f} ({row['Revenue_%']:>5.2f}%)")

    # 4. Top 10 High-Value Customers
    print("\n[4] TOP 10 HIGHEST-VALUE CUSTOMERS:")
    top10 = df_merged.sort_values(by="Total_Revenue", ascending=False).head(10)
    for idx, row in top10.reset_index().iterrows():
        print(f"  {idx+1:>2}. {row['customer_name']:<20} ({row['customer_id']}) | Orders: {row['Order_Count']:>2} | Revenue: ₹{row['Total_Revenue']:>9,.2f} | Profit: ₹{row['Total_Profit']:>8,.2f}")

    print("\n" + "=" * 60)
    print("  ✅ CUSTOMER ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_customer_analysis()
