"""
pytest configuration and fixtures for YouTube Auto Uploader tests.
"""

import pytest
import logging
from pathlib import Path

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def sample_script():
    """Provide sample video script for tests."""
    return """
    In this video, we explore how to make money online.
    There are several proven methods that work well.
    You can use tools like freelancing platforms and affiliate marketing.
    Start with what interests you most.
    The journey to financial freedom begins with a single step.
    """


@pytest.fixture
def sample_title():
    """Provide sample video title for tests."""
    return "How to Make Money Online"


@pytest.fixture
def sample_topic():
    """Provide sample topic for tests."""
    return "money"


@pytest.fixture
def channel_stats():
    """Provide sample channel statistics."""
    return {
        "avg_views": 5000,
        "avg_engagement": 0.08,
        "avg_watch_time": 20,
        "views": 5000,
        "likes": 400,
        "comments": 50,
        "shares": 10,
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide temporary directory for output files."""
    return str(tmp_path)


def pytest_configure(config):
    """pytest hook for custom configuration."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "network: marks tests as requiring network (deselect with '-m \"not network\"')"
    )
