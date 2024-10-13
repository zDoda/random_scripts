import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os  # For handling directories

# Read the CSV file
df = pd.read_csv('class.csv')

# Display the initial DataFrame
print("Initial Data:")
print(df)

# Define years
years = list(range(2018, 2025))  # 2018 to 2024

# Function to generate intermediate values
def generate_values(start, end, num_years=7):
    # Generate intermediate values using linear interpolation
    middle_values = np.linspace(start, end, num=num_years)
    # Add small random noise
    noise = np.random.uniform(-10, 10, size=num_years)
    values = middle_values + noise
    # Ensure values don't fluctuate too much
    values = np.clip(values, min(start, end) - 20, max(start, end) + 20)
    values[0] = start
    values[-1] = end
    return values

# Set a random seed for reproducibility
np.random.seed(123)

# Generate values for each stock
all_values = []
for index, row in df.iterrows():
    stock = row['Stock']
    start_value = row['2018']
    end_value = row['2024']
    values = generate_values(start_value, end_value)
    all_values.append([stock] + values.tolist())

# Create a new DataFrame with all years
columns = ['Stock'] + years
df_full = pd.DataFrame(all_values, columns=columns)

# Display the full DataFrame
print("\nData with Intermediate Years:")
print(df_full)

# Directory to save the graphs
output_dir = 'stock_graphs'

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\nCreated directory '{output_dir}' for saving graphs.")
else:
    print(f"\nDirectory '{output_dir}' already exists.")

# Plot individual graphs and save them as images
for index, row in df_full.iterrows():
    plt.figure(figsize=(10, 6))
    plt.plot(years, row[1:], marker='o', linestyle='-')
    plt.title(f"Stock Prices of {row['Stock']} (2018-2024)")
    plt.xlabel('Year')
    plt.ylabel('Stock Price')
    plt.grid(True)
    plt.xticks(years)
    
    # Save the plot as an image
    # Replace spaces and special characters in the stock name for the filename
    filename = ''.join(e for e in row['Stock'] if e.isalnum() or e == ' ').replace(' ', '_')
    filepath = os.path.join(output_dir, f"{filename}.png")
    plt.savefig(filepath)
    plt.close()  # Close the figure to free memory
    print(f"Saved graph for '{row['Stock']}' as '{filepath}'.")

# Plot overall graph
plt.figure(figsize=(12, 7))

for index, row in df_full.iterrows():
    plt.plot(years, row[1:], marker='o', linestyle='-', label=row['Stock'])

plt.title("Individual T&V 500 Prices Comparison (2018-2024)")
plt.xlabel('Year')
plt.ylabel('Stock Price')
plt.grid(True)
plt.xticks(years)

# Save the overall graph as an image
overall_graph_path = os.path.join(output_dir, "Overall_Stock_Prices.png")
plt.savefig(overall_graph_path)
print(f"\nSaved overall stock prices graph as '{overall_graph_path}'.")

# Display the overall graph
plt.show()

total_values_per_year = df_full[years].sum(axis=0)

# Plot the total stock values over time
plt.figure(figsize=(12, 7))
plt.plot(years, total_values_per_year, marker='o', linestyle='-', color='green')

plt.title("T&V 500 Total Stock Prices Over Time (2018-2024)")
plt.xlabel('Year')
plt.ylabel('T&V 500 Stock Price')
plt.grid(True)
plt.xticks(years)

# Save the cumulative total graph as an image
cumulative_total_graph_path = os.path.join(output_dir, "TV500_Prices.png")
plt.savefig(cumulative_total_graph_path)
print(f"\nT&V 500 prices graph as '{cumulative_total_graph_path}'.")

# Display the cumulative total graph
plt.show()
