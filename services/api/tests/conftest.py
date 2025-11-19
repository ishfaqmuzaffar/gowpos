"""Test fixtures for the API service."""
import pytest

from services.api.app import create_app
from services.api.framework import TestClient


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    return {"authorization": "Bearer secret-token"}
