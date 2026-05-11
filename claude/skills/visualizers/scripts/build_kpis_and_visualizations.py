from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set up paths
data_dir = Path("D:\\Documentos\\estudioProgramacion\\claude_tutorial\\.claude\\skills\\migrate\\data")
latest_data_dir = sorted(data_dir.glob("*"))[-1]  # Get latest timestamp folder
output_dir = Path("D:\\Documentos\\estudioProgramacion\\claude_tutorial\\.claude\\skills\\visualizers\\visualizations")

# Create output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

print(f"Reading data from: {latest_data_dir}")

# Read parquet files
fact_sales = pd.read_parquet(latest_data_dir / "fact_sales.parquet")
fact_returns = pd.read_parquet(latest_data_dir / "fact_returns.parquet")
dim_customer = pd.read_parquet(latest_data_dir / "dim_customer.parquet")
dim_product = pd.read_parquet(latest_data_dir / "dim_product.parquet")

print("Data loaded successfully!")
print(f"\nfact_sales shape: {fact_sales.shape}")
print(f"fact_returns shape: {fact_returns.shape}")

# Calculate KPIs
print("\n=== KPI Calculations ===")

# 1. Total Sales Amount
total_sales_amount = fact_sales["net_amount"].sum()
print(f"Total Sales Amount: ${total_sales_amount:,.2f}")

# 2. Average Sales Amount per Sale
avg_sales_per_order = fact_sales["net_amount"].mean()
print(f"Average Sales Amount per Order: ${avg_sales_per_order:,.2f}")

# 3. Total Returns Amount
total_returns_amount = fact_returns["refund_amount"].sum()
print(f"Total Returns Amount: ${total_returns_amount:,.2f}")

# 4. Average Returns Amount per Return
avg_returns_per_order = fact_returns["refund_amount"].mean()
print(f"Average Returns Amount per Order: ${avg_returns_per_order:,.2f}")

# Create visualizations
print("\n=== Creating Visualizations ===")

# Visualization 1: KPI Summary (Bar chart)
fig, ax = plt.subplots(figsize=(10, 6))
kpis = ["Total Sales", "Avg Sales/Order", "Total Returns", "Avg Returns/Order"]
values = [total_sales_amount, avg_sales_per_order, total_returns_amount, avg_returns_per_order]
colors = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12"]

bars = ax.bar(kpis, values, color=colors, alpha=0.7, edgecolor="black")
ax.set_ylabel("Amount ($)", fontsize=12, fontweight="bold")
ax.set_title("Sales & Returns KPIs Overview", fontsize=14, fontweight="bold")

# Add value labels on bars
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"${value:,.0f}",
        ha="center",
        va="bottom",
        fontweight="bold",
    )

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(output_dir / "01_kpi_summary.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 01_kpi_summary.png")
plt.close()

# Visualization 2: Sales Amount Distribution
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(fact_sales["net_amount"], bins=50, color="#3498db", alpha=0.7, edgecolor="black")
ax.set_xlabel("Sales Amount ($)", fontsize=12, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=12, fontweight="bold")
ax.set_title("Distribution of Sales Amounts", fontsize=14, fontweight="bold")
ax.axvline(fact_sales["net_amount"].mean(), color="red", linestyle="--", linewidth=2, label=f"Mean: ${fact_sales['net_amount'].mean():,.2f}")
ax.legend()
plt.tight_layout()
plt.savefig(output_dir / "02_sales_distribution.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 02_sales_distribution.png")
plt.close()

# Visualization 3: Returns Amount Distribution
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(fact_returns["refund_amount"], bins=50, color="#e74c3c", alpha=0.7, edgecolor="black")
ax.set_xlabel("Returns Amount ($)", fontsize=12, fontweight="bold")
ax.set_ylabel("Frequency", fontsize=12, fontweight="bold")
ax.set_title("Distribution of Returns Amounts", fontsize=14, fontweight="bold")
ax.axvline(fact_returns["refund_amount"].mean(), color="orange", linestyle="--", linewidth=2, label=f"Mean: ${fact_returns['refund_amount'].mean():,.2f}")
ax.legend()
plt.tight_layout()
plt.savefig(output_dir / "03_returns_distribution.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 03_returns_distribution.png")
plt.close()

