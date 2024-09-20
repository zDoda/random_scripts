#!/usr/bin/env python3

import os
import datetime
import pandas as pd

# Define the path where progress photos and reports are stored
PHOTO_DIR = '/path/to/progress_photos'
REPORT_DIR = '/path/to/progress_reports'

# Define the structure of your project's progress information
project_stages = [
    'Design',
    'Foundation',
    'Framing',
    'Roofing',
    'Exterior Finishing',
    'Interior Finishing',
    'Landscaping',
    'Final Touches'
]

# Function to automate tracking of progress
def track_progress(project_stages, photo_dir, report_dir):

    # Get the current date for timestamp
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    # Create a DataFrame to store the progress information
    progress_df = pd.DataFrame(columns=['Date', 'Stage', 'Photo', 'Report'])

    # Iterate over the project stages and check for new files
    for stage in project_stages:
        # Paths for photos and reports of each stage
        stage_photo_dir = os.path.join(photo_dir, stage)
        stage_report_dir = os.path.join(report_dir, stage)

        # Latest photo and report for the stage
        latest_photo = max([os.path.join(stage_photo_dir, f) for f in os.listdir(stage_photo_dir) if f.endswith('.jpg')], default=None)
        latest_report = max([os.path.join(stage_report_dir, f) for f in os.listdir(stage_report_dir) if f.endswith('.pdf')], default=None)

        # Append the records to the DataFrame
        progress_record = {'Date': today, 'Stage': stage, 'Photo': latest_photo, 'Report': latest_report}
        progress_df = progress_df.append(progress_record, ignore_index=True)

    # Save the progress information to a CSV file
    progress_df.to_csv(os.path.join(report_dir, f'progress_tracker_{today}.csv'), index=False)

    print(f"Progress tracking for {today} is done.")

# Main function to run the tracker
def main():
    track_progress(project_stages, PHOTO_DIR, REPORT_DIR)

if __name__ == '__main__':
    main()
