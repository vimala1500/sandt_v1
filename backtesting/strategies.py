"""
Trading strategies for backtesting
"""

import pandas as pd
import numpy as np


class BaseStrategy:
    """Base class for trading strategies"""
    
    def __init__(self):
        """Initialize base strategy"""
        self.name = "Base Strategy"
    
    def generate_signals(self, data):
        """
        Generate trading signals based on the strategy
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with additional signal columns
        """
        raise NotImplementedError("Strategy must implement generate_signals method")


class SMAStrategy(BaseStrategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, short_window=20, long_window=50):
        """
        Initialize SMA strategy
        
        Args:
            short_window (int): Short-term moving average window
            long_window (int): Long-term moving average window
        """
        super().__init__()
        self.name = f"SMA Strategy ({short_window}/{long_window})"
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data):
        """Generate trading signals based on SMA crossover"""
        df = data.copy()
        
        # Calculate moving averages
        df['sma_short'] = df['close'].rolling(window=self.short_window).mean()
        df['sma_long'] = df['close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1  # Buy signal
        df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1  # Sell signal
        
        # Generate trading orders (when signal changes)
        df['position'] = df['signal'].diff()
        
        return df


class EMAStrategy(BaseStrategy):
    """Exponential Moving Average Crossover Strategy"""
    
    def __init__(self, short_window=12, long_window=26):
        """
        Initialize EMA strategy
        
        Args:
            short_window (int): Short-term EMA window
            long_window (int): Long-term EMA window
        """
        super().__init__()
        self.name = f"EMA Strategy ({short_window}/{long_window})"
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data):
        """Generate trading signals based on EMA crossover"""
        df = data.copy()
        
        # Calculate exponential moving averages
        df['ema_short'] = df['close'].ewm(span=self.short_window, adjust=False).mean()
        df['ema_long'] = df['close'].ewm(span=self.long_window, adjust=False).mean()
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['ema_short'] > df['ema_long'], 'signal'] = 1  # Buy signal
        df.loc[df['ema_short'] < df['ema_long'], 'signal'] = -1  # Sell signal
        
        # Generate trading orders
        df['position'] = df['signal'].diff()
        
        return df


class RSIStrategy(BaseStrategy):
    """Relative Strength Index Strategy"""
    
    def __init__(self, window=14, oversold=30, overbought=70):
        """
        Initialize RSI strategy
        
        Args:
            window (int): RSI calculation window
            oversold (int): Oversold threshold (buy signal)
            overbought (int): Overbought threshold (sell signal)
        """
        super().__init__()
        self.name = f"RSI Strategy (window={window})"
        self.window = window
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, data):
        """Calculate RSI indicator"""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.window).mean()
        
        # Avoid division by zero - when loss is 0, RSI is 100
        rs = gain / loss.replace(0, np.nan)
        rs = rs.fillna(float('inf'))
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_signals(self, data):
        """Generate trading signals based on RSI"""
        df = data.copy()
        
        # Calculate RSI
        df['rsi'] = self.calculate_rsi(df)
        
        # Generate signals
        df['signal'] = 0
        df.loc[df['rsi'] < self.oversold, 'signal'] = 1  # Buy signal (oversold)
        df.loc[df['rsi'] > self.overbought, 'signal'] = -1  # Sell signal (overbought)
        
        # Generate trading orders
        df['position'] = df['signal'].diff()
        
        return df
