"""
The API routes for admin
"""

from litestar import get


@get("/healthz", sync_to_thread=False)
def health() -> bool:
    """
    Basic health check to ensure API is responding. Returns `True`.
    """
    return True
