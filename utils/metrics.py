"""
Performance metrics calculations
"""

import numpy as np
import pandas as pd


def calculate_total_return(initial_value, final_value):
    """
    Calculate total return percentage
    
    Args:
        initial_value (float): Initial portfolio value
        final_value (float): Final portfolio value
        
    Returns:
        float: Total return percentage
    """
    return ((final_value - initial_value) / initial_value) * 100


def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio (annualized)
    
    Args:
        returns (pd.Series): Daily returns
        risk_free_rate (float): Annual risk-free rate (default: 2%)
        
    Returns:
        float: Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / 252)
    if excess_returns.std() == 0:
        return 0
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)


def calculate_max_drawdown(portfolio_values):
    """
    Calculate maximum drawdown
    
    Args:
        portfolio_values (pd.Series): Portfolio values over time
        
    Returns:
        float: Maximum drawdown percentage
    """
    rolling_max = portfolio_values.expanding().max()
    drawdown = (portfolio_values - rolling_max) / rolling_max
    return drawdown.min() * 100


def calculate_win_rate(trades_df):
    """
    Calculate win rate from trades
    
    Args:
        trades_df (pd.DataFrame): DataFrame with trade information
        
    Returns:
        float: Win rate percentage
    """
    if len(trades_df) == 0:
        return 0
    
    winning_trades = len(trades_df[trades_df['pnl'] > 0])
    return (winning_trades / len(trades_df)) * 100


def calculate_volatility(returns):
    """
    Calculate annualized volatility
    
    Args:
        returns (pd.Series): Daily returns
        
    Returns:
        float: Annualized volatility
    """
    return returns.std() * np.sqrt(252)


def calculate_sortino_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sortino ratio (annualized)
    
    Args:
        returns (pd.Series): Daily returns
        risk_free_rate (float): Annual risk-free rate (default: 2%)
        
    Returns:
        float: Sortino ratio
    """
    excess_returns = returns - (risk_free_rate / 252)
    downside_returns = returns[returns < 0]
    
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0
    
    return (excess_returns.mean() / downside_returns.std()) * np.sqrt(252)
