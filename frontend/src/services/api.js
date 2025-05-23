/**
 * API service for StockBot
 */

// Base URL for API requests - point to the actual backend server
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

/**
 * Query the StockBot API with a natural language question
 * @param {string} text - The natural language query
 * @returns {Promise<Object>} - The response data
 */
export const queryStockBot = async (text) => {
  try {
    // For development testing without backend, return mock data if needed
    if (process.env.NODE_ENV === 'development' && process.env.REACT_APP_USE_MOCK_DATA === 'true') {
      return getMockResponse(text);
    }
    
    // Make the actual API call to the backend
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API error: ${response.status} - ${errorData.detail || 'Unknown error'}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * Generate mock response data for development
 * @param {string} text - The query text
 * @returns {Object} - Mock response data
 */
const getMockResponse = (text) => {
  // Extract ticker from query if possible
  const tickerMatch = text.match(/\b([A-Z]{1,5})\b/);
  const ticker = tickerMatch ? tickerMatch[1] : getDefaultTicker(text);
  
  // Generate positive or negative change based on query
  const isPositive = !text.toLowerCase().includes('drop') && 
                    !text.toLowerCase().includes('fall') &&
                    !text.toLowerCase().includes('down');
  
  // Get timeframe from query
  const timeframe = text.toLowerCase().includes('week') ? 'week' : 
                    text.toLowerCase().includes('month') ? 'month' : 'today';
  
  // Generate mock data
  const change = isPositive ? 
    (Math.random() * 50 + 5).toFixed(2) : 
    -(Math.random() * 50 + 5).toFixed(2);
  
  const changePercent = isPositive ? 
    (Math.random() * 5 + 0.5).toFixed(1) : 
    -(Math.random() * 5 + 0.5).toFixed(1);
  
  const currentPrice = Math.random() * 500 + 50;
  
  return {
    answer: getAnswerText(ticker, change, changePercent, timeframe, isPositive),
    metadata: {
      ticker: ticker,
      company_name: getCompanyName(ticker),
      current_price: currentPrice,
      price_change: {
        change: parseFloat(change),
        change_percent: parseFloat(changePercent),
        timeframe: timeframe
      },
      news: getNewsItems(ticker, isPositive),
      analysis: {
        summary: getAnalysisSummary(ticker, change, changePercent, timeframe, isPositive),
        details: {}
      }
    }
  };
};

/**
 * Generate a default ticker based on query
 */
const getDefaultTicker = (text) => {
  const lowerText = text.toLowerCase();
  
  if (lowerText.includes('tesla') || lowerText.includes('musk')) return 'TSLA';
  if (lowerText.includes('apple')) return 'AAPL';
  if (lowerText.includes('microsoft')) return 'MSFT';
  if (lowerText.includes('amazon')) return 'AMZN';
  if (lowerText.includes('google')) return 'GOOGL';
  if (lowerText.includes('meta') || lowerText.includes('facebook')) return 'META';
  if (lowerText.includes('nvidia')) return 'NVDA';
  
  // Default to AAPL if no match
  return 'AAPL';
};

/**
 * Get company name from ticker
 */
const getCompanyName = (ticker) => {
  const companies = {
    'TSLA': 'Tesla, Inc.',
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'AMZN': 'Amazon.com, Inc.',
    'GOOGL': 'Alphabet Inc.',
    'META': 'Meta Platforms, Inc.',
    'NVDA': 'NVIDIA Corporation',
    'AMD': 'Advanced Micro Devices, Inc.',
    'INTC': 'Intel Corporation',
    'IBM': 'International Business Machines',
  };
  
  return companies[ticker] || `${ticker} Corporation`;
};

/**
 * Generate mock news items
 */
const getNewsItems = (ticker, isPositive) => {
  const positiveNews = [
    `${ticker} Reports Better-Than-Expected Earnings`,
    `${ticker} Stock Jumps After Analyst Upgrade`,
    `${ticker} Announces New Product Line, Shares Up`,
    `${getCompanyName(ticker)} Expands into New Markets`
  ];
  
  const negativeNews = [
    `${ticker} Stock Falls After Missing Quarterly Expectations`,
    `Analyst Downgrades ${ticker}, Citing Growth Concerns`,
    `${ticker} Faces Regulatory Challenges, Shares Drop`,
    `${getCompanyName(ticker)} Announces Restructuring Plan`
  ];
  
  const neutralNews = [
    `${ticker} Announces New CEO Appointment`,
    `${getCompanyName(ticker)} to Present at Upcoming Investor Conference`,
    `${ticker} Releases Sustainability Report`,
    `What Investors Should Know About ${ticker}'s Strategy`
  ];
  
  // Mix of news with bias toward sentiment
  let news = [];
  
  if (isPositive) {
    news = [...positiveNews.slice(0, 2), neutralNews[0], positiveNews[2]];
  } else {
    news = [...negativeNews.slice(0, 2), neutralNews[1], negativeNews[2]];
  }
  
  // Shuffle array
  return news.sort(() => Math.random() - 0.5).slice(0, 3);
};

/**
 * Generate answer text
 */
const getAnswerText = (ticker, change, changePercent, timeframe, isPositive) => {
  const direction = isPositive ? 'increased' : 'decreased';
  const companyName = getCompanyName(ticker);
  
  let timeframeText = timeframe === 'today' ? 'today' : 
                      timeframe === 'week' ? 'this week' : 'this month';
  
  let reason;
  if (isPositive) {
    reason = "This appears to be related to recent positive earnings reports and analyst upgrades.";
  } else {
    reason = "This appears to be related to recent market volatility and sector-wide pressure.";
  }
  
  return `${companyName} (${ticker}) stock ${direction} by ${Math.abs(changePercent)}% ${timeframeText}. ${reason}`;
};

/**
 * Generate analysis summary
 */
const getAnalysisSummary = (ticker, change, changePercent, timeframe, isPositive) => {
  const direction = isPositive ? 'increased' : 'decreased';
  const timeframeText = timeframe === 'today' ? 'today' : 
                        timeframe === 'week' ? 'this week' : 'this month';
  
  return `${ticker} stock ${direction} by ${Math.abs(changePercent)}% ${timeframeText}.`;
};