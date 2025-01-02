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

def download_okx_news(start_date, end_date, folder):
    """Download news articles from OKX within a date range."""
    if not os.path.exists(folder):
        os.makedirs(folder)

    current_url = "https://www.okx.com/help/category/announcements"
    all_news_data = []
    earliest_date = None

    while current_url:
        response = requests.get(current_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {current_url}")

        soup = BeautifulSoup(response.content, 'html.parser')
        news_data, page_earliest_date = scrape_page_articles(soup, start_date, end_date)
        all_news_data.extend(news_data)

        if earliest_date is None or (page_earliest_date and page_earliest_date < earliest_date):
            earliest_date = page_earliest_date

        if earliest_date and earliest_date > start_date:
            current_url = get_next_page_url(soup)
        else:
            current_url = None

    file_path = os.path.join(folder, f"okx_news_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json")
    with open(file_path, 'w') as f:
        json.dump(all_news_data, f, indent=4)

    return file_path


# download_okx_news(datetime(2020, 10, 1), datetime(2020, 10, 30), './output')
