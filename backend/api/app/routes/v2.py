"""
The API routes for v2
"""

# Standard Library
from typing import Annotated

# Third Party
from app.helpers.query import get_requester, query_ipv4
from app.schemas.api import APIResponseSchema, APISchema, RequesterAnnotation
from litestar import MediaType, Request, get, post
from litestar.openapi.spec import Example
from litestar.params import Body, Parameter
from litestar.status_codes import HTTP_200_OK


@get("/api/me", media_type=MediaType.TEXT, sync_to_thread=False)
def my_ip(request: Request) -> RequesterAnnotation:
    """
    Returns the requester IP.

    Auto-detects the requester IP address using the following headers:
       - `cf-connecting-ip`
       - `do-connecting-ip`
       - `x-real-ip`

    These headers are typically added by the application ingress router (ie, Nginx)
    and so does not need to be explicitly provided.

    The live production environment version of this app lives on
    DigitalOceans App Platform, and so the `do-connecting-ip` will be leveraged.

    *Note:* The responses from this endpoint are *not* logged in production.
    """
    return get_requester(request)


@get("/api/{host:str}/{port:int}", media_type=MediaType.TEXT, sync_to_thread=False)
def get_port_check(
    request: Request,
    host: str = Parameter(examples=[Example(value="example.com")]),
    port: int = Parameter(examples=[Example(value=443)]),
) -> str:
    """
    A `GET` endpoint to check the status of a specific port on a given
    resolvable hostname or IPv4 address.

    Use `me` as the host to auto-detect the requester IP address based
    on the following headers:
       - `cf-connecting-ip`
       - `do-connecting-ip`
       - `x-real-ip`

    These headers are typically added by the application ingress router (ie, Nginx)
    and so does not need to be explicitly provided.

    **Note:** Whilst the results of this endpoints port check are not logged,
    if a host is explicitly passed, the URL will be logged to `STDOUT`.
    For example;
    ~~~
    "GET /foo.com/443 HTTP/1.1" 200 OK
    ~~~

    If `me` is provided as the host, requester auto-detection will be used using
    the above headers. However, the requester will not be logged. For example;
    ~~~
    "GET /me/443 HTTP/1.1" 200 OK
    ~~~

    Application logs are not forwarded or permanently stored.
    """
    host = get_requester(request) if host == "me" else host
    APISchema(host=host, ports=[port])
    return str(query_ipv4(host, [port])[0].get("status"))


@post(
    "/api/query",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=False,
)
def query_post(
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
