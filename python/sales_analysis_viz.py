#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the sales data into a pandas DataFrame
sales_data = pd.read_csv('sales_data.csv')

# Basic data analysis
# Basic summary of data
print(sales_data.describe())
# Check for missing values
print(sales_data.isnull().sum())

# Top 10 products by sales quantity
top_products = sales_data.groupby('product_name').sum()['quantity_ordered'].sort_values(ascending=False).head(10)
print("Top 10 Products by Quantity Ordered:")
print(top_products)

# Total sales per month
sales_data['Month'] = pd.to_datetime(sales_data['order_date']).dt.month
monthly_sales = sales_data.groupby('Month').sum()['sales']
print("Total Sales Per Month:")
print(monthly_sales)

# Data Visualization
# Setting up the visualisation environment
sns.set(style="whitegrid")

# Sales by month
plt.figure(figsize=(10, 6))
sns.barplot(x=monthly_sales.index, y=monthly_sales.values)
plt.title('Total Sales by Month')
plt.xlabel('Month')
plt.ylabel('Sales in USD')
plt.show()

# Quantity ordered by product
plt.figure(figsize=(12, 7))
top_products.plot(kind='bar')
plt.title('Top 10 Products by Quantity Ordered')
plt.xlabel('Product Name')
plt.ylabel('Quantity Ordered')
plt.xticks(rotation=75)
plt.show()

# Sales per category
category_sales = sales_data.groupby('category').sum()['sales'].sort_values(ascending=False)
plt.figure(figsize=(10, 6))
category_sales.plot(kind='pie', autopct='%1.1f%%')
plt.title('Sales Distribution by Category')
plt.ylabel('')
plt.show()

# Heatmap of sales by day of week and hour of day
sales_data['Hour'] = pd.to_datetime(sales_data['order_date']).dt.hour
sales_data['DayOfWeek'] = pd.to_datetime(sales_data['order_date']).dt.dayofweek
day_hour = sales_data.groupby(['DayOfWeek', 'Hour']).sum()['sales'].unstack()
plt.figure(figsize=(12, 6))
sns.heatmap(day_hour, cmap='viridis')
plt.title('Sales Heatmap by Day of Week and Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.show()

# Note: Please ensure the columns like 'order_date', 'product_name', 'quantity_ordered',
# 'sales', and 'category' exist in your 'sales_data.csv' file for the above script to work properly.
