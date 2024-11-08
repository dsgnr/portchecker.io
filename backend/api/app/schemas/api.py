"""
The API schemas
"""

from typing import Annotated, Union

from annotated_types import Ge, Le, MaxLen, MinLen
from litestar.openapi.spec import Example
from litestar.params import Parameter
from pydantic import BaseModel, Field

HostAnnotation = Annotated[
    str,
    Parameter(
        description="The IPv4 address or hostname of the host to query",
        examples=[Example(value="example.com"), Example(value="1.1.1.1")],
        min_length=1,
        max_length=253,
    ),
    MinLen(1),
    MaxLen(253),
]

PortAnnotation = Annotated[
    int,
    Parameter(
        description="The port number to query",
        examples=[Example(value=443)],
        ge=1,
        le=65535,
    ),
    Ge(1),
    Le(65535),
]

PortCheckAnnotation = Annotated[
    bool,
    Parameter(
        description="Whether the port was connectable",
        examples=[Example(value=True)],
    ),
]

RequesterAnnotation = Annotated[
    str,
    Parameter(
        description="The IP address of the requester",
        examples=[Example(value="1.1.1.1")],
    ),
]


class APISchema(BaseModel):
    host: HostAnnotation
    ports: list[PortAnnotation]


class APICheckSchema(BaseModel):
    port: PortAnnotation
    status: PortCheckAnnotation


class APIResponseSchema(BaseModel):
    error: bool = Field(
        description="Whether an error occurred during the check", examples=[False]
    )
    msg: Union[str, None]
    check: list[APICheckSchema]
    host: HostAnnotation


class APIErrorResponseSchema(BaseModel):
    error: bool = Field(description="Whether an error occurred", examples=[True])
    detail: str = Field(description="The error message")
    extra: list[dict] = Field(
        description="The parameter and error this exception relates to"
    )
