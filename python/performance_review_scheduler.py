#!/usr/bin/env python3

import datetime
import smtplib
from email.message import EmailMessage
import calendar

# Configuration: Set up the details for the email server and the performance review period
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@example.com'
SMTP_PASSWORD = 'your-password'
FROM_EMAIL = 'your-email@example.com'
TO_EMAILS = ['employee1@example.com', 'employee2@example.com']  # Add employee emails
SUBJECT = 'Performance Review Schedule'
MESSAGE_TEMPLATE = '''Hello {name},

This is a reminder that your performance review has been scheduled for {date}.
Please make sure to prepare the necessary documents and reports before the meeting.

Best,
HR Team
'''

# Customize these as per your company's scheduling policy
PERFORMANCE_REVIEW_CYCLE = 6  # months
START_MONTH = 1  # January
START_DAY = 15  # 15th of January

def schedule_performance_reviews(start_month, start_day, cycle_months):
    current_year = datetime.datetime.today().year
    current_month = datetime.datetime.today().month

    # Calculate the month for the next review
    months_to_next_review = cycle_months - ((current_month - start_month) % cycle_months)
    next_review_month = (current_month + months_to_next_review) % 12 or 12

    # Calculate the date for the next review
    _, last_day_of_month = calendar.monthrange(current_year, next_review_month)
    next_review_day = min(start_day, last_day_of_month)
    next_review_date = datetime.date(current_year, next_review_month, next_review_day)

    return next_review_date

def send_email(to_email, name, review_date):
    message = EmailMessage()
    message.set_content(MESSAGE_TEMPLATE.format(name=name, date=review_date))
    message['Subject'] = SUBJECT
    message['From'] = FROM_EMAIL
    message['To'] = to_email

    # Send the email via the configured SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp_server.send_message(message)
    
def main():
    # Automate scheduling of performance reviews
    next_review_date = schedule_performance_reviews(START_MONTH, START_DAY, PERFORMANCE_REVIEW_CYCLE)
    
    for email in TO_EMAILS:
        # Assume emails are in the format of "username@example.com"
        # Splitting the email to use the username as the employee's name for now
        name = email.split('@')[0].capitalize()
        send_email(email, name, next_review_date)

# Run the main function
if __name__ == '__main__':
    main()