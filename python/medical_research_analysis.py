#!/usr/bin/env python3

import pandas as pd
import numpy as np
from scipy import stats

# Replace 'data.csv' with the path to the dataset you want to analyze
DATA_PATH = 'data.csv'

def load_data(path):
    """Load the dataset from the specified path."""
    return pd.read_csv(path)

def describe_data(df):
    """Provide basic statistics for the dataset."""
    return df.describe()

def normality_test(df, column_name):
    """Test if the data in a specific column is normally distributed."""
    data = df[column_name]
    k2, p = stats.normaltest(data)
    alpha = 1e-3
    print(f"Normality test for {column_name}:")
    print(f"Statistics={k2:.3f}, p={p:.3f}")
    if p < alpha:  # null hypothesis: data comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")

def t_test(df, column1, column2):
    """Perform a T-test on two independent samples."""
    data1 = df[column1]
    data2 = df[column2]
    stat, p = stats.ttest_ind(data1, data2)
    print(f"T-test between {column1} and {column2}:")
    print(f"Statistics={stat:.3f}, p={p:.3f}")

def correlation_analysis(df, column1, column2):
    """Perform correlation analysis between two columns."""
    correlation_coefficient, p_value = stats.pearsonr(df[column1], df[column2])
    print(f"Pearson correlation between {column1} and {column2}:")
    print(f"Correlation Coefficient={correlation_coefficient:.3f}, p-value={p_value:.3f}")

def main():
    # Load the dataset
    df = load_data(DATA_PATH)

    # Descriptive statistics
    stats_summary = describe_data(df)
    print("Descriptive Statistics:")
    print(stats_summary)
    
    # Normality tests on each numerical column
    for column in df.select_dtypes(include=[np.number]).columns:
        normality_test(df, column)

    # Two sample T-tests
    # NOTE: Replace 'Age' and 'BloodPressure' with actual column names you are interested in
    t_test(df, 'Age', 'BloodPressure')

    # Correlation analysis
    # NOTE: Replace 'Cholesterol' and 'BloodPressure' with actual column names you are interested in
    correlation_analysis(df, 'Cholesterol', 'BloodPressure')

if __name__ == "__main__":
    main()
