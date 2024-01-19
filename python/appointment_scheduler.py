#!/usr/bin/env python3
import datetime

class PatientAppointmentScheduler:
    def __init__(self):
        self.appointments = {}
    
    def schedule_appointment(self, patient_id, date_time):
        if date_time in self.appointments:
            print(f"The time slot on {date_time} is already booked. Please choose another time.")
            return False
        
        self.appointments[date_time] = patient_id
        print(f"Appointment scheduled for patient {patient_id} on {date_time}")
        return True
      
    def schedule_follow_up(self, patient_id, days_after):
        last_appointment_date = None
        for appointment_date in sorted(self.appointments.keys()):
            if self.appointments[appointment_date] == patient_id:
                last_appointment_date = appointment_date
        
        if last_appointment_date is None:
            print(f"No previous appointment found for patient {patient_id}.")
            return False
        
        follow_up_date = last_appointment_date + datetime.timedelta(days=days_after)
        return self.schedule_appointment(patient_id, follow_up_date)
        
    def cancel_appointment(self, date_time):
        if date_time not in self.appointments:
            print("No appointment found at the specified time.")
            return False
        
        patient_id = self.appointments.pop(date_time)
        print(f"Appointment for patient {patient_id} on {date_time} has been canceled.")
        return True
    
    def print_schedule(self):
        print("Scheduled Appointments:")
        for date_time, patient_id in sorted(self.appointments.items()):
            print(f"{date_time}: Patient {patient_id}")

# Example usage
if __name__ == "__main__":
    scheduler = PatientAppointmentScheduler()
    patient_id_example = "P123456"
    appointment_time = datetime.datetime(year=2023, month=4, day=20, hour=10, minute=30)
    
    scheduler.schedule_appointment(patient_id_example, appointment_time)
    scheduler.schedule_follow_up(patient_id_example, days_after=30)
    scheduler.print_schedule()
    
    # Cancel an appointment
    scheduler.cancel_appointment(appointment_time)
    scheduler.print_schedule()
