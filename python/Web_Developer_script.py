Sure! Here's a simple example of a Python script that a web developer might use to scrape a website using the Beautiful Soup library.

```python
import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = 'https://www.example.com'
response = requests.get(url)

# Parse the HTML content of the website
soup = BeautifulSoup(response.content, 'html.parser')

# Extract specific elements from the page
title = soup.title.text
links = soup.find_all('a')
paragraphs = soup.find_all('p')

# Print the results
print('Title:', title)
print('Links:')
for link in links:
    print(link.get('href'))
print('Paragraphs:')
for p in paragraphs:
    print(p.text)
```

This script uses the requests library to send a GET request to a website and the Beautiful Soup library to parse the HTML content of the page. It then extracts the title, links, and paragraphs from the page and prints them out.