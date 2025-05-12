import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns




"""

To run the dashboard, use the following command in your terminal:
streamlit run sales_dashboard.py

Make sure you change to the directory where the script is located, in this case the path is:
dashboards\sales_dashboard.py

"""

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

# Add Regional Sales to the Dashboard
st.subheader("Total Sales by Region and Drink Type")
query = """
SELECT 
    sp.Region AS Region,
    p.Category AS DrinkType,
    SUM(s.TotalAmount) AS TotalSales
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Suppliers sp ON p.SupplierID = sp.SupplierID
GROUP BY Region, DrinkType
ORDER BY Region, DrinkType;
"""
df_region_drink = get_data(query)

# Create a bar chart grouped by Region and Drink Type
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_region_drink, x="Region", y="TotalSales", hue="DrinkType", ax=ax)
ax.set_title("Total Sales by Region and Drink Type")
ax.set_ylabel("Total Sales ($)")
ax.set_xlabel("Region")
ax.legend(title="Drink Type")
plt.xticks(rotation=45)

# Display the chart in Streamlit
st.pyplot(fig)


# Add Total Sales by Day of the Week and Drink Type to the Dashboard
st.subheader("Total Sales by Day of the Week and Drink Type")
query = """
SELECT 
    CASE strftime('%w', s.SaleDate)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END AS DayOfWeek,
    p.Category AS DrinkType,
    SUM(s.TotalAmount) AS TotalSales
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
GROUP BY DayOfWeek, DrinkType
ORDER BY 
    CASE strftime('%w', s.SaleDate)
        WHEN '1' THEN 1
        WHEN '2' THEN 2
        WHEN '3' THEN 3
        WHEN '4' THEN 4
        WHEN '5' THEN 5
        WHEN '6' THEN 6
        WHEN '0' THEN 7
    END,
    DrinkType
"""
df_day_drink = get_data(query)

# Create a bar chart grouped by Day of the Week and Drink Type
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_day_drink, x="DayOfWeek", y="TotalSales", hue="DrinkType", ax=ax)
ax.set_title("Total Sales by Day of the Week and Drink Type")
ax.set_ylabel("Total Sales ($)")
ax.set_xlabel("Day of the Week")
ax.legend(title="Drink Type")
plt.xticks(rotation=45)

# Display the chart in Streamlit
st.pyplot(fig)