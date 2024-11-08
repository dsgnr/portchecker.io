"""
The custom exceptions for the API
"""

from typing import Any

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST


class JsonAPIException(HTTPException):
    """Exception for JSON HTTP error responses."""

    def __init__(
        self,
        *args: Any,
        message: str | None,
        key: str | None,
    ) -> None:
        self.status_code = HTTP_400_BAD_REQUEST
        self.detail = self.message = message
        self.key = key
        super().__init__(*args)
