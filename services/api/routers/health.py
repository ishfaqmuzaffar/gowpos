"""Health check endpoint using the custom framework."""
from ..config import get_settings
from ..framework import Router

router = Router(tags=["health"])


@router.get("/health")
def health(_request):
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "environment": settings.environment}
