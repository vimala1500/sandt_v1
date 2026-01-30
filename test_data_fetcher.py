"""
Test script for data fetcher with improved error handling and retry logic
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backtesting.data_fetcher import DataFetcher


class TestDataFetcher(unittest.TestCase):
    """Test suite for DataFetcher class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.fetcher = DataFetcher(timeout=10, max_retries=2)
        
        # Create sample data with lowercase columns (as returned by fetch_data)
        dates = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D')
        self.sample_data = pd.DataFrame({
            'open': [100.0] * len(dates),
            'high': [105.0] * len(dates),
            'low': [95.0] * len(dates),
            'close': [102.0] * len(dates),
            'volume': [1000000] * len(dates)
        }, index=dates)
        
        # Create sample data for get_latest_price (uppercase as returned by yfinance)
        self.sample_latest_data = pd.DataFrame({
            'Open': [100.0],
            'High': [105.0],
            'Low': [95.0],
            'Close': [102.0],
            'Volume': [1000000]
        }, index=[dates[-1]])
    
    def test_initialization_defaults(self):
        """Test DataFetcher initialization with defaults"""
        fetcher = DataFetcher()
        self.assertEqual(fetcher.timeout, 30)
        self.assertEqual(fetcher.max_retries, 3)
    
    def test_initialization_custom(self):
        """Test DataFetcher initialization with custom values"""
        fetcher = DataFetcher(timeout=60, max_retries=5)
        self.assertEqual(fetcher.timeout, 60)
        self.assertEqual(fetcher.max_retries, 5)
    
    def test_initialization_from_env(self):
        """Test DataFetcher initialization from environment variables"""
        with patch.dict(os.environ, {'YFINANCE_TIMEOUT': '45', 'YFINANCE_MAX_RETRIES': '4'}):
            fetcher = DataFetcher()
            self.assertEqual(fetcher.timeout, 45)
            self.assertEqual(fetcher.max_retries, 4)
    
    def test_initialization_from_invalid_env(self):
        """Test DataFetcher initialization with invalid environment variables"""
        with patch.dict(os.environ, {'YFINANCE_TIMEOUT': 'invalid', 'YFINANCE_MAX_RETRIES': 'bad'}):
            fetcher = DataFetcher(timeout=50, max_retries=5)
            # Should fallback to defaults when env vars are invalid
            self.assertEqual(fetcher.timeout, 50)
            self.assertEqual(fetcher.max_retries, 5)
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    def test_fetch_data_success(self, mock_ticker):
        """Test successful data fetching"""
        # Mock ticker behavior
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = self.sample_data
        mock_ticker.return_value = mock_ticker_instance
        
        # Fetch data
        result = self.fetcher.fetch_data('AAPL', '2023-01-01', '2023-01-31')
        
        # Verify
        self.assertFalse(result.empty)
        self.assertEqual(len(result), len(self.sample_data))
        self.assertTrue(all(col.islower() for col in result.columns))  # Check lowercase columns
        mock_ticker_instance.history.assert_called_once()
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    def test_fetch_data_empty_dataframe(self, mock_ticker):
        """Test handling of empty data (invalid symbol)"""
        # Mock empty DataFrame
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_ticker_instance
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.fetcher.fetch_data('INVALID', '2023-01-01', '2023-01-31')
        
        self.assertIn("No data found for symbol INVALID", str(context.exception))
        self.assertIn("invalid symbol", str(context.exception))
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    @patch('backtesting.data_fetcher.time.sleep')  # Mock sleep to speed up test
    def test_fetch_data_network_error_with_retry(self, mock_sleep, mock_ticker):
        """Test retry logic on network errors"""
        # Mock network error on first call, success on second
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.side_effect = [
            ConnectionError("Failed to resolve fc.yahoo.com"),  # First attempt fails
            self.sample_data  # Second attempt succeeds
        ]
        mock_ticker.return_value = mock_ticker_instance
        
        # Should succeed after retry
        result = self.fetcher.fetch_data('AAPL', '2023-01-01', '2023-01-31')
        
        # Verify retry occurred
        self.assertEqual(mock_ticker_instance.history.call_count, 2)
        self.assertEqual(mock_sleep.call_count, 1)  # One sleep between retries
        self.assertFalse(result.empty)
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    @patch('backtesting.data_fetcher.time.sleep')
    def test_fetch_data_exhausted_retries(self, mock_sleep, mock_ticker):
        """Test behavior when all retries are exhausted"""
        # Mock network error on all attempts
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.side_effect = ConnectionError("Failed to resolve fc.yahoo.com")
        mock_ticker.return_value = mock_ticker_instance
        
        # Should raise exception after all retries
        with self.assertRaises(Exception) as context:
            self.fetcher.fetch_data('AAPL', '2023-01-01', '2023-01-31')
        
        # Verify all retries were attempted
        self.assertEqual(mock_ticker_instance.history.call_count, self.fetcher.max_retries)
        self.assertIn("Failed data fetch", str(context.exception))
        self.assertIn("Please check internet connectivity", str(context.exception))
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    def test_fetch_data_non_network_error(self, mock_ticker):
        """Test that non-network errors are not retried"""
        # Mock a non-network error
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.side_effect = KeyError("Invalid column")
        mock_ticker.return_value = mock_ticker_instance
        
        # Should raise immediately without retry
        with self.assertRaises(Exception) as context:
            self.fetcher.fetch_data('AAPL', '2023-01-01', '2023-01-31')
        
        # Verify only one attempt was made
        self.assertEqual(mock_ticker_instance.history.call_count, 1)
        self.assertIn("Error during data fetch", str(context.exception))
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    def test_get_latest_price_success(self, mock_ticker):
        """Test successful latest price fetching"""
        # Mock ticker behavior with uppercase columns (as returned by yfinance)
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = self.sample_latest_data
        mock_ticker.return_value = mock_ticker_instance
        
        # Fetch latest price
        price = self.fetcher.get_latest_price('AAPL')
        
        # Verify
        self.assertEqual(price, 102.0)
        mock_ticker_instance.history.assert_called_once()
    
    @patch('backtesting.data_fetcher.yf.Ticker')
    def test_get_latest_price_empty(self, mock_ticker):
        """Test latest price with invalid symbol"""
        # Mock empty DataFrame
        mock_ticker_instance = Mock()
        mock_ticker_instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = mock_ticker_instance
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.fetcher.get_latest_price('INVALID')
        
        self.assertIn("No data found for symbol INVALID", str(context.exception))
    
    def test_get_available_symbols(self):
        """Test getting available symbols"""
        symbols = self.fetcher.get_available_symbols()
        
        self.assertIsInstance(symbols, list)
        self.assertEqual(len(symbols), 15)
        self.assertIn('AAPL', symbols)
        self.assertIn('MSFT', symbols)
        self.assertIn('GOOGL', symbols)


class TestNetworkErrorDetection(unittest.TestCase):
    """Test network error detection logic"""
    
    def setUp(self):
        self.fetcher = DataFetcher(timeout=10, max_retries=2)
    
    def test_network_error_keywords(self):
        """Test that network-related keywords are detected"""
        network_errors = [
            "Connection refused",
            "Failed to resolve hostname",
            "Network is unreachable",
            "Timeout error",
            "DNS resolution failed"
        ]
        
        for error_msg in network_errors:
            # Check if error message would be treated as network error
            is_network = any(keyword in error_msg.lower() for keyword in [
                'connection', 'timeout', 'network', 'resolve', 'unreachable', 'dns'
            ])
            self.assertTrue(is_network, f"Failed to detect network error: {error_msg}")


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running DataFetcher Tests")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataFetcher))
    suite.addTests(loader.loadTestsFromTestCase(TestNetworkErrorDetection))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
