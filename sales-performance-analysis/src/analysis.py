"""
analysis.py
End-to-end sales data analysis:
  1. Load & clean raw tables
  2. Merge into master DataFrame
  3. Engineer business metrics
  4. EDA — revenue / profit / margin by product, customer, channel, region
  5. Monthly trend analysis
  6. Export processed data + charts
"""

import os, warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings("ignore")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.abspath(__file__)) + "/.."
RAW    = f"{BASE}/data/raw"
PROC   = f"{BASE}/data/processed"
IMGDIR = f"{BASE}/images"
os.makedirs(PROC,   exist_ok=True)
os.makedirs(IMGDIR, exist_ok=True)

# ── Styling ────────────────────────────────────────────────────────────────────
PALETTE  = ["#2563EB","#7C3AED","#059669","#DC2626","#D97706",
            "#0891B2","#DB2777","#65A30D","#EA580C","#4F46E5"]
BG       = "#F8FAFC"
GRID_CLR = "#E2E8F0"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG,
    "axes.edgecolor": "#CBD5E1", "axes.grid": True,
    "grid.color": GRID_CLR, "grid.linewidth": 0.6,
    "font.family": "DejaVu Sans", "axes.titlesize": 13,
    "axes.titleweight": "bold", "axes.labelsize": 11,
    "xtick.labelsize": 9, "ytick.labelsize": 9,
})

def save(fig, name):
    path = f"{IMGDIR}/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  📊  Saved: {name}.png")

def fmt_inr(x, pos=None):
    if x >= 1e6: return f"₹{x/1e6:.1f}M"
    if x >= 1e3: return f"₹{x/1e3:.0f}K"
    return f"₹{x:.0f}"

# ══════════════════════════════════════════════════════════════════════════════
# 1 ── LOAD & CLEAN
# ══════════════════════════════════════════════════════════════════════════════
print("\n📂  Loading data …")
orders_df    = pd.read_csv(f"{RAW}/orders.csv",    parse_dates=["order_date"])
products_df  = pd.read_csv(f"{RAW}/products.csv")
customers_df = pd.read_csv(f"{RAW}/customers.csv")

# Basic cleaning
orders_df.dropna(subset=["order_id","customer_id","product_id"], inplace=True)
orders_df["quantity"] = orders_df["quantity"].clip(lower=1)
orders_df["discount"] = orders_df["discount"].clip(0, 0.50)

print(f"   Orders: {len(orders_df):,} rows  | nulls: {orders_df.isnull().sum().sum()}")

# ══════════════════════════════════════════════════════════════════════════════
# 2 ── MERGE
# ══════════════════════════════════════════════════════════════════════════════
df = (orders_df
      .merge(products_df,  on="product_id",  how="left")
      .merge(customers_df, on="customer_id", how="left"))

# ══════════════════════════════════════════════════════════════════════════════
# 3 ── FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════════════════════
df["profit_margin_pct"] = (df["profit"] / df["revenue"].replace(0, np.nan) * 100).round(2)
df["avg_order_value"]   = df["revenue"] / df["quantity"]
df["year"]              = df["order_date"].dt.year
df["month"]             = df["order_date"].dt.month
df["month_name"]        = df["order_date"].dt.strftime("%b")
df["year_month"]        = df["order_date"].dt.to_period("M")

# Save processed
df.to_csv(f"{PROC}/master_sales.csv", index=False)
print(f"   ✅  Master dataset: {df.shape[0]:,} rows × {df.shape[1]} cols\n")

# ══════════════════════════════════════════════════════════════════════════════
# 4 ── KPI SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
total_rev    = df["revenue"].sum()
total_profit = df["profit"].sum()
avg_margin   = df["profit_margin_pct"].mean()
total_orders = df["order_id"].nunique()
aov          = df["revenue"].sum() / total_orders

print("═" * 50)
print("📈  KPI SUMMARY")
print("═" * 50)
print(f"   Total Revenue  : {fmt_inr(total_rev)}")
print(f"   Total Profit   : {fmt_inr(total_profit)}")
print(f"   Avg Margin     : {avg_margin:.1f}%")
print(f"   Total Orders   : {total_orders:,}")
print(f"   Avg Order Value: {fmt_inr(aov)}")
print("═" * 50 + "\n")

