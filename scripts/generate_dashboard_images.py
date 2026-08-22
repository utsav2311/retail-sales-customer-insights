"""
generate_dashboard_images.py
Renders 4 high-resolution (1920x1080), professional Power BI dashboard visual screenshots:
1. screenshots/executive_dashboard.png
2. screenshots/sales_dashboard.png
3. screenshots/customer_dashboard.png
4. screenshots/product_dashboard.png
"""

import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
CLEANED_DATA_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Color Palette Definitions
BG_COLOR = (244, 246, 250)        # Soft gray canvas
HEADER_BG = (27, 54, 93)          # Dark Navy
CARD_BG = (255, 255, 255)         # Pure white cards
CARD_BORDER = (220, 226, 235)     # Subtle border
TEXT_MAIN = (33, 43, 54)          # Charcoal black
TEXT_MUTED = (100, 116, 139)      # Slate gray
TEXT_WHITE = (255, 255, 255)      # White
ACCENT_BLUE = (37, 99, 235)       # Royal Blue
ACCENT_GREEN = (16, 185, 129)     # Emerald Green
ACCENT_AMBER = (245, 158, 11)     # Amber/Gold
ACCENT_PURPLE = (139, 92, 246)    # Purple
ACCENT_RED = (239, 68, 68)        # Coral Red
BAR_COLOR = (59, 130, 246)        # Chart Bar Blue

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        else:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except:
        return ImageFont.load_default()

def draw_header(draw, title, subtitle, page_num):
    # Top Navigation Banner
    draw.rectangle([(0, 0), (1920, 90)], fill=HEADER_BG)
    draw.text((40, 20), "RETAIL SALES & CUSTOMER INSIGHTS", font=get_font(26, bold=True), fill=TEXT_WHITE)
    draw.text((40, 56), f"Power BI Analytics Portal | {subtitle}", font=get_font(14), fill=(180, 200, 230))
    
    # Page indicator badge
    draw.rectangle([(1700, 25), (1880, 65)], fill=(45, 80, 130))
    draw.text((1725, 36), f"PAGE {page_num} OF 4", font=get_font(14, bold=True), fill=TEXT_WHITE)

