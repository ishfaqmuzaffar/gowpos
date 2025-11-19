"""Tests for inventory adjustments."""
from services.api.framework import status


def test_inventory_adjustment(client, auth_headers):
    product_payload = {"name": "Case", "description": "", "price": 19.0, "sku": "SKU-CASE"}
    product_id = client.post("/products", json=product_payload, headers=auth_headers).json()["id"]

    adjust_resp = client.post(
        f"/inventory/{product_id}/adjust",
        json={"quantity_delta": 10},
        headers=auth_headers,
    )
    assert adjust_resp.status_code == status.HTTP_200_OK
    assert adjust_resp.json()["quantity"] == 10

    adjust_resp = client.post(
        f"/inventory/{product_id}/adjust",
        json={"quantity_delta": -5},
        headers=auth_headers,
    )
    assert adjust_resp.status_code == status.HTTP_200_OK
    assert adjust_resp.json()["quantity"] == 5

    bad_resp = client.post(
        f"/inventory/{product_id}/adjust",
        json={"quantity_delta": -10},
        headers=auth_headers,
    )
    assert bad_resp.status_code == status.HTTP_400_BAD_REQUEST
