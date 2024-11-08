"""
The API schemas
"""

# Standard Library
from ipaddress import IPv4Address
from typing import List, Union

# Third Party
from app.helpers.query import validate_port
from litestar.exceptions import ValidationException
from pydantic import BaseModel, Field, field_validator


class APISchema(BaseModel):
    host: Union[IPv4Address, str] = Field(
        description="The IPv4 address or hostname of the host to query",
        examples=["example.com"],
    )
    ports: List[int] = Field(
        description="An array of port numbers to query", examples=[[443]]
    )

    @field_validator("ports")
    @classmethod
    def validate_ports(cls, ports: list[int]) -> list[int]:
        for port in ports:
            if not validate_port(port):
                raise ValidationException(
                    "Only a valid port number between 1 and 65535 can be queried. "
                    f"Port {port} is not valid"
                )
        return ports


class APICheckSchema(BaseModel):
    port: int = Field(examples=[443])
    status: bool = Field(examples=[True])


class APIResponseSchema(BaseModel):
    error: bool = Field(examples=[False])
    msg: Union[str, None]
    check: List[APICheckSchema]
    host: str = Field(examples=["example.com"])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": False,
                    "msg": None,
                    "host": "1.1.1.1",
                    "check": [{"status": True, "ports": 443}],
                }
            ]
        }
    }


class APIErrorResponseSchema(BaseModel):
    error: bool = Field(description="Whether an error occurred", examples=[True])
    detail: str = Field(description="The error message")
    extra: list[dict] = Field(
        description="The parameter and error this exception relates to"
    )
