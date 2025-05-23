# StockBot - Multi-Agent Stock Analysis System

A multi-agent system built with Google ADK for answering stock-related questions using real-time data and news.

## Project Overview

This system uses a modular multi-agent architecture to process natural language queries about stocks. It fetches real-time stock data and news to provide insightful answers about stock performance and market trends.

## Features

- Stock ticker identification from natural language
- Real-time stock price information
- Recent news retrieval for stocks
- Price change analysis over different timeframes
- Comprehensive stock analysis with news correlation

## Project Structure

The project is organized as follows:

- `src/`: Contains the source code for the multi-agent system.
- `data/`: Stores sample data and configurations.
- `docs/`: Includes documentation and resources.
- `tests/`: Contains unit tests for the system.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/username/StockBot.git
   ```
2. Navigate to the project directory:
   ```
   cd StockBot
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage

To use StockBot, simply run the application and input your stock-related queries. The system will process your query and provide real-time data and insights.

Example:
```
What is the current price of AAPL stock?
```

## Example Queries and Responses

StockBot can handle a variety of natural language questions. Here are some examples:

### Price Movement Queries

**Query:** "Why did Tesla stock drop today?"  
**Response:** "Tesla, Inc. (TSLA) stock decreased by 3.2% today. This appears to be related to recent supply chain disruptions and increased competition in the EV market, as reported in recent news about production delays at the Shanghai factory."

**Query:** "How has Apple performed this week?"  
**Response:** "Apple Inc. (AAPL) stock has increased by 2.4% this week. The positive performance coincides with the announcement of new product releases and better-than-expected quarterly earnings results."

### Market Analysis Queries

**Query:** "What's happening with Microsoft stock recently?"  
**Response:** "Microsoft Corporation (MSFT) is currently trading at $337.50, up 1.8% this month. Recent news highlights strong cloud service growth and strategic AI partnerships that have positively influenced investor sentiment."

**Query:** "Compare NVIDIA and AMD performance"  
**Response:** "NVIDIA (NVDA) has outperformed AMD with a 5.3% increase this week compared to AMD's 1.2% gain. NVIDIA's strong performance is attributed to growing demand for its AI chips, while AMD continues to face more competitive pressure in the consumer GPU market."

### Timeframe-Specific Queries

**Query:** "What happened to Amazon stock in the last 30 days?"  
**Response:** "Amazon.com, Inc. (AMZN) stock has decreased by 4.1% over the last month. This decline coincides with concerns about consumer spending slowdown and recent announcements about increasing competition in the cloud services sector."

**Query:** "Is Walmart stock up year-to-date?"  
**Response:** "Yes, Walmart Inc. (WMT) stock is up 12.4% year-to-date. The company has benefited from strong retail performance and successful expansion of its e-commerce capabilities during inflationary market conditions."

## API Endpoints

StockBot provides the following API endpoints:

- `GET /api/stock/{ticker}`: Fetches real-time stock data for the given ticker.
- `GET /api/news/{ticker}`: Retrieves recent news articles related to the given ticker.
- `GET /api/analysis/{ticker}`: Provides a comprehensive analysis of the stock, including price trends and news correlation.

