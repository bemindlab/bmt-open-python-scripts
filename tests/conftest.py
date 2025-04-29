"""
Configuration file for pytest.
This file contains fixtures and configuration that will be available to all test files.
"""

import os
import sys
import pytest

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

@pytest.fixture(scope="session")
def sample_fixture():
    """
    A sample fixture that can be used across test files.
    Returns a simple string that can be used in tests.
    """
    return "This is a sample fixture"


# Add more fixtures as needed 