import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

class NewsAPI:
    """
    Client for interacting with a news API to get stock-related news.
    """
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
        
        if not self.api_key:
            raise ValueError("News API key not found in environment variables")
    
    def get_company_news(self, ticker, days=7):
        """
        Get news articles about a company based on its ticker symbol.
        
        Args:
            ticker (str): The stock ticker symbol
            days (int): Number of days to look back for news
            
        Returns:
            list: News articles
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for the API
        from_date = start_date.strftime("%Y-%m-%d")
        to_date = end_date.strftime("%Y-%m-%d")
        
        # Construct query using the ticker symbol and company name
        query = f"{ticker} stock"
        
        params = {
            "q": query,
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "relevancy",
            "apiKey": self.api_key
        }
        
        response = requests.get(f"{self.base_url}/everything", params=params)
        data = response.json()
        
        # Check for error responses
        if response.status_code != 200:
            raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")
        
        # Return articles or empty list if none found
        return data.get("articles", [])
