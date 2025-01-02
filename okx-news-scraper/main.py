from okx_news_scraper.scraper import download_okx_news
from okx_news_scraper.utils import setup_logging, validate_date_format
from datetime import datetime 
import argparse

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Download OKX news within a date range.")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format.")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format.")
    parser.add_argument("output_folder", type=str, help="Folder to save the news data.")

    args = parser.parse_args()

    try:
        start_date = validate_date_format(args.start_date)
        end_date = validate_date_format(args.end_date)

        if start_date > end_date:
            raise ValueError("Start date must be earlier than or equal to end date.")

        file_path = download_okx_news(start_date, end_date, args.output_folder)
        print(f"News data saved to {file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
