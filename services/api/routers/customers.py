"""Customer account endpoints."""
from ..data_store import DataStore
from ..framework import HTTPException, Router, status

router = Router(prefix="/customers", tags=["customers"])


def _store(request) -> DataStore:
    return request.app.state.data_store


def _validate_required(payload: dict) -> None:
    missing = [field for field in ("first_name", "last_name", "email") if field not in payload]
    if missing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Missing fields: {', '.join(missing)}")


@router.get("")
def list_customers(request):
    return _store(request).list_customers()


@router.post("")
def create_customer(request):
    payload = request.json()
    _validate_required(payload)
    return _store(request).create_customer(payload), status.HTTP_201_CREATED


@router.get("/{customer_id}")
def get_customer(request, customer_id: str):
    try:
        return _store(request).get_customer(customer_id)
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found") from exc


@router.put("/{customer_id}")
def update_customer(request, customer_id: str):
    payload = {k: v for k, v in request.json().items() if v is not None}
    if not payload:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields to update")
    try:
        return _store(request).update_customer(customer_id, payload)
    except KeyError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found") from exc
