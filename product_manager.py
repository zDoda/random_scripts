
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_total_value(self):
        return self.price * self.quantity

    def increase_quantity(self, amount):
        self.quantity += amount

    def decrease_quantity(self, amount):
        if self.quantity - amount >= 0:
            self.quantity -= amount
        else:
            print("Error: Quantity can't be negative")

# Example usage
product1 = Product("Chair", 50, 20)
print(product1.calculate_total_value())
product1.increase_quantity(10)
print(product1.calculate_total_value())
product1.decrease_quantity(5)
print(product1.calculate_total_value())