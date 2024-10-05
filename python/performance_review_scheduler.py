#!/usr/bin/env python3

import csv
import datetime
from dateutil.relativedelta import relativedelta
import smtplib
from email.message import EmailMessage

# Configuration start
csv_file_path = 'employees.csv' # Path to the CSV file with employee details
smtp_server = 'smtp.example.com' # SMTP server
smtp_port = 587 # SMTP port
email_username = 'your_email@example.com' # Your email that you'll use to send notifications
email_password = 'your_password' # Your email password
from_address = email_username # From address for the email notification
subject = 'Upcoming Performance Review' # Subject for the email notification
template = '''Dear {name},

This is a gentle reminder that your next performance review is scheduled for {review_date}. 
Please make sure you have prepared all necessary documents and reports.

Best regards,

Performance Review Team
'''
# Configuration end

# Get today's date
today = datetime.date.today()

# Open the CSV file and read employee details
employees = []
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert hire_date from string to date
        hire_date = datetime.datetime.strptime(row['hire_date'], '%Y-%m-%d').date()
        # Schedule the review every year on the hire_date
        next_review_date = hire_date + relativedelta(years=(today.year - hire_date.year))
        # If the review date has passed for this year, schedule it for next year
        if next_review_date < today:
            next_review_date = next_review_date + relativedelta(years=1)
        employees.append({
            'name': row['name'],
            'email': row['email'],
            'next_review_date': next_review_date
        })

# Set up server connection
server = smtplib.SMTP(smtp_server, smtp_port)
server.ehlo()
server.starttls()
server.login(email_username, email_password)

# Send reminders
for employee in employees:
    if employee['next_review_date'] == today:
        # Form message
        message = EmailMessage()
        message.set_content(template.format(name=employee['name'], review_date=employee['next_review_date']))
        message['Subject'] = subject
        message['From'] = from_address
        message['To'] = employee['email']
        
        # Send the email
        server.send_message(message)
        print(f'Sent review reminder to: {employee["email"]}')

# Close server connection
server.quit()
