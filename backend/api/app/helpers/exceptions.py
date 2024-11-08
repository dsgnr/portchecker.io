from typing import Any, Union

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST


class JsonAPIException(HTTPException):
    def __init__(
        self,
        *args: Any,
        message: Union[str, None] = None,
        key: Union[str, None] = None,
    ) -> None:
        self.status_code = HTTP_400_BAD_REQUEST
        self.detail = self.message = message
        self.key = key
        super().__init__(*args)
