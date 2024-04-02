#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime

# Define a list of stocks for the portfolio
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Define the start and end date for historical data
start_date = datetime.datetime.now() - datetime.timedelta(days=365)
end_date = datetime.datetime.now()

# Fetch the stock data using pandas_datareader
def get_stock_data(tickers, start, end):
    stock_data = {}
    for ticker in tickers:
        stock_data[ticker] = pdr.get_data_yahoo(ticker, start, end)
    return stock_data

# Calculate daily returns
def calculate_daily_returns(stock_data):
    stock_returns = {}
    for ticker in stock_data.keys():
        stock_returns[ticker] = stock_data[ticker]['Adj Close'].pct_change().dropna()
    return pd.DataFrame(stock_returns)

# Calculate portfolio performance
def calculate_portfolio_performance(daily_returns, weights):
    weighted_returns = daily_returns * weights
    portfolio_returns = weighted_returns.sum(axis=1)
    return portfolio_returns

# Risk assessment using the portfolio standard deviation
def assess_portfolio_risk(portfolio_returns):
    return portfolio_returns.std()

# Optimize Portfolio
def optimize_portfolio(daily_returns):
    # Portfolio optimization (Minimum Volatility Portfolio)
    num_assets = len(daily_returns.columns)
    args = (daily_returns.mean(), daily_returns.cov(), num_assets)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    
    initial_guess = num_assets * [1. / num_assets,]
    opt_results = minimize(
        lambda x: -sharpe_ratio(x, *args), 
        initial_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    return opt_results.x

# Sharpe ratio is a measure for calculating risk-adjusted return
def sharpe_ratio(weights, mean_returns, covariance, risk_free_rate=0.01):
    portfolio_return = np.sum(mean_returns * weights) * 252
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(covariance, weights))) * np.sqrt(252)
    return (portfolio_return - risk_free_rate) / portfolio_std

# Main program logic
if __name__ == '__main__':
    # Fetch stock data
    stock_data = get_stock_data(stocks, start_date, end_date)

    # Calculate daily returns
    daily_returns = calculate_daily_returns(stock_data)

    # Set initial portfolio weights, for example equally distributed
    portfolio_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

    # Calculate portfolio returns
    portfolio_returns = calculate_portfolio_performance(daily_returns, portfolio_weights)

    # Assess risk
    portfolio_risk = assess_portfolio_risk(portfolio_returns)

    # Find the optimal portfolio
    from scipy.optimize import minimize
    optimal_weights = optimize_portfolio(daily_returns)

    # Print the results
    print('Optimal portfolio weights:', optimal_weights)
    print('Portfolio risk (standard deviation):', portfolio_risk)
