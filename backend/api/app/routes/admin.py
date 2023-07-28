"""
The API routes for admin
"""
# Third Party
from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/healthz")
def health() -> bool:
    """
    Basic health check to ensure API is responding. Returns `True`.
    """
    return True
