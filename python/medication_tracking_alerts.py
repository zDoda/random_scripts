#!/usr/bin/env python3

import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler

# Class to hold medication information
class Medication:
    def __init__(self, name, dose, frequency, start_time):
        self.name = name
        self.dose = dose
        self.frequency = frequency  # in hours
        self.start_time = start_time
        self.next_dose_time = self.calculate_next_dose_time()

    def calculate_next_dose_time(self):
        return self.start_time + datetime.timedelta(hours=self.frequency)

    def time_for_next_dose(self):
        return datetime.datetime.now() >= self.next_dose_time

    def take_medication(self):
        print(f"Time to take {self.dose} of {self.name}.")
        self.start_time = datetime.datetime.now()
        self.next_dose_time = self.calculate_next_dose_time()

# Medication reminder scheduler
class MedicationScheduler:
    def __init__(self):
        self.medications = []
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_medication(self, medication):
        self.medications.append(medication)
        self.scheduler.add_job(
            func=self.check_medication,
            trigger='interval',
            minutes=1,
            args=[medication]
        )

    def check_medication(self, medication):
        if medication.time_for_next_dose():
            medication.take_medication()

    def start(self):
        try:
            print("Medication scheduler running...")
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

# Example usage
if __name__ == "__main__":
    # Example medication: Paracetamol every 6 hours, starting now
    paracetamol = Medication(
        name='Paracetamol',
        dose='500mg',
        frequency=6,  # in hours
        start_time=datetime.datetime.now()
    )

    # Initialize the scheduler and add medication
    scheduler = MedicationScheduler()
    scheduler.add_medication(paracetamol)

    # Start the scheduler to check and alert for medication
    scheduler.start()
