from setuptools import setup, find_packages

setup(
    name="okx_news_scraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "okx-scraper=okx_news_scraper.main:main",
        ],
    },
    author="Igor Koptev",
    description="A CLI tool for scraping OKX news articles.",
    url="https://github.com/kippusen/okx-news-scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)