#!/usr/bin/env python3

import csv
from datetime import datetime

# Define the inventory file and order file
inventory_file = 'inventory.csv'
order_file = 'orders_to_place.csv'

# Define thresholds and restock levels
restock_threshold = 10  # The minimum amount before restocking
restock_level = 25      # The amount to restock to

# Inventory tracking and ordering function
def check_inventory_and_create_orders(inventory_file, order_file, restock_threshold, restock_level):
    inventory_to_restock = []

    # Read the inventory file
    with open(inventory_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if int(row['Quantity']) < restock_threshold:
                restock_amount = restock_level - int(row['Quantity'])
                inventory_to_restock.append({'Product ID': row['Product ID'], 'Product Name': row['Product Name'], 'Quantity to Order': restock_amount})

    # Write to the order file if restocking needed
    if inventory_to_restock:
        with open(order_file, mode='w', newline='') as file:
            fieldnames = ['Product ID', 'Product Name', 'Quantity to Order', 'Order Date']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for item in inventory_to_restock:
                item['Order Date'] = datetime.now().strftime('%Y-%m-%d')
                csv_writer.writerow(item)
        print(f"Order file '{order_file}' has been updated with restock orders.")
    else:
        print("No restocking required at this time.")

# Execute the function
if __name__ == "__main__":
    check_inventory_and_create_orders(inventory_file, order_file, restock_threshold, restock_level)
