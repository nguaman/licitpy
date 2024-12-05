from typing import Union

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.sources import API, Local


class PurchaseOrdersClient:
    def __init__(self, source: Union[API, Local]) -> None:
        self.source = source

    def from_code(self, code: str) -> PurchaseOrder:
        return self.source.get_purchase_order(code)
