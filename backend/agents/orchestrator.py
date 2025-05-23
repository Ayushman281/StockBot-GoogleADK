from agents.identify_ticker import IdentifyTickerAgent
from agents.ticker_news import TickerNewsAgent
from agents.ticker_price import TickerPriceAgent
from agents.ticker_price_change import TickerPriceChangeAgent
from agents.ticker_analysis import TickerAnalysisAgent
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockOrchestratorAgent:
    """
    Main orchestrator agent that coordinates the subagents to process stock queries.
    """
    
    def __init__(self):
        self.identify_ticker_agent = IdentifyTickerAgent()
        self.ticker_news_agent = TickerNewsAgent()
        self.ticker_price_agent = TickerPriceAgent()
        self.ticker_price_change_agent = TickerPriceChangeAgent()
        self.ticker_analysis_agent = TickerAnalysisAgent()
    
    def process_query(self, query_text):
        """
        Process a natural language query about stocks.
        
        Args:
            query_text (str): The natural language query text
            
        Returns:
            dict: A dictionary containing the answer and metadata
        """
        # Default response for errors
        default_response = {
            "answer": "Unable to analyze the stock due to insufficient data.",
            "metadata": {
                "ticker": None,
                "company_name": None,
                "current_price": None,
                "price_change": {"success": False, "error": "Processing error"},
                "news": [],
                "analysis": {
                    "summary": "Analysis unavailable",
                    "detailed_analysis": "",
                    "details": {}
                }
            }
        }
        
        try:
            # Parse query to identify ticker symbol and query intent
            ticker_info = self.identify_ticker_agent.identify(query_text)
            ticker = ticker_info.get("ticker")
            timeframe = ticker_info.get("timeframe", "today")
            
            # If no ticker identified, return early
            if not ticker:
                logger.warning("No ticker identified for query: %s", query_text)
                default_response["metadata"]["error"] = "No ticker identified"
                return default_response
            
            logger.info(f"Processing query for ticker: {ticker}, timeframe: {timeframe}")
            
            # Collect data based on identified ticker - with error handling
            try:
                news_data = self.ticker_news_agent.get_news(ticker)
            except Exception as e:
                logger.error(f"Error getting news for {ticker}: {str(e)}")
                news_data = {"headlines": [], "success": False}
            
            try:
                price_data = self.ticker_price_agent.get_price(ticker)
                # Ensure we always have a valid price value to display
                if not price_data.get("price"):
                    logger.warning(f"No price returned for {ticker}, using fallback method")
                    # Try alternative price source if primary failed
                    alt_price_data = self._get_fallback_price(ticker)
                    if alt_price_data and alt_price_data.get("price"):
                        price_data = alt_price_data
            except Exception as e:
                logger.error(f"Error getting price for {ticker}: {str(e)}")
                price_data = {"price": 0.0, "success": False}
            
            try:
                price_change = self.ticker_price_change_agent.get_price_change(ticker, timeframe)
            except Exception as e:
                logger.error(f"Error getting price change for {ticker}: {str(e)}")
                price_change = {
                    "change": None, 
                    "change_percent": None, 
                    "timeframe": timeframe,
                    "success": False,
                    "error": str(e)
                }
            
            # Generate comprehensive analysis
            try:
                analysis = self.ticker_analysis_agent.analyze(
                    ticker=ticker,
                    query=query_text,
                    news=news_data,
                    price=price_data,
                    price_change=price_change,
                    timeframe=timeframe
                )
            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {str(e)}")
                analysis = {
                    "summary": "Unable to generate analysis", 
                    "detailed_analysis": "", 
                    "details": {}, 
                    "success": False
                }
            
            # Add company name if missing
            if "company_name" not in price_data:
                price_data["company_name"] = ticker_info.get("company_name", f"{ticker} Inc.")
            
            return {
                "answer": analysis.get("summary", "Analysis unavailable"),
                "metadata": {
                    "ticker": ticker,
                    "company_name": price_data.get("company_name", ticker_info.get("company_name")),
                    "current_price": price_data.get("price"),  # This should now be more reliable
                    "price_change": price_change,
                    "news": news_data.get("headlines", []),
                    "analysis": {
                        "summary": analysis.get("summary", "No analysis available"),
                        "detailed_analysis": analysis.get("detailed_analysis", ""),
                        "details": analysis.get("details", {})
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error in orchestrator: {str(e)}")
            return default_response
        
    def _get_fallback_price(self, ticker):
        """Try alternative methods to get stock price if primary method fails."""
        try:
            import yfinance as yf
            ticker_data = yf.Ticker(ticker)
            info = ticker_data.info
            if info and "regularMarketPrice" in info:
                return {
                    "price": info["regularMarketPrice"],
                    "currency": "USD",
                    "success": True,
                    "source": "yfinance"
                }
        except:
            pass
        
        # Additional fallback could be added here
        return None
