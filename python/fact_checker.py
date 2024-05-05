#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import nltk
from newspaper import Article
from textblob import TextBlob
import spacy

# Load Spacy's English language model
nlp = spacy.load("en_core_web_sm")

# List of reliable source URLs
reliable_sources = [
    'https://www.bbc.com/news',
    'https://www.nytimes.com',
    'https://www.theguardian.com',
    # ...
]

# Fact-check function
def fact_check(statement):
    # Tokenize the statement
    doc = nlp(statement)
    # Find named entities, phrases, and concepts
    entities = [ent.text for ent in doc.ents]

    for entity in entities:
        for source in reliable_sources:
            # Search for the entity in each reliable source
            response = requests.get(f"{source}/search?q={entity}")
            # Check if there is an article available in the source about the entity
            if response.status_code == 200:
                source_content = response.content
                soup = BeautifulSoup(source_content, 'html.parser')
                articles = soup.find_all('article')
                for article in articles:
                    try:
                        article_url = article.find('a')['href']
                        # Check for full URL or relative path
                        if not article_url.startswith('http'):
                            article_url = f"{source}{article_url}"
                        # Fetch article content
                        article_page = Article(article_url)
                        article_page.download()
                        article_page.parse()
                        # Fact-checking by comparing statements
                        if entity.lower() in article_page.text.lower():
                            print(f"Entity '{entity}' found in article: {article_url}")
                            return True
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        continue
    return False

# Test a statement for fact-checking
test_statement = "The COVID-19 pandemic began in 2019."
checked_fact = fact_check(test_statement)

if checked_fact:
    print("Statement is found in reliable sources.")
else:
    print("Statement couldn't be verified or is not present in the reliable sources."