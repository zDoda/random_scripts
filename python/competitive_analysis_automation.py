#!/usr/bin/env python3

import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configure your list of competitors and your company
competitors = [
    'competitor1.com',
    'competitor2.com',
    'competitor3.com',
]

your_company = 'yourcompany.com'

# List of features or keywords to compare
features = [
    'feature1',
    'feature2',
    'feature3',
]

# Function to get the HTML content of a website
def get_website_content(url):
    try:
        response = requests.get(f"https://{url}")
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve content for {url}, status code: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Error occurred while getting the website content for {url}: {str(e)}")
        return ""

# Function to check the presence of features in a website's content
def check_features_in_content(content, features_list):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text().lower()
    feature_presence = {}
    for feature in features_list:
        feature_presence[feature] = feature in text
    return feature_presence

# Create a CSV to store the analysis report
report_filename = 'competitive_analysis_report.csv'

# Analyze each competitor
report_data = []

for competitor in [your_company] + competitors:
    website_content = get_website_content(competitor)
    feature_presence = check_features_in_content(website_content, features)
    report_data.append([competitor] + [feature_presence[feature] for feature in features])

# Write to CSV file
with open(report_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Website'] + features)
    for row in report_data:
        writer.writerow(row)

# Convert CSV to Excel for a more user-friendly format (optional)
excel_filename = report_filename.replace('.csv', '.xlsx')
df = pd.read_csv(report_filename)
df.to_excel(excel_filename, index=False)

print(f"Competitive analysis report created successfully as {excel_filename}"