#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import numpy as np

# Load dataset
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Clean dataset
def clean_and_preprocess(data):
    # Example of dropping columns with too many missing values
    missing_threshold = 0.6
    data = data.dropna(thresh=int(missing_threshold * len(data)), axis=1)

    # Example of replacing outliers with median values
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR
        data[col] = np.where((data[col] > upper_bound) | (data[col] < lower_bound), 
                                data[col].median(), data[col])
    
    # Fill missing values for numeric data
    numeric_features = data.select_dtypes(include=['int64', 'float64']).columns
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    # Fill missing values and encode categorical data
    categorical_features = data.select_dtypes(include=['object', 'bool']).columns
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    # Create a column transformer to apply the transformations to the correct columns in the dataframe
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    # Apply the transformations
    data = preprocessor.fit_transform(data)
    
    return data

def main():
    # Change the path to where your dataset is located
    file_path = 'path_to_your_dataset.csv'
    data = load_data(file_path)
    cleaned_data = clean_and_preprocess(data)

    # You could then split the data into training and testing sets
    X_train, X_test = train_test_split(cleaned_data, test_size=0.2, random_state=42)

    # Do additional operations with X_train and X_test as needed
    # ...

if __name__ == '__main__':
    main()
