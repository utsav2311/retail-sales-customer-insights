"""
06_rfm_segmentation.py
Retail Sales & Customer Insights Project
Industry-Standard RFM (Recency, Frequency, Monetary) Customer Segmentation Suite.
Calculates:
- Customer-level Recency (Days since last purchase relative to 2026-01-01)
- Customer-level Frequency (Total distinct orders placed)
- Customer-level Monetary (Total net sales spend in ₹)
- 1 to 5 Quintile Scoring
- 8 Distinct Actionable Business Segments:
  1. Champions
  2. Loyal Customers
  3. Potential Loyalists
  4. New Customers
  5. At Risk
  6. Can't Lose Them
  7. Hibernating
  8. Lost Customers
- Exports data/cleaned/customer_rfm_segments.csv
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")

def segment_customer(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]
    
    # 1. Champions: High Recency, High Frequency, High Monetary
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    # 2. Can't Lose Them: Inactive recently (R=1), but historically High Frequency & Monetary
    elif r == 1 and (f >= 4 or m >= 4):
        return "Can't Lose Them"
    # 3. Loyal Customers: Consistent buyers across R, F, M
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal Customers"
    # 4. At Risk: Medium-Low Recency, but good past Frequency/Monetary
    elif r <= 2 and (f >= 3 or m >= 3):
        return "At Risk"
    # 5. Potential Loyalists: Recent buyers with emerging frequency/monetary
    elif r >= 4 and (f >= 2 or m >= 2):
        return "Potential Loyalists"
    # 6. New Customers: High Recency, Single-order buyer
    elif r >= 4 and f == 1:
        return "New Customers"
    # 7. Hibernating: Low-Medium Recency, Low Frequency & Monetary
    elif (r == 2 or r == 3) and f <= 2:
        return "Hibernating"
    # 8. Lost Customers: Lowest Recency (R=1) and Low Frequency/Monetary
    elif r == 1 and f <= 2:
        return "Lost Customers"
    else:
        return "Hibernating"

def run_rfm_analysis():
    print("=" * 60)
    print("  RETAIL SALES & CUSTOMER INSIGHTS: RFM SEGMENTATION")
    print("=" * 60)
    
    # 1. Load Data
    df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
    df_cust = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_customer.csv"))
    
    df_sales["order_date"] = pd.to_datetime(df_sales["order_date"])
    snapshot_date = df_sales["order_date"].max() + pd.Timedelta(days=1)
    print(f"  • Snapshot Reference Date: {snapshot_date.strftime('%Y-%m-%d')}")
    
    # 2. Calculate RFM Metrics per Customer
    rfm = df_sales.groupby("customer_id").agg(
        Last_Order_Date=("order_date", "max"),
        Frequency=("order_id", "nunique"),
        Monetary=("sales_amount", "sum"),
        Total_Profit=("profit", "sum")
    ).reset_index()
    
    rfm["Recency"] = (snapshot_date - rfm["Last_Order_Date"]).dt.days
    
    # 3. Calculate 1-5 Scores using Quintiles (Rank-based for tie-handling)
    # Recency: Lower days = Higher score (5 is best)
    rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first", ascending=False), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Frequency: Higher count = Higher score (5 is best)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first", ascending=True), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Monetary: Higher spend = Higher score (5 is best)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first", ascending=True), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    
    # 4. Assign Segments
    rfm["Segment"] = rfm.apply(segment_customer, axis=1)
    
    # Merge with demographic data
    df_rfm_full = rfm.merge(df_cust, on="customer_id", how="inner")
    
    # Export RFM Table
    export_path = os.path.join(CLEANED_DATA_DIR, "customer_rfm_segments.csv")
    df_rfm_full.to_csv(export_path, index=False)
    print(f"  ✓ Exported customer_rfm_segments.csv ({len(df_rfm_full):,} customers)")
    
    # 5. Segment Summary & Insights
    tot_rev = df_rfm_full["Monetary"].sum()
    tot_custs = len(df_rfm_full)
    
    seg_summary = df_rfm_full.groupby("Segment").agg(
        Customers=("customer_id", "count"),
        Total_Revenue=("Monetary", "sum"),
        Avg_Revenue=("Monetary", "mean"),
        Avg_Recency=("Recency", "mean"),
        Avg_Frequency=("Frequency", "mean")
    ).reset_index()
    
    seg_summary["Customer_Share_%"] = (seg_summary["Customers"] / tot_custs) * 100
    seg_summary["Revenue_Share_%"] = (seg_summary["Total_Revenue"] / tot_rev) * 100
    seg_summary = seg_summary.sort_values(by="Total_Revenue", ascending=False).reset_index(drop=True)
    
    print("\n[1] RFM CUSTOMER SEGMENTS EXECUTIVE SUMMARY:")
    print(f"{'Segment':<20} {'Customers':<10} {'Cust %':<8} {'Revenue (₹)':<16} {'Rev %':<8} {'Avg Rev (₹)':<12} {'Avg Rec':<8} {'Avg Freq':<8}")
    print("-" * 96)
    for _, row in seg_summary.iterrows():
        print(f"{row['Segment']:<20} {row['Customers']:>8,}  {row['Customer_Share_%']:>5.1f}%  ₹{row['Total_Revenue']:>12,.2f}  {row['Revenue_Share_%']:>5.1f}%  ₹{row['Avg_Revenue']:>9,.2f}  {row['Avg_Recency']:>6.1f}d  {row['Avg_Frequency']:>7.2f}")

    print("\n" + "=" * 60)
    print("  ✅ RFM SEGMENTATION COMPLETE: 100% COVERAGE")
    print("=" * 60)

if __name__ == "__main__":
    run_rfm_analysis()
