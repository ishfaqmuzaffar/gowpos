"""Authentication middleware for the custom framework."""
from typing import Iterable

from .config import get_settings
from .framework import Response, status


class AuthMiddleware:
    def __init__(self, exempt_paths: Iterable[str] | None = None):
        self._settings = get_settings()
        self._exempt_paths = tuple(exempt_paths or ("/health",))

    def __call__(self, request, call_next):
        if any(request.path.startswith(path) for path in self._exempt_paths):
            return call_next(request)

        expected = f"Bearer {self._settings.auth_token}"
        provided = request.headers.get("authorization")

        if provided != expected:
            return Response({"detail": "Unauthorized"}, status.HTTP_401_UNAUTHORIZED)

        return call_next(request)
