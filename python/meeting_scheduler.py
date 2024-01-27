#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

# Configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@example.com'  # Replace with your email
SMTP_PASSWORD = 'your-password'  # Replace with your password

EMAIL_FROM = 'your-email@example.com'
EMAIL_TO = 'recipient-email@example.com'
EMAIL_SUBJECT = 'Meeting Reminder: {meeting_subject}'

CALENDAR_INVITE = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your Product//EN
METHOD:REQUEST
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{dtstart}
DTEND:{dtend}
SUMMARY:{summary}
DESCRIPTION:{description}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
"""

def send_email(meeting_subject, meeting_description, meeting_location, meeting_start, meeting_end):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = EMAIL_SUBJECT.format(meeting_subject=meeting_subject)
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    # Replace newline characters with CRLF
    cal_invite = CALENDAR_INVITE.replace('\n', '\r\n').format(
        uid=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ') + "-" + SMTP_USERNAME,
        dtstamp=datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'),
        dtstart=meeting_start.strftime('%Y%m%dT%H%M%SZ'),
        dtend=meeting_end.strftime('%Y%m%dT%H%M%SZ'),
        summary=meeting_subject,
        description=meeting_description,
        location=meeting_location
    )
    part = MIMEText(cal_invite, 'calendar;method=REQUEST')
    msg.attach(part)

    # SMTP session
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    smtp.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    smtp.quit()

# Meeting information
meeting_subject = 'Project Sync-Up'
meeting_description = 'Discuss project updates and next steps.'
meeting_location = 'Conference Room 1'
meeting_start = datetime.now() + timedelta(days=1, hours=9) # Schedule for the next day at 9 AM
meeting_end = meeting_start + timedelta(hours=1) # Duration of 1 hour

# Send the invitation
send_email(meeting_subject, meeting_description, meeting_location, meeting_start, meeting_end)
