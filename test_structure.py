"""
Simple test to verify application structure
"""

import sys
import os


def test_imports():
    """Test that all modules can be imported"""
    
    print("=" * 60)
    print("Testing Project Structure")
    print("=" * 60)
    
    tests = []
    
    # Test backtesting module
    print("\n1. Testing backtesting module...")
    try:
        from backtesting import data_fetcher, engine, strategies
        print("   ✓ backtesting.data_fetcher")
        print("   ✓ backtesting.engine")
        print("   ✓ backtesting.strategies")
        tests.append(("Backtesting module", True))
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        tests.append(("Backtesting module", False))
    
    # Test dashboard module
    print("\n2. Testing dashboard module...")
    try:
        from dashboard import layout, callbacks
        print("   ✓ dashboard.layout")
        print("   ✓ dashboard.callbacks")
        tests.append(("Dashboard module", True))
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        tests.append(("Dashboard module", False))
    
    # Test utils module
    print("\n3. Testing utils module...")
    try:
        from utils import metrics
        print("   ✓ utils.metrics")
        tests.append(("Utils module", True))
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        tests.append(("Utils module", False))
    
    # Test main app
    print("\n4. Testing main app...")
    try:
        import app
        print("   ✓ app.py")
        tests.append(("Main app", True))
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        tests.append(("Main app", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


def test_file_structure():
    """Test that all expected files exist"""
    
    print("\n" + "=" * 60)
    print("Testing File Structure")
    print("=" * 60)
    
    expected_files = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        'app.py',
        'example.py',
        'test_sample.py',
        'backtesting/__init__.py',
        'backtesting/data_fetcher.py',
        'backtesting/engine.py',
        'backtesting/strategies.py',
        'dashboard/__init__.py',
        'dashboard/layout.py',
        'dashboard/callbacks.py',
        'utils/__init__.py',
        'utils/metrics.py',
    ]
    
    all_exist = True
    
    for filepath in expected_files:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} (missing)")
            all_exist = False
    
    if all_exist:
        print(f"\n✓ All {len(expected_files)} expected files exist!")
        return 0
    else:
        print("\n✗ Some files are missing")
        return 1


if __name__ == '__main__':
    result1 = test_file_structure()
    result2 = test_imports()
    
    sys.exit(max(result1, result2))
