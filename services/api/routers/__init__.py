"""API routers package."""
from . import customers, health, inventory, orders, products  # noqa: F401

__all__ = [
    "customers",
    "health",
    "inventory",
    "orders",
    "products",
]
