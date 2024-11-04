"""
The API routes for v2
"""

# Standard Library
from typing import Annotated

from litestar import MediaType, Request, get, post
from litestar.openapi.spec import Example
from litestar.params import Body, Parameter
from litestar.status_codes import HTTP_200_OK

# Third Party
from app.helpers.query import get_requester, query_ipv4
from app.schemas.api import APIResponseSchema, APISchema


@get("/api/me", media_type=MediaType.TEXT, sync_to_thread=False)
def my_ip(request: Request) -> str:
    """
    Returns the requester IP back to the user via the following request headers;
    `cf-connecting-ip`, `do-connecting-ip`, `x-real-ip`.

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
    A `GET` endpoint to query a port for a hostname or IP address.

    Autodetection of the requesters address is available by providing the host as `me`.
    If `me` is provided as the host, we will check the request headers for the following
    parameters; `cf-connecting-ip`, `do-connecting-ip`, `x-real-ip`.
    These headers would be automatically passed to the API via its ingress.

    **Note:** Whilst the results of this endpoints port check are not logged,
    if a host is explicitly passed, the URL will be logged to STDOUT.
    For example;
    ~~~
    "GET /foo.com/443 HTTP/1.1" 200 OK
    ~~~

    If `me` is provided as the host, requester autodetection will be used via
    the above headers. However, the requester will not be logged. For example;
    ~~~
    "GET /me/443 HTTP/1.1" 200 OK
    ~~~

    Application logs are not collected, forwarded or permanently stored.

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
