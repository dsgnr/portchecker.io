"""Tests for schemas"""
import pytest
from pydantic import ValidationError

from api.app.schemas.api import (
    APICheckSchema,
    APIErrorResponseSchema,
    APIResponseSchema,
    APISchema,
)

# Dummy values for annotations
HOST = "example.com"
PORT = 443


def test_apischema_valid():
    """Test that APISchema validates and parses correct input data."""
    data = {"host": HOST, "ports": [PORT, 80]}
    schema = APISchema(**data)
    assert schema.host == HOST
    assert schema.ports == [PORT, 80]


def test_apischema_missing_host():
    """Test that APISchema raises ValidationError if 'host' is missing."""
    data = {"ports": [PORT]}
    with pytest.raises(ValidationError):
        APISchema(**data)


def test_apicheckschema_valid():
    """Test that APICheckSchema validates and parses correct input data."""
    data = {"port": PORT, "status": True}
    schema = APICheckSchema(**data)
    assert schema.port == PORT
    assert schema.status is True


def test_apiresponseschema_valid():
    """Test that APIResponseSchema validates and parses correct input data."""
    check = {"port": PORT, "status": True}
    data = {
        "error": False,
        "msg": "OK",
        "check": [check],
        "host": HOST,
    }
    schema = APIResponseSchema(**data)
    assert schema.error is False
    assert schema.msg == "OK"
    assert schema.host == HOST
    assert schema.check[0].port == PORT


def test_apierrorresponseschema_valid():
    """Test that APIErrorResponseSchema validates and parses correct input data."""
    data = {
        "error": True,
        "detail": "fail",
        "extra": [{"param": "host", "error": "invalid"}],
    }
    schema = APIErrorResponseSchema(**data)
    assert schema.error is True
    assert schema.detail == "fail"
    assert schema.extra[0]["param"] == "host"


def test_apierrorresponseschema_missing_fields():
    """Test that APIErrorResponseSchema raises ValidationError if required fields are missing."""
    data = {"error": True}
    with pytest.raises(ValidationError):
        APIErrorResponseSchema(**data)
