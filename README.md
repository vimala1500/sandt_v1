# Stock Backtesting and Dashboard (SandT v1)

A Python-based stock backtesting application with an interactive Dash frontend for visualizing trading strategies and performance.

## Features

- **Stock Data Fetching**: Download historical stock data using Yahoo Finance API
- **Backtesting Engine**: Test trading strategies on historical data
- **Interactive Dashboard**: Visualize backtest results with Dash and Plotly
- **Strategy Analysis**: Analyze strategy performance with key metrics
- **Multiple Strategies**: Support for various trading strategies (SMA, EMA, RSI)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

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

## Usage

### Running the Dashboard

Start the Dash application:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:8050`

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

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
