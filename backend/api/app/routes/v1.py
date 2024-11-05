"""
The API routes for V1
"""

# Standard Library
from typing import Annotated

from litestar import post
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

# Third Party
from app.helpers.query import query_ipv4
from app.schemas.api import APIResponseSchema, APISchema


@post("/api/v1/query", status_code=HTTP_200_OK, sync_to_thread=False, deprecated=True)
def v1_query_post(
    data: Annotated[
        APISchema,
        Body(title="Query a hostname or IP", description="Query a hostname or IP"),
    ],
) -> APIResponseSchema:
    """
    A `POST` endpoint to query a range of ports for a hostname or IP address.

    This endpoint will accept an IPv4 IP address or resolveable hostname,
    and iterate an array of port numbers provided.

    The port check will timeout after 1 second.

    **NOTE:** The request body for this endpoint is not logged.
    ~~~
    "POST / HTTP/1.1" 200 OK
    ~~~
    """
    return APIResponseSchema(
        msg=None,
        error=False,
        host=data.host,
        check=query_ipv4(data.host, data.ports),
    )
