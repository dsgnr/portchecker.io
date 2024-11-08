"""Tests for get_requester"""
import pytest

from api.app.helpers.query import get_requester


def test_get_requester_with_cf_connecting_ip(mock_request):
    """Test get_requester with 'cf-connecting-ip' header."""
    request = mock_request({"cf-connecting-ip": "192.168.1.1"})
    assert get_requester(request) == "192.168.1.1"


def test_get_requester_with_do_connecting_ip(mock_request):
    """Test get_requester with 'do-connecting-ip' header."""
    request = mock_request({"do-connecting-ip": "192.168.1.2"})
    assert get_requester(request) == "192.168.1.2"


def test_get_requester_with_x_real_ip(mock_request):
    """Test get_requester with 'x-real-ip' header."""
    request = mock_request({"x-real-ip": "192.168.1.3"})
    assert get_requester(request) == "192.168.1.3"


def test_get_requester_prioritizes_known_headers(mock_request):
    """Test get_requester prioritizes 'cf-connecting-ip' over other headers."""
    request = mock_request(
        {
            "cf-connecting-ip": "192.168.1.1",
            "do-connecting-ip": "192.168.1.2",
            "x-real-ip": "192.168.1.3",
        }
    )
    assert get_requester(request) == "192.168.1.1"  # should prioritize cf-connecting-ip


def test_get_requester_no_known_headers(mock_request):
    """Test get_requester raises error when no known headers are present."""
    request = mock_request({"some-other-header": "192.168.1.4"})
    with pytest.raises(ValueError, match="The requester IP was not detected"):
        get_requester(request)


def test_get_requester_empty_headers(mock_request):
    """Test get_requester raises error when headers are empty."""
    request = mock_request({})
    with pytest.raises(ValueError, match="The requester IP was not detected"):
        get_requester(request)


def test_get_requester_case_insensitivity(mock_request):
    """Test get_requester handles case-insensitive header keys."""
    request = mock_request({"Cf-Connecting-Ip": "192.168.1.5"})
    assert get_requester(request) == "192.168.1.5"
