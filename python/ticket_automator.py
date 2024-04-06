#!/usr/bin/env python3

import re
from datetime import datetime

# Define a simple rule-based categorization
def categorize_ticket(subject, description):
    category = "General"
    if re.search(r"(login|password)", subject, re.IGNORECASE):
        category = "Authentication"
    elif re.search(r"(error|crash|failure)", description, re.IGNORECASE):
        category = "Technical Issue"
    elif re.search(r"(refund|payment|billing)", subject, re.IGNORECASE):
        category = "Finance"
    return category

# Define a simple rule-based prioritization
def prioritize_ticket(category, creation_date):
    # Priority levels are High, Medium, Low
    priority = "Low"
    high_priority_categories = ["Authentication", "Technical Issue"]
    high_priority_age_threshold_days = 1
    age = (datetime.now() - creation_date).days

    if category in high_priority_categories or age > high_priority_age_threshold_days:
        priority = "High"
    elif category == "Finance":
        priority = "Medium"
    return priority

# Example usage
if __name__ == "__main__":
    # Dummy ticket data
    tickets = [
        {
            "id": 1,
            "subject": "Can't log in to my account",
            "description": "Every time I try to log in, it says 'incorrect password'.",
            "creation_date": datetime.strptime('2023-04-10', '%Y-%m-%d')
        },
        {
            "id": 2,
            "subject": "Refund for overcharge",
            "description": "I have been charged twice for my subscription this month.",
            "creation_date": datetime.strptime('2023-04-08', '%Y-%m-%d')
        },
        {
            "id": 3,
            "subject": "Feature request",
            "description": "Could you add more color themes to the application?",
            "creation_date": datetime.strptime('2023-04-12', '%Y-%m-%d')
        }
    ]

    # Process each ticket
    for ticket in tickets:
        category = categorize_ticket(ticket['subject'], ticket['description'])
        priority = prioritize_ticket(category, ticket['creation_date'])
        print(f"Ticket ID {ticket['id']} is categorized as {category} with {priority} priority.")
