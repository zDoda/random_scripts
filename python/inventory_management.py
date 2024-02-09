#!/usr/bin/env python3

import csv
import datetime


class InventoryManagement:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory()

    def load_inventory(self):
        inventory = []
        try:
            with open(self.inventory_file, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    row['expiration_date'] = datetime.datetime.strptime(row['expiration_date'], '%Y-%m-%d').date()
                    inventory.append(row)
        except FileNotFoundError:
            print("Inventory file not found.")
        return inventory

    def save_inventory(self):
        fields = ['item_id', 'item_name', 'quantity', 'expiration_date']
        with open(self.inventory_file, mode='w') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fields)
            csv_writer.writeheader()
            for item in self.inventory:
                item['expiration_date'] = item['expiration_date'].strftime('%Y-%m-%d')
                csv_writer.writerow(item)

    def add_item(self, item_id, item_name, quantity, expiration_date):
        new_item = {
            'item_id': item_id,
            'item_name': item_name,
            'quantity': quantity,
            'expiration_date': datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()
        }
        self.inventory.append(new_item)
        self.save_inventory()

    def remove_item(self, item_id, quantity):
        for item in self.inventory:
            if item['item_id'] == item_id and int(item['quantity']) >= quantity:
                item['quantity'] = int(item['quantity']) - quantity
                self.save_inventory()
                return True
        return False

    def check_expired_items(self):
        today = datetime.date.today()
        expired_items = [item for item in self.inventory if item['expiration_date'] < today]
        return expired_items

    def list_inventory(self):
        return self.inventory


def main():
    # Create an instance of InventoryManagement
    inventory_manager = InventoryManagement('inventory.csv')

    # Add test items to inventory
    inventory_manager.add_item('001', 'Apple', 100, '2023-05-12')
    inventory_manager.add_item('002', 'Banana', 150, '2023-06-10')

    # List the current inventory
    current_inventory = inventory_manager.list_inventory()
    print("Current Inventory:", current_inventory)

    # Check for expired items
    expired_items = inventory_manager.check_expired_items()
    print("Expired Items:", expired_items)

    # Remove some items from inventory
    inventory_manager.remove_item('001', 20)


if __name__ == "__main__":
    main()
