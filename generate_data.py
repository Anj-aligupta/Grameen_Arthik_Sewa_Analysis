"""
generate_data.py
================
Simulates 6 data sources: ERP, CRM, Marketing, Finance, HR, Support.
Run once to create all CSV files in the /data folder.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Date range: last 12 months, daily
START = datetime(2023, 3, 1)
END   = datetime(2024, 2, 29)
dates = pd.date_range(START, END, freq="D")
months = pd.date_range(START, END, freq="MS")

REGIONS   = ["North", "South", "East", "West"]
PRODUCTS  = ["Nexora Pro", "Nexora Lite", "Nexora Enterprise", "Nexora API"]
PRICES    = {"Nexora Pro": 299, "Nexora Lite": 99, "Nexora Enterprise": 999, "Nexora API": 499}
REPS      = ["Alice Chen", "Bob Kumar", "Carol Zhang", "David Patel",
             "Emma Singh", "Frank Liu", "Grace Kim", "Henry Mehta"]
CHANNELS  = ["Organic", "Paid Search", "Social", "Email", "Referral", "Direct"]
SEGMENTS  = ["SMB", "Mid-Market", "Enterprise"]

# ── 1. ERP — Daily Sales Orders ──────────────────────────────────────────────
print("Generating ERP data...")
erp_rows = []
for d in dates:
    n = random.randint(8, 25)
    for _ in range(n):
        product = random.choice(PRODUCTS)
        qty     = random.randint(1, 10) if product != "Nexora Enterprise" else 1
        price   = PRICES[product] * (1 - random.uniform(0, 0.15))  # up to 15% discount
        erp_rows.append({
            "order_id":    f"ORD-{len(erp_rows)+1000:05d}",
            "date":        d.strftime("%Y-%m-%d"),
            "product":     product,
            "region":      random.choice(REGIONS),
            "sales_rep":   random.choice(REPS),
            "segment":     random.choice(SEGMENTS),
            "quantity":    qty,
            "unit_price":  round(price, 2),
            "revenue":     round(price * qty, 2),
            "status":      random.choices(["Completed","Pending","Refunded"], weights=[88,8,4])[0],
        })

erp = pd.DataFrame(erp_rows)
erp.to_csv(f"{DATA_DIR}/erp_sales.csv", index=False)
print(f"  ERP: {len(erp)} orders")

# ── 2. CRM — Customer & Pipeline ─────────────────────────────────────────────
print("Generating CRM data...")
crm_rows = []
for i in range(320):
    created = START + timedelta(days=random.randint(0, 364))
    stage   = random.choices(
        ["Lead","Qualified","Proposal","Negotiation","Closed Won","Closed Lost"],
        weights=[20,20,18,12,20,10])[0]
    value   = random.choice([PRICES[p] for p in PRODUCTS]) * random.randint(1,12)
    crm_rows.append({
        "deal_id":      f"CRM-{i+1:04d}",
        "company":      f"Company {i+1:03d}",
        "segment":      random.choice(SEGMENTS),
        "region":       random.choice(REGIONS),
        "sales_rep":    random.choice(REPS),
        "stage":        stage,
        "deal_value":   round(value, 2),
        "created_date": created.strftime("%Y-%m-%d"),
        "close_date":   (created + timedelta(days=random.randint(14, 90))).strftime("%Y-%m-%d"),
        "probability":  {"Lead":10,"Qualified":30,"Proposal":50,"Negotiation":75,
                         "Closed Won":100,"Closed Lost":0}[stage],
        "churn_risk":   random.choices(["Low","Medium","High"], weights=[60,25,15])[0],
    })

crm = pd.DataFrame(crm_rows)
crm.to_csv(f"{DATA_DIR}/crm_pipeline.csv", index=False)
print(f"  CRM: {len(crm)} deals")

# ── 3. Marketing — Daily Channel Metrics ─────────────────────────────────────
print("Generating Marketing data...")
mkt_rows = []
for d in dates:
    for ch in CHANNELS:
        spend    = round(random.uniform(50, 800) if ch == "Paid Search" else random.uniform(0, 200), 2)
        sessions = int(random.uniform(200, 2000) * (1.3 if ch == "Organic" else 1))
        conv_r   = random.uniform(0.01, 0.06)
        leads    = int(sessions * conv_r)
        mkt_rows.append({
            "date":        d.strftime("%Y-%m-%d"),
            "channel":     ch,
            "spend":       spend,
            "sessions":    sessions,
            "leads":       leads,
            "conversions": int(leads * random.uniform(0.05, 0.25)),
            "cpc":         round(spend / max(sessions, 1) * 100, 4),
            "cpl":         round(spend / max(leads, 1), 2),
        })

mkt = pd.DataFrame(mkt_rows)
mkt.to_csv(f"{DATA_DIR}/marketing_channels.csv", index=False)
print(f"  Marketing: {len(mkt)} rows")

# ── 4. Finance — Monthly P&L ─────────────────────────────────────────────────
print("Generating Finance data...")
fin_rows = []
base_rev = 380_000
for m in months:
    growth   = 1 + random.uniform(0.02, 0.09)
    base_rev *= growth
    revenue  = round(base_rev, 2)
    cogs     = round(revenue * random.uniform(0.28, 0.34), 2)
    gp       = revenue - cogs
    opex     = round(revenue * random.uniform(0.38, 0.48), 2)
    ebitda   = gp - opex
    fin_rows.append({
        "month":          m.strftime("%Y-%m"),
        "revenue":        revenue,
        "cogs":           cogs,
        "gross_profit":   gp,
        "gross_margin":   round(gp / revenue * 100, 2),
        "opex":           opex,
        "ebitda":         round(ebitda, 2),
        "ebitda_margin":  round(ebitda / revenue * 100, 2),
        "cash_balance":   round(random.uniform(1_200_000, 3_500_000), 2),
        "arr":            round(revenue * 12, 2),
        "mrr":            round(revenue, 2),
        "new_mrr":        round(revenue * random.uniform(0.12, 0.22), 2),
        "churned_mrr":    round(revenue * random.uniform(0.02, 0.06), 2),
        "expansion_mrr":  round(revenue * random.uniform(0.04, 0.10), 2),
    })

fin = pd.DataFrame(fin_rows)
fin.to_csv(f"{DATA_DIR}/finance_pl.csv", index=False)
print(f"  Finance: {len(fin)} months")

# ── 5. HR — Headcount & Productivity ─────────────────────────────────────────
print("Generating HR data...")
departments = ["Sales","Engineering","Marketing","Customer Success","Finance","Operations"]
hr_rows = []
for m in months:
    for dept in departments:
        base_hc = {"Sales":18,"Engineering":32,"Marketing":10,"Customer Success":14,
                   "Finance":6,"Operations":8}[dept]
        hc      = base_hc + random.randint(-1, 3)
        hr_rows.append({
            "month":       m.strftime("%Y-%m"),
            "department":  dept,
            "headcount":   hc,
            "new_hires":   random.randint(0, 2),
            "attrition":   random.randint(0, 1),
            "avg_salary":  round(random.uniform(65000, 135000), 0),
            "quota_attainment": round(random.uniform(70, 120), 1) if dept == "Sales" else None,
        })

hr = pd.DataFrame(hr_rows)
hr.to_csv(f"{DATA_DIR}/hr_headcount.csv", index=False)
print(f"  HR: {len(hr)} rows")

# ── 6. Support — Ticket Metrics ───────────────────────────────────────────────
print("Generating Support data...")
sup_rows = []
for d in dates:
    opened = random.randint(5, 35)
    sup_rows.append({
        "date":              d.strftime("%Y-%m-%d"),
        "tickets_opened":    opened,
        "tickets_resolved":  int(opened * random.uniform(0.80, 1.10)),
        "avg_resolution_hrs":round(random.uniform(1.5, 18), 1),
        "csat_score":        round(random.uniform(3.5, 5.0), 2),
        "nps":               random.randint(20, 75),
        "escalations":       random.randint(0, 4),
    })

sup = pd.DataFrame(sup_rows)
sup.to_csv(f"{DATA_DIR}/support_tickets.csv", index=False)
print(f"  Support: {len(sup)} rows")

print("\n✅ All 6 data sources generated in /data/")
print("   Files: erp_sales.csv, crm_pipeline.csv, marketing_channels.csv,")
print("          finance_pl.csv, hr_headcount.csv, support_tickets.csv")
