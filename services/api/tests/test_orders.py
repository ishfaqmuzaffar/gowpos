"""Tests for draft order endpoints."""
from services.api.framework import status


def test_create_draft_order(client, auth_headers):
    customer = client.post(
        "/customers",
        json={"first_name": "Kai", "last_name": "Smith", "email": "kai@example.com"},
        headers=auth_headers,
    ).json()

    product = client.post(
        "/products",
        json={"name": "Tablet", "price": 499.0, "sku": "SKU-TAB"},
        headers=auth_headers,
    ).json()

    order_resp = client.post(
        "/orders/draft",
        json={
            "customer_id": customer["id"],
            "items": [{"product_id": product["id"], "quantity": 2}],
        },
        headers=auth_headers,
    )

    assert order_resp.status_code == status.HTTP_201_CREATED
    order = order_resp.json()
    assert order["status"] == "draft"
    assert order["items"][0]["product_id"] == product["id"]


def test_order_requires_existing_entities(client, auth_headers):
    response = client.post(
        "/orders/draft",
        json={"customer_id": "missing", "items": []},
        headers=auth_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