# Visualization 4: Sales by Store (Top 20)
top_sales_by_store = fact_sales.groupby("store_sk")["net_amount"].sum().nlargest(20)
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.barh(range(len(top_sales_by_store)), top_sales_by_store.values, color="#2ecc71", alpha=0.7, edgecolor="black")
ax.set_yticks(range(len(top_sales_by_store)))
ax.set_yticklabels([f"Store {int(x)}" for x in top_sales_by_store.index])
ax.set_xlabel("Total Sales Amount ($)", fontsize=12, fontweight="bold")
ax.set_title("Top 20 Stores by Sales Amount", fontsize=14, fontweight="bold")
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_sales_by_store.values)):
    ax.text(value, i, f" ${value:,.0f}", va="center", fontweight="bold")

plt.tight_layout()
plt.savefig(output_dir / "04_top_20_orders_sales.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 04_top_20_orders_sales.png")
plt.close()

# Visualization 5: Sales vs Returns Comparison
fig, ax = plt.subplots(figsize=(10, 6))
comparison_data = {
    "Total Amount": [total_sales_amount, total_returns_amount],
    "Average per Order": [avg_sales_per_order, avg_returns_per_order],
}

x = list(comparison_data.keys())
sales_vals = [comparison_data[k][0] for k in x]
returns_vals = [comparison_data[k][1] for k in x]

x_pos = range(len(x))
width = 0.35

bars1 = ax.bar([p - width / 2 for p in x_pos], sales_vals, width, label="Sales", color="#2ecc71", alpha=0.7, edgecolor="black")
bars2 = ax.bar([p + width / 2 for p in x_pos], returns_vals, width, label="Returns", color="#e74c3c", alpha=0.7, edgecolor="black")

ax.set_ylabel("Amount ($)", fontsize=12, fontweight="bold")
ax.set_title("Sales vs Returns Comparison", fontsize=14, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(x)
ax.legend()

# Add value labels
for bar in bars1 + bars2:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"${height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig(output_dir / "05_sales_vs_returns.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 05_sales_vs_returns.png")
plt.close()

# Visualization 6: KPI Summary Table
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis("tight")
ax.axis("off")

kpi_data = [
    ["Metric", "Value"],
    ["Total Sales Amount", f"${total_sales_amount:,.2f}"],
    ["Average Sales Amount per Order", f"${avg_sales_per_order:,.2f}"],
    ["Total Returns Amount", f"${total_returns_amount:,.2f}"],
    ["Average Returns Amount per Order", f"${avg_returns_per_order:,.2f}"],
    ["Total Sales Records", f"{len(fact_sales)}"],
    ["Total Return Records", f"{len(fact_returns)}"],
]

table = ax.table(cellText=kpi_data, cellLoc="left", loc="center", colWidths=[0.6, 0.4])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Format header row
for i in range(2):
    table[(0, i)].set_facecolor("#34495e")
    table[(0, i)].set_text_props(weight="bold", color="white")

# Alternate row colors
for i in range(1, len(kpi_data)):
    for j in range(2):
        if i % 2 == 0:
            table[(i, j)].set_facecolor("#ecf0f1")
        else:
            table[(i, j)].set_facecolor("#ffffff")

ax.set_title("KPI Summary Table", fontsize=14, fontweight="bold", pad=20)
plt.savefig(output_dir / "06_kpi_summary_table.png", dpi=300, bbox_inches="tight")
print("[OK] Saved: 06_kpi_summary_table.png")
plt.close()

print(f"\n[OK] All visualizations saved to: {output_dir}")
print(f"[OK] Total visualizations created: 6")
