# StockBot - Multi-Agent Stock Analysis System

A multi-agent system built with Google ADK for answering stock-related questions using real-time data and news.

## Features

- Stock ticker identification from natural language
- Real-time stock price information
- Recent news retrieval for stocks
- Price change analysis over different timeframes
- Comprehensive stock analysis with news correlation

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file:
   - `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key
   - `NEWS_API_KEY`: Your News API key

3. Run the application:
   ```
   python main.py
   ```

## Usage

Example queries:
- "Why did Tesla stock drop today?"
- "What's happening with Palantir stock recently?"
- "How has Nvidia stock changed in the last 7 days?"

## API Endpoints

- `/query` - POST: Send natural language queries about stocks
