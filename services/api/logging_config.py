"""Logging configuration utilities."""
import logging
import logging.config
from typing import Any, Dict


LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "loggers": {
        "gowpos": {"handlers": ["default"], "level": "INFO"},
    },
}


def configure_logging() -> None:
    """Apply the dictionary-based logging configuration."""
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).debug("Logging has been configured")
