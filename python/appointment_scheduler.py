#!/usr/bin/env python3

from datetime import datetime, timedelta
import json

# Dummy data store file
DATA_FILE = 'appointments.json'

def load_appointments():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_appointments(appointments):
    with open(DATA_FILE, 'w') as file:
        json.dump(appointments, file, indent=2)

def schedule_appointment(patient_id, date_time_str):
    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    
    # Check for conflicts before scheduling
    if any(app for app in appointments.values() if app['date_time'] == date_time_str):
        print("Conflict! Another appointment is already scheduled for this time.")
        return
    
    appointments[patient_id] = {
        'patient_id': patient_id,
        'date_time': date_time_str,
        'status': 'scheduled'
    }
    save_appointments(appointments)
    print(f"Appointment scheduled for patient {patient_id} on {date_time}.")

def follow_up_appointment(patient_id, days_after=7):
    if patient_id in appointments:
        last_app_date_str = appointments[patient_id]['date_time']
        last_app_date = datetime.strptime(last_app_date_str, '%Y-%m-%d %H:%M')
        follow_up_date = last_app_date + timedelta(days=days_after)
        follow_up_date_str = follow_up_date.strftime('%Y-%m-%d %H:%M')
        
        # Schedule follow-up
        schedule_appointment(patient_id, follow_up_date_str)
    else:
        print(f"No previous appointment found for patient {patient_id}.")

appointments = load_appointments()

# Example usage:
# schedule_appointment('patient_123', '2023-04-20 14:00')
# follow_up_appointment('patient_123', 14)
