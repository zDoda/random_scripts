#!/usr/bin/env python3
import csv
import os

# Define the inventory file path
INVENTORY_FILE = 'inventory.csv'

# Inventory fields: Part ID, Part Name, Material, Quantity
INVENTORY_FIELDS = ['Part ID', 'Part Name', 'Material', 'Quantity']

# Check if inventory file exists, if not, create it
if not os.path.exists(INVENTORY_FILE):
    with open(INVENTORY_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()


def add_part(part_id, part_name, material, quantity):
    with open(INVENTORY_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=INVENTORY_FIELDS)
        writer.writerow({'Part ID': part_id, 'Part Name': part_name, 'Material': material, 'Quantity': quantity})


def update_part(part_id, quantity):
    parts = []
    with open(INVENTORY_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Part ID'] == part_id:
                row['Quantity'] = str(int(row['Quantity']) + int(quantity))
            parts.append(row)

    with open(INVENTORY_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()
        writer.writerows(parts)


def delete_part(part_id):
    parts = []
    with open(INVENTORY_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Part ID'] != part_id:
                parts.append(row)

    with open(INVENTORY_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=INVENTORY_FIELDS)
        writer.writeheader()
        writer.writerows(parts)


def view_inventory():
    with open(INVENTORY_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)


# Example operations
if __name__ == '__main__':
    print("Inventory Management System")
    print("[A]dd a part")
    print("[U]pdate part quantity")
    print("[D]elete a part")
    print("[V]iew inventory")
    print("[Q]uit")
    
    while True:
        choice = input("Enter your choice: ").upper()
        if choice == 'A':
            part_id = input("Enter part ID: ")
            part_name = input("Enter part name: ")
            material = input("Enter material: ")
            quantity = input("Enter quantity: ")
            
            add_part(part_id, part_name, material, quantity)
        
        elif choice == 'U':
            part_id = input("Enter part ID to update: ")
            quantity = input("Enter quantity to add or subtract (use - for subtracting): ")
            
            update_part(part_id, quantity)
        
        elif choice == 'D':
            part_id = input("Enter part ID to delete: ")
            
            delete_part(part_id)
        
        elif choice == 'V':
            view_inventory()
        
        elif choice == 'Q':
            break
        else:
            print("Invalid choice. Please try again.")
