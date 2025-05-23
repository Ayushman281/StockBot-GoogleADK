import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_moving_average(data, window):
    """
    Calculate moving average for stock price data.
    
    Args:
        data (dict): Time series data from Alpha Vantage API
        window (int): Window size for moving average
        
    Returns:
        pd.DataFrame: DataFrame with moving average data
    """
    # Convert data to DataFrame
    df = pd.DataFrame(data).T
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    
    # Convert values to float
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    
    # Sort by date
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    # Calculate moving average
    df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
    
    return df

def calculate_volatility(data, window=30):
    """
    Calculate rolling volatility for stock price data.
    
    Args:
        data (dict): Time series data from Alpha Vantage API
        window (int): Window size for volatility calculation
        
    Returns:
        pd.DataFrame: DataFrame with volatility data
    """
    # Convert data to DataFrame
    df = pd.DataFrame(data).T
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    
    # Convert values to float
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)
    
    # Sort by date
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change()
    
    # Calculate rolling volatility (standard deviation of returns)
    df['volatility'] = df['daily_return'].rolling(window=window).std() * np.sqrt(window)
    
    return df

def find_price_correlation(price_data, news_dates):
    """
    Find correlation between price movements and news dates.
    
    Args:
        price_data (pd.DataFrame): DataFrame with price data
        news_dates (list): List of dates with significant news
        
    Returns:
        dict: Analysis of price movements around news dates
    """
    results = []
    
    for date_str in news_dates:
        try:
            # Convert string to datetime
            news_date = pd.to_datetime(date_str)
            
            # Find the nearest trading day (might not be exact if news came on weekend)
            if news_date in price_data.index:
                trading_day = news_date
            else:
                # Find closest date
                trading_day = price_data.index[price_data.index.get_indexer([news_date], method='nearest')[0]]
            
            # Get day before and after
            day_before_idx = price_data.index.get_loc(trading_day) - 1
            day_after_idx = price_data.index.get_loc(trading_day) + 1
            
            # Make sure indices are valid
            if day_before_idx >= 0 and day_after_idx < len(price_data):
                day_before = price_data.index[day_before_idx]
                day_after = price_data.index[day_after_idx]
                
                # Calculate price changes
                change_on_day = (price_data.loc[trading_day, 'close'] - price_data.loc[trading_day, 'open']) / price_data.loc[trading_day, 'open']
                change_next_day = (price_data.loc[day_after, 'close'] - price_data.loc[trading_day, 'close']) / price_data.loc[trading_day, 'close']
                
                results.append({
                    'news_date': news_date,
                    'trading_day': trading_day,
                    'change_on_day': change_on_day,
                    'change_next_day': change_next_day,
                    'closing_price': price_data.loc[trading_day, 'close'],
                    'volume': price_data.loc[trading_day, 'volume']
                })
        except Exception as e:
            # Skip dates that can't be processed
            continue
    
    return results
