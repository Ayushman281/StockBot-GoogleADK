# StockBot - Multi-Agent Stock Analysis System

A multi-agent system built with Google ADK for answering stock-related questions using real-time data and news.

# Live Demo

The application is deployed and accessible at: https://stock-bot-google-adk.vercel.app/

## Project Overview

This system uses a modular multi-agent architecture to process natural language queries about stocks. It fetches real-time stock data and news to provide insightful answers about stock performance and market trends.

## Tech Stack

### Frontend
- **React**: JavaScript library for building the user interface
- **Vite**: Build tool and development server providing fast HMR
- **Tailwind CSS**: Utility-first CSS framework for styling components
- **Lucide React**: Lightweight icon library for UI elements

### Backend
- **FastAPI**: High-performance Python web framework for building APIs
- **Python 3.10+**: Core programming language for backend logic
- **OpenRouter AI**: API gateway providing access to the deepseek/deepseek-chat:free LLM
- **Financial Data APIs**:
  - Financial Modeling Prep API: Real-time stock data and fundamentals 
  - Yahoo Finance (fallback): Alternative source for price data

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical operations for financial calculations

### Architecture
- **Multi-Agent System**: Specialized agents handling different aspects of stock analysis
- **RESTful API**: Communication protocol between frontend and backend

## System Architecture

StockBot employs a multi-agent architecture where specialized agents collaborate to process user queries:

1. **Identify Ticker Agent**: Extracts stock ticker symbols from natural language queries
2. **Ticker News Agent**: Fetches relevant news articles for the identified stock
3. **Ticker Price Agent**: Retrieves current and historical price data 
4. **Ticker Price Change Agent**: Calculates price changes over different timeframes
5. **Ticker Analysis Agent**: Analyzes data and generates insights
6. **Orchestrator Agent**: Coordinates all agents and assembles the final response

The LLM integration provides AI-enhanced analysis summaries and detailed reports based on the collected data.

## Features

- Stock ticker identification from natural language
- Real-time stock price information
- Recent news retrieval for stocks
- Price change analysis over different timeframes
- Comprehensive stock analysis with news correlation
- AI-enhanced analysis using deepseek/deepseek-chat LLM

## Project Structure

The project is organized as follows:

- `frontend/`: React-based frontend application
- `backend/`: FastAPI server and multi-agent system
  - `agents/`: Individual specialist agents
  - `api/`: API clients for financial data sources
  - `utils/`: Helper functions and utilities
- `data/`: Stores sample data and configurations
- `docs/`: Includes documentation and resources
- `tests/`: Contains unit tests for the system

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/username/StockBot.git
   ```
2. Navigate to the project directory:
   ```
   cd StockBot
   ```

3. Setup the backend:
   ```
   cd backend
   pip install -r requirements.txt
   # Create .env file with your API keys
   # OPENROUTER_API_KEY=your_key_here
   # FMP_API_KEY=your_key_here
   # NEWS_API_KEY=your_key_here
   python main.py
   ```

4. Setup the frontend:
   ```
   cd frontend
   npm install
   npm run dev
   ```

## Usage

To use StockBot:

1. Start the backend FastAPI server (`python main.py`)
2. Launch the frontend development server (`npm run dev`)
3. Open your browser to `http://localhost:5173`
4. Enter your stock-related query in the search bar
5. View the analysis results, news, and price information

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

## API Documentation

### Backend FastAPI Endpoints

- **POST** `/query`: Main endpoint for stock queries
  - Request Body: `{ "text": "your natural language query" }`
  - Response: JSON with analysis and stock data
  ```json
  {
    "answer": "Summary analysis of the query",
    "metadata": {
      "ticker": "AAPL",
      "company_name": "Apple Inc.",
      "current_price": 175.32,
      "price_change": {
        "change": 2.45,
        "change_percent": 1.38,
        "timeframe": "today"
      },
      "news": ["Headline 1", "Headline 2"],
      "analysis": {
        "summary": "Brief analysis",
        "detailed_analysis": "In-depth analysis with multiple paragraphs"
      }
    }
  }
  ```

- **GET** `/health`: Health check endpoint
  - Response: `{ "status": "healthy" }`

### Integration with External APIs

- **Financial Modeling Prep API**: Used for real-time stock quotes and historical data
- **Yahoo Finance API**: Fallback source for stock price information
- **OpenRouter AI API**: Powers the AI-enhanced analysis using deepseek/deepseek-chat model

## Environment Variables

The following environment variables should be configured in your `.env` file:

```
NEWS_API_KEY=your_key_here
FMP_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

## Contributing

Contributions to StockBot are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Financial data provided by Financial Modeling Prep and NewsAPI
- NLP powered by OpenRouter AI's deepseek/deepseek-chat model

