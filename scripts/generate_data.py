import os
import sqlite3
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Ensure the 'data' folder exists
os.makedirs("data", exist_ok=True)

# Build the path to the database file
db_path = os.path.join(os.path.dirname(__file__), "../data/sales_data.db")

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute("DROP TABLE IF EXISTS Suppliers")
cursor.execute("DROP TABLE IF EXISTS Products")
cursor.execute("DROP TABLE IF EXISTS Sales")

cursor.execute("""
CREATE TABLE Suppliers (
    SupplierID INTEGER PRIMARY KEY,
    SupplierName TEXT NOT NULL,
    Region TEXT NOT NULL,
    ContactEmail TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT NOT NULL,
    Category TEXT NOT NULL,
    SupplierID INTEGER,
    PricePerUnit REAL NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
)
""")

cursor.execute("""
CREATE TABLE Sales (
    SaleID INTEGER PRIMARY KEY,
    ProductID INTEGER,
    SaleDate TEXT NOT NULL,
    Quantity INTEGER NOT NULL,
    TotalAmount REAL NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
)
""")

# Generate fake suppliers
suppliers = []
for _ in range(10):  # 10 suppliers
    suppliers.append((
        fake.company(),
        fake.state(),
        fake.email()
    ))
cursor.executemany("INSERT INTO Suppliers (SupplierName, Region, ContactEmail) VALUES (?, ?, ?)", suppliers)

# Generate fake products
categories = ["Beer", "Wine", "Spirits"]
products = []
for supplier_id in range(1, 11):  # Each supplier gets 5 products
    for _ in range(5):
        products.append((
            fake.word().capitalize() + " " + random.choice(categories),
            random.choice(categories),
            supplier_id,
            round(random.uniform(5, 50), 2)  # Price between $5 and $50
        ))
cursor.executemany("INSERT INTO Products (ProductName, Category, SupplierID, PricePerUnit) VALUES (?, ?, ?, ?)", products)

# Generate fake sales
sales = []
for _ in range(500):  # 500 sales transactions
    product_id = random.randint(1, 50)  # 50 products total
    quantity = random.randint(1, 20)  # Quantity between 1 and 20
    price_per_unit = cursor.execute("SELECT PricePerUnit FROM Products WHERE ProductID = ?", (product_id,)).fetchone()[0]
    total_amount = round(price_per_unit * quantity, 2)
    sales.append((
        product_id,
        fake.date_between(start_date="-1y", end_date="today").isoformat(),
        quantity,
        total_amount
    ))
cursor.executemany("INSERT INTO Sales (ProductID, SaleDate, Quantity, TotalAmount) VALUES (?, ?, ?, ?)", sales)

# Commit and close
conn.commit()
conn.close()
print("Fake data generated and saved to 'sales_data.db'")