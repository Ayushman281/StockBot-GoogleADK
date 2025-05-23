import requests
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Get OpenRouter API key from .env
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_analysis_with_llm(ticker, query, price_info, news_info, price_change_info):
    """
    Generate both a concise summary and detailed analysis using the deepseek-chat model.
    
    Args:
        ticker (str): Stock ticker symbol
        query (str): Original user query
        price_info (dict): Current price information
        news_info (dict): News headlines and information
        price_change_info (dict): Price change data
        
    Returns:
        dict: Generated summary and detailed analysis
    """
    if not OPENROUTER_API_KEY:
        logger.warning("OpenRouter API key not found. Using fallback summary generation.")
        return None
    
    try:
        # Extract price information
        current_price = price_info.get("price")
        company_name = price_info.get("company_name", ticker)
        
        # Extract price change details
        change = price_change_info.get("change")
        change_percent = price_change_info.get("change_percent")
        from_price = price_change_info.get("from_price")
        to_price = price_change_info.get("to_price")
        timeframe = price_change_info.get("timeframe", "today")
        
        # Get news headlines and their sentiments
        headlines = news_info.get("headlines", [])
        
        # Get sentiments if available in the analysis section
        sentiments = []
        if "news_analysis" in price_info and "sentiments" in price_info["news_analysis"]:
            sentiments = price_info["news_analysis"]["sentiments"]
        
        # Prepare news with sentiments for the prompt
        news_items = []
        for i, headline in enumerate(headlines[:10]):  # Limit to top 10 headlines
            sentiment = ""
            if i < len(sentiments):
                sentiment = f" (Sentiment: {sentiments[i]})"
            news_items.append(f"- {headline}{sentiment}")
        
        news_section = "\n".join(news_items) if news_items else "No recent news available."
        
        # Create detailed price information section
        price_section = ""
        if current_price is not None:
            price_section += f"Current Price: ${current_price}\n"
        else:
            price_section += "Current Price: Not available\n"
            
        if to_price is not None:
            price_section += f"Latest Price: ${to_price}\n"
            
        if from_price is not None:
            price_section += f"Previous Price (start of {timeframe}): ${from_price}\n"
            
        if change is not None and change_percent is not None:
            direction = "increased" if change > 0 else "decreased" if change < 0 else "unchanged"
            price_section += f"Price Change: {direction} by ${abs(change):.2f} ({abs(change_percent):.2f}%) over {timeframe}\n"
        
        # Create the prompt with stronger emphasis on addressing the query
        prompt = f"""You are a professional financial analyst. The user has asked: "{query}"

Please analyze {company_name} ({ticker}) stock to directly answer this question based on the following data:

{price_section}
Recent News (with sentiment analysis):
{news_section}

Provide two detailed responses:

1. CONCISE SUMMARY (2-3 sentences): 
   - Directly answer the user's question "{query}"
   - Focus on the most relevant news/data points that explain the situation
   - Be specific about the cause-effect relationship between events and stock movement

2. DETAILED ANALYSIS (4-5 paragraphs):
   - Paragraph 1: Direct answer to "{query}" with supporting evidence from the news
   - Paragraph 2: Deeper analysis of how specific news items relate to the stock movement
   - Paragraph 3: Industry context and comparison with competitors if relevant
   - Paragraph 4: Technical factors affecting the stock price (support/resistance levels, volume, etc.)
   - Paragraph 5: Forward-looking insights and what investors should watch for

Format your response as a JSON object with two keys: "summary" and "detailed_analysis".
"""

        # Make API call to OpenRouter
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8000",  # For testing on localhost
            "X-Title": "StockBot"
        }
        
        data = {
            "model": "deepseek/deepseek-chat:free",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are StockBot, a professional stock analysis assistant that provides both concise summaries and detailed analyses."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        logger.info(f"Requesting LLM analysis for {ticker}")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=30
        )
        
        if response.status_code != 200:
            logger.error(f"Error from OpenRouter API: {response.status_code} - {response.text}")
            return None
            
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated LLM analysis for {ticker} - length: {len(content)} chars")
            
            # Parse the JSON response
            try:
                # Check if the content is formatted as JSON
                if content.startswith("{") and content.endswith("}"):
                    analysis_data = json.loads(content)
                    return analysis_data
                else:
                    # Try to extract JSON from the text
                    import re
                    json_match = re.search(r'(\{[\s\S]*\})', content)
                    if json_match:
                        analysis_data = json.loads(json_match.group(1))
                        return analysis_data
                    else:
                        # Fallback: split into summary and detailed
                        parts = content.split("\n\n", 1)
                        if len(parts) > 1:
                            return {
                                "summary": parts[0].replace("CONCISE SUMMARY:", "").strip(),
                                "detailed_analysis": parts[1].replace("DETAILED ANALYSIS:", "").strip()
                            }
                        else:
                            return {
                                "summary": content[:150] + "...",
                                "detailed_analysis": content
                            }
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
                # Fallback approach if JSON parsing fails
                parts = content.split("\n\n", 1)
                if len(parts) > 1:
                    return {
                        "summary": parts[0].replace("CONCISE SUMMARY:", "").strip(),
                        "detailed_analysis": parts[1].replace("DETAILED ANALYSIS:", "").strip()
                    }
                else:
                    return {
                        "summary": content[:150] + "...",
                        "detailed_analysis": content
                    }
        else:
            logger.error(f"Unexpected response format from OpenRouter: {result}")
            return None
            
    except Exception as e:
        logger.error(f"Error generating analysis with LLM: {str(e)}")
        return None
