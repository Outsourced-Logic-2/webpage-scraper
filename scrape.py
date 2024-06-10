import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def fetch_url_content(url):
    print(f"Fetching content from {url}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

def extract_text_from_html(html_content):
    print("Extracting text from HTML...")
    if not html_content.strip():  # Check if the content is empty or whitespace
        print("No HTML content to parse.")
        return ""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def get_all_hyperlinks(html_content, base_url):
    print("Extracting hyperlinks from HTML...")
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if 'docs.multion.ai' in urljoin(base_url, a['href'])]
    return links

def scrape_hyperlinked_pages(main_url):
    print(f"Starting scraping from main URL: {main_url}")
    main_page_content = fetch_url_content(main_url)
    hyperlinks = get_all_hyperlinks(main_page_content, main_url)
    print(f"Found {len(hyperlinks)} links to scrape.")
    pages_text = {}

    for link in hyperlinks:
        time.sleep(1)  # Delay to prevent being blocked by the server
        page_content = fetch_url_content(link)
        plain_text = extract_text_from_html(page_content)
        pages_text[link] = plain_text

    return pages_text

def save_texts_to_file(texts, file_name):
    print(f"Saving scraped texts to {file_name}...")
    with open(file_name, 'w', encoding='utf-8') as file:
        for url, text in texts.items():
            file.write(f"URL: {url}\n{text}\n\n")
    print("Saving completed.")

# Main URL to start with
main_url = 'https://docs.multion.ai/get-started/welcome'

# Scrape the hyperlinked pages from the given main URL
all_texts = scrape_hyperlinked_pages(main_url)

# Save the scraped texts to a file
save_texts_to_file(all_texts, 'scraped_texts.txt')

print("Script completed.")
