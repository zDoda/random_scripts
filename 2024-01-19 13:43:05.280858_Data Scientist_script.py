Here's a basic python script for a data scientist to get started with data analysis and visualization using popular libraries like pandas and matplotlib:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Reading data from a CSV file
data = pd.read_csv('data.csv')

# Exploring the data
print(data.head())  # Display the first few rows of the dataset
print(data.describe())  # Summary statistics for the numerical columns
print(data.info())  # Information about the dataset

# Data visualization
plt.figure(figsize=(10, 6))
plt.scatter(data['x'], data['y'])
plt.title('Scatter Plot of x vs y')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
```

In this script, we are using the pandas library to read data from a CSV file into a DataFrame, and then exploring the data using various pandas functions like head(), describe(), and info(). We are also using matplotlib to create a simple scatter plot of two columns ('x' and 'y') from the dataset. 

You can customize and expand this script based on your specific data analysis requirements and dataset.