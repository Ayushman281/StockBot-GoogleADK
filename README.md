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

## API Endpoints

StockBot provides the following API endpoints:

- `GET /api/stock/{ticker}`: Fetches real-time stock data for the given ticker.
- `GET /api/news/{ticker}`: Retrieves recent news articles related to the given ticker.
- `GET /api/analysis/{ticker}`: Provides a comprehensive analysis of the stock, including price trends and news correlation.

