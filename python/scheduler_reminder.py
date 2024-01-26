#!/usr/bin/env python3

import schedule
import time
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

# Configuration for your email
email_address = "your_email@example.com"  # Update with your email address
email_password = "your_password"          # Update with your email password
smtp_server = "smtp.example.com"          # Update with your SMTP server
smtp_port = 587                           # Update with your SMTP port (commonly 587 for TLS)

# Follow-up configuration
follow_ups = [
    {
        "name": "Client A",
        "email": "client.a@example.com",
        "date": "2023-04-15 09:00"  # Example date format
    },
    # Add more follow-up configurations here
]

# Function to send reminder email
def send_reminder(follow_up):
    try:
        msg = EmailMessage()
        msg.set_content(f"Hi {follow_up['name']},\n\nJust a reminder about our scheduled follow-up on {follow_up['date']}.\n\nBest regards,\nYour Name")
        msg['Subject'] = f"Reminder: Upcoming Follow-up on {follow_up['date']}"
        msg['From'] = email_address
        msg['To'] = follow_up['email']

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)
        server.quit()

        print(f"Sent reminder to {follow_up['name']} scheduled on {follow_up['date']}.")
    except Exception as e:
        print(f"Failed to send reminder to {follow_up['name']}. Error: {e}")

# Function to schedule reminders
def schedule_reminders():
    for follow_up in follow_ups:
        follow_up_date = datetime.strptime(follow_up['date'], "%Y-%m-%d %H:%M")
        schedule_date = follow_up_date - timedelta(days=1)  # Send reminder 1 day before
        if schedule_date > datetime.now():
            schedule_date_str = schedule_date.strftime("%Y-%m-%d %H:%M")
            schedule.every().day.at(schedule_date_str).do(send_reminder, follow_up)

# Main function to handle the scheduling
def main():
    schedule_reminders()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
