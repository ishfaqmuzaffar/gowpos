"""Tests for product CRUD endpoints."""
from services.api.framework import status


def test_product_crud_flow(client, auth_headers):
    payload = {"name": "Phone", "description": "Flagship", "price": 899.0, "sku": "SKU-1"}
    create_resp = client.post("/products", json=payload, headers=auth_headers)
    assert create_resp.status_code == status.HTTP_201_CREATED
    product = create_resp.json()

    list_resp = client.get("/products", headers=auth_headers)
    assert list_resp.status_code == status.HTTP_200_OK
    assert len(list_resp.json()) == 1

    detail_resp = client.get(f"/products/{product['id']}", headers=auth_headers)
    assert detail_resp.status_code == status.HTTP_200_OK
    assert detail_resp.json()["name"] == "Phone"

    update_resp = client.put(
        f"/products/{product['id']}",
        json={"price": 799.0},
        headers=auth_headers,
    )
    assert update_resp.status_code == status.HTTP_200_OK
    assert update_resp.json()["price"] == 799.0

    delete_resp = client.delete(f"/products/{product['id']}", headers=auth_headers)
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    list_resp = client.get("/products", headers=auth_headers)
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.json() == []
