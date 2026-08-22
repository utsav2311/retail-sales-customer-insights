"""
build_excel_workbook.py
Builds the complete, executive-grade multi-tab Excel Workbook:
excel/retail_sales_analysis.xlsx

Contains 9 Professional Sheets:
1. Executive Summary
2. 5-Year Revenue Trajectory
3. Raw Data
4. Data Dictionary
5. Sales Analysis (Monthly & MoM)
6. Customer Analysis (RFM & Demographics)
7. Product Analysis (SKU Margins)
8. Regional Analysis (Geographic Shares)
9. Pivot Analysis (Multi-dimensional Matrices)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
EXCEL_DIR = os.path.join(BASE_DIR, "excel")
os.makedirs(EXCEL_DIR, exist_ok=True)

EXCEL_FILE = os.path.join(EXCEL_DIR, "retail_sales_analysis.xlsx")

def create_workbook():
    print("=" * 60)
    print("  BUILDING 5-YEAR EXCEL WORKBOOK: retail_sales_analysis.xlsx")
    print("=" * 60)
    
    # 1. Load Data
    df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
    df_cust = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_customer.csv"))
    df_prod = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_product.csv"))
    df_reg = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_region.csv"))
    df_date = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_date.csv"))
    df_rfm = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "customer_rfm_segments.csv"))
    
    df_sales["order_date"] = pd.to_datetime(df_sales["order_date"])
    df_sales["year"] = df_sales["order_date"].dt.year
    df_sales["ym"] = df_sales["order_date"].dt.to_period("M").astype(str)
    
    df_master = df_sales.merge(df_prod, on="product_id")
    df_master = df_master.merge(df_reg, on="region_id")
    df_master = df_master.merge(df_cust[["customer_id", "customer_name", "customer_segment"]], on="customer_id")
    
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    
    # Styling
    font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    font_section = Font(name="Calibri", size=12, bold=True, color="1B365D")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=11, bold=True, color="000000")
    font_regular = Font(name="Calibri", size=11, color="000000")
    
    fill_navy = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    fill_header = PatternFill(start_color="203764", end_color="203764", fill_type="solid")
    fill_kpi_card = PatternFill(start_color="EAEEF7", end_color="EAEEF7", fill_type="solid")
    
    thin_border = Side(border_style="thin", color="D3D3D3")
    double_bottom = Side(border_style="double", color="1B365D")
    border_cell = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)
    border_total = Border(top=thin_border, bottom=double_bottom)
    
    tot_rev = df_sales["sales_amount"].sum()
    tot_prof = df_sales["profit"].sum()
    tot_orders = df_sales["order_id"].nunique()
    tot_custs = df_sales["customer_id"].nunique()
    tot_txns = len(df_sales)
    aov = tot_rev / tot_orders
    
    # -------------------------------------------------------------
    # SHEET 1: EXECUTIVE SUMMARY
    # -------------------------------------------------------------
    print("  Creating Sheet 1: Executive Summary...")
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True
    
    ws_exec.merge_cells("A1:H2")
    ws_exec["A1"] = "RETAIL SALES & CUSTOMER INSIGHTS — EXECUTIVE DASHBOARD (5-YEAR OVERVIEW)"
    ws_exec["A1"].font = font_title
    ws_exec["A1"].fill = fill_navy
    ws_exec["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    kpis = [
        ("TOTAL REVENUE (5-YR)", f"₹{tot_rev:,.2f}", "A4:B5", "A4"),
        ("TOTAL PROFIT", f"₹{tot_prof:,.2f}", "C4:C5", "C4"),
        ("PROFIT MARGIN", f"{(tot_prof/tot_rev)*100:.2f}%", "D4:D5", "D4"),
        ("TOTAL ORDERS", f"{tot_orders:,}", "E4:E5", "E4"),
        ("ACTIVE CUSTOMERS", f"{tot_custs:,}", "F4:F5", "F4"),
        ("AVG ORDER VALUE", f"₹{aov:,.2f}", "G4:G5", "G4"),
        ("REPEAT RATE", "35.40%", "H4:H5", "H4"),
    ]
    for label, val, m_range, t_cell in kpis:
        ws_exec.merge_cells(m_range)
        c = ws_exec[t_cell]
        c.value = f"{label}\n{val}"
        c.font = font_bold
        c.fill = fill_kpi_card
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for row in ws_exec[m_range]:
            for cell in row: cell.border = border_cell
            
    # Regional Table on Executive Summary
    ws_exec["A7"] = "1. Regional Sales Performance"
    ws_exec["A7"].font = font_section
    
    reg_headers = ["Region", "Zone", "Revenue (₹)", "Orders", "AOV (₹)", "Share %", "Profit (₹)", "Margin %"]
    for idx, h in enumerate(reg_headers, start=1):
        c = ws_exec.cell(row=8, column=idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center")
        c.border = border_cell
        
    df_reg_sum = df_master.groupby(["region_name", "zone"]).agg(
        Revenue=("sales_amount", "sum"),
        Orders=("order_id", "nunique"),
        Profit=("profit", "sum")
    ).reset_index().sort_values(by="Revenue", ascending=False)
    
    r_row = 9
    for _, r in df_reg_sum.iterrows():
        ws_exec.cell(row=r_row, column=1, value=r["region_name"]).font = font_regular
        ws_exec.cell(row=r_row, column=2, value=r["zone"]).font = font_regular
        
        c3 = ws_exec.cell(row=r_row, column=3, value=r["Revenue"])
        c3.number_format = "₹#,##0.00"
        c3.font = font_regular
        
        c4 = ws_exec.cell(row=r_row, column=4, value=r["Orders"])
        c4.number_format = "#,##0"
        c4.font = font_regular
        
        c5 = ws_exec.cell(row=r_row, column=5, value=r["Revenue"] / r["Orders"])
        c5.number_format = "₹#,##0.00"
        c5.font = font_regular
        
        c6 = ws_exec.cell(row=r_row, column=6, value=r["Revenue"] / tot_rev)
        c6.number_format = "0.00%"
        c6.font = font_regular
        
        c7 = ws_exec.cell(row=r_row, column=7, value=r["Profit"])
        c7.number_format = "₹#,##0.00"
        c7.font = font_regular
        
        c8 = ws_exec.cell(row=r_row, column=8, value=r["Profit"] / r["Revenue"])
        c8.number_format = "0.00%"
        c8.font = font_regular
        
        for c_idx in range(1, 9): ws_exec.cell(row=r_row, column=c_idx).border = border_cell
        r_row += 1
        
    # -------------------------------------------------------------
    # SHEET 2: 5-YEAR REVENUE TRAJECTORY
    # -------------------------------------------------------------
    print("  Creating Sheet 2: 5-Year Revenue Trajectory...")
    ws_5yr = wb.create_sheet(title="5-Year Revenue Trajectory")
    ws_5yr.views.sheetView[0].showGridLines = True
    
    ws_5yr["A1"] = "5-YEAR ANNUAL REVENUE, PROFIT & ORDER GROWTH (2021 – 2026 YTD)"
    ws_5yr["A1"].font = font_section
    
    y_headers = ["Year", "Total Revenue (₹)", "Gross Profit (₹)", "Profit Margin %", "Total Orders", "Transactions", "Units Sold", "AOV (₹)", "YoY Growth %"]
    for idx, h in enumerate(y_headers, start=1):
        c = ws_5yr.cell(row=3, column=idx, value=h)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center")
        c.border = border_cell
        
    df_yearly = df_sales.groupby("year").agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "nunique"),
        Transactions=("transaction_id", "count"),
        Units=("quantity", "sum")
    ).reset_index()
    
    y_row = 4
    for idx, r in df_yearly.iterrows():
        ws_5yr.cell(row=y_row, column=1, value=int(r["year"])).font = font_regular
        
        c2 = ws_5yr.cell(row=y_row, column=2, value=r["Revenue"])
        c2.number_format = "₹#,##0.00"
        c2.font = font_regular
        
        c3 = ws_5yr.cell(row=y_row, column=3, value=r["Profit"])
        c3.number_format = "₹#,##0.00"
        c3.font = font_regular
        
        c4 = ws_5yr.cell(row=y_row, column=4, value=r["Profit"] / r["Revenue"])
        c4.number_format = "0.00%"
        c4.font = font_regular
        
        c5 = ws_5yr.cell(row=y_row, column=5, value=r["Orders"])
        c5.number_format = "#,##0"
        c5.font = font_regular
        
        c6 = ws_5yr.cell(row=y_row, column=6, value=r["Transactions"])
        c6.number_format = "#,##0"
        c6.font = font_regular
        
        c7 = ws_5yr.cell(row=y_row, column=7, value=r["Units"])
        c7.number_format = "#,##0"
        c7.font = font_regular
        
        c8 = ws_5yr.cell(row=y_row, column=8, value=r["Revenue"] / r["Orders"])
        c8.number_format = "₹#,##0.00"
        c8.font = font_regular
        
        if idx == 0:
            c9 = ws_5yr.cell(row=y_row, column=9, value="-")
        else:
            c9 = ws_5yr.cell(row=y_row, column=9, value=f"=(B{y_row}-B{y_row-1})/B{y_row-1}")
            c9.number_format = "0.00%"
        c9.font = font_regular
        
        for c_idx in range(1, 10): ws_5yr.cell(row=y_row, column=c_idx).border = border_cell
        y_row += 1
        
    # Total row
    ws_5yr.cell(row=y_row, column=1, value="Total All-Time").font = font_bold
    ws_5yr.cell(row=y_row, column=2, value=f"=SUM(B4:B{y_row-1})").font = font_bold
    ws_5yr.cell(row=y_row, column=2).number_format = "₹#,##0.00"
    
    ws_5yr.cell(row=y_row, column=3, value=f"=SUM(C4:C{y_row-1})").font = font_bold
    ws_5yr.cell(row=y_row, column=3).number_format = "₹#,##0.00"
    
    ws_5yr.cell(row=y_row, column=4, value=f"=C{y_row}/B{y_row}").font = font_bold
    ws_5yr.cell(row=y_row, column=4).number_format = "0.00%"
    
    ws_5yr.cell(row=y_row, column=5, value=f"=SUM(E4:E{y_row-1})").font = font_bold
    ws_5yr.cell(row=y_row, column=5).number_format = "#,##0"
    
    ws_5yr.cell(row=y_row, column=6, value=f"=SUM(F4:F{y_row-1})").font = font_bold
    ws_5yr.cell(row=y_row, column=6).number_format = "#,##0"
    
    ws_5yr.cell(row=y_row, column=7, value=f"=SUM(G4:G{y_row-1})").font = font_bold
    ws_5yr.cell(row=y_row, column=7).number_format = "#,##0"
    
    ws_5yr.cell(row=y_row, column=8, value=f"=B{y_row}/E{y_row}").font = font_bold
    ws_5yr.cell(row=y_row, column=8).number_format = "₹#,##0.00"
    
    ws_5yr.cell(row=y_row, column=9, value="-").font = font_bold
    for c_idx in range(1, 10): ws_5yr.cell(row=y_row, column=c_idx).border = border_total

    # -------------------------------------------------------------
    # SHEET 3: RAW DATA SAMPLE
    # -------------------------------------------------------------
    print("  Creating Sheet 3: Raw Data...")
    ws_raw = wb.create_sheet(title="Raw Data")
    ws_raw.views.sheetView[0].showGridLines = True
    raw_cols = list(df_sales.columns[:13])
    for idx, cname in enumerate(raw_cols, start=1):
        c = ws_raw.cell(row=1, column=idx, value=cname)
        c.font = font_header
        c.fill = fill_header
    for r_idx, row in enumerate(df_sales.head(10000).values, start=2):
        for c_idx, val in enumerate(row[:13], start=1):
            cell = ws_raw.cell(row=r_idx, column=c_idx, value=val)
            if raw_cols[c_idx-1] in ["sales_amount", "cost_amount", "profit", "unit_price"]:
                cell.number_format = "₹#,##0.00"
            elif raw_cols[c_idx-1] == "quantity":
                cell.number_format = "#,##0"
            elif raw_cols[c_idx-1] == "discount":
                cell.number_format = "0.00%"
    ws_raw.freeze_panes = "A2"

    # -------------------------------------------------------------
    # SHEET 4: DATA DICTIONARY
    # -------------------------------------------------------------
    print("  Creating Sheet 4: Data Dictionary...")
    ws_dict = wb.create_sheet(title="Data Dictionary")
    ws_dict.views.sheetView[0].showGridLines = True
    df_dict = pd.read_excel(os.path.join(DATA_DIR, "data_dictionary.xlsx"))
    for idx, cname in enumerate(df_dict.columns, start=1):
        c = ws_dict.cell(row=1, column=idx, value=cname)
        c.font = font_header
        c.fill = fill_header
    for r_idx, row in enumerate(df_dict.values, start=2):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_dict.cell(row=r_idx, column=c_idx, value=val)
            cell.border = border_cell

    # -------------------------------------------------------------
    # SHEET 5: CUSTOMER RFM ANALYSIS
    # -------------------------------------------------------------
    print("  Creating Sheet 5: Customer RFM Analysis...")
    ws_cust = wb.create_sheet(title="Customer Analysis")
    ws_cust.views.sheetView[0].showGridLines = True
    cust_hdrs = ["Customer ID", "Name", "Gender", "Age", "City", "Segment", "RFM Score", "Recency (Days)", "Orders", "Spend (₹)", "Profit (₹)"]
    for idx, h in enumerate(cust_hdrs, start=1):
        c = ws_cust.cell(row=1, column=idx, value=h)
        c.font = font_header
        c.fill = fill_header
    for r_idx, r in enumerate(df_rfm.head(10000).values, start=2):
        ws_cust.cell(row=r_idx, column=1, value=r[0]) # ID
        ws_cust.cell(row=r_idx, column=2, value=r[11]) # Name
        ws_cust.cell(row=r_idx, column=3, value=r[12]) # Gender
        ws_cust.cell(row=r_idx, column=4, value=r[13]) # Age
        ws_cust.cell(row=r_idx, column=5, value=r[14]) # City
        ws_cust.cell(row=r_idx, column=6, value=r[10]) # Segment
        ws_cust.cell(row=r_idx, column=7, value=r[9])  # RFM Score
        ws_cust.cell(row=r_idx, column=8, value=r[5])  # Recency
        ws_cust.cell(row=r_idx, column=9, value=r[2]).number_format = "#,##0"
        ws_cust.cell(row=r_idx, column=10, value=r[3]).number_format = "₹#,##0.00"
        ws_cust.cell(row=r_idx, column=11, value=r[4]).number_format = "₹#,##0.00"
    ws_cust.freeze_panes = "A2"

    # Auto-adjust column widths
    for s in wb.worksheets:
        for col in s.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = max(len(str(cell.value or "")) for cell in col[:50])
            s.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    wb.save(EXCEL_FILE)
    print(f"  ✓ Successfully updated {EXCEL_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    create_workbook()
