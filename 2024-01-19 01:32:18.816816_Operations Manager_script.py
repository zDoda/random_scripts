
class OperationsManager:
    def __init__(self, name, department):
        self.name = name
        self.department = department

    def assign_task(self, task, employee):
        print(f"{self.name} from the {self.department} department assigned {task} to {employee}")

    def analyze_performance(self, employee):
        print(f"{self.name} from the {self.department} department is analyzing the performance of {employee}")

# Example usage
manager1 = OperationsManager("John", "Operations")
manager1.assign_task("Prepare monthly report", "Alice")
manager1.analyze_performance("Bob")
