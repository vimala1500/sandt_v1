"""
Script to download stock data from yfinance and store in parquet format

This script allows you to:
1. Download historical stock data for one or multiple symbols
2. Store the data in parquet format for efficient storage and fast loading
3. Use cached data for backtesting without requiring internet connectivity

Usage:
    # Download single symbol
    python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31
    
    # Download multiple symbols
    python download_data.py --symbols AAPL MSFT GOOGL --start 2020-01-01 --end 2023-12-31
    
    # Download popular stocks
    python download_data.py --popular --start 2020-01-01 --end 2023-12-31
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from backtesting.data_fetcher import DataFetcher


# Default data directory
DEFAULT_DATA_DIR = 'data'


def create_data_directory(data_dir):
    """
    Create data directory if it doesn't exist
    
    Args:
        data_dir (str): Path to data directory
    """
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    print(f"Data directory: {data_dir}")


def get_parquet_filename(symbol, start_date, end_date, data_dir):
    """
    Generate parquet filename for a symbol and date range
    
    Args:
        symbol (str): Stock ticker symbol
        start_date (str): Start date
        end_date (str): End date
        data_dir (str): Data directory path
        
    Returns:
        str: Path to parquet file
    """
    filename = f"{symbol}_{start_date}_{end_date}.parquet"
    return os.path.join(data_dir, filename)


def download_and_save_data(symbol, start_date, end_date, data_dir, force=False):
    """
    Download stock data and save to parquet file
    
    Args:
        symbol (str): Stock ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        data_dir (str): Directory to save parquet files
        force (bool): If True, re-download even if file exists
        
    Returns:
        bool: True if successful, False otherwise
    """
    parquet_file = get_parquet_filename(symbol, start_date, end_date, data_dir)
    
    # Check if file already exists
    if os.path.exists(parquet_file) and not force:
        print(f"✓ {symbol}: Data already exists at {parquet_file}")
        return True
    
    try:
        print(f"Downloading {symbol} from {start_date} to {end_date}...")
        
        # Fetch data using DataFetcher
        fetcher = DataFetcher()
        data = fetcher.fetch_data(symbol, start_date, end_date)
        
        # Save to parquet
        data.to_parquet(parquet_file, engine='pyarrow', compression='snappy')
        
        print(f"✓ {symbol}: Downloaded {len(data)} rows and saved to {parquet_file}")
        print(f"  Date range: {data.index[0]} to {data.index[-1]}")
        print(f"  File size: {os.path.getsize(parquet_file) / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"✗ {symbol}: Failed to download - {str(e)}")
        return False


def download_multiple_symbols(symbols, start_date, end_date, data_dir, force=False):
    """
    Download data for multiple symbols
    
    Args:
        symbols (list): List of stock ticker symbols
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        data_dir (str): Directory to save parquet files
        force (bool): If True, re-download even if file exists
        
    Returns:
        tuple: (successful_count, failed_count)
    """
    successful = 0
    failed = 0
    
    print(f"\n{'=' * 70}")
    print(f"Downloading data for {len(symbols)} symbols")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'=' * 70}\n")
    
    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] ", end="")
        
        if download_and_save_data(symbol, start_date, end_date, data_dir, force):
            successful += 1
        else:
            failed += 1
        
        print()  # Empty line for readability
    
    return successful, failed


def get_popular_symbols():
    """
    Get list of popular stock symbols
    
    Returns:
        list: List of popular stock ticker symbols
    """
    fetcher = DataFetcher()
    return fetcher.get_available_symbols()


def list_cached_data(data_dir):
    """
    List all cached parquet files in data directory
    
    Args:
        data_dir (str): Data directory path
    """
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' does not exist.")
        return
    
    parquet_files = list(Path(data_dir).glob('*.parquet'))
    
    if not parquet_files:
        print(f"No cached data found in '{data_dir}'.")
        return
    
    print(f"\n{'=' * 70}")
    print(f"Cached data files in '{data_dir}':")
    print(f"{'=' * 70}\n")
    
    total_size = 0
    for parquet_file in sorted(parquet_files):
        file_size = os.path.getsize(parquet_file)
        total_size += file_size
        
        # Try to read basic info
        try:
            df = pd.read_parquet(parquet_file)
            rows = len(df)
            date_range = f"{df.index[0]} to {df.index[-1]}"
        except Exception:
            rows = "?"
            date_range = "?"
        
        print(f"  {parquet_file.name}")
        print(f"    Rows: {rows}, Size: {file_size / 1024:.2f} KB")
        print(f"    Date range: {date_range}\n")
    
    print(f"Total: {len(parquet_files)} files, {total_size / 1024:.2f} KB")


def validate_date(date_string):
    """
    Validate date string format
    
    Args:
        date_string (str): Date in 'YYYY-MM-DD' format
        
    Returns:
        str: Validated date string
        
    Raises:
        argparse.ArgumentTypeError: If date format is invalid
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Download stock data from yfinance and store in parquet format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download single symbol
  python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31
  
  # Download multiple symbols
  python download_data.py --symbols AAPL MSFT GOOGL --start 2020-01-01 --end 2023-12-31
  
  # Download popular stocks for last 2 years
  python download_data.py --popular --start 2022-01-01 --end 2023-12-31
  
  # Force re-download existing data
  python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31 --force
  
  # List cached data
  python download_data.py --list
        """
    )
    
    # Symbol selection (mutually exclusive)
    symbol_group = parser.add_mutually_exclusive_group()
    symbol_group.add_argument('--symbol', type=str, help='Single stock symbol to download')
    symbol_group.add_argument('--symbols', nargs='+', help='Multiple stock symbols to download')
    symbol_group.add_argument('--popular', action='store_true', help='Download popular stocks')
    
    # Date range
    parser.add_argument('--start', type=validate_date, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=validate_date, help='End date (YYYY-MM-DD)')
    
    # Options
    parser.add_argument('--data-dir', type=str, default=DEFAULT_DATA_DIR, 
                       help=f'Directory to store data files (default: {DEFAULT_DATA_DIR})')
    parser.add_argument('--force', action='store_true', 
                       help='Force re-download even if data exists')
    parser.add_argument('--list', action='store_true', 
                       help='List all cached data files')
    
    args = parser.parse_args()
    
    # Create data directory
    create_data_directory(args.data_dir)
    
    # List cached data
    if args.list:
        list_cached_data(args.data_dir)
        return 0
    
    # Determine symbols to download
    if args.symbol:
        symbols = [args.symbol]
    elif args.symbols:
        symbols = args.symbols
    elif args.popular:
        symbols = get_popular_symbols()
        print(f"Popular symbols: {', '.join(symbols)}")
    else:
        parser.error('Must specify --symbol, --symbols, --popular, or --list')
    
    # Validate date range is provided
    if not args.start or not args.end:
        parser.error('Must specify both --start and --end dates')
    
    # Download data
    successful, failed = download_multiple_symbols(
        symbols, args.start, args.end, args.data_dir, args.force
    )
    
    # Print summary
    print(f"{'=' * 70}")
    print(f"Download Summary:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {successful + failed}")
    print(f"{'=' * 70}")
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
