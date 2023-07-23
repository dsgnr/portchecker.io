"""
The API schema for V1
"""
# Standard Library
from ipaddress import IPv4Address
from typing import List, Union

# Third Party
from pydantic import BaseModel, Field


class APISchema(BaseModel):
    host: Union[IPv4Address, str] = Field(description="The IPv4 address of the host to query")
    ports: List[int]

    model_config = {"json_schema_extra": {"examples": [{"host": "1.1.1.1", "ports": [444]}]}}


class APICheckSchema(BaseModel):
    port: int
    status: bool


class APIResponseSchema(BaseModel):
    error: bool
    msg: Union[str, None]
    check: List[APICheckSchema]
    host: str

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
