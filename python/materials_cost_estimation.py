#!/usr/bin/env python3

import csv

# Define a material class to store the details of each material
class Material:
    def __init__(self, name, cost_per_unit, unit):
        self.name = name
        self.cost_per_unit = cost_per_unit
        self.unit = unit  # e.g., pieces, kg, meters, etc.
        
    def estimate_cost(self, quantity):
        return self.cost_per_unit * quantity

# Function to read materials and their costs from a CSV file
def read_materials_from_csv(file_path):
    materials = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Material']
            cost_per_unit = float(row['Cost Per Unit'])
            unit = row['Unit']
            materials[name] = Material(name, cost_per_unit, unit)
    return materials

# Function to estimate the total cost of the provided materials list
def estimate_materials_cost(materials, materials_required):
    total_cost = 0
    for material_name, quantity in materials_required.items():
        if material_name in materials:
            total_cost += materials[material_name].estimate_cost(quantity)
        else:
            print(f"Material {material_name} not found in the database.")
    return total_cost

def main():
    # Define materials needed for construction
    materials_required = {
        'Cement': 50,  # 50 bags of cement
        'Sand': 2.5,  # 2.5 cubic meters of sand
        'Gravel': 3.5,  # 3.5 cubic meters of gravel
        'Steel Rods': 100  # 100 kg of steel rods
    }
    
    # File path to the CSV with material costs
    materials_csv = 'materials_costs.csv'
    
    # Read materials from CSV file
    materials = read_materials_from_csv(materials_csv)
    
    # Estimate the total cost
    total_cost = estimate_materials_cost(materials, materials_required)
    
    print(f"The total estimated cost is: ${total_cost:.2f}")

if __name__ == "__main__":
    main()
