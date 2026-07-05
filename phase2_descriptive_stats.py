# ============================================================
#  PHASE 2 - Descriptive Statistics & Univariate Analysis
#  Charts are saved as PNG files - no popup windows needed
# ============================================================
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')   # <-- saves charts as files, no popup needed
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

print("="*55)
print("  PHASE 2 - Descriptive Statistics")
print("="*55)

# ── Connect ──────────────────────────────────────────────────
print("\nStep 1: Connecting to database...")
conn = sqlite3.connect("ecommerce.db")
customers   = pd.read_sql("SELECT * FROM customers",   conn)
products    = pd.read_sql("SELECT * FROM products",    conn)
orders      = pd.read_sql("SELECT * FROM orders",      conn)
order_items = pd.read_sql("SELECT * FROM order_items", conn)
print(f"  customers   : {len(customers)} rows")
print(f"  products    : {len(products)} rows")
print(f"  orders      : {len(orders)} rows")
print(f"  order_items : {len(order_items)} rows")

# ── Numerical Stats ──────────────────────────────────────────
print("\n" + "="*55)
print("Step 2: NUMERICAL SUMMARY - CUSTOMERS (age)")
print("="*55)
print(customers[["age"]].describe().round(2).to_string())

print("\n" + "="*55)
print("Step 3: NUMERICAL SUMMARY - PRODUCTS (price, cost)")
print("="*55)
print(products[["price","cost_price"]].describe().round(2).to_string())

print("\n" + "="*55)
print("Step 4: NUMERICAL SUMMARY - ORDER ITEMS")
print("="*55)
order_items["revenue"] = order_items["quantity"] * order_items["unit_price"]
print(order_items[["quantity","unit_price","revenue"]].describe().round(2).to_string())

# ── Categorical Stats ─────────────────────────────────────────
print("\n" + "="*55)
print("Step 5: CATEGORICAL SUMMARY")
print("="*55)
print("\nCity distribution:")
print(customers["city"].value_counts().to_string())
print("\nGender distribution:")
print(customers["gender"].value_counts().to_string())
print("\nOrder status:")
print(orders["status"].value_counts().to_string())
print("\nProducts per category:")
print(products["category"].value_counts().to_string())

print("\n" + "="*55)
print("Step 6: Creating and saving 6 charts as PNG files...")
print("="*55)

# ── Chart 1: Age Histogram ────────────────────────────────────
fig, ax = plt.subplots(figsize=(9,5))
ax.hist(customers["age"], bins=15, color="#5B5EA6", edgecolor="white")
ax.axvline(customers["age"].mean(),   color="#E8593C", linestyle="--", linewidth=2, label=f"Mean   = {customers['age'].mean():.1f} yrs")
ax.axvline(customers["age"].median(), color="#1D9E75", linestyle="--", linewidth=2, label=f"Median = {customers['age'].median():.1f} yrs")
ax.set_title("Age Distribution of Customers", fontsize=14, fontweight="bold")
ax.set_xlabel("Age (years)")
ax.set_ylabel("Number of Customers")
ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("hist_age.png", dpi=150)
plt.close()
print("  Chart 1/6 saved --> hist_age.png")

# ── Chart 2: Price Histogram ──────────────────────────────────
fig, ax = plt.subplots(figsize=(9,5))
ax.hist(products["price"], bins=15, color="#1D9E75", edgecolor="white")
ax.axvline(products["price"].mean(),   color="#E8593C", linestyle="--", linewidth=2, label=f"Mean   = Rs.{products['price'].mean():.0f}")
ax.axvline(products["price"].median(), color="#5B5EA6", linestyle="--", linewidth=2, label=f"Median = Rs.{products['price'].median():.0f}")
ax.set_title("Product Price Distribution", fontsize=14, fontweight="bold")
ax.set_xlabel("Price (Rs.)")
ax.set_ylabel("Number of Products")
ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("hist_price.png", dpi=150)
plt.close()
print("  Chart 2/6 saved --> hist_price.png")

# ── Chart 3: Order Status Bar ─────────────────────────────────
status_counts = orders["status"].value_counts()
color_map = {"Completed":"#1D9E75", "Pending":"#EF9F27", "Cancelled":"#E24B4A"}
bar_colors = [color_map.get(s, "#888") for s in status_counts.index]
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(status_counts.index, status_counts.values, color=bar_colors, edgecolor="white", width=0.5)
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3,
            str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax.set_title("Order Count by Status", fontsize=14, fontweight="bold")
ax.set_xlabel("Order Status"); ax.set_ylabel("Number of Orders")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("bar_order_status.png", dpi=150)
plt.close()
print("  Chart 3/6 saved --> bar_order_status.png")

# ── Chart 4: Customers by City ────────────────────────────────
city_counts = customers["city"].value_counts()
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.bar(city_counts.index, city_counts.values, color="#5B5EA6", edgecolor="white")
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            str(int(bar.get_height())), ha="center", fontsize=10)
ax.set_title("Number of Customers per City", fontsize=14, fontweight="bold")
ax.set_xlabel("City"); ax.set_ylabel("Number of Customers")
plt.xticks(rotation=30, ha="right"); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("bar_customers_city.png", dpi=150)
plt.close()
print("  Chart 4/6 saved --> bar_customers_city.png")

# ── Chart 5: Products by Category ────────────────────────────
cat_counts  = products["category"].value_counts()
cat_colors  = ["#1D9E75","#5B5EA6","#EF9F27","#E24B4A","#185FA5","#BA7517","#D85A30","#639922"]
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(cat_counts.index, cat_counts.values,
               color=cat_colors[:len(cat_counts)], edgecolor="white")
for bar in bars:
    ax.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
            str(int(bar.get_width())), va="center", fontsize=10)
ax.set_title("Number of Products per Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Number of Products"); ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("bar_products_category.png", dpi=150)
plt.close()
print("  Chart 5/6 saved --> bar_products_category.png")

# ── Chart 6: Monthly Orders ───────────────────────────────────
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["month"]      = orders["order_date"].dt.to_period("M")
monthly_orders       = orders.groupby("month").size()
fig, ax = plt.subplots(figsize=(12,5))
ax.bar(monthly_orders.index.astype(str), monthly_orders.values,
       color="#185FA5", edgecolor="white")
ax.plot(monthly_orders.index.astype(str), monthly_orders.values,
        color="#E8593C", marker="o", linewidth=2, label="Trend line")
ax.set_title("Monthly Order Volume - 2023", fontsize=14, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Number of Orders")
plt.xticks(rotation=45, ha="right"); ax.legend(); ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("bar_monthly_orders.png", dpi=150)
plt.close()
print("  Chart 6/6 saved --> bar_monthly_orders.png")

conn.close()

print("\n" + "="*55)
print("  PHASE 2 COMPLETE!")
print("="*55)
print("\n6 chart PNG files saved in your folder:")
for f in ["hist_age.png","hist_price.png","bar_order_status.png",
          "bar_customers_city.png","bar_products_category.png","bar_monthly_orders.png"]:
    print(f"  --> {f}")
print("\nOpen these PNG files to view your charts.")
print("Go to your folder and double-click any PNG file to open it.")