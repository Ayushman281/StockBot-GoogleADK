from api.news_api import NewsAPI

class TickerNewsAgent:
    """
    Agent responsible for retrieving news about a stock ticker.
    """
    
    def __init__(self):
        self.news_api = NewsAPI()
    
    def get_news(self, ticker, days=7):
        """
        Get recent news articles about the given ticker.
        
        Args:
            ticker (str): The stock ticker symbol
            days (int): Number of days to look back for news
            
        Returns:
            dict: News data including headlines, sources, and summaries
        """
        if not ticker:
            return {
                "headlines": [],
                "sources": [],
                "summaries": [],
                "success": False,
                "error": "No ticker provided"
            }
        
        try:
            # Get news articles from the API
            articles = self.news_api.get_company_news(ticker, days)
            
            # Extract relevant information from articles
            headlines = [article.get("title", "") for article in articles]
            sources = [article.get("source", {}).get("name", "") for article in articles]
            summaries = [article.get("description", "") for article in articles]
            
            return {
                "headlines": headlines,
                "sources": sources,
                "summaries": summaries,
                "full_articles": articles,
                "success": True
            }
        except Exception as e:
            return {
                "headlines": [],
                "sources": [],
                "summaries": [],
                "success": False,
                "error": str(e)
            }
