# Project: OKX News Scraper
# Structure Suggestions:
# 1. scraper.py - Core scraping logic
# 2. utils.py - Helper functions
# 3. main.py - Entry point for CLI
# 4. setup.py - For installation and versioning
# 5. requirements.txt - List of dependencies

# First File: scraper.py
# This contains the main logic of scraping
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging

def get_next_page_url(soup):
    """Get the URL of the next page."""
    next_link = soup.find('a', class_='okui-powerLink-a11y okui-powerLink okui-pagination-next')
    if next_link and 'href' in next_link.attrs:
        #print(f"https://www.okx.com{next_link['href']}") #debuggin purpose
        return f"https://www.okx.com{next_link['href']}"
    return None

def scrape_page_articles(soup, start_date, end_date):
    """Scrape articles on the given page."""
    articles = soup.find_all('li', class_='index_articleItem__d-8iK')
    news_data = []
    earliest_date = None

    for article in articles:
        date_str = article.find('span', {'data-testid': 'DateDisplay'}).text.strip().replace('Published on ', '')
        article_date = datetime.strptime(date_str, '%b %d, %Y')

        if earliest_date is None or article_date < earliest_date:
            earliest_date = article_date

        #print(article_date, start_date, end_date) #debuggin purpose    
        if start_date <= article_date <= end_date:
            title = article.find('div', class_='index_title__iTmos index_articleTitle__ys7G7').text.strip()
            link = article.find('a', class_='okui-powerLink-a11y okui-powerLink index_articleLink__Z6ycB')['href']
            full_link = f"https://www.okx.com{link}"

            article_response = requests.get(full_link)
            if article_response.status_code == 200:
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                content_div = article_soup.find('div', class_=['index_richTextContent__9H5yk', 'index_markdownContent__YOE4e'])

                if content_div:
                    text_content = content_div.get_text(separator='\n', strip=True)
                    html_content = str(content_div)
                    news_data.append({
                        'date': article_date.strftime('%Y-%m-%d'),
                        'title': title,
                        'link': full_link,
                        'content_text': text_content,
                        'content_html': html_content
                    })
    #print(news_data, earliest_date) #debuggin purpose
    return news_data, earliest_date

def create_session():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def download_okx_news(start_date, end_date, folder):
    """Download news articles from OKX within a date range."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, f"okx_news_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json")
    current_url = "https://www.okx.com/help/category/announcements"
    all_news_data = []
    earliest_date = None

    session = create_session()

    # Write data in batches
    BATCH_SIZE = 100
    current_batch = []
    
    while current_url:
        try:
            response = session.get(current_url, timeout=30)
            # Add rate limiting
            time.sleep(1)  # Wait 1 second between requests
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data from {current_url}")

            soup = BeautifulSoup(response.content, 'html.parser')
            news_data, page_earliest_date = scrape_page_articles(soup, start_date, end_date)
            current_batch.extend(news_data)

            if earliest_date is None or (page_earliest_date and page_earliest_date < earliest_date):
                earliest_date = page_earliest_date

                if earliest_date and earliest_date > start_date:
                    current_url = get_next_page_url(soup)
                else:
                    current_url = None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {current_url}: {e}")
            raise

        # Write batch to file when it reaches the threshold
        if len(current_batch) >= BATCH_SIZE:
            write_batch_to_file(current_batch, file_path)
            current_batch = []
    
    # Write remaining articles
    if current_batch:
        write_batch_to_file(current_batch, file_path)

    return file_path

def write_batch_to_file(batch, file_path):
    """Write a batch of articles to file"""
    mode = 'w' if not os.path.exists(file_path) else 'r+'
    try:
        with open(file_path, mode) as f:
            if mode == 'r+':
                # Read existing data
                f.seek(0)
                existing_data = json.load(f)
                existing_data.extend(batch)
                batch = existing_data
                f.seek(0)
            json.dump(batch, f, indent=4)
    except Exception as e:
        logging.error(f"Error writing to file: {e}")
        raise

download_okx_news(datetime(2020, 10, 1), datetime(2020, 10, 30), './output')
