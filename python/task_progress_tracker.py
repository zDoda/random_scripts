#!/usr/bin/env python3

import json
from datetime import datetime

# Define a file for storing tasks data
TASKS_FILE = "tasks.json"

# Function to load tasks from the tasks file
def load_tasks(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save tasks to the tasks file
def save_tasks(tasks, filename):
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to add a new task
def add_task(tasks, task_name):
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {
        'name': task_name,
        'status': 'pending',
        'created_at': str(datetime.now()),
        'updated_at': str(datetime.now())
    }
    return task_id

# Function to update a task's progress
def update_task(tasks, task_id, status):
    if task_id in tasks:
        tasks[task_id]['status'] = status
        tasks[task_id]['updated_at'] = str(datetime.now())
        return True
    else:
        return False

# Main function to handle task operations
def main():
    tasks = load_tasks(TASKS_FILE)

    # Example task operations
    new_task_name = "Learn Python Scripting"
    task_id = add_task(tasks, new_task_name)
    print(f"Task '{new_task_name}' added with ID {task_id}")

    # Updating task status
    if update_task(tasks, task_id, 'in progress'):
        print(f"Task {task_id} status updated to 'in progress'")
    else:
        print(f"Task {task_id} not found")

    # Save tasks back to the file
    save_tasks(tasks, TASKS_FILE)

if __name__ == '__main__':
    main()
