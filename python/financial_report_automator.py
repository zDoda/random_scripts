#!/usr/bin/env python3
import pandas as pd
from openpyxl import load_workbook
import datetime

def generate_financial_report(financial_data_csv, template_xlsx, output_xlsx):
    # Load financial data from CSV file
    financial_data = pd.read_csv(financial_data_csv)

    # Calculate summary metrics
    total_revenue = financial_data['Revenue'].sum()
    total_expense = financial_data['Expenses'].sum()
    net_income = total_revenue - total_expense

    # Load Excel report template
    workbook = load_workbook(template_xlsx)
    sheet = workbook.active

    # Write calculated metrics to the report
    sheet['B2'] = datetime.date.today().strftime('%Y-%m-%d')  # Report Date
    sheet['B3'] = total_revenue  # Total Revenue
    sheet['B4'] = total_expense  # Total Expenses
    sheet['B5'] = net_income  # Net Income

    # Save the report to a new file
    workbook.save(output_xlsx)

    print(f"Report generated: {output_xlsx}")


# Example Usage
financial_data_csv = 'financial_data.csv'  # Your financial data CSV file path
template_xlsx = 'financial_report_template.xlsx'  # Your Excel template file path
output_xlsx = f'financial_report_{datetime.date.today().strftime("%Y%m%d")}.xlsx'  # Output file path
generate_financial_report(financial_data_csv, template_xlsx, output_xlsx)
