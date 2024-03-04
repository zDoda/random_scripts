#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import datetime as dt

# Define time frame for the report
start_date = dt.datetime.now() - dt.timedelta(days=365)
end_date = dt.datetime.now()

# Financial data to fetch (e.g., stock symbols)
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Create an empty DataFrame to store fetched financial data
financial_data = pd.DataFrame()

# Fetch financial data
for ticker in tickers:
    financial_data[ticker] = web.DataReader(ticker, data_source='yahoo', start=start_date, end=end_date)['Close']

# Generate descriptive statistics report
stats_report = financial_data.describe()

# Save statistics report to Excel file
stats_report.to_excel('financial_report_statistics.xlsx')

# Generate and save plots for each stock
for ticker in tickers:
    plt.figure(figsize=(10, 5))
    plt.plot(financial_data.index, financial_data[ticker])
    plt.title(f'Stock Price of {ticker} Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.savefig(f'stock_price_{ticker}.png')

# Generating a correlation matrix
correlation_matrix = financial_data.corr()
correlation_matrix.to_excel('financial_report_correlation.xlsx')

# Example of more advanced financial analysis can be added here (e.g., moving average)

print("Financial report generation complete.")
