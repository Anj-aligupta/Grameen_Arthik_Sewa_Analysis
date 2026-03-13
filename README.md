# 📊 Executive Revenue Intelligence Dashboard

A real-time C-suite business intelligence dashboard that consolidates data from **6 sources** — ERP, CRM, Marketing, Finance, HR, and Support — into a single interactive interface used for executive decision-making.



---

## 🖥️ Live Preview

![Dashboard Preview](https://via.placeholder.com/900x500/080c14/3b82f6?text=Revenue+Intelligence+Dashboard)

---

## 🚀 Quick Start (Run in 3 steps)

```bash
# 1. Clone and enter the project
git clone https://github.com/YOUR_USERNAME/revenue-dashboard.git
cd revenue-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate mock data, then run the app
python generate_data.py
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## 📁 Project Structure

```
revenue-dashboard/
│
├── generate_data.py        ← Step 1: Creates all 6 mock data sources
├── app.py                  ← Step 2: Flask backend + REST API
├── requirements.txt        ← Python dependencies
│
├── data/                   ← Auto-generated CSV files (git-ignored)
│   ├── erp_sales.csv           (6,000+ rows · sales orders)
│   ├── crm_pipeline.csv        (320 deals · pipeline stages)
│   ├── marketing_channels.csv  (2,196 rows · channel metrics)
│   ├── finance_pl.csv          (12 months · P&L data)
│   ├── hr_headcount.csv        (72 rows · dept headcount)
│   └── support_tickets.csv     (366 rows · daily tickets)
│
└── templates/
    └── dashboard.html      ← Full frontend (HTML + CSS + Chart.js)
```

---

## 🔌 Data Sources (Simulated)

| Source | File | Rows | Key Metrics |
|--------|------|------|-------------|
| **ERP** (Sales Orders) | `erp_sales.csv` | 6,013 | Revenue, units sold, product, region, rep |
| **CRM** (Pipeline) | `crm_pipeline.csv` | 320 | Deal stage, value, probability, churn risk |
| **Marketing** | `marketing_channels.csv` | 2,196 | Spend, leads, CPL, sessions by channel |
| **Finance** (P&L) | `finance_pl.csv` | 12 | MRR, ARR, Gross Margin, EBITDA |
| **HR** | `hr_headcount.csv` | 72 | Headcount, new hires, attrition by dept |
| **Support** | `support_tickets.csv` | 366 | CSAT, NPS, resolution time, ticket volume |

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard UI |
| `GET /api/kpis` | Top-level KPI cards (MRR, ARR, EBITDA, etc.) |
| `GET /api/revenue-trend` | Monthly revenue, GP, EBITDA trend |
| `GET /api/sales-breakdown` | Revenue by product, region, rep, segment |
| `GET /api/pipeline` | CRM funnel, churn risk, won deals |
| `GET /api/marketing` | Channel spend, leads, CPL |
| `GET /api/support` | CSAT, NPS, ticket volume |
| `GET /api/headcount` | Headcount by dept/month |

---

## 📊 Dashboard Views

1. **Executive Summary** — KPI cards + top 4 charts from all sources
2. **Revenue & Finance** — MRR trend, waterfall, margins
3. **Sales (ERP)** — Product/region/rep/segment breakdown
4. **Pipeline (CRM)** — Deal funnel, churn risk, won by rep
5. **Marketing** — Channel spend, leads, CPL efficiency
6. **Support** — CSAT, NPS, resolution time
7. **Headcount (HR)** — Team growth by department

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Flask |
| Data | Pandas · NumPy |
| Frontend | Vanilla JS · Chart.js 4 |
| Fonts | Google Fonts (Syne + JetBrains Mono) |
| Deployment | Any Python host (Railway, Render, Heroku) |

---

## 🌐 Deploy to the Web (Free)

### Option A: Render.com
1. Push to GitHub
2. Create a new **Web Service** on render.com
3. Build command: `pip install -r requirements.txt && python generate_data.py`
4. Start command: `python app.py`

### Option B: Railway.app
1. Push to GitHub
2. Connect repo on railway.app
3. It auto-detects Flask and deploys

---

## 💼 What This Demonstrates

- **Data Engineering** — Building ETL-ready data pipelines from multiple sources
- **Backend Development** — RESTful API design with Flask
- **Data Analysis** — P&L modeling, MRR waterfall, funnel analysis, cohort metrics
- **Data Visualization** — Interactive Chart.js dashboards
- **Business Acumen** — Understanding of SaaS metrics (MRR, ARR, EBITDA, CSAT, NPS)
- **Full-Stack Delivery** — End-to-end project from data → API → UI

---


