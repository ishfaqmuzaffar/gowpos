"""Tests for customer account endpoints."""
from services.api.framework import status


def test_customer_lifecycle(client, auth_headers):
    payload = {
        "first_name": "Jamie",
        "last_name": "Doe",
        "email": "jamie@example.com",
        "phone": "555-1212",
    }
    create_resp = client.post("/customers", json=payload, headers=auth_headers)
    assert create_resp.status_code == status.HTTP_201_CREATED
    customer = create_resp.json()

    list_resp = client.get("/customers", headers=auth_headers)
    assert list_resp.status_code == status.HTTP_200_OK
    assert len(list_resp.json()) == 1

    update_resp = client.put(
        f"/customers/{customer['id']}",
        json={"phone": "555-2323"},
        headers=auth_headers,
    )
    assert update_resp.status_code == status.HTTP_200_OK
    assert update_resp.json()["phone"] == "555-2323"
