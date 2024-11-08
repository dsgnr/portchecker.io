"""Fixtures for testing the application routes and helper functions"""
from unittest.mock import patch

import pytest
from litestar import Request
from litestar.testing import TestClient

from api.main import app

IPV4_VERSION = 4
HEADER_REAL_IP = "1.2.3.4"
VALID_PRIVATE_IPV4 = "192.168.1.1"
VALID_PUBLIC_IPV4 = "8.8.8.8"
VALID_DOMAIN = "example.com"
INVALID_HOST = "foo"
LOCALHOST_IPV4 = "127.0.0.1"

@pytest.fixture
def client():
    """Fixture to provide a test client for app requests."""
    return TestClient(app)


@pytest.fixture
def mock_request_path():
    """Fixture to create a mock Request object with a specified path."""
    return Request(scope={"method": "GET", "path": "/test-path"})


@pytest.fixture
def mock_socket():
    """Fixture to mock socket.socket calls."""
    with patch("socket.socket") as sock:
        yield sock


@pytest.fixture
def mock_request():
    """Fixture to create a mock request with customizable headers."""
    class MockRequest: # pylint: disable=too-few-public-methods
        """The MockRequest class"""
        def __init__(self, headers):
            self.headers = headers

    return MockRequest


@pytest.fixture
def mock_is_ip_address(mocker):
    """Fixture to mock the is_ip_address helper function."""
    return mocker.patch("app.helpers.query.is_ip_address")


@pytest.fixture
def mock_is_address_valid(mocker):
    """Fixture to mock the is_address_valid helper function."""
    return mocker.patch("app.helpers.query.is_address_valid")


@pytest.fixture
def mock_is_valid_hostname(mocker):
    """Fixture to mock the is_valid_hostname helper function."""
    return mocker.patch("app.helpers.query.is_valid_hostname")
