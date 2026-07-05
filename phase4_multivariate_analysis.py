# ============================================================
#  PHASE 4 - Multivariate Analysis & Correlation
#  Charts saved as PNG files - no popup windows needed
# ============================================================
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid", palette="muted")

print("="*60)
print("  PHASE 4 - Multivariate Analysis & Correlation")
print("="*60)

conn = sqlite3.connect("ecommerce.db")

print("\nStep 1: Building master dataframe from all 4 tables...")
df = pd.read_sql("""
SELECT c.age, c.city, c.gender, p.category, p.price, p.cost_price,
    ROUND(p.price - p.cost_price, 2)                      AS profit_per_unit,
    ROUND((p.price - p.cost_price)*100.0 / p.price, 2)   AS margin_pct,
    oi.quantity,
    ROUND(oi.quantity * oi.unit_price, 2)                 AS line_revenue
FROM customers c
JOIN orders      o  ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
JOIN products    p  ON oi.product_id = p.product_id
WHERE o.status = 'Completed'
""", conn)
df["age_group"] = pd.cut(df["age"], bins=[17,25,35,45,55,100],
                          labels=["18-25","26-35","36-45","46-55","56+"])
print(f"  Master dataframe ready: {df.shape[0]} rows x {df.shape[1]} columns")
print("\nStep 2: Creating and saving 7 advanced charts...\n")

# ── Chart 1: Scatter - Age vs Revenue ────────────────────────
fig, ax = plt.subplots(figsize=(9,6))
for cat in df["category"].unique():
    sub = df[df["category"]==cat]
    ax.scatter(sub["age"], sub["line_revenue"], alpha=0.4, s=25, label=cat)
z = np.polyfit(df["age"], df["line_revenue"], 1)
x_line = np.linspace(df["age"].min(), df["age"].max(), 100)
ax.plot(x_line, np.poly1d(z)(x_line), color="red", linewidth=2, linestyle="--", label="Trend")
corr = df["age"].corr(df["line_revenue"])
ax.set_title(f"Age vs Revenue  (Pearson r = {corr:.3f})", fontsize=13, fontweight="bold")
ax.set_xlabel("Customer Age"); ax.set_ylabel("Line Revenue (Rs.)")
ax.legend(bbox_to_anchor=(1.01,1), loc="upper left", fontsize=8)
plt.tight_layout(); plt.savefig("scatter_age_vs_revenue.png", dpi=150, bbox_inches="tight"); plt.close()
print(f"  Chart 1/7 saved --> scatter_age_vs_revenue.png  (Correlation = {corr:.3f})")

# ── Chart 2: Scatter - Price vs Margin ───────────────────────
product_df = pd.read_sql("""
SELECT name, category, price, cost_price,
    ROUND((price-cost_price)*100.0/price, 2) AS margin_pct
FROM products""", conn)
fig, ax = plt.subplots(figsize=(9,6))
for cat in product_df["category"].unique():
    sub = product_df[product_df["category"]==cat]
    ax.scatter(sub["price"], sub["margin_pct"], s=80, alpha=0.8, label=cat)
z2 = np.polyfit(product_df["price"], product_df["margin_pct"], 1)
x2 = np.linspace(product_df["price"].min(), product_df["price"].max(), 100)
ax.plot(x2, np.poly1d(z2)(x2), color="red", linestyle="--", linewidth=1.8, label="Trend")
ax.set_title("Product Price vs Profit Margin %", fontsize=13, fontweight="bold")
ax.set_xlabel("Selling Price (Rs.)"); ax.set_ylabel("Profit Margin (%)")
ax.legend(bbox_to_anchor=(1.01,1), loc="upper left", fontsize=8)
plt.tight_layout(); plt.savefig("scatter_price_vs_margin.png", dpi=150, bbox_inches="tight"); plt.close()
print("  Chart 2/7 saved --> scatter_price_vs_margin.png")

# ── Chart 3: Scatter - Quantity vs Revenue ────────────────────
fig, ax = plt.subplots(figsize=(9,6))
sc = ax.scatter(df["quantity"], df["line_revenue"], c=df["price"], cmap="YlOrRd", alpha=0.5, s=30)
plt.colorbar(sc, ax=ax).set_label("Unit Price (Rs.)", fontsize=10)
ax.set_title("Quantity Ordered vs Line Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Quantity Ordered"); ax.set_ylabel("Line Revenue (Rs.)")
plt.tight_layout(); plt.savefig("scatter_qty_vs_revenue.png", dpi=150); plt.close()
print("  Chart 3/7 saved --> scatter_qty_vs_revenue.png")

# ── Chart 4: Correlation Heatmap ─────────────────────────────
num_cols = ["age","price","cost_price","profit_per_unit","margin_pct","quantity","line_revenue"]
corr_matrix = df[num_cols].corr().round(2)
print("\n  Correlation Matrix:")
print(corr_matrix.to_string())
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
fig, ax = plt.subplots(figsize=(10,8))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            center=0, vmin=-1, vmax=1, linewidths=0.5, linecolor="white", square=True, ax=ax)
ax.set_title("Correlation Heatmap - All Numerical Variables", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("heatmap_correlation.png", dpi=150); plt.close()
print("\n  Chart 4/7 saved --> heatmap_correlation.png")

# ── Chart 5: Pair Plot ────────────────────────────────────────
top4 = df["category"].value_counts().head(4).index.tolist()
pair_df = df[df["category"].isin(top4)][["age","price","quantity","line_revenue","category"]].copy()
g = sns.pairplot(pair_df, hue="category",
                 vars=["age","price","quantity","line_revenue"],
                 diag_kind="kde", plot_kws={"alpha":0.4,"s":20}, height=2.2)
g.figure.suptitle("Pair Plot - Key Variables by Category", y=1.02, fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("pairplot_key_variables.png", dpi=130, bbox_inches="tight"); plt.close()
print("  Chart 5/7 saved --> pairplot_key_variables.png")

# ── Chart 6: City x Category Heatmap ─────────────────────────
pivot = df.groupby(["city","category"])["line_revenue"].sum().unstack(fill_value=0).round(0)
fig, ax = plt.subplots(figsize=(12,7))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
            linewidths=0.4, linecolor="white", ax=ax)
ax.set_title("Total Revenue - City x Product Category", fontsize=13, fontweight="bold")
plt.xticks(rotation=30, ha="right")
plt.tight_layout(); plt.savefig("heatmap_city_category.png", dpi=150); plt.close()
print("  Chart 6/7 saved --> heatmap_city_category.png")

# ── Chart 7: Box Plot ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10,6))
sns.boxplot(data=df, x="age_group", y="line_revenue", palette="Set2", ax=ax,
            order=["18-25","26-35","36-45","46-55","56+"])
ax.set_title("Revenue Distribution by Age Group", fontsize=13, fontweight="bold")
ax.set_xlabel("Age Group"); ax.set_ylabel("Line Revenue (Rs.)")
plt.tight_layout(); plt.savefig("boxplot_revenue_age_group.png", dpi=150); plt.close()
print("  Chart 7/7 saved --> boxplot_revenue_age_group.png")

conn.close()
print("\n" + "="*60)
print("  PHASE 4 COMPLETE!")
print("="*60)
print("\n7 advanced chart PNG files saved in your folder:")
for f in ["scatter_age_vs_revenue.png","scatter_price_vs_margin.png",
          "scatter_qty_vs_revenue.png","heatmap_correlation.png",
          "pairplot_key_variables.png","heatmap_city_category.png",
          "boxplot_revenue_age_group.png"]:
    print(f"  --> {f}")
print("\nOpen your folder and double-click any PNG to view it.")