"""
Dashboard layout for the stock backtesting application
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_layout():
    """Create the main dashboard layout"""
    
    layout = dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Stock Backtesting Dashboard", className="text-center mb-4 mt-4"),
                html.Hr()
            ])
        ]),
        
        # Controls Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("Backtest Parameters")),
                    dbc.CardBody([
                        # Stock Symbol
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Stock Symbol"),
                                dcc.Dropdown(
                                    id='symbol-dropdown',
                                    options=[
                                        {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                                        {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                                        {'label': 'Google (GOOGL)', 'value': 'GOOGL'},
                                        {'label': 'Amazon (AMZN)', 'value': 'AMZN'},
                                        {'label': 'Tesla (TSLA)', 'value': 'TSLA'},
                                        {'label': 'NVIDIA (NVDA)', 'value': 'NVDA'},
                                        {'label': 'Meta (META)', 'value': 'META'},
                                    ],
                                    value='AAPL',
                                    clearable=False
                                )
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Strategy"),
                                dcc.Dropdown(
                                    id='strategy-dropdown',
                                    options=[
                                        {'label': 'SMA (20/50)', 'value': 'sma_20_50'},
                                        {'label': 'SMA (50/200)', 'value': 'sma_50_200'},
                                        {'label': 'EMA (12/26)', 'value': 'ema_12_26'},
                                        {'label': 'RSI (14)', 'value': 'rsi_14'},
                                    ],
                                    value='sma_20_50',
                                    clearable=False
                                )
                            ], width=6)
                        ], className="mb-3"),
                        
                        # Date Range
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Start Date"),
                                dcc.DatePickerSingle(
                                    id='start-date',
                                    date='2022-01-01',
                                    display_format='YYYY-MM-DD'
                                )
                            ], width=4),
                            dbc.Col([
                                dbc.Label("End Date"),
                                dcc.DatePickerSingle(
                                    id='end-date',
                                    date='2023-12-31',
                                    display_format='YYYY-MM-DD'
                                )
                            ], width=4),
                            dbc.Col([
                                dbc.Label("Initial Capital ($)"),
                                dbc.Input(
                                    id='initial-capital',
                                    type='number',
                                    value=10000,
                                    min=1000,
                                    step=1000
                                )
                            ], width=4)
                        ], className="mb-3"),
                        
                        # Run Backtest Button
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    "Run Backtest",
                                    id='run-button',
                                    color='primary',
                                    size='lg',
                                    className='w-100'
                                )
                            ])
                        ])
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Loading Spinner
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=html.Div(id="loading-output")
                )
            ])
        ]),
        
        # Results Section
        dbc.Row([
            dbc.Col([
                html.Div(id='results-container')
            ])
        ])
    ], fluid=True)
    
    return layout


def create_results_layout(results):
    """Create the results display layout"""
    
    metrics = results['metrics']
    
    layout = html.Div([
        # Metrics Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Return", className="card-title"),
                        html.H3(f"{metrics['total_return']}%",
                               className="text-success" if metrics['total_return'] > 0 else "text-danger")
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Buy & Hold", className="card-title"),
                        html.H3(f"{metrics['buy_hold_return']}%",
                               className="text-success" if metrics['buy_hold_return'] > 0 else "text-danger")
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Sharpe Ratio", className="card-title"),
                        html.H3(f"{metrics['sharpe_ratio']}")
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Max Drawdown", className="card-title"),
                        html.H3(f"{metrics['max_drawdown']}%", className="text-danger")
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Num Trades", className="card-title"),
                        html.H3(f"{metrics['num_trades']}")
                    ])
                ])
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Win Rate", className="card-title"),
                        html.H3(f"{metrics['win_rate']}%")
                    ])
                ])
            ], width=2)
        ], className="mb-4"),
        
        # Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Portfolio Value Over Time")),
                    dbc.CardBody([
                        dcc.Graph(id='portfolio-chart')
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Price and Trading Signals")),
                    dbc.CardBody([
                        dcc.Graph(id='signals-chart')
                    ])
                ])
            ], width=12)
        ])
    ])
    
    return layout
