#!/usr/bin/env python3

# Environmental Impact Assessment Automation Script

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuration: Placeholder paths and dummy data for the example.
PROJECT_DESCRIPTIONS_PATH = "project_descriptions.csv"
ENVIRONMENTAL_FACTORS_PATH = "environmental_factors.csv"
EIA_REPORT_SAVE_PATH = "eia_report.txt"

# Load project descriptions
projects_df = pd.read_csv(PROJECT_DESCRIPTIONS_PATH)

# Load environmental factors
environmental_factors_df = pd.read_csv(ENVIRONMENTAL_FACTORS_PATH)

# Function to evaluate environmental impact
def evaluate_impact(project_desc, environmental_factors):
    # Use TF-IDF Vectorizer to convert a collection of raw documents to a matrix of TF-IDF features
    vectorizer = TfidfVectorizer(stop_words='english')

    # Document consisting of all concatenated project descriptions and environmental factors
    docs = [project_desc] + environmental_factors['factor'].tolist()
    tfidf_matrix = vectorizer.fit_transform(docs)
    
    # Calculate cosine similarity between the project description and each environmental factor
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Combine environmental factors with their respective similarity scores
    impact_scores = list(zip(environmental_factors['factor'], cosine_similarities))
    
    # Sort by similarity score in descending order to determine the most impacted factors
    sorted_impact_scores = sorted(impact_scores, key=lambda x: x[1], reverse=True)
    
    return sorted_impact_scores

# Process each project
for index, project in projects_df.iterrows():
    project_desc = project['description']
    impacts = evaluate_impact(project_desc, environmental_factors_df)
    
    # Generate a simple report for the project's environmental impact
    with open(EIA_REPORT_SAVE_PATH.format(id=project['id']), 'w') as report_file:
        report_file.write(f"Environmental Impact Assessment Report for Project {project['id']}\n")
        report_file.write(f"Project Description: {project_desc}\n\n")
        report_file.write("Estimated Environmental Factors Impact:\n")
        for factor, score in impacts:
            report_file.write(f"- {factor}: {score:.2f}\n")

print("Environmental Impact Assessments have been generated and saved.")
