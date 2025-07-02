"""Tests for query_address"""

import pytest

from api.app.helpers.query import (
    JsonAPIException,
    _check_port_status,
    check_ports,
    query_address,
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


@pytest.mark.parametrize(
    "host,ports,expected",
    [
        (
            VALID_PUBLIC_IPV4,
            [CLOSED_PORTS[0]],
            [{"port": CLOSED_PORTS[0], "status": False}],
        ),
        (
            VALID_PUBLIC_IPV4,
            OPEN_PORTS,
            [{"port": port, "status": True} for port in OPEN_PORTS],
        ),
        (
            VALID_PUBLIC_IPV4,
            CLOSED_PORTS,
            [{"port": port, "status": False} for port in CLOSED_PORTS],
        ),
        (VALID_PUBLIC_IPV4, [], []),
    ],
)
def test_query_address_various(host, ports, expected):
    """Test query_address for various valid scenarios."""
    assert query_address(host, ports) == expected


def test_query_address_multiple_ports_mixed_status():
    """Test when some ports are open and some are closed."""
    result = query_address(VALID_PUBLIC_IPV4, PORTS)
    expected = [
        {"port": port, "status": mock_connect((VALID_PUBLIC_IPV4, port)) == SOCKET_OPEN}
        for port in PORTS
    ]
    assert result == expected


def test_query_address_invalid_hostname(mocker):
    """Test query_address raises JsonAPIException for an invalid hostname (mocked DNS failure)."""
    mocker.patch(
        "socket.gethostbyname",
        side_effect=OSError("Hostname does not appear to resolve"),
    )
    with pytest.raises(JsonAPIException, match=".*Hostname does not appear to resolve"):
        query_address(INVALID_HOST, [OPEN_PORTS[0]])


def test_query_address_empty_host():
    """Test query_address raises JsonAPIException for empty host."""
    with pytest.raises(JsonAPIException, match="A hostname must be provided"):
        query_address("", [80])


def test_query_address_none_host():
    """Test query_address raises JsonAPIException for None as host."""
    with pytest.raises(JsonAPIException):
        query_address(None, [80])


def test_query_address_invalid_port_type():
    """Test query_address raises TypeError for non-integer port."""
    with pytest.raises(Exception):
        query_address(VALID_PUBLIC_IPV4, ["notaport"])


def test_query_address_ipv6():
    """Test query_address raises JsonAPIException for IPv6 address."""
    with pytest.raises(JsonAPIException, match="IPv6 is not currently supported"):
        query_address("2001:4860:4860::8888", [80])


def test_query_address_duplicate_ports():
    """Test query_address handles duplicate ports gracefully."""
    ports = [80, 80, 443]
    result = query_address(VALID_PUBLIC_IPV4, ports)
    assert result.count({"port": 80, "status": True}) == 2
    assert {"port": 443, "status": True} in result


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
