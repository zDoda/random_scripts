#!/usr/bin/env python3
import os
import datetime
import json

def generate_status_report(project_name, tasks):
    # Create a directory to store reports if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Get current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Construct the report file name
    report_filename = f'reports/{project_name}_status_{date_time}.txt'

    # Generate report content
    report_content = f'Project Status Report - {project_name}\n'
    report_content += f'Generated on: {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n'
    report_content += f'Total number of tasks: {len(tasks)}\n\n'
    
    completed_tasks = [task for task in tasks if task['status'].lower() == 'completed']
    ongoing_tasks = [task for task in tasks if task['status'].lower() == 'ongoing']
    upcoming_tasks = [task for task in tasks if task['status'].lower() == 'upcoming']

    report_content += f'Completed Tasks ({len(completed_tasks)}):\n'
    for task in completed_tasks:
        report_content += f"- {task['title']} (Completed on: {task['completed_on']})\n"

    report_content += f'\nOngoing Tasks ({len(ongoing_tasks)}):\n'
    for task in ongoing_tasks:
        report_content += f"- {task['title']} (Due by: {task['due_date']})\n"

    report_content += f'\nUpcoming Tasks ({len(upcoming_tasks)}):\n'
    for task in upcoming_tasks:
        report_content += f"- {task['title']} (Starts on: {task['start_date']})\n"
    
    # Write report to a text file
    with open(report_filename, 'w') as file:
        file.write(report_content)
    
    print(f'Report generated: {report_filename}')

# Example data
project_name = "AI Development Project"
tasks = [
    {"title": "Task 1", "status": "completed", "completed_on": "2023-02-01"},
    {"title": "Task 2", "status": "ongoing", "due_date": "2023-02-15"},
    {"title": "Task 3", "status": "upcoming", "start_date": "2023-03-01"},
]

# Generate the report
generate_status_report(project_name, tasks)
