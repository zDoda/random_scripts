#!/usr/bin/env python3

import os
import json
from datetime import datetime, timedelta
import csv

# Project Initialization with Initial Data
class Project:
    def __init__(self, name, start_date, end_date, total_budget, tasks):
        self.name = name
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.total_budget = total_budget
        self.tasks = tasks  # List of Task objects
    
    # Calculate the progress based on tasks completed
    def compute_progress(self):
        completed_tasks = sum(task.is_completed for task in self.tasks)
        return (completed_tasks / len(self.tasks)) * 100

    # Check if the Project is within the budget
    def check_budget(self):
        current_expense = sum(task.cost for task in self.tasks)
        return current_expense <= self.total_budget

# Task for the construction project
class Task:
    def __init__(self, name, start_date, end_date, cost, responsible_person):
        self.name = name
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.duration = (self.end_date - self.start_date).days
        self.cost = cost
        self.responsible_person = responsible_person
        self.is_completed = False
    
    # Complete the task
    def complete_task(self):
        self.is_completed = True

# Function to load tasks from a CSV file
def load_tasks_from_csv(csv_file):
    tasks = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tasks.append(
                Task(
                    name=row['Name'],
                    start_date=row['StartDate'],
                    end_date=row['EndDate'],
                    cost=float(row['Cost']),
                    responsible_person=row['ResponsiblePerson']
                )
            )
    return tasks

# Main function to automate construction project progress tracking
def main():
    # Load tasks from a CSV file
    csv_file_path = 'tasks.csv'
    tasks = load_tasks_from_csv(csv_file_path)

    # Sample initialization of a project
    project = Project(
        name='City Center Tower',
        start_date='2023-01-01',
        end_date='2024-12-31',
        total_budget=50000000,
        tasks=tasks
    )

    # Check the project progress
    project_progress = project.compute_progress()
    print(f"Project '{project.name}' is {project_progress:.2f}% completed.")

    # Check if the project is within the budget
    within_budget = project.check_budget()
    print(f"Project '{project.name}' is within the budget: {within_budget}")

    # Example of updating a task status to completed
    tasks[0].complete_task()

    # Recalculate progress after task completion
    updated_project_progress = project.compute_progress()
    print(f"Project '{project.name}' is {updated_project_progress:.2f}% completed after completing Task: {tasks[0].name}")

if __name__ == "__main__":
    main()
