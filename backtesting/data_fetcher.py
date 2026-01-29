"""
Data fetcher for downloading stock market data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class DataFetcher:
    """Fetch historical stock data from Yahoo Finance"""
    
    def __init__(self):
        """Initialize DataFetcher"""
        pass
    
    def fetch_data(self, symbol, start_date, end_date):
        """
        Fetch historical stock data for a given symbol
        
        Args:
            symbol (str): Stock ticker symbol
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: Historical stock data with OHLCV columns
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Rename columns to lowercase for consistency
            data.columns = [col.lower() for col in data.columns]
            
            return data
        
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def get_latest_price(self, symbol):
        """
        Get the latest price for a stock
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            float: Latest closing price
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            return data['close'].iloc[-1]
        
        except Exception as e:
            raise Exception(f"Error fetching latest price for {symbol}: {str(e)}")
    
    def get_available_symbols(self):
        """
        Get a list of popular stock symbols
        
        Returns:
            list: List of popular stock ticker symbols
        """
        return [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META',
            'TSLA', 'NVDA', 'JPM', 'V', 'WMT',
            'DIS', 'NFLX', 'PYPL', 'INTC', 'AMD'
        ]
