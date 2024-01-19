#!/usr/bin/env python3

import os
from PIL import Image

# Set the path to the directory where the architectural plans are stored
plans_directory = "/path/to/architectural/plans"

# Set the compliance criteria (this is just an example and would be different depending on actual requirements)
compliance_criteria = {
    'minimum_resolution': (3000, 2000),  # Minimum resolution in pixels (width x height)
    'file_format': 'pdf',                # Required file format
    'max_file_size_mb': 10               # Maximum file size in MB
}

# Function to check if image meets resolution criteria
def check_resolution(image_path):
    with Image.open(image_path) as img:
        return img.size >= compliance_criteria['minimum_resolution']

# Function to check file extension
def check_file_format(file_path):
    return file_path.lower().endswith(compliance_criteria['file_format'])

# Function to check file size
def check_file_size(file_path):
    return (os.path.getsize(file_path) / 1024 / 1024) <= compliance_criteria['max_file_size_mb']

# Function to check compliance of all architectural plans
def check_architectural_compliance(directory):
    compliance_results = {}
    for file_name in os.listdir(directory):
        if file_name.endswith('.pdf'):  # Process only PDF files, assuming plans are in PDF format
            file_path = os.path.join(directory, file_name)
            
            resolution_check = False
            format_check = check_file_format(file_path)
            size_check = check_file_size(file_path)
            
            if format_check and size_check:
                # Perform resolution check only if the file is in the correct format and size
                resolution_check = check_resolution(file_path)
            
            compliance_results[file_name] = {
                'resolution': resolution_check,
                'format': format_check,
                'size': size_check
            }
    return compliance_results

# Run compliance check
results = check_architectural_compliance(plans_directory)

# Print the results
for plan, result in results.items():
    print(f'Plan: {plan}')
    print(f'\tResolution Compliant: {result["resolution"]}')
    print(f'\tFormat Compliant: {result["format"]}')
    print(f'\tSize Compliant: {result["size"]}')
