import requests
from bs4 import BeautifulSoup

def extract_urls(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Base URL to append to relative URLs
        base_url = 'https://www.finder.fi'

        # Find all relevant <a> tags based on the class attributes
        profile_links = soup.find_all('a', class_='SearchResult__ProfileLink')
        other_links = soup.find_all('a', class_='SearchResult__Link')

        # Extract href attributes, convert to absolute URLs, and filter out those containing "kartat"
        urls = [base_url + link.get('href') for link in profile_links + other_links 
                if link.get('href') and 'kartat' not in link.get('href')]

        return urls

    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# List of source URLs
source_urls = [
    '',
    # Add more URLs as needed
]

# Iterate through each source URL and accumulate the extracted URLs
all_extracted_urls = []
for url in source_urls:
    extracted_urls = extract_urls(url)
    if extracted_urls:
        all_extracted_urls.extend(extracted_urls)

# Print each extracted URL on a new line, enclosed in single quotes and followed by a comma
for url in all_extracted_urls:
    print(f"'{url}',")
