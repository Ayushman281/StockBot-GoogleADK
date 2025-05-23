import os
import requests
import logging
import time
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

logger = logging.getLogger(__name__)

class AlphaVantageAPI:
    """
    Client for the Alpha Vantage API.
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.base_url = "https://www.alphavantage.co/query"
        self.last_call_time = 0
        self.min_call_interval = 12  # seconds, to avoid hitting rate limits
        
        if not self.api_key:
            raise ValueError("Alpha Vantage API key not found in environment variables")
    
    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits."""
        current_time = time.time()
        elapsed = current_time - self.last_call_time
        
        if elapsed < self.min_call_interval:
            time.sleep(self.min_call_interval - elapsed)
        
        self.last_call_time = time.time()
    
    def get_quote(self, symbol):
        """
        Get current quote data for a symbol.
        """
        self._rate_limit()
        logger.info(f"Fetching quote for {symbol}")
        
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error fetching quote: {response.status_code}")
                return None
                
            data = response.json()
            
            # Alpha Vantage returns an empty object or error message when rate limited
            if "Global Quote" not in data or not data["Global Quote"]:
                logger.warning(f"No quote data returned: {data}")
                return None
                
            return data["Global Quote"]
            
        except Exception as e:
            logger.error(f"Exception fetching quote: {str(e)}")
            return None
    
    def get_daily_time_series(self, symbol, outputsize="compact"):
        """
        Get daily time series data for a symbol.
        
        Args:
            symbol (str): Stock ticker symbol
            outputsize (str): 'compact' for last 100 data points, 'full' for 20+ years of data
        """
        self._rate_limit()
        logger.info(f"Fetching daily time series for {symbol}")
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error fetching time series: {response.status_code}")
                return None
                
            data = response.json()
            
            # Check for rate limit or error messages
            if "Time Series (Daily)" not in data:
                logger.warning(f"No time series data returned: {data}")
                if "Note" in data:
                    logger.error(f"API Note: {data['Note']}")
                if "Information" in data:
                    logger.error(f"API Information: {data['Information']}")
                return None
                
            return data["Time Series (Daily)"]
            
        except Exception as e:
            logger.error(f"Exception fetching time series: {str(e)}")
            return None
    
    def search_symbol(self, keywords):
        """
        Search for stock symbols based on keywords.
        
        Args:
            keywords (str): Search keywords or company name
            
        Returns:
            list: Matching stock symbols and companies
        """
        self._rate_limit()
        logger.info(f"Searching for symbols with keywords: {keywords}")
        
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": keywords,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error searching symbols: {response.status_code}")
                return None
                
            data = response.json()
            
            # Check for rate limit or error messages
            if "bestMatches" not in data:
                logger.warning(f"No matches found: {data}")
                if "Note" in data:
                    logger.error(f"API Note: {data['Note']}")
                if "Information" in data:
                    logger.error(f"API Information: {data['Information']}")
                return None
                
            return data["bestMatches"]
            
        except Exception as e:
            logger.error(f"Exception searching symbols: {str(e)}")
            return None
