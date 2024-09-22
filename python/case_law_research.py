#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re

class CaseLawResearch:
    def __init__(self, base_url):
        self.base_url = base_url

    def search_case_law(self, query, num_results=10):
        # Construct the search URL
        search_url = f"{self.base_url}/search?q={query}"
        # Fetch search results
        response = requests.get(search_url)
        if response.status_code == 200:
            return self._parse_search_results(response.text, num_results)
        else:
            print("Failed to retrieve search results")
            return None

    def _parse_search_results(self, html_content, num_results):
        # Parse the search results using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        cases = []

        # Find case law search results
        search_results = soup.find_all('div', class_='search-result')
        for result in search_results[:num_results]:
            title = result.find('a').text.strip()
            link = result.find('a')['href']
            snippet = result.find('div', class_='search-snippet').text.strip()

            # Cleaning up the link to be a full URL if it is relative
            if link.startswith('/'):
                link = f"{self.base_url}{link}"

            cases.append({
                'title': title,
                'link': link,
                'snippet': snippet
            })

        return cases

    def get_case_text(self, case_url):
        # Fetch the full text of a case law
        response = requests.get(case_url)
        if response.status_code == 200:
            return self._extract_case_text(response.text)
        else:
            print(f"Failed to retrieve case text from {case_url}")
            return None

    def _extract_case_text(self, html_content):
        # Parse the full text of case law using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Assuming that the case text is contained within a specific tag, e.g., a <div> with class "case-text"
        case_text_div = soup.find('div', class_='case-text')
        if case_text_div:
            return case_text_div.get_text(strip=True)
        else:
            print("Case text not found in the provided HTML content.")
            return None


# Usage example
if __name__ == "__main__":
    BASE_URL = "https://www.examplecaselaw.com"  # Replace with actual case law database URL
    SEARCH_QUERY = "intellectual property rights"

    research_tool = CaseLawResearch(BASE_URL)

    # Search for case law related to the query
    cases = research_tool.search_case_law(SEARCH_QUERY)
    for case in cases:
        print(f"Title: {case['title']}")
        print(f"Link: {case['link']}")
        print(f"Snippet: {case['snippet']}")
        print("---------------------------------------------------")

    # Optionally, retrieve the full text of a particular case
    if cases:
        case_text = research_tool.get_case_text(cases[0]['link'])
        print(f"Case Text for {cases[0]['title']}:")
        print(case_text