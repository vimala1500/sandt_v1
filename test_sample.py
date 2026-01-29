"""
Test script with sample data (no internet required)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backtesting.strategies import SMAStrategy, EMAStrategy, RSIStrategy


def generate_sample_data(days=500):
    """Generate sample stock data for testing"""
    
    # Create date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate random price data with trend
    np.random.seed(42)
    base_price = 100
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


def test_strategies():
    """Test all trading strategies with sample data"""
    
    print("=" * 60)
    print("Stock Backtesting Test (Sample Data)")
    print("=" * 60)
    
    # Generate sample data
    print("\nGenerating sample stock data...")
    data = generate_sample_data(days=500)
    
    print(f"Data period: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
    print(f"Number of days: {len(data)}")
    print(f"Starting price: ${data['close'].iloc[0]:.2f}")
    print(f"Ending price: ${data['close'].iloc[-1]:.2f}")
    
    # Test different strategies
    strategies = [
        SMAStrategy(short_window=20, long_window=50),
        EMAStrategy(short_window=12, long_window=26),
        RSIStrategy(window=14)
    ]
    
    print("\nTesting strategies...\n")
    
    for strategy in strategies:
        print(f"{'=' * 60}")
        print(f"Strategy: {strategy.name}")
        print('=' * 60)
        
        try:
            # Generate signals
            df = strategy.generate_signals(data)
            
            # Count signals
            buy_signals = len(df[df['position'] > 0])
            sell_signals = len(df[df['position'] < 0])
            
            print(f"\nSignals generated successfully!")
            print(f"  Buy signals:  {buy_signals}")
            print(f"  Sell signals: {sell_signals}")
            print(f"  Data rows:    {len(df)}")
            
            # Show sample of data with signals
            signal_rows = df[df['position'] != 0].head(5)
            if not signal_rows.empty:
                print(f"\nFirst few signals:")
                for idx, row in signal_rows.iterrows():
                    signal_type = "BUY" if row['position'] > 0 else "SELL"
                    print(f"  {idx.strftime('%Y-%m-%d')}: {signal_type} at ${row['close']:.2f}")
            
            print(f"\n✓ {strategy.name} test passed!")
            
        except Exception as e:
            print(f"\n✗ {strategy.name} test failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


def test_backtesting_logic():
    """Test the backtesting logic without fetching real data"""
    
    print("\n" + "=" * 60)
    print("Testing Backtesting Engine Logic")
    print("=" * 60)
    
    # Generate sample data
    data = generate_sample_data(days=365)
    
    # Create a simple strategy
    strategy = SMAStrategy(short_window=20, long_window=50)
    df = strategy.generate_signals(data)
    
    # Simulate portfolio calculation
    initial_capital = 10000
    cash = initial_capital
    shares = 0
    portfolio_values = []
    
    for i in range(len(df)):
        if pd.notna(df['position'].iloc[i]):
            # Buy signal
            if df['position'].iloc[i] > 0 and shares == 0:
                shares = cash / df['close'].iloc[i]
                cash = 0
            
            # Sell signal
            elif df['position'].iloc[i] < 0 and shares > 0:
                cash = shares * df['close'].iloc[i]
                shares = 0
        
        portfolio_value = cash + shares * df['close'].iloc[i]
        portfolio_values.append(portfolio_value)
    
    final_value = portfolio_values[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    
    print(f"\nBacktest Results:")
    print(f"  Initial Capital: ${initial_capital:,.2f}")
    print(f"  Final Value:     ${final_value:,.2f}")
    print(f"  Total Return:    {total_return:.2f}%")
    
    # Buy and hold comparison
    initial_shares = initial_capital / df['close'].iloc[0]
    buy_hold_value = initial_shares * df['close'].iloc[-1]
    buy_hold_return = ((buy_hold_value - initial_capital) / initial_capital) * 100
    
    print(f"\nBuy & Hold Comparison:")
    print(f"  Final Value:     ${buy_hold_value:,.2f}")
    print(f"  Total Return:    {buy_hold_return:.2f}%")
    
    print(f"\n✓ Backtesting logic test passed!")


if __name__ == '__main__':
    test_strategies()
    test_backtesting_logic()
