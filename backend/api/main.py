# Third Party
from litestar import Litestar
from litestar.exceptions import ValidationException
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin

from app.helpers.exceptions import JsonAPIException
from app.helpers.handlers import (
    json_api_exception_handler,
    text_value_error_exception_handler,
    validation_exception_handler,
)
from app.routes.admin import health
from app.routes.v1 import v1_query_post
from app.routes.v2 import get_port_check, my_ip, query_post

app = Litestar(
    route_handlers=[my_ip, query_post, get_port_check, v1_query_post, health],
    openapi_config=OpenAPIConfig(
        title="portchecker.io",
        description=(
            "portchecker.io is an open-source API for checking port \
            availability on specified hostnames or IP addresses. \
            Ideal for developers and network admins, it helps troubleshoot network \
            setups, validate firewall rules, and assess potential access points."
        ),
        version="3.0.0",
        render_plugins=[ScalarRenderPlugin()],
        path="/docs",
        use_handler_docstrings=True,
    ),
    exception_handlers={
        ValidationException: validation_exception_handler,
        JsonAPIException: json_api_exception_handler,
        ValueError: text_value_error_exception_handler,
    },
)

if __name__ == "__main__":
    # Third Party
    import uvicorn

    uvicorn.run(app)
