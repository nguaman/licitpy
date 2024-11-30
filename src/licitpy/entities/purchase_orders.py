from __future__ import annotations

from typing import Iterator, List, Optional

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.services.purchase_order import PurchaseOrderServices


class PurchaseOrders:
    def __init__(
        self,
        purchase_orders: List[PurchaseOrder],
        services: Optional[PurchaseOrderServices] = None,
    ):

        self._purchase_orders = purchase_orders

        self.services = services or PurchaseOrderServices()

    @classmethod
    def from_tender(cls, purchase_orders: List[PurchaseOrder]) -> PurchaseOrders:
        return PurchaseOrders(purchase_orders)

    def limit(self, limit: int) -> PurchaseOrders:
        return PurchaseOrders(self._purchase_orders[:limit])

    def count(self) -> int:
        return len(self._purchase_orders)

    def __iter__(self) -> Iterator[PurchaseOrder]:
        return iter(self._purchase_orders)
