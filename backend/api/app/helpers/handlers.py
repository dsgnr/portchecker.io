# Standard Library
import json

# Third Party
from litestar import MediaType, Request, Response


def value_error_handler(request: Request, exc: ValueError) -> Response:
    try:
        ret = json.loads(exc.json())
    except Exception:
        ret = str(exc)
    return Response(
        media_type=MediaType.JSON,
        content={"error": True, "detail": ret},
        status_code=400,
    )
