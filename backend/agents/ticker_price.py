import logging
import random

logger = logging.getLogger(__name__)

class TickerPriceAgent:
    """
    Agent for retrieving current stock prices.
    """
    
    def __init__(self):
        # Mock prices for common tickers (for demo purposes)
        self.mock_prices = {
            'AAPL': 175.32,
            'TSLA': 243.98,
            'MSFT': 386.24,
            'AMZN': 179.25,
            'GOOGL': 142.65,
            'META': 469.27,
            'NFLX': 628.45,
            'NVDA': 874.50,
            'AMD': 146.72,
            'INTC': 31.21,
        }
    
    def get_price(self, ticker):
        """
        Get the current price for a ticker symbol.
        
        Args:
            ticker (str): The ticker symbol
            
        Returns:
            dict: A dictionary containing the price data
        """
        logger.info(f"Getting price for ticker: {ticker}")
        
        try:
            # In a real implementation, you would make an API call here
            # For this example, we'll use mock data
            if ticker in self.mock_prices:
                price = self.mock_prices[ticker]
            else:
                # Generate a random price for tickers we don't have data for
                price = random.uniform(50.0, 500.0)
            
            return {
                "price": price,
                "currency": "USD",
                "success": True
            }
        except Exception as e:
            logger.error(f"Error retrieving price for {ticker}: {str(e)}")
            return {
                "price": 100.0,  # Default fallback price
                "success": False,
                "error": str(e)
            }
