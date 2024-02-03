#!/usr/bin/env python3
import datetime

class PatientScheduler:
    def __init__(self):
        self.appointments = {}
    
    def schedule_appointment(self, patient_id, date_time):
        if date_time in self.appointments:
            print(f"The time slot on {date_time} is already booked.")
        else:
            self.appointments[date_time] = patient_id
            print(f"Appointment scheduled for patient {patient_id} on {date_time}.")

    def reschedule_appointment(self, patient_id, current_date_time, new_date_time):
        if current_date_time not in self.appointments or self.appointments[current_date_time] != patient_id:
            print(f"No appointment found for patient {patient_id} on {current_date_time}.")
        elif new_date_time in self.appointments:
            print(f"The time slot on {new_date_time} is already booked.")
        else:
            del self.appointments[current_date_time]
            self.appointments[new_date_time] = patient_id
            print(f"Appointment rescheduled for patient {patient_id} from {current_date_time} to {new_date_time}.")

    def cancel_appointment(self, patient_id, date_time):
        if date_time not in self.appointments or self.appointments[date_time] != patient_id:
            print(f"No appointment found for patient {patient_id} on {date_time}.")
        else:
            del self.appointments[date_time]
            print(f"Appointment for patient {patient_id} on {date_time} has been canceled.")

    def schedule_follow_up(self, patient_id, days_after):
        date_time = datetime.datetime.now() + datetime.timedelta(days=days_after)
        # Round the date_time to the next full hour
        date_time = date_time.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
        self.schedule_appointment(patient_id, date_time)
    
    def list_appointments(self):
        for date_time, patient_id in sorted(self.appointments.items()):
            print(f"Patient {patient_id} has an appointment on {date_time}.")

# Example usage
if __name__ == "__main__":
    scheduler = PatientScheduler()
    
    # Schedule some appointments
    scheduler.schedule_appointment("Patient-001", datetime.datetime(2023, 4, 30, 9, 0))
    scheduler.schedule_appointment("Patient-002", datetime.datetime(2023, 4, 30, 10, 0))

    # Schedule a follow-up in 10 days
    scheduler.schedule_follow_up("Patient-003", 10)

    # Reschedule an appointment
    scheduler.reschedule_appointment("Patient-002", datetime.datetime(2023, 4, 30, 10, 0), datetime.datetime(2023, 5, 1, 10, 0))

    # Cancel an appointment
    scheduler.cancel_appointment("Patient-001", datetime.datetime(2023, 4, 30, 9, 0))

    # List all appointments
    scheduler.list_appointments()
