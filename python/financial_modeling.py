#!/usr/bin/env python3
import numpy_financial as npf
import pandas as pd

def build_financial_projections(
    starting_revenue,
    revenue_growth_rate,
    gross_margin,
    operating_margin,
    tax_rate,
    initial_investments,
    capex_percentage_of_revenue,
    working_capital_change,
    depreciation_amortization_percentage_of_revenue,
    forecast_years
):
    index = pd.date_range(start=pd.Timestamp('today').normalize(), periods=forecast_years, freq='Y')
    projections = pd.DataFrame(index=index, columns=[
        'Revenue',
        'Cost of Goods Sold',
        'Gross Profit',
        'Operating Expenses',
        'Operating Income',
        'Taxes',
        'Net Income',
        'CapEx',
        'Working Capital Change',
        'Depreciation & Amortization',
        'Cash Flow'
    ])
    
    revenue = starting_revenue
    for year in range(forecast_years):
        # Revenue
        projections.at[index[year], 'Revenue'] = revenue
        
        # Cost of Goods Sold
        cogs = revenue * (1 - gross_margin)
        projections.at[index[year], 'Cost of Goods Sold'] = cogs
        
        # Gross Profit
        gross_profit = revenue * gross_margin
        projections.at[index[year], 'Gross Profit'] = gross_profit
        
        # Operating Expenses
        operating_expenses = revenue * (1 - operating_margin)
        projections.at[index[year], 'Operating Expenses'] = operating_expenses
        
        # Operating Income
        operating_income = gross_profit - operating_expenses
        projections.at[index[year], 'Operating Income'] = operating_income
        
        # Taxes
        taxes = operating_income * tax_rate
        projections.at[index[year], 'Taxes'] = taxes
        
        # Net Income
        net_income = operating_income - taxes
        projections.at[index[year], 'Net Income'] = net_income
        
        # CapEx
        capex = revenue * capex_percentage_of_revenue
        projections.at[index[year], 'CapEx'] = capex
        
        # Working Capital Change
        working_capital = revenue * working_capital_change
        projections.at[index[year], 'Working Capital Change'] = working_capital
        
        # Depreciation & Amortization
        depreciation_amortization = revenue * depreciation_amortization_percentage_of_revenue
        projections.at[index[year], 'Depreciation & Amortization'] = depreciation_amortization
        
        # Cash Flow
        cash_flow = net_income - capex - working_capital + depreciation_amortization
        projections.at[index[year], 'Cash Flow'] = cash_flow
        
        # Next Year's Revenue
        revenue *= (1 + revenue_growth_rate)

    return projections

# Adjust these variables as needed
starting_revenue = 1e6  # starting revenue
revenue_growth_rate = 0.1  # 10% growth rate
gross_margin = 0.6  # 60% gross margin
operating_margin = 0.15  # 15% operating margin
tax_rate = 0.3  # 30% tax rate
initial_investments = 1e5  # initial investment
capex_percentage_of_revenue = 0.05  # 5% of revenue
working_capital_change = 0.1  # change in working capital
depreciation_amortization_percentage_of_revenue = 0.02  # 2% of revenue
forecast_years = 5  # 5 years forecast

# Build the financial projections
projections = build_financial_projections(
    starting_revenue,
    revenue_growth_rate,
    gross_margin,
    operating_margin,
    tax_rate,
    initial_investments,
    capex_percentage_of_revenue,
    working_capital_change,
    depreciation_amortization_percentage_of_revenue,
    forecast_years
)

# Output to console or use projections as needed
print(projections)