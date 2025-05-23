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
            analysis += f"{company_name} stock has {direction} by ${abs(change):.2f} "
            if from_price and to_price:
                analysis += f"(from ${from_price:.2f} to ${to_price:.2f}), "
            analysis += f"representing a {abs(change_percent):.2f}% change over {timeframe}.\n\n"
            
            if change > 0:
                analysis += "This upward movement suggests positive market sentiment toward the company. "
                analysis += "The price action shows momentum that could continue if supported by fundamental factors."
            elif change < 0:
                analysis += "This downward movement indicates market concern about the company's prospects. "
                analysis += "The selling pressure could continue unless positive catalysts emerge."
        else:
            analysis += f"Price movement data for {timeframe} is not available.\n\n"
        
        # Technical Analysis
        analysis += "\n### Technical Analysis\n"
        analysis += f"Based on recent price action, {ticker} "
        if change is not None:
            if change > 0:
                analysis += f"is showing bullish momentum with potential resistance at ${(to_price * 1.05):.2f}. "
                analysis += f"Support levels appear to be forming near ${(to_price * 0.95):.2f}. "
                analysis += "The trading volume has been above average, indicating strong buyer interest."
            else:
                analysis += f"is displaying bearish momentum with support around ${(to_price * 0.95):.2f}. "
                analysis += f"The stock may face resistance at ${(to_price * 1.05):.2f} on any recovery attempts. "
                analysis += "Trading volume trends suggest continued selling pressure in the near term."
        
        # News Impact Analysis
        analysis += "\n\n### News Impact\n"
        if news_analysis:
            # Count positive and negative news
            positive_news = [item for item in news_analysis if item["sentiment"] == "positive"]
            negative_news = [item for item in news_analysis if item["sentiment"] == "negative"]
            neutral_news = [item for item in news_analysis if item["sentiment"] == "neutral"]
            
            analysis += f"Recent news coverage includes {len(positive_news)} positive, {len(negative_news)} negative, "
            analysis += f"and {len(neutral_news)} neutral headlines. "
            
            # Sentiment analysis
            if len(positive_news) > len(negative_news):
                analysis += f"The positive news cycle suggests a potential improvement in {ticker}'s market perception. "
                if positive_news:
                    analysis += f"Key positive headline: \"{positive_news[0]['headline']}\" "
            elif len(negative_news) > len(positive_news):
                analysis += f"The negative news cycle may continue to pressure {ticker}'s valuation. "
                if negative_news:
                    analysis += f"Key negative headline: \"{negative_news[0]['headline']}\" "
            else:
                analysis += f"The balanced news sentiment indicates market indecision about {ticker}'s direction. "
            
            # Include key headlines
            analysis += "\n\nSignificant news headlines:\n"
            for i, item in enumerate(news_analysis[:4]):
                analysis += f"- {item['headline']} (Sentiment: {item['sentiment'].title()})\n"
        else:
            analysis += "No significant news has been reported recently that might explain the price movement."
        
        # Market Context
        analysis += "\n\n### Market Context\n"
        analysis += f"{ticker} operates in a rapidly evolving industry environment. "
        if change is not None:
            if change > 0:
                analysis += f"The stock's recent outperformance suggests company-specific strengths that differentiate it from peers. "
                analysis += f"Investors should evaluate whether this momentum is sustainable based on upcoming catalysts and broader sector trends. "
            else:
                analysis += f"The recent underperformance may reflect either company-specific challenges or sector-wide pressures. "
                analysis += f"A comparative analysis with peers would help determine if this is an industry-wide trend or unique to {ticker}. "
        
        analysis += f"\nKey factors to monitor include:\n"
        analysis += f"- Changes in consumer/business spending patterns\n"
        analysis += f"- Competitive landscape developments\n"
        analysis += f"- Regulatory environment shifts\n"
        analysis += f"- Macroeconomic indicators affecting the sector\n"
        
        # Outlook
        analysis += "\n\n### Investment Outlook\n"
        analysis += f"Based on the current data, {ticker} "
        if change is not None:
            if change > 2:
                analysis += "shows strong positive momentum that may indicate a longer-term bullish trend. "
                analysis += "Investors might consider this an opportunity, with appropriate position sizing and risk management. "
            elif change > 0:
                analysis += "shows modest positive movement that warrants cautious optimism. "
                analysis += "Risk-averse investors should wait for confirmation of the trend before increasing exposure. "
            elif change > -2:
                analysis += "shows minor weakness that may represent a short-term pullback rather than a reversal. "
                analysis += "This could present a buying opportunity if fundamentals remain strong. "
            else:
                analysis += "faces significant downward pressure that suggests caution. "
                analysis += "Investors should carefully evaluate whether this represents a temporary setback or a fundamental shift in prospects. "
        
        analysis += f"\n\nInvestors should monitor upcoming earnings reports, product announcements, and industry developments before making decisions about {ticker}."
        
        return analysis