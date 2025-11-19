"""Draft order endpoints."""
from ..data_store import DataStore
from ..framework import HTTPException, Router, status

router = Router(prefix="/orders", tags=["orders"])


def _store(request) -> DataStore:
    return request.app.state.data_store


@router.post("/draft")
def create_draft_order(request):
    payload = request.json()
    if "customer_id" not in payload or "items" not in payload:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "customer_id and items are required")
    try:
        order = _store(request).create_draft_order(payload["customer_id"], payload["items"])
        return order, status.HTTP_201_CREATED
    except KeyError as exc:
        detail = "Customer not found" if exc.args and exc.args[0] == "customer not found" else "Product not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail) from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
