#!/usr/bin/env python3
import json
from datetime import datetime

# Assuming tickets come in as a list of dictionaries in JSON format
# You would likely be getting this from a database or an API in a real-world scenario
json_tickets = """
[
    {"id": 1, "title": "Cannot log in to the website", "description": "When I try to log in, I get an error message.", "created_at": "2023-02-15T12:00:00Z"},
    {"id": 2, "title": "Error in quarterly sales report", "description": "The sales figures do not add up correctly.", "created_at": "2023-02-16T09:30:00Z"},
    {"id": 3, "title": "WiFi keeps dropping out", "description": "Every 10 minutes or so, the WiFi cuts out for about a minute.", "created_at": "2023-02-16T11:20:00Z"}
]
"""

tickets = json.loads(json_tickets)
prioritized_tickets = []

# Define categorization rules
def categorize_ticket(title, description):
    if "log in" in description.lower():
        return "Authentication Issues"
    elif "error" in title.lower():
        return "Report Errors"
    elif "wifi" in description.lower():
        return "Network Problems"
    else:
        return "General"

# Define prioritization rules
def prioritize_ticket(category, created_at):
    high_priority_categories = ["Authentication Issues", "Network Problems"]
    recent_issue_threshold_days = 1
    
    if category in high_priority_categories:
        return "High"

    creation_datetime = datetime.fromisoformat(created_at[:-1])  # Remove Z
    time_since_creation = datetime.utcnow() - creation_datetime

    if time_since_creation.days < recent_issue_threshold_days:
        return "Medium"

    return "Low"

# Process each ticket
for ticket in tickets:
    category = categorize_ticket(ticket["title"], ticket["description"])
    priority = prioritize_ticket(category, ticket["created_at"])
    ticket["category"] = category
    ticket["priority"] = priority
    prioritized_tickets.append(ticket)

# Output the result
print(json.dumps(prioritized_tickets, indent=4))
