# Stock Backtesting and Dashboard (SandT v1)

A Python-based stock backtesting application with an interactive Dash frontend for visualizing trading strategies and performance.

## Features

- **Stock Data Fetching**: Download historical stock data using Yahoo Finance API (requires internet connectivity)
- **Backtesting Engine**: Test trading strategies on historical data
- **Interactive Dashboard**: Visualize backtest results with Dash and Plotly
- **Strategy Analysis**: Analyze strategy performance with key metrics
- **Multiple Strategies**: Support for various trading strategies (SMA, EMA, RSI)
- **Robust Error Handling**: Automatic retry logic for transient network failures
- **Configurable Timeouts**: Adjust request timeouts and retry attempts via environment variables

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- **Internet connectivity** (required for fetching stock data from Yahoo Finance API)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vimala1500/sandt_v1.git
cd sandt_v1
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env to customize timeout and retry settings
# YFINANCE_TIMEOUT=60
# YFINANCE_MAX_RETRIES=3
```

## Usage

### Running the Dashboard Locally

Start the Dash application:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:8050`

### Deploying to Google Cloud Run

Want to deploy your dashboard to the cloud? Check out our comprehensive deployment guide:

📖 **[Complete GCP Deployment Guide](DEPLOY_TO_GCP.md)**

This beginner-friendly guide covers:
- Google Cloud Platform setup
- Docker containerization
- Cloud Run deployment
- Optional Cloud SQL database setup
- Cost optimization tips

Perfect for those with no prior GCP experience!

### Running a Backtest

You can run backtests programmatically:

```python
from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy

# Initialize backtest engine
engine = BacktestEngine(
    symbol='AAPL',
    start_date='2022-01-01',
    end_date='2023-12-31',
    initial_capital=10000
)

# Run strategy
strategy = SMAStrategy(short_window=20, long_window=50)
results = engine.run(strategy)

# Display results
print(results)
```

## Project Structure

```
sandt_v1/
├── app.py                      # Main Dash application
├── backtesting/               # Backtesting engine
│   ├── __init__.py
│   ├── engine.py             # Core backtesting logic
│   ├── strategies.py         # Trading strategies
│   └── data_fetcher.py       # Stock data fetching
├── dashboard/                 # Dashboard components
│   ├── __init__.py
│   ├── layout.py             # Dashboard layout
│   └── callbacks.py          # Dash callbacks
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── metrics.py            # Performance metrics
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Trading Strategies

### Simple Moving Average (SMA)
- Buy signal: Short-term SMA crosses above long-term SMA
- Sell signal: Short-term SMA crosses below long-term SMA

### Exponential Moving Average (EMA)
- Buy signal: Short-term EMA crosses above long-term EMA
- Sell signal: Short-term EMA crosses below long-term EMA

### Relative Strength Index (RSI)
- Buy signal: RSI crosses below oversold threshold (default: 30)
- Sell signal: RSI crosses above overbought threshold (default: 70)

## Performance Metrics

The backtesting engine calculates the following metrics:

- **Total Return**: Overall percentage return
- **Sharpe Ratio**: Risk-adjusted return
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Number of Trades**: Total trades executed

## Network Requirements

This application requires internet access to fetch stock data from Yahoo Finance API. The following domains must be accessible:

- `query1.finance.yahoo.com` (primary API endpoint)
- `query2.finance.yahoo.com` (backup API endpoint)
- `fc.yahoo.com` (session management)

### Configuration

You can configure the data fetching behavior using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `YFINANCE_TIMEOUT` | 30 | Request timeout in seconds |
| `YFINANCE_MAX_RETRIES` | 3 | Maximum retry attempts for failed requests |

### Troubleshooting Data Fetching Issues

If you encounter "No data found for symbol" errors:

1. **Check internet connectivity**: Ensure you can access Yahoo Finance websites
2. **Verify firewall settings**: Make sure outbound HTTPS (port 443) is allowed
3. **Review logs**: Check application logs for detailed error messages
4. **Increase timeout**: Set `YFINANCE_TIMEOUT=60` for slow connections
5. **Cloud Run deployment**: Ensure egress connectivity is enabled (see deployment guide)

For detailed diagnosis and solutions, see [STOCK_DATA_FETCHING_ANALYSIS.md](STOCK_DATA_FETCHING_ANALYSIS.md).

## Testing

Run the test suite to verify functionality:

```bash
# Test strategies with sample data (no internet required)
python test_sample.py

# Test data fetcher (includes unit tests with mocks)
python test_data_fetcher.py

# Test repository structure
python test_structure.py
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
