from litestar import MediaType
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from api.app.helpers.exceptions import JsonAPIException
from api.app.helpers.handlers import (
    json_api_exception_handler,
    text_value_error_exception_handler,
    validation_exception_handler,
)


# Test for validation_exception_handler
def test_validation_exception_handler(mock_request_path):
    # Create a ValidationException with sample details
    exc = ValidationException(detail="Invalid data provided", extra={"field": "value"})

    # Call the handler
    response = validation_exception_handler(mock_request_path, exc)

    # Assert response status and structure
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.media_type == MediaType.JSON
    assert response.content == {
        "error": True,
        "detail": "validation error: Invalid data provided",
        "extra": {"field": "value"},
    }


# Test for json_api_exception_handler
def test_json_api_exception_handler(mock_request_path):
    # Create a JsonAPIException with sample details
    exc = JsonAPIException(key="username", message="This field is required")

    # Call the handler
    response = json_api_exception_handler(mock_request_path, exc)

    # Assert response status and structure
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.media_type == MediaType.JSON
    assert response.content.error is True
    assert (
        response.content.detail
        == "validation error: Validation failed for GET /test-path"
    )
    assert response.content.extra == [
        {"key": "username", "message": "This field is required"}
    ]


# Test for text_value_error_exception_handler
def test_text_value_error_exception_handler(mock_request_path):
    # Create a ValueError with a sample message
    exc = ValueError("An unexpected value error occurred")

    # Call the handler
    response = text_value_error_exception_handler(mock_request_path, exc)

    # Assert response status and content type
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.media_type == MediaType.TEXT
    assert (
        response.content
        == "An error occurred for GET /test-path: An unexpected value error occurred"
    )
