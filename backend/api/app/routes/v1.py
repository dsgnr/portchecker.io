"""
The API routes for V1
"""

# Standard Library
from typing import Annotated

# Third Party
from app.helpers.query import query_ipv4
from app.schemas.api import APIResponseSchema, APISchema
from litestar import MediaType, post
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK


@post(
    "/api/v1/query",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=False,
    deprecated=True,
)
def v1_query_post(
    data: Annotated[
        APISchema,
        Body(
            title="Query a resolvable hostname or IPv4 address",
            description="Query a resolvable hostname or IPv4 address",
        ),
    ],
) -> APIResponseSchema:
    """
    A `POST` endpoint to query the status of multiple ports on a given hostname
    or IP address.

    This endpoint accepts a JSON payload containing either an IPv4 address
    or a resolvable hostname, along with an array of port numbers to be checked.
    For each port in the array, the endpoint performs a connectivity check with a
    timeout of 1 second per port.

    **NOTE:** The request body for this endpoint is not logged.
    ~~~
    "POST /api/query HTTP/1.1" 200 OK
    ~~~
    """
    return APIResponseSchema(
        msg=None,
        error=False,
        host=data.host,
        check=query_ipv4(data.host, data.ports),
    )
