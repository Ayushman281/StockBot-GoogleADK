import os
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

logger = logging.getLogger(__name__)

class FinancialModelingPrepAPI:
    """
    Client for the Financial Modeling Prep API.
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.base_url = "https://financialmodelingprep.com/api/v3"
        
        if not self.api_key:
            raise ValueError("FMP API key not found in environment variables")
    
    def get_quote(self, symbol):
        """Get current quote data for a symbol."""
        logger.info(f"Fetching quote for {symbol}")
        
        url = f"{self.base_url}/quote/{symbol}?apikey={self.api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error fetching quote: {response.status_code}")
                return None
                
            data = response.json()
            
            if not data:
                logger.warning(f"No quote data returned for {symbol}")
                return None
            
            # Format data to match Alpha Vantage structure for compatibility
            quote_data = data[0]
            return {
                "01. symbol": quote_data["symbol"],
                "02. open": str(quote_data["open"]),
                "03. high": str(quote_data["dayHigh"]),
                "04. low": str(quote_data["dayLow"]),
                "05. price": str(quote_data["price"]),
                "06. volume": str(quote_data["volume"]),
                "07. latest trading day": quote_data["date"],
                "08. previous close": str(quote_data["previousClose"]),
                "09. change": str(quote_data["change"]),
                "10. change percent": str(quote_data["changesPercentage"]) + "%"
            }
            
        except Exception as e:
            logger.error(f"Exception fetching quote: {str(e)}")
            return None
    
    def get_daily_time_series(self, symbol, outputsize="compact"):
        """Get daily time series data for a symbol."""
        logger.info(f"Fetching daily time series for {symbol}")
        
        # Determine number of data points based on outputsize
        limit = 100 if outputsize == "compact" else 5000
        
        url = f"{self.base_url}/historical-price-full/{symbol}?apikey={self.api_key}&limit={limit}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error fetching time series: {response.status_code}")
                return None
                
            data = response.json()
            
            if "historical" not in data or not data["historical"]:
                logger.warning(f"No historical data returned for {symbol}")
                return None
            
            # Format data to match Alpha Vantage structure for compatibility
            historical_data = {}
            for item in data["historical"]:
                date_str = item["date"]  # Format: YYYY-MM-DD
                historical_data[date_str] = {
                    "1. open": str(item["open"]),
                    "2. high": str(item["high"]),
                    "3. low": str(item["low"]),
                    "4. close": str(item["close"]),
                    "5. volume": str(item["volume"])
                }
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Exception fetching time series: {str(e)}")
            return None
    
    def search_symbol(self, keywords):
        """Search for stock symbols based on keywords."""
        logger.info(f"Searching for symbols with keywords: {keywords}")
        
        url = f"{self.base_url}/search?query={keywords}&limit=10&apikey={self.api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error searching symbols: {response.status_code}")
                return None
                
            data = response.json()
            
            if not data:
                logger.warning(f"No matches found for {keywords}")
                return None
            
            # Format data to match Alpha Vantage structure for compatibility
            results = []
            for item in data:
                results.append({
                    "1. symbol": item["symbol"],
                    "2. name": item["name"],
                    "3. type": "Equity",
                    "4. region": item.get("exchangeShortName", "US"),
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "1.0"
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Exception searching symbols: {str(e)}")
            return None