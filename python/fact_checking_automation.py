#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import spacy

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

# List of credible sources
trusted_sources = [
    'bbc.com',
    'reuters.com',
    'theguardian.com',
    'npr.org'
]

# Function to check if the URL is from a trusted source
def is_trusted_source(url):
    parsed_url = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_url).replace('www.', '')
    return domain in trusted_sources

# Function to extract the body text from a webpage
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join(paragraph.text for paragraph in paragraphs)
        return article_text
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None

# Function to check if a claim is in the article text
def check_claim_in_text(claim, text):
    doc = nlp(claim)
    claim_ents = {ent.text.lower() for ent in doc.ents}

    doc = nlp(text)
    text_ents = {ent.text.lower() for ent in doc.ents}

    return claim_ents.issubset(text_ents)

# Main function to check a list of claims against a list of sources
def fact_check_claims(claims, sources):
    for claim in claims:
        print(f"Fact-checking claim: {claim}")
        claim_verified = False

        for source in sources:
            if is_trusted_source(source):
                article_text = extract_text_from_url(source)
                if article_text and check_claim_in_text(claim, article_text):
                    print(f"Claim \"{claim}\" verified by trusted source: {source}")
                    claim_verified = True
                    break
            else:
                print(f"Source {source} is not trusted.")
        
        if not claim_verified:
            print(f"Claim \"{claim}\" could not be verified by any of the trusted sources provided.")

# Example usage
claims_to_check = [
    "France is planning to ban diesel cars by 2040.",
    "The CEO of Acme Corp has announced a new product."
]

sources_to_check = [
    "https://www.bbc.com/news/world-europe-40518293",
    "https://www.reuters.com/article/us-autos-france-idUSKBN19S1I3",
    "https://example.com/news/latest-product"
]

if __name__ == "__main__":
    fact_check_claims(claims_to_check, sources_to_check)
