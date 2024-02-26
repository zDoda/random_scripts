#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Sample data file path
data_file = 'campaign_data.csv'

# Read dataset
df = pd.read_csv(data_file)

# Print basic statistics
print(df.describe())
print(df.head())

# Assume 'response' column records if the target customer responded to the campaign
# and 'campaign_cost' column records the cost of the campaign for each instance
response_rate = df['response'].mean()
campaign_cost = df['campaign_cost'].sum()
print(f"Response rate: {response_rate:.2%}")
print(f"Total campaign cost: {campaign_cost}")

# Calculate cost per acquisition
acquisition = df[df['response'] == 1]
cost_per_acquisition = campaign_cost / len(acquisition)
print(f"Cost per acquisition: {cost_per_acquisition:.2f}")

# Create a ROC curve
# Assuming there's a probability score 'score' for predicting the 'response'
fpr, tpr, thresholds = roc_curve(df['response'], df['score'])
roc_auc = auc(fpr, tpr)

# Plot a ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

# Save ROC curve
plt.savefig("roc_curve.png")
