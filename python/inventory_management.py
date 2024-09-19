#!/usr/bin/env python3
import csv
from pathlib import Path

class InventoryManagement:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory()

    def load_inventory(self):
        if not Path(self.inventory_file).exists():
            return {}
        with open(self.inventory_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            inventory = {row['PartNumber']: {'Description': row['Description'], 'Quantity': int(row['Quantity'])} for row in reader}
        return inventory

    def add_part(self, part_number, description, quantity):
        if part_number in self.inventory:
            self.inventory[part_number]['Quantity'] += quantity
        else:
            self.inventory[part_number] = {'Description': description, 'Quantity': quantity}
        self.save_inventory()

    def remove_part(self, part_number, quantity):
        if part_number in self.inventory and self.inventory[part_number]['Quantity'] >= quantity:
            self.inventory[part_number]['Quantity'] -= quantity
            if self.inventory[part_number]['Quantity'] == 0:
                del self.inventory[part_number]
            self.save_inventory()
        else:
            print("Error: Not enough inventory or part not found")

    def get_inventory(self):
        return self.inventory

    def save_inventory(self):
        with open(self.inventory_file, mode='w', newline='') as file:
            fieldnames = ['PartNumber', 'Description', 'Quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for part_number, data in self.inventory.items():
                writer.writerow({'PartNumber': part_number, 'Description': data['Description'], 'Quantity': data['Quantity']})

def main():
    inventory_file = 'inventory.csv'
    inventory_manager = InventoryManagement(inventory_file)
    
    # Examples of how to use the inventory management
    inventory_manager.add_part('PN1234', 'Widget A', 10)
    inventory_manager.add_part('PN5678', 'Widget B', 5)
    inventory_manager.remove_part('PN1234', 3)
    
    current_inventory = inventory_manager.get_inventory()
    print("Current Inventory: ")
    for part, data in current_inventory.items():
        print(f"Part Number: {part}, Description: {data['Description']}, Quantity: {data['Quantity']}")

if __name__ == '__main__':
    main()
