"""
Configuration settings for E-Commerce Analytics
"""

import os
from pathlib import Path


class Config:
    """Configuration class for the analytics system"""
    
    # Base directories
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / 'data'
    LOG_DIR = BASE_DIR / 'logs'
    REPORTS_DIR = BASE_DIR / 'reports'
    TESTS_DIR = BASE_DIR / 'tests'
    
    # Website settings
    BASE_URL = 'https://www.bestbuy.com'
    
    # Selenium settings
    HEADLESS_MODE = False  # Set to True for production
    IMPLICIT_WAIT = 10  # seconds
    EXPLICIT_WAIT = 15  # seconds
    PAGE_LOAD_DELAY = 3  # seconds
    REQUEST_DELAY = 2  # seconds between requests
    
    # User agent
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Scraping limits
    MAX_PAGES = 5  # Maximum number of product listing pages to scrape
    MAX_PRODUCTS = 50  # Maximum total products to collect
    MAX_PRODUCTS_DETAIL = 20  # Maximum products to get detailed info for
    MAX_REVIEWS_PER_PRODUCT = 50  # Maximum reviews per product
    
    # Filter settings
    PRICE_MIN = 500
    PRICE_MAX = 1500
    MIN_RATING = 4.0
    TOP_BRANDS = ['Dell', 'HP', 'Lenovo']  # Adjust based on site
    
    # Excel settings
    EXCEL_FILENAME = 'ecommerce_analysis.xlsx'
    
    # Report settings
    PDF_REPORT_FILENAME = 'analytics_report.pdf'
    HTML_DASHBOARD_FILENAME = 'dashboard.html'
    
    # Sentiment analysis
    SENTIMENT_MODEL = 'vader'  # or 'textblob'
    
    # Email settings (for bonus feature)
    ENABLE_EMAIL_NOTIFICATIONS = False
    EMAIL_FROM = os.getenv('EMAIL_FROM', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Cache settings (for bonus feature)
    ENABLE_CACHE = True
    CACHE_EXPIRY = 3600  # seconds
    
    # Multi-threading settings (for bonus feature)
    ENABLE_MULTITHREADING = False
    NUM_THREADS = 4
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.TESTS_DIR.mkdir(parents=True, exist_ok=True)


# Create directories on import
Config.create_directories()