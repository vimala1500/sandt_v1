"""
Backtesting engine for testing trading strategies
"""

import pandas as pd
import numpy as np
from backtesting.data_fetcher import DataFetcher


class BacktestEngine:
    """Engine for backtesting trading strategies"""
    
    def __init__(self, symbol, start_date, end_date, initial_capital=10000):
        """
        Initialize backtesting engine
        
        Args:
            symbol (str): Stock ticker symbol
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
            initial_capital (float): Initial investment capital
        """
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        
        # Fetch data
        fetcher = DataFetcher()
        self.data = fetcher.fetch_data(symbol, start_date, end_date)
    
    def run(self, strategy):
        """
        Run backtest with given strategy
        
        Args:
            strategy: Trading strategy object
            
        Returns:
            dict: Backtest results with performance metrics
        """
        # Generate signals using strategy
        df = strategy.generate_signals(self.data)
        
        # Calculate portfolio value
        df = self._calculate_portfolio(df)
        
        # Calculate performance metrics
        metrics = self._calculate_metrics(df)
        
        return {
            'strategy': strategy.name,
            'symbol': self.symbol,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': self.initial_capital,
            'final_capital': df['portfolio_value'].iloc[-1],
            'data': df,
            'metrics': metrics
        }
    
    def _calculate_portfolio(self, df):
        """Calculate portfolio value over time"""
        df = df.copy()
        
        # Initialize portfolio
        df['holdings'] = 0
        df['cash'] = float(self.initial_capital)
        df['portfolio_value'] = float(self.initial_capital)
        
        position = 0  # 0: no position, 1: long position
        shares = 0
        cash = float(self.initial_capital)
        
        for i in range(len(df)):
            if pd.isna(df['position'].iloc[i]):
                df.loc[df.index[i], 'holdings'] = shares * df['close'].iloc[i]
                df.loc[df.index[i], 'cash'] = cash
                df.loc[df.index[i], 'portfolio_value'] = cash + shares * df['close'].iloc[i]
                continue
            
            # Buy signal
            if df['position'].iloc[i] > 0 and position == 0:
                shares = cash / df['close'].iloc[i]
                cash = 0
                position = 1
            
            # Sell signal
            elif df['position'].iloc[i] < 0 and position == 1:
                cash = shares * df['close'].iloc[i]
                shares = 0
                position = 0
            
            df.loc[df.index[i], 'holdings'] = shares * df['close'].iloc[i]
            df.loc[df.index[i], 'cash'] = cash
            df.loc[df.index[i], 'portfolio_value'] = cash + shares * df['close'].iloc[i]
        
        return df
    
    def _calculate_metrics(self, df):
        """Calculate performance metrics"""
        # Total return
        total_return = ((df['portfolio_value'].iloc[-1] - self.initial_capital) / 
                       self.initial_capital * 100)
        
        # Buy and hold return
        buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[0]) / 
                          df['close'].iloc[0] * 100)
        
        # Daily returns
        df['daily_return'] = df['portfolio_value'].pct_change()
        
        # Sharpe ratio (annualized)
        sharpe_ratio = (df['daily_return'].mean() / df['daily_return'].std() * 
                       np.sqrt(252) if df['daily_return'].std() != 0 else 0)
        
        # Max drawdown
        rolling_max = df['portfolio_value'].expanding().max()
        drawdown = (df['portfolio_value'] - rolling_max) / rolling_max
        max_drawdown = drawdown.min() * 100
        
        # Number of trades
        num_trades = int(df['position'].abs().sum() / 2)
        
        # Win rate (if applicable)
        win_rate = 0
        if num_trades > 0:
            trades = df[df['position'] != 0].copy()
            wins = 0
            for i in range(0, len(trades), 2):
                if i + 1 < len(trades):
                    entry_price = trades['close'].iloc[i]
                    exit_price = trades['close'].iloc[i + 1]
                    if exit_price > entry_price:
                        wins += 1
            win_rate = (wins / (num_trades / 2) * 100) if num_trades > 0 else 0
        
        return {
            'total_return': round(total_return, 2),
            'buy_hold_return': round(buy_hold_return, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'num_trades': num_trades,
            'win_rate': round(win_rate, 2)
        }
