"""Tests for query_ipv4"""

import pytest

from api.app.helpers.query import (
    JsonAPIException,
    _check_port_status,
    check_ports,
    query_ipv4,
)

from .conftest import (
    CLOSED_PORTS,
    INVALID_HOST,
    OPEN_PORTS,
    PORTS,
    SOCKET_OPEN,
    VALID_PUBLIC_IPV4,
    mock_connect,
)


def test_query_ipv4_single_closed_port():
    """Mock socket connection to return non-zero, indicating the port is closed"""
    result = query_ipv4(VALID_PUBLIC_IPV4, [CLOSED_PORTS[0]])
    assert result == [{"port": CLOSED_PORTS[0], "status": False}]


def test_query_ipv4_multiple_ports_mixed_status():
    """Test when some ports are open and some are closed."""
    result = query_ipv4(VALID_PUBLIC_IPV4, PORTS)
    expected = [
        {
            "port": port,
            "status": mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN,
        }
        for port in PORTS
    ]
    assert result == expected


def test_query_ipv4_empty_ports_list():
    """Test query_ipv4 returns empty list when ports list is empty."""
    ports = expected_result = []
    assert query_ipv4(VALID_PUBLIC_IPV4, ports) == expected_result


def test_query_ipv4_invalid_address():
    """Test query_ipv4 raises JsonAPIException for an invalid hostname."""
    with pytest.raises(JsonAPIException, match=".*Hostname does not appear to resolve"):
        query_ipv4(INVALID_HOST, [OPEN_PORTS[0]])


def test_check_ports_all_open():
    """Test when all ports are open."""
    result = check_ports(VALID_PUBLIC_IPV4, OPEN_PORTS)
    expected = [{"port": port, "status": True} for port in OPEN_PORTS]
    assert result == expected


def test_check_ports_all_closed():
    """Test when all ports are closed."""
    result = check_ports(VALID_PUBLIC_IPV4, CLOSED_PORTS)
    expected = [{"port": port, "status": False} for port in CLOSED_PORTS]
    assert result == expected


def test_check_ports_mixed():
    """Test when some ports are open and some are closed."""
    result = check_ports(VALID_PUBLIC_IPV4, PORTS)
    expected = [
        {
            "port": port,
            "status": mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN,
        }
        for port in PORTS
    ]
    assert result == expected


def test_check_port_status_open():
    """Test _check_port_status with an open port."""
    result = _check_port_status(VALID_PUBLIC_IPV4, OPEN_PORTS[0])
    expected = {"port": OPEN_PORTS[0], "status": True}
    assert result == expected


def test_check_port_status_closed():
    """Test _check_port_status with a closed port."""
    result = _check_port_status(VALID_PUBLIC_IPV4, CLOSED_PORTS[0])
    expected = {"port": CLOSED_PORTS[0], "status": False}
    assert result == expected
