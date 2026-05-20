
#Generates realistic synthetic sales dataset (multi-table) for analysis.

import pandas as pd
import numpy as np
import os

np.random.seed(42)

N_ORDERS = 5000
START_DATE = "2022-01-01"
END_DATE   = "2024-12-31"

REGIONS   = ["North", "South", "East", "West", "Central"]
CHANNELS  = ["Online", "Retail", "Wholesale", "Direct Sales"]
CATEGORIES = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch"],
    "Furniture":   ["Office Chair", "Standing Desk", "Bookshelf", "Sofa", "Lamp"],
    "Clothing":    ["Jacket", "Sneakers", "T-Shirt", "Jeans", "Hoodie"],
    "Food & Bev":  ["Coffee Beans", "Energy Drink", "Protein Bar", "Tea Pack", "Juice"],
}

# Products Table 
products = []
pid = 1
for cat, items in CATEGORIES.items():
    for item in items:
        cost   = round(np.random.uniform(10, 400), 2)
        price  = round(cost * np.random.uniform(1.3, 2.5), 2)
        products.append({
            "product_id":   f"P{pid:03d}",
            "product_name": item,
            "category":     cat,
            "unit_cost":    cost,
            "unit_price":   price,
        })
        pid += 1

products_df = pd.DataFrame(products)

#  Customers Table
first_names = ["Aarav","Priya","Rahul","Sneha","Vikram","Anjali","Rohan","Nisha",
               "Arjun","Pooja","Karan","Meera","Dev","Riya","Siddharth","Ananya"]
last_names  = ["Sharma","Patel","Gupta","Singh","Kumar","Joshi","Mehta","Verma",
               "Rao","Nair","Iyer","Malhotra","Bose","Das","Reddy","Chopra"]

customers = []
for i in range(1, 501):
    customers.append({
        "customer_id":   f"C{i:04d}",
        "customer_name": f"{np.random.choice(first_names)} {np.random.choice(last_names)}",
        "region":        np.random.choice(REGIONS, p=[0.25,0.20,0.20,0.20,0.15]),
        "customer_segment": np.random.choice(
            ["Enterprise","SMB","Individual"], p=[0.20,0.35,0.45]
        ),
    })

customers_df = pd.DataFrame(customers)

#  Orders Tabl
dates = pd.date_range(START_DATE, END_DATE, freq="D")

orders = []
for i in range(1, N_ORDERS + 1):
    date      = np.random.choice(dates)
    customer  = customers_df.sample(1).iloc[0]
    product   = products_df.sample(1).iloc[0]
    qty       = int(np.random.choice([1,2,3,4,5], p=[0.45,0.25,0.15,0.10,0.05]))
    discount  = round(np.random.choice([0,0.05,0.10,0.15,0.20], p=[0.50,0.20,0.15,0.10,0.05]), 2)
    channel   = np.random.choice(CHANNELS, p=[0.35,0.30,0.20,0.15])

    revenue   = round(product["unit_price"] * qty * (1 - discount), 2)
    cost      = round(product["unit_cost"]  * qty, 2)
    profit    = round(revenue - cost, 2)

    orders.append({
        "order_id":    f"ORD{i:05d}",
        "order_date":  date,
        "customer_id": customer["customer_id"],
        "product_id":  product["product_id"],
        "quantity":    qty,
        "discount":    discount,
        "channel":     channel,
        "revenue":     revenue,
        "cost":        cost,
        "profit":      profit,
    })

orders_df = pd.DataFrame(orders).sort_values("order_date").reset_index(drop=True)

#  Save 
out = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(out, exist_ok=True)

products_df.to_csv(f"{out}/products.csv",   index=False)
customers_df.to_csv(f"{out}/customers.csv", index=False)
orders_df.to_csv(f"{out}/orders.csv",       index=False)

print(f"  Generated {len(orders_df)} orders | {len(customers_df)} customers | {len(products_df)} products")
print(f"    Saved to {os.path.abspath(out)}")
