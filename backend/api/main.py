# Standard Library
import logging

# Third Party
from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI

# First Party
from app.routes import admin, v1

# Init the app
app = FastAPI(title="portchecker.io", version="1.0.0")

# Logging
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.setLevel(gunicorn_logger.level)

# Routes
app.include_router(v1.router, tags=["Routes"])
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/api/v{major}")
app.include_router(admin.router, tags=["Admin"])

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
