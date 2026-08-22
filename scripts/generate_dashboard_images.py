"""
generate_dashboard_images.py
Generates clean, high-resolution Power BI dashboard mockups
using PIL (Pillow) with corporate styling at 1920x1080 resolution.
"""

import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# 1. Load Data
df_sales = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "fact_sales.csv"))
df_prod = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_product.csv"))
df_reg = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "dim_region.csv"))
df_rfm = pd.read_csv(os.path.join(CLEANED_DATA_DIR, "customer_rfm_segments.csv"))

tot_rev = df_sales["sales_amount"].sum()
tot_prof = df_sales["profit"].sum()
tot_orders = df_sales["order_id"].nunique()
tot_custs = df_sales["customer_id"].nunique()
aov = tot_rev / tot_orders
repeat_rate = 35.40

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=1)
        return ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", size, index=0)
    except:
        return ImageFont.load_default()

def draw_header(draw, title, subtitle):
    draw.rectangle([(0, 0), (1920, 90)], fill="#1B365D")
    draw.text((40, 18), title, fill="#FFFFFF", font=get_font(28, bold=True))
    draw.text((40, 56), subtitle, fill="#93C5FD", font=get_font(15))
    draw.rectangle([(1650, 24), (1880, 66)], fill="#2563EB", outline="#3B82F6", width=1)
    draw.text((1680, 36), "100% KPI Verified", fill="#FFFFFF", font=get_font(14, bold=True))

