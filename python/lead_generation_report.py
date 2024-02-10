#!/usr/bin/env python3

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_webpage(url):
    # Scrape the website
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    leads = []

    # Extract leads
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        if columns:
            lead_info = {
                'Name': columns[0].text.strip(),
                'Email': columns[1].text.strip(),
                'Phone': columns[2].text.strip(),
                'Interest': columns[3].text.strip(),
                'Date': columns[4].text.strip(),
            }
            leads.append(lead_info)

    return leads

def generate_report(leads, filename):
    # Generate a lead generation report
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=leads[0].keys())
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead)

def main():
    url = 'http://example.com/leads' # Replace with your actual URL
    report_filename = f'lead_generation_report_{datetime.now().strftime("%Y%m%d")}.csv'
    
    leads = scrape_webpage(url)
    generate_report(leads, report_filename)
    print(f"Lead generation report has been generated: {report_filename}")

if __name__ == '__main__':
    main()
