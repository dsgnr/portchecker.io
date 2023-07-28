"""
The API routes for V1
"""
# Third Party
from app.helpers.query import (
    is_address_valid,
    is_ip_address,
    is_valid_hostname,
    query_ipv4,
    validate_port,
)
from app.schemas.api import APIResponseSchema, APISchema
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi_versioning import version

router = APIRouter()


@router.post("/query", response_model=APIResponseSchema)
@version(1)
def query_host(body: APISchema) -> APIResponseSchema:
    ret = {"error": False, "host": None, "check": [], "msg": None}

    try:
        ret["host"] = body.host
    except Exception:
        ret["error"] = True
        ret["msg"] = "A host must be defined"
        return JSONResponse(status_code=400, content=ret)

    try:
        ports = body.ports
    except Exception:
        ret["error"] = True
        ret["msg"] = "A list of ports must be defined"
        return JSONResponse(status_code=400, content=ret)

    try:
        for port in ports:
            if not validate_port(port):
                raise ValueError(
                    "Only a valid port number between 1 and 65535 can be queried. "
                    f"Port {port} is not valid"
                )
    except Exception as ex:
        ret["error"] = True
        ret["msg"] = str(ex)
        return JSONResponse(status_code=400, content=ret)

    is_ip = is_ip_address(ret["host"])
    ip_version = 4
    try:
        if is_ip:
            ip_version = is_address_valid(ret["host"])
        else:
            is_valid_hostname(ret["host"])
    except Exception as ex:
        ret["error"] = True
        ret["msg"] = str(ex)
        return JSONResponse(status_code=400, content=ret)

    if ip_version == 6:
        ret["error"] = True
        ret["msg"] = "IPv6 is not currently supported"
        return JSONResponse(status_code=400, content=ret)

    ret["check"] = query_ipv4(ret["host"], ports)
    return JSONResponse(status_code=200, content=ret)
