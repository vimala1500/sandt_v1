"""
Test script for data caching functionality (uses sample data, no internet required)
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_sample_data(symbol, start_date, end_date):
    """
    Generate sample stock data for testing
    
    Args:
        symbol (str): Stock ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        
    Returns:
        pd.DataFrame: Sample stock data
    """
    # Create date range
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    dates = pd.date_range(start=start, end=end, freq='D')
    
    # Generate random price data with trend
    np.random.seed(hash(symbol) % 2**32)  # Different seed for each symbol
    base_price = 100 + (hash(symbol) % 200)  # Different base prices
    trend = np.linspace(0, 50, len(dates))
    noise = np.random.randn(len(dates)) * 5
    close_prices = base_price + trend + noise
    
    # Ensure prices are positive
    close_prices = np.maximum(close_prices, 50)
    
    # Create OHLCV data
    data = pd.DataFrame({
        'open': close_prices * (1 + np.random.randn(len(dates)) * 0.01),
        'high': close_prices * (1 + abs(np.random.randn(len(dates))) * 0.02),
        'low': close_prices * (1 - abs(np.random.randn(len(dates))) * 0.02),
        'close': close_prices,
        'volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    return data


def create_sample_cache(symbols, start_date, end_date, data_dir='data'):
    """
    Create sample cached parquet files for testing
    
    Args:
        symbols (list): List of stock symbols
        start_date (str): Start date
        end_date (str): End date
        data_dir (str): Directory to store parquet files
    """
    # Create data directory
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("Creating Sample Cached Data for Testing")
    print("=" * 70)
    print(f"\nData directory: {data_dir}")
    print(f"Symbols: {', '.join(symbols)}")
    print(f"Date range: {start_date} to {end_date}\n")
    
    for symbol in symbols:
        print(f"Generating sample data for {symbol}...")
        
        # Generate sample data
        data = generate_sample_data(symbol, start_date, end_date)
        
        # Save to parquet
        filename = f"{symbol}_{start_date}_{end_date}.parquet"
        filepath = os.path.join(data_dir, filename)
        data.to_parquet(filepath, engine='pyarrow', compression='snappy')
        
        file_size = os.path.getsize(filepath)
        print(f"  ✓ Created {filename}")
        print(f"    Rows: {len(data)}, Size: {file_size / 1024:.2f} KB")
        print(f"    Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}\n")
    
    print("=" * 70)
    print(f"✓ Created {len(symbols)} sample data files")
    print("=" * 70)
    print("\nYou can now run:")
    print("  python example_offline.py")


def test_data_fetcher():
    """Test DataFetcher with parquet loading"""
    from backtesting.data_fetcher import DataFetcher
    
    print("\n" + "=" * 70)
    print("Testing DataFetcher with Sample Cached Data")
    print("=" * 70)
    
    # Create sample data first
    symbol = 'TEST'
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    data_dir = 'data'
    
    print(f"\nCreating sample data for {symbol}...")
    data = generate_sample_data(symbol, start_date, end_date)
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}_{start_date}_{end_date}.parquet"
    filepath = os.path.join(data_dir, filename)
    data.to_parquet(filepath, engine='pyarrow', compression='snappy')
    print(f"  ✓ Saved to {filepath}")
    
    # Test loading from parquet
    print(f"\nTesting load_from_parquet()...")
    fetcher = DataFetcher()
    loaded_data = fetcher.load_from_parquet(filepath)
    print(f"  ✓ Loaded {len(loaded_data)} rows")
    print(f"  Columns: {list(loaded_data.columns)}")
    print(f"  Date range: {loaded_data.index[0]} to {loaded_data.index[-1]}")
    
    # Test fetch_or_load with cache
    print(f"\nTesting fetch_or_load() with cache...")
    cached_data = fetcher.fetch_or_load(symbol, start_date, end_date, 
                                        data_dir=data_dir, use_cache=True)
    print(f"  ✓ Loaded {len(cached_data)} rows from cache")
    
    print("\n" + "=" * 70)
    print("✓ DataFetcher tests passed!")
    print("=" * 70)


def test_backtest_engine():
    """Test BacktestEngine with cached data"""
    from backtesting.engine import BacktestEngine
    from backtesting.strategies import SMAStrategy
    
    print("\n" + "=" * 70)
    print("Testing BacktestEngine with Cached Data")
    print("=" * 70)
    
    # Create sample data
    symbol = 'TESTSTOCK'
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    data_dir = 'data'
    
    print(f"\nCreating sample data for {symbol}...")
    data = generate_sample_data(symbol, start_date, end_date)
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    filename = f"{symbol}_{start_date}_{end_date}.parquet"
    filepath = os.path.join(data_dir, filename)
    data.to_parquet(filepath, engine='pyarrow', compression='snappy')
    print(f"  ✓ Saved to {filepath}")
    
    # Test BacktestEngine with cached data
    print(f"\nInitializing BacktestEngine with cached data...")
    engine = BacktestEngine(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        initial_capital=10000,
        use_cache=True,
        data_dir=data_dir
    )
    print(f"  ✓ Engine initialized with {len(engine.data)} rows")
    
    # Run a simple backtest
    print(f"\nRunning backtest with SMA strategy...")
    strategy = SMAStrategy(short_window=20, long_window=50)
    results = engine.run(strategy)
    
    metrics = results['metrics']
    print(f"  ✓ Backtest completed")
    print(f"    Total Return: {metrics['total_return']:.2f}%")
    print(f"    Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"    Number of Trades: {metrics['num_trades']}")
    
    print("\n" + "=" * 70)
    print("✓ BacktestEngine tests passed!")
    print("=" * 70)


def main():
    """Main test function"""
    print("\n" + "=" * 70)
    print("TESTING DATA CACHING FUNCTIONALITY")
    print("=" * 70)
    
    # Create sample cached data for offline backtesting demo
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    
    create_sample_cache(symbols, start_date, end_date)
    
    # Test DataFetcher
    test_data_fetcher()
    
    # Test BacktestEngine
    test_backtest_engine()
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED!")
    print("=" * 70)
    print("\nSample data has been created in the 'data/' directory.")
    print("You can now run the offline backtesting example:")
    print("  python example_offline.py")


if __name__ == '__main__':
    main()
