#!/usr/bin/env python3

import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Define the ticker symbol and the time frame for which you want to fetch data
ticker_symbol = 'AAPL'  # Apple Inc.
start_date = '2020-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

# Download historical data for the specified ticker
def download_data(ticker_symbol, start_date, end_date):
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data

# Calculate moving averages
def calculate_moving_averages(data, window=50):
    data['MA50'] = data['Close'].rolling(window=window).mean()
    return data

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data['RSI'] = rsi
    return data

# Generate a plot with moving averages and closing price
def plot_data(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Close'], label='Closing Price', color='blue')
    plt.plot(data.index, data['MA50'], label='50-day Moving Average', color='red')
    plt.title(f'{ticker_symbol} Stock Price and Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price in $')
    plt.legend()
    plt.show()

# Main function to execute the analysis
def main():
    data = download_data(ticker_symbol, start_date, end_date)
    data_with_ma = calculate_moving_averages(data)
    data_with_rsi = calculate_rsi(data_with_ma)
    
    plot_data(data_with_rsi)

if __name__ == "__main__":
    main()
