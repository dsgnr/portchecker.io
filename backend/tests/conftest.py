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
PORTS = [80, 22, 8080, 443]
OPEN_PORTS = [80, 443]
CLOSED_PORTS = [22, 8080]
SOCKET_OPEN = 0
SOCKET_CLOSED = 1


@pytest.fixture
def client():
    """Fixture to provide a test client for app requests."""
    return TestClient(app)


def mock_connect(address_port_tuple: tuple[str, int]) -> int:
    """Simulate mixed open/closed ports based on port numbers."""
    return SOCKET_OPEN if address_port_tuple[1] in OPEN_PORTS else SOCKET_CLOSED


@pytest.fixture(autouse=True)
def mock_socket():
    """
    Simulate the socket connection.
    Uses the `mock_connect` method above to return the state value
    """
    with patch("socket.socket.connect_ex", side_effect=mock_connect):
        yield


@pytest.fixture
def mock_request_path():
    """Fixture to create a mock Request object with a specified path."""
    return Request(scope={"method": "GET", "path": "/test-path"})


@pytest.fixture
def mock_request():
    """Fixture to create a mock request with customizable headers."""

    class MockRequest:  # pylint: disable=too-few-public-methods
        """The MockRequest class"""

        def __init__(self, headers):
            self.headers = headers

    return MockRequest
