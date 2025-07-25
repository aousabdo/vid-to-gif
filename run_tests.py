#!/usr/bin/env python3
"""
Test runner for vid-to-gif.
"""

import sys
import os
import unittest

# Add the tests directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

if __name__ == '__main__':
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    sys.exit(not result.wasSuccessful())