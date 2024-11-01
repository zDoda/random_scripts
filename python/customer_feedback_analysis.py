#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
import pandas as pd
from textblob import TextBlob

# Email settings
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username@example.com'
smtp_password = 'your_password'

# Email content
from_email = smtp_username
to_emails = ['customer1@example.com', 'customer2@example.com']  # Add customers' email addresses
subject = 'We value your feedback!'
body = """
Dear valued customer,

We hope that you are enjoying your purchase. We are always looking to improve our services and would greatly appreciate your feedback.

Please click the link below to complete a short survey:
http://example.com/feedback

Thank you for your time,
Customer Service Team
"""

# Sending the emails
def send_emails(smtp_server, smtp_port, smtp_username, smtp_password, from_email, to_emails, subject, body):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    for to_email in to_emails:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        try:
            server.sendmail(from_email, to_email, msg.as_string())
            print(f'Email sent to {to_email}')
        except Exception as e:
            print(f'Failed to send email to {to_email}: {str(e)}')

    server.quit()

send_emails(smtp_server, smtp_port, smtp_username, smtp_password, from_email, to_emails, subject, body)

# Customer feedback analysis
feedback_data = 'feedback.csv' # Assume feedback is collected in a CSV file with a column 'Feedback'

def analyze_feedback(feedback_file):
    feedback_df = pd.read_csv(feedback_file)
    feedback_df['Polarity'] = feedback_df['Feedback'].apply(lambda x: TextBlob(x).sentiment.polarity)
    feedback_df['Subjectivity'] = feedback_df['Feedback'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

    # Save the analyzed data back to a file
    feedback_df.to_csv('analyzed_feedback.csv', index=False)

    # Returning the average scores
    return feedback_df['Polarity'].mean(), feedback_df['Subjectivity'].mean()

# Run analysis
average_polarity, average_subjectivity = analyze_feedback(feedback_data)
print(f'Average Sentiment Polarity: {average_polarity}')
print(f'Average Sentiment Subjectivity: {average_subjectivity}')
