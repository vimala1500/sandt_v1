"""
Example script demonstrating offline backtesting using cached parquet data

This script shows how to:
1. Use pre-downloaded data stored in parquet format
2. Run backtests without internet connectivity
3. Compare results across multiple stocks

Before running this script, download data using:
    python download_data.py --symbols AAPL MSFT --start 2022-01-01 --end 2023-12-31
"""

import os
from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy, EMAStrategy, RSIStrategy


def run_offline_backtest(symbol, start_date, end_date, data_dir='data'):
    """
    Run backtest using cached data
    
    Args:
        symbol (str): Stock ticker symbol
        start_date (str): Start date
        end_date (str): End date
        data_dir (str): Directory containing cached parquet files
    """
    print("=" * 70)
    print(f"Offline Backtesting: {symbol}")
    print("=" * 70)
    
    # Configuration
    initial_capital = 10000
    
    print(f"\nSymbol: {symbol}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    
    # Check if cached data exists
    parquet_file = os.path.join(data_dir, f"{symbol}_{start_date}_{end_date}.parquet")
    if not os.path.exists(parquet_file):
        print(f"\n❌ Error: Cached data not found at {parquet_file}")
        print(f"\nPlease download data first using:")
        print(f"  python download_data.py --symbol {symbol} --start {start_date} --end {end_date}")
        return
    
    # Initialize backtest engine with cached data
    print(f"\nLoading cached data from {parquet_file}...")
    engine = BacktestEngine(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        use_cache=True,
        data_dir=data_dir
    )
    
    # Test different strategies
    strategies = [
        SMAStrategy(short_window=20, long_window=50),
        EMAStrategy(short_window=12, long_window=26),
        RSIStrategy(window=14)
    ]
    
    print("\nRunning backtests...\n")
    
    results_summary = []
    
    for strategy in strategies:
        print(f"{'=' * 70}")
        print(f"Strategy: {strategy.name}")
        print('=' * 70)
        
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
        print()
        
        # Store for summary
        results_summary.append({
            'strategy': strategy.name,
            'return': metrics['total_return'],
            'sharpe': metrics['sharpe_ratio'],
            'trades': metrics['num_trades']
        })
    
    # Print comparison summary
    print("=" * 70)
    print("Strategy Comparison Summary")
    print("=" * 70)
    print(f"{'Strategy':<30} {'Return %':>12} {'Sharpe':>10} {'Trades':>8}")
    print("-" * 70)
    for result in results_summary:
        print(f"{result['strategy']:<30} {result['return']:>12.2f} {result['sharpe']:>10.2f} {result['trades']:>8}")
    
    print("\n" + "=" * 70)
    print("✓ Offline Backtest Complete!")
    print("=" * 70)


def run_multi_symbol_comparison(symbols, start_date, end_date, data_dir='data'):
    """
    Compare same strategy across multiple stocks using cached data
    
    Args:
        symbols (list): List of stock ticker symbols
        start_date (str): Start date
        end_date (str): End date
        data_dir (str): Directory containing cached parquet files
    """
    print("=" * 70)
    print("Multi-Symbol Strategy Comparison (Offline)")
    print("=" * 70)
    
    strategy = SMAStrategy(short_window=20, long_window=50)
    initial_capital = 10000
    
    print(f"\nStrategy: {strategy.name}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Symbols: {', '.join(symbols)}\n")
    
    results_summary = []
    
    for symbol in symbols:
        parquet_file = os.path.join(data_dir, f"{symbol}_{start_date}_{end_date}.parquet")
        
        if not os.path.exists(parquet_file):
            print(f"⚠️  {symbol}: Cached data not found, skipping...")
            continue
        
        try:
            print(f"Processing {symbol}...")
            
            # Initialize backtest engine with cached data
            engine = BacktestEngine(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                initial_capital=initial_capital,
                use_cache=True,
                data_dir=data_dir
            )
            
            # Run backtest
            results = engine.run(strategy)
            metrics = results['metrics']
            final_value = results['final_capital']
            profit = final_value - initial_capital
            
            results_summary.append({
                'symbol': symbol,
                'return': metrics['total_return'],
                'buy_hold': metrics['buy_hold_return'],
                'sharpe': metrics['sharpe_ratio'],
                'max_drawdown': metrics['max_drawdown'],
                'trades': metrics['num_trades'],
                'final_value': final_value,
                'profit': profit
            })
            
            print(f"✓ {symbol}: Return {metrics['total_return']:.2f}%, "
                  f"Sharpe {metrics['sharpe_ratio']:.2f}, "
                  f"Trades {metrics['num_trades']}")
            
        except Exception as e:
            print(f"✗ {symbol}: Error - {str(e)}")
    
    if not results_summary:
        print("\n❌ No results to display. Please download data first.")
        return
    
    # Print detailed comparison
    print("\n" + "=" * 70)
    print("Detailed Comparison")
    print("=" * 70)
    print(f"{'Symbol':<8} {'Return %':>10} {'Buy&Hold':>10} {'Sharpe':>8} {'MaxDD %':>10} {'Trades':>8} {'Profit $':>12}")
    print("-" * 70)
    
    for result in sorted(results_summary, key=lambda x: x['return'], reverse=True):
        print(f"{result['symbol']:<8} "
              f"{result['return']:>10.2f} "
              f"{result['buy_hold']:>10.2f} "
              f"{result['sharpe']:>8.2f} "
              f"{result['max_drawdown']:>10.2f} "
              f"{result['trades']:>8} "
              f"{result['profit']:>12.2f}")
    
    # Find best performer
    best = max(results_summary, key=lambda x: x['return'])
    print("\n" + "=" * 70)
    print(f"🏆 Best Performer: {best['symbol']} with {best['return']:.2f}% return")
    print("=" * 70)


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("OFFLINE BACKTESTING DEMO")
    print("Using Cached Parquet Data")
    print("=" * 70 + "\n")
    
    # Example 1: Single symbol backtest
    print("\n### Example 1: Single Symbol Backtesting ###\n")
    run_offline_backtest(
        symbol='AAPL',
        start_date='2022-01-01',
        end_date='2023-12-31'
    )
    
    # Example 2: Multi-symbol comparison
    print("\n\n### Example 2: Multi-Symbol Comparison ###\n")
    run_multi_symbol_comparison(
        symbols=['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
        start_date='2022-01-01',
        end_date='2023-12-31'
    )
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nNote: This demo requires pre-downloaded data.")
    print("If you see errors, download data first using:")
    print("  python download_data.py --symbols AAPL MSFT GOOGL AMZN --start 2022-01-01 --end 2023-12-31")


if __name__ == '__main__':
    main()
