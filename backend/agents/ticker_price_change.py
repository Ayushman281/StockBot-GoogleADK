from api.fmp_api import FinancialModelingPrepAPI  # Change import
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class TickerPriceChangeAgent:
    """
    Agent responsible for calculating price changes over a timeframe.
    """
    
    def __init__(self):
        self.stock_api = FinancialModelingPrepAPI()  # Use FMP instead of Alpha Vantage
    
    def get_price_change(self, ticker, timeframe="today"):
        """
        Calculate price change for the given ticker over the specified timeframe.
        """
        if not ticker:
            return {
                "change": None,
                "change_percent": None,
                "timeframe": timeframe,
                "success": False,
                "error": "No ticker provided"
            }
        
        try:
            # Get daily time series data from the API
            time_series = self.stock_api.get_daily_time_series(ticker, outputsize="compact")
            
            # Check if we have data
            if not time_series or len(time_series) == 0:
                logger.error(f"No historical data available for {ticker}")
                return {
                    "change": None,
                    "change_percent": None,
                    "timeframe": timeframe,
                    "success": False,
                    "error": "No historical data available"
                }
            
            # Convert to a more usable format
            dates = list(time_series.keys())
            dates.sort(reverse=True)  # Most recent first
            
            if len(dates) < 2:
                return {
                    "change": None,
                    "change_percent": None,
                    "timeframe": timeframe,
                    "success": False,
                    "error": "Insufficient historical data points"
                }
            
            # Get today's close and previous close
            latest = time_series[dates[0]]
            latest_close = float(latest["4. close"])
            
            # Handle different timeframes
            if timeframe == "today":
                # For today, compare to previous day's close
                previous = time_series[dates[1]]
                previous_close = float(previous["4. close"])
                
            elif timeframe in ["week", "7days"]:
                # Find data point ~7 days ago
                index = min(7, len(dates) - 1)
                previous = time_series[dates[index]]
                previous_close = float(previous["4. close"])
                
            elif timeframe in ["month", "30days"]:
                # Find data point ~30 days ago
                index = min(30, len(dates) - 1)
                previous = time_series[dates[index]]
                previous_close = float(previous["4. close"])
                
            else:
                # Default to previous day
                previous = time_series[dates[1]]
                previous_close = float(previous["4. close"])
            
            # Calculate changes
            change = latest_close - previous_close
            change_percent = (change / previous_close) * 100
            
            return {
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "from_price": previous_close,
                "to_price": latest_close,
                "timeframe": timeframe,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error calculating price change for {ticker}: {str(e)}")
            return {
                "change": None,
                "change_percent": None,
                "timeframe": timeframe,
                "success": False,
                "error": str(e)
            }
