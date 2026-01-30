# Data Downloading and Caching Guide

This guide explains how to download stock data from yfinance, store it in efficient parquet format, and use it for offline backtesting.

## Table of Contents

1. [Overview](#overview)
2. [Benefits of Data Caching](#benefits-of-data-caching)
3. [Quick Start](#quick-start)
4. [Download Script Usage](#download-script-usage)
5. [Offline Backtesting](#offline-backtesting)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Overview

The data caching system allows you to:
- Download historical stock data once from Yahoo Finance
- Store it in compressed parquet format for efficient storage
- Use cached data for backtesting without internet connectivity
- Speed up backtesting by loading data from local files

## Benefits of Data Caching

### 1. **No Internet Required**
Once data is downloaded, you can run backtests offline. This is especially useful for:
- Cloud Run deployments with limited egress connectivity
- Development environments with restricted network access
- Faster iteration during strategy development

### 2. **Faster Performance**
- Parquet files load 10-50x faster than CSV files
- No network latency or API rate limits
- Immediate data access for backtesting

### 3. **Efficient Storage**
- Compressed parquet files are 60-80% smaller than CSV
- Type information is preserved (no parsing overhead)
- Columnar storage format optimized for analytics

### 4. **Reproducibility**
- Downloaded data is frozen at a point in time
- Ensures consistent backtest results
- Easy to share data with team members

## Quick Start

### 1. Download Data

```bash
# Download single stock
python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31

# Download multiple stocks
python download_data.py --symbols AAPL MSFT GOOGL AMZN --start 2020-01-01 --end 2023-12-31

# Download popular stocks
python download_data.py --popular --start 2022-01-01 --end 2023-12-31
```

### 2. List Cached Data

```bash
python download_data.py --list
```

### 3. Run Offline Backtest

```bash
python example_offline.py
```

Or use programmatically:

```python
from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy

# Use cached data
engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000,
    use_cache=True
)

strategy = SMAStrategy(short_window=20, long_window=50)
results = engine.run(strategy)
```

## Download Script Usage

### Basic Commands

#### Download Single Symbol

```bash
python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31
```

#### Download Multiple Symbols

```bash
python download_data.py --symbols AAPL MSFT GOOGL --start 2020-01-01 --end 2023-12-31
```

#### Download Popular Stocks

Downloads 15 popular stocks (AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA, JPM, V, WMT, DIS, NFLX, PYPL, INTC, AMD):

```bash
python download_data.py --popular --start 2022-01-01 --end 2023-12-31
```

#### List Cached Data

```bash
python download_data.py --list
```

#### Force Re-download

Re-download data even if it already exists:

```bash
python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31 --force
```

#### Custom Data Directory

Specify a different directory for storing data:

```bash
python download_data.py --symbol AAPL --start 2020-01-01 --end 2023-12-31 --data-dir my_data
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--symbol SYMBOL` | Download single stock symbol |
| `--symbols SYMBOL [SYMBOL ...]` | Download multiple stock symbols |
| `--popular` | Download popular stocks |
| `--start YYYY-MM-DD` | Start date for data (required unless --list) |
| `--end YYYY-MM-DD` | End date for data (required unless --list) |
| `--data-dir DIR` | Directory to store parquet files (default: data) |
| `--force` | Force re-download even if data exists |
| `--list` | List all cached data files |
| `--help` | Show help message |

## Offline Backtesting

### Using BacktestEngine

The `BacktestEngine` supports three modes:

#### 1. Automatic Cache (Recommended)

Uses cached data if available, otherwise downloads from yfinance:

```python
engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000,
    use_cache=True  # Default behavior
)
```

#### 2. Force Download

Always download from yfinance, ignore cache:

```python
engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000,
    data_source='yfinance'
)
```

#### 3. Specific Parquet File

Load from a specific parquet file:

```python
engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000,
    data_source='data/AAPL_2022-01-01_2023-12-31.parquet'
)
```

### Using DataFetcher Directly

```python
from backtesting.data_fetcher import DataFetcher

fetcher = DataFetcher()

# Load from parquet file
data = fetcher.load_from_parquet('data/AAPL_2022-01-01_2023-12-31.parquet')

# Fetch or load (uses cache if available)
data = fetcher.fetch_or_load('AAPL', '2022-01-01', '2023-12-31', use_cache=True)
```

## API Reference

### DataFetcher Methods

#### `load_from_parquet(parquet_file)`

Load stock data from a parquet file.

**Parameters:**
- `parquet_file` (str): Path to parquet file

**Returns:**
- `pd.DataFrame`: Historical stock data with OHLCV columns

**Raises:**
- `FileNotFoundError`: If parquet file doesn't exist
- `Exception`: If error reading parquet file

#### `fetch_or_load(symbol, start_date, end_date, data_dir='data', use_cache=True)`

Fetch data from cache if available, otherwise download from yfinance.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `start_date` (str): Start date in 'YYYY-MM-DD' format
- `end_date` (str): End date in 'YYYY-MM-DD' format
- `data_dir` (str): Directory containing cached parquet files (default: 'data')
- `use_cache` (bool): If True, try to load from cache first (default: True)

**Returns:**
- `pd.DataFrame`: Historical stock data with OHLCV columns

### BacktestEngine Parameters

#### Additional Parameters for Caching

- `data_source` (str, optional): Path to parquet file or 'yfinance' to fetch from API
- `use_cache` (bool): If True, try to use cached data first (default: True)
- `data_dir` (str): Directory containing cached parquet files (default: 'data')

## Examples

### Example 1: Download and Backtest

```python
# Step 1: Download data (run once)
# python download_data.py --symbol AAPL --start 2022-01-01 --end 2023-12-31

# Step 2: Run backtest using cached data
from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy

engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000,
    use_cache=True
)

strategy = SMAStrategy(short_window=20, long_window=50)
results = engine.run(strategy)
print(f"Total Return: {results['metrics']['total_return']:.2f}%")
```

### Example 2: Multi-Symbol Comparison

```python
from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy

symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
strategy = SMAStrategy(short_window=20, long_window=50)

results = []
for symbol in symbols:
    engine = BacktestEngine(
        symbol=symbol,
        start_date='2022-01-01',
        end_date='2023-12-31',
        initial_capital=10000,
        use_cache=True
    )
    result = engine.run(strategy)
    results.append({
        'symbol': symbol,
        'return': result['metrics']['total_return']
    })

# Display comparison
for r in sorted(results, key=lambda x: x['return'], reverse=True):
    print(f"{r['symbol']}: {r['return']:.2f}%")
```

### Example 3: Batch Download for Multiple Years

```bash
# Download data for multiple time periods
for year in 2020 2021 2022 2023; do
    python download_data.py \
        --symbols AAPL MSFT GOOGL \
        --start ${year}-01-01 \
        --end ${year}-12-31
done
```

## Troubleshooting

### "No cached data found"

**Problem:** Backtest fails with message about missing cached data.

**Solution:** Download the data first:
```bash
python download_data.py --symbol AAPL --start 2022-01-01 --end 2023-12-31
```

### "Failed to download data"

**Problem:** Download script fails with network errors.

**Solution:** 
1. Check internet connectivity
2. Verify Yahoo Finance is accessible
3. Try increasing timeout:
   ```bash
   export YFINANCE_TIMEOUT=60
   python download_data.py --symbol AAPL --start 2022-01-01 --end 2023-12-31
   ```

### File Size Too Large

**Problem:** Parquet files are larger than expected.

**Solution:** 
- Parquet files are already compressed with snappy compression
- Consider downloading shorter date ranges
- Each year of daily data is typically 40-50 KB per symbol

### Wrong Date Range

**Problem:** Cached data has different date range than needed.

**Solution:**
1. Download data with the correct date range
2. Or use `data_source='yfinance'` to force download:
   ```python
   engine = BacktestEngine(
       symbol='AAPL',
       start_date='2020-01-01',
       end_date='2023-12-31',
       initial_capital=10000,
       data_source='yfinance'  # Force download
   )
   ```

### Parquet File Corrupted

**Problem:** Error reading parquet file.

**Solution:** Re-download with `--force`:
```bash
python download_data.py --symbol AAPL --start 2022-01-01 --end 2023-12-31 --force
```

## Best Practices

1. **Download Once, Use Many Times**: Download data once and reuse for multiple backtests
2. **Organize by Date Range**: Use consistent date ranges for easy comparison
3. **Regular Updates**: Update cached data periodically for recent market data
4. **Backup Data**: Back up your data directory to avoid re-downloading
5. **Version Control**: Don't commit data files to git (already in .gitignore)

## File Format

Parquet files are named using the convention:
```
{SYMBOL}_{START_DATE}_{END_DATE}.parquet
```

Examples:
- `AAPL_2022-01-01_2023-12-31.parquet`
- `MSFT_2020-01-01_2023-12-31.parquet`

Each file contains:
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Trading volume

Index: DatetimeIndex with trading dates
