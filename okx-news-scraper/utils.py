import logging
from datetime import datetime

def setup_logging():
    """Configure logging settings for the scraper."""
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Logging is configured.")

def validate_date_format(date_str):
    """Validate and parse date strings."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Date format for '{date_str}' is invalid. Use YYYY-MM-DD.")
