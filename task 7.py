import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# STEP 1: Create Database & Table
# ------------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Drop table if exists (so script can be rerun)
cursor.execute("DROP TABLE IF EXISTS sales")

cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# ------------------------------
# STEP 2: Insert Sample Data
# ------------------------------
sample_data = [
    ("Laptop", 5, 60000),
    ("Laptop", 3, 60000),
    ("Phone", 10, 15000),
    ("Phone", 8, 15000),
    ("Headphones", 15, 2000),
    ("Headphones", 20, 2000),
    ("Tablet", 7, 25000),
    ("Tablet", 5, 25000),
]

cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# ------------------------------
# STEP 3: Run SQL Query
# ------------------------------
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# ------------------------------
# STEP 4: Print Results
# ------------------------------
print("📊 Sales Summary:")
print(df)

# ------------------------------
# STEP 5: Plot Bar Chart
# ------------------------------
df.plot(kind="bar", x="product", y="revenue", legend=False, color="skyblue")
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("sales_chart.png")  # saves chart
plt.show()

# ------------------------------
# STEP 6: Close Connection
# ------------------------------
conn.close()
