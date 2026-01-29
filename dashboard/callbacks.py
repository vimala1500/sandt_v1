"""
Dashboard callbacks for handling user interactions
"""

from dash.dependencies import Input, Output, State
from dash import no_update
import plotly.graph_objs as go
from datetime import datetime

from backtesting.engine import BacktestEngine
from backtesting.strategies import SMAStrategy, EMAStrategy, RSIStrategy
from dashboard.layout import create_results_layout


def register_callbacks(app):
    """Register all dashboard callbacks"""
    
    @app.callback(
        [Output('results-container', 'children'),
         Output('loading-output', 'children')],
        [Input('run-button', 'n_clicks')],
        [State('symbol-dropdown', 'value'),
         State('strategy-dropdown', 'value'),
         State('start-date', 'date'),
         State('end-date', 'date'),
         State('initial-capital', 'value')]
    )
    def run_backtest(n_clicks, symbol, strategy_type, start_date, end_date, initial_capital):
        """Run backtest and update results"""
        
        if n_clicks is None:
            return no_update, ""
        
        try:
            # Create strategy based on selection
            if strategy_type == 'sma_20_50':
                strategy = SMAStrategy(short_window=20, long_window=50)
            elif strategy_type == 'sma_50_200':
                strategy = SMAStrategy(short_window=50, long_window=200)
            elif strategy_type == 'ema_12_26':
                strategy = EMAStrategy(short_window=12, long_window=26)
            elif strategy_type == 'rsi_14':
                strategy = RSIStrategy(window=14)
            else:
                strategy = SMAStrategy(short_window=20, long_window=50)
            
            # Run backtest
            engine = BacktestEngine(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                initial_capital=initial_capital
            )
            
            results = engine.run(strategy)
            
            # Create charts
            portfolio_chart = create_portfolio_chart(results)
            signals_chart = create_signals_chart(results, strategy_type)
            
            # Create results layout
            layout = create_results_layout(results)
            
            # Update charts in layout
            for component in layout.children:
                if hasattr(component, 'children'):
                    for row in component.children:
                        if hasattr(row, 'children'):
                            for col in row.children:
                                if hasattr(col, 'children') and hasattr(col.children, 'children'):
                                    card_body = col.children.children
                                    if hasattr(card_body, 'children'):
                                        for item in card_body.children:
                                            if hasattr(item, 'id'):
                                                if item.id == 'portfolio-chart':
                                                    item.figure = portfolio_chart
                                                elif item.id == 'signals-chart':
                                                    item.figure = signals_chart
            
            return layout, ""
        
        except Exception as e:
            error_msg = f"Error running backtest: {str(e)}"
            return error_msg, ""


def create_portfolio_chart(results):
    """Create portfolio value chart"""
    
    df = results['data']
    
    fig = go.Figure()
    
    # Portfolio value line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['portfolio_value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='blue', width=2)
    ))
    
    # Buy and hold comparison
    initial_shares = results['initial_capital'] / df['close'].iloc[0]
    buy_hold_value = initial_shares * df['close']
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=buy_hold_value,
        mode='lines',
        name='Buy & Hold',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f"Portfolio Performance - {results['strategy']}",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def create_signals_chart(results, strategy_type):
    """Create price and signals chart"""
    
    df = results['data']
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='black', width=2)
    ))
    
    # Add strategy-specific indicators
    if strategy_type.startswith('sma'):
        if 'sma_short' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['sma_short'],
                mode='lines',
                name='Short SMA',
                line=dict(color='blue', width=1)
            ))
        if 'sma_long' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['sma_long'],
                mode='lines',
                name='Long SMA',
                line=dict(color='red', width=1)
            ))
    
    elif strategy_type.startswith('ema'):
        if 'ema_short' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['ema_short'],
                mode='lines',
                name='Short EMA',
                line=dict(color='blue', width=1)
            ))
        if 'ema_long' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['ema_long'],
                mode='lines',
                name='Long EMA',
                line=dict(color='red', width=1)
            ))
    
    # Buy signals
    buy_signals = df[df['position'] > 0]
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(
            x=buy_signals.index,
            y=buy_signals['close'],
            mode='markers',
            name='Buy Signal',
            marker=dict(color='green', size=10, symbol='triangle-up')
        ))
    
    # Sell signals
    sell_signals = df[df['position'] < 0]
    if not sell_signals.empty:
        fig.add_trace(go.Scatter(
            x=sell_signals.index,
            y=sell_signals['close'],
            mode='markers',
            name='Sell Signal',
            marker=dict(color='red', size=10, symbol='triangle-down')
        ))
    
    fig.update_layout(
        title=f"Price and Trading Signals - {results['symbol']}",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig
