"""
Example script demonstrating how to use the backtesting engine
"""

from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy, EMAStrategy, RSIStrategy


def run_simple_backtest():
    """Run a simple backtest example"""
    
    print("=" * 60)
    print("Stock Backtesting Example")
    print("=" * 60)
    
    # Configuration
    symbol = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2023-12-31'
    initial_capital = 10000
    
    print(f"\nSymbol: {symbol}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    
    # Initialize backtest engine
    print("\nFetching data...")
    engine = BacktestEngine(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital
    )
    
    # Test different strategies
    strategies = [
        SMAStrategy(short_window=20, long_window=50),
        EMAStrategy(short_window=12, long_window=26),
        RSIStrategy(window=14)
    ]
    
    print("\nRunning backtests...\n")
    
    for strategy in strategies:
        print(f"\n{'=' * 60}")
        print(f"Strategy: {strategy.name}")
        print('=' * 60)
        
        # Run backtest
        results = engine.run(strategy)
        
        # Display results
        metrics = results['metrics']
        
        print(f"\nPerformance Metrics:")
        print(f"  Total Return:     {metrics['total_return']:>8.2f}%")
        print(f"  Buy & Hold:       {metrics['buy_hold_return']:>8.2f}%")
        print(f"  Sharpe Ratio:     {metrics['sharpe_ratio']:>8.2f}")
        print(f"  Max Drawdown:     {metrics['max_drawdown']:>8.2f}%")
        print(f"  Number of Trades: {metrics['num_trades']:>8}")
        print(f"  Win Rate:         {metrics['win_rate']:>8.2f}%")
        
        final_value = results['final_capital']
        profit = final_value - initial_capital
        
        print(f"\nFinal Portfolio Value: ${final_value:,.2f}")
        print(f"Profit/Loss: ${profit:,.2f}")
    
    print("\n" + "=" * 60)
    print("Backtest Complete!")
    print("=" * 60)


if __name__ == '__main__':
    run_simple_backtest()