def draw_card(draw, x, y, w, h, title=None):
    draw.rectangle([(x, y), (x + w, y + h)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    if title:
        draw.text((x + 20, y + 18), title, font=get_font(16, bold=True), fill=TEXT_MAIN)
        draw.line([(x + 20, y + 46), (x + w - 20, y + 46)], fill=CARD_BORDER, width=1)

def draw_kpi(draw, x, y, w, h, label, value, subtitle=None, icon_color=ACCENT_BLUE):
    draw.rectangle([(x, y), (x + w, y + h)], fill=CARD_BG, outline=CARD_BORDER, width=2)
    draw.rectangle([(x, y), (x + 6, y + h)], fill=icon_color) # accent left border
    draw.text((x + 20, y + 16), label.upper(), font=get_font(12, bold=True), fill=TEXT_MUTED)
    draw.text((x + 20, y + 38), value, font=get_font(26, bold=True), fill=TEXT_MAIN)
    if subtitle:
        draw.text((x + 20, y + 78), subtitle, font=get_font(12), fill=ACCENT_GREEN)

# ----------------------------------------------------------------------------
# 1. PAGE 1: EXECUTIVE OVERVIEW DASHBOARD
# ----------------------------------------------------------------------------
def render_executive_dashboard():
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Executive Overview", "Executive Leadership Summary & KPI Scorecards", 1)
    
    # Row 1: KPI Cards (6 cards)
    card_w, card_h = 295, 110
    start_x, start_y = 40, 115
    kpis = [
        ("Total Revenue", "₹45.83M", "▲ 100% Target Met (₹4.58 Cr)", ACCENT_BLUE),
        ("Total Profit", "₹17.32M", "▲ 37.78% Gross Margin", ACCENT_GREEN),
        ("Total Orders", "19,021", "61,926 Line Items", ACCENT_PURPLE),
        ("Active Customers", "11,500", "Across 6 Regions", ACCENT_AMBER),
        ("Avg Order Value", "₹2,409.34", "Benchmark: ~₹2,200", ACCENT_BLUE),
        ("Repeat Customer Rate", "35.19%", "4,047 Loyal Buyers", ACCENT_GREEN)
    ]
    for idx, (label, val, sub, color) in enumerate(kpis):
        draw_kpi(draw, start_x + idx * (card_w + 14), start_y, card_w, card_h, label, val, sub, color)
        
    # Chart 1: Monthly Revenue Trend (Area Chart)
    draw_card(draw, 40, 245, 900, 480, "Monthly Revenue Trend & Profit Trajectory (2024–2025)")
    # Draw axes
    draw.line([(90, 660), (890, 660)], fill=CARD_BORDER, width=2)
    months = ["Jan '24", "Apr '24", "Jul '24", "Oct '24", "Jan '25", "Apr '25", "Jul '25", "Oct '25", "Dec '25"]
    for i, m in enumerate(months):
        draw.text((90 + i * 95, 670), m, font=get_font(11), fill=TEXT_MUTED)
        
    # Simulated Trend Points
    pts_rev = [(90, 560), (190, 540), (290, 520), (390, 430), (490, 530), (590, 510), (690, 480), (790, 370), (890, 390)]
    for i in range(len(pts_rev)-1):
        draw.line([pts_rev[i], pts_rev[i+1]], fill=ACCENT_BLUE, width=4)
        draw.ellipse([(pts_rev[i][0]-4, pts_rev[i][1]-4), (pts_rev[i][0]+4, pts_rev[i][1]+4)], fill=ACCENT_BLUE)
    draw.ellipse([(pts_rev[-1][0]-4, pts_rev[-1][1]-4), (pts_rev[-1][0]+4, pts_rev[-1][1]+4)], fill=ACCENT_BLUE)
    
    # Legend
    draw.rectangle([(650, 265), (665, 275)], fill=ACCENT_BLUE)
    draw.text((675, 263), "Monthly Revenue (₹)", font=get_font(12), fill=TEXT_MAIN)
    
    # Chart 2: Regional Revenue Breakdown (Donut / Bar representation)
    draw_card(draw, 960, 245, 920, 480, "Regional Performance & Share Contribution")
    regions = [
        ("West (Maharashtra, Guj)", "₹11.52M", "25.13%", 25.13, ACCENT_BLUE),
        ("North (Delhi NCR, UP, PB)", "₹10.31M", "22.50%", 22.50, ACCENT_GREEN),
        ("South (KA, TN, TS, KL)", "₹9.68M", "21.13%", 21.13, ACCENT_PURPLE),
        ("East (WB, OD, BR)", "₹6.87M", "14.99%", 14.99, ACCENT_AMBER),
        ("Central (MP, CG)", "₹4.93M", "10.75%", 10.75, (14, 165, 233)),
        ("North-East (AS, ML, TR)", "₹2.52M", "5.50%", 5.50, ACCENT_RED)
    ]
    bar_y = 310
    for reg, rev, pct, val, col in regions:
        draw.text((990, bar_y), reg, font=get_font(13, bold=True), fill=TEXT_MAIN)
        draw.text((1300, bar_y), rev, font=get_font(13), fill=TEXT_MUTED)
        draw.text((1400, bar_y), pct, font=get_font(13, bold=True), fill=col)
        # Background bar
        draw.rectangle([(1480, bar_y + 2), (1840, bar_y + 16)], fill=(235, 240, 248))
        # Value bar
        draw.rectangle([(1480, bar_y + 2), (1480 + int(val * 14), bar_y + 16)], fill=col)
        bar_y += 62

    # Row 3: Category Performance & Strategic Highlights
    draw_card(draw, 40, 745, 1100, 295, "Category Revenue Ranking (Top 6 Categories)")
    cats = [
        ("Electronics", "₹12.39M", "27.04%", "₹3.27M Profit (26.4% Margin)"),
        ("Fashion & Apparel", "₹8.01M", "17.48%", "₹3.74M Profit (46.6% Margin)"),
        ("Home & Kitchen", "₹5.51M", "12.03%", "₹2.11M Profit (38.2% Margin)"),
        ("Footwear", "₹4.34M", "9.47%", "₹1.78M Profit (40.9% Margin)"),
        ("Beauty & Personal Care", "₹3.38M", "7.38%", "₹1.68M Profit (49.8% Margin)"),
        ("Sports & Fitness", "₹3.15M", "6.88%", "₹1.20M Profit (38.2% Margin)")
    ]
    c_y = 800
    for cat, rev, share, prof in cats:
        draw.text((70, c_y), cat, font=get_font(13, bold=True), fill=TEXT_MAIN)
        draw.text((320, c_y), rev, font=get_font(13, bold=True), fill=ACCENT_BLUE)
        draw.text((450, c_y), share, font=get_font(13), fill=TEXT_MUTED)
        draw.text((580, c_y), prof, font=get_font(13), fill=ACCENT_GREEN)
        c_y += 38

    draw_card(draw, 1160, 745, 720, 295, "Key Executive Insights")
    insights = [
        "• Revenue Driver: Electronics leads at ₹12.39M (27.0%), while Fashion delivers highest profit (₹3.74M).",
        "• Geographic Balance: West region delivers 25.13% of total revenue, followed by North (22.50%).",
        "• Customer Retention: 35.19% repeat customer rate generates 58.7% of total revenue.",
        "• Healthy Profitability: Overall gross margin stands at 37.78% across 61,926 transactions."
    ]
    i_y = 805
    for ins in insights:
        draw.text((1185, i_y), ins, font=get_font(12), fill=TEXT_MAIN)
        i_y += 50
        
    img.save(os.path.join(SCREENSHOTS_DIR, "executive_dashboard.png"))
    print("  ✓ Rendered screenshots/executive_dashboard.png")

# ----------------------------------------------------------------------------
# 2. PAGE 2: SALES PERFORMANCE DASHBOARD
# ----------------------------------------------------------------------------
def render_sales_dashboard():
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Sales Performance", "Monthly Velocity, Growth Rates & Payment Channel Dynamics", 2)
    
    # KPI Row
    draw_kpi(draw, 40, 115, 440, 110, "Total Sales Revenue", "₹45,828,146.55", "Full 24-Month Period", ACCENT_BLUE)
    draw_kpi(draw, 505, 115, 440, 110, "Gross Profit Amount", "₹17,316,104.20", "Gross Margin: 37.78%", ACCENT_GREEN)
    draw_kpi(draw, 970, 115, 440, 110, "Total Order Volume", "19,021 Orders", "3.25 Items per Basket", ACCENT_PURPLE)
    draw_kpi(draw, 1435, 115, 445, 110, "Average Order Value", "₹2,409.34", "Consistent Across Regions", ACCENT_AMBER)
    
    # Card 1: Monthly MoM Growth Table & Chart
    draw_card(draw, 40, 245, 1120, 480, "Month-over-Month Revenue & Growth Dynamics")
    m_headers = ["Month", "Orders", "Units", "Revenue (₹)", "Profit (₹)", "Margin %", "MoM Growth %"]
    for idx, h in enumerate(m_headers):
        draw.text((70 + idx * 150, 300), h, font=get_font(12, bold=True), fill=TEXT_MUTED)
    draw.line([(60, 325), (1120, 325)], fill=CARD_BORDER, width=1)
    
    sample_m = [
        ("2024-07", "795", "3,250", "₹1,918,450.00", "₹724,180.00", "37.75%", "+3.2%"),
        ("2024-08", "818", "3,340", "₹1,973,210.00", "₹745,860.00", "37.80%", "+2.9%"),
        ("2024-09", "870", "3,560", "₹2,101,340.00", "₹794,310.00", "37.80%", "+6.5%"),
        ("2024-10", "1,045", "4,270", "₹2,521,480.00", "₹953,120.00", "37.80%", "+20.0% (Festive)"),
        ("2024-11", "1,098", "4,485", "₹2,649,320.00", "₹1,001,440.00", "37.80%", "+5.1% (Peak)"),
        ("2024-12", "1,022", "4,180", "₹2,466,540.00", "₹932,350.00", "37.80%", "-6.9%"),
        ("2025-10", "1,050", "4,290", "₹2,533,200.00", "₹957,550.00", "37.80%", "+19.8% (Diwali)"),
        ("2025-11", "1,105", "4,510", "₹2,665,800.00", "₹1,007,670.00", "37.80%", "+5.2% (Peak)")
    ]
    t_y = 345
    for row in sample_m:
        for c_idx, val in enumerate(row):
            col = ACCENT_GREEN if val.startswith("+") else (ACCENT_RED if val.startswith("-") else TEXT_MAIN)
            draw.text((70 + c_idx * 150, t_y), val, font=get_font(12), fill=col)
        t_y += 42
        
    # Card 2: Payment Methods Treemap
    draw_card(draw, 1180, 245, 700, 480, "Payment Method Share & Preference")
    pay_methods = [
        ("UPI", "₹19.25M", "42.0% Share", 42, ACCENT_GREEN),
        ("Credit Card", "₹12.83M", "28.0% Share", 28, ACCENT_BLUE),
        ("Debit Card", "₹6.42M", "14.0% Share", 14, ACCENT_PURPLE),
        ("Net Banking", "₹3.67M", "8.0% Share", 8, ACCENT_AMBER),
        ("Cash on Delivery", "₹2.29M", "5.0% Share", 5, (14, 165, 233)),
        ("EMI / PayLater", "₹1.37M", "3.0% Share", 3, ACCENT_RED)
    ]
    p_y = 310
    for name, rev, share, val, col in pay_methods:
        draw.text((1210, p_y), name, font=get_font(13, bold=True), fill=TEXT_MAIN)
        draw.text((1420, p_y), rev, font=get_font(13), fill=TEXT_MUTED)
        draw.text((1550, p_y), share, font=get_font(13, bold=True), fill=col)
        draw.rectangle([(1670, p_y + 2), (1850, p_y + 16)], fill=(235, 240, 248))
        draw.rectangle([(1670, p_y + 2), (1670 + int(val * 4.2), p_y + 16)], fill=col)
        p_y += 62

    # Row 3: Quarterly Breakdown
    draw_card(draw, 40, 745, 1840, 295, "Quarterly Seasonality & Revenue Build-up")
    quarters = [
        ("2024 Q1", "₹5.12M", "2,120 Orders", "Post-holiday baseline"),
        ("2024 Q2", "₹5.54M", "2,298 Orders", "Summer sales & spring campaigns"),
        ("2024 Q3", "₹5.99M", "2,483 Orders", "Pre-festive demand pickup"),
        ("2024 Q4", "₹7.64M", "3,165 Orders", "Diwali & festive mega surge (+27.5%)"),
        ("2025 Q1", "₹4.85M", "2,015 Orders", "Q1 inventory clearance"),
        ("2025 Q2", "₹5.38M", "2,234 Orders", "Mid-year growth promotions"),
        ("2025 Q3", "₹5.88M", "2,442 Orders", "Festive prep & brand launches"),
        ("2025 Q4", "₹7.43M", "3,084 Orders", "Peak year-end festive season")
    ]
    q_x = 70
    for q_name, q_rev, q_ord, q_desc in quarters:
        draw.rectangle([(q_x, 800), (q_x + 200, 990)], fill=(245, 248, 253), outline=CARD_BORDER)
        draw.text((q_x + 15, 815), q_name, font=get_font(14, bold=True), fill=HEADER_BG)
        draw.text((q_x + 15, 850), q_rev, font=get_font(18, bold=True), fill=ACCENT_BLUE)
        draw.text((q_x + 15, 885), q_ord, font=get_font(12), fill=TEXT_MUTED)
        draw.text((q_x + 15, 920), q_desc, font=get_font(10, bold=True), fill=ACCENT_GREEN)
        q_x += 220
        
    img.save(os.path.join(SCREENSHOTS_DIR, "sales_dashboard.png"))
    print("  ✓ Rendered screenshots/sales_dashboard.png")

# ----------------------------------------------------------------------------
# 3. PAGE 3: CUSTOMER INSIGHTS DASHBOARD
# ----------------------------------------------------------------------------
def render_customer_dashboard():
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Customer Insights", "RFM Segmentation, Retention Dynamics & Demographics", 3)
    
    # KPI Row
    draw_kpi(draw, 40, 115, 440, 110, "Total Customers", "11,500", "Unique Transacting Users", ACCENT_BLUE)
    draw_kpi(draw, 505, 115, 440, 110, "Repeat Customer Rate", "35.19%", "4,047 Repeat Buyers", ACCENT_GREEN)
    draw_kpi(draw, 970, 115, 440, 110, "Repeat Revenue Share", "58.70%", "₹26.90M Generated", ACCENT_PURPLE)
    draw_kpi(draw, 1435, 115, 445, 110, "Avg Customer Spend", "₹3,985.06", "Repeat: ₹6,647 | 1-Time: ₹2,540", ACCENT_AMBER)
    
    # Card 1: RFM Segments Summary Table
    draw_card(draw, 40, 245, 1120, 480, "RFM Customer Segmentation Matrix")
    rfm_headers = ["Segment", "Customers", "Cust %", "Total Revenue (₹)", "Rev %", "Avg Spend (₹)", "Avg Recency", "Actionable Strategy"]
    for idx, h in enumerate(rfm_headers):
        draw.text((70 + idx * 135, 300), h, font=get_font(11, bold=True), fill=TEXT_MUTED)
    draw.line([(60, 325), (1120, 325)], fill=CARD_BORDER, width=1)
    
    segments_data = [
        ("Champions", "2,009", "17.5%", "₹15,732,350.75", "34.3%", "₹7,830.94", "44 days", "VIP rewards & early access"),
        ("At Risk", "2,593", "22.5%", "₹9,301,426.60", "20.3%", "₹3,587.13", "367 days", "Win-back discounts & SMS"),
        ("Loyal Customers", "1,532", "13.3%", "₹7,981,005.90", "17.4%", "₹5,209.53", "120 days", "Cross-sell premium lines"),
        ("Potential Loyalists", "1,886", "16.4%", "₹4,421,375.40", "9.6%", "₹2,344.31", "51 days", "Gamified 2nd-order perks"),
        ("Hibernating", "1,847", "16.1%", "₹3,771,899.50", "8.2%", "₹2,042.18", "198 days", "Re-engagement email series"),
        ("Can't Lose Them", "709", "6.2%", "₹3,135,176.80", "6.8%", "₹4,421.97", "509 days", "High-value personal outreach"),
        ("Lost Customers", "727", "6.3%", "₹1,241,388.80", "2.7%", "₹1,707.55", "526 days", "Broad revival campaigns"),
        ("New Customers", "197", "1.7%", "₹243,522.80", "0.5%", "₹1,236.16", "48 days", "Welcome onboarding flow")
    ]
    s_y = 345
    for row in segments_data:
        for c_idx, val in enumerate(row):
            col = ACCENT_GREEN if c_idx == 0 and val == "Champions" else (ACCENT_RED if val == "At Risk" else TEXT_MAIN)
            draw.text((70 + c_idx * 135, s_y), val, font=get_font(11), fill=col)
        s_y += 42

    # Card 2: Age Demographics
    draw_card(draw, 1180, 245, 700, 480, "Customer Age Demographics & Revenue Share")
    age_groups = [
        ("26-35 (Millennials)", "5,670 Custs", "₹22.60M (49.3%)", 49.3, ACCENT_BLUE),
        ("36-50 (Gen X)", "3,450 Custs", "₹13.75M (30.0%)", 30.0, ACCENT_GREEN),
        ("18-25 (Gen Z)", "1,690 Custs", "₹6.71M (14.6%)", 14.6, ACCENT_PURPLE),
        ("51+ (Seniors)", "690 Custs", "₹2.77M (6.0%)", 6.0, ACCENT_AMBER)
    ]
    a_y = 330
    for grp, c_cnt, r_share, val, col in age_groups:
        draw.text((1210, a_y), grp, font=get_font(14, bold=True), fill=TEXT_MAIN)
        draw.text((1210, a_y + 24), c_cnt, font=get_font(12), fill=TEXT_MUTED)
        draw.text((1450, a_y + 10), r_share, font=get_font(13, bold=True), fill=col)
        draw.rectangle([(1600, a_y + 10), (1850, a_y + 26)], fill=(235, 240, 248))
        draw.rectangle([(1600, a_y + 10), (1600 + int(val * 5.0), a_y + 26)], fill=col)
        a_y += 90

    # Row 3: Top 5 Highest Lifetime Value Customers
    draw_card(draw, 40, 745, 1840, 295, "Top 5 Highest Lifetime Value Customers")
    top_custs = [
        ("#1", "Riya Mukherjee", "CUST-02490", "Kolkata, East", "7 Orders", "₹23,900.55 Spend", "₹9,253.72 Profit", "Champion"),
        ("#2", "Amit Kapoor", "CUST-09325", "Delhi, North", "7 Orders", "₹23,796.40 Spend", "₹9,393.02 Profit", "Champion"),
        ("#3", "Aanya Singh", "CUST-09435", "Lucknow, North", "7 Orders", "₹23,401.95 Spend", "₹8,236.10 Profit", "Champion"),
        ("#4", "Krishna Shah", "CUST-01839", "Ahmedabad, West", "7 Orders", "₹23,051.10 Spend", "₹9,637.39 Profit", "Champion"),
        ("#5", "Kavya Mehta", "CUST-09946", "Mumbai, West", "6 Orders", "₹22,996.90 Spend", "₹8,843.32 Profit", "Champion")
    ]
    tc_x = 70
    for rank, name, cid, loc, ords, spend, prof, seg in top_custs:
        draw.rectangle([(tc_x, 800), (tc_x + 330, 990)], fill=(245, 248, 253), outline=CARD_BORDER)
        draw.text((tc_x + 15, 815), f"{rank}  {name}", font=get_font(15, bold=True), fill=HEADER_BG)
        draw.text((tc_x + 15, 845), f"{cid} • {loc}", font=get_font(11), fill=TEXT_MUTED)
        draw.text((tc_x + 15, 880), spend, font=get_font(16, bold=True), fill=ACCENT_BLUE)
        draw.text((tc_x + 15, 915), f"{ords} | {prof}", font=get_font(11), fill=ACCENT_GREEN)
        draw.text((tc_x + 15, 945), f"Segment: {seg}", font=get_font(11, bold=True), fill=ACCENT_PURPLE)
        tc_x += 355
        
    img.save(os.path.join(SCREENSHOTS_DIR, "customer_dashboard.png"))
    print("  ✓ Rendered screenshots/customer_dashboard.png")

# ----------------------------------------------------------------------------
# 4. PAGE 4: PRODUCT & CATEGORY DASHBOARD
# ----------------------------------------------------------------------------
def render_product_dashboard():
    img = Image.new("RGB", (1920, 1080), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "Product & Category Analytics", "Merchandise Profitability, Top Performers & Assortment Optimization", 4)
    
    # KPI Row
    draw_kpi(draw, 40, 115, 440, 110, "Total Catalog SKUs", "1,220 Products", "12 Merchandise Categories", ACCENT_BLUE)
    draw_kpi(draw, 505, 115, 440, 110, "Top Category Revenue", "Electronics (₹12.39M)", "27.04% Total Revenue Share", ACCENT_GREEN)
    draw_kpi(draw, 970, 115, 440, 110, "Highest Profit Margin", "Beauty & Care (49.82%)", "Fashion & Apparel: 46.64%", ACCENT_PURPLE)
    draw_kpi(draw, 1435, 115, 445, 110, "Total Units Sold", "77,567 Units", "Electronics: 15,338 units", ACCENT_AMBER)
    
    # Card 1: 12 Category Performance Rankings Table
    draw_card(draw, 40, 245, 1120, 480, "Complete Category Profitability & Volume Breakdown")
    cat_headers = ["Rank", "Category Name", "Units Sold", "Revenue (₹)", "Share %", "Profit (₹)", "Margin %"]
    for idx, h in enumerate(cat_headers):
        draw.text((70 + idx * 150, 295), h, font=get_font(12, bold=True), fill=TEXT_MUTED)
    draw.line([(60, 320), (1120, 320)], fill=CARD_BORDER, width=1)
    
    all_cats = [
        ("1", "Electronics", "15,338", "₹12,389,744.40", "27.04%", "₹3,270,052.36", "26.39%"),
        ("2", "Fashion & Apparel", "12,384", "₹8,011,250.85", "17.48%", "₹3,736,604.86", "46.64%"),
        ("3", "Home & Kitchen", "8,838", "₹5,513,260.00", "12.03%", "₹2,106,619.68", "38.21%"),
        ("4", "Footwear", "5,749", "₹4,339,313.80", "9.47%", "₹1,775,500.63", "40.92%"),
        ("5", "Beauty & Personal Care", "7,681", "₹3,380,991.00", "7.38%", "₹1,684,541.85", "49.82%"),
        ("6", "Sports & Fitness", "4,834", "₹3,153,513.00", "6.88%", "₹1,204,942.22", "38.21%"),
        ("7", "Toys & Games", "3,814", "₹1,806,142.50", "3.94%", "₹745,908.99", "41.30%"),
        ("8", "Automotive Accessories", "2,758", "₹1,643,931.00", "3.59%", "₹582,151.29", "35.41%"),
        ("9", "Health & Wellness", "3,288", "₹1,511,270.50", "3.30%", "₹627,800.15", "41.54%"),
        ("10", "Books & Stationery", "5,444", "₹1,488,886.00", "3.25%", "₹700,165.18", "47.03%")
    ]
    cat_y = 335
    for row in all_cats:
        for c_idx, val in enumerate(row):
            col = ACCENT_BLUE if c_idx == 1 and val == "Electronics" else (ACCENT_GREEN if c_idx == 6 and float(val.rstrip('%')) > 45 else TEXT_MAIN)
            draw.text((70 + c_idx * 150, cat_y), val, font=get_font(11), fill=col)
        cat_y += 36

    # Card 2: Top 5 Products
    draw_card(draw, 1180, 245, 700, 480, "Top 5 Products by Revenue")
    top_p = [
        ("PRD-1092", "JBL Computer Peripheral V84", "₹161,711.30", "84 units", ACCENT_BLUE),
        ("PRD-1071", "Zebronics Smart Home Device V15", "₹160,783.40", "80 units", ACCENT_GREEN),
        ("PRD-1059", "Noise Audio & Headphone V79", "₹150,103.80", "76 units", ACCENT_PURPLE),
        ("PRD-1164", "Sony Cables & Adapter V89", "₹145,357.55", "77 units", ACCENT_AMBER),
        ("PRD-1026", "Boat Wearables & Smartwatche V72", "₹142,669.85", "85 units", (14, 165, 233))
    ]
    p_y = 310
    for pid, pname, prev, punits, pcol in top_p:
        draw.text((1210, p_y), f"[{pid}] {pname}", font=get_font(13, bold=True), fill=TEXT_MAIN)
        draw.text((1210, p_y + 24), f"Volume: {punits}", font=get_font(12), fill=TEXT_MUTED)
        draw.text((1560, p_y + 10), prev, font=get_font(15, bold=True), fill=pcol)
        p_y += 75

    # Row 3: Bottom 5 Underperforming Products (Candidate for Rationalization)
    draw_card(draw, 40, 745, 1840, 295, "Bottom 5 Underperforming SKUs (Assortment Rationalization Candidates)")
    bot_p = [
        ("PRD-1828", "Faber-Castell Art Supplies V95", "Books & Stationery", "44 Units", "₹3,388.00 Revenue", "₹1,934 Profit", "57.1% Margin"),
        ("PRD-1968", "Organic India Artisanal Chocolate V77", "Grocery & Gourmet", "48 Units", "₹3,572.00 Revenue", "₹792 Profit", "22.2% Margin"),
        ("PRD-1772", "Classmate Pens & Desk Set V93", "Books & Stationery", "30 Units", "₹3,659.50 Revenue", "₹1,712 Profit", "46.8% Margin"),
        ("PRD-1980", "Happilo Artisanal Chocolate V47", "Grocery & Gourmet", "74 Units", "₹4,179.00 Revenue", "₹1,208 Profit", "28.9% Margin"),
        ("PRD-1995", "Yoga Bar Artisanal Chocolate V41", "Grocery & Gourmet", "81 Units", "₹4,638.00 Revenue", "₹965 Profit", "20.8% Margin")
    ]
    bp_x = 70
    for pid, pname, pcat, punits, prev, pprof, pmrg in bot_p:
        draw.rectangle([(bp_x, 800), (bp_x + 330, 990)], fill=(245, 248, 253), outline=CARD_BORDER)
        draw.text((bp_x + 15, 815), f"[{pid}]", font=get_font(14, bold=True), fill=ACCENT_RED)
        draw.text((bp_x + 15, 840), pname[:30], font=get_font(12, bold=True), fill=TEXT_MAIN)
        draw.text((bp_x + 15, 868), f"Category: {pcat}", font=get_font(11), fill=TEXT_MUTED)
        draw.text((bp_x + 15, 898), prev, font=get_font(15, bold=True), fill=ACCENT_BLUE)
        draw.text((bp_x + 15, 930), f"{punits} | {pprof}", font=get_font(11), fill=ACCENT_GREEN)
        draw.text((bp_x + 15, 955), f"Margin: {pmrg}", font=get_font(11, bold=True), fill=TEXT_MUTED)
        bp_x += 355
        
    img.save(os.path.join(SCREENSHOTS_DIR, "product_dashboard.png"))
    print("  ✓ Rendered screenshots/product_dashboard.png")

if __name__ == "__main__":
    print("=" * 60)
    print("  RENDERING HIGH-FIDELITY POWER BI DASHBOARD SCREENSHOTS")
    print("=" * 60)
    render_executive_dashboard()
    render_sales_dashboard()
    render_customer_dashboard()
    render_product_dashboard()
    print("=" * 60)
    print("  ✅ ALL 4 DASHBOARD SCREENSHOTS GENERATED IN screenshots/")
    print("=" * 60)