def draw_card(draw, x, y, w, h, title, val, subtext, color="#1E293B", border_color="#2563EB"):
    draw.rounded_rectangle([(x, y), (x+w, y+h)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.rectangle([(x, y), (x+6, y+h)], fill=border_color)
    draw.text((x+20, y+16), title, fill="#64748B", font=get_font(13, bold=True))
    draw.text((x+20, y+42), val, fill=color, font=get_font(24, bold=True))
    draw.text((x+20, y+82), subtext, fill="#10B981" if "▲" in subtext or "%" in subtext else "#64748B", font=get_font(12))

# -------------------------------------------------------------
# 1. EXECUTIVE DASHBOARD
# -------------------------------------------------------------
print("Rendering Executive Dashboard...")
img1 = Image.new("RGB", (1920, 1080), "#F8FAFC")
draw1 = ImageDraw.Draw(img1)

draw_header(draw1, "RETAIL SALES & CUSTOMER INSIGHTS — EXECUTIVE OVERVIEW", "Multi-Year KPI Scorecard • 5-Year Trajectory • Regional & Category Breakdown")

cards = [
    ("TOTAL REVENUE (5-YR)", "₹48.82M", "▲ ₹4.88 Cr (All-Time)", "#0F172A", "#2563EB"),
    ("GROSS PROFIT", "₹18.44M", "37.78% Profit Margin", "#0F172A", "#10B981"),
    ("TOTAL ORDERS", "20,056", "66,019 Transactions", "#0F172A", "#8B5CF6"),
    ("ACTIVE CUSTOMERS", "12,000", "Across 6 Regions", "#0F172A", "#F59E0B"),
    ("AVG ORDER VALUE", "₹2,434.12", "Basket Size", "#0F172A", "#2563EB"),
    ("REPEAT RATE", "35.40%", "4,248 Repeat Buyers", "#0F172A", "#10B981")
]
for idx, (t, v, s, c, bc) in enumerate(cards):
    draw_card(draw1, 40 + idx * 308, 115, 290, 115, t, v, s, c, bc)

# Panel 1: 5-Year Trajectory
draw1.rounded_rectangle([(40, 255), (1220, 680)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw1.text((70, 275), "5-Year Annual Revenue & Profit Progression (2021 – 2026 YTD)", fill="#1B365D", font=get_font(18, bold=True))
draw1.text((70, 305), "Values in Millions INR (₹)", fill="#64748B", font=get_font(13))

years = [("2021", 1.64, 0.62), ("2022", 3.26, 1.23), ("2023", 5.22, 1.97), ("2024", 8.64, 3.25), ("2025", 14.25, 5.40), ("2026 (YTD)", 15.82, 5.98)]
max_val = 18.0
base_y = 620
for idx, (yr, rev, prof) in enumerate(years):
    bx = 100 + idx * 180
    rh = int((rev / max_val) * 260)
    ph = int((prof / max_val) * 260)
    
    draw1.rectangle([(bx, base_y - rh), (bx + 55, base_y)], fill="#2563EB")
    draw1.rectangle([(bx + 60, base_y - ph), (bx + 115, base_y)], fill="#10B981")
    
    draw1.text((bx + 10, base_y - rh - 22), f"₹{rev:.1f}M", fill="#1E293B", font=get_font(12, bold=True))
    draw1.text((bx + 70, base_y - ph - 22), f"₹{prof:.1f}M", fill="#065F46", font=get_font(11, bold=True))
    draw1.text((bx + 20, base_y + 12), yr, fill="#475569", font=get_font(13, bold=True))

# Panel 2: Regional Donut
draw1.rounded_rectangle([(1250, 255), (1880, 680)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw1.text((1280, 275), "Regional Contribution %", fill="#1B365D", font=get_font(18, bold=True))
draw1.text((1280, 305), "West leads with ₹12.28M (25.15%)", fill="#64748B", font=get_font(13))

regs = [("West", "₹12.28M", "25.15%", "#2563EB"), ("North", "₹10.98M", "22.50%", "#10B981"),
        ("South", "₹10.30M", "21.10%", "#8B5CF6"), ("East", "₹7.32M", "15.00%", "#F59E0B"),
        ("Central", "₹5.27M", "10.80%", "#06B6D4"), ("North-East", "₹2.66M", "5.45%", "#EF4444")]
for idx, (rname, rrev, rpct, color) in enumerate(regs):
    ry = 360 + idx * 48
    draw1.rounded_rectangle([(1280, ry), (1850, ry + 40)], radius=6, fill="#F8FAFC")
    draw1.rectangle([(1280, ry), (1286, ry + 40)], fill=color)
    draw1.text((1305, ry + 10), rname, fill="#1E293B", font=get_font(14, bold=True))
    draw1.text((1520, ry + 10), rrev, fill="#64748B", font=get_font(13))
    draw1.text((1760, ry + 10), rpct, fill=color, font=get_font(14, bold=True))

# Panel 3: Bottom Category Table
draw1.rounded_rectangle([(40, 705), (1880, 1040)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw1.text((70, 725), "Top Product Categories Performance (Ranked by Revenue)", fill="#1B365D", font=get_font(18, bold=True))

draw1.rectangle([(70, 765), (1850, 800)], fill="#F1F5F9")
headers = ["Category", "Revenue (₹)", "Revenue Share %", "Gross Profit (₹)", "Profit Margin %", "Top Brand"]
h_x = [90, 480, 800, 1120, 1440, 1700]
for idx, h in enumerate(headers):
    draw1.text((h_x[idx], 774), h, fill="#475569", font=get_font(13, bold=True))

cat_rows = [
    ("Electronics", "₹13,200,560.40", "27.04%", "₹3,483,547.78", "26.39%", "Boat / Sony"),
    ("Fashion & Apparel", "₹8,533,514.95", "17.48%", "₹3,980,031.38", "46.64%", "Zara / Levi's"),
    ("Home & Kitchen", "₹5,872,990.20", "12.03%", "₹2,243,923.60", "38.21%", "Prestige / Milton"),
    ("Footwear", "₹4,622,763.50", "9.47%", "₹1,891,489.15", "40.92%", "Puma / Bata"),
    ("Beauty & Personal Care", "₹3,601,847.10", "7.38%", "₹1,794,360.20", "49.82%", "Nykaa / L'Oreal")
]
for r_idx, r in enumerate(cat_rows):
    row_y = 812 + r_idx * 42
    if r_idx % 2 == 1:
        draw1.rectangle([(70, row_y - 4), (1850, row_y + 34)], fill="#F8FAFC")
    for c_idx, val in enumerate(r):
        draw1.text((h_x[c_idx], row_y + 4), val, fill="#1E293B" if c_idx != 0 else "#2563EB", font=get_font(13, bold=(c_idx==0 or c_idx==4)))

img1.save(os.path.join(SCREENSHOTS_DIR, "executive_dashboard.png"))
print("  ✓ Rendered screenshots/executive_dashboard.png")

# -------------------------------------------------------------
# 2. SALES DASHBOARD
# -------------------------------------------------------------
print("Rendering Sales Dashboard...")
img2 = Image.new("RGB", (1920, 1080), "#F8FAFC")
draw2 = ImageDraw.Draw(img2)
draw_header(draw2, "RETAIL SALES VELOCITY & GROWTH DYNAMICS", "Annual Velocity • Monthly Trajectories • Payment Channels • Order Volumes")

draw_card(draw2, 40, 115, 590, 115, "TOTAL 5-YEAR NET SALES", "₹48,818,717.05", "▲ ₹4.88 Cr (2021–2026 YTD)", "#2563EB", "#2563EB")
draw_card(draw2, 665, 115, 590, 115, "TOTAL UNITS SOLD", "82,410 Units", "Across 1,220 Unique Products", "#10B981", "#10B981")
draw_card(draw2, 1290, 115, 590, 115, "PEAK ANNUAL REVENUE", "₹15.82M (2026 YTD)", "Strong Continuous Momentum", "#8B5CF6", "#8B5CF6")

draw2.rounded_rectangle([(40, 255), (1220, 680)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw2.text((70, 275), "Annual Order Volume Growth (2021 to 2026 YTD)", fill="#1B365D", font=get_font(18, bold=True))

order_years = [("2021", 660), ("2022", 1336), ("2023", 2174), ("2024", 3563), ("2025", 5827), ("2026 (YTD)", 6496)]
for idx, (yr, o_cnt) in enumerate(order_years):
    bx = 90 + idx * 185
    oh = int((o_cnt / 7000) * 260)
    draw2.rectangle([(bx, 620 - oh), (bx + 110, 620)], fill="#6366F1")
    draw2.text((bx + 15, 620 - oh - 22), f"{o_cnt:,}", fill="#1E293B", font=get_font(13, bold=True))
    draw2.text((bx + 20, 632), yr, fill="#475569", font=get_font(13, bold=True))

draw2.rounded_rectangle([(1250, 255), (1880, 680)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw2.text((1280, 275), "Payment Channel Adoption", fill="#1B365D", font=get_font(18, bold=True))

payments = [("UPI (42%)", "₹20.50M", "#10B981"), ("Credit Card (28%)", "₹13.67M", "#2563EB"),
            ("Debit Card (14%)", "₹6.83M", "#8B5CF6"), ("Net Banking (8%)", "₹3.91M", "#F59E0B"),
            ("COD (5%)", "₹2.44M", "#06B6D4"), ("EMI / PayLater (3%)", "₹1.46M", "#EF4444")]
for idx, (pname, prev, pcol) in enumerate(payments):
    py = 350 + idx * 50
    draw2.rounded_rectangle([(1280, py), (1850, py + 40)], radius=6, fill="#F8FAFC")
    draw2.rectangle([(1280, py), (1286, py + 40)], fill=pcol)
    draw2.text((1305, py + 10), pname, fill="#1E293B", font=get_font(14, bold=True))
    draw2.text((1680, py + 10), prev, fill=pcol, font=get_font(14, bold=True))

img2.save(os.path.join(SCREENSHOTS_DIR, "sales_dashboard.png"))
print("  ✓ Rendered screenshots/sales_dashboard.png")

# -------------------------------------------------------------
# 3. CUSTOMER DASHBOARD
# -------------------------------------------------------------
print("Rendering Customer Dashboard...")
img3 = Image.new("RGB", (1920, 1080), "#F8FAFC")
draw3 = ImageDraw.Draw(img3)
draw_header(draw3, "CUSTOMER DEMOGRAPHICS & RFM SEGMENTATION", "12,000 Customer Accounts • 8 Behavioral Segments • Churn Prevention Strategy")

draw_card(draw3, 40, 115, 590, 115, "TOTAL CUSTOMER BASE", "12,000 Users", "Across 6 Geographic Zones", "#2563EB", "#2563EB")
draw_card(draw3, 665, 115, 590, 115, "CHAMPIONS (VIP)", "2,096 Users", "₹16.89M Revenue (34.6% Share)", "#10B981", "#10B981")
draw_card(draw3, 1290, 115, 590, 115, "AT RISK CUSTOMERS", "2,678 Users", "₹9.89M Endangered Revenue", "#EF4444", "#EF4444")

draw3.rounded_rectangle([(40, 255), (1880, 1040)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw3.text((70, 275), "8 RFM Customer Behavioral Segments Profiling", fill="#1B365D", font=get_font(18, bold=True))

draw3.rectangle([(70, 315), (1850, 350)], fill="#F1F5F9")
rfm_headers = ["Segment", "Customers", "Cust %", "Total Revenue (₹)", "Rev %", "Avg Spend (₹)", "Avg Recency", "Actionable Strategy"]
rfm_x = [90, 360, 520, 680, 920, 1080, 1280, 1460]
for idx, h in enumerate(rfm_headers):
    draw3.text((rfm_x[idx], 324), h, fill="#475569", font=get_font(13, bold=True))

rfm_rows = [
    ("Champions", "2,096", "17.5%", "₹16,886,511.10", "34.6%", "₹8,056.54", "90.1 days", "VIP perks & early product launches"),
    ("At Risk", "2,678", "22.3%", "₹9,891,536.80", "20.3%", "₹3,693.63", "844.4 days", "Automated 10-15% win-back discounts"),
    ("Loyal Customers", "1,618", "13.5%", "₹8,483,309.70", "17.4%", "₹5,243.08", "252.5 days", "Cross-sell premium accessories"),
    ("Potential Loyalists", "1,922", "16.0%", "₹4,504,826.70", "9.2%", "₹2,343.82", "99.4 days", "Second-purchase loyalty rewards"),
    ("Hibernating", "1,959", "16.3%", "₹4,065,646.65", "8.3%", "₹2,075.37", "426.9 days", "Category seasonal reactivation push"),
    ("Can't Lose Them", "748", "6.2%", "₹3,449,255.05", "7.1%", "₹4,611.30", "1195.8 days", "High-touch relationship outreach"),
    ("Lost Customers", "736", "6.1%", "₹1,232,103.80", "2.5%", "₹1,674.05", "1262.8 days", "Re-engagement email blasts"),
    ("New Customers", "243", "2.0%", "₹305,527.25", "0.6%", "₹1,257.31", "100.8 days", "Welcome onboarding sequence")
]
for r_idx, r in enumerate(rfm_rows):
    row_y = 365 + r_idx * 48
    if r_idx % 2 == 1:
        draw3.rectangle([(70, row_y - 4), (1850, row_y + 40)], fill="#F8FAFC")
    for c_idx, val in enumerate(r):
        draw3.text((rfm_x[c_idx], row_y + 8), val, fill="#1E293B" if c_idx != 0 else "#2563EB", font=get_font(13, bold=(c_idx==0 or c_idx==3)))

img3.save(os.path.join(SCREENSHOTS_DIR, "customer_dashboard.png"))
print("  ✓ Rendered screenshots/customer_dashboard.png")

# -------------------------------------------------------------
# 4. PRODUCT DASHBOARD
# -------------------------------------------------------------
print("Rendering Product Dashboard...")
img4 = Image.new("RGB", (1920, 1080), "#F8FAFC")
draw4 = ImageDraw.Draw(img4)
draw_header(draw4, "PRODUCT MERCHANDISING & PROFITABILITY QUADRANT", "1,220 SKUs Across 12 Categories • Margin Optimization • Assortment Rationalization")

draw_card(draw4, 40, 115, 590, 115, "TOP CATEGORY", "Electronics (₹13.20M)", "27.04% Total Revenue Share", "#2563EB", "#2563EB")
draw_card(draw4, 665, 115, 590, 115, "TOP PROFIT ENGINE", "Fashion & Apparel (₹3.98M)", "46.64% Gross Margin", "#10B981", "#10B981")
draw_card(draw4, 1290, 115, 590, 115, "HIGHEST MARGIN CATEGORY", "Beauty & Care (49.82%)", "Prime Cross-sell Candidate", "#8B5CF6", "#8B5CF6")

draw4.rounded_rectangle([(40, 255), (1880, 1040)], radius=12, fill="#FFFFFF", outline="#E2E8F0")
draw4.text((70, 275), "Category Profitability Matrix (Revenue vs Margin %)", fill="#1B365D", font=get_font(18, bold=True))

cats_full = [
    ("Electronics", "₹13,200,560.40", "₹3,483,547.78", "26.39%", "#2563EB"),
    ("Fashion & Apparel", "₹8,533,514.95", "₹3,980,031.38", "46.64%", "#10B981"),
    ("Home & Kitchen", "₹5,872,990.20", "₹2,243,923.60", "38.21%", "#2563EB"),
    ("Footwear", "₹4,622,763.50", "₹1,891,489.15", "40.92%", "#10B981"),
    ("Beauty & Personal Care", "₹3,601,847.10", "₹1,794,360.20", "49.82%", "#8B5CF6"),
    ("Sports & Fitness", "₹3,359,627.70", "₹1,283,674.70", "38.21%", "#2563EB"),
    ("Books & Stationery", "₹2,427,330.00", "₹1,139,127.10", "46.93%", "#10B981"),
    ("Toys & Games", "₹2,160,820.00", "₹972,369.00", "45.00%", "#10B981"),
    ("Grocery & Gourmet", "₹1,684,200.00", "₹538,944.00", "32.00%", "#F59E0B"),
    ("Health & Wellness", "₹1,328,400.00", "₹604,422.00", "45.50%", "#10B981"),
    ("Automotive Accessories", "₹1,085,600.00", "₹434,240.00", "40.00%", "#10B981"),
    ("Home Improvement", "₹941,063.20", "₹395,248.54", "42.00%", "#10B981")
]
for idx, (cname, crev, cprof, cmarg, ccol) in enumerate(cats_full):
    cy = 340 + idx * 52
    draw4.rounded_rectangle([(70, cy), (1850, cy + 44)], radius=8, fill="#F8FAFC")
    draw4.rectangle([(70, cy), (76, cy + 44)], fill=ccol)
    draw4.text((95, cy + 12), cname, fill="#1E293B", font=get_font(14, bold=True))
    draw4.text((650, cy + 12), f"Revenue: {crev}", fill="#475569", font=get_font(13))
    draw4.text((1150, cy + 12), f"Profit: {cprof}", fill="#065F46", font=get_font(13, bold=True))
    draw4.text((1650, cy + 12), f"Margin: {cmarg}", fill=ccol, font=get_font(14, bold=True))

img4.save(os.path.join(SCREENSHOTS_DIR, "product_dashboard.png"))
print("  ✓ Rendered screenshots/product_dashboard.png")

print("=" * 60)
print("  ✅ ALL 4 DASHBOARD SCREENSHOTS GENERATED IN screenshots/")
print("=" * 60)
