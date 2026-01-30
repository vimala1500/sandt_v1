# Stock Data Fetching Analysis and Diagnosis

## Executive Summary

The sandt_v1 application uses **yfinance library (v0.2.33)** to fetch historical stock data from Yahoo Finance API for backtesting. The "No data found for symbol MSFT" error in Google Cloud Run deployment is caused by **network connectivity issues** preventing the application from reaching Yahoo Finance servers.

## Current Implementation

### Data Fetching Library
- **Library**: `yfinance==0.2.33` (Yahoo Finance API wrapper)
- **Location**: `/backtesting/data_fetcher.py`
- **Key Methods**:
  - `fetch_data()`: Downloads historical OHLCV data
  - `get_latest_price()`: Retrieves current stock price
  - `get_available_symbols()`: Returns list of 15 popular tickers

### Network Requirements
- **Internet Connectivity**: ✅ REQUIRED
- **External Hosts**: 
  - `query1.finance.yahoo.com` (primary API endpoint)
  - `fc.yahoo.com` (finance cookie/session management)
  - `query2.finance.yahoo.com` (backup endpoint)
- **API Keys**: ❌ NOT REQUIRED (yfinance uses public Yahoo Finance API)
- **Rate Limiting**: Yes, Yahoo Finance has rate limits (not documented officially)

### Current Error Handling
```python
# In data_fetcher.py lines 29-42
try:
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    
    if data.empty:
        raise ValueError(f"No data found for symbol {symbol}")
    
    return data

except Exception as e:
    raise Exception(f"Error fetching data for {symbol}: {str(e)}")
```

**Limitations**:
- ❌ No retry logic for transient network failures
- ❌ No timeout configuration
- ❌ Generic error messages don't distinguish network vs. symbol issues
- ❌ No caching mechanism
- ❌ No logging for debugging

## Root Cause Analysis

### Why "No data found for symbol MSFT" in Cloud Run

1. **Network Resolution Failure**
   - yfinance cannot resolve `fc.yahoo.com` hostname
   - Error: `NameResolutionError: Failed to resolve 'fc.yahoo.com'`
   - Results in empty DataFrame → triggers "No data found" error

2. **Potential Cloud Run Issues**
   - VPC network restrictions preventing external API access
   - No egress (outbound) connectivity configured
   - DNS resolution issues in the container environment
   - Firewall rules blocking Yahoo Finance domains

3. **yfinance Library Limitations**
   - No built-in retry mechanism
   - Default timeout may be too short for Cloud Run cold starts
   - Relies on external network without fallback

## Test Results

```
Testing yfinance data fetching...
Failed to get ticker 'MSFT' reason: HTTPSConnectionPool(host='fc.yahoo.com', port=443): 
Max retries exceeded with url: / (Caused by NameResolutionError(...Failed to resolve 'fc.yahoo.com'))
MSFT: No timezone found, symbol may be delisted
Data shape: (0, 6)
Empty: True
```

## Configuration Needs

### Current Configuration
- **Dockerfile**: 
  - Gunicorn timeout: 300 seconds
  - No yfinance-specific configuration
- **Dependencies**: Standard `requests==2.31.0` library
- **Environment Variables**: None for data fetching

### Required for Cloud Run Deployment

1. **Network Access**
   - ✅ Egress (outbound) connectivity must be enabled
   - ✅ Allow HTTPS (443) to Yahoo Finance domains
   - Consider using Cloud Run with VPC connector if network restrictions exist

2. **Application Configuration**
   - Increase request timeouts for yfinance
   - Add retry logic with exponential backoff
   - Implement caching to reduce API calls
   - Add comprehensive logging

3. **Environment Variables** (Recommended)
   ```
   YFINANCE_TIMEOUT=30
   YFINANCE_MAX_RETRIES=3
   ENABLE_DATA_CACHE=true
   CACHE_EXPIRY_HOURS=24
   LOG_LEVEL=INFO
   ```

## Recommendations

### Immediate Fixes

1. **Improve Error Handling**
   - Add specific error messages for network failures
   - Distinguish between symbol not found vs. connection issues
   - Add logging to track failures

2. **Add Retry Logic**
   - Implement exponential backoff (3 retries with 2s, 4s, 8s delays)
   - Handle transient network failures gracefully

3. **Configure Timeouts**
   - Set explicit timeout values for yfinance requests
   - Prevent hanging requests in Cloud Run

4. **Update Deployment Documentation**
   - Document network requirements clearly
   - Add troubleshooting section for "No data found" errors
   - Include Cloud Run egress configuration steps

### Long-term Improvements

1. **Implement Caching**
   - Cache historical data locally (Redis or filesystem)
   - Reduce API calls and improve performance
   - Handle rate limiting better

2. **Add Alternative Data Sources**
   - Fallback to other providers (Alpha Vantage, Polygon.io)
   - Support CSV file uploads for offline testing
   - Implement mock data mode for testing

3. **Monitoring and Alerting**
   - Track data fetch success rates
   - Monitor API response times
   - Alert on repeated failures

## Cloud Run Deployment Checklist

- [ ] Verify egress connectivity is enabled
- [ ] Test DNS resolution from Cloud Run container
- [ ] Configure appropriate timeout values (>300s)
- [ ] Add retry logic to data fetcher
- [ ] Implement comprehensive logging
- [ ] Test with multiple symbols before deployment
- [ ] Monitor logs after deployment
- [ ] Set up health check endpoint

## References

- yfinance documentation: https://pypi.org/project/yfinance/
- Yahoo Finance API (unofficial): https://query1.finance.yahoo.com/
- Cloud Run networking: https://cloud.google.com/run/docs/configuring/vpc-egress
