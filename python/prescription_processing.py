#!/usr/bin/env python3
import json
import datetime
import os

# You would need to customize the following function according to your specific requirements and system.

def process_prescription(prescription_data_file, output_directory):
    try:
        # Load the prescription data
        with open(prescription_data_file, 'r') as file:
            prescriptions = json.load(file)

        # Process each prescription
        for prescription in prescriptions["prescriptions"]:
            patient_name = prescription["patient_name"]
            medication = prescription["medication"]
            dosage = prescription["dosage"]
            frequency = prescription["frequency"]
            duration = prescription["duration"]

            # You can add more checks and processes to validate the prescription here
            
            # Generate prescription text
            prescription_text = (
                f"Patient: {patient_name}\n"
                f"Medication: {medication}\n"
                f"Dosage: {dosage}\n"
                f"Frequency: {frequency}\n"
                f"Duration: {duration}\n"
                f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                "-----\n"
            )

            # Save the processed prescription to a file
            output_filename = f"{patient_name.replace(' ', '_').lower()}_prescription.txt"
            output_path = os.path.join(output_directory, output_filename)

            with open(output_path, 'w') as output_file:
                output_file.write(prescription_text)

            print(f"Processed and saved prescription for {patient_name}")

    except Exception as e:
        print(f"An error occurred while processing the prescription: {e}")

if __name__ == "__main__":
    PRESCRIPTION_DATA_FILE = 'prescriptions.json'  # Path to the JSON file containing prescriptions
    OUTPUT_DIRECTORY = './processed_prescriptions/'  # Directory to save processed prescriptions

    # Create output directory if not exists
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    process_prescription(PRESCRIPTION_DATA_FILE, OUTPUT_DIRECTORY)
