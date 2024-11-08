from litestar import MediaType, Request, Response
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from app.helpers.exceptions import JsonAPIException
from app.schemas.api import APIErrorResponseSchema


def validation_exception_handler(
    request: Request, exc: ValidationException
) -> APIErrorResponseSchema:
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
    return Response(
        media_type=MediaType.TEXT,
        content=(
            "An error occurred for " f"{request.method} {request.url.path}: {str(exc)}"
        ),
        status_code=HTTP_400_BAD_REQUEST,
    )
