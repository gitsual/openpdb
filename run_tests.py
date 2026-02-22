#!/usr/bin/env python3
"""
Run all tests for OpenClaw Agent Generator.

Usage:
    python run_tests.py           # Run all unit tests
    python run_tests.py --full    # Include integration tests (requires Ollama)
    python run_tests.py --quick   # Only fast tests
"""

import sys
import argparse
import unittest
from pathlib import Path

def run_tests(include_integration=False, quick=False):
    """Run test suite."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Always include unit tests
    from tests import test_generator
    suite.addTests(loader.loadTestsFromModule(test_generator))
    
    # Include integration tests if requested
    if include_integration and not quick:
        from tests import test_integration
        suite.addTests(loader.loadTestsFromModule(test_integration))
    
    # Run
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 60)
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
        for test, trace in result.failures + result.errors:
            print(f"\n  ❌ {test}")
    
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('--full', action='store_true', 
                        help='Include integration tests (requires Ollama)')
    parser.add_argument('--quick', action='store_true',
                        help='Only fast unit tests')
    args = parser.parse_args()
    
    success = run_tests(
        include_integration=args.full,
        quick=args.quick
    )
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
