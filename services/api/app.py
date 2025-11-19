"""Application factory for the custom framework."""
from .auth import AuthMiddleware
from .config import get_settings
from .data_store import DataStore
from .framework import Application
from .logging_config import configure_logging
from .routers import customers, health, inventory, orders, products


def create_app() -> Application:
    configure_logging()
    settings = get_settings()

    app = Application(title=settings.app_name)
    app.state.data_store = DataStore()
    app.add_middleware(AuthMiddleware, exempt_paths=("/health",))

    app.include_router(health.router)
    app.include_router(products.router)
    app.include_router(inventory.router)
    app.include_router(customers.router)
    app.include_router(orders.router)
    return app


app = create_app()
