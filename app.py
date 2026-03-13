"""
app.py
======
Flask backend that reads the 6 CSV data sources and exposes
REST API endpoints consumed by the dashboard frontend.

Run:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template
import pandas as pd
import os, json
from datetime import datetime

app = Flask(__name__)
DATA = os.path.join(os.path.dirname(__file__), "data")

# ── Helpers ────────────────────────────────────────────────────────────────────
def load():
    erp = pd.read_csv(f"{DATA}/erp_sales.csv", parse_dates=["date"])
    crm = pd.read_csv(f"{DATA}/crm_pipeline.csv", parse_dates=["created_date","close_date"])
    mkt = pd.read_csv(f"{DATA}/marketing_channels.csv", parse_dates=["date"])
    fin = pd.read_csv(f"{DATA}/finance_pl.csv")
    hr  = pd.read_csv(f"{DATA}/hr_headcount.csv")
    sup = pd.read_csv(f"{DATA}/support_tickets.csv", parse_dates=["date"])
    return erp, crm, mkt, fin, hr, sup

def pct_change(new, old):
    if old == 0: return 0
    return round((new - old) / old * 100, 1)

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/kpis")
def kpis():
    erp, crm, mkt, fin, hr, sup = load()

    completed = erp[erp.status == "Completed"]
    this_m = fin.iloc[-1]
    last_m = fin.iloc[-2]

    # Pipeline value
    pipeline = crm[crm.stage.isin(["Lead","Qualified","Proposal","Negotiation"])]
    pipeline_val = pipeline["deal_value"].sum()
    weighted_pipeline = (pipeline["deal_value"] * pipeline["probability"] / 100).sum()

    # Support CSAT last 30 days
    recent_sup = sup.tail(30)
    csat = round(recent_sup["csat_score"].mean(), 2)

    return jsonify({
        "mrr":              {"value": round(this_m["mrr"]), "change": pct_change(this_m["mrr"], last_m["mrr"])},
        "arr":              {"value": round(this_m["arr"]), "change": pct_change(this_m["arr"], last_m["arr"])},
        "gross_margin":     {"value": round(this_m["gross_margin"], 1), "change": pct_change(this_m["gross_margin"], last_m["gross_margin"])},
        "ebitda":           {"value": round(this_m["ebitda"]), "change": pct_change(this_m["ebitda"], last_m["ebitda"])},
        "pipeline":         {"value": round(pipeline_val), "change": round(weighted_pipeline)},
        "deals_won":        {"value": int((crm.stage == "Closed Won").sum()), "change": 0},
        "csat":             {"value": csat, "change": 0},
        "headcount":        {"value": int(hr[hr.month == hr.month.max()]["headcount"].sum()), "change": 0},
    })

@app.route("/api/revenue-trend")
def revenue_trend():
    fin = pd.read_csv(f"{DATA}/finance_pl.csv")
    return jsonify({
        "labels":         fin["month"].tolist(),
        "revenue":        fin["revenue"].round(0).tolist(),
        "gross_profit":   fin["gross_profit"].round(0).tolist(),
        "ebitda":         fin["ebitda"].round(0).tolist(),
        "mrr":            fin["mrr"].round(0).tolist(),
        "new_mrr":        fin["new_mrr"].round(0).tolist(),
        "churned_mrr":    fin["churned_mrr"].round(0).tolist(),
        "expansion_mrr":  fin["expansion_mrr"].round(0).tolist(),
    })

@app.route("/api/sales-breakdown")
def sales_breakdown():
    erp = pd.read_csv(f"{DATA}/erp_sales.csv", parse_dates=["date"])
    completed = erp[erp.status == "Completed"]

    by_product = completed.groupby("product")["revenue"].sum().round(0)
    by_region  = completed.groupby("region")["revenue"].sum().round(0)
    by_segment = completed.groupby("segment")["revenue"].sum().round(0)

    monthly = completed.copy()
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    by_month_product = monthly.groupby(["month","product"])["revenue"].sum().round(0).reset_index()

    top_reps = completed.groupby("sales_rep")["revenue"].sum().round(0).sort_values(ascending=False).head(8)

    return jsonify({
        "by_product":       {"labels": by_product.index.tolist(), "values": by_product.values.tolist()},
        "by_region":        {"labels": by_region.index.tolist(),  "values": by_region.values.tolist()},
        "by_segment":       {"labels": by_segment.index.tolist(), "values": by_segment.values.tolist()},
        "top_reps":         {"labels": top_reps.index.tolist(),   "values": top_reps.values.tolist()},
        "monthly_product":  by_month_product.to_dict(orient="records"),
    })

@app.route("/api/pipeline")
def pipeline():
    crm = pd.read_csv(f"{DATA}/crm_pipeline.csv")
    stages = ["Lead","Qualified","Proposal","Negotiation","Closed Won","Closed Lost"]
    funnel = crm.groupby("stage")["deal_value"].agg(["count","sum"]).reindex(stages).fillna(0)

    by_rep = crm[crm.stage == "Closed Won"].groupby("sales_rep")["deal_value"].sum().round(0).sort_values(ascending=False)
    by_seg = crm.groupby("segment")["deal_value"].sum().round(0)

    return jsonify({
        "funnel_stages":  stages,
        "funnel_count":   funnel["count"].astype(int).tolist(),
        "funnel_value":   funnel["sum"].round(0).tolist(),
        "by_rep":         {"labels": by_rep.index.tolist(), "values": by_rep.values.tolist()},
        "by_segment":     {"labels": by_seg.index.tolist(), "values": by_seg.values.tolist()},
        "churn_risk":     crm["churn_risk"].value_counts().to_dict(),
    })

@app.route("/api/marketing")
def marketing():
    mkt = pd.read_csv(f"{DATA}/marketing_channels.csv", parse_dates=["date"])
    mkt["month"] = mkt["date"].dt.to_period("M").astype(str)

    by_channel   = mkt.groupby("channel")[["spend","leads","conversions","sessions"]].sum().round(0)
    monthly_spend = mkt.groupby("month")["spend"].sum().round(0)
    cpl_channel  = (mkt.groupby("channel")["spend"].sum() / mkt.groupby("channel")["leads"].sum()).round(2)

    return jsonify({
        "channels":       by_channel.index.tolist(),
        "spend":          by_channel["spend"].tolist(),
        "leads":          by_channel["leads"].tolist(),
        "conversions":    by_channel["conversions"].tolist(),
        "sessions":       by_channel["sessions"].tolist(),
        "cpl":            cpl_channel.tolist(),
        "monthly_spend":  {"labels": monthly_spend.index.tolist(), "values": monthly_spend.values.tolist()},
    })

@app.route("/api/support")
def support():
    sup = pd.read_csv(f"{DATA}/support_tickets.csv", parse_dates=["date"])
    sup["month"] = sup["date"].dt.to_period("M").astype(str)

    monthly = sup.groupby("month").agg(
        tickets=("tickets_opened","sum"),
        resolved=("tickets_resolved","sum"),
        csat=("csat_score","mean"),
        nps=("nps","mean"),
        avg_resolution=("avg_resolution_hrs","mean"),
    ).round(2).reset_index()

    return jsonify({
        "labels":       monthly["month"].tolist(),
        "tickets":      monthly["tickets"].tolist(),
        "resolved":     monthly["resolved"].tolist(),
        "csat":         monthly["csat"].tolist(),
        "nps":          monthly["nps"].round(1).tolist(),
        "resolution":   monthly["avg_resolution"].tolist(),
    })

@app.route("/api/headcount")
def headcount():
    hr = pd.read_csv(f"{DATA}/hr_headcount.csv")
    months = sorted(hr["month"].unique())
    depts  = hr["department"].unique().tolist()

    pivot = hr.pivot_table(index="month", columns="department", values="headcount", aggfunc="sum")
    pivot = pivot.reindex(months)

    return jsonify({
        "months":      months,
        "departments": depts,
        "data":        {dept: pivot[dept].fillna(0).astype(int).tolist() for dept in depts if dept in pivot.columns},
    })

# Change this (development):
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# To this (production):
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
