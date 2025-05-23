from api.fmp_api import FinancialModelingPrepAPI  # Change import

class TickerPriceAgent:
    """
    Agent responsible for fetching current price data for a stock.
    """
    
    def __init__(self):
        self.stock_api = FinancialModelingPrepAPI()  # Use FMP instead of Alpha Vantage
    
    def get_price(self, ticker):
        """
        Get the current price for the given ticker.
        """
        if not ticker:
            return {
                "price": None,
                "currency": "USD",
                "timestamp": None,
                "success": False,
                "error": "No ticker provided"
            }
        
        try:
            # Get quote data from the API
            quote = self.stock_api.get_quote(ticker)
            
            # Check if we actually got data
            if not quote:
                return {
                    "price": None,
                    "currency": "USD",
                    "timestamp": None,
                    "success": False,
                    "error": "No quote data returned from API"
                }
            
            # Try to get price with proper error handling
            try:
                price = float(quote.get("05. price", 0))
            except (ValueError, TypeError):
                price = 0.0
            
            # Check if we got a valid price
            if price <= 0:
                return {
                    "price": None,
                    "currency": "USD",
                    "timestamp": None,
                    "company_name": ticker,
                    "success": False,
                    "error": "Invalid price returned"
                }
            
            return {
                "price": price,
                "currency": "USD",
                "timestamp": quote.get("07. latest trading day", ""),
                "company_name": f"{ticker}, Inc.",  # Add company name for display
                "success": True
            }
            
        except Exception as e:
            return {
                "price": None,
                "currency": "USD",
                "timestamp": None,
                "company_name": ticker,
                "success": False,
                "error": str(e)
            }
