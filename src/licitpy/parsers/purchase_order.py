from pydantic import HttpUrl

from licitpy.parsers.base import BaseParser
from licitpy.types.purchase_order import Status


class PurchaseOrderParser(BaseParser):

    def get_url_from_code(self, code: str) -> HttpUrl:
        url = f"https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC={code}"
        return HttpUrl(url)

    def get_purchase_order_status(self, html: str) -> Status:
        status = self.get_text_by_element_id(html, "lblStatusPOValue")
        return Status(status)

    def get_purchase_order_title_from_html(self, html: str) -> str:
        return self.get_text_by_element_id(html, "lblNamePOValue")
