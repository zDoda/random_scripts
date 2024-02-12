#!/usr/bin/env python3
import datetime
from collections import defaultdict

# Define a class to manage inventory items
class InventoryItem:
    def __init__(self, name, quantity, expiration_date=None):
        self.name = name
        self.quantity = quantity
        self.expiration_date = expiration_date if expiration_date else None

    def __str__(self):
        return f"{self.name}, Quantity: {self.quantity}, Expiration: {self.expiration_date}"
    
# Define the inventory management class
class Inventory:
    def __init__(self):
        self.items = defaultdict(list)

    def add_item(self, item):
        self.items[item.name].append(item)

    def remove_item(self, name, quantity):
        if name in self.items:
            items_to_remove = []
            for item in self.items[name]:
                if item.quantity <= quantity:
                    quantity -= item.quantity
                    items_to_remove.append(item)
                else:
                    item.quantity -= quantity
                    quantity = 0
                if quantity == 0:
                    break
            for item in items_to_remove:
                self.items[name].remove(item)
            if not self.items[name]:
                del self.items[name]
            return True
        return False

    def check_expired(self):
        today = datetime.date.today()
        for name, items in list(self.items.items()):
            self.items[name] = [
                item for item in items if not item.expiration_date or item.expiration_date >= today
            ]
            if not self.items[name]:
                del self.items[name]

    def list_inventory(self):
        for name, items in self.items.items():
            print(f"Inventory for {name}:")
            for item in items:
                print(f" - {item}")

# Example usage
if __name__ == "__main__":
    inventory = Inventory()

    inventory.add_item(InventoryItem("Milk", 10, datetime.date(2023, 5, 1)))
    inventory.add_item(InventoryItem("Bread", 20, datetime.date(2023, 4, 15)))
    
    # Check and remove expired items
    inventory.check_expired()

    # Remove some items
    inventory.remove_item("Milk", 5)
    
    # List current inventory
    inventory.list_inventory()
