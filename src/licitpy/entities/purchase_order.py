from __future__ import annotations

from typing import Optional

from pydantic import HttpUrl

from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.types.purchase_order import Status


class PurchaseOrder:

    def __init__(
        self,
        code: str,
        services: Optional[PurchaseOrderServices] = None,
    ):

        self.code: str = code
        self._url: Optional[HttpUrl] = None
        self._html: Optional[str] = None
        self._status: Optional[Status] = None
        self._title: Optional[str] = None
        self.services = services or PurchaseOrderServices()

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.code)
        return self._url

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def status(self) -> Status:
        if self._status is None:
            self._status = self.services.get_status(self.html)
        return self._status

    @property
    def title(self) -> str:
        if self._title is None:
            self._title = self.services.get_title(self.html)
        return self._title

    @classmethod
    def create(cls, code: str) -> PurchaseOrder:
        return cls(code)
