"""
02_data_cleaning.py
Retail Sales & Customer Insights Project
Data Cleaning, Schema Standardization, Star Schema Export & Master Combined Excel Generator.
Outputs:
- data/cleaned/fact_sales.csv
- data/cleaned/dim_customer.csv
- data/cleaned/dim_product.csv
- data/cleaned/dim_region.csv
- data/cleaned/dim_date.csv (2021-2026)
- data/data_dictionary.xlsx
- data/retail_raw_and_cleaned_master.xlsx (All Raw + Cleaned sheets in 1 downloadable master Excel)
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

def run_cleaning_and_export():
    print("=" * 60)
    print("  DATA CLEANING & 5-YEAR STAR SCHEMA EXPORT")
    print("=" * 60)
    
    # 1. Load Raw Data
    df_raw_txns = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_sales_transactions.csv"))
    df_raw_cust = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_customers.csv"))
    df_raw_prod = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_products.csv"))
    df_raw_reg = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_regions.csv"))
    
    # 2. Clean & Standardize Fact Sales
    df_fact_sales = df_raw_txns[[
        "transaction_id", "order_id", "order_date", "customer_id", "product_id",
        "quantity", "unit_price", "discount", "sales_amount", "cost_amount",
        "profit", "payment_method", "region_id"
    ]].copy()
    
    df_fact_sales["transaction_id"] = df_fact_sales["transaction_id"].str.strip()
    df_fact_sales["order_id"] = df_fact_sales["order_id"].str.strip()
    df_fact_sales["order_date"] = pd.to_datetime(df_fact_sales["order_date"]).dt.strftime("%Y-%m-%d")
    df_fact_sales["customer_id"] = df_fact_sales["customer_id"].str.strip()
    df_fact_sales["product_id"] = df_fact_sales["product_id"].str.strip()
    df_fact_sales["quantity"] = df_fact_sales["quantity"].astype(int)
    df_fact_sales["unit_price"] = df_fact_sales["unit_price"].astype(float).round(2)
    df_fact_sales["discount"] = df_fact_sales["discount"].astype(float).round(4)
    df_fact_sales["sales_amount"] = df_fact_sales["sales_amount"].astype(float).round(2)
    df_fact_sales["cost_amount"] = df_fact_sales["cost_amount"].astype(float).round(2)
    df_fact_sales["profit"] = df_fact_sales["profit"].astype(float).round(2)
    df_fact_sales["payment_method"] = df_fact_sales["payment_method"].str.strip()
    df_fact_sales["region_id"] = df_fact_sales["region_id"].str.strip()
    
    df_fact_sales = df_fact_sales.sort_values(by=["order_date", "order_id", "transaction_id"]).reset_index(drop=True)
    df_fact_sales.to_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"), index=False)
    print(f"  ✓ Exported fact_sales.csv ({len(df_fact_sales):,} rows)")
    
    # 3. Clean Customer Dimension
    df_dim_customer = df_raw_cust[[
        "customer_id", "customer_name", "gender", "age", "city", "region_id", "signup_date", "customer_segment"
    ]].copy()
    df_dim_customer["customer_id"] = df_dim_customer["customer_id"].str.strip()
    df_dim_customer["customer_name"] = df_dim_customer["customer_name"].str.strip()
    df_dim_customer["gender"] = df_dim_customer["gender"].str.strip()
    df_dim_customer["age"] = df_dim_customer["age"].astype(int)
    df_dim_customer["city"] = df_dim_customer["city"].str.strip()
    df_dim_customer["region_id"] = df_dim_customer["region_id"].str.strip()
    df_dim_customer["signup_date"] = pd.to_datetime(df_dim_customer["signup_date"]).dt.strftime("%Y-%m-%d")
    df_dim_customer["customer_segment"] = df_dim_customer["customer_segment"].str.strip()
    
    df_dim_customer = df_dim_customer.sort_values(by="customer_id").reset_index(drop=True)
    df_dim_customer.to_csv(os.path.join(CLEANED_DATA_DIR, "dim_customer.csv"), index=False)
    print(f"  ✓ Exported dim_customer.csv ({len(df_dim_customer):,} rows)")
    
    # 4. Clean Product Dimension
    df_dim_product = df_raw_prod[[
        "product_id", "product_name", "category", "subcategory", "brand", "unit_cost", "unit_price"
    ]].copy()
    df_dim_product["product_id"] = df_dim_product["product_id"].str.strip()
    df_dim_product["product_name"] = df_dim_product["product_name"].str.strip()
    df_dim_product["category"] = df_dim_product["category"].str.strip()
    df_dim_product["subcategory"] = df_dim_product["subcategory"].str.strip()
    df_dim_product["brand"] = df_dim_product["brand"].str.strip()
    df_dim_product["unit_cost"] = df_dim_product["unit_cost"].astype(float).round(2)
    df_dim_product["unit_price"] = df_dim_product["unit_price"].astype(float).round(2)
    
    df_dim_product = df_dim_product.sort_values(by="product_id").reset_index(drop=True)
    df_dim_product.to_csv(os.path.join(CLEANED_DATA_DIR, "dim_product.csv"), index=False)
    print(f"  ✓ Exported dim_product.csv ({len(df_dim_product):,} rows)")
    
    # 5. Clean Region Dimension
    df_dim_region = df_raw_reg[[
        "region_id", "region_name", "state", "zone"
    ]].copy()
    df_dim_region["region_id"] = df_dim_region["region_id"].str.strip()
    df_dim_region["region_name"] = df_dim_region["region_name"].str.strip()
    df_dim_region["state"] = df_dim_region["state"].str.strip()
    df_dim_region["zone"] = df_dim_region["zone"].str.strip()
    
    df_dim_region = df_dim_region.sort_values(by="region_id").reset_index(drop=True)
    df_dim_region.to_csv(os.path.join(CLEANED_DATA_DIR, "dim_region.csv"), index=False)
    print(f"  ✓ Exported dim_region.csv ({len(df_dim_region):,} rows)")
    
    # 6. Generate 5-Year Date Dimension (2021 to 2026)
    min_date = pd.to_datetime("2021-01-01")
    max_date = pd.to_datetime("2026-12-31")
    date_range = pd.date_range(start=min_date, end=max_date)
    
    date_records = []
    for dt in date_range:
        date_records.append({
            "date": dt.strftime("%Y-%m-%d"),
            "year": dt.year,
            "quarter": f"Q{dt.quarter}",
            "month": dt.strftime("%B"),
            "month_number": dt.month,
            "week": int(dt.isocalendar().week),
            "day": dt.day,
            "day_name": dt.strftime("%A")
        })
    df_dim_date = pd.DataFrame(date_records)
    df_dim_date.to_csv(os.path.join(CLEANED_DATA_DIR, "dim_date.csv"), index=False)
    print(f"  ✓ Exported dim_date.csv ({len(df_dim_date):,} rows)")
    
    # 7. Generate Data Dictionary Excel
    dict_tables = [
        {"Table": "fact_sales", "Field": "transaction_id", "Data Type": "VARCHAR(20)", "Key Type": "PK", "Description": "Unique line item identifier"},
        {"Table": "fact_sales", "Field": "order_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Checkout order session identifier"},
        {"Table": "fact_sales", "Field": "order_date", "Data Type": "DATE", "Key Type": "FK", "Description": "Date of transaction (2021 to 2026)"},
        {"Table": "fact_sales", "Field": "customer_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Purchasing customer identifier"},
        {"Table": "fact_sales", "Field": "product_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Purchased SKU identifier"},
        {"Table": "fact_sales", "Field": "quantity", "Data Type": "INTEGER", "Key Type": "None", "Description": "Units of product purchased"},
        {"Table": "fact_sales", "Field": "unit_price", "Data Type": "NUMERIC(10,2)", "Key Type": "None", "Description": "Retail catalog price in ₹"},
        {"Table": "fact_sales", "Field": "discount", "Data Type": "NUMERIC(4,2)", "Key Type": "None", "Description": "Discount rate applied (0.00 to 0.20)"},
        {"Table": "fact_sales", "Field": "sales_amount", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Net revenue: Quantity * Unit Price * (1 - Discount)"},
        {"Table": "fact_sales", "Field": "cost_amount", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Cost of goods: Quantity * Unit Cost"},
        {"Table": "fact_sales", "Field": "profit", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Gross profit: Sales Amount - Cost Amount"},
        {"Table": "fact_sales", "Field": "payment_method", "Data Type": "VARCHAR(30)", "Key Type": "None", "Description": "Payment method (UPI, Card, Net Banking, COD)"},
        {"Table": "fact_sales", "Field": "region_id", "Data Type": "VARCHAR(10)", "Key Type": "FK", "Description": "Delivery fulfillment territory"}
    ]
    df_dict = pd.DataFrame(dict_tables)
    with pd.ExcelWriter(os.path.join(DATA_DIR, "data_dictionary.xlsx"), engine="openpyxl") as writer:
        df_dict.to_excel(writer, sheet_name="Data Dictionary", index=False)
        
    # 8. Generate 5-Year Revenue Summary Table
    df_fact_sales["year"] = pd.to_datetime(df_fact_sales["order_date"]).dt.year
    df_5year_rev = df_fact_sales.groupby("year").agg(
        Total_Revenue=("sales_amount", "sum"),
        Total_Profit=("profit", "sum"),
        Total_Orders=("order_id", "nunique"),
        Total_Transactions=("transaction_id", "count"),
        Total_Units=("quantity", "sum")
    ).reset_index()
    df_5year_rev["Profit_Margin_%"] = (df_5year_rev["Total_Profit"] / df_5year_rev["Total_Revenue"]) * 100
    df_5year_rev["Average_Order_Value"] = df_5year_rev["Total_Revenue"] / df_5year_rev["Total_Orders"]
    
    # 9. Create Master Downloadable Excel Workbook: data/retail_raw_and_cleaned_master.xlsx
    master_excel_path = os.path.join(DATA_DIR, "retail_raw_and_cleaned_master.xlsx")
    print(f"  Generating Master Downloadable Excel: {master_excel_path}...")
    with pd.ExcelWriter(master_excel_path, engine="openpyxl") as writer:
        df_5year_rev.to_excel(writer, sheet_name="5_Year_Revenue_Summary", index=False)
        df_raw_txns.head(20000).to_excel(writer, sheet_name="Raw_Transactions_Sample", index=False)
        df_raw_cust.to_excel(writer, sheet_name="Raw_Customers", index=False)
        df_raw_prod.to_excel(writer, sheet_name="Raw_Products", index=False)
        df_raw_reg.to_excel(writer, sheet_name="Raw_Regions", index=False)
        df_fact_sales.head(20000).to_excel(writer, sheet_name="Cleaned_Fact_Sales_Sample", index=False)
        df_dim_customer.to_excel(writer, sheet_name="Cleaned_Dim_Customer", index=False)
        df_dim_product.to_excel(writer, sheet_name="Cleaned_Dim_Product", index=False)
        df_dim_region.to_excel(writer, sheet_name="Cleaned_Dim_Region", index=False)
        df_dim_date.head(1000).to_excel(writer, sheet_name="Cleaned_Dim_Date", index=False)
        df_dict.to_excel(writer, sheet_name="Data_Dictionary", index=False)
        
    print(f"  ✓ Exported retail_raw_and_cleaned_master.xlsx (11 Complete Sheets)")
    print("\n" + "=" * 60)
    print("  ✅ 5-YEAR DATA CLEANING & MASTER EXCEL GENERATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_cleaning_and_export()
