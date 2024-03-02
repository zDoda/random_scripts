#!/usr/bin/env python3

import os
import shutil

# Define the paths and categories
source_path = '/path/to/source/assets'
destination_path = '/path/to/organized/assets'

# You can customize these categories and file types according to your requirements
categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.svg'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
    'Audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z']
}

# Function to organize assets
def organize_assets(source, destination, file_categories):
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    # Loop through all files in source directory
    for filename in os.listdir(source):
        if os.path.isfile(os.path.join(source, filename)):
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Find the category for each file type
            for category, extensions in file_categories.items():
                if file_extension in extensions:
                    category_path = os.path.join(destination, category)
                    
                    # Create a directory for the category if it doesn't exist
                    if not os.path.exists(category_path):
                        os.makedirs(category_path)
                    
                    # Move the file to the category directory
                    shutil.move(os.path.join(source, filename), os.path.join(category_path, filename))
                    break

# Call the function to organize assets
organize_assets(source_path, destination_path, categories)
