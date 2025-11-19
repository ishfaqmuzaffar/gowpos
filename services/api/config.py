"""Application configuration management without external deps."""
from dataclasses import dataclass
import os
from functools import lru_cache


@dataclass(frozen=True)
class AppSettings:
    app_name: str = "gowpos API"
    environment: str = os.getenv("APP_ENVIRONMENT", "development")
    auth_token: str = os.getenv("APP_AUTH_TOKEN", "secret-token")


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
