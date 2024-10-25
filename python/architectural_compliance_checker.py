#!/usr/bin/env python3
import os
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract

# Define the criteria for compliance
MIN_ROOM_SIZE = 15.0  # in square meters
DOOR_WIDTH = 0.8  # in meters
WINDOW_AREA_TO_FLOOR_RATIO = 0.1  # 10%

class ArchitecturalPlan:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.text = pytesseract.image_to_string(self.image)
        
    def check_room_size(self, room):
        words = self.text.split()
        try:
            size_index = words.index('Room') + words[words.index('Room'):].index(room) + 1
            size = float(words[size_index])
        except (ValueError, IndexError):
            return False
        
        return size >= MIN_ROOM_SIZE

    def check_door_width(self, door):
        words = self.text.split()
        try:
            width_index = words.index('Door') + words[words.index('Door'):].index(door) + 1
            width = float(words[width_index])
        except (ValueError, IndexError):
            return False
        
        return width >= DOOR_WIDTH

    def calculate_window_area(self, room):
        words = self.text.split()
        try:
            window_index = words.index('Window') + words[words.index('Window'):].index(room)
            width_index = window_index + 1
            height_index = window_index + 2
            width = float(words[width_index])
            height = float(words[height_index])
        except (ValueError, IndexError):
            return 0
        
        return width * height

    def check_window_to_floor_ratio(self, room):
        floor_area = self.check_room_size(room)
        window_area = self.calculate_window_area(room)
        return window_area / floor_area >= WINDOW_AREA_TO_FLOOR_RATIO if floor_area else False

# Example usage:
if __name__ == "__main__":
    # Path to the architectural plan image
    plan_path = "path/to/architectural_plan.jpg"
    
    # Create ArchitecturalPlan object
    plan = ArchitecturalPlan(plan_path)

    # Check compliance for different aspects
    # For simplicity, assume there is only one room and door and the naming is 'Room1' and 'Door1'
    room_compliance = plan.check_room_size('Room1')
    door_compliance = plan.check_door_width('Door1')
    window_compliance = plan.check_window_to_floor_ratio('Room1')

    # Print out the compliance checks
    print(f"Room Size Compliance: {'Passed' if room_compliance else 'Failed'}")
    print(f"Door Width Compliance: {'Passed' if door_compliance else 'Failed'}")
    print(f"Window to Floor Ratio Compliance: {'Passed' if window_compliance else 'Failed'}")
    
    # Plot the image for manual inspection
    plt.imshow(plan.image)
    plt.title('Architectural Plan')
    plt.axis('off')  # Remove axis
    plt.show()
