import sqlite3, pandas as pd, random
from datetime import datetime, timedelta
random.seed(42)

def random_date(start, end):
    return start + timedelta(days=random.randint(0,(end-start).days))

cities  = ["Mumbai","Delhi","Bangalore","Hyderabad","Chennai","Kolkata","Pune","Ahmedabad","Jaipur","Lucknow"]
genders = ["Male","Female","Other"]
customers = []
for i in range(1,201):
    signup = random_date(datetime(2021,1,1), datetime(2023,12,31))
    customers.append({"customer_id":i,"name":f"Customer_{i}","age":random.randint(18,65),"city":random.choice(cities),"gender":random.choice(genders),"signup_date":signup.strftime("%Y-%m-%d")})

product_names = {
    "Electronics":["Laptop","Smartphone","Headphones","Smartwatch","Tablet","Camera","Speaker","Keyboard","Mouse","Monitor"],
    "Clothing":["T-Shirt","Jeans","Dress","Jacket","Saree","Kurta","Shorts","Hoodie","Blazer","Leggings"],
    "Home & Kitchen":["Mixer","Pressure Cooker","Bed Sheet","Pillow","Curtain","Air Fryer","Toaster","Iron","Vacuum Cleaner","Water Purifier"],
    "Books":["Fiction Novel","Self Help","Biography","Science Book","History Book"],
    "Sports":["Cricket Bat","Football","Yoga Mat","Dumbbells","Cycling Helmet"],
    "Beauty":["Face Cream","Shampoo","Perfume","Lipstick","Sunscreen"],
    "Toys":["Lego Set","Board Game","Action Figure","Puzzle","Remote Car"],
    "Grocery":["Rice 5kg","Cooking Oil","Atta 10kg","Tea Powder","Coffee Powder"]
}
products = []
pid = 1
for cat, names in product_names.items():
    for name in names:
        cost  = round(random.uniform(100,8000),2)
        price = round(cost * random.uniform(1.2,2.5),2)
        products.append({"product_id":pid,"name":name,"category":cat,"price":price,"cost_price":cost})
        pid += 1

statuses = ["Completed","Completed","Completed","Pending","Cancelled"]
orders = []
for i in range(1,501):
    order_date = random_date(datetime(2023,1,1), datetime(2023,12,31))
    orders.append({"order_id":i,"customer_id":random.randint(1,200),"order_date":order_date.strftime("%Y-%m-%d"),"status":random.choice(statuses)})

order_items = []
item_id = 1
for order in orders:
    for p in random.sample(products, random.randint(1,4)):
        qty = random.randint(1,5)
        order_items.append({"item_id":item_id,"order_id":order["order_id"],"product_id":p["product_id"],"quantity":qty,"unit_price":p["price"]})
        item_id += 1

conn = sqlite3.connect("ecommerce.db")
cur  = conn.cursor()
for tbl in ["order_items","orders","products","customers"]:
    cur.execute(f"DROP TABLE IF EXISTS {tbl}")
cur.executescript("""
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, city TEXT, gender TEXT, signup_date TEXT);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL, cost_price REAL);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT);
CREATE TABLE order_items (item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price REAL);
""")
pd.DataFrame(customers).to_sql("customers",   conn, if_exists="append", index=False)
pd.DataFrame(products).to_sql("products",     conn, if_exists="append", index=False)
pd.DataFrame(orders).to_sql("orders",         conn, if_exists="append", index=False)
pd.DataFrame(order_items).to_sql("order_items", conn, if_exists="append", index=False)
conn.commit()
print("Database created successfully!")
for tbl in ["customers","products","orders","order_items"]:
    count = pd.read_sql(f"SELECT COUNT(*) as total FROM {tbl}", conn).iloc[0,0]
    print(f"  {tbl:<15} -> {count} rows")
conn.close()
print("Phase 1 DONE - ecommerce.db file created in your folder!")