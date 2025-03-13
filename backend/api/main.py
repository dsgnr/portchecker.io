"""
The portchecker.io App
"""

import pathlib

import tomli
from litestar import Litestar
from litestar.exceptions import ValidationException
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from app.helpers.exceptions import JsonAPIException
from app.helpers.handlers import (
    json_api_exception_handler,
    text_value_error_exception_handler,
    validation_exception_handler,
)
from app.routes.admin import health
from app.routes.v1 import v1_query_post
from app.routes.v2 import get_port_check, my_ip, query_post


def _get_project_meta():
    """Parse the pyproject.toml file to retrieve project information"""
    with open(
        f"{pathlib.Path(__file__).parent.resolve().parent}/pyproject.toml", mode="rb"
    ) as pyproject:
        return tomli.load(pyproject)["tool"]["poetry"]


project_meta = _get_project_meta()


prometheus_config = PrometheusConfig(
    app_name="api",
    prefix=project_meta["name"].split(".")[0],
    group_path=True,
    labels={
        "version": project_meta["version"],
    },
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5],
)

app = Litestar(
    route_handlers=[
        PrometheusController,
        my_ip,
        query_post,
        get_port_check,
        v1_query_post,
        health,
    ],
    middleware=[prometheus_config.middleware],
    openapi_config=OpenAPIConfig(
        title=project_meta["name"],
        description=project_meta["description"],
        version=project_meta["version"],
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
