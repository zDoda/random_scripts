Sure, here's an example of a Python script for a financial analyst that calculates some basic financial metrics:

```python
# Importing necessary libraries
import pandas as pd

# Reading the data from a CSV file
data = pd.read_csv('financial_data.csv')

# Calculating the average revenue
average_revenue = data['revenue'].mean()

# Calculating the total expenses
total_expenses = data['expenses'].sum()

# Calculating the net profit
net_profit = average_revenue - total_expenses

# Calculating the profit margin
profit_margin = (net_profit / average_revenue) * 100

# Displaying the results
print('Average Revenue:', average_revenue)
print('Total Expenses:', total_expenses)
print('Net Profit:', net_profit)
print('Profit Margin:', profit_margin)
```

This script assumes that you have a CSV file named 'financial_data.csv' with columns for revenue and expenses. Adjust the script according to your specific data and requirements.