#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# Path to your marketing campaign data file (CSV)
# The CSV should have columns like campaign_name, clicks, impressions, cost, conversions
data_file_path = 'marketing_campaign_data.csv'

# Load data using pandas
campaign_data = pd.read_csv(data_file_path)

# Calculate Key Performance Indicators (KPIs)
campaign_data['CTR'] = campaign_data['clicks'] / campaign_data['impressions']  # Click-Through Rate
campaign_data['CPC'] = campaign_data['cost'] / campaign_data['clicks']  # Cost Per Click
campaign_data['CPA'] = campaign_data['cost'] / campaign_data['conversions']  # Cost Per Acquisition
campaign_data['ROAS'] = campaign_data['revenue'] / campaign_data['cost']  # Return on Advertising Spend
campaign_data['ConversionRate'] = campaign_data['conversions'] / campaign_data['clicks']  # Conversion Rate

# Print summary stats
print("Summary statistics for campaigns:")
print(campaign_data.describe())

# Analysis of Campaign Effectiveness
# Sorting data based on effectiveness (e.g., by CPA or ROAS)
campaign_sorted_by_cpa = campaign_data.sort_values(by='CPA', ascending=True)
campaign_sorted_by_roas = campaign_data.sort_values(by='ROAS', ascending=False)

# Plotting data for visual analysis
plt.figure(figsize=(10, 6))

# Plotting CPA
plt.subplot(1, 2, 1)
plt.bar(campaign_sorted_by_cpa['campaign_name'], campaign_sorted_by_cpa['CPA'], color='blue')
plt.xlabel('Campaign')
plt.ylabel('CPA')
plt.title('Campaign Cost Per Acquisition')
plt.xticks(rotation=90)

# Plotting ROAS
plt.subplot(1, 2, 2)
plt.bar(campaign_sorted_by_roas['campaign_name'], campaign_sorted_by_roas['ROAS'], color='green')
plt.xlabel('Campaign')
plt.ylabel('ROAS')
plt.title('Return on Advertising Spend')
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()

# Save processed data to a new CSV
processed_file_path = 'processed_marketing_campaign_data.csv'
campaign_data.to_csv(processed_file_path, index=False)
