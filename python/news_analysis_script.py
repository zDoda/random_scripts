#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Ensure that the NLTK stopwords and tokenizer are downloaded.
nltk.download('punkt')
nltk.download('stopwords')

ENGLISH_STOPWORDS = set(stopwords.words('english'))
TRENDING_TOPICS_LIMIT = 10

# Define the sources from where to fetch news
NEWS_SOURCES = [
    'https://news.google.com',
    'https://www.cnn.com/world',
    'https://www.bbc.com/news'
]

def fetch_news(url):
    """Fetch news from a given source URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3')
    return [h.get_text() for h in headlines]

def clean_and_tokenize(text):
    """Clean and tokenize text removing punctuation and stopwords."""
    tokens = nltk.word_tokenize(text)
    return [word for word in tokens if word.isalpha() and word not in ENGLISH_STOPWORDS]

def aggregate_and_analyze(news_sources):
    """Aggregate news from sources and analyze for trending topics."""
    all_headlines = []
    
    for source in news_sources:
        all_headlines.extend(fetch_news(source))

    # Tokenize and clean the headlines
    all_tokens = []
    for headline in all_headlines:
        all_tokens.extend(clean_and_tokenize(headline.lower()))

    # Frequency distribution of words
    frequency_distribution = Counter(all_tokens)
    
    # Find trending topics by taking the most common words
    trending = frequency_distribution.most_common(TRENDING_TOPICS_LIMIT)
    
    # Plotting trend analysis
    words = [item[0] for item in trending]
    counts = [item[1] for item in trending]
    
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Trend Analysis')
    plt.xticks(rotation=90)
    plt.show()

    return trending

if __name__ == "__main__":
    trending_topics = aggregate_and_analyze(NEWS_SOURCES)
    print("Trending topics:")
    for topic in trending_topics:
        print(f"Topic: {topic[0]}, Count: {topic[1]}")
