from typing import Optional

from pydantic import HttpUrl

from licitpy.downloader.purchase_order import PurchaseOrderDownloader
from licitpy.parsers.purchase_order import PurchaseOrderParser
from licitpy.types.purchase_order import Status


class PurchaseOrderServices:

    def __init__(
        self,
        downloader: Optional[PurchaseOrderDownloader] = None,
        parser: Optional[PurchaseOrderParser] = None,
    ):
        self.downloader = downloader or PurchaseOrderDownloader()
        self.parser = parser or PurchaseOrderParser()

    def get_url(self, code: str) -> HttpUrl:
        return self.parser.get_url_from_code(code)

    def get_html(self, url: HttpUrl) -> str:
        return self.downloader.get_html_from_url(url)

    def get_status(self, html: str) -> Status:
        return self.parser.get_purchase_order_status(html)

    def get_title(self, html: str) -> str:
        return self.parser.get_purchase_order_title_from_html(html)
