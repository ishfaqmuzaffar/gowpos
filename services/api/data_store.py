"""In-memory data storage for the API."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Dict, List
from uuid import uuid4


@dataclass
class Product:
    id: str
    name: str
    description: str | None = None
    price: float = 0.0
    sku: str = ""


@dataclass
class Customer:
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None


@dataclass
class OrderItem:
    product_id: str
    quantity: int


@dataclass
class DraftOrder:
    id: str
    customer_id: str
    items: List[OrderItem] = field(default_factory=list)
    status: str = "draft"


class DataStore:
    def __init__(self) -> None:
        self.products: Dict[str, Product] = {}
        self.customers: Dict[str, Customer] = {}
        self.inventory: Dict[str, int] = {}
        self.orders: Dict[str, DraftOrder] = {}

    def create_product(self, payload: dict) -> dict:
        product = Product(id=str(uuid4()), **payload)
        self.products[product.id] = product
        self.inventory.setdefault(product.id, 0)
        return asdict(product)

    def update_product(self, product_id: str, payload: dict) -> dict:
        if product_id not in self.products:
            raise KeyError("product not found")
        sanitized_payload = self._sanitize_update_payload(payload, product_id, "product")
        product = replace(self.products[product_id], **sanitized_payload)
        self.products[product_id] = product
        return asdict(product)

    def delete_product(self, product_id: str) -> None:
        if product_id not in self.products:
            raise KeyError("product not found")
        self.products.pop(product_id)
        self.inventory.pop(product_id, None)

    def list_products(self) -> list[dict]:
        return [asdict(product) for product in self.products.values()]

    def get_product(self, product_id: str) -> dict:
        if product_id not in self.products:
            raise KeyError("product not found")
        return asdict(self.products[product_id])

    def create_customer(self, payload: dict) -> dict:
        customer = Customer(id=str(uuid4()), **payload)
        self.customers[customer.id] = customer
        return asdict(customer)

    def update_customer(self, customer_id: str, payload: dict) -> dict:
        if customer_id not in self.customers:
            raise KeyError("customer not found")
        sanitized_payload = self._sanitize_update_payload(payload, customer_id, "customer")
        customer = replace(self.customers[customer_id], **sanitized_payload)
        self.customers[customer_id] = customer
        return asdict(customer)

    def list_customers(self) -> list[dict]:
        return [asdict(customer) for customer in self.customers.values()]

    def get_customer(self, customer_id: str) -> dict:
        if customer_id not in self.customers:
            raise KeyError("customer not found")
        return asdict(self.customers[customer_id])

    def adjust_inventory(self, product_id: str, delta: int) -> int:
        if product_id not in self.products:
            raise KeyError("product not found")
        current = self.inventory.get(product_id, 0)
        new_quantity = current + delta
        if new_quantity < 0:
            raise ValueError("inventory cannot be negative")
        self.inventory[product_id] = new_quantity
        return new_quantity

    def create_draft_order(self, customer_id: str, items: List[dict]) -> dict:
        if customer_id not in self.customers:
            raise KeyError("customer not found")
        validated_items = []
        for item in items:
            if item["product_id"] not in self.products:
                raise KeyError("product not found")
            if item["quantity"] <= 0:
                raise ValueError("quantity must be positive")
            validated_items.append(OrderItem(**item))
        order = DraftOrder(id=str(uuid4()), customer_id=customer_id, items=validated_items)
        self.orders[order.id] = order
        return asdict(order)

    @staticmethod
    def _sanitize_update_payload(payload: dict, entity_id: str, entity_name: str) -> dict:
        """Reject or ignore attempts to mutate immutable identifiers."""

        if "id" in payload and payload["id"] != entity_id:
            raise ValueError(f"{entity_name} id is immutable")
        # Remove the id key so dataclasses.replace won't attempt to update it
        return {key: value for key, value in payload.items() if key != "id"}
