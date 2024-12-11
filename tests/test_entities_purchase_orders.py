from typing import List

import pytest

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.purchase_orders import PurchaseOrders


@pytest.fixture
def mock_purchase_orders() -> List[str]:
    """Return a list of mock purchase order codes."""
    return [
        "750301-54-L124",
        "2405-120-SE10",
        "2405-121-SE10",
        "2404-2281-SE10",
        "2404-1231-SE11",
    ]


def test_purchase_orders_from_tender(mock_purchase_orders: List[str]) -> None:
    """Test the creation of a PurchaseOrders instance from a list of purchase order codes."""
    purchase_orders = PurchaseOrders.from_tender(mock_purchase_orders)

    assert isinstance(purchase_orders, PurchaseOrders)
    assert purchase_orders.count() == len(mock_purchase_orders)


def test_purchase_orders_limit(mock_purchase_orders: List[PurchaseOrder]) -> None:
    """Test the limit method of the PurchaseOrders entity."""

    purchase_orders = PurchaseOrders(mock_purchase_orders)
    limited_purchase_orders = purchase_orders.limit(3)

    assert isinstance(limited_purchase_orders, PurchaseOrders)
    assert limited_purchase_orders.count() == 3
    assert limited_purchase_orders._purchase_orders == mock_purchase_orders[:3]


def test_purchase_orders_count(mock_purchase_orders: List[PurchaseOrder]) -> None:
    """Test the count method of the PurchaseOrders entity."""
    purchase_orders = PurchaseOrders(mock_purchase_orders)
    assert purchase_orders.count() == len(mock_purchase_orders)


def test_purchase_orders_iteration(mock_purchase_orders: List[PurchaseOrder]) -> None:
    """Test the iteration of the PurchaseOrders entity."""
    purchase_orders = PurchaseOrders(mock_purchase_orders)
    for po, expected_po in zip(purchase_orders, mock_purchase_orders):
        assert po == expected_po
