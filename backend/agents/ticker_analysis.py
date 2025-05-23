from datetime import datetime
import re
import logging
from utils.llm import generate_analysis_with_llm  # Updated import

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
                "detailed_analysis": "",
                "details": {},
                "success": False
            }
        
        # Get key data points - with fallbacks for missing data
        current_price = price.get("price")
        change = price_change.get("change")
        change_percent = price_change.get("change_percent")
        company_name = price.get("company_name", ticker)
        from_price = price_change.get("from_price")
        to_price = price_change.get("to_price")
        
        # Process news for analysis
        headlines = news.get("headlines", [])
        news_analysis = []
        
        for headline in headlines:
            sentiment = self._analyze_sentiment(headline)
            news_analysis.append({
                "headline": headline,
                "sentiment": sentiment
            })
        
        # Add news_analysis to price object for LLM processing
        enhanced_price = dict(price)
        enhanced_price["news_analysis"] = {
            "headlines": [item["headline"] for item in news_analysis[:10]],
            "sentiments": [item["sentiment"] for item in news_analysis[:10]]
        }
        
        # Try to generate a summary and detailed analysis using the LLM
        llm_result = generate_analysis_with_llm(ticker, query, enhanced_price, news, price_change)
        
        # If LLM analysis is available, use it
        if llm_result and "summary" in llm_result and "detailed_analysis" in llm_result:
            summary = llm_result["summary"]
            detailed_analysis = llm_result["detailed_analysis"]
            llm_used = True
        else:
            # Generate an appropriate summary based on available data
            if "why" in query.lower():
                summary = self._generate_why_summary(ticker, company_name, timeframe, 
                                                  current_price is not None, current_price,
                                                  change is not None, change, change_percent,
                                                  bool(headlines), news_analysis)
            elif "what's happening" in query.lower() or "what is happening" in query.lower():
                summary = self._generate_whats_happening_summary(ticker, company_name, timeframe,
                                                              current_price is not None, current_price,
                                                              change is not None, change, change_percent,
                                                              bool(headlines), news_analysis)
            else:
                summary = self._generate_default_summary(ticker, company_name, timeframe,
                                                      current_price is not None, current_price,
                                                      change is not None, change, change_percent,
                                                      bool(headlines), news_analysis)
            
            # Generate a basic detailed analysis
            detailed_analysis = self._generate_detailed_analysis(ticker, company_name, timeframe,
                                                           current_price, change, change_percent,
                                                           from_price, to_price,
                                                           news_analysis)
            llm_used = False
        
        # Create details with whatever data we have
        details = {
            "llm_enhanced": llm_used,
            "price_analysis": {
                "timeframe": timeframe
            }
        }
        
        # Add price information to details
        if current_price is not None:
            details["price_analysis"]["current_price"] = current_price
        
        if change is not None:
            details["price_analysis"]["change"] = change
            details["price_analysis"]["change_percent"] = change_percent
            details["price_analysis"]["direction"] = "up" if change > 0 else "down" if change < 0 else "flat"
            
        if from_price is not None:
            details["price_analysis"]["from_price"] = from_price
            
        if to_price is not None:
            details["price_analysis"]["to_price"] = to_price
        
        # Add news analysis to details
        if headlines:
            details["news_analysis"] = {
                "headlines": [item["headline"] for item in news_analysis[:5]],
                "sentiments": [item["sentiment"] for item in news_analysis[:5]],
                "news_count": len(headlines)
            }
        
        return {
            "summary": summary,
            "detailed_analysis": detailed_analysis,
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
    
    def _generate_detailed_analysis(self, ticker, company_name, timeframe, 
                                  current_price, change, change_percent, from_price, to_price,
                                  news_analysis):
        """Generate a detailed analysis for the popup view."""
        analysis = f"## {company_name} ({ticker}) - Detailed Analysis\n\n"
        
        # Price Movement Analysis
        analysis += "### Price Movement\n"
        if change is not None and change_percent is not None:
            direction = "increased" if change > 0 else "decreased" if change < 0 else "remained stable"
            analysis += f"{company_name} stock has {direction} by ${abs(change):.2f} (${from_price:.2f} to ${to_price:.2f}), "
            analysis += f"representing a {abs(change_percent):.2f}% change over {timeframe}. "
            
            if change > 0:
                analysis += "This upward movement suggests positive market sentiment toward the company. "
            elif change < 0:
                analysis += "This downward movement indicates market concern about the company's prospects. "
        else:
            analysis += f"Price movement data for {timeframe} is not available. "
        
        # News Impact Analysis
        analysis += "\n\n### News Impact\n"
        if news_analysis:
            # Count positive and negative news
            positive_news = [item for item in news_analysis if item["sentiment"] == "positive"]
            negative_news = [item for item in news_analysis if item["sentiment"] == "negative"]
            neutral_news = [item for item in news_analysis if item["sentiment"] == "neutral"]
            
            analysis += f"Recent news coverage includes {len(positive_news)} positive, {len(negative_news)} negative, "
            analysis += f"and {len(neutral_news)} neutral headlines. "
            
            # Highlight key news based on sentiment
            if change is not None:
                if change > 0 and positive_news:
                    analysis += f"The positive price movement correlates with favorable headlines such as: "
                    analysis += f"\"{positive_news[0]['headline']}\". "
                elif change < 0 and negative_news:
                    analysis += f"The negative price movement aligns with concerning headlines such as: "
                    analysis += f"\"{negative_news[0]['headline']}\". "
            
            # Include a few key headlines
            analysis += "\n\nKey recent headlines:\n"
            for i, item in enumerate(news_analysis[:3]):
                analysis += f"- {item['headline']} (Sentiment: {item['sentiment']})\n"
        else:
            analysis += "No significant news has been reported recently that might explain the price movement."
        
        # Market Context
        analysis += "\n\n### Market Context\n"
        analysis += f"To fully understand {ticker}'s performance, it's important to consider the broader market context. "
        if change is not None:
            if change > 0:
                analysis += f"Investors should evaluate whether this gain is company-specific or part of a sector-wide trend. "
            else:
                analysis += f"Investors should determine if this decline is unique to {ticker} or reflects industry-wide challenges. "
        
        # Outlook
        analysis += "\n\n### Outlook\n"
        analysis += f"Based on the current data, {ticker} "
        if change is not None:
            if change > 1.5:
                analysis += "shows strong momentum that may continue if supported by positive fundamentals and market conditions. "
            elif change > 0:
                analysis += "shows modest positive movement that warrants cautious optimism. "
            elif change > -1.5:
                analysis += "shows minor weakness that may be temporary depending on upcoming news and market trends. "
            else:
                analysis += "faces significant downward pressure that could continue unless fundamental factors improve. "
        else:
            analysis += "requires more data to make a confident assessment of future price movements. "
        
        return analysis