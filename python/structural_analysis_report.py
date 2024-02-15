#!/usr/bin/env python3

import numpy as np
import pandas as pd

# Function to perform structural analysis on a dataframe
def structural_analysis(df):
    # Analysis report dictionary
    analysis_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'column_details': {}
    }
    
    # Iterate through each column for details
    for col in df.columns:
        col_data = df[col]
        col_details = {
            'non_null_count': col_data.notnull().sum(),
            'null_count': col_data.isnull().sum(),
            'unique_values': len(col_data.unique()),
            'data_type': col_data.dtypes,
            'sample_values': col_data.dropna().sample(min(5, len(col_data))).tolist()
        }
        analysis_report['column_details'][col] = col_details
    
    return analysis_report

# Function to pretty print the report
def print_report(report):
    print(f"Total Rows: {report['total_rows']}")
    print(f"Total Columns: {report['total_columns']}")
    print("\nColumn Details:")
    for col, details in report['column_details'].items():
        print(f"Column: {col}")
        for key, value in details.items():
            print(f"  {key.replace('_', ' ').capitalize()}: {value}")
        print("")

# Example usage
if __name__ == '__main__':
    # Sample dataframe creation
    data = {
        'A': [1, 2, 3, np.nan, 5],
        'B': ['a', 'b', 'c', 'd', 'e'],
        'C': [1.1, np.nan, 3.3, 4.4, 5.5]
    }
    sample_df = pd.DataFrame(data)
    
    # Perform structural analysis
    report = structural_analysis(sample_df)
    
    # Print the report
    print_report(report)
