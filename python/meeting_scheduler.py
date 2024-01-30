#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
import schedule
import time
from datetime import datetime, timedelta

# Email credentials
email_address = 'your_email@example.com' # Replace with your email address
email_password = 'your_password' # Replace with your email password

# SMTP server configuration
smtp_server = 'smtp.example.com' # Replace with your SMTP server
smtp_port = 587 # Replace with your SMTP port

# Recipient email and meeting details
recipient_email = 'recipient@example.com' # Replace with recipient's email
meeting_subject = 'Scheduled Meeting Reminder'
meeting_agenda = 'Discuss the upcoming project milestones.'
meeting_date = '2023-04-10' # Replace with your scheduled meeting date (YYYY-MM-DD)
meeting_time = '10:00 AM' # Replace with your scheduled meeting time

# Time before the meeting to send the reminder
reminder_advance_minutes = 30 # Send reminder 30 minutes before the meeting

# Function to send an email
def send_email(to, subject, content):
    msg = EmailMessage()
    msg['From'] = email_address
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(content)
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        
    print("Reminder email sent to", to)

# Function to send a meeting reminder
def send_meeting_reminder():
    meeting_datetime = datetime.strptime(f'{meeting_date} {meeting_time}', '%Y-%m-%d %I:%M %p')
    now = datetime.now()
    
    if now < meeting_datetime:
        time_diff = meeting_datetime - now
        if time_diff <= timedelta(minutes=reminder_advance_minutes):
            email_content = f'Dear recipient,\n\nThis is a reminder about our scheduled meeting on {meeting_date} at {meeting_time}.\n\nAgenda:\n{meeting_agenda}\n\nBest regards,\n\nYour Name'
            send_email(recipient_email, meeting_subject, email_content)

# Function to schedule the reminders
def schedule_reminders():
    # Calculate the exact time to send the reminder
    meeting_datetime = datetime.strptime(f'{meeting_date} {meeting_time}', '%Y-%m-%d %I:%M %p')
    reminder_time = meeting_datetime - timedelta(minutes=reminder_advance_minutes)
    reminder_time_str = reminder_time.strftime('%Y-%m-%d %H:%M:%S')

    # Schedule the reminder
    schedule.every().day.at(reminder_time_str).do(send_meeting_reminder)

    # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the meeting reminder scheduler
if __name__ == '__main__':
    schedule_reminders()
