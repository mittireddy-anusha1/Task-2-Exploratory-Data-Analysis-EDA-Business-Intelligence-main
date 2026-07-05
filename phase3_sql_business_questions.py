# ============================================================
#  PHASE 3 - SQL for Business Questions
#  7 business questions answered with SQL queries
#  Charts saved as PNG files - no popup windows needed
# ============================================================
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

print("="*60)
print("  PHASE 3 - SQL Business Questions")
print("="*60)

conn = sqlite3.connect("ecommerce.db")

def run_query(title, sql, interpretation):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)
    df = pd.read_sql(sql, conn)
    print(df.to_string(index=False))
    print(f"\n  INSIGHT: {interpretation}")
    return df

# ── Q1 ────────────────────────────────────────────────────────
df1 = run_query("Q1 - Top 5 Products by Revenue", """
SELECT p.name AS product_name, p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders   o ON oi.order_id   = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.product_id, p.name, p.category
ORDER BY total_revenue DESC
LIMIT 5;""",
"These 5 products generate the most revenue. Focus marketing and stock on them.")
fig, ax = plt.subplots(figsize=(9,5))
ax.barh(df1["product_name"][::-1], df1["total_revenue"][::-1], color="#5B5EA6", edgecolor="white")
ax.set_title("Top 5 Products by Revenue", fontsize=13, fontweight="bold")
ax.set_xlabel("Total Revenue (Rs.)"); ax.grid(axis="x", alpha=0.3)
plt.tight_layout(); plt.savefig("q1_top5_products.png", dpi=150); plt.close()
print("  Chart saved --> q1_top5_products.png")

