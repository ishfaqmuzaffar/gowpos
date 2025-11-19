"""Inventory adjustment endpoints."""
from ..data_store import DataStore
from ..framework import HTTPException, Router, status

router = Router(prefix="/inventory", tags=["inventory"])


def _store(request) -> DataStore:
    return request.app.state.data_store


@router.post("/{product_id}/adjust")
def adjust_inventory(request, product_id: str):
    payload = request.json()
    if "quantity_delta" not in payload:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "quantity_delta is required")
    try:
        quantity = _store(request).adjust_inventory(product_id, int(payload["quantity_delta"]))
        return {"product_id": product_id, "quantity": quantity}
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
