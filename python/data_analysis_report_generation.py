#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
from pandas_profiling import ProfileReport

# Load your dataset
# Replace 'data.csv' with your own data file, make sure the path is correct
data = pd.read_csv('data.csv')

# Generate a basic report using pandas profiling
profile = ProfileReport(data, title='Pandas Profiling Report', explorative=True)

# Save the report to an HTML file
profile.to_file("data_analysis_report.html")

# Example of simple data analysis: describe the data and plot figures

# Describe the data
summary = data.describe()
summary.to_csv('data_summary.csv')

# Plot and save figures
for column in data.select_dtypes(include=['number']).columns:
    plt.figure()
    data[column].hist()
    plt.title(column)
    plt.savefig(f'{column}_histogram.png')

# This is a basic template. You would need to customize the analysis
# depending on the nature of your data and the requirements of your report