# ── Q2 ────────────────────────────────────────────────────────
df2 = run_query("Q2 - Monthly Revenue Trend", """
SELECT strftime('%Y-%m', o.order_date) AS month,
    COUNT(DISTINCT o.order_id)                  AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS monthly_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'Completed'
GROUP BY month
ORDER BY month;""",
"Identifies peak and slow months. Use for seasonal promotions.")
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(df2["month"], df2["monthly_revenue"], color="#1D9E75", edgecolor="white")
ax.plot(df2["month"], df2["monthly_revenue"], color="#E8593C", marker="o", linewidth=2, label="Trend")
ax.set_title("Monthly Revenue Trend - 2023", fontsize=13, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Revenue (Rs.)")
plt.xticks(rotation=45, ha="right"); ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig("q2_monthly_revenue.png", dpi=150); plt.close()
print("  Chart saved --> q2_monthly_revenue.png")

# ── Q3 ────────────────────────────────────────────────────────
df3 = run_query("Q3 - Revenue by Product Category", """
SELECT p.category,
    COUNT(DISTINCT o.order_id)                  AS total_orders,
    SUM(oi.quantity)                            AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders   o ON oi.order_id   = o.order_id
WHERE o.status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;""",
"Shows which categories drive the business most.")
fig, ax = plt.subplots(figsize=(8,8))
ax.pie(df3["total_revenue"], labels=df3["category"], autopct="%1.1f%%", startangle=140,
    colors=["#5B5EA6","#1D9E75","#EF9F27","#E24B4A","#185FA5","#BA7517","#D85A30","#639922"])
ax.set_title("Revenue Share by Category", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("q3_category_revenue.png", dpi=150); plt.close()
print("  Chart saved --> q3_category_revenue.png")

# ── Q4 ────────────────────────────────────────────────────────
df4 = run_query("Q4 - Top 10 Customers by Spend", """
SELECT c.customer_id, c.name, c.city, c.age,
    COUNT(DISTINCT o.order_id)                  AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS total_spend
FROM customers c
JOIN orders      o  ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE o.status = 'Completed'
GROUP BY c.customer_id
ORDER BY total_spend DESC
LIMIT 10;""",
"These are your VIP customers. Target them with loyalty programmes.")
fig, ax = plt.subplots(figsize=(10,5))
ax.barh(df4["name"][::-1], df4["total_spend"][::-1], color="#E8593C", edgecolor="white")
ax.set_title("Top 10 Customers by Total Spend", fontsize=13, fontweight="bold")
ax.set_xlabel("Total Spend (Rs.)"); ax.grid(axis="x", alpha=0.3)
plt.tight_layout(); plt.savefig("q4_top_customers.png", dpi=150); plt.close()
print("  Chart saved --> q4_top_customers.png")

# ── Q5 ────────────────────────────────────────────────────────
df5 = run_query("Q5 - Cancellation Rate by City", """
SELECT c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN o.status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0
        / COUNT(o.order_id), 1
    ) AS cancellation_rate_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY cancellation_rate_pct DESC;""",
"High cancellation cities need a delivery or service audit.")
fig, ax = plt.subplots(figsize=(10,5))
colors5 = ["#E24B4A" if r>20 else "#EF9F27" if r>15 else "#1D9E75" for r in df5["cancellation_rate_pct"]]
ax.bar(df5["city"], df5["cancellation_rate_pct"], color=colors5, edgecolor="white")
ax.axhline(df5["cancellation_rate_pct"].mean(), color="#5B5EA6", linestyle="--",
           linewidth=1.5, label=f"Avg = {df5['cancellation_rate_pct'].mean():.1f}%")
ax.set_title("Cancellation Rate by City (%)", fontsize=13, fontweight="bold")
ax.set_ylabel("Cancellation Rate (%)"); ax.legend()
plt.xticks(rotation=30, ha="right"); ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig("q5_cancellation_city.png", dpi=150); plt.close()
print("  Chart saved --> q5_cancellation_city.png")

# ── Q6 ────────────────────────────────────────────────────────
df6 = run_query("Q6 - Avg Order Value by Age Group", """
SELECT
    CASE WHEN c.age BETWEEN 18 AND 25 THEN '18-25'
         WHEN c.age BETWEEN 26 AND 35 THEN '26-35'
         WHEN c.age BETWEEN 36 AND 45 THEN '36-45'
         WHEN c.age BETWEEN 46 AND 55 THEN '46-55'
         ELSE '56+' END                             AS age_group,
    COUNT(DISTINCT o.order_id)                      AS total_orders,
    ROUND(AVG(oi.quantity * oi.unit_price), 2)      AS avg_order_value,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)      AS total_revenue
FROM customers c
JOIN orders      o  ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id    = oi.order_id
WHERE o.status = 'Completed'
GROUP BY age_group
ORDER BY age_group;""",
"Reveals which age group spends most per order. Helps target ads.")
fig, ax = plt.subplots(figsize=(9,5))
ax.bar(df6["age_group"], df6["avg_order_value"], color="#185FA5", edgecolor="white", width=0.5)
ax.set_title("Average Order Value by Age Group", fontsize=13, fontweight="bold")
ax.set_xlabel("Age Group"); ax.set_ylabel("Avg Order Value (Rs.)"); ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig("q6_aov_age_group.png", dpi=150); plt.close()
print("  Chart saved --> q6_aov_age_group.png")

# ── Q7 ────────────────────────────────────────────────────────
df7 = run_query("Q7 - Profit Margin by Category", """
SELECT p.category,
    ROUND(AVG(p.price),      2)                          AS avg_selling_price,
    ROUND(AVG(p.cost_price), 2)                          AS avg_cost_price,
    ROUND(AVG(p.price - p.cost_price), 2)                AS avg_profit_per_unit,
    ROUND(AVG((p.price - p.cost_price)*100.0/p.price),1) AS profit_margin_pct
FROM products p
GROUP BY p.category
ORDER BY profit_margin_pct DESC;""",
"Categories with the highest margin are the most profitable per sale.")
fig, ax = plt.subplots(figsize=(10,5))
bar_colors7 = ["#1D9E75" if m>=40 else "#EF9F27" if m>=30 else "#E24B4A" for m in df7["profit_margin_pct"]]
bars = ax.bar(df7["category"], df7["profit_margin_pct"], color=bar_colors7, edgecolor="white")
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f"{bar.get_height():.1f}%", ha="center", fontsize=9)
ax.set_title("Profit Margin % by Category", fontsize=13, fontweight="bold")
ax.set_xlabel("Category"); ax.set_ylabel("Profit Margin (%)")
plt.xticks(rotation=30, ha="right"); ax.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.savefig("q7_profit_margin.png", dpi=150); plt.close()
print("  Chart saved --> q7_profit_margin.png")

conn.close()
print("\n" + "="*60)
print("  PHASE 3 COMPLETE!")
print("="*60)
print("\n7 charts saved in your folder:")
for f in ["q1_top5_products.png","q2_monthly_revenue.png","q3_category_revenue.png",
          "q4_top_customers.png","q5_cancellation_city.png","q6_aov_age_group.png","q7_profit_margin.png"]:
    print(f"  --> {f}")