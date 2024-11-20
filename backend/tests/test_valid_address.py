"""Tests for is_address_valid"""
import pytest

from api.app.helpers.query import is_address_valid

from .conftest import LOCALHOST_IPV4, VALID_PRIVATE_IPV4, VALID_PUBLIC_IPV4


def test_is_address_valid_public_ipv4():
    """Test is_address_valid returns True for a public IPv4 address."""
    assert is_address_valid(VALID_PUBLIC_IPV4) is True


def test_is_address_valid_private_ipv4_with_allow_private(monkeypatch):
    """Test is_address_valid allows private IPv4 if ALLOW_PRIVATE is set."""
    monkeypatch.setenv("ALLOW_PRIVATE", "True")
    assert is_address_valid(VALID_PRIVATE_IPV4) is True


def test_is_address_valid_private_ipv4_without_allow_private():
    """Test is_address_valid raises ValueError for private IPv4 without ALLOW_PRIVATE."""
    with pytest.raises(
        ValueError,
        match=f"IPv4 address '{VALID_PRIVATE_IPV4}' does not appear to be public",
    ):
        is_address_valid(VALID_PRIVATE_IPV4)


def test_is_address_ipv6():
    """Test is_address_valid raises ValueError for IPv6 address."""
    with pytest.raises(ValueError, match="IPv6 is not currently supported"):
        is_address_valid("2001:4860:4860::8888")


def test_is_address_valid_invalid_address():
    """Test is_address_valid raises ValueError for an invalid IP address."""
    with pytest.raises(
        ValueError,
        match=".*does not appear to be an IPv4 or IPv6 address",
    ):
        is_address_valid("invalid_address")


def test_is_address_valid_none():
    """Test is_address_valid raises ValueError if None is passed as address."""
    with pytest.raises(ValueError, match="An IPv4 address must be provided"):
        is_address_valid(None)


def test_is_address_valid_loopback_without_allow_private():
    """Test is_address_valid raises ValueError for loopback address without ALLOW_PRIVATE."""
    with pytest.raises(
        ValueError,
        match=f"IPv4 address '{LOCALHOST_IPV4}' does not appear to be public",
    ):
        is_address_valid(LOCALHOST_IPV4)
