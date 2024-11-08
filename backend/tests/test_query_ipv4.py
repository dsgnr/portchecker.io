"""Tests for query_ipv4"""
import socket
from unittest.mock import MagicMock, patch

import pytest

from api.app.helpers.query import JsonAPIException, query_ipv4

from .conftest import INVALID_HOST, VALID_PUBLIC_IPV4


def test_query_ipv4_single_open_port(mock_socket):
    """Mock socket connection to return 0, indicating the port is open"""
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 0
    mock_socket.return_value = mock_sock_instance

    ports = [80]
    assert query_ipv4(VALID_PUBLIC_IPV4, ports) == [{"port": ports[0], "status": True}]


def test_query_ipv4_single_closed_port(mock_socket):
    """Mock socket connection to return non-zero, indicating the port is closed"""
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 1
    mock_socket.return_value = mock_sock_instance

    ports = [81]
    assert query_ipv4(VALID_PUBLIC_IPV4, ports) == [{"port": ports[0], "status": False}]


def test_query_ipv4_multiple_ports_mixed_status(mock_socket):
    """Simulate one open port and one closed port"""
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.side_effect = [
        0,
        1,
    ]  # Open for port 80, closed for port 443
    mock_socket.return_value = mock_sock_instance

    ports = [80, 443]
    assert query_ipv4(VALID_PUBLIC_IPV4, ports) == [
        {"port": ports[0], "status": True},
        {"port": ports[1], "status": False},
    ]

def test_query_ipv4_empty_ports_list():
    """Test query_ipv4 returns empty list when ports list is empty."""
    ports = expected_result = []
    assert query_ipv4(VALID_PUBLIC_IPV4, ports) == expected_result


def test_query_ipv4_invalid_address():
    """Test query_ipv4 raises JsonAPIException for an invalid hostname."""
    with (
        patch("socket.gethostbyname", side_effect=socket.gaierror),
        pytest.raises(JsonAPIException, match=".*Hostname does not appear to resolve"),
    ):
        query_ipv4(INVALID_HOST, [443])


def test_query_ipv4_valid_address(mock_socket):
    """Test query_ipv4 returns correct status for a valid IP and port."""
    mock_sock_instance = MagicMock()
    mock_sock_instance.connect_ex.return_value = 0
    mock_socket.return_value = mock_sock_instance
    assert query_ipv4(VALID_PUBLIC_IPV4, [443]) == [{"port": 443, "status": True}]
