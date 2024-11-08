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


# Define a fixture to initialize the app with routes
@pytest.fixture
def client():
    return TestClient(app)


# Fixture for creating a mock Request object
@pytest.fixture
def mock_request_path():
    return Request(scope={"method": "GET", "path": "/test-path"})


@pytest.fixture
def mock_socket():
    with patch("socket.socket") as sock:
        yield sock


# Mock request headers
@pytest.fixture
def mock_request():
    class MockRequest:
        def __init__(self, headers):
            self.headers = headers

    return MockRequest


# Mocking the helper functions
@pytest.fixture
def mock_is_ip_address(mocker):
    return mocker.patch("app.helpers.query.is_ip_address")


@pytest.fixture
def mock_is_address_valid(mocker):
    return mocker.patch("app.helpers.query.is_address_valid")


@pytest.fixture
def mock_is_valid_hostname(mocker):
    return mocker.patch("app.helpers.query.is_valid_hostname")
