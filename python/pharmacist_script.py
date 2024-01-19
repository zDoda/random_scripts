class Pharmacist:
    def __init__(self, name, age, license_number):
        self.name = name
        self.age = age
        self.license_number = license_number

    def dispense_medication(self, medication):
        print(f"{self.name} dispenses {medication}")

    def verify_prescription(self, prescription):
        if prescription.is_valid():
            print("Prescription is valid.")
        else:
            print("Prescription is not valid.")

class Prescription:
    def __init__(self, patient_name, medication, dosage):
        self.patient_name = patient_name
        self.medication = medication
        self.dosage = dosage

    def is_valid(self):
        # Add validation logic here
        return True  # Placeholder for demonstration purposes
