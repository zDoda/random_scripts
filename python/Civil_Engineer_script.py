Certainly! Here's an example of a Python script that a civil engineer might use to calculate the volume of a cylindrical water tank:

```python
import math

def calculate_cylinder_volume(radius, height):
    volume = math.pi * radius ** 2 * height
    return volume

tank_radius = float(input("Enter the radius of the cylindrical water tank (in meters): "))
tank_height = float(input("Enter the height of the cylindrical water tank (in meters): "))

tank_volume = calculate_cylinder_volume(tank_radius, tank_height)
print(f"The volume of the cylindrical water tank is: {tank_volume} cubic meters.")
```

This script uses the formula for the volume of a cylinder (π * r^2 * h) to calculate the volume of a cylindrical water tank based on user input for the radius and height of the tank.