import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set up Streamlit page
st.title("Sales Dashboard")
st.sidebar.header("Filters")

# Connect to the database
def get_data(query):
    with sqlite3.connect("../data/sales_data.db") as conn:
        return pd.read_sql_query(query, conn)

# Total Sales by Category
st.subheader("Total Sales by Category")
query = """
SELECT p.Category, SUM(s.TotalAmount) AS TotalSales
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY TotalSales DESC
"""
df_category = get_data(query)
st.bar_chart(df_category.set_index("Category"))

# Total Sales by Month
st.subheader("Total Sales by Month")
query = """
SELECT strftime('%Y-%m', s.SaleDate) AS Month, SUM(s.TotalAmount) AS TotalSales
FROM Sales s
GROUP BY Month
ORDER BY Month
"""
df_month = get_data(query)
st.line_chart(df_month.set_index("Month"))

# Total Sales by Supplier
st.subheader("Total Sales by Supplier")
query = """
SELECT sp.SupplierName, SUM(s.TotalAmount) AS TotalSales
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Suppliers sp ON p.SupplierID = sp.SupplierID
GROUP BY sp.SupplierName
ORDER BY TotalSales DESC
"""
df_supplier = get_data(query)
st.dataframe(df_supplier)

# Rolling 7-Day Sales
st.subheader("Rolling 7-Day Sales")
query = """
SELECT s.SaleDate, SUM(s.TotalAmount) AS DailySales
FROM Sales s
GROUP BY s.SaleDate
ORDER BY s.SaleDate
"""
df_daily = get_data(query)
df_daily["SaleDate"] = pd.to_datetime(df_daily["SaleDate"])
df_daily["Rolling7DaySales"] = df_daily["DailySales"].rolling(window=7).sum()
st.line_chart(df_daily.set_index("SaleDate")["Rolling7DaySales"])