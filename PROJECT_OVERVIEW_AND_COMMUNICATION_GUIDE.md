# Project Overview and Communication Guide

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Key Features](#key-features)
4. [High-Level Workflow](#high-level-workflow)
5. [Architecture Overview](#architecture-overview)
6. [Communication Guide for New Users and AI Assistants](#communication-guide-for-new-users-and-ai-assistants)
7. [Quick Reference](#quick-reference)

---

## Project Overview

### What is SandT v1?

**SandT v1 (Stock and Trading v1)** is a Python-based stock backtesting application with an interactive web dashboard. It enables users to:

- Test trading strategies against historical stock data
- Visualize strategy performance through an interactive Dash web interface
- Download and cache stock data for offline analysis
- Deploy the application to cloud platforms (Google Cloud Run)
- Analyze trading performance with key metrics (Sharpe ratio, max drawdown, win rate, etc.)

**Primary Use Cases:**
- **Strategy Development**: Test and refine trading strategies before live trading
- **Performance Analysis**: Evaluate historical performance of different trading approaches
- **Educational Tool**: Learn about algorithmic trading and backtesting concepts
- **Research**: Analyze stock price patterns and strategy effectiveness

**Target Audience:**
- Algorithmic traders and quantitative analysts
- Students learning about trading and finance
- Developers interested in financial applications
- Researchers studying market behavior

---

## Technologies Used

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary programming language | 3.8+ |
| **Dash** | Web application framework for interactive dashboards | 2.14.2 |
| **Plotly** | Interactive data visualization | 5.18.0 |
| **Pandas** | Data manipulation and analysis | 2.1.4 |
| **NumPy** | Numerical computing | 1.26.2 |
| **yfinance** | Yahoo Finance API wrapper for stock data | 0.2.33 |
| **Dash Bootstrap Components** | UI components and styling | 1.5.0 |
| **PyArrow** | Parquet file format support | 14.0.1 |
| **Gunicorn** | Production WSGI server | 22.0.0 |

### Deployment Technologies

- **Docker**: Containerization for consistent deployment
- **Google Cloud Run**: Serverless container platform
- **Cloud SQL** (optional): Managed database service

### Data Storage

- **Parquet format**: Efficient columnar storage for stock data
- **Local file system**: Cached data storage in `data/` directory

---

## Key Features

### 1. Stock Data Fetching
- **Yahoo Finance Integration**: Download historical stock data via yfinance API
- **Automatic Retry Logic**: Handles transient network failures gracefully
- **Configurable Timeouts**: Adjust request timeouts via environment variables
- **Multiple Symbols Support**: Download data for multiple stocks simultaneously

### 2. Data Caching System
- **Parquet Storage**: Store data in compressed, efficient parquet format
- **Offline Capability**: Run backtests without internet connectivity
- **Fast Loading**: 10-50x faster than CSV files
- **Space Efficient**: 60-80% smaller than equivalent CSV files
- **Type Preservation**: No parsing overhead, data types preserved

### 3. Backtesting Engine
- **Flexible Framework**: Support for multiple trading strategies
- **Historical Simulation**: Test strategies on past market data
- **Position Tracking**: Monitor trades and portfolio value over time
- **Configurable Parameters**: Customize initial capital, date ranges, etc.

### 4. Trading Strategies
Built-in strategies include:

- **SMA (Simple Moving Average)**: Crossover strategy using two moving averages
- **EMA (Exponential Moving Average)**: Similar to SMA but with exponential weighting
- **RSI (Relative Strength Index)**: Momentum-based overbought/oversold strategy

**Extensible Design**: Easy to create custom strategies by extending `BaseStrategy` class

### 5. Interactive Dashboard
- **Web-Based Interface**: Accessible via browser at `http://localhost:8050`
- **Parameter Selection**: Choose stocks, strategies, date ranges, and parameters
- **Real-Time Visualization**: Interactive charts with Plotly
- **Performance Metrics Display**: View key statistics and trade history
- **Responsive Design**: Bootstrap-based UI works on desktop and mobile

### 6. Performance Metrics
Comprehensive analysis including:

- **Total Return**: Overall percentage gain/loss
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Number of Trades**: Total trade count
- **Volatility**: Portfolio risk measurement

### 7. Cloud Deployment
- **Docker Support**: Containerized application for consistent deployment
- **Google Cloud Run Ready**: Pre-configured for serverless deployment
- **Environment Variable Configuration**: Customize behavior without code changes
- **Production WSGI Server**: Gunicorn for robust production serving

---

## High-Level Workflow

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│  (Symbol, Date Range, Strategy, Parameters)                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA ACQUISITION                              │
│  ┌──────────────────┐              ┌────────────────────┐       │
│  │  Yahoo Finance   │◄────OR──────►│  Cached Parquet    │       │
│  │  API (yfinance)  │              │  Files (local)     │       │
│  └──────────────────┘              └────────────────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  BACKTESTING ENGINE                             │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  1. Load historical price data (OHLCV)               │       │
│  │  2. Apply selected trading strategy                  │       │
│  │  3. Generate buy/sell signals                        │       │
│  │  4. Simulate trades and portfolio changes            │       │
│  │  5. Calculate performance metrics                    │       │
│  └──────────────────────────────────────────────────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RESULTS & VISUALIZATION                        │
│  ┌──────────────────┐              ┌────────────────────┐       │
│  │  Performance     │              │  Interactive       │       │
│  │  Metrics Table   │              │  Charts (Plotly)   │       │
│  └──────────────────┘              └────────────────────┘       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │  Trade History & Portfolio Value Over Time           │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

### Typical Usage Workflow

#### Workflow 1: First-Time User (Online)

1. **Installation**
   - Clone repository
   - Create virtual environment
   - Install dependencies: `pip install -r requirements.txt`

2. **Run Dashboard**
   - Execute: `python app.py`
   - Open browser to `http://localhost:8050`

3. **Configure Backtest**
   - Select stock symbol (e.g., AAPL)
   - Choose strategy (e.g., SMA)
   - Set date range and strategy parameters
   - Click "Run Backtest"

4. **Analyze Results**
   - View performance metrics
   - Examine portfolio value chart
   - Review trade history
   - Compare with buy-and-hold baseline

#### Workflow 2: Offline Development

1. **Download Data Once**
   ```bash
   python download_data.py --symbols AAPL MSFT GOOGL --start 2022-01-01 --end 2023-12-31
   ```

2. **Use Cached Data**
   ```python
   from backtesting.engine import BacktestEngine
   from backtesting.strategies import SMAStrategy
   
   engine = BacktestEngine(
       symbol='AAPL',
       start_date='2022-01-01',
       end_date='2023-12-31',
       initial_capital=10000,
       use_cache=True  # Use local parquet files
   )
   
   strategy = SMAStrategy(short_window=20, long_window=50)
   results = engine.run(strategy)
   ```

3. **Iterate on Strategies**
   - Modify strategy parameters
   - Test different indicators
   - No internet required after initial download

#### Workflow 3: Cloud Deployment

1. **Prepare Docker Image**
   - Application includes Dockerfile
   - Build: `docker build -t sandt-v1 .`
   - Test locally: `docker run -p 8080:8080 sandt-v1`

2. **Deploy to Google Cloud Run**
   - Follow `DEPLOY_TO_GCP.md` guide
   - Configure environment variables
   - Deploy containerized application
   - Access via public URL

3. **Production Usage**
   - Users access via web browser
   - No local installation required
   - Serverless scaling handles traffic

---

## Architecture Overview

### Directory Structure

```
sandt_v1/
│
├── app.py                          # Main Dash application entry point
│
├── backtesting/                    # Core backtesting logic
│   ├── __init__.py
│   ├── engine.py                   # BacktestEngine class - runs strategies
│   ├── strategies.py               # Trading strategy implementations
│   └── data_fetcher.py             # Data retrieval (yfinance + cache)
│
├── dashboard/                      # Web interface components
│   ├── __init__.py
│   ├── layout.py                   # UI layout definition (HTML/Dash)
│   └── callbacks.py                # Event handlers (button clicks, etc.)
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── metrics.py                  # Performance calculation functions
│
├── data/                           # Cached stock data (parquet files)
│   └── [Generated at runtime]
│
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container definition
├── .env.example                    # Environment variable template
├── download_data.py                # Data download script
├── example.py                      # Online backtest example
├── example_offline.py              # Offline backtest example
│
├── test_*.py                       # Test files
│
└── Documentation files:
    ├── README.md
    ├── DEPLOY_TO_GCP.md
    ├── DATA_CACHING_GUIDE.md
    └── PROJECT_OVERVIEW_AND_COMMUNICATION_GUIDE.md (this file)
```

### Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                           app.py                                │
│  (Dash application initialization & server configuration)       │
└───────┬─────────────────────────────────────────────────────────┘
        │
        ├──────────────────┬────────────────────┐
        │                  │                    │
        ▼                  ▼                    ▼
┌─────────────┐   ┌─────────────┐    ┌──────────────────┐
│  dashboard/ │   │ backtesting/│    │     utils/       │
│   layout    │   │   engine    │    │    metrics       │
│  callbacks  │   │  strategies │    └──────────────────┘
└─────────────┘   │data_fetcher │
        │         └─────────────┘
        │                │
        └────────────────┴───────► Orchestrates backtesting
                                   and displays results
```

### Key Classes and Modules

1. **BacktestEngine** (`backtesting/engine.py`)
   - Manages data loading (from yfinance or cache)
   - Executes trading strategy logic
   - Tracks portfolio positions and value
   - Calculates performance metrics

2. **Strategy Classes** (`backtesting/strategies.py`)
   - `BaseStrategy`: Abstract base class
   - `SMAStrategy`: Simple Moving Average implementation
   - `EMAStrategy`: Exponential Moving Average implementation
   - `RSIStrategy`: Relative Strength Index implementation

3. **DataFetcher** (`backtesting/data_fetcher.py`)
   - Handles yfinance API calls
   - Implements retry logic
   - Manages parquet file caching
   - Provides offline data access

4. **Dashboard Layout** (`dashboard/layout.py`)
   - Defines UI structure using Dash components
   - Creates input controls (dropdowns, date pickers)
   - Defines chart placeholders

5. **Dashboard Callbacks** (`dashboard/callbacks.py`)
   - Handles user interactions
   - Triggers backtest execution
   - Updates charts and metrics displays

---

## Communication Guide for New Users and AI Assistants

This section provides structured prompts and questions to ensure effective communication when working with this project, whether you're a new user or an AI assistant helping with development, deployment, or troubleshooting.

### Section 1: Understanding Requirements

When starting a new task or feature request, use these prompts to clarify requirements:

#### For Feature Requests
1. **"What specific feature or functionality would you like to add to the backtesting system?"**
   - Examples: New strategy type, additional metric, UI enhancement

2. **"What problem does this feature solve for users?"**
   - Helps understand the motivation and ensure alignment with project goals

3. **"Do you have a specific implementation approach in mind, or would you like recommendations?"**
   - Clarifies whether to proceed with user's design or suggest alternatives

4. **"Are there existing systems or libraries you'd like this to integrate with?"**
   - Identifies dependencies and compatibility requirements

5. **"What data or inputs will this feature require?"**
   - Ensures necessary data sources are available

6. **"Should this feature work with cached data, live data, or both?"**
   - Important for offline capability planning

#### For Bug Reports
1. **"Can you describe the exact steps to reproduce the issue?"**
   - Step-by-step reproduction is critical for debugging

2. **"What error messages or unexpected behavior did you observe?"**
   - Helps identify the root cause

3. **"Which environment are you using? (Local development, Docker, Cloud Run, etc.)"**
   - Environment-specific issues are common

4. **"What stock symbol, date range, and strategy were you testing?"**
   - Context helps isolate data-related issues

5. **"Is this a new issue, or has it worked before?"**
   - Identifies potential regressions

6. **"Are you connected to the internet, or using cached data?"**
   - Network issues are a common source of problems

### Section 2: Deployment Questions

When deploying or configuring the application, ask these questions:

#### For Local Development
1. **"What operating system are you using? (Windows, macOS, Linux)"**
   - Setup instructions may vary by OS

2. **"Do you have Python 3.8 or higher installed? Can you run `python --version`?"**
   - Verifies prerequisite

3. **"Do you have internet access to download stock data from Yahoo Finance?"**
   - Determines if offline setup is needed

4. **"Would you like to set up a virtual environment? (Recommended)"**
   - Best practice for Python development

5. **"Do you plan to modify the code, or just run the application?"**
   - Affects setup recommendations

#### For Docker Deployment
1. **"Do you have Docker installed? Can you run `docker --version`?"**
   - Verifies prerequisite

2. **"Are you deploying locally with Docker, or to a cloud platform?"**
   - Different considerations for each

3. **"What port would you like the application to run on? (Default: 8080)"**
   - Configuration option

4. **"Do you need to persist data between container restarts?"**
   - Determines volume mounting strategy

#### For Google Cloud Run Deployment
1. **"Do you have a Google Cloud Platform account with billing enabled?"**
   - Required for Cloud Run

2. **"Have you installed the Google Cloud SDK (`gcloud`)?"**
   - Necessary for deployment

3. **"Do you want the service to be publicly accessible or private?"**
   - Security and access control decision

4. **"What region do you prefer for deployment? (e.g., us-central1, us-east1)"**
   - Affects latency and pricing

5. **"Do you need to configure environment variables (e.g., API keys, timeouts)?"**
   - Customization options

6. **"Will the application need to fetch live data, or will you pre-download and cache it?"**
   - Cloud Run egress costs consideration

7. **"Do you need Cloud SQL database integration?"**
   - Optional advanced feature

### Section 3: Code Modification Requests

When making code changes, clarify these details:

#### For New Trading Strategies
1. **"What is the strategy logic? (e.g., buy when X crosses Y, sell when Z)"**
   - Core algorithm definition

2. **"What indicators or technical analysis tools does it require?"**
   - Determines additional dependencies

3. **"What parameters should be configurable by users?"**
   - UI and flexibility considerations

4. **"Should this strategy be added to the dashboard dropdown?"**
   - Integration with UI

5. **"Do you have test data or expected results to validate the strategy?"**
   - Quality assurance

#### For Performance Improvements
1. **"Which operation is slow? (data loading, strategy calculation, visualization)"**
   - Identifies optimization target

2. **"What is the current performance and what is your target?"**
   - Sets expectations

3. **"Are you willing to add dependencies for better performance?"**
   - Trade-off consideration

4. **"Is this a one-time concern or ongoing production issue?"**
   - Determines urgency and approach

#### For UI Changes
1. **"Which part of the dashboard needs modification?"**
   - Specific component identification

2. **"Do you have a mockup or example of the desired layout?"**
   - Visual communication

3. **"Should the change work on mobile devices?"**
   - Responsive design consideration

4. **"Does this require new data or calculations?"**
   - Backend implications

### Section 4: Troubleshooting Prompts

When diagnosing issues, work through these systematically:

#### Data Fetching Issues
1. **"Can you access Yahoo Finance in your browser? Try visiting finance.yahoo.com"**
   - Verifies basic connectivity

2. **"What error message do you see? Please share the full traceback."**
   - Error details are essential

3. **"Have you configured environment variables like YFINANCE_TIMEOUT?"**
   - Check configuration

4. **"Can you try downloading data manually with the download_data.py script?"**
   - Isolates the issue

5. **"If using Cloud Run, is egress connectivity enabled?"**
   - Cloud-specific networking issue

6. **"Would you like to switch to offline mode using cached data?"**
   - Alternative solution

#### Performance Issues
1. **"How large is the date range you're testing?"**
   - Large datasets can cause slowness

2. **"How many data points are being processed?"**
   - Quantifies the load

3. **"Are you running multiple backtests simultaneously?"**
   - Resource contention

4. **"Is the data being fetched from the internet or loaded from cache?"**
   - Cache is much faster

5. **"What are your system specs? (RAM, CPU)"**
   - Hardware limitations

#### Dashboard Issues
1. **"What browser are you using? (Chrome, Firefox, Safari, etc.)"**
   - Browser compatibility

2. **"Does the page load but the charts don't appear?"**
   - JavaScript or callback issue

3. **"Do you see any error messages in the browser console?"**
   - Client-side debugging

4. **"What port is the application running on?"**
   - Connection verification

5. **"Can you access http://localhost:8050 (or your configured port)?"**
   - Basic connectivity check

### Section 5: Update and Maintenance Questions

When updating or maintaining the project:

#### For Dependency Updates
1. **"Which package needs updating and why?"**
   - Specific package identification

2. **"Is this a security update or feature enhancement?"**
   - Determines urgency

3. **"Have you checked for breaking changes in the new version?"**
   - Compatibility verification

4. **"Should we update all dependencies or just specific ones?"**
   - Scope of update

5. **"Do you want to test locally before updating requirements.txt?"**
   - Safe update process

#### For Data Management
1. **"How much cached data do you have in the data/ directory?"**
   - Storage management

2. **"Do you want to refresh cached data for specific symbols?"**
   - Data currency

3. **"Should old cached data be automatically cleaned up?"**
   - Maintenance automation

4. **"What date ranges do you commonly use for backtesting?"**
   - Determines useful cache strategy

### Section 6: AI Assistant Specific Guidelines

When an AI assistant is helping with this project, it should:

#### Initial Assessment
1. **Ask: "What is the goal of your task? (Development, deployment, debugging, feature addition, etc.)"**
   - Determines the type of assistance needed

2. **Ask: "Are you working in a local environment, Docker, or cloud deployment?"**
   - Context for providing relevant guidance

3. **Ask: "Have you already set up the project, or is this the first time?"**
   - Determines starting point

#### Code Changes
1. **Clarify: "Should I make minimal changes to existing code or refactor for better design?"**
   - Scope management

2. **Verify: "Do you want me to add tests for the new functionality?"**
   - Quality assurance

3. **Ask: "Should the changes be backward compatible with existing saved data/configurations?"**
   - Migration considerations

4. **Confirm: "Would you like me to update relevant documentation files?"**
   - Documentation maintenance

#### Before Making Changes
1. **State: "Based on my analysis, here's what I understand needs to be done: [summary]. Is this correct?"**
   - Verification step

2. **Explain: "I'll be modifying these files: [list]. The changes will affect: [impact]."**
   - Transparency

3. **Warn: "This change may require: [dependencies, migrations, etc.]"**
   - Risk communication

#### After Making Changes
1. **Summarize: "I've completed these changes: [list]"**
   - Change summary

2. **Provide: "To test these changes, run: [commands]"**
   - Testing instructions

3. **Recommend: "Next steps: [suggestions for testing, deployment, etc.]"**
   - Guidance

---

## Quick Reference

### Essential Commands

```bash
# Local Development
python app.py                        # Start dashboard locally
python download_data.py --help       # See data download options
python test_sample.py                # Run tests

# Data Management
python download_data.py --symbols AAPL MSFT --start 2022-01-01 --end 2023-12-31
python download_data.py --list       # List cached data

# Docker
docker build -t sandt-v1 .           # Build image
docker run -p 8080:8080 sandt-v1     # Run container

# Cloud Deployment (see DEPLOY_TO_GCP.md for details)
gcloud run deploy sandt-v1 --source .
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `YFINANCE_TIMEOUT` | 30 | Request timeout in seconds |
| `YFINANCE_MAX_RETRIES` | 3 | Maximum retry attempts |
| `PORT` | 8050 (local), 8080 (cloud) | Application port |
| `DASH_DEBUG` | True (local), False (production) | Debug mode |

### Common File Locations

| Path | Description |
|------|-------------|
| `/data/` | Cached stock data (parquet files) |
| `/backtesting/` | Core backtesting engine and strategies |
| `/dashboard/` | Web UI components |
| `/utils/` | Helper functions |
| `requirements.txt` | Python dependencies |
| `.env` | Local environment variables (create from .env.example) |

### Key Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project introduction and basic usage |
| `DEPLOY_TO_GCP.md` | Complete Google Cloud Run deployment guide |
| `DATA_CACHING_GUIDE.md` | Data downloading and offline usage |
| `PROJECT_OVERVIEW_AND_COMMUNICATION_GUIDE.md` | This file - comprehensive overview and communication guide |

### Getting Help

1. **Documentation**: Start with README.md and relevant guides
2. **Code Examples**: Check `example.py` and `example_offline.py`
3. **Tests**: Review test files to understand expected behavior
4. **Issues**: Check repository issues for known problems
5. **AI Assistance**: Use the communication prompts in this guide for effective interaction

---

## Conclusion

This guide serves as a comprehensive reference for understanding the SandT v1 project and communicating effectively about it. Whether you're a new user setting up the project, an AI assistant helping with development, or a team member troubleshooting issues, following these structured prompts will ensure clear communication and efficient problem-solving.

**Remember**: The key to effective collaboration on this project is clear communication about:
- **Environment** (local, Docker, cloud)
- **Data source** (online/Yahoo Finance vs. offline/cached)
- **Objective** (development, deployment, troubleshooting)
- **Constraints** (internet access, resources, timeline)

Always start by understanding the context before diving into implementation!
