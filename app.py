"""
Main Dash application for stock backtesting
"""

from dash import Dash
import dash_bootstrap_components as dbc

from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks


# Initialize Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Set app title
app.title = "Stock Backtesting Dashboard"

# Create layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Expose Flask server for production deployment (gunicorn, etc.)
server = app.server

# Run the app
if __name__ == '__main__':
    print("Starting Stock Backtesting Dashboard...")
    print("Open your browser and navigate to http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
