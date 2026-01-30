"""
Data fetcher for downloading stock market data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
import os

# Get or create logger for this module
logger = logging.getLogger(__name__)
# Only set level if not already configured
if not logger.handlers:
    logger.setLevel(logging.INFO)


class DataFetcher:
    """Fetch historical stock data from Yahoo Finance"""
    
    def __init__(self, timeout=30, max_retries=3):
        """
        Initialize DataFetcher
        
        Args:
            timeout (int): Request timeout in seconds (default: 30)
            max_retries (int): Maximum number of retry attempts (default: 3)
        """
        # Parse environment variables with fallback to defaults
        try:
            self.timeout = int(os.environ.get('YFINANCE_TIMEOUT', timeout))
        except (ValueError, TypeError):
            logger.warning(f"Invalid YFINANCE_TIMEOUT value, using default: {timeout}")
            self.timeout = timeout
        
        try:
            self.max_retries = int(os.environ.get('YFINANCE_MAX_RETRIES', max_retries))
        except (ValueError, TypeError):
            logger.warning(f"Invalid YFINANCE_MAX_RETRIES value, using default: {max_retries}")
            self.max_retries = max_retries
        
        logger.info(f"DataFetcher initialized with timeout={self.timeout}s, max_retries={self.max_retries}")
    
    def _fetch_with_retry(self, fetch_func, symbol, operation_name):
        """
        Execute a fetch operation with retry logic for network errors
        
        Args:
            fetch_func: Function to execute that returns data
            symbol (str): Stock ticker symbol
            operation_name (str): Description of operation for logging
            
        Returns:
            Result from fetch_func
            
        Raises:
            ValueError: For invalid symbols or missing data
            Exception: For other errors after retries exhausted
        """
        last_error = None
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries} for {symbol} {operation_name}")
                return fetch_func()
            
            except ValueError as ve:
                # Don't retry for invalid symbols or missing data
                logger.error(f"ValueError for {symbol}: {str(ve)}")
                raise
            
            except Exception as e:
                last_error = e
                error_type = type(e).__name__
                
                # Check if it's a network-related error
                is_network_error = any(keyword in str(e).lower() for keyword in [
                    'connection', 'timeout', 'network', 'resolve', 'unreachable', 'dns'
                ])
                
                if is_network_error:
                    logger.warning(
                        f"Network error on attempt {attempt + 1}/{self.max_retries} "
                        f"for {symbol}: {error_type} - {str(e)}"
                    )
                    
                    if attempt < self.max_retries - 1:
                        # Exponential backoff: 2s, 4s, 8s
                        wait_time = 2 ** (attempt + 1)
                        logger.info(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                else:
                    logger.error(f"Non-network error for {symbol}: {error_type} - {str(e)}")
                    raise Exception(f"Error during {operation_name} for {symbol}: {str(e)}")
        
        # All retries exhausted
        error_msg = (
            f"Failed {operation_name} for {symbol} after {self.max_retries} attempts. "
            f"Last error: {type(last_error).__name__} - {str(last_error)}. "
            f"Please check internet connectivity and ensure Yahoo Finance is accessible."
        )
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def fetch_data(self, symbol, start_date, end_date):
        """
        Fetch historical stock data for a given symbol with retry logic
        
        Args:
            symbol (str): Stock ticker symbol
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            
        Returns:
            pd.DataFrame: Historical stock data with OHLCV columns
        """
        logger.info(f"Fetching data for {symbol} from {start_date} to {end_date}")
        
        def _fetch():
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, timeout=self.timeout)
            
            if data.empty:
                error_msg = (
                    f"No data found for symbol {symbol}. "
                    f"Possible reasons: invalid symbol, delisted stock, "
                    f"or no trading data in specified date range ({start_date} to {end_date})."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Rename columns to lowercase for consistency
            data.columns = [col.lower() for col in data.columns]
            
            logger.info(f"Successfully fetched {len(data)} rows for {symbol}")
            return data
        
        return self._fetch_with_retry(_fetch, symbol, "data fetch")
    
    def get_latest_price(self, symbol):
        """
        Get the latest price for a stock with retry logic
        
        Args:
            symbol (str): Stock ticker symbol
            
        Returns:
            float: Latest closing price
        """
        logger.info(f"Fetching latest price for {symbol}")
        
        def _fetch():
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", timeout=self.timeout)
            
            if data.empty:
                error_msg = f"No data found for symbol {symbol}. Symbol may be invalid or delisted."
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            # Use uppercase 'Close' because history() returns uppercase column names
            latest_price = data['Close'].iloc[-1]
            logger.info(f"Successfully fetched latest price for {symbol}: ${latest_price:.2f}")
            return latest_price
        
        return self._fetch_with_retry(_fetch, symbol, "latest price fetch")
    
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
