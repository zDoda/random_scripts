#!/usr/bin/env python3

import csv
from datetime import datetime

# Define the file that will be used to store the data
LEAVE_DATA_FILE = 'leave_data.csv'

# Define the headers for the CSV file
HEADERS = ['Employee ID', 'Employee Name', 'Leave Start Date', 'Leave End Date', 'Leave Type', 'Comments']

# Function to add a leave record
def add_leave_record(employee_id, employee_name, start_date, end_date, leave_type, comments):
    with open(LEAVE_DATA_FILE, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writerow({
            'Employee ID': employee_id,
            'Employee Name': employee_name,
            'Leave Start Date': start_date,
            'Leave End Date': end_date,
            'Leave Type': leave_type,
            'Comments': comments
        })

# Function to view all leave records
def view_leave_records():
    try:
        with open(LEAVE_DATA_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(dict(row))
    except FileNotFoundError:
        print('No leave record found.')

# Function to set up the CSV file
def setup_csv_file():
    try:
        with open(LEAVE_DATA_FILE, 'x') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
            writer.writeheader()
    except FileExistsError:
        pass

# Main function to handle leave and absence tracking
def main():
    setup_csv_file()
    while True:
        action = input('Do you want to add a leave record or view all records? (add/view/exit) ').lower()
        if action == 'add':
            employee_id = input('Enter the employee ID: ')
            employee_name = input('Enter the employee name: ')
            leave_type = input('Enter the leave type (e.g., Sick Leave, Vacation, etc.): ')
            start_date = input('Enter the leave start date (YYYY-MM-DD): ')
            end_date = input('Enter the leave end date (YYYY-MM-DD): ')
            comments = input('Enter any comments regarding the leave: ')
            add_leave_record(employee_id, employee_name, start_date, end_date, leave_type, comments)
            print('Leave record added successfully.')
        elif action == 'view':
            view_leave_records()
        elif action == 'exit':
            print('Exiting leave and absence tracking.')
            break
        else:
            print('Invalid input, please type "add", "view", or "exit".')

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
