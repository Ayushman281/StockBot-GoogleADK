import re
import nltk
import requests
import logging
from nltk.tokenize import word_tokenize
from utils.nlp import extract_timeframe
from dotenv import load_dotenv
import os

# Load API keys from .env
load_dotenv()
API_KEY = os.getenv("FMP_API_KEY")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nltk.download('punkt', quiet=True)

class IdentifyTickerAgent:
    """
    Agent responsible for identifying stock ticker symbols from natural language queries.
    """
    
    def __init__(self):
        self.api_key = API_KEY
        self.ticker_pattern = re.compile(r'[$]?([A-Z]{1,5})\b')
        self.skip_words = {"why", "how", "what", "when", "the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for", "with", "by", "about", "of"}
        self.stock_keywords = {"stock", "shares", "share", "price"}
        self.common_companies = {
            'apple': 'AAPL',
            'tesla': 'TSLA',
            'microsoft': 'MSFT',
            'amazon': 'AMZN',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'nvidia': 'NVDA',
            'amd': 'AMD',
            'intel': 'INTC',
            'ibm': 'IBM',
            'oracle': 'ORCL',
            'cisco': 'CSCO',
            'walmart': 'WMT',
            'disney': 'DIS',
            'coca-cola': 'KO',
            'coke': 'KO',
            'pepsi': 'PEP',
            'nike': 'NKE',
            'mcdonalds': 'MCD',
            'starbucks': 'SBUX',
            'boeing': 'BA'
        }
        self.company_names = {
            'AAPL': 'Apple Inc.',
            'TSLA': 'Tesla, Inc.',
            'MSFT': 'Microsoft Corporation',
            'AMZN': 'Amazon.com, Inc.',
            'GOOGL': 'Alphabet Inc.',
            'META': 'Meta Platforms, Inc.',
            'NFLX': 'Netflix, Inc.',
            'NVDA': 'NVIDIA Corporation',
            'AMD': 'Advanced Micro Devices, Inc.',
            'INTC': 'Intel Corporation',
            'IBM': 'International Business Machines',
            'ORCL': 'Oracle Corporation',
            'CSCO': 'Cisco Systems, Inc.',
            'WMT': 'Walmart Inc.',
            'DIS': 'The Walt Disney Company',
            'KO': 'The Coca-Cola Company',
            'PEP': 'PepsiCo, Inc.',
            'NKE': 'Nike, Inc.',
            'MCD': "McDonald's Corporation",
            'SBUX': 'Starbucks Corporation',
            'BA': 'The Boeing Company'
        }
        
    def get_ticker_from_api(self, company_name):
        """Fetch ticker using the Financial Modeling Prep search endpoint."""
        try:
            # Check if it's in our common companies first
            if company_name.lower() in self.common_companies:
                ticker = self.common_companies[company_name.lower()]
                return ticker, f"{company_name.title()}, Inc."
                
            # Search across multiple exchanges, not just NASDAQ
            url = f"https://financialmodelingprep.com/api/v3/search?query={company_name}&limit=5&apikey={self.api_key}"
            logger.info(f"Querying API for: {company_name}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    logger.info(f"API returned data for {company_name}: {data[0]['symbol']}")
                    return data[0]["symbol"], data[0]["name"]
                else:
                    logger.warning(f"API returned empty data for {company_name}")
            else:
                logger.error(f"API error {response.status_code} for {company_name}")
                
        except Exception as e:
            logger.error(f"Exception in API call: {str(e)}")
            
        return None, None

    def _extract_timeframe(self, query_text):
        """
        Extract timeframe from query text.
        
        Args:
            query_text (str): The user's query text
            
        Returns:
            str: The identified timeframe ('today', 'week', 'month', etc.)
        """
        query_lower = query_text.lower()
        
        # Check for explicit timeframe mentions
        if 'today' in query_lower:
            return 'today'
        elif 'yesterday' in query_lower:
            return 'yesterday'
        elif any(term in query_lower for term in ['this week', 'current week']):
            return 'week'
        elif any(term in query_lower for term in ['this month', 'current month']):
            return 'month'
        elif any(term in query_lower for term in ['this year', 'current year']):
            return 'year'
        elif 'quarter' in query_lower:
            return 'quarter'
        
        # Check for "last X days/weeks/months" patterns
        day_pattern = re.search(r'last\s+(\d+)\s+day', query_lower)
        if day_pattern:
            days = int(day_pattern.group(1))
            if days <= 1:
                return 'today'
            elif days <= 7:
                return 'week'
            elif days <= 30:
                return 'month'
            elif days <= 90:
                return 'quarter'
            else:
                return 'year'
        
        # Check for specific number of days/weeks/months
        if re.search(r'(\d+)\s+day', query_lower):
            days_match = re.search(r'(\d+)\s+day', query_lower)
            days = int(days_match.group(1))
            if days <= 1:
                return 'today'
            elif days <= 7:
                return 'week'
            elif days <= 30:
                return 'month'
            else:
                return 'quarter'
        
        if 'week' in query_lower:
            weeks_match = re.search(r'(\d+)\s+week', query_lower)
            if weeks_match:
                weeks = int(weeks_match.group(1))
                if weeks <= 1:
                    return 'week'
                elif weeks <= 4:
                    return 'month'
                else:
                    return 'quarter'
            return 'week' 
        
        if 'month' in query_lower:
            months_match = re.search(r'(\d+)\s+month', query_lower)
            if months_match:
                months = int(months_match.group(1))
                if months <= 1:
                    return 'month'
                elif months <= 3:
                    return 'quarter'
                else:
                    return 'year'
            return 'month' 
        
        if 'year' in query_lower:
            return 'year'
    
        return 'today'

    def identify(self, query):
        """
        Identify ticker symbol from the query.
        
        Args:
            query (str): The natural language query
            
        Returns:
            dict: Information about the identified ticker
        """
        if not query:
            logger.warning("Empty query received")
            return {
                "ticker": None,
                "company_name": None,
                "timeframe": "today",
                "confidence": 0.0
            }
            
        logger.info(f"Processing query: '{query}'")
        original_query = query
        query_lower = query.lower()
        
        # First try direct ticker mentions
        ticker_matches = self.ticker_pattern.findall(original_query)
        if ticker_matches:
            ticker = ticker_matches[0]
            if ticker.lower() not in self.skip_words:
                # Validate the ticker using the API
                try:
                    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={self.api_key}"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200 and response.json():
                        company_data = response.json()[0]
                        timeframe = self._extract_timeframe(query_lower)
                        logger.info(f"Found ticker via direct mention: {ticker}")
                        return {
                            "ticker": ticker,
                            "company_name": company_data.get("companyName", f"{ticker} Inc."),
                            "timeframe": timeframe,
                            "confidence": 0.9
                        }
                except Exception as e:
                    logger.error(f"Error validating ticker {ticker}: {str(e)}")
        
        # Extract potential company names
        tokens = word_tokenize(query_lower)
        
        # Remove stock keywords to help isolate company name
        cleaned_tokens = [t for t in tokens if t not in self.stock_keywords]
        
        # Check for common company names directly in the query
        for company, ticker in self.common_companies.items():
            if company in query_lower:
                timeframe = self._extract_timeframe(query_lower)
                logger.info(f"Found ticker via common company match: {ticker}")
                return {
                    "ticker": ticker, 
                    "company_name": f"{company.title()}, Inc.",
                    "timeframe": timeframe,
                    "confidence": 0.9
                }
        
        # Try multi-word company names 
        n = len(cleaned_tokens)
        max_phrase_length = min(5, n) 
        
        for phrase_length in range(max_phrase_length, 0, -1):
            for i in range(n - phrase_length + 1):
                phrase_tokens = cleaned_tokens[i:i+phrase_length]
                
                # Skip if phrase consists mainly of skip words
                if sum(1 for t in phrase_tokens if t not in self.skip_words) <= 1:
                    continue
                    
                phrase = " ".join(phrase_tokens)
                ticker, full_name = self.get_ticker_from_api(phrase)
                
                if ticker:
                    timeframe = self._extract_timeframe(query_lower)
                    logger.info(f"Found ticker via API phrase search: {ticker}")
                    return {
                        "ticker": ticker,
                        "company_name": full_name,
                        "timeframe": timeframe,
                        "confidence": 0.95
                    }

        # Fallback - try the whole query without stock keywords
        clean_query = ' '.join([t for t in tokens if t not in self.stock_keywords])
        ticker, full_name = self.get_ticker_from_api(clean_query)
        if ticker:
            timeframe = self._extract_timeframe(query_lower)
            logger.info(f"Found ticker via whole query fallback: {ticker}")
            return {
                "ticker": ticker,
                "company_name": full_name,
                "timeframe": timeframe,
                "confidence": 0.8
            }

        # Default fallback
        logger.warning("No ticker identified for query")
        return {
            "ticker": None,
            "company_name": None,
            "timeframe": "today",
            "confidence": 0.0
        }
