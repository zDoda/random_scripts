#!/usr/bin/env python3

import json

class InventoryManagement:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        try:
            with open(inventory_file, 'r') as file:
                self.inventory = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.inventory = {}

    def add_item(self, item_id, quantity):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity
        self.save_inventory()

    def remove_item(self, item_id, quantity):
        if item_id in self.inventory and self.inventory[item_id] >= quantity:
            self.inventory[item_id] -= quantity
            if self.inventory[item_id] == 0:
                del self.inventory[item_id]
            self.save_inventory()
            return True
        else:
            print("Insufficient quantity or item not found in the inventory.")
            return False

    def check_inventory(self, item_id):
        return self.inventory.get(item_id, 0)

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            json.dump(self.inventory, file, indent=4)

    def display_inventory(self):
        for item_id, quantity in self.inventory.items():
            print(f"Item ID: {item_id}, Quantity: {quantity}")

class OrderManagement:
    def __init__(self, inventory):
        self.inventory = inventory

    def place_order(self, order_items):
        for item_id, quantity in order_items.items():
            if self.inventory.check_inventory(item_id) < quantity:
                print(f"Cannot place order for item {item_id}. Not enough in stock.")
                return False
        for item_id, quantity in order_items.items():
            self.inventory.remove_item(item_id, quantity)
        print("Order successfully placed.")
        return True

def main():
    inventory_file = "inventory.json"
    inventory_manager = InventoryManagement(inventory_file)

    # Example usage:
    # Add some items to the inventory
    inventory_manager.add_item("A001", 20)
    inventory_manager.add_item("B002", 50)

    # Remove some items from the inventory
    inventory_manager.remove_item("A001", 5)

    # Check the inventory for a specific item
    print(f"Current quantity for item A001: {inventory_manager.check_inventory('A001')}")

    # Display the entire inventory
    inventory_manager.display_inventory()

    # Place an order
    order_manager = OrderManagement(inventory_manager)
    order = {
        "A001": 2,
        "B002": 10
    }
    order_manager.place_order(order)

    # Display inventory after placing an order
    inventory_manager.display_inventory()

if __name__ == "__main__":
    main()
