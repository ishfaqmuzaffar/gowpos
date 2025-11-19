"""Product CRUD endpoints for the custom framework."""
from ..data_store import DataStore
from ..framework import HTTPException, Router, status

router = Router(prefix="/products", tags=["products"])


def _store(request) -> DataStore:
    return request.app.state.data_store


def _validate_required(payload: dict, fields: list[str]) -> None:
    missing = [field for field in fields if field not in payload]
    if missing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Missing fields: {', '.join(missing)}")


@router.get("")
def list_products(request):
    return _store(request).list_products()


@router.post("")
def create_product(request):
    payload = request.json()
    _validate_required(payload, ["name", "price", "sku"])
    return _store(request).create_product(payload), status.HTTP_201_CREATED


@router.get("/{product_id}")
def get_product(request, product_id: str):
    try:
        return _store(request).get_product(product_id)
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc


@router.put("/{product_id}")
def update_product(request, product_id: str):
    payload = {k: v for k, v in request.json().items() if v is not None}
    if not payload:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields to update")
    try:
        return _store(request).update_product(product_id, payload)
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc


@router.delete("/{product_id}")
def delete_product(request, product_id: str):
    try:
        _store(request).delete_product(product_id)
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found") from exc
    return None, status.HTTP_204_NO_CONTENT
