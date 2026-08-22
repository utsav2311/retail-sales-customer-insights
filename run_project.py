"""
run_project.py
Master Local Execution Pipeline for Retail Sales & Customer Insights.
Executes the entire end-to-end workflow sequentially:
1. Data Validation
2. Data Cleaning & Star Schema Generation
3. Sales Analysis
4. Customer Analysis
5. Product & Regional Analysis
6. RFM Segmentation
7. SQL Engine Verification (All 27 Queries)
8. Excel Workbook Build (retail_sales_analysis.xlsx)
9. Power BI Dashboard Screenshot Rendering
10. Multi-Tool KPI Reconciliation (kpi_reconciliation.xlsx)
"""

import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("1. Data Validation & Quality Audit", "python/01_data_validation.py"),
    ("2. Data Cleaning & Star Schema Export", "python/02_data_cleaning.py"),
    ("3. Sales Performance & Time-Series Analysis", "python/03_sales_analysis.py"),
    ("4. Customer Cohorts & Retention Analysis", "python/04_customer_analysis.py"),
    ("5. Product & Regional Performance Analysis", "python/05_product_analysis.py"),
    ("6. RFM Customer Segmentation (8 Segments)", "python/06_rfm_segmentation.py"),
    ("7. SQL Database Engine & 27 Master Queries", "scripts/verify_sql_queries.py"),
    ("8. Excel 8-Sheet Analytics Workbook Build", "scripts/build_excel_workbook.py"),
    ("9. Power BI Dashboard Visuals Rendering", "scripts/generate_dashboard_images.py"),
    ("10. Multi-Tool KPI Reconciliation & Resume Audit", "scripts/generate_kpi_reconciliation.py")
]

def main():
    print("=" * 70)
    print("  🚀 RETAIL SALES & CUSTOMER INSIGHTS — MASTER EXECUTION PIPELINE")
    print("=" * 70)
    start_total = time.time()
    
    for step_num, (title, rel_path) in enumerate(STEPS, start=1):
        script_path = os.path.join(BASE_DIR, rel_path)
        print(f"\n[{step_num}/10] RUNNING: {title}")
        print(f"       Script: {rel_path}")
        print("-" * 70)
        
        t0 = time.time()
        result = subprocess.run([sys.executable, script_path], cwd=BASE_DIR, capture_output=True, text=True)
        t_elapsed = time.time() - t0
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"  ✓ {title} COMPLETED in {t_elapsed:.2f}s")
        else:
            print(f"  ❌ ERROR in {title} (Exit Code {result.returncode}):")
            print(result.stderr)
            print(result.stdout)
            sys.exit(1)
            
    total_time = time.time() - start_total
    print("\n" + "=" * 70)
    print(f"  🎉 ALL 10 PIPELINE MODULES EXECUTED SUCCESSFULLY IN {total_time:.2f} SECONDS!")
    print("=" * 70)
    print("\nGenerated Project Assets:")
    print("  • Cleaned Star Schema: data/cleaned/ (fact_sales, dim_customer, dim_product, dim_region, dim_date)")
    print("  • Data Dictionary:     data/data_dictionary.xlsx")
    print("  • Excel Workbook:      excel/retail_sales_analysis.xlsx (8 Sheets)")
    print("  • Power BI Measures:   powerbi/dax_measures.dax")
    print("  • Dashboard Visuals:   screenshots/ (4 PNGs)")
    print("  • Reconciliation:      documentation/kpi_reconciliation.xlsx")
    print("  • Technical Report:    documentation/project_documentation.md")
    print("  • Interview Guide:     documentation/interview_preparation.md")
    print("=" * 70)

if __name__ == "__main__":
    main()
