from datetime import datetime
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TickerAnalysisAgent:
    """
    Agent responsible for analyzing and summarizing stock price movements
    based on news and historical price data.
    """
    
    def __init__(self):
        pass
    
    def analyze(self, ticker, query, news, price, price_change, timeframe):
        """
        Analyze stock data and news to explain price movements.
        """
        logger.info(f"Analyzing {ticker} with data: price_success={price.get('success')}, price_change_success={price_change.get('success')}")
        
        # Only require ticker, don't fail if price data is incomplete
        if not ticker:
            return {
                "summary": "Unable to analyze without a valid stock ticker.",
                "details": {},
                "success": False
            }
        
        # Get key data points - with fallbacks for missing data
        current_price = price.get("price")
        change = price_change.get("change")
        change_percent = price_change.get("change_percent")
        company_name = price.get("company_name", ticker)
        
        # Use news even if we don't have price data
        has_news = bool(news.get("headlines"))
        has_price = current_price is not None and current_price > 0
        has_change = change is not None and change_percent is not None
        
        # Process news for analysis
        headlines = news.get("headlines", [])
        news_analysis = []
        
        for headline in headlines:
            sentiment = self._analyze_sentiment(headline)
            news_analysis.append({
                "headline": headline,
                "sentiment": sentiment
            })
        
        # Generate an appropriate summary based on available data
        if "why" in query.lower():
            summary = self._generate_why_summary(ticker, company_name, timeframe, 
                                              has_price, current_price,
                                              has_change, change, change_percent,
                                              has_news, news_analysis)
        elif "what's happening" in query.lower() or "what is happening" in query.lower():
            summary = self._generate_whats_happening_summary(ticker, company_name, timeframe,
                                                          has_price, current_price,
                                                          has_change, change, change_percent,
                                                          has_news, news_analysis)
        elif "how has" in query.lower():
            summary = self._generate_how_has_summary(ticker, company_name, timeframe,
                                                  has_price, current_price,
                                                  has_change, change, change_percent,
                                                  has_news, news_analysis)
        else:
            # Default summary
            summary = self._generate_default_summary(ticker, company_name, timeframe,
                                                  has_price, current_price,
                                                  has_change, change, change_percent,
                                                  has_news, news_analysis)
        
        # Create details with whatever data we have
        details = {}
        
        if has_price or has_change:
            details["price_analysis"] = {
                "timeframe": timeframe
            }
            
            if has_price:
                details["price_analysis"]["current_price"] = current_price
                
            if has_change:
                details["price_analysis"]["change"] = change
                details["price_analysis"]["change_percent"] = change_percent
                details["price_analysis"]["direction"] = "up" if change > 0 else "down" if change < 0 else "flat"
        
        if has_news:
            details["news_analysis"] = {
                "headlines": [item["headline"] for item in news_analysis[:5]],
                "sentiments": [item["sentiment"] for item in news_analysis[:5]],
                "news_count": len(headlines)
            }
        
        return {
            "summary": summary,
            "details": details,
            "success": True
        }
    
    def _analyze_sentiment(self, headline):
        """Simple keyword-based sentiment analysis."""
        headline_lower = headline.lower()
        
        positive_keywords = ["up", "rise", "gain", "growth", "profit", "success", "positive", "bullish", "recover"]
        negative_keywords = ["down", "drop", "fall", "loss", "decline", "risk", "bearish", "concern", "layoff"]
        
        positive_score = sum(1 for word in positive_keywords if word in headline_lower)
        negative_score = sum(1 for word in negative_keywords if word in headline_lower)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"
    
    def _generate_why_summary(self, ticker, company_name, timeframe, has_price, price, 
                            has_change, change, change_percent, has_news, news_analysis):
        """Generate summary for 'why' questions."""
        if has_change:
            direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
            summary = f"{company_name} stock {direction} by {abs(change_percent):.2f}% {timeframe}. "
            
            if has_news and news_analysis:
                # Find news with matching sentiment to the price change
                expected_sentiment = "positive" if change > 0 else "negative" if change < 0 else "neutral"
                matching_news = [item for item in news_analysis if item["sentiment"] == expected_sentiment]
                
                if matching_news:
                    summary += f"This appears to be related to recent news: {matching_news[0]['headline']}"
                else:
                    summary += f"Recent news includes: {news_analysis[0]['headline']}"
            else:
                summary += "No specific news was found to explain this movement."
        elif has_news:
            summary = f"For {company_name}, recent news includes: {news_analysis[0]['headline']}"
        else:
            summary = f"Unable to determine why {company_name} stock moved {timeframe} due to insufficient data."
        
        return summary
    
    def _generate_whats_happening_summary(self, ticker, company_name, timeframe, has_price, price,
                                       has_change, change, change_percent, has_news, news_analysis):
        """Generate summary for 'what's happening' questions."""
        summary = f"For {company_name} "
        
        if has_price:
            summary += f"(currently trading at ${price:.2f}) "
            
        if has_change:
            direction = "up" if change > 0 else "down" if change < 0 else "stable"
            summary += f"the stock is {direction} by {abs(change_percent):.2f}% {timeframe}. "
        else:
            summary += "current price movement data is unavailable. "
            
        if has_news and news_analysis:
            summary += f"Recent news: {news_analysis[0]['headline']}"
            
            if len(news_analysis) > 1:
                summary += f" and {news_analysis[1]['headline']}"
        else:
            summary += "No significant news has been reported recently."
            
        return summary
    
    def _generate_how_has_summary(self, ticker, company_name, timeframe, has_price, price,
                               has_change, change, change_percent, has_news, news_analysis):
        """Generate summary for 'how has' questions."""
        if has_change:
            direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
            summary = f"{company_name} stock has {direction} by {abs(change_percent):.2f}% ({abs(change):.2f} points) {timeframe}. "
            
            if has_news and news_analysis:
                summary += f"Recent headlines include: {news_analysis[0]['headline']}"
        elif has_price:
            summary = f"{company_name} is currently trading at ${price:.2f}, but historical data for {timeframe} is unavailable."
        else:
            summary = f"Unable to determine how {company_name} stock has changed {timeframe} due to insufficient data."
            
        return summary
    
    def _generate_default_summary(self, ticker, company_name, timeframe, has_price, price,
                               has_change, change, change_percent, has_news, news_analysis):
        """Generate a default summary when no specific question type is identified."""
        summary = f"{company_name} ({ticker}) "
        
        if has_price:
            summary += f"is currently trading at ${price:.2f}. "
        else:
            summary += "current price data is unavailable. "
            
        if has_change:
            direction = "up" if change > 0 else "down" if change < 0 else "flat"
            summary += f"The stock is {direction} by {abs(change_percent):.2f}% {timeframe}. "
            
        if has_news and news_analysis:
            summary += f"Recent news: {news_analysis[0]['headline']}"
        
        return summary