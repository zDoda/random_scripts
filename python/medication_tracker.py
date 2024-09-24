#!/usr/bin/env python3

import datetime
import threading

# Define a medication class to keep track of medication details
class Medication:
    def __init__(self, name, dose, time_to_take, interval_hours):
        self.name = name
        self.dose = dose
        self.time_to_take = time_to_take
        self.interval_hours = interval_hours
        self.next_dose_time = self.calculate_next_dose_time()

    def calculate_next_dose_time(self):
        return self.time_to_take + datetime.timedelta(hours=self.interval_hours)

    def take_medication(self):
        print(f"Time to take {self.dose} of {self.name}.")
        self.time_to_take = datetime.datetime.now()
        self.next_dose_time = self.calculate_next_dose_time()

# List of medications to track
medications = [
    Medication("MedicationA", "1 pill", datetime.datetime.now(), 24),
    Medication("MedicationB", "2 pills", datetime.datetime.now(), 8)
]

def medication_alert(medication):
    while True:
        current_time = datetime.datetime.now()
        if current_time >= medication.next_dose_time:
            medication.take_medication()
            # Setting a delay to avoid repeated messages in case of slight miscalculations or delays in taking the medication.
            threading.Timer(60 * 60, medication_alert, [medication]).start()
            break
        else:
            # Check again in 1 minute
            threading.Timer(60, medication_alert, [medication]).start()
            break

if __name__ == "__main__":
    for med in medications:
        medication_alert(med)
