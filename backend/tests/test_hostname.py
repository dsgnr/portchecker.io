import socket
from unittest.mock import patch

import pytest

from api.app.helpers.query import is_valid_hostname

from .conftest import INVALID_HOST, LOCALHOST_IPV4, VALID_DOMAIN, VALID_PUBLIC_IPV4


def test_is_valid_hostname_valid():
    # Test a valid hostname (e.g., google.com)
    with patch("socket.gethostbyname", return_value=VALID_PUBLIC_IPV4):
        assert is_valid_hostname(VALID_DOMAIN) is True


def test_is_valid_hostname_valid_with_ip():
    # Test an IP address (should return True)
    with patch("socket.gethostbyname", return_value=VALID_PUBLIC_IPV4):
        assert is_valid_hostname(VALID_PUBLIC_IPV4) is True


def test_is_valid_hostname_with_scheme():
    # Test hostname with a scheme (e.g., http://)
    with pytest.raises(ValueError, match="The hostname must not have a scheme"):
        is_valid_hostname(f"http://{VALID_DOMAIN}")


def test_is_valid_hostname_invalid():
    # Test an invalid hostname that cannot be resolved
    with (
        patch("socket.gethostbyname", side_effect=socket.gaierror),
        pytest.raises(ValueError, match="Hostname does not appear to resolve"),
    ):
        is_valid_hostname(INVALID_HOST)


def test_is_valid_hostname_empty():
    # Test an empty hostname
    with pytest.raises(ValueError, match="A hostname must be provided"):
        is_valid_hostname("")


def test_is_valid_hostname_localhost():
    # Test localhost hostname
    with patch("socket.gethostbyname", return_value=LOCALHOST_IPV4):
        assert is_valid_hostname("localhost") is True
