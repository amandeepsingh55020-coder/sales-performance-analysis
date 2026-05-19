# 📊 Sales Performance Analysis

> End-to-end sales data analysis using Python — uncovering revenue & profit drivers across products, customers, channels, and regions.

---

## 🗂 Project Structure

```
sales-performance-analysis/
│
├── data/
│   ├── raw/                  # Source tables (orders, products, customers)
│   └── processed/            # Cleaned master dataset + aggregated CSVs
│
├── notebooks/
│   └── sales_analysis.ipynb  # Full analysis notebook (EDA + insights)
│
├── src/
│   ├── generate_data.py      # Synthetic dataset generator (reproducible)
│   └── analysis.py           # End-to-end analysis + chart export script
│
├── images/                   # All exported charts (8 visualizations)
├── requirements.txt
└── README.md
```

---

## 🎯 Problem Statement

A sales team needs visibility into **what's driving revenue and profit** across 3 years of transactions. The goal: identify top-performing products, high-value customers, and underperforming regions to support data-driven decisions.

---

## 📦 Dataset Overview

| Table | Rows | Description |
|---|---|---|
| `orders.csv` | 5,000 | Order-level transactions (2022–2024) |
| `products.csv` | 20 | Product catalog with unit cost & price |
| `customers.csv` | 500 | Customer profiles — region & segment |

---

## ⚙️ What Was Done

### 1. Data Cleaning & Merging
- Handled nulls, clipped invalid quantities & discounts
- Merged 3 tables into a single master DataFrame (5,000 × 23)

### 2. Feature Engineering
| Metric | Formula |
|---|---|
| Profit | Revenue − Cost |
| Profit Margin % | (Profit / Revenue) × 100 |
| Avg Order Value | Revenue / Quantity |
| Year-Month | Derived from order_date |

### 3. Exploratory Data Analysis (EDA)
- Revenue & profit by **product category**
- Performance by **region** and **sales channel**
- **Top 10 products** and **Top 15 customers** by revenue
- **Monthly trend** and **Year-over-Year** comparison

---

## 📈 Key KPIs

| KPI | Value |
|---|---|
| Total Revenue | ₹3.1M |
| Total Profit | ₹1.3M |
| Avg Profit Margin | 41.9% |
| Total Orders | 5,000 |
| Avg Order Value | ₹615 |

---

## 💡 Key Insights

1. **Electronics** generates the highest revenue; **Clothing** has the best profit margin
2. **North region** leads in revenue — **Central region** consistently underperforms
3. **Online channel** (35%+ share) is the top-performing sales channel
4. Top 15 customers contribute ~18% of total revenue — high-value retention is critical
5. Strong **Q4 seasonality** (Oct–Dec) — inventory and campaign planning needed

---

## 📊 Visualizations

| Chart | Description |
|---|---|
| `01_monthly_trend` | Revenue & Profit trend across 36 months |
| `02_revenue_profit_by_category` | Category-wise revenue & profit bars |
| `03_region_analysis` | Regional performance with margin % |
| `04_channel_analysis` | Channel mix (pie) + profit by channel |
| `05_top_products` | Top 10 products with margin annotation |
| `06_top_customers` | Top 15 customers by revenue |
| `07_margin_analysis` | Margin distribution + segment comparison |
| `08_yoy_comparison` | Year-over-Year monthly revenue overlay |

---

## 🖥 Power BI Dashboard

The analyzed data (`data/processed/master_sales.csv`) powers an interactive Power BI dashboard featuring:
- **KPI Cards** — Revenue, Profit, Margin, Orders
- **Slicers** — Year, Region, Channel, Category
- **Drill-throughs** — Product → Order detail
- **Page Navigation** — Overview → Products → Customers → Regions

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/your-username/sales-performance-analysis.git
cd sales-performance-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic data
python src/generate_data.py

# 4. Run full analysis (exports charts + processed CSVs)
python src/analysis.py

# 5. Or open the notebook
jupyter notebook notebooks/sales_analysis.ipynb
```

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-purple?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12-teal)
![PowerBI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?logo=powerbi)

---

