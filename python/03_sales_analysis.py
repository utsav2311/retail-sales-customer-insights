"""
03_sales_analysis.py
Retail Sales & Customer Insights Project
Comprehensive Sales Performance & Time-Series Trend Analysis.
Calculates:
- Total Sales, Orders, Quantity, Profit, and Overall Margin
- Monthly Revenue & Orders Time-Series
- Month-over-Month (MoM) Revenue Growth %
- Yearly Revenue Comparison (2024 vs 2025)
- Average Order Value (AOV) Trends
- Payment Method Distribution & Preference Analysis
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")

def run_sales_analysis():
    print("=" * 60)
    print("  RETAIL SALES & CUSTOMER INSIGHTS: SALES ANALYSIS")
    print("=" * 60)
    
    # 1. Load Data
    df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
    df_sales["order_date"] = pd.to_datetime(df_sales["order_date"])
    df_sales["year"] = df_sales["order_date"].dt.year
    df_sales["year_month"] = df_sales["order_date"].dt.to_period("M").astype(str)
    
    # 2. High-Level Summary
    tot_revenue = df_sales["sales_amount"].sum()
    tot_orders = df_sales["order_id"].nunique()
    tot_txns = len(df_sales)
    tot_qty = df_sales["quantity"].sum()
    tot_profit = df_sales["profit"].sum()
    profit_margin = (tot_profit / tot_revenue) * 100
    aov = tot_revenue / tot_orders
    
    print("\n[1] EXECUTIVE SALES SCORECARD:")
    print(f"  • Total Revenue:       ₹{tot_revenue:,.2f} (₹{tot_revenue/10000000:.2f} Cr)")
    print(f"  • Total Profit:        ₹{tot_profit:,.2f}")
    print(f"  • Overall Margin:      {profit_margin:.2f}%")
    print(f"  • Total Orders:        {tot_orders:,}")
    print(f"  • Total Transactions:  {tot_txns:,}")
    print(f"  • Total Units Sold:    {tot_qty:,}")
    print(f"  • Average Order Value: ₹{aov:,.2f}")
    
    # 3. Yearly Performance
    print("\n[2] YEAR-OVER-YEAR PERFORMANCE:")
    yearly = df_sales.groupby("year").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Quantity=("quantity", "sum")
    ).reset_index()
    yearly["Margin_%"] = (yearly["Profit"] / yearly["Revenue"]) * 100
    yearly["AOV"] = yearly["Revenue"] / yearly["Orders"]
    for _, row in yearly.iterrows():
        print(f"  • Year {int(row['year'])}: Revenue = ₹{row['Revenue']:,.2f} | Orders = {int(row['Orders']):,} | AOV = ₹{row['AOV']:,.2f} | Margin = {row['Margin_%']:.2f}%")
        
    # 4. Monthly Revenue & MoM Growth
    print("\n[3] MONTHLY REVENUE & MoM GROWTH TRENDS (Sample 6 months):")
    monthly = df_sales.groupby("year_month").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Units=("quantity", "sum")
    ).reset_index()
    monthly["MoM_Growth_%"] = monthly["Revenue"].pct_change() * 100
    monthly["AOV"] = monthly["Revenue"] / monthly["Orders"]
    print(monthly.tail(6).to_string(index=False))
    
    # 5. Payment Method Analysis
    print("\n[4] PAYMENT METHOD BREAKDOWN:")
    pay = df_sales.groupby("payment_method").agg(
        Transactions=("transaction_id", "count"),
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum")
    ).reset_index()
    pay["Revenue_Share_%"] = (pay["Revenue"] / tot_revenue) * 100
    pay = pay.sort_values(by="Revenue", ascending=False)
    for _, row in pay.iterrows():
        print(f"  • {row['payment_method']:<18} | Txns: {row['Transactions']:>6,} | Revenue: ₹{row['Revenue']:>11,.2f} ({row['Revenue_Share_%']:>5.2f}%)")

    print("\n" + "=" * 60)
    print("  ✅ SALES ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_sales_analysis()
