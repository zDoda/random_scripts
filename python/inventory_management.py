#!/usr/bin/env python3

import json

class InventoryManagement:
    def __init__(self, inventory_file):
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                inventory_data = json.load(file)
        except FileNotFoundError:
            inventory_data = {}
        return inventory_data

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            json.dump(self.inventory, file, indent=4)

    def add_item(self, item, quantity):
        self.inventory[item] = self.inventory.get(item, 0) + quantity
        self.save_inventory()

    def remove_item(self, item, quantity):
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            print("Not enough inventory or item not found.")
        self.save_inventory()

    def check_inventory(self):
        for item, quantity in self.inventory.items():
            print(f"{item}: {quantity}")

    def order_item(self, item, order_quantity, reorder_threshold, reorder_amount):
        current_quantity = self.inventory.get(item, 0)
        if current_quantity < reorder_threshold:
            self.add_item(item, reorder_amount)
            print(f"Reordered {reorder_amount} of {item}.")
        elif current_quantity < order_quantity:
            print(f"Cannot place order for {item}. Not enough stock.")
        else:
            self.remove_item(item, order_quantity)
            print(f"Order placed for {item} (quantity: {order_quantity}).")

def main():
    inventory_file = "inventory.json"
    inventory_manager = InventoryManagement(inventory_file)

    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Check Inventory")
        print("4. Order Item")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            item = input("Enter item name to add: ")
            quantity = int(input("Enter quantity: "))
            inventory_manager.add_item(item, quantity)

        elif choice == "2":
            item = input("Enter item name to remove: ")
            quantity = int(input("Enter quantity: "))
            inventory_manager.remove_item(item, quantity)

        elif choice == "3":
            inventory_manager.check_inventory()

        elif choice == "4":
            item = input("Enter item name to order: ")
            order_quantity = int(input("Enter order quantity: "))
            reorder_threshold = int(input("Enter reorder threshold: "))
            reorder_amount = int(input("Enter reorder amount: "))
            inventory_manager.order_item(item, order_quantity, reorder_threshold, reorder_amount)

        elif choice == "5":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
