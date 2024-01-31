#!/usr/bin/env python3
import os
import shutil

# Define the mapping of extensions to directory names
EXTENSION_CATEGORIES = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.bmp': 'Images',
    '.svg': 'Images',
    '.txt': 'Documents',
    '.doc': 'Documents',
    '.docx': 'Documents',
    '.pdf': 'Documents',
    '.xls': 'Documents',
    '.xlsx': 'Documents',
    '.csv': 'Documents',
    '.ppt': 'Presentations',
    '.pptx': 'Presentations',
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.ogg': 'Audio',
    '.mp4': 'Videos',
    '.mov': 'Videos',
    '.avi': 'Videos',
    '.mkv': 'Videos'
}

def organize_assets(source_directory):
    # Ensure source_directory exists
    if not os.path.exists(source_directory):
        print(f"Error: The source directory {source_directory} does not exist.")
        return

    # Iterate over all files in the source directory
    for filename in os.listdir(source_directory):
        # Extract the file extension
        _, extension = os.path.splitext(filename)

        # Check if the file extension is in our mapping
        if extension.lower() in EXTENSION_CATEGORIES:
            # Determine the subdirectory name based on the file extension
            subdirectory_name = EXTENSION_CATEGORIES[extension.lower()]
            
            # Create the subdirectory if it doesn't exist
            subdirectory_path = os.path.join(source_directory, subdirectory_name)
            if not os.path.exists(subdirectory_path):
                os.makedirs(subdirectory_path)
            
            # Move the file to the categorized subdirectory
            shutil.move(os.path.join(source_directory, filename), os.path.join(subdirectory_path, filename))

# Example usage
organize_assets('/path/to/your/assets')
