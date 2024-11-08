"""
The exception handlers for the API
"""

from litestar import MediaType, Request, Response
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from app.helpers.exceptions import JsonAPIException
from app.schemas.api import APIErrorResponseSchema


def validation_exception_handler(
    request: Request, exc: ValidationException  # pylint:disable=unused-argument
) -> APIErrorResponseSchema:
    """
    Catches `ValidationException` instances, typically raised due to invalid
    input data, and responds with an `application/json` HTTP response with a 400 status code.
    The response includes an error flag, a detailed message indicating the validation issue,
    and any additional information about specific validation errors.

    Parameters:
        request (Request): The HTTP request that triggered the exception.
        exc (ValidationException): The `ValidationException` instance containing error details.

    Returns:
        APIErrorResponseSchema: A JSON response dictionary, structured according to the
        `APIErrorResponseSchema` model, with a 400 status code, including error details
        and additional information about validation errors.
    """
    return Response(
        media_type=MediaType.JSON,
        content={
            "error": True,
            "detail": f"validation error: {exc.detail}",
            "extra": exc.extra,
        },
        status_code=HTTP_400_BAD_REQUEST,
    )


def json_api_exception_handler(
    request: Request, exc: JsonAPIException
) -> APIErrorResponseSchema:
    """
    Catches `JsonAPIException` instances, extracts error details, and returns
    an `application/json` HTTP response with a 400 status code. The JSON response includes
    an error flag, details about the validation failure, and additional information
    about the specific validation issue encountered.

    Parameters:
        request (Request): The HTTP request that triggered the exception.
        exc (JsonAPIException): The `JsonAPIException` instance containing error details.

    Returns:
        APIErrorResponseSchema: A structured `application/json` response with error details,
        formatted as per the `APIErrorResponseSchema` model, with a 400 status code.
    """
    return Response(
        media_type=MediaType.JSON,
        content=APIErrorResponseSchema(
            error=True,
            detail=(
                "validation error: Validation failed for "
                f"{request.method} {request.url.path}"
            ),
            extra=[{"key": exc.key, "message": exc.message}],
        ),
        status_code=HTTP_400_BAD_REQUEST,
    )


def text_value_error_exception_handler(request: Request, exc: ValueError) -> Response:
    """
    Handles `ValueError` exceptions by returning a plain text error response.

    Catches `ValueError` exceptions raised during request processing,
    formats the error details, and returns them in a `text/plain` content-type response with a 400
    status code.

    Parameters:
        request (Request): The HTTP request that triggered the exception.
        exc (ValueError): The ValueError instance containing error details.

    Returns:
        Response: An HTTP response object with a `text/plain` message and a 400 status code.
    """
    return Response(
        media_type=MediaType.TEXT,
        content=(
            "An error occurred for " f"{request.method} {request.url.path}: {str(exc)}"
        ),
        status_code=HTTP_400_BAD_REQUEST,
    )
