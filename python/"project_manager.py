#!/usr/bin/env python3
import sys
import csv
from datetime import datetime, timedelta

class ProjectManager:
    def __init__(self, project_file):
        self.project_file = project_file
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.project_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tasks.append(row)
        except FileNotFoundError:
            print("Project file not found, starting with an empty task list.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_task(self, task_name, due_date, responsible_person):
        new_task = {
            "Task Name": task_name,
            "Due Date": due_date,
            "Responsible Person": responsible_person,
            "Status": "Open"
        }
        self.tasks.append(new_task)
        self.save_tasks()

    def save_tasks(self):
        keys = self.tasks[0].keys() if self.tasks else ["Task Name", "Due Date", "Responsible Person", "Status"]
        with open(self.project_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.tasks)

    def mark_task_completed(self, task_name):
        for task in self.tasks:
            if task["Task Name"] == task_name:
                task["Status"] = "Completed"
                self.save_tasks()
                return True
        return False

    def get_overdue_tasks(self):
        current_date = datetime.now().date()
        overdue_tasks = [
            task for task in self.tasks if datetime.strptime(task["Due Date"], "%Y-%m-%d").date() < current_date and task["Status"] == "Open"
        ]
        return overdue_tasks

    def print_tasks(self):
        for task in self.tasks:
            print(f'Task: {task["Task Name"]}, Due: {task["Due Date"]}, Assigned to: {task["Responsible Person"]}, Status: {task["Status"]}')

if __name__ == "__main__":
    project_manager = ProjectManager("tasks.csv")

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "add" and len(sys.argv) == 5:
            project_manager.add_task(sys.argv[2], sys.argv[3], sys.argv[4])
        elif command == "complete" and len(sys.argv) == 3:
            if not project_manager.mark_task_completed(sys.argv[2]):
                print("Task not found.")
        elif command == "overdue":
            overdue_tasks = project_manager.get_overdue_tasks()
            for task in overdue_tasks:
                print(f'Overdue Task: {task["Task Name"]}, Due: {task["Due Date"]}, Assigned to: {task["Responsible Person"]}')
        elif command == "list":
            project_manager.print_tasks()
        else:
            print("Unknown command or wrong number of arguments.")
    else:
        print("Usage: python project_manager.py [command]")
