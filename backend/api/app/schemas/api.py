"""
The API schemas
"""

# Standard Library
from ipaddress import IPv4Address
from typing import List, Union

from litestar.exceptions import ValidationException
from pydantic import BaseModel, Field, field_validator

# Third Party
from app.helpers.query import (
    is_address_valid,
    is_ip_address,
    is_valid_hostname,
    validate_port,
)


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

    @field_validator("host")
    @classmethod
    def validate_host(cls, host: str) -> str:
        is_ip = is_ip_address(host)
        ip_version = 4
        try:
            if is_ip:
                ip_version = is_address_valid(host)
            else:
                is_valid_hostname(host)
        except Exception as ex:
            raise ValueError(ex)

        if ip_version == 6:
            raise ValueError("IPv6 is not currently supported")
        return host


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
