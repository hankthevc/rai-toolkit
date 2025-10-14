"""Pytest configuration for Playwright stress tests."""

import pytest
from playwright.sync_api import Page as SyncPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments."""
    return {
        **browser_type_launch_args,
        "headless": True,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
    }


@pytest.fixture
def page_url():
    """Base URL for the app - can be overridden via environment variable."""
    import os
    return os.getenv("STRESS_TEST_URL", "http://localhost:8501")

