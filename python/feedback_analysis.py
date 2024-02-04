#!/usr/bin/env python3

import json
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter

def load_feedback(file_path):
    with open(file_path, 'r') as file:
        feedback_data = json.load(file)
    return feedback_data

def analyze_sentiment(feedback):
    polarity_scores = []
    for review in feedback:
        blob = TextBlob(review.get('comment', ''))
        polarity_scores.append(blob.sentiment.polarity)
    return polarity_scores

def plot_sentiment_histogram(polarity_scores):
    plt.hist(polarity_scores, bins=20, color='blue', edgecolor='black')
    plt.title('Histogram of User Feedback Sentiment Scores')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.axvline(0, color='red', linestyle='dashed', linewidth=1)  # Add a line at polarity 0
    plt.show()

def get_most_common_words(feedback, num_words=10):
    all_words = ' '.join([review.get('comment', '').lower() for review in feedback])
    blob = TextBlob(all_words)
    word_counts = Counter(blob.words).most_common(num_words)
    return word_counts

def plot_word_frequency(word_counts):
    words, counts = zip(*word_counts)
    plt.bar(words, counts)
    plt.title('Most Common Words in User Feedback')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    feedback_file_path = 'user_feedback.json'  # Assume feedback data is in JSON format
    feedback_data = load_feedback(feedback_file_path)
    
    sentiment_scores = analyze_sentiment(feedback_data)
    plot_sentiment_histogram(sentiment_scores)
    
    most_common_words = get_most_common_words(feedback_data)
    plot_word_frequency(most_common_words)
