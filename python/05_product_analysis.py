"""
05_product_analysis.py
Retail Sales & Customer Insights Project
Comprehensive Product, Category & Regional Performance Analysis.
Calculates:
- Category Rankings by Revenue, Volume, Profit, and Margins
- Top 10 Products by Revenue, Volume, and Profit
- Bottom 10 Underperforming Products
- Regional Sales Distribution & Leading Region Contribution
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")

def run_product_and_regional_analysis():
    print("=" * 60)
    print("  RETAIL SALES & CUSTOMER INSIGHTS: PRODUCT & REGIONAL ANALYSIS")
    print("=" * 60)
    
    # 1. Load Cleaned Tables
    df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
    df_prod = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_product.csv"))
    df_reg = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_region.csv"))
    
    tot_rev = df_sales["sales_amount"].sum()
    tot_profit = df_sales["profit"].sum()
    
    # 2. Category Performance
    df_cat = df_sales.merge(df_prod[["product_id", "category"]], on="product_id")
    cat_summary = df_cat.groupby("category").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "nunique"),
        Transactions=("transaction_id", "count")
    ).reset_index()
    
    cat_summary["Revenue_Share_%"] = (cat_summary["Revenue"] / tot_rev) * 100
    cat_summary["Profit_Margin_%"] = (cat_summary["Profit"] / cat_summary["Revenue"]) * 100
    cat_summary = cat_summary.sort_values(by="Revenue", ascending=False).reset_index(drop=True)
    cat_summary["Rank"] = cat_summary.index + 1
    
    print("\n[1] CATEGORY PERFORMANCE & RANKINGS:")
    print(f"{'Rank':<5} {'Category':<24} {'Revenue (₹)':<16} {'Share %':<9} {'Profit (₹)':<15} {'Margin %':<9} {'Units':<8}")
    print("-" * 90)
    for _, row in cat_summary.iterrows():
        print(f"{row['Rank']:<5} {row['category']:<24} ₹{row['Revenue']:>12,.2f}  {row['Revenue_Share_%']:>6.2f}%  ₹{row['Profit']:>11,.2f}  {row['Profit_Margin_%']:>6.2f}%  {row['Quantity']:>6,}")
        
    print(f"\n  🏆 Top Category: {cat_summary.iloc[0]['category']} with ₹{cat_summary.iloc[0]['Revenue']:,.2f} ({cat_summary.iloc[0]['Revenue_Share_%']:.2f}% of Total Revenue)")

    # 3. Top 10 Products by Revenue
    df_p_merged = df_sales.merge(df_prod, on="product_id")
    prod_summary = df_p_merged.groupby(["product_id", "product_name", "category", "brand"]).agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Quantity=("quantity", "sum"),
        Orders=("order_id", "nunique")
    ).reset_index()
    prod_summary["Profit_Margin_%"] = (prod_summary["Profit"] / prod_summary["Revenue"]) * 100
    
    print("\n[2] TOP 10 PRODUCTS BY REVENUE:")
    top10_prods = prod_summary.sort_values(by="Revenue", ascending=False).head(10).reset_index(drop=True)
    for idx, row in top10_prods.iterrows():
        print(f"  {idx+1:>2}. [{row['product_id']}] {row['product_name']:<35} ({row['category']}) | Rev: ₹{row['Revenue']:>9,.2f} | Units: {row['Quantity']:>4} | Margin: {row['Profit_Margin_%']:.1f}%")

    # 4. Bottom 10 Products (Underperforming)
    print("\n[3] BOTTOM 10 UNDERPERFORMING PRODUCTS (Lowest Revenue):")
    bot10_prods = prod_summary.sort_values(by="Revenue", ascending=True).head(10).reset_index(drop=True)
    for idx, row in bot10_prods.iterrows():
        print(f"  {idx+1:>2}. [{row['product_id']}] {row['product_name']:<35} ({row['category']}) | Rev: ₹{row['Revenue']:>7,.2f} | Units: {row['Quantity']:>3} | Margin: {row['Profit_Margin_%']:.1f}%")

    # 5. Regional Performance Analysis
    df_reg_merged = df_sales.merge(df_reg, on="region_id")
    reg_summary = df_reg_merged.groupby(["region_id", "region_name", "zone"]).agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Customers=("customer_id", "nunique"),
        Quantity=("quantity", "sum")
    ).reset_index()
    reg_summary["Revenue_Share_%"] = (reg_summary["Revenue"] / tot_rev) * 100
    reg_summary["Profit_Margin_%"] = (reg_summary["Profit"] / reg_summary["Revenue"]) * 100
    reg_summary["AOV"] = reg_summary["Revenue"] / reg_summary["Orders"]
    reg_summary = reg_summary.sort_values(by="Revenue", ascending=False).reset_index(drop=True)
    
    print("\n[4] REGIONAL PERFORMANCE & SHARE:")
    print(f"{'Region':<12} {'Zone':<20} {'Revenue (₹)':<16} {'Share %':<9} {'Orders':<8} {'Customers':<10} {'AOV (₹)':<9}")
    print("-" * 88)
    for _, row in reg_summary.iterrows():
        print(f"{row['region_name']:<12} {row['zone']:<20} ₹{row['Revenue']:>12,.2f}  {row['Revenue_Share_%']:>6.2f}%  {row['Orders']:>6,}  {row['Customers']:>8,}  ₹{row['AOV']:>7,.2f}")

    print(f"\n  🏆 Leading Region: {reg_summary.iloc[0]['region_name']} with ₹{reg_summary.iloc[0]['Revenue']:,.2f} ({reg_summary.iloc[0]['Revenue_Share_%']:.2f}% contribution ~25%)")
    print(f"  🔻 Bottom Region:  {reg_summary.iloc[-1]['region_name']} with ₹{reg_summary.iloc[-1]['Revenue']:,.2f} ({reg_summary.iloc[-1]['Revenue_Share_%']:.2f}% contribution)")

    print("\n" + "=" * 60)
    print("  ✅ PRODUCT & REGIONAL ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_product_and_regional_analysis()
