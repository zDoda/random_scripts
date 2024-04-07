#!/usr/bin/env python3
import re

# Define categories and their keywords
CATEGORIES = {
    'network': ['outage', 'slow', 'latency'],
    'hardware': ['broken', 'repair', 'replacement'],
    'software': ['bug', 'error', 'update', 'crash'],
    'account': ['password', 'login', 'access', 'authentication'],
}

# Priority levels
PRIORITY = {
    'high': ['urgent', 'severe', 'crash', 'outage', 'broken'],
    'medium': ['slow', 'error', 'repair', 'password'],
    'low': ['update', 'login', 'access'],
}

def categorize_ticket(description):
    category = 'general'
    for cat, keywords in CATEGORIES.items():
        if any(keyword in description.lower() for keyword in keywords):
            category = cat
            break
    return category

def prioritize_ticket(description):
    for level, keywords in PRIORITY.items():
        if any(keyword in description.lower() for keyword in keywords):
            return level
    return 'low'

def process_ticket(ticket_description):
    category = categorize_ticket(ticket_description)
    priority = prioritize_ticket(ticket_description)
    return category, priority

if __name__ == '__main__':
    # Example ticket description
    example_ticket = "Customer reports that the system crashes when they try to login."
    
    # Process the ticket to get its category and priority
    ticket_category, ticket_priority = process_ticket(example_ticket)
    
    # Output the result (you would replace this with the code to update the ticketing system in a real application)
    print(f"Ticket Category: {ticket_category}")
    print(f"Ticket Priority: {ticket_priority}")

