#!/usr/bin/env python3
import json
from datetime import datetime

class TreatmentPlanManager:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'r') as file:
                self.plans = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.plans = {}

    def add_plan(self, patient_id, plan):
        timestamp = datetime.now().isoformat()
        plan['created_at'] = timestamp
        self.plans[patient_id] = plan
        self.save_plans()

    def update_plan(self, patient_id, plan):
        timestamp = datetime.now().isoformat()
        plan['updated_at'] = timestamp
        if patient_id in self.plans:
            self.plans[patient_id].update(plan)
            self.save_plans()
        else:
            print(f"No treatment plan found for patient {patient_id}. Please add a new plan.")

    def get_plan(self, patient_id):
        return self.plans.get(patient_id)

    def remove_plan(self, patient_id):
        if patient_id in self.plans:
            del self.plans[patient_id]
            self.save_plans()
        else:
            print(f"No treatment plan found for patient {patient_id}.")

    def save_plans(self):
        with open(self.filename, 'w') as file:
            json.dump(self.plans, file, indent=4)

def main():
    treatment_plan_manager = TreatmentPlanManager('treatment_plans.json')

    # Example usage
    
    # Add a new treatment plan
    treatment_plan_manager.add_plan('123', {
        'diagnosis': 'Condition XYZ',
        'medication': 'Medication ABC',
        'duration': '14 days'
    })

    # Get a treatment plan
    plan = treatment_plan_manager.get_plan('123')
    print(f"Patient 123's Treatment Plan: {plan}")

    # Update a treatment plan
    treatment_plan_manager.update_plan('123', {
        'medication': 'New Medication XYZ',
        'notes': 'Patient reported side effects.'
    })

    # Remove a treatment plan
    treatment_plan_manager.remove_plan('123')

if __name__ == "__main__":
    main()
