# Project: OKX News Scraper

This project scrape news from https://www.okx.com/help/category/announcements into json file for future analysis

## Installation

- Install latest version from git repository using pip:
```bash
$ pip install git+https://github.com/kippusen/okx-news-scraper.git
```

- Install from source:
```bash
$ pip install .
```

## How to use

"okx-scraper START_DATE END_DATE FOLDER". Example:
```bash
$ okx-scraper 2024-12-01 2024-12-31 ./output
```
## Structure:

- scraper.py - Core scraping logic
- utils.py - Helper functions
- main.py - Entry point for CLI
- setup.py - For installation and versioning
- requirements.txt - List of dependencies
