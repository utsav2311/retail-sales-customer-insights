"""
02_data_cleaning.py
Retail Sales & Customer Insights Project
Data Cleaning, Schema Standardization, Star Schema Export & Data Dictionary Generator.
Outputs:
- data/cleaned/fact_sales.csv
- data/cleaned/dim_customer.csv
- data/cleaned/dim_product.csv
- data/cleaned/dim_region.csv
- data/cleaned/dim_date.csv
- data/data_dictionary.xlsx
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

def run_cleaning_and_export():
    print("=" * 60)
    print("  RETAIL SALES & CUSTOMER INSIGHTS: DATA CLEANING & MODELING")
    print("=" * 60)
    
    # 1. Load Raw Data
    df_raw_txns = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_sales_transactions.csv"))
    df_raw_cust = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_customers.csv"))
    df_raw_prod = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_products.csv"))
    df_raw_reg = pd.read_csv(os.path.join(RAW_DATA_DIR, "raw_regions.csv"))
    
    # 2. Clean & Standardize Transactions (Fact Table)
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
    
    # Sort logically
    df_fact_sales = df_fact_sales.sort_values(by=["order_date", "order_id", "transaction_id"]).reset_index(drop=True)
    df_fact_sales.to_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"), index=False)
    print(f"  ✓ Exported fact_sales.csv ({len(df_fact_sales):,} rows)")
    
    # 3. Clean & Standardize Customer Dimension
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
    
    # 4. Clean & Standardize Product Dimension
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
    
    # 5. Clean & Standardize Region Dimension
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
    
    # 6. Generate Date Dimension
    min_date = pd.to_datetime("2024-01-01")
    max_date = pd.to_datetime("2025-12-31")
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
    
    # 7. Generate Comprehensive Data Dictionary (Excel)
    dict_tables = [
        {"Table": "fact_sales", "Field": "transaction_id", "Data Type": "VARCHAR(20)", "Key Type": "PK", "Description": "Unique identifier for each transaction line item in an order"},
        {"Table": "fact_sales", "Field": "order_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Identifier linking items purchased in the same customer checkout session"},
        {"Table": "fact_sales", "Field": "order_date", "Data Type": "DATE", "Key Type": "FK", "Description": "Date when the order transaction was completed (YYYY-MM-DD)"},
        {"Table": "fact_sales", "Field": "customer_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Unique identifier of the customer who placed the order"},
        {"Table": "fact_sales", "Field": "product_id", "Data Type": "VARCHAR(20)", "Key Type": "FK", "Description": "Unique identifier of the product item purchased"},
        {"Table": "fact_sales", "Field": "quantity", "Data Type": "INTEGER", "Key Type": "None", "Description": "Units of the product purchased in the transaction line item"},
        {"Table": "fact_sales", "Field": "unit_price", "Data Type": "NUMERIC(10,2)", "Key Type": "None", "Description": "Standard catalog retail selling price per single unit in INR (₹)"},
        {"Table": "fact_sales", "Field": "discount", "Data Type": "NUMERIC(4,2)", "Key Type": "None", "Description": "Discount rate applied to the line item (0.00 to 0.25)"},
        {"Table": "fact_sales", "Field": "sales_amount", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Net revenue: Quantity * Unit Price * (1 - Discount)"},
        {"Table": "fact_sales", "Field": "cost_amount", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Cost of Goods Sold: Quantity * Unit Cost"},
        {"Table": "fact_sales", "Field": "profit", "Data Type": "NUMERIC(12,2)", "Key Type": "None", "Description": "Gross profit generated: Sales Amount - Cost Amount"},
        {"Table": "fact_sales", "Field": "payment_method", "Data Type": "VARCHAR(30)", "Key Type": "None", "Description": "Payment method used (UPI, Credit Card, Debit Card, Net Banking, COD, EMI)"},
        {"Table": "fact_sales", "Field": "region_id", "Data Type": "VARCHAR(10)", "Key Type": "FK", "Description": "Geographic delivery fulfillment region identifier"},
        
        {"Table": "dim_customer", "Field": "customer_id", "Data Type": "VARCHAR(20)", "Key Type": "PK", "Description": "Unique customer primary key"},
        {"Table": "dim_customer", "Field": "customer_name", "Data Type": "VARCHAR(100)", "Key Type": "None", "Description": "Full name of the registered customer"},
        {"Table": "dim_customer", "Field": "gender", "Data Type": "VARCHAR(10)", "Key Type": "None", "Description": "Customer gender (Male, Female, Other)"},
        {"Table": "dim_customer", "Field": "age", "Data Type": "INTEGER", "Key Type": "None", "Description": "Customer age in years (18 to 72)"},
        {"Table": "dim_customer", "Field": "city", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Customer registered residence city"},
        {"Table": "dim_customer", "Field": "region_id", "Data Type": "VARCHAR(10)", "Key Type": "FK", "Description": "Regional zone identifier for the customer residence"},
        {"Table": "dim_customer", "Field": "signup_date", "Data Type": "DATE", "Key Type": "None", "Description": "Account registration date (YYYY-MM-DD)"},
        {"Table": "dim_customer", "Field": "customer_segment", "Data Type": "VARCHAR(30)", "Key Type": "None", "Description": "Account classification (Consumer, Corporate, Small Business)"},

        {"Table": "dim_product", "Field": "product_id", "Data Type": "VARCHAR(20)", "Key Type": "PK", "Description": "Unique product primary key"},
        {"Table": "dim_product", "Field": "product_name", "Data Type": "VARCHAR(150)", "Key Type": "None", "Description": "Descriptive brand and model name of the product"},
        {"Table": "dim_product", "Field": "category", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Top-level retail merchandise category (12 categories)"},
        {"Table": "dim_product", "Field": "subcategory", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Granular product subcategory (45+ subcategories)"},
        {"Table": "dim_product", "Field": "brand", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Brand / Manufacturer name"},
        {"Table": "dim_product", "Field": "unit_cost", "Data Type": "NUMERIC(10,2)", "Key Type": "None", "Description": "Unit wholesale manufacturing/acquisition cost in INR (₹)"},
        {"Table": "dim_product", "Field": "unit_price", "Data Type": "NUMERIC(10,2)", "Key Type": "None", "Description": "Unit retail catalog price in INR (₹)"},

        {"Table": "dim_region", "Field": "region_id", "Data Type": "VARCHAR(10)", "Key Type": "PK", "Description": "Unique geographic region primary key"},
        {"Table": "dim_region", "Field": "region_name", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Commercial sales operational territory (West, North, South, East, Central, North-East)"},
        {"Table": "dim_region", "Field": "state", "Data Type": "VARCHAR(100)", "Key Type": "None", "Description": "States covered under the sales region"},
        {"Table": "dim_region", "Field": "zone", "Data Type": "VARCHAR(50)", "Key Type": "None", "Description": "Macro geopolitical zone in India"},

        {"Table": "dim_date", "Field": "date", "Data Type": "DATE", "Key Type": "PK", "Description": "Calendar calendar date (YYYY-MM-DD)"},
        {"Table": "dim_date", "Field": "year", "Data Type": "INTEGER", "Key Type": "None", "Description": "Calendar year (2024, 2025)"},
        {"Table": "dim_date", "Field": "quarter", "Data Type": "VARCHAR(5)", "Key Type": "None", "Description": "Financial calendar quarter (Q1, Q2, Q3, Q4)"},
        {"Table": "dim_date", "Field": "month", "Data Type": "VARCHAR(20)", "Key Type": "None", "Description": "Full month name (January to December)"},
        {"Table": "dim_date", "Field": "month_number", "Data Type": "INTEGER", "Key Type": "None", "Description": "Month sequence index (1 to 12)"},
        {"Table": "dim_date", "Field": "week", "Data Type": "INTEGER", "Key Type": "None", "Description": "ISO calendar week of the year (1 to 53)"},
        {"Table": "dim_date", "Field": "day", "Data Type": "INTEGER", "Key Type": "None", "Description": "Day of the month (1 to 31)"},
        {"Table": "dim_date", "Field": "day_name", "Data Type": "VARCHAR(15)", "Key Type": "None", "Description": "Name of the day of the week (Monday to Sunday)"}
    ]
    
    df_dict = pd.DataFrame(dict_tables)
    
    with pd.ExcelWriter(os.path.join(DATA_DIR, "data_dictionary.xlsx"), engine="openpyxl") as writer:
        df_dict.to_excel(writer, sheet_name="Data Dictionary", index=False)
        
    print(f"  ✓ Exported data_dictionary.xlsx ({len(df_dict)} field definitions)")
    print("\n" + "=" * 60)
    print("  ✅ DATA CLEANING & STAR SCHEMA CREATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_cleaning_and_export()