kpis = pd.DataFrame({
    "KPI": ["Total Revenue","Total Profit","Avg Profit Margin %","Total Orders","Avg Order Value"],
    "Value": [f"₹{total_rev:,.0f}", f"₹{total_profit:,.0f}",
              f"{avg_margin:.1f}%", f"{total_orders:,}", f"₹{aov:,.0f}"]
})
kpis.to_csv(f"{PROC}/kpi_summary.csv", index=False)

# ══════════════════════════════════════════════════════════════════════════════
# 5 ── CHART 1: Monthly Revenue & Profit Trend
# ══════════════════════════════════════════════════════════════════════════════
monthly = (df.groupby("year_month")[["revenue","profit"]]
             .sum().reset_index())
monthly["year_month_str"] = monthly["year_month"].astype(str)
monthly.to_csv(f"{PROC}/monthly_trend.csv", index=False)

fig, ax = plt.subplots(figsize=(14, 5))
x = range(len(monthly))
ax.fill_between(x, monthly["revenue"], alpha=0.15, color=PALETTE[0])
ax.fill_between(x, monthly["profit"],  alpha=0.20, color=PALETTE[2])
ax.plot(x, monthly["revenue"], color=PALETTE[0], lw=2.2, label="Revenue",  marker="o", ms=3)
ax.plot(x, monthly["profit"],  color=PALETTE[2], lw=2.2, label="Profit",   marker="o", ms=3)
step = max(1, len(monthly) // 12)
ax.set_xticks(list(x)[::step])
ax.set_xticklabels(monthly["year_month_str"].iloc[::step], rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Monthly Revenue & Profit Trend (2022–2024)")
ax.set_xlabel("Month"); ax.set_ylabel("Amount (₹)")
ax.legend(framealpha=0.9)
save(fig, "01_monthly_trend")

# ══════════════════════════════════════════════════════════════════════════════
# 6 ── CHART 2: Revenue by Category
# ══════════════════════════════════════════════════════════════════════════════
cat_rev = (df.groupby("category")[["revenue","profit"]]
             .sum().sort_values("revenue", ascending=True))
cat_rev.to_csv(f"{PROC}/revenue_by_category.csv")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, col, color, title in zip(
        axes, ["revenue","profit"], [PALETTE[0],PALETTE[2]],
        ["Revenue by Category","Profit by Category"]):
    bars = ax.barh(cat_rev.index, cat_rev[col], color=color, alpha=0.85, edgecolor="white")
    for bar in bars:
        ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height()/2,
                fmt_inr(bar.get_width()), va="center", fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
    ax.set_title(title); ax.set_xlabel("Amount (₹)")
fig.tight_layout()
save(fig, "02_revenue_profit_by_category")

# ══════════════════════════════════════════════════════════════════════════════
# 7 ── CHART 3: Revenue & Profit by Region
# ══════════════════════════════════════════════════════════════════════════════
region = df.groupby("region")[["revenue","profit"]].sum().reset_index()
region["margin"] = (region["profit"] / region["revenue"] * 100).round(1)
region.to_csv(f"{PROC}/region_analysis.csv", index=False)

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(region))
w = 0.38
ax.bar(x - w/2, region["revenue"], w, color=PALETTE[0], alpha=0.85, label="Revenue")
ax.bar(x + w/2, region["profit"],  w, color=PALETTE[2], alpha=0.85, label="Profit")
for i, row in region.iterrows():
    ax.text(i, max(row["revenue"], row["profit"]) * 1.02,
            f'{row["margin"]}%', ha="center", fontsize=9, fontweight="bold", color="#374151")
ax.set_xticks(x); ax.set_xticklabels(region["region"])
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Revenue & Profit by Region  (% = Profit Margin)")
ax.legend(framealpha=0.9)
save(fig, "03_region_analysis")

# ══════════════════════════════════════════════════════════════════════════════
# 8 ── CHART 4: Sales Channel Mix
# ══════════════════════════════════════════════════════════════════════════════
channel = df.groupby("channel")[["revenue","profit"]].sum().reset_index().sort_values("revenue", ascending=False)
channel.to_csv(f"{PROC}/channel_analysis.csv", index=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
wedges, texts, autotexts = axes[0].pie(
    channel["revenue"], labels=channel["channel"],
    autopct="%1.1f%%", colors=PALETTE[:4],
    startangle=140, pctdistance=0.82,
    wedgeprops=dict(width=0.55, edgecolor="white"))
axes[0].set_title("Revenue Mix by Channel")

sns.barplot(data=channel, x="channel", y="profit", ax=axes[1],
            palette=PALETTE[:4], edgecolor="white")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
axes[1].set_title("Profit by Channel")
axes[1].set_xlabel(""); axes[1].set_ylabel("Profit (₹)")
fig.tight_layout()
save(fig, "04_channel_analysis")

# ══════════════════════════════════════════════════════════════════════════════
# 9 ── CHART 5: Top 10 Products by Revenue
# ══════════════════════════════════════════════════════════════════════════════
prod = (df.groupby("product_name")[["revenue","profit"]]
          .sum().sort_values("revenue", ascending=False).head(10))
prod["margin"] = (prod["profit"] / prod["revenue"] * 100).round(1)
prod.to_csv(f"{PROC}/top_products.csv")

fig, ax = plt.subplots(figsize=(12, 5))
colors = [PALETTE[0] if m >= prod["margin"].median() else PALETTE[3] for m in prod["margin"]]
bars = ax.bar(prod.index, prod["revenue"], color=colors, alpha=0.88, edgecolor="white")
for bar, margin in zip(bars, prod["margin"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
            f"{margin}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Top 10 Products by Revenue  (% = Profit Margin)  |  Blue = above-median margin")
ax.set_xlabel("Product"); ax.set_ylabel("Revenue (₹)")
plt.xticks(rotation=30, ha="right")
save(fig, "05_top_products")

# ══════════════════════════════════════════════════════════════════════════════
# 10 ── CHART 6: Top 15 Customers by Revenue (RFM proxy)
# ══════════════════════════════════════════════════════════════════════════════
cust = (df.groupby("customer_name").agg(
    revenue=("revenue","sum"), profit=("profit","sum"),
    orders=("order_id","nunique")).sort_values("revenue", ascending=False).head(15))
cust.to_csv(f"{PROC}/top_customers.csv")

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(cust.index[::-1], cust["revenue"][::-1],
               color=PALETTE[4], alpha=0.85, edgecolor="white")
for bar in bars:
    ax.text(bar.get_width() * 1.005, bar.get_y() + bar.get_height()/2,
            fmt_inr(bar.get_width()), va="center", fontsize=9)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Top 15 Customers by Revenue")
ax.set_xlabel("Revenue (₹)")
save(fig, "06_top_customers")

# ══════════════════════════════════════════════════════════════════════════════
# 11 ── CHART 7: Profit Margin Distribution
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].hist(df["profit_margin_pct"].dropna(), bins=40, color=PALETTE[1],
             alpha=0.8, edgecolor="white")
axes[0].axvline(avg_margin, color=PALETTE[3], lw=2, linestyle="--",
                label=f"Mean {avg_margin:.1f}%")
axes[0].set_title("Profit Margin Distribution")
axes[0].set_xlabel("Profit Margin %"); axes[0].legend()

seg = df.groupby("customer_segment")[["revenue","profit"]].sum().reset_index()
seg["margin"] = (seg["profit"] / seg["revenue"] * 100).round(1)
axes[1].bar(seg["customer_segment"], seg["margin"],
            color=PALETTE[:3], alpha=0.85, edgecolor="white")
for i, row in seg.iterrows():
    axes[1].text(i, row["margin"] + 0.3, f'{row["margin"]}%',
                 ha="center", fontsize=10, fontweight="bold")
axes[1].set_title("Avg Profit Margin by Customer Segment")
axes[1].set_ylabel("Margin %")
fig.tight_layout()
save(fig, "07_margin_analysis")

# ══════════════════════════════════════════════════════════════════════════════
# 12 ── CHART 8: Year-over-Year Comparison
# ══════════════════════════════════════════════════════════════════════════════
yoy = df.groupby(["year","month"])[["revenue","profit"]].sum().reset_index()
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
yoy["month_name"] = yoy["month"].apply(lambda x: months[x-1])

fig, ax = plt.subplots(figsize=(14, 5))
for yr, color in zip(sorted(yoy["year"].unique()), PALETTE):
    subset = yoy[yoy["year"] == yr].sort_values("month")
    ax.plot(subset["month_name"], subset["revenue"], marker="o",
            color=color, lw=2, label=str(yr), ms=5)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_inr))
ax.set_title("Year-over-Year Monthly Revenue Comparison")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (₹)")
ax.legend(title="Year", framealpha=0.9)
save(fig, "08_yoy_comparison")

print("\n✅  All charts saved to /images/")
print("✅  Processed data saved to /data/processed/")
print("\n🎉  Analysis complete!\n")
