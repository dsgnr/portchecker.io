"""Tests for resolve_hostname"""
import asyncio
import socket
from unittest.mock import patch

import pytest

from api.app.helpers.query import resolve_hostname

from .conftest import (
    INVALID_HOST,
    LOCALHOST_IPV4,
    VALID_DOMAIN,
    VALID_PUBLIC_IPV4,
    mock_getaddrinfo,
)


def test_resolve_hostname_valid():
    """Test that a valid hostname resolves to its IPv4 address."""
    with patch("socket.getaddrinfo", return_value=mock_getaddrinfo(VALID_PUBLIC_IPV4)):
        assert asyncio.run(resolve_hostname(VALID_DOMAIN)) == VALID_PUBLIC_IPV4


def test_resolve_hostname_valid_with_ip():
    """Test that a valid IP address resolves to itself."""
    with patch("socket.getaddrinfo", return_value=mock_getaddrinfo(VALID_PUBLIC_IPV4)):
        assert asyncio.run(resolve_hostname(VALID_PUBLIC_IPV4)) == VALID_PUBLIC_IPV4


def test_resolve_hostname_with_scheme():
    """Test that a hostname with a scheme (e.g., http://) raises a ValueError."""
    with pytest.raises(ValueError, match="The hostname must not have a scheme"):
        asyncio.run(resolve_hostname(f"http://{VALID_DOMAIN}"))


def test_resolve_hostname_invalid():
    """Test that an invalid hostname raises a ValueError."""
    with (
        patch("socket.getaddrinfo", side_effect=socket.gaierror),
        pytest.raises(ValueError, match="Hostname does not appear to resolve"),
    ):
        asyncio.run(resolve_hostname(INVALID_HOST))


def test_resolve_hostname_no_results():
    """Test that an empty resolver result raises a ValueError."""
    with (
        patch("socket.getaddrinfo", return_value=[]),
        pytest.raises(ValueError, match="Hostname does not appear to resolve"),
    ):
        asyncio.run(resolve_hostname(INVALID_HOST))


def test_resolve_hostname_empty():
    """Test that an empty hostname raises a ValueError."""
    with pytest.raises(ValueError, match="A hostname must be provided"):
        asyncio.run(resolve_hostname(""))


def test_resolve_hostname_localhost():
    """Test that the `localhost` hostname resolves."""
    with patch("socket.getaddrinfo", return_value=mock_getaddrinfo(LOCALHOST_IPV4)):
        assert asyncio.run(resolve_hostname("localhost")) == LOCALHOST_IPV4